import type { Metadata } from "next";
import { Schibsted_Grotesk, Instrument_Sans } from "next/font/google";
import localFont from "next/font/local";
import "./globals.css";
import { AuthProvider } from "@/lib/auth";

/* Supplement AI — sustituye a src/app/layout.tsx.
   Schibsted Grotesk (titulares) + Instrument Sans (texto) vía next/font/google;
   se conserva Geist Mono local para datos y microetiquetas. */

const schibsted = Schibsted_Grotesk({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-schibsted",
});

const instrument = Instrument_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-instrument",
});

const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Supplement AI",
  description: "Recomendaciones personalizadas de suplementos basadas en evidencia.",
  openGraph: {
    title: "Supplement AI",
    description: "Recomendaciones personalizadas de suplementos basadas en evidencia.",
    url: "https://supplement.billytheboy.com",
    siteName: "Supplement AI",
    images: [
      {
        url: "https://supplement.billytheboy.com/logo/supplement-ai-logo.svg",
        width: 400,
        height: 200,
        alt: "Supplement AI logo",
      },
    ],
    locale: "es_ES",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className={`${schibsted.variable} ${instrument.variable} ${geistMono.variable} antialiased`}>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
