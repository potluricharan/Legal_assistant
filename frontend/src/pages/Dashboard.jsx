import { useState } from 'react';
import UploadZone from '../components/UploadZone';

const Dashboard = () => {
  const [analysisResult, setAnalysisResult] = useState("");

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <header className="mb-10 text-center">
        <h1 className="text-4xl font-extrabold text-blue-900">Judicial AI Dashboard</h1>
        <p className="text-gray-600 mt-2">Verified Case Assistance & Document Intelligence</p>
      </header>

      <div className="max-w-4xl mx-auto grid gap-8">
        <UploadZone onAnalysisComplete={(res) => setAnalysisResult(res)} />
        
        {analysisResult && (
          <div className="bg-white p-8 rounded-xl shadow-lg border-l-8 border-green-500">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">AI Legal Insights</h2>
            <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
              {analysisResult}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;