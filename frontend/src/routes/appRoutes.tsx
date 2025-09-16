// src/routes/appRoutes.tsx
import { createBrowserRouter } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout";
import DashboardLayout from "../layouts/DashboardLayout";

import LoginPage from "../pages/auth/LoginPage";
import RegisterPage from "../pages/auth/RegisterPage";
import DashboardHome from "../pages/dashboard/DashboardHome";

const router = createBrowserRouter([
  {
    path: "/",
    element: <DashboardLayout />,
    children: [{ index: true, element: <DashboardHome /> }],
  },
  {
    path: "/login",
    element: <AuthLayout />,
    children: [{ index: true, element: <LoginPage /> }],
  },
  {
    path: "/register",
    element: <AuthLayout />,
    children: [{ index: true, element: <RegisterPage /> }],
  },
]);

export default router;
