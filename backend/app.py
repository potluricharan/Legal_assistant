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
        if os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        else:
            # For Render deployment
            sa_data = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT'))
            cred = credentials.Certificate(sa_data)
            firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_db()

# 2. Automated Seeder
def auto_seed():
    # Mapping: "File Name" -> "Firestore Collection Name"
    seeds = {
        "mock_data/lawyer.json": "lawyers",
        "mock_data/background.json": "background_checks",
        "mock_data/precedent.json": "judgments",
        "mock_data/mobile.json": "evidence"
    }

    for file_path, collection in seeds.items():
        # Only seed if collection is empty to avoid duplicates
        docs = db.collection(collection).limit(1).get()
        if not docs and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                db.collection(collection).add(data)
                print(f"✅ Seeded {collection} from {file_path}")

@app.route('/')
def home():
    auto_seed() # Runs check on every refresh
    return jsonify({"status": "online", "message": "Legal AI Backend Seeded"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)