"use client";

import type { RecommendationsResponse } from "@/lib/api";

export default function Results({ data, onRestart }: { data: RecommendationsResponse; onRestart: () => void }) {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Tus recomendaciones</h2>

      {data.advisory && (
        <div className="rounded border border-amber-300 bg-amber-50 px-4 py-3 text-amber-900">
          <strong>Aviso de seguridad. </strong>
          {data.advisory}
        </div>
      )}

      <ul className="space-y-3">
        {data.recommendations.map((r) => (
          <li key={r.slug} className="rounded border border-gray-200 p-4">
            <div className="flex items-baseline justify-between gap-3">
              <h3 className="font-semibold">{r.name}</h3>
              <span className="shrink-0 text-sm text-gray-500">score {r.score.toFixed(2)}</span>
            </div>
            <p className="text-sm text-gray-500">
              {r.category} · evidencia {r.evidence_level} · {r.standard_dose}
            </p>
            {r.safety_flags.map((flag, i) => (
              <p key={i} className="mt-2 text-sm text-amber-700">
                ⚠ {flag}
              </p>
            ))}
          </li>
        ))}
      </ul>

      <p className="rounded bg-gray-100 px-4 py-3 text-sm text-gray-600">{data.disclaimer}</p>

      <button onClick={onRestart} className="text-sm text-emerald-700 hover:underline">
        Repetir cuestionario
      </button>
    </div>
  );
}
