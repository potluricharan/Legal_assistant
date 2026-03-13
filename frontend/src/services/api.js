// Vite uses import.meta.env for variables defined in your .env file
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "https://legal-assistant-3mws.onrender.com";

export const api = {
    // Check if server is awake
    testConnection: () => fetch(`${BACKEND_URL}/api/test`).then(res => res.json()),
    
    // Get Mock Data (lawyer, background, mobile, precedent)
    getMockData: (category) => fetch(`${BACKEND_URL}/api/mock/${category}`).then(res => res.json()),
    
    // Send text to Gemini AI
    analyzeText: (text) => fetch(`${BACKEND_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    }).then(res => res.json()),

    // FEATURE 1: ML Predictor
    predictOutcome: (text) => fetch(`${BACKEND_URL}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    }).then(res => res.json()),

    // FEATURE 2: RAG Legal Vault
    searchVault: (query) => fetch(`${BACKEND_URL}/api/vault/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
    }).then(res => res.json())
};