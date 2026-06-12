"use client";

/* Supplement AI — bienvenida del onboarding.
   Nuevo componente: extrae la fase "onboarding" de src/app/page.tsx. */

import { LogoMark } from "@/components/Logo";

const STEPS = [
  { n: "01", title: "Responde", text: "15 preguntas sobre hábitos, dieta y objetivos. Unos 3 minutos." },
  { n: "02", title: "Analizamos", text: "Cruzamos tu perfil con literatura científica publicada." },
  { n: "03", title: "Tu protocolo", text: "Recomendaciones priorizadas, con dosis y evidencia citada." },
];

export default function Onboarding({ busy, onBegin }: { busy: boolean; onBegin: () => void }) {
  return (
    <div className="mx-auto w-full max-w-3xl px-6 pb-20 pt-14 sm:pt-24">
      <div className="mx-auto max-w-xl text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl border border-line bg-white shadow-card">
          <LogoMark size={38} />
        </div>
        <h1 className="mt-8 font-display text-4xl font-semibold leading-[1.1] tracking-tight sm:text-5xl">
          Tu protocolo empieza con 15 preguntas.
        </h1>
        <p className="mx-auto mt-5 max-w-md text-[15px] leading-relaxed text-muted">
          Cuéntanos cómo vives, entrenas y duermes. Construiremos un protocolo de suplementación
          a tu medida, basado en evidencia — no en tendencias.
        </p>
      </div>

      <div className="mt-12 grid gap-4 sm:grid-cols-3">
        {STEPS.map((s) => (
          <div key={s.n} className="rounded-card border border-line bg-white p-6 shadow-card">
            <p className="font-mono text-[11px] tracking-[0.18em] text-accent">{s.n}</p>
            <h3 className="mt-3 font-display text-lg font-semibold tracking-tight">{s.title}</h3>
            <p className="mt-1.5 text-sm leading-relaxed text-muted">{s.text}</p>
          </div>
        ))}
      </div>

      <div className="mt-12 flex flex-col items-center gap-4">
        <button
          onClick={onBegin}
          disabled={busy}
          className="rounded-field bg-primary px-10 py-4 text-[15px] font-medium text-white shadow-lift transition hover:opacity-90 disabled:opacity-50"
        >
          Empezar cuestionario
        </button>
        <p className="font-mono text-[11px] uppercase tracking-[0.14em] text-muted">
          ≈ 3 minutos · Puedes pausar cuando quieras
        </p>
      </div>
    </div>
  );
}
