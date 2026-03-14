import React from 'react';

const ActionButtons = ({ onDiagnose, onUnlock, onAIFix, loading }: any) => (
  <div className="grid grid-cols-3 gap-4">
    <button onClick={onDiagnose} disabled={loading} className="bg-blue-600 text-white p-3 rounded">Diagnose</button>
    <button onClick={() => onUnlock('com.payjoy.credito')} disabled={loading} className="bg-orange-600 text-white p-3 rounded">Remove PayJoy</button>
    <button onClick={onAIFix} disabled={loading} className="bg-purple-600 text-white p-3 rounded">AI Fix</button>
  </div>
);

export default ActionButtons;
