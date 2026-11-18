
"use client";

import posthog from "posthog-js";

// Starts PostHog in the browser once, the first time any component asks for it.
let started = false;

export function normalizeSource(source: unknown) {
  return typeof source === "string" && ["friend", "groupchat", "other"].includes(source) ? source : "other";
}

export function getPostHog(anonymousId?: string) {
  if (typeof window === "undefined") return null;
  if (!started) {
    const key = process.env.NEXT_PUBLIC_POSTHOG_KEY;
    if (!key) return null;
    posthog.init(key, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || "/ingest",
      ui_host: process.env.NEXT_PUBLIC_POSTHOG_UI_HOST || "https://eu.posthog.com",
      bootstrap: anonymousId ? { distinctID: anonymousId, isIdentifiedID: false } : undefined,
      person_profiles: "never",
      capture_pageview: false,
      capture_pageleave: false,
      autocapture: false,
      disable_session_recording: true,
      disable_surveys: true,
      advanced_disable_feature_flags: true,
      ip: false,
      before_send: (event) => {
        if (!event || !["student_opens_card_set", "student_views_card"].includes(event.event)) return null;
        // SDK defaults include URLs/referrers. Keep only the documented anonymous
        // facts so query strings, contacts and admin tokens cannot ride along.
        const allowed = new Set(["distinct_id", "set_id", "card_id", "position", "source", "environment",
          "is_internal", "$lib", "$lib_version", "$insert_id"]);
        event.properties = Object.fromEntries(Object.entries(event.properties).filter(([key]) => allowed.has(key)));
        event.properties.$geoip_disable = true;
        return event;
      },
    });
    started = true;
  }
  return posthog;
}
