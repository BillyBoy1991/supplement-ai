"use client";

import { createContext, useContext, useState } from "react";

interface AuthState {
  token: string | null;
  setToken: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  // Token solo en memoria (no localStorage): se pierde al recargar, por diseño.
  const [token, setToken] = useState<string | null>(null);
  const logout = () => setToken(null);
  return <AuthContext.Provider value={{ token, setToken, logout }}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth debe usarse dentro de AuthProvider");
  return ctx;
}
