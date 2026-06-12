"use client";

/* Supplement AI — sustituye a src/app/page.tsx.
   Misma máquina de fases; añade cabecera con logo y usa el nuevo Onboarding. */

import { useState } from "react";
import {
  ApiError,
  questionnaire,
  recommendations,
  type Question,
  type RecommendationsResponse,
} from "@/lib/api";
import { useAuth } from "@/lib/auth";
import AuthScreen from "@/components/AuthScreen";
import Onboarding from "@/components/Onboarding";
import QuestionView from "@/components/QuestionView";
import Results from "@/components/Results";
import { LogoLockup } from "@/components/Logo";

const TOTAL_QUESTIONS = 15;

type Phase = "onboarding" | "questionnaire" | "results";

export default function Home() {
  const { token, logout } = useAuth();
  const [authNotice, setAuthNotice] = useState<string>();

  const [phase, setPhase] = useState<Phase>("onboarding");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [question, setQuestion] = useState<Question | null>(null);
  const [index, setIndex] = useState(0);
  const [result, setResult] = useState<RecommendationsResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const reset = () => {
    setPhase("onboarding");
    setSessionId(null);
    setQuestion(null);
    setIndex(0);
    setResult(null);
  };

  // Ejecuta una llamada protegida; si el token caduca (401) cierra sesión.
  const guard = async (fn: () => Promise<void>) => {
    setError(null);
    setBusy(true);
    try {
      await fn();
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        setAuthNotice("Tu sesión ha expirado. Vuelve a entrar.");
        reset();
        logout();
      } else {
        setError(err instanceof ApiError ? err.message : "Error de conexión");
      }
    } finally {
      setBusy(false);
    }
  };

  if (!token) return <AuthScreen notice={authNotice} />;

  const begin = () =>
    guard(async () => {
      const step = await questionnaire.start(token);
      setSessionId(step.session_id);
      setQuestion(step.question);
      setIndex(1);
      setPhase("questionnaire");
    });

  const handleAnswer = (answer: unknown) =>
    guard(async () => {
      if (!sessionId) return;
      const step = await questionnaire.answer(token, sessionId, answer);
      if (step.finished) {
        setResult(await recommendations.get(token, sessionId));
        setPhase("results");
      } else {
        setQuestion(step.question);
        setIndex((i) => i + 1);
      }
    });

  return (
    <main className="min-h-screen bg-mist">
      <header className="sticky top-0 z-10 border-b border-line bg-mist/85 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-3xl items-center justify-between px-6">
          <LogoLockup size={26} />
          <button onClick={logout} className="text-sm text-muted transition hover:text-ink">
            Salir
          </button>
        </div>
      </header>

      {error && (
        <p className="mx-auto mt-4 max-w-xl rounded-field border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </p>
      )}

      {phase === "onboarding" && <Onboarding busy={busy} onBegin={begin} />}

      {phase === "questionnaire" && question && (
        <QuestionView
          key={question.id}
          question={question}
          index={index}
          total={TOTAL_QUESTIONS}
          busy={busy}
          onSubmit={handleAnswer}
        />
      )}

      {phase === "results" && result && <Results data={result} onRestart={reset} />}
    </main>
  );
}
