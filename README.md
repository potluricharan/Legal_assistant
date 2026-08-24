# AI Legal Assistance Platform & Courtroom Intelligence System

An AI-powered decision-support platform designed to assist judges, legal researchers, and investigators in analyzing court documents, tracking case timelines, predicting outcomes, and executing semantic searches.

---

## Features

- **AI Document Summarization:** Extracts executive summaries, key legal arguments, and procedural/investigative gaps from complex case PDFs using Gemini.
- **Outcome Prediction:** Uses machine learning classification models to evaluate case facts and project outcome probabilities.
- **Semantic Vector Vault:** Generates vector embeddings to perform cosine similarity searches across historical case precedents.
- **Context-Aware Legal Assistant:** Firestore-backed conversational assistant that retains recent case history for continuity.
- **Deduplication Engine:** Employs MD5 file hashing to identify and flag repeated document uploads instantly.

---

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI, Uvicorn
- **Database:** Google Cloud Firestore (Firebase Admin SDK)
- **AI & Embeddings:** Google GenAI SDK (`gemini-3.6-flash`, `text-embedding-004`)
- **Machine Learning & NLP:** Scikit-Learn, NumPy, PyPDF2

---

## Project Structure

```text
Legal_assistant/
├── backend/
│   ├── database.py              # Firebase Admin initialization
│   ├── embeddings.py            # Vector embedding utilities
│   ├── main.py                  # FastAPI REST endpoints
│   ├── ml_model.py              # ML inference pipeline
│   ├── models.py                # Schema definitions
│   ├── requirements.txt         # Backend Python dependencies
│   ├── services.py              # Gemini LLM logic & PDF extraction
│   └── test_api.py              # Verification script for API connectivity
├── frontend/
│   ├── app.py                   # Streamlit UI dashboard
│   └── requirements.txt         # Frontend dependencies
├── data/
│   └── precedents/              # Legal dataset reference files
├── .gitignore
└── README.md
