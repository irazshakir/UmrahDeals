// src/layouts/AuthLayout.tsx
import { ReactNode } from "react";
import { Outlet } from "react-router-dom";

type AuthLayoutProps = {
  children?: ReactNode;
};

export default function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md p-6 bg-white rounded-xl shadow-lg">
        {children ?? <Outlet />}
      </div>
    </div>
  );
}
