import { useState } from 'react';
import { api } from '../services/api';

const CasePredictor = () => {
  const [facts, setFacts] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    if (!facts.trim()) return alert("Please enter the case facts.");
    setLoading(true);
    setResult(null);
    try {
      // This calls the FastAPI endpoint we set up
      const data = await api.predictOutcome(facts); 
      setResult(data);
    } catch (err) {
      alert("Prediction failed. Make sure the backend is running and the .pkl model is loaded.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-8 rounded-xl shadow-md border border-gray-200">
      {/* Mimicking st.title and st.write from Streamlit */}
      <h2 className="text-3xl font-bold text-gray-900 mb-2">Supreme Court Case Predictor</h2>
      <p className="text-gray-600 mb-6">
        Enter the facts of a case to predict the winning party based on historical data.
      </p>

      {/* Mimicking st.text_area */}
      <div className="mb-4">
        <label className="block text-sm font-semibold text-gray-700 mb-2">Case Facts</label>
        <textarea
          className="w-full h-48 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none resize-none font-mono text-sm"
          placeholder="In 1992, a high school student..."
          value={facts}
          onChange={(e) => setFacts(e.target.value)}
        />
      </div>

      {/* Mimicking st.button */}
      <button
        onClick={handlePredict}
        disabled={loading}
        className={`w-full py-3 rounded-lg text-white font-bold transition-colors ${
          loading ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
        }`}
      >
        {loading ? "Analyzing Historical Data..." : "Predict Outcome"}
      </button>

      {/* Mimicking st.success block shown in your second screenshot */}
      {result && (
        <div className="mt-6 bg-green-50 border-l-4 border-green-500 p-4 rounded-r-lg shadow-sm">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-lg font-bold text-green-800">
                Prediction: {result.prediction}
              </h3>
              <p className="text-sm text-green-700 mt-1">
                Confidence / Probability: <strong>{result.confidence}%</strong>
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CasePredictor;