/* Supplement AI — logo como componente React.
   Colocar en src/components/Logo.tsx */

const HEX_PATH = "M24 10 L36.12 17 L36.12 31 L24 38 L11.88 31 L11.88 17 Z";

export function LogoMark({ size = 32, tone = "dark" }: { size?: number; tone?: "dark" | "light" }) {
  const stroke = tone === "dark" ? "var(--sa-primary)" : "#ffffff";
  const node = tone === "dark" ? "var(--sa-primary)" : "#ffffff";
  const accent = tone === "dark" ? "var(--sa-accent)" : "#7fc8a4";
  return (
    <svg width={size} height={size} viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <path d={HEX_PATH} stroke={stroke} strokeWidth="2.6" strokeLinejoin="round" />
      <circle cx="24" cy="10" r="3.8" fill={accent} />
      <circle cx="11.88" cy="31" r="3.4" fill={node} />
      <circle cx="36.12" cy="31" r="3.4" fill={node} />
    </svg>
  );
}

export function LogoLockup({ size = 28, tone = "dark" }: { size?: number; tone?: "dark" | "light" }) {
  const text = tone === "dark" ? "text-ink" : "text-white";
  return (
    <span className="inline-flex items-center gap-2.5">
      <LogoMark size={size} tone={tone} />
      <span
        className={`whitespace-nowrap font-display font-semibold tracking-tight ${text}`}
        style={{ fontSize: size * 0.68 }}
      >
        Supplement <span className="text-accent">AI</span>
      </span>
    </span>
  );
}
