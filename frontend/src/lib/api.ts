import axios from 'axios';

// Create an instance of axios
export const api = axios.create({
  baseURL: '/api', // The base URL will be proxied by Nginx to the backend
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the JWT token in headers
api.interceptors.request.use(
  (config) => {
    // We will get the token from our state management (Zustand)
    // For now, we'll just check for it in localStorage as a placeholder
    const token = localStorage.getItem('sardin-ai-token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
