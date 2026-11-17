"use client";

import posthog from "posthog-js";

// Starts PostHog in the browser once, the first time any component asks for it.
// Next.js 14 has no instrumentation-client.ts, so this replaces it.
let started = false;

export function getPostHog() {
  if (typeof window === "undefined") return null;
  if (!started) {
    const key = process.env.NEXT_PUBLIC_POSTHOG_KEY;
    if (!key) return null;
    posthog.init(key, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || "https://eu.i.posthog.com",
      ui_host: "https://eu.posthog.com",
      capture_pageview: true,
    });
    started = true;
  }
  return posthog;
}
