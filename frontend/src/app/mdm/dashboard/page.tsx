'use client';
import React, { useState } from 'react';
import axios from 'axios';
import DeviceStatus from '@/components/mdm/DeviceStatus';
import LogConsole from '@/components/mdm/LogConsole';
import ActionButtons from '@/components/mdm/ActionButtons';

export default function MDMDashboard() {
  const [deviceInfo, setDeviceInfo] = useState(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const addLog = (message: string) => setLogs(p => [...p, { timestamp: new Date().toLocaleTimeString(), message }]);

  const handleDiagnose = async () => {
    setLoading(true);
    try {
      const res = await axios.get('/api/mdm/diagnose');
      setDeviceInfo(res.data);
      addLog(`Device: ${res.data.brand} ${res.data.model}`);
    } catch (e: any) { addLog(`Error: ${e.message}`); }
    setLoading(false);
  };

  const handleUnlock = async (pkg: string) => {
    setLoading(true);
    try {
      const res = await axios.post('/api/mdm/unlock', { package: pkg });
      addLog(res.data.success ? `Removed ${pkg}` : `Failed: ${res.data.error}`);
    } catch (e: any) { addLog(`Error: ${e.message}`); }
    setLoading(false);
  };

  const handleAIFix = async () => {
    setLoading(true);
    try {
      const res = await axios.post('/api/mdm/ai-fix', { device_info: JSON.stringify(deviceInfo) });
      res.data.results.forEach((r: any) => addLog(`AI Executed: ${r.command}`));
    } catch (e: any) { addLog(`Error: ${e.message}`); }
    setLoading(false);
  };

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">MDM Unlocker Pro</h1>
      <div className="grid grid-cols-3 gap-8 mb-8">
        <div className="col-span-1"><DeviceStatus deviceInfo={deviceInfo} loading={loading} /></div>
        <div className="col-span-2"><LogConsole logs={logs} /></div>
      </div>
      <ActionButtons onDiagnose={handleDiagnose} onUnlock={handleUnlock} onAIFix={handleAIFix} loading={loading} />
    </div>
  );
}
