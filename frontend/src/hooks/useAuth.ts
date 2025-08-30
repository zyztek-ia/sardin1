import { useAuthStore } from '../store/authStore';
import { api } from '../lib/api';

// This hook provides a simple interface to the auth store and related logic
export const useAuth = () => {
  const { token, user, isAuthenticated, login, logout, setUser } = useAuthStore();

  const fetchProfile = async () => {
    if (token && !user) {
      try {
        const response = await api.get('/auth/profile');
        // This is a simplified user object. Adjust based on your actual user model.
        setUser({ id: response.data.logged_in_as, username: 'user', role: 'user' });
      } catch (error) {
        console.error('Failed to fetch profile', error);
        // If profile fetch fails, the token is likely invalid, so log out.
        logout();
      }
    }
  };

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    fetchProfile,
  };
};
