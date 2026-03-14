from fastapi import FastAPI, UploadFile, File, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import numpy as np
from datetime import datetime, timezone
from database import db
from services import (
    analyze_case_with_gemini, 
    analyze_with_history, 
    calculate_file_hash, 
    get_embedding
)
from models import FirebaseSchema
from ml_model import predict_outcome

# Initialize FastAPI App
app = FastAPI(title="Legal AI Assistant Pro")

# --- CORS CONFIGURATION ---
# Necessary for the Streamlit frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. CASE ANALYSIS ROUTE ---
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Handles PDF upload, duplicate detection, AI analysis, 
    embedding generation, and Firestore storage.
    """
    path = f"temp_{file.filename}"
    try:
        # Save file locally temporarily for processing
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # A. Duplicate Detection via MD5 File Hash
        file_hash = calculate_file_hash(path)
        existing_docs = db.collection('cases').where('file_hash', '==', file_hash).stream()
        
        for doc in existing_docs:
            data = doc.to_dict()
            return {
                "status": "repeated",
                "case_id": doc.id,
                "filename": data.get('filename'),
                "report": {"summary": data.get('current_summary')},
                "explanation": f"Duplicate upload detected. Already stored as '{data.get('filename')}'."
            }

        # B. AI Analysis & Embedding Generation
        # This uses Gemini 1.5-Flash to summarize and identify gaps
        report = analyze_case_with_gemini(path)
        prediction = predict_outcome(report['summary'])
        
        # C. Generate Vector Embedding for Semantic Search
        vector = get_embedding(report['summary'])
        
        # D. Save to Firestore Cloud Database
        case_data = FirebaseSchema.create_case_doc(
            file.filename, 
            report['summary'], 
            prediction, 
            "Stored Locally"
        )
        case_data.update({
            "file_hash": file_hash,
            "vector": vector,
            "timestamp": datetime.now(timezone.utc)
        })
        
        _, doc_ref = db.collection('cases').add(case_data)
        
        return {
            "status": "success",
            "case_id": doc_ref.id, 
            "report": report, 
            "prediction": prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup: Remove temp file from server
        if os.path.exists(path):
            os.remove(path)

# --- 2. SEMANTIC SEARCH ROUTE ---
@app.get("/search")
async def search(q: str):
    """
    Performs vector-based semantic search across all stored cases.
    """
    try:
        # Convert user query into a vector
        query_vec = get_embedding(q)
        if not query_vec:
            return {"results": []}

        all_cases = db.collection('cases').stream()
        results = []

        for doc in all_cases:
            data = doc.to_dict()
            if 'vector' not in data:
                continue
            
            # Mathematical Cosine Similarity Calculation
            case_vec = np.array(data['vector'])
            q_vec = np.array(query_vec)
            
            similarity = np.dot(q_vec, case_vec) / (np.linalg.norm(q_vec) * np.linalg.norm(case_vec))
            
            # Filter results by a relevance threshold (0.65)
            if similarity > 0.65:
                results.append({
                    "case_id": doc.id,
                    "filename": data.get('filename'),
                    "score": round(float(similarity), 4),
                    "summary_preview": data.get('current_summary')[:250] + "..."
                })
        
        # Sort results by highest match score
        results.sort(key=lambda x: x['score'], reverse=True)
        return {"results": results[:5]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 3. CHAT WITH HISTORY ROUTE ---
@app.post("/chat_with_history")
async def chat(case_id: str = Body(..., embed=True), query: str = Body(..., embed=True)):
    """
    Context-aware chatbot that uses Firestore to maintain session history.
    """
    try:
        answer = analyze_with_history(case_id, query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))