import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

CERT_PATH = "serviceAccountKey.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(CERT_PATH)
    # Initializing without storage bucket to keep it 100% free/no-card
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_firebase_db():
    return db