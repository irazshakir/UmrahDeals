// src/store/authStore.ts
import { create } from "zustand";
import type { AuthResponse } from "../types/auth";
import auth from "../lib/auth";

type AuthState = {
  user: Omit<AuthResponse, "access_token" | "refresh_token" | "token_type"> | null;
  setUser: (data: AuthResponse) => void;
  logout: () => void;
};

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  setUser: (data) => {
    auth.setTokens(data);
    set({
      user: {
        role: data.role,
        tenant_id: data.tenant_id,
        name: data.name,
      },
    });
  },
  logout: () => {
    auth.clearTokens();
    set({ user: null });
  },
}));
