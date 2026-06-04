"use client";

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
import QuestionView from "@/components/QuestionView";
import Results from "@/components/Results";

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

  if (!token)
    return (
      <Shell>
        <AuthScreen notice={authNotice} />
      </Shell>
    );

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
    <Shell>
      {error && <p className="mb-4 text-sm text-red-600">{error}</p>}

      {phase === "onboarding" && (
        <div className="space-y-6 text-center">
          <h1 className="text-3xl font-bold">Bienvenido a Supplement AI</h1>
          <p className="text-gray-600">
            Responde 15 preguntas rápidas sobre tus hábitos y objetivos. Generaremos
            recomendaciones personalizadas y basadas en evidencia.
          </p>
          <button
            onClick={begin}
            disabled={busy}
            className="rounded bg-emerald-600 px-6 py-3 font-medium text-white hover:bg-emerald-700 disabled:opacity-50"
          >
            Empezar cuestionario
          </button>
        </div>
      )}

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
    </Shell>
  );
}

function Shell({ children }: { children: React.ReactNode }) {
  return <main className="mx-auto min-h-screen max-w-2xl px-4 py-12">{children}</main>;
}
