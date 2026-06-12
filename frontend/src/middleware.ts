import { NextRequest, NextResponse } from "next/server";

const BOT_AGENTS = [
  "facebookexternalhit",
  "Facebot",
  "WhatsApp",
  "Twitterbot",
  "LinkedInBot",
  "Slackbot",
];

export function middleware(request: NextRequest) {
  const ua = request.headers.get("user-agent") ?? "";
  const isBot = BOT_AGENTS.some((bot) => ua.includes(bot));

  if (isBot && request.nextUrl.pathname === "/") {
    const html = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <title>Supplement AI</title>
  <meta name="description" content="Recomendaciones personalizadas de suplementos basadas en evidencia." />
  <meta property="og:title" content="Supplement AI" />
  <meta property="og:description" content="Recomendaciones personalizadas de suplementos basadas en evidencia." />
  <meta property="og:url" content="https://supplement.billytheboy.com" />
  <meta property="og:image" content="https://supplement.billytheboy.com/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="es_ES" />
  <meta property="og:site_name" content="Supplement AI" />
</head>
<body></body>
</html>`;
    return new NextResponse(html, {
      status: 200,
      headers: { "Content-Type": "text/html" },
    });
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/"],
};
