const region = process.env.NEXT_PUBLIC_POSTHOG_REGION || "eu";
if (!["eu", "us"].includes(region)) throw new Error("NEXT_PUBLIC_POSTHOG_REGION must be eu or us");
if (process.env.VERCEL_ENV === "production" || process.env.APP_ENV === "production") {
  const api = process.env.NEXT_PUBLIC_API_URL;
  const origin = api && URL.canParse(api) ? new URL(api) : null;
  if (!origin || origin.protocol !== "https:" || origin.username || origin.password || origin.search || origin.hash
      || !["", "/"].includes(origin.pathname) || ["localhost", "127.0.0.1", "[::1]"].includes(origin.hostname)) {
    throw new Error("Production NEXT_PUBLIC_API_URL must be the backend HTTPS origin");
  }
  if (!process.env.NEXT_PUBLIC_POSTHOG_KEY) throw new Error("Production NEXT_PUBLIC_POSTHOG_KEY is required");
}

/** @type {import('next').NextConfig} */
const nextConfig = {
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return [
      { source: "/ingest/static/:path*", destination: `https://${region}-assets.i.posthog.com/static/:path*` },
      { source: "/ingest/array/:path*", destination: `https://${region}-assets.i.posthog.com/array/:path*` },
      { source: "/ingest/:path*", destination: `https://${region}.i.posthog.com/:path*` },
    ];
  },
  async headers() {
    return [{ source: "/:path*", headers: [
      { key: "Referrer-Policy", value: "no-referrer" },
      { key: "X-Content-Type-Options", value: "nosniff" },
    ] }, { source: "/admin/:path*", headers: [
      { key: "Cache-Control", value: "no-store" },
      { key: "X-Robots-Tag", value: "noindex, nofollow" },
    ] }];
  },
};

export default nextConfig;
