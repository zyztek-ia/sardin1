'use client';

import React, { useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';

const DashboardPage: React.FC = () => {
  const { isAuthenticated, user, fetchProfile } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // If the user is not authenticated, redirect to login
    // This is a client-side check. Middleware is better for production.
    if (!isAuthenticated) {
      router.push('/login');
    } else {
      // If authenticated but user profile is not loaded, fetch it.
      if (!user) {
        fetchProfile();
      }
    }
  }, [isAuthenticated, user, router, fetchProfile]);

  if (!isAuthenticated || !user) {
    // You can show a loading spinner here
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 style={{ fontSize: '2rem', fontWeight: 'bold' }}>Dashboard</h1>
      <p style={{ marginTop: '1rem' }}>
        Welcome, User ID: {user.id}!
      </p>
      <p style={{ marginTop: '0.5rem' }}>
        This is the main dashboard for SARDIN-AI. More widgets and data visualizations will be added here.
      </p>
    </div>
  );
};

export default DashboardPage;
