import { useState } from 'react';
import { pingServer, fetchMockLawyer } from './services/api';

function App() {
  const [pingStatus, setPingStatus] = useState("Waiting to test connection...");
  const [lawyerData, setLawyerData] = useState(null);

  return (
    <div style={{ padding: '40px', fontFamily: 'system-ui, sans-serif', maxWidth: '600px', margin: '0 auto' }}>
      <h1 style={{ color: '#1e3a8a' }}>AI Legal Assistant: Systems Check</h1>
      
      {/* Test 1: Network Ping */}
      <div style={{ background: '#f3f4f6', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
        <h2 style={{ marginTop: 0 }}>1. Test API Routing</h2>
        <button 
          onClick={async () => {
            setPingStatus("Pinging...");
            const res = await pingServer();
            setPingStatus(res.message || res.error);
          }}
          style={{ background: '#2563eb', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          Ping Render Backend
        </button>
        <p style={{ fontWeight: 'bold', marginTop: '15px' }}>{pingStatus}</p>
      </div>

      {/* Test 2: File Reading */}
      <div style={{ background: '#f3f4f6', padding: '20px', borderRadius: '8px' }}>
        <h2 style={{ marginTop: 0 }}>2. Test Mock Data Retrieval</h2>
        <button 
          onClick={async () => {
            const data = await fetchMockLawyer();
            setLawyerData(data);
          }}
          style={{ background: '#059669', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          Fetch Lawyer Profile
        </button>
        
        {lawyerData && (
          <pre style={{ background: '#1f2937', color: '#10b981', padding: '15px', borderRadius: '4px', marginTop: '15px', overflowX: 'auto' }}>
            {JSON.stringify(lawyerData, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}

export default App;