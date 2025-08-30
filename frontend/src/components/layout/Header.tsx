import React from 'react';

const Header: React.FC = () => {
  return (
    <header style={{ padding: '1rem', background: 'white', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', zIndex: 10 }}>
      <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>SARDIN-AI</h1>
      {/* User profile, logout button, etc. would go here */}
    </header>
  );
};

export default Header;
