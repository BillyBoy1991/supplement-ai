"use client";

/* Supplement AI — resultados rediseñados.
   Sustituye a src/components/Results.tsx (misma API de props).
   Nota: usa el campo opcional `citations?: string[]` en Recommendation (ver README). */

import type { Recommendation, RecommendationsResponse } from "@/lib/api";

function ScoreRing({ score }: { score: number }) {
  const R = 24;
  const C = 2 * Math.PI * R;
  const pct = Math.round(score * 100);
  return (
    <div className="relative h-[68px] w-[68px] shrink-0">
      <svg width="68" height="68" viewBox="0 0 68 68" className="-rotate-90">
        <circle cx="34" cy="34" r={R} fill="none" strokeWidth="5" stroke="var(--sa-line)" />
        <circle
          cx="34" cy="34" r={R} fill="none" strokeWidth="5" strokeLinecap="round"
          stroke="var(--sa-accent)" strokeDasharray={C} strokeDashoffset={C * (1 - score)}
          className="transition-all duration-700 ease-out"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-display text-lg font-semibold leading-none tabular-nums">{pct}</span>
        <span className="font-mono text-[8px] uppercase tracking-[0.12em] text-muted">match</span>
      </div>
    </div>
  );
}

function EvidenceBadge({ level }: { level: string }) {
  return (
    <span className="inline-flex items-center gap-1.5 rounded-full border border-line bg-mist px-2.5 py-0.5 font-mono text-[11px] text-ink">
      <span className="h-1.5 w-1.5 rounded-full bg-accent" />
      Evidencia {level}
    </span>
  );
}

function NeedProfile({ scores }: { scores: Record<string, number> }) {
  const entries = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  return (
    <section className="rounded-card border border-line bg-white p-6 shadow-card sm:p-7">
      <h3 className="font-display text-lg font-semibold tracking-tight">Tu perfil de necesidades</h3>
      <p className="mt-1 text-sm text-muted">Dónde tus respuestas señalan más margen de mejora.</p>
      <div className="mt-6 grid gap-3.5">
        {entries.map(([label, value]) => (
          <div key={label} className="grid grid-cols-[110px_1fr_40px] items-center gap-3 sm:grid-cols-[130px_1fr_44px]">
            <span className="text-sm text-ink">{label}</span>
            <div className="h-1.5 overflow-hidden rounded-full bg-line">
              <div
                className="h-1.5 rounded-full bg-primary transition-all duration-700 ease-out"
                style={{ width: `${value * 100}%` }}
              />
            </div>
            <span className="text-right font-mono text-[11px] tabular-nums text-muted">
              {Math.round(value * 100)}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}

function RecommendationCard({ r, rank }: { r: Recommendation; rank: number }) {
  return (
    <article className="rounded-card border border-line bg-white p-6 shadow-card transition hover:shadow-lift sm:p-7">
      <div className="flex items-start gap-5">
        <ScoreRing score={r.score} />
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1.5">
            <span className="font-mono text-[11px] text-muted">{String(rank).padStart(2, "0")}</span>
            <h3 className="font-display text-xl font-semibold tracking-tight">{r.name}</h3>
          </div>
          <div className="mt-2 flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-soft px-2.5 py-0.5 text-[12px] font-medium text-primary">
              {r.category}
            </span>
            <EvidenceBadge level={r.evidence_level} />
          </div>
        </div>
      </div>

      <div className="mt-5 flex items-baseline gap-3 border-t border-line pt-4">
        <span className="font-mono text-[11px] uppercase tracking-[0.14em] text-muted">Dosis</span>
        <span className="text-[15px] font-medium text-ink">{r.standard_dose}</span>
        {r.mechanisms?.length > 0 && (
          <span className="ml-auto hidden text-[12px] text-muted sm:block">{r.mechanisms.join(" · ")}</span>
        )}
      </div>

      {r.llm_explanation?.trim() && (
        <div className="mt-4 rounded-field bg-mist px-5 py-4">
          <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-accent">Análisis IA</p>
          <p className="mt-1.5 text-[14px] italic leading-relaxed text-ink/85">{r.llm_explanation}</p>
        </div>
      )}

      {(r.citations?.length ?? 0) > 0 && (
        <div className="mt-4 flex flex-wrap gap-2">
          {r.citations!.map((c) => (
            <span key={c} className="rounded border border-line bg-white px-2 py-1 font-mono text-[11px] text-muted">
              [{c}]
            </span>
          ))}
        </div>
      )}

      {r.safety_flags.map((flag, i) => (
        <p key={i} className="mt-4 rounded-field border border-amber-200 bg-amber-50 px-4 py-2.5 text-[13px] text-amber-900">
          ⚠ {flag}
        </p>
      ))}
    </article>
  );
}

export default function Results({ data, onRestart }: { data: RecommendationsResponse; onRestart: () => void }) {
  return (
    <div className="mx-auto w-full max-w-2xl px-6 pb-24 pt-12 sm:pt-16">
      <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-accent">
        Protocolo · {data.recommendations.length} recomendaciones
      </p>
      <h2 className="mt-3 font-display text-3xl font-semibold tracking-tight sm:text-4xl">
        Tu protocolo personalizado
      </h2>
      <p className="mt-3 max-w-lg text-[15px] leading-relaxed text-muted">
        Construido a partir de tus 15 respuestas y de evidencia publicada revisada por pares.
      </p>

      {data.advisory && (
        <div className="mt-7 rounded-card border border-amber-200 bg-amber-50 px-5 py-4 text-sm leading-relaxed text-amber-900">
          <strong className="font-semibold">Aviso de seguridad. </strong>
          {data.advisory}
        </div>
      )}

      <div className="mt-7">
        <NeedProfile scores={data.need_scores} />
      </div>

      <div className="mt-7 flex flex-col gap-5">
        {data.recommendations.map((r, i) => (
          <RecommendationCard key={r.slug} r={r} rank={i + 1} />
        ))}
      </div>

      <p className="mt-9 border-t border-line pt-6 font-mono text-[11px] leading-relaxed text-muted">
        {data.disclaimer}
      </p>

      <button onClick={onRestart} className="mt-6 text-sm font-medium text-accent transition hover:opacity-75">
        ↺ Repetir cuestionario
      </button>
    </div>
  );
}
