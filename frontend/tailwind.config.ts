import type { Config } from "tailwindcss";

/* Supplement AI — sustituye a tailwind.config.ts */
const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "var(--sa-primary)",
        accent: "var(--sa-accent)",
        ink: "var(--sa-ink)",
        muted: "var(--sa-muted)",
        mist: "var(--sa-mist)",
        line: "var(--sa-line)",
        soft: "var(--sa-soft)",
      },
      fontFamily: {
        display: ["var(--sa-font-display)"],
        body: ["var(--sa-font-body)"],
        mono: ["var(--font-geist-mono)", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      borderRadius: {
        card: "var(--sa-radius)",
        field: "calc(var(--sa-radius) - 4px)",
      },
      boxShadow: {
        card: "0 1px 2px rgba(14,42,35,.04), 0 8px 24px -12px rgba(14,42,35,.12)",
        lift: "0 2px 4px rgba(14,42,35,.06), 0 16px 40px -16px rgba(14,42,35,.18)",
      },
    },
  },
  plugins: [],
};
export default config;
