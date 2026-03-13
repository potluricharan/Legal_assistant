const MobileForensics = () => {
  // Hardcoded for hackathon speed, normally fetched from API
  const pings = [
    { time: "22:15", location: "Tower 4A - Downtown", match: "Alibi Mismatch" },
    { time: "22:45", location: "Tower 7B - Industrial Park", match: "Crime Scene Proximity" },
    { time: "23:10", location: "Tower 2C - Highway 9", match: "Flight Risk Route" }
  ];

  return (
    <div className="bg-white p-6 rounded-xl shadow-lg border border-slate-200">
      <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center">
        📱 Mobile GPS & Tower Forensics
      </h3>
      
      <div className="relative border-l-2 border-slate-300 ml-3 space-y-6 mt-6">
        {pings.map((ping, i) => (
          <div key={i} className="mb-8 ml-6 relative">
            <span className="absolute flex items-center justify-center w-6 h-6 bg-blue-100 rounded-full -left-10 ring-8 ring-white">
              📍
            </span>
            <h4 className="font-bold text-slate-700">{ping.location}</h4>
            <div className="text-sm text-slate-500 flex justify-between mt-1">
              <span>Time: {ping.time}</span>
              <span className={`font-bold ${ping.match.includes('Mismatch') || ping.match.includes('Risk') ? 'text-red-500' : 'text-orange-500'}`}>
                {ping.match}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MobileForensics;