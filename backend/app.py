import os
import shutil
import pickle
import random
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore
from google import genai
from PyPDF2 import PdfReader
import uvicorn

app = FastAPI(title="Judicial AI Engine")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. FIREBASE SETUP ---
try:
    if not firebase_admin._apps:
        sa_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
        if sa_json:
            import json
            cred = credentials.Certificate(json.loads(sa_json))
        elif os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
        else:
            cred = None
        
        if cred:
            firebase_admin.initialize_app(cred)
            db = firestore.client()
        else:
            db = None
except Exception as e:
    print(f"Firebase Init Error: {e}")
    db = None

# --- 2. LOAD ML MODEL ---
try:
    with open("simple_facts_model.pkl", "rb") as f:
        ml_model = pickle.load(f)
except Exception as e:
    print(f"Warning: ML model offline. {e}")
    ml_model = None

# --- 3. TEAMMATES' HELPER FUNCTIONS ---
def extract_text_from_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content: text += content
    return text

def predict_outcome(case_summary):
    """Fallback logic from teammates' ml_model.py if .pkl fails"""
    summary_lower = str(case_summary).lower()
    if "violation" in summary_lower or "compelling interest" in summary_lower:
        return {"prediction": "High Probability of Constitutional Merit", "confidence": 80.0}
    elif "lack of evidence" in summary_lower or "dismissed" in summary_lower:
        return {"prediction": "Likely Dismissal / Acquittal", "confidence": 75.0}
    else:
        return {"prediction": "Further Judicial Review Required", "confidence": random.randint(55, 65)}

# --- 4. THE MAIN ENDPOINT (Feature 1) ---
@app.post("/api/analyze")
async def analyze_case(file: UploadFile = File(...)):
    # 1. Save uploaded PDF temporarily
    path = f"temp_{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 2. Extract Text
        text = extract_text_from_pdf(path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Scanned PDF or no text found.")

        # 3. Gemini AI Analysis (from services.py)
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        prompt = f"Analyze this case. Provide a concise legal summary and list investigation gaps: {text[:8000]}"
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        summary = response.text

        # 4. ML Prediction
        if ml_model:
            pred_text = ml_model.predict([summary])[0]
            confidence = max(ml_model.predict_proba([summary])[0]) * 100
            prediction_data = {"prediction": str(pred_text), "confidence": round(confidence, 1)}
        else:
            prediction_data = predict_outcome(summary)

        # 5. Save to Firebase (Replacing SQLite)
        if db:
            db.collection('legal_cases').add({
                'filename': file.filename,
                'summary': summary,
                'prediction': prediction_data['prediction'],
                'confidence': prediction_data['confidence']
            })

        # Cleanup temp file
        os.remove(path)

        return {
            "summary": summary,
            "prediction": prediction_data['prediction'],
            "confidence": prediction_data['confidence']
        }

    except Exception as e:
        if os.path.exists(path): os.remove(path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)