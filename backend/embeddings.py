import os
import numpy as np
from google import genai
from database import db
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text):
    """Generates a vector using the text-embedding-004 model."""
    # Truncate text to avoid token limits just in case
    safe_text = str(text)[:3000]
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=safe_text
    )
    # Access the embedding values properly from the GenAI SDK
    return response.embeddings[0].values

def semantic_search(query):
    """Queries Firestore to find the top 3 similar cases."""
    query_vec = get_embedding(query)
    
    # Fetch all cases from the Firebase 'cases' collection
    cases_ref = db.collection('cases').stream()
    
    results = []
    for doc in cases_ref:
        case = doc.to_dict()
        
        # Check if the case has a summary to embed
        summary = case.get('current_summary', '')
        if not summary:
            continue
            
        case_vec = get_embedding(summary)
        
        # Calculate Cosine Similarity
        similarity = np.dot(query_vec, case_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(case_vec))
        
        results.append((similarity, {
            "filename": case.get('filename', 'Unknown'),
            "id": doc.id,
            "summary": summary[:200] + "..." # Return a snippet for the frontend
        }))
    
    # Sort by highest similarity and return top 3
    results.sort(key=lambda x: x[0], reverse=True)
    return [res[1] for res in results[:3]]