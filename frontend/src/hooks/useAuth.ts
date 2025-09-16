// src/hooks/useAuth.ts
import { useState } from "react";
import { authApi, coreApi } from "../lib/api";
import { useAuthStore } from "../store/authStore";
import type { AuthResponse, LoginRequest, RegisterRequest } from "../types/auth";

export function useAuth() {
  const { user, setUser, logout } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function login(data: LoginRequest) {
    try {
      setLoading(true);
      const res = await authApi.post<AuthResponse>("/login", data);
      setUser(res.data);
      setError(null);
      return res.data;
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed");
      return null;
    } finally {
      setLoading(false);
    }
  }

  async function register(data: RegisterRequest) {
    try {
      setLoading(true);
      // Register tenant in crm-core
      const res = await coreApi.post<AuthResponse>("/tenants/register", data);
      setUser(res.data);
      setError(null);
      return res.data;
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed");
      return null;
    } finally {
      setLoading(false);
    }
  }

  return { user, login, register, logout, loading, error };
}
