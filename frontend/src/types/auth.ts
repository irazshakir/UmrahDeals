// src/types/auth.ts
export type AuthResponse = {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
  role: string;
  tenant_id: string;
  name: string;
};

export type LoginRequest = {
  email: string;
  password: string;
};

export type RegisterRequest = {
  tenant_name: string;
  tenant_email: string;
  tenant_phone?: string;
  tenant_address?: string;
  password: string; // for admin user
  name: string;     // admin user name
};
