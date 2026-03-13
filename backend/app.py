import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

def init_db():
    if not firebase_admin._apps:
        # Check for Render environment variable first
        sa_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
        if sa_json:
            cred = credentials.Certificate(json.loads(sa_json))
            firebase_admin.initialize_app(cred)
        # Fallback to local keys for Person 2's testing
        elif os.path.exists("backend/serviceAccountKey.json"):
            cred = credentials.Certificate("backend/serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        else:
            print("CRITICAL: No Firebase credentials found!")
            return None
    return firestore.client()

try:
    db = init_db()
except Exception as e:
    print(f"Firebase Init Error: {e}")
    db = None

# --- AI ANALYSIS ROUTE ---
@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    data = request.json
    text_content = data.get("text")
    
    if not text_content:
        return jsonify({"error": "No legal text provided"}), 400

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Analyze this legal evidence for a judge. Summarize key facts and identify investigation gaps: {text_content}"
        response = model.generate_content(prompt)
        return jsonify({"analysis": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- DATA SEEDER & MOCK ROUTES ---
@app.route('/api/mock/<category>', methods=['GET'])
def get_mock_data(category):
    try:
        file_path = f"backend/mock_data/{category}.json"
        with open(file_path, 'r') as f:
            return jsonify(json.load(f))
    except:
        return jsonify({"error": "Category not found"}), 404

@app.route('/api/test')
def home():
    return jsonify({"status": "online", "message": "Legal AI Backend is LIVE"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)