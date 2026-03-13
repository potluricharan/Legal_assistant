import os
import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS so Vercel can talk to Render
CORS(app)

# --- TEST ROUTE 1: The Ping ---
@app.route('/api/test', methods=['GET'])
def test_connection():
    return jsonify({
        "status": "success",
        "message": "✅ Vercel and Render are successfully connected! The API is LIVE."
    })

# --- TEST ROUTE 2: Mock Data Retrieval ---
@app.route('/api/mock/lawyer', methods=['GET'])
def get_mock_lawyer():
    try:
        # Reads the JSON file you generated in the mock_data folder
        file_path = os.path.join(os.path.dirname(__file__), 'mock_data', 'lawyer.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 500

if __name__ == "__main__":
    # Render assigns a dynamic PORT, fallback to 10000 locally
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)