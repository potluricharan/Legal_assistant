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
# Set these in your Render Dashboard Environment Variables
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

def init_db():
    if not firebase_admin._apps:
        sa_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
        if sa_json:
            # For Render/Production
            cred = credentials.Certificate(json.loads(sa_json))
            firebase_admin.initialize_app(cred)
        elif os.path.exists("backend/serviceAccountKey.json"):
            # For Local Development
            cred = credentials.Certificate("backend/serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        else:
            return None
    return firestore.client()

db = init_db()

# --- AI ANALYSIS ENDPOINT ---
@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    data = request.json
    text_content = data.get("text")
    
    if not text_content:
        return jsonify({"error": "No text provided"}), 400

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Act as a senior judicial assistant. Analyze the following legal evidence:
        {text_content}
        
        Provide a structured legal brief including:
        1. Executive Summary
        2. Key Factual Findings
        3. Potential Legal Vulnerabilities
        4. Recommended Next Steps for Investigation
        """
        response = model.generate_content(prompt)
        return jsonify({"analysis": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- MOCK DATA RETRIEVAL ---
@app.route('/api/mock/<category>', methods=['GET'])
def get_mock_data(category):
    try:
        # Matches your backend/mock_data/*.json files
        file_path = os.path.join(os.path.dirname(__file__), 'mock_data', f'{category}.json')
        with open(file_path, 'r') as f:
            return jsonify(json.load(f))
    except Exception:
        return jsonify({"error": "Data category not found"}), 404

@app.route('/api/test')
def test():
    return jsonify({"status": "online", "message": "Judicial AI Engine is LIVE"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)