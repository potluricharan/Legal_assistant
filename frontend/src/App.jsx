import { useState } from 'react';
import UploadZone from './components/UploadZone';
import VerificationTable from './components/VerificationTable';

function App() {
  const [analysis, setAnalysis] = useState("");

  return (
    <div className="min-h-screen bg-slate-100 p-4 md:p-10 font-sans">
      <div className="max-w-5xl mx-auto">
        {/* Navigation / Header */}
        <header className="flex justify-between items-center mb-10 bg-blue-900 text-white p-6 rounded-2xl shadow-xl">
          <div>
            <h1 className="text-2xl font-black tracking-tight">JUDICIAL <span className="text-blue-400">AI</span></h1>
            <p className="text-xs text-blue-200">Courtroom Assistance System v1.0</p>
          </div>
          <div className="text-right hidden sm:block">
            <p className="text-sm font-medium">Session: ACTIVE</p>
            <p className="text-xs opacity-70">Authenticated: Judge / Magistrate</p>
          </div>
        </header>

        <main className="space-y-8">
          {/* Top Section: Action & AI */}
          <section className="grid lg:grid-cols-3 gap-8">
            <div className="lg:col-span-1">
              <UploadZone onAnalysisComplete={(res) => setAnalysis(res)} />
            </div>
            
            <div className="lg:col-span-2">
              <div className="bg-white h-full min-h-[400px] p-8 rounded-2xl shadow-lg border border-slate-200 overflow-auto">
                <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center">
                  <span className="w-3 h-3 bg-green-500 rounded-full mr-3 animate-pulse"></span>
                  AI Analysis Output
                </h2>
                {analysis ? (
                  <div className="prose prose-blue max-w-none whitespace-pre-wrap text-slate-700 leading-relaxed">
                    {analysis}
                  </div>
                ) : (
                  <div className="h-64 flex flex-col items-center justify-center text-slate-400">
                    <p>No documents analyzed yet.</p>
                    <p className="text-sm">Upload evidence on the left to begin.</p>
                  </div>
                )}
              </div>
            </div>
          </section>

          {/* Bottom Section: Verification Panels */}
          <section>
            <h2 className="text-2xl font-bold text-slate-800 mb-4">Case Entities Verification</h2>
            <VerificationTable />
          </section>
        </main>
      </div>
    </div>
  );
}

export default App;