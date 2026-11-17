
"use client";

import { useEffect, useRef, useState } from "react";
import type { CardSet } from "@/lib/cards";
import { apiError, apiUrl } from "@/lib/api";
import { getPostHog } from "@/lib/posting-client";

const SKIP_REASONS = [
  "not_my_field",
  "not_eligible",
  "hours",
  "pay",
  "not_interested",
  "other",
] as const;

const REASON_LABELS: Record<(typeof SKIP_REASONS)[number], string> = {
  not_my_field: "Not my field",
  not_eligible: "I don't qualify",
  hours: "Hours don't fit",
  pay: "Pay",
  not_interested: "Not interested",
  other: "Other",
};

type Decision = "apply" | "skip";

function anonymousId() {
  const key = "cc_anon";
  try {
    let id = localStorage.getItem(key);
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem(key, id);
    }
    return id;
  } catch {
    return crypto.randomUUID();
  }
}

// Timestamps are taken only in effects and click handlers, never during render.
function nowMs() {
  return Date.now();
}

export function StudentCardSet({ set, source }: { set: CardSet; source: string }) {
  const [choices, setChoices] = useState<Record<string, Decision | null>>({});
  const [skipFor, setSkipFor] = useState<string | null>(null);
  const [pending, setPending] = useState<string | null>(null);
  const [restoring, setRestoring] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<
    { role: string; deadline: string; source_url: string }[] | null
  >(null);

  const anon = useRef("");
  const inFlight = useRef(false);
  const opened = useRef(false);
  const viewed = useRef<Set<string>>(new Set());
  const viewedAt = useRef<Record<string, number>>({});
  const firstViewAt = useRef<number | null>(null);
  const cardEls = useRef<Record<string, HTMLElement | null>>({});

  // student_opens_card_set: once per page load. The ref stops React's double run in dev.
  useEffect(() => {
    if (opened.current) return;
    opened.current = true;
    anon.current = anonymousId();
    try {
      const saved = Number(localStorage.getItem(`cc_first_view:${set.id}:${anon.current}`));
      if (saved > 0 && saved <= nowMs()) firstViewAt.current = saved;
    } catch { /* Storage can be unavailable in private browsing. */ }
    const ph = getPostHog();
    // Same id as the backend's anonymous_id, so browser and server events join up in PostHog.
    ph?.identify(anon.current);
    ph?.capture("student_opens_card_set", { set_id: set.id, source });
  }, [set.id, source]);

  // A reload must display the first decisions already accepted by the server.
  useEffect(() => {
    let cancelled = false;
    setRestoring(true);
    async function restore() {
      try {
        const res = await fetch(apiUrl(`/api/sets/${set.id}/decisions?anonymous_id=${encodeURIComponent(anon.current)}`),
          { cache: "no-store" });
        const data = await res.json();
        if (!res.ok) throw new Error(apiError(data, "Could not load saved decisions."));
        if (cancelled) return;
        setChoices(data.choices);
        setSummary(data.summary);
        setRestoring(false);
      } catch (e) {
        if (!cancelled) setError(`${e instanceof Error ? e.message : "Could not load saved decisions."} Reload to retry.`);
      }
    }
    void restore();
    return () => { cancelled = true; };
  }, [set.id]);

  // student_views_card: once per card, when half of it is on screen.
  useEffect(() => {
    if (summary) return;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          const id = (entry.target as HTMLElement).dataset.cardId;
          const card = set.cards.find((c) => c.id === id);
          if (!card || viewed.current.has(card.id)) continue;
          viewed.current.add(card.id);
          const now = nowMs();
          viewedAt.current[card.id] = now;
          if (firstViewAt.current === null) {
            firstViewAt.current = now;
            try {
              localStorage.setItem(`cc_first_view:${set.id}:${anon.current}`, String(now));
            } catch { /* Keep the in-memory timestamp when storage is unavailable. */ }
          }
          getPostHog()?.capture("student_views_card", {
            set_id: set.id,
            card_id: card.id,
            position: card.position,
          });
        }
      },
      { threshold: 0.5 },
    );
    for (const el of Object.values(cardEls.current)) if (el) observer.observe(el);
    return () => observer.disconnect();
  }, [set, summary]);

  async function decide(cardId: string, decision: Decision, skip_reason?: string) {
    if (restoring || inFlight.current || choices[cardId]) return; // no double taps
    const card = set.cards.find((c) => c.id === cardId);
    if (!card) return;
    inFlight.current = true;

    // Open the post BEFORE waiting for the server: iPhones block tabs opened after a wait.
    if (decision === "apply" && card.source_url) {
      window.open(card.source_url, "_blank", "noopener,noreferrer");
    }

    setPending(cardId);
    setError(null);
    const now = nowMs();
    try {
      const res = await fetch(apiUrl("/api/decide"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          set_id: set.id,
          card_id: cardId,
          position: card.position,
          decision,
          skip_reason: skip_reason || null,
          ms_on_card: viewedAt.current[cardId] ? Math.max(0, now - viewedAt.current[cardId]) : null,
          anonymous_id: anon.current || anonymousId(),
          ms_total: firstViewAt.current ? Math.max(0, now - firstViewAt.current) : null,
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        setError(apiError(data, "Could not save. Check your connection and tap again."));
        return;
      }
      setChoices((prev) => ({ ...prev, [cardId]: data.decision }));
      setSkipFor(null);
      if (data.summary) setSummary(data.summary);
    } catch {
      setError("Could not save. Check your connection and tap again.");
    } finally {
      inFlight.current = false;
      setPending(null);
    }
  }

  return (
    <section>
      {error && (
        <p className="note" role="alert" style={{ color: "#b42318" }}>
          {error}
        </p>
      )}

      {set.cards.map((card) => {
        const choice = choices[card.id];
        return (
          <article
            className="card"
            key={card.id}
            data-card-id={card.id}
            ref={(el) => {
              cardEls.current[card.id] = el;
            }}
          >
            <p className="note">
              {card.position}/5 · {card.source} · {card.field}
            </p>
            <h2 style={{ margin: "0.2rem 0 0.6rem", fontSize: "1.2rem" }}>{card.role}</h2>
            <p style={{ marginTop: 0 }}>{card.company}</p>
            <div className="meta">
              <div>
                <strong>Students OK</strong>
                <div>{card.students_ok ? "Yes" : "No"}</div>
              </div>
              <div>
                <strong>Experience</strong>
                <div>{card.experience}</div>
              </div>
              <div>
                <strong>Hours</strong>
                <div>{card.hours}</div>
              </div>
              <div>
                <strong>Pay</strong>
                <div>{card.pay?.trim() ? card.pay : "Pay: not stated"}</div>
              </div>
              <div>
                <strong>Deadline</strong>
                <div>{card.deadline || "Not stated"}</div>
              </div>
            </div>
            {choice ? (
              <p className="note">{choice === "apply" ? "Applying ↗" : "Skipped"}</p>
            ) : (
              <div className="actions">
                <button
                  type="button"
                  className="skip"
                  disabled={restoring || !!pending}
                  onClick={() => setSkipFor(card.id)}
                >
                  Skip
                </button>
                <button
                  type="button"
                  className="apply"
                  disabled={restoring || !!pending}
                  onClick={() => decide(card.id, "apply")}
                >
                  {pending === card.id ? "Saving…" : "Apply"}
                </button>
              </div>
            )}
            {skipFor === card.id && !choice && (
              <div style={{ marginTop: "0.75rem" }}>
                <p className="note">Why skip?</p>
                <div className="actions" style={{ flexWrap: "wrap" }}>
                  {SKIP_REASONS.map((reason) => (
                    <button
                      key={reason}
                      type="button"
                      className="skip"
                      disabled={restoring || !!pending}
                      onClick={() => decide(card.id, "skip", reason)}
                    >
                      {REASON_LABELS[reason]}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </article>
        );
      })}

      {summary && (
        <section className="card">
          <h2 style={{ marginTop: 0 }}>Your apply list</h2>
          {summary.length === 0 ? (
            <p>You skipped all five.</p>
          ) : (
            <ul>
              {summary.map((row) => (
                <li key={row.source_url}>
                  <a href={row.source_url} target="_blank" rel="noreferrer">
                    {row.role}
                  </a>{" "}
                  · deadline {row.deadline || "not stated"}
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </section>
  );
}
