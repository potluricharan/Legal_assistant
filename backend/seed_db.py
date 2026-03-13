import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
import time
import os

# 1. Connect to Firebase (Make sure serviceAccountKey.json is in the same folder)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. Connect to Gemini (Replace with your actual key if not in env)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_ACTUAL_API_KEY_HERE"))

# 3. Read the Data
print("Loading justice.csv...")
df = pd.read_csv("justice.csv")
df = df.dropna(subset=['facts'])

# HACKATHON TIP: We only upload the first 50 cases to save time and avoid API limits.
# You can change this number later if you want the full database.
df = df.head(50) 

print(f"Uploading {len(df)} cases to Firebase Legal Vault...")

for index, row in df.iterrows():
    title = str(row.get('name', f"Case {index}"))
    text = str(row.get('facts', ''))
    
    try:
        # Turn the case facts into a mathematical vector
        embedding = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )['embedding']
        
        # Push to Firebase Firestore
        db.collection('legal_vault').add({
            'title': title,
            'text': text,
            'embedding': embedding,
            'issue_area': str(row.get('issue_area', 'General'))
        })
        
        print(f"✅ Uploaded: {title}")
        time.sleep(1) # 1-second delay to prevent Gemini API from blocking us
        
    except Exception as e:
        print(f"❌ Failed to upload {title}: {e}")

print("🎉 Database Seed Complete! Your Legal Vault is ready.")