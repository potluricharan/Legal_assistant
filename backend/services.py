import os
import hashlib
import numpy as np
from google import genai
from PyPDF2 import PdfReader
from database import db
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Using v1beta to ensure support for text-embedding-004 and the latest Gemini 2.5 features
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'api_version': 'v1beta'}
)

def calculate_file_hash(path):
    """
    Generates a unique MD5 hash fingerprint for the file.
    Used to detect if the same document has been uploaded before.
    """
    hasher = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            # Read in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Hash Calculation Error: {e}")
        return None

def get_embedding(text):
    """
    Converts raw text into a 768-dimensional numerical vector.
    This allows the 'Legal Vault' to perform semantic (meaning-based) searches.
    """
    try:
        # Capped at 3000 tokens as embeddings have shorter context windows
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=text[:3000]
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"Embedding Generation Error: {e}")
        return []

def extract_text_from_pdf(path):
    """Extracts all text content from an uploaded PDF file."""
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        print(f"PDF Text Extraction Error: {e}")
        return ""

def analyze_case_with_gemini(pdf_path):
    """
    Uses Gemini 2.5 Flash to extract a legal summary, 
    arguments, and investigation gaps from the case.
    """
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        return {"summary": "Error: Scanned PDF detected or no readable text found."}

    # Capped at 12,000 characters to ensure fast response and token safety
    safe_text = text[:12000] 
    
    prompt = (
        f"You are a Senior Legal Analyst. Analyze this court document and provide:\n"
        f"1. A concise executive summary.\n"
        f"2. Key legal arguments presented.\n"
        f"3. Potential procedural or investigation gaps found in the case.\n\n"
        f"TEXT CONTENT:\n{safe_text}"
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return {"summary": response.text}
    except Exception as e:
        return {"summary": f"AI Generation Error: {str(e)}"}

def analyze_with_history(case_id, user_query):
    """
    Core Chat Logic: Retrieves previous conversations and the case summary
    from Firestore to provide context-aware legal advice.
    """
    try:
        case_ref = db.collection('cases').document(case_id)
        case_doc = case_ref.get()
        
        if not case_doc.exists:
            return "System Error: The selected Case ID was not found in the vault."
            
        case_data = case_doc.to_dict()
        
        # Retrieve the 5 most recent chat messages to maintain context
        history_ref = case_ref.collection('case_history').order_by('timestamp', direction='DESCENDING').limit(5).stream()
        
        history_text = ""
        history_list = list(history_ref)
        # Reverse history to maintain chronological order for the model
        for doc in reversed(history_list):
            item = doc.to_dict()
            history_text += f"\n{item.get('content')}"

        full_prompt = (
            f"Role: Expert AI Legal Counsel\n"
            f"Context: {case_data.get('current_summary', 'No summary available.')}\n"
            f"Recent Chat History: {history_text}\n"
            f"User Query: {user_query}\n\n"
            f"Instructions: Answer the query based on the case facts and legal principles. "
            f"Be professional and maintain continuity with previous answers."
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=full_prompt
        )
        
        # Log this interaction to Firestore for future context
        case_ref.collection('case_history').add({
            "type": "CHAT", 
            "content": f"User: {user_query} | AI: {response.text}", 
            "timestamp": datetime.now(timezone.utc)
        })
        
        return response.text
    except Exception as e:
        return f"Service Error in Chat: {str(e)}"