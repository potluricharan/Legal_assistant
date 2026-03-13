import os
import json
from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app)

# --- FIREBASE INITIALIZATION ---
def init_firebase():
    if not firebase_admin._apps:
        # Check for local key file first
        if os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        else:
            # For Render: Use Environment Variable
            sa_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
            if sa_json:
                cred = credentials.Certificate(json.loads(sa_json))
                firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

# --- AUTO-SEEDER ---
def seed_data():
    # Only seed if the collection is empty
    docs = db.collection('lawyer_portfolios').limit(1).get()
    if not docs:
        print("Seeding initial mock data...")
        with open('mock_data/lawyer.json') as f:
            db.collection('lawyer_portfolios').add(json.load(f))
        print("Database seeded successfully!")

@app.route('/')
def home():
    seed_data()
    return jsonify({"status": "active", "database": "connected"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)