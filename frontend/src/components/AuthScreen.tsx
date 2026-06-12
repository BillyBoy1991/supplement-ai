"use client";

/* Supplement AI — login / registro rediseñado.
   Sustituye a src/components/AuthScreen.tsx (misma lógica, nuevo visual). */

import { useState } from "react";
import { ApiError, auth } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { LogoLockup, LogoMark } from "@/components/Logo";

function Field({
  label, type, value, onChange, placeholder, autoComplete,
}: {
  label: string; type: string; value: string;
  onChange: (v: string) => void; placeholder?: string; autoComplete?: string;
}) {
  return (
    <label className="block">
      <span className="font-mono text-[11px] uppercase tracking-[0.14em] text-muted">{label}</span>
      <input
        type={type}
        required
        value={value}
        placeholder={placeholder}
        autoComplete={autoComplete}
        onChange={(e) => onChange(e.target.value)}
        className="mt-1.5 w-full rounded-field border border-line bg-white px-4 py-3 text-[15px] text-ink outline-none transition placeholder:text-muted/60 focus:border-accent focus:ring-2 focus:ring-accent/15"
      />
    </label>
  );
}

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
    <div className="grid min-h-screen lg:grid-cols-[1.05fr_1fr]">
      {/* Panel de marca */}
      <div
        className="relative hidden flex-col justify-between overflow-hidden p-12 lg:flex"
        style={{ background: "linear-gradient(160deg, var(--sa-primary) 0%, var(--sa-primary-deep) 100%)" }}
      >
        <div className="pointer-events-none absolute -bottom-32 -right-24 opacity-[0.07]">
          <LogoMark size={520} tone="light" />
        </div>
        <LogoLockup size={30} tone="light" />
        <div className="relative max-w-md">
          <h2 className="font-display text-4xl font-semibold leading-[1.12] tracking-tight text-white">
            La ciencia de lo que tu cuerpo necesita.
          </h2>
          <p className="mt-5 text-[15px] leading-relaxed text-white/65">
            15 preguntas sobre tus hábitos. Un protocolo de suplementación construido sobre
            evidencia publicada — no sobre promesas.
          </p>
        </div>
        <p className="relative font-mono text-[11px] uppercase tracking-[0.18em] text-white/40">
          Evidencia · Personalización · Transparencia
        </p>
      </div>

      {/* Formulario */}
      <div className="flex items-center justify-center bg-mist px-6 py-14">
        <div className="w-full max-w-sm">
          <div className="mb-9 lg:hidden">
            <LogoLockup size={28} />
          </div>

          <h1 className="font-display text-2xl font-semibold tracking-tight">
            {mode === "login" ? "Bienvenido de nuevo" : "Crea tu cuenta"}
          </h1>
          <p className="mt-2 text-[15px] leading-relaxed text-muted">
            {mode === "login"
              ? "Tu protocolo te está esperando."
              : "Tu perfil es único. Tu protocolo también lo será."}
          </p>

          {notice && (
            <p className="mt-5 rounded-field border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900">
              {notice}
            </p>
          )}

          <form onSubmit={submit} className="mt-7 flex flex-col gap-4">
            <Field label="Email" type="email" value={email} onChange={setEmail} placeholder="tu@email.com" autoComplete="email" />
            <Field
              label="Contraseña" type="password" value={password} onChange={setPassword} placeholder="••••••••"
              autoComplete={mode === "login" ? "current-password" : "new-password"}
            />
            {error && <p className="text-sm text-red-600">{error}</p>}
            <button
              type="submit"
              disabled={busy}
              className="mt-2 w-full rounded-field bg-primary py-3.5 text-[15px] font-medium text-white shadow-card transition hover:opacity-90 disabled:opacity-50"
            >
              {busy ? "Un momento…" : mode === "login" ? "Entrar" : "Crear cuenta"}
            </button>
          </form>

          <div className="mt-6 flex items-center gap-3">
            <span className="h-px flex-1 bg-line" />
            <button
              onClick={() => { setMode(mode === "login" ? "register" : "login"); setError(null); }}
              className="text-sm font-medium text-accent transition hover:opacity-75"
            >
              {mode === "login" ? "¿No tienes cuenta? Regístrate" : "¿Ya tienes cuenta? Entra"}
            </button>
            <span className="h-px flex-1 bg-line" />
          </div>

          <p className="mt-10 text-center font-mono text-[11px] leading-relaxed text-muted/80">
            Tus datos de salud se usan solo para generar tu protocolo.
          </p>
        </div>
      </div>
    </div>
  );
}
