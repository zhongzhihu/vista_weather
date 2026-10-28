const ALLOWED_ORIGINS = new Set([
  "https://vistaweather.com",
  "https://www.vistaweather.com",
  "https://vistaweatherapp.netlify.app",
  "https://zhongzhihu.github.io",
]);

export default async function region(request, context) {
  const headers = new Headers({
    "Cache-Control": "no-store",
    "Content-Type": "application/json; charset=utf-8",
  });
  const origin = request.headers.get("origin");

  if (origin && ALLOWED_ORIGINS.has(origin)) {
    headers.set("Access-Control-Allow-Origin", origin);
    headers.set("Access-Control-Allow-Methods", "GET, OPTIONS");
    headers.set("Access-Control-Allow-Headers", "Accept");
    headers.set("Vary", "Origin");
  }

  if (request.method === "OPTIONS") return new Response(null, { status: 204, headers });

  const rawCountryCode = context.geo?.country?.code;
  const countryCode = typeof rawCountryCode === "string" && /^[A-Za-z]{2}$/.test(rawCountryCode)
    ? rawCountryCode.toUpperCase()
    : null;

  // Return only the country code; the visitor's IP address is never sent to the page.
  return new Response(JSON.stringify({ countryCode }), { status: 200, headers });
}

export const config = { path: "/api/region" };
