import React from 'react';

const DeviceStatus = ({ deviceInfo, loading }: any) => (
  <div className="bg-white p-6 rounded shadow border">
    <h2 className="text-xl font-bold mb-4">Device Status</h2>
    {loading ? <p>Loading...</p> : deviceInfo ? (
      <div>
        <p><b>Brand:</b> {deviceInfo.brand}</p>
        <p><b>Model:</b> {deviceInfo.model}</p>
      </div>
    ) : <p>No device connected</p>}
  </div>
);

export default DeviceStatus;
