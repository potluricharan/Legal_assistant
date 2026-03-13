import { useState } from 'react';
import { api } from '../services/api';

const SingleCaseAnalysis = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    if (!file) return alert("Please upload a PDF file first.");
    setLoading(true);
    setResult(null);
    try {
      const data = await api.analyzeFile(file);
      setResult(data);
    } catch (err) {
      alert("Analysis Failed. Ensure backend is running and Gemini API key is valid.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-8 rounded-xl shadow-md border border-gray-200">
      <h2 className="text-2xl font-bold text-gray-900 mb-2">📄 Single Case Analysis</h2>
      <p className="text-gray-600 mb-6">Upload a case PDF to extract facts, identify gaps, and predict outcomes.</p>

      {/* Upload Area */}
      <div className="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:bg-slate-50 transition mb-4">
        <input 
          type="file" 
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
      </div>

      {/* Analyze Button */}
      <button 
        onClick={handleAnalyze} 
        disabled={loading || !file}
        className={`w-full py-3 rounded-lg font-bold text-white transition-colors ${
          loading || !file ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
        }`}
      >
        {loading ? "Analyzing Document & Predicting Outcome..." : "Analyze & Save"}
      </button>

      {/* Results Display */}
      {result && (
        <div className="mt-8 space-y-6">
          {/* AI Summary */}
          <div className="p-6 bg-slate-50 rounded-lg border border-slate-200">
            <h3 className="text-lg font-bold text-slate-800 mb-3">AI Case Summary & Gaps</h3>
            <div className="prose prose-sm max-w-none text-slate-700 whitespace-pre-wrap">
              {result.summary}
            </div>
          </div>

          {/* ML Prediction (Teammates' green box UI) */}
          <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded-r-lg shadow-sm">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl">⚖️</span>
              </div>
              <div className="ml-4">
                <p className="text-sm text-green-700 uppercase tracking-wide font-bold mb-1">Predicted Outcome</p>
                <h3 className="text-xl font-black text-green-900">{result.prediction}</h3>
                <p className="text-sm text-green-800 mt-1">
                  Model Confidence: <strong>{result.confidence}%</strong>
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SingleCaseAnalysis;