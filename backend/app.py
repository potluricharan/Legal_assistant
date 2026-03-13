import os
import json
from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app)

# 1. Initialize Firebase
def init_db():
    if not firebase_admin._apps:
        # Check for local key file (for your laptop)
        if os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        else:
            # For Render deployment (using Environment Variable)
            sa_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
            if sa_json:
                cred = credentials.Certificate(json.loads(sa_json))
                firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_db()

# 2. Automated Seeder logic
def auto_seed():
    # Only seed if 'cases' doesn't exist yet
    docs = db.collection('cases').limit(1).get()
    if not docs:
        print("Empty database found. Planting seeds...")
        # Path must match your backend/mock_data folder
        case_data = {
            "caseId": "CASE-2026-0042",
            "title": "State vs. Sharma",
            "status": "Active"
        }
        db.collection('cases').add(case_data)
        print("✅ Data pushed to Firebase!")

@app.route('/')
def home():
    auto_seed() # Runs the check
    return jsonify({
        "status": "online", 
        "message": "Legal AI Backend Seeded & Ready!"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)