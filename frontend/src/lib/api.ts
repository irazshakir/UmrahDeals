// src/lib/api.ts
import axios from "axios";
import auth from "./auth";

export const authApi = axios.create({
  baseURL: import.meta.env.VITE_AUTH_API_URL || "http://localhost:8001/api/v1/auth",
});

export const coreApi = axios.create({
  baseURL: import.meta.env.VITE_CORE_API_URL || "http://localhost:8002/api/v1",
});

// Attach tokens
[authApi, coreApi].forEach((instance) => {
  instance.interceptors.request.use((config) => {
    const token = auth.getAccessToken();
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  });
});
