import React from 'react';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';

// This layout will wrap all pages inside the (main) route group
export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', flexDirection: 'column' }}>
      <Header />
      <div style={{ display: 'flex', flex: '1' }}>
        <Sidebar />
        <main style={{ flex: '1', padding: '1rem', background: '#f9fafb' }}>
          {children}
        </main>
      </div>
    </div>
  );
}
