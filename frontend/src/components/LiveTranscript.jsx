import { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';

const LiveTranscript = ({ evidenceText }) => {
  const [transcript, setTranscript] = useState([
    "Prosecutor: Can you state your location on the night of the 14th?",
    "Witness: I was at home the entire evening. I never left my apartment."
  ]);
  const [isListening, setIsListening] = useState(false);
  const [conflictAlert, setConflictAlert] = useState(null);
  const bottomRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [transcript]);

  const addSimulatedLine = () => {
    setTranscript(prev => [...prev, "Witness: And I certainly didn't have a black duffel bag."]);
  };

  const checkConflicts = async () => {
    if (!evidenceText) return alert("Upload base evidence first!");
    const prompt = `Compare this live testimony: "${transcript.join(" ")}" against this evidence: "${evidenceText}". Are there contradictions? Keep it short.`;
    
    // Reusing the analyzeText endpoint for a custom prompt
    const res = await api.analyzeText(prompt); 
    setConflictAlert(res.analysis);
  };

  return (
    <div className="bg-slate-900 p-6 rounded-xl shadow-lg border-t-4 border-red-500 text-white flex flex-col h-96">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold flex items-center">
          <span className={`w-3 h-3 rounded-full mr-2 ${isListening ? 'bg-red-500 animate-pulse' : 'bg-gray-500'}`}></span>
          Live Witness Feed
        </h3>
        <button onClick={() => setIsListening(!isListening)} className="text-xs bg-slate-700 px-3 py-1 rounded">
          {isListening ? "Stop Recording" : "Start Mic"}
        </button>
      </div>

      <div className="flex-1 overflow-y-auto bg-slate-800 p-4 rounded text-sm font-mono space-y-2 mb-4">
        {transcript.map((line, i) => (
          <p key={i} className={line.startsWith("Witness:") ? "text-blue-300" : "text-gray-300"}>{line}</p>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="flex gap-2">
        <button onClick={addSimulatedLine} className="flex-1 bg-slate-700 hover:bg-slate-600 py-2 rounded text-sm transition">
          Simulate Next Line
        </button>
        <button onClick={checkConflicts} className="flex-1 bg-red-600 hover:bg-red-500 py-2 rounded text-sm font-bold transition">
          AI Conflict Check
        </button>
      </div>

      {conflictAlert && (
        <div className="mt-4 p-3 bg-red-900 border border-red-500 rounded text-sm text-red-100">
          <strong>⚠️ Contradiction Detected:</strong> {conflictAlert}
        </div>
      )}
    </div>
  );
};

export default LiveTranscript;