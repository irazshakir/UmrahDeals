// src/hooks/useApi.ts
import { useState } from "react";
import api from "../lib/api";

export function useApi<T>() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const request = async (url: string, method = "GET", data?: any): Promise<T | null> => {
    try {
      setLoading(true);
      setError(null);
      const res = await api.request<T>({ url, method, data });
      return res.data;
    } catch (err: any) {
      setError(err.response?.data?.detail || "Something went wrong");
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { request, loading, error };
}
