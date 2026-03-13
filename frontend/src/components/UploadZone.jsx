import { useState } from 'react';
import { api } from '../services/api';

const UploadZone = ({ onAnalysisComplete }) => {
  const [loading, setLoading] = useState(false);
  const [text, setText] = useState("");

  const handleAnalyze = async () => {
    if (!text) return alert("Please paste legal text first!");
    setLoading(true);
    try {
      const data = await api.analyzeText(text);
      onAnalysisComplete(data.analysis);
    } catch (err) {
      alert("AI Analysis failed. Check Backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-white rounded-xl shadow-lg border-2 border-dashed border-blue-200">
      <h3 className="text-xl font-bold text-blue-900 mb-4">Evidence Analysis Portal</h3>
      <textarea 
        className="w-full h-40 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
        placeholder="Paste witness statements, FIR text, or forensic logs here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button 
        onClick={handleAnalyze}
        disabled={loading}
        className={`mt-4 w-full py-3 rounded-lg text-white font-bold transition ${
          loading ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'
        }`}
      >
        {loading ? "AI is Analyzing Evidence..." : "Run Judicial AI Scan"}
      </button>
    </div>
  );
};

export default UploadZone;