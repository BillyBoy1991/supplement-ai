"use client";

/* Supplement AI — vista de pregunta rediseñada.
   Sustituye a src/components/QuestionView.tsx (misma API de props). */

import { useState } from "react";
import type { Question } from "@/lib/api";

interface Props {
  question: Question;
  index: number;
  total: number;
  busy: boolean;
  onSubmit: (answer: unknown) => void;
}

const MICROCOPY = [
  "Cada respuesta afina tu perfil.",
  "La precisión está en los detalles.",
  "Tu protocolo se construye con esto.",
  "Sin datos genéricos: solo tu contexto.",
  "Casi todo lo importante es un hábito.",
];

export default function QuestionView({ question, index, total, busy, onSubmit }: Props) {
  const [text, setText] = useState("");
  const [selected, setSelected] = useState<string[]>([]);

  const toggle = (value: string) =>
    setSelected((prev) => (prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]));

  const pct = Math.round(((index - 1) / total) * 100);

  return (
    <div className="mx-auto w-full max-w-xl px-6 pb-20 pt-12 sm:pt-16">
      {/* Progreso */}
      <div className="flex items-baseline justify-between">
        <p className="font-mono text-[11px] uppercase tracking-[0.16em] text-muted">
          Pregunta {index} de {total}
        </p>
        <p className="font-mono text-[11px] tabular-nums text-accent">{pct}%</p>
      </div>
      <div className="mt-2.5 h-1 w-full overflow-hidden rounded-full bg-line">
        <div
          className="h-1 rounded-full bg-accent transition-all duration-700 ease-out"
          style={{ width: `${pct}%` }}
        />
      </div>
      <p className="mt-3 text-[13px] italic text-muted">{MICROCOPY[(index - 1) % MICROCOPY.length]}</p>

      <h2 className="mt-9 font-display text-2xl font-semibold leading-snug tracking-tight sm:text-[28px]">
        {question.prompt}
      </h2>

      <div className="mt-8">
        {question.type === "single_choice" && (
          <div className="grid gap-2.5">
            {question.options?.map((o) => (
              <button
                key={o.value}
                disabled={busy}
                onClick={() => onSubmit(o.value)}
                className="group flex items-center justify-between rounded-field border border-line bg-white px-5 py-4 text-left text-[15px] shadow-card transition hover:border-accent hover:shadow-lift disabled:opacity-50"
              >
                <span>{o.label}</span>
                <span className="text-line transition group-hover:text-accent">→</span>
              </button>
            ))}
          </div>
        )}

        {question.type === "multi_choice" && (
          <form
            onSubmit={(e) => { e.preventDefault(); onSubmit(selected); }}
            className="flex flex-col gap-6"
          >
            <div className="grid gap-2.5">
              {question.options?.map((o) => {
                const on = selected.includes(o.value);
                return (
                  <label
                    key={o.value}
                    className={`flex cursor-pointer items-center gap-3.5 rounded-field border bg-white px-5 py-4 text-[15px] shadow-card transition ${
                      on ? "border-accent ring-2 ring-accent/15" : "border-line hover:border-accent/50"
                    }`}
                  >
                    <input type="checkbox" className="peer sr-only" checked={on} onChange={() => toggle(o.value)} />
                    <span
                      className={`flex h-5 w-5 shrink-0 items-center justify-center rounded border text-[11px] text-white transition ${
                        on ? "border-accent bg-accent" : "border-line bg-white"
                      }`}
                    >
                      {on ? "✓" : ""}
                    </span>
                    <span>{o.label}</span>
                  </label>
                );
              })}
            </div>
            <NextButton busy={busy} disabled={selected.length === 0} />
          </form>
        )}

        {(question.type === "number" || question.type === "text") && (
          <form
            onSubmit={(e) => { e.preventDefault(); onSubmit(question.type === "number" ? Number(text) : text); }}
            className="flex flex-col gap-6"
          >
            <input
              autoFocus
              type={question.type === "number" ? "number" : "text"}
              value={text}
              required
              placeholder={question.type === "number" ? "0" : "Escribe tu respuesta…"}
              onChange={(e) => setText(e.target.value)}
              className="w-full rounded-field border border-line bg-white px-5 py-4 text-lg shadow-card outline-none transition placeholder:text-muted/50 focus:border-accent focus:ring-2 focus:ring-accent/15"
            />
            <NextButton busy={busy} disabled={text.trim() === ""} />
          </form>
        )}
      </div>
    </div>
  );
}

function NextButton({ busy, disabled }: { busy: boolean; disabled?: boolean }) {
  return (
    <button
      type="submit"
      disabled={busy || disabled}
      className="self-start rounded-field bg-primary px-8 py-3.5 text-[15px] font-medium text-white shadow-card transition hover:opacity-90 disabled:opacity-40"
    >
      Siguiente
    </button>
  );
}
