"use client";

import { useState } from "react";
import { ApiError, auth } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function AuthScreen({ notice }: { notice?: string }) {
  const { setToken } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      const fn = mode === "login" ? auth.login : auth.register;
      const { access_token } = await fn(email, password);
      setToken(access_token);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Error de conexión");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-sm space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Supplement AI</h1>
        <p className="text-gray-500">Recomendaciones personalizadas basadas en evidencia.</p>
      </div>

      {notice && <p className="rounded bg-amber-50 px-3 py-2 text-sm text-amber-800">{notice}</p>}

      <form onSubmit={submit} className="space-y-3">
        <input
          type="email"
          placeholder="Email"
          value={email}
          required
          onChange={(e) => setEmail(e.target.value)}
          className="w-full rounded border border-gray-300 px-4 py-2 focus:border-emerald-500 focus:outline-none"
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          required
          onChange={(e) => setPassword(e.target.value)}
          className="w-full rounded border border-gray-300 px-4 py-2 focus:border-emerald-500 focus:outline-none"
        />
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button
          type="submit"
          disabled={busy}
          className="w-full rounded bg-emerald-600 py-2 font-medium text-white hover:bg-emerald-700 disabled:opacity-50"
        >
          {mode === "login" ? "Entrar" : "Crear cuenta"}
        </button>
      </form>

      <button
        onClick={() => {
          setMode(mode === "login" ? "register" : "login");
          setError(null);
        }}
        className="text-sm text-emerald-700 hover:underline"
      >
        {mode === "login" ? "¿No tienes cuenta? Regístrate" : "¿Ya tienes cuenta? Entra"}
      </button>
    </div>
  );
}
