import React from 'react';

const LogConsole = ({ logs }: any) => (
  <div className="bg-gray-900 text-green-400 p-4 rounded h-64 overflow-y-auto font-mono text-sm">
    <h3 className="text-xs text-gray-500 mb-2">SYSTEM CONSOLE</h3>
    {logs.map((log: any, i: number) => (
      <div key={i}><span className="text-gray-500">[{log.timestamp}]</span> {log.message}</div>
    ))}
  </div>
);

export default LogConsole;
