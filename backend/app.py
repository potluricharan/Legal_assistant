import os
import json
from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app)

# --- FIREBASE INITIALIZATION ---
def init_db():
    if not firebase_admin._apps:
        # Check for local key (on your laptop) or Render environment variable
        if os.path.exists("backend/serviceAccountKey.json"):
            cred = credentials.Certificate("backend/serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        elif os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        else:
            # This part runs on RENDER
            sa_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
            if sa_json:
                cred = credentials.Certificate(json.loads(sa_json))
                firebase_admin.initialize_app(cred)
            else:
                print("CRITICAL: No Firebase credentials found!")
    return firestore.client()

try:
    db = init_db()
except Exception as e:
    print(f"Firebase Init Error: {e}")
    db = None

# --- AUTOMATED DATA SEEDER ---
def auto_seed():
    if not db: return "Database not connected"
    
    # Check if 'cases' collection is empty
    docs = db.collection('cases').limit(1).get()
    if not docs:
        print("Empty database. Seeding data...")
        
        # 1. Seed Case Data
        case_data = {
            "caseId": "CASE-2026-0042",
            "title": "State vs. Sharma (Financial Fraud)",
            "status": "Active",
            "filingDate": "2026-02-15"
        }
        db.collection('cases').add(case_data)
        
        # 2. Seed Lawyer Data
        lawyer_data = {
            "fullName": "Vikram Desai",
            "barId": "MAH/1024/2012",
            "status": "Verified"
        }
        db.collection('lawyers').add(lawyer_data)
        
        return "Database Successfully Seeded!"
    return "Database already has data."

@app.route('/')
def home():
    try:
        status = auto_seed()
        return jsonify({
            "status": "online",
            "database_status": status,
            "message": "Legal AI Backend is LIVE"
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

if __name__ == "__main__":
    # Render uses port 10000 by default
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)