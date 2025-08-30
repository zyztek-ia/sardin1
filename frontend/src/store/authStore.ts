import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface AuthState {
  token: string | null;
  user: { id: number; username: string; role: string } | null;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
  setUser: (user: any) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      login: (token) => {
        set({ token, isAuthenticated: true });
        // In a real app, you'd decode the token to get user info
        // or fetch it from a /profile endpoint.
      },
      logout: () => {
        set({ token: null, user: null, isAuthenticated: false });
      },
      setUser: (user) => {
        set({ user });
      },
    }),
    {
      name: 'sardin-ai-auth-storage', // name of the item in the storage (must be unique)
      storage: createJSONStorage(() => localStorage), // (optional) by default, 'localStorage' is used
      partialize: (state) => ({ token: state.token }), // only persist the token
    }
  )
);
