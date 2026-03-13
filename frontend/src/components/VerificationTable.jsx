import { useEffect, useState } from 'react';
import { api } from '../services/api';

const VerificationTable = () => {
  const [lawyer, setLawyer] = useState(null);
  const [background, setBackground] = useState(null);

  useEffect(() => {
    api.getMockData('lawyer').then(setLawyer);
    api.getMockData('background').then(setBackground);
  }, []);

  return (
    <div className="grid md:grid-cols-2 gap-6 mt-8">
      {/* Lawyer Profile Card */}
      <div className="bg-white p-6 rounded-xl shadow-md border-t-4 border-blue-600">
        <h3 className="text-lg font-bold text-blue-900 mb-4">Lawyer Verification</h3>
        {lawyer && (
          <div className="space-y-2 text-sm">
            <p><strong>Name:</strong> {lawyer.fullName}</p>
            <p><strong>Status:</strong> <span className="text-green-600 font-bold">{lawyer.verificationStatus}</span></p>
            <p><strong>Success Rate:</strong> {lawyer.successRate}%</p>
            <p><strong>Specialization:</strong> {lawyer.specialization}</p>
          </div>
        )}
      </div>

      {/* Background Check Card */}
      <div className="bg-white p-6 rounded-xl shadow-md border-t-4 border-red-500">
        <h3 className="text-lg font-bold text-red-900 mb-4">Background Intelligence</h3>
        {background && (
          <div className="space-y-2 text-sm">
            <p><strong>Subject:</strong> {background.fullName}</p>
            <p><strong>Risk Level:</strong> <span className="font-bold text-orange-600">{background.riskLevel}</span></p>
            <p><strong>Prior Convictions:</strong> {background.priorConvictions}</p>
            <p className="italic text-gray-500 mt-2">{background.notes}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default VerificationTable;