"use client";

import { useState } from "react";
import type { Question } from "@/lib/api";

interface Props {
  question: Question;
  index: number;
  total: number;
  busy: boolean;
  onSubmit: (answer: unknown) => void;
}

export default function QuestionView({ question, index, total, busy, onSubmit }: Props) {
  const [text, setText] = useState("");
  const [selected, setSelected] = useState<string[]>([]);

  const toggle = (value: string) =>
    setSelected((prev) => (prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]));

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-gray-500">
          Pregunta {index} de {total}
        </p>
        <div className="mt-2 h-1.5 w-full rounded bg-gray-200">
          <div className="h-1.5 rounded bg-emerald-500 transition-all" style={{ width: `${(index / total) * 100}%` }} />
        </div>
        <h2 className="mt-4 text-xl font-semibold">{question.prompt}</h2>
      </div>

      {question.type === "single_choice" && (
        <div className="grid gap-2">
          {question.options?.map((o) => (
            <button
              key={o.value}
              disabled={busy}
              onClick={() => onSubmit(o.value)}
              className="rounded border border-gray-300 px-4 py-3 text-left hover:border-emerald-500 hover:bg-emerald-50 disabled:opacity-50"
            >
              {o.label}
            </button>
          ))}
        </div>
      )}

      {question.type === "multi_choice" && (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            onSubmit(selected);
          }}
          className="space-y-4"
        >
          <div className="grid gap-2">
            {question.options?.map((o) => (
              <label key={o.value} className="flex items-center gap-3 rounded border border-gray-300 px-4 py-3">
                <input type="checkbox" checked={selected.includes(o.value)} onChange={() => toggle(o.value)} />
                {o.label}
              </label>
            ))}
          </div>
          <SubmitButton busy={busy} />
        </form>
      )}

      {(question.type === "number" || question.type === "text") && (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            onSubmit(question.type === "number" ? Number(text) : text);
          }}
          className="space-y-4"
        >
          <input
            autoFocus
            type={question.type === "number" ? "number" : "text"}
            value={text}
            required
            onChange={(e) => setText(e.target.value)}
            className="w-full rounded border border-gray-300 px-4 py-3 focus:border-emerald-500 focus:outline-none"
          />
          <SubmitButton busy={busy} />
        </form>
      )}
    </div>
  );
}

function SubmitButton({ busy }: { busy: boolean }) {
  return (
    <button
      type="submit"
      disabled={busy}
      className="rounded bg-emerald-600 px-6 py-2 font-medium text-white hover:bg-emerald-700 disabled:opacity-50"
    >
      Siguiente
    </button>
  );
}
