import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# Build absolute path to key file regardless of execution directory
CERT_PATH = os.path.join(os.path.dirname(__file__), "serviceAccountKey (2).json")

if not firebase_admin._apps:
    cred = credentials.Certificate(CERT_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_firebase_db():
    return db