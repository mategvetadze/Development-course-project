"use client";

import { useEffect, useMemo, useState } from "react";
import type { CardSet } from "@/lib/cards";
import { apiUrl } from "@/lib/api";

const SKIP_REASONS = [
  "not_my_field",
  "not_eligible",
  "hours",
  "pay",
  "not_interested",
  "other",
] as const;

type Decision = "apply" | "skip";

function anonymousId() {
  const key = "cc_anon";
  let id = typeof window !== "undefined" ? localStorage.getItem(key) : null;
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(key, id);
  }
  return id;
}

export function StudentCardSet({ set, source }: { set: CardSet; source: string }) {
  const [choices, setChoices] = useState<Record<string, Decision | null>>({});
  const [skipFor, setSkipFor] = useState<string | null>(null);
  const [summary, setSummary] = useState<
    { role: string; deadline: string; source_url: string }[] | null
  >(null);
  const [startedAt] = useState(() => Date.now());
  const anon = useMemo(() => (typeof window === "undefined" ? "" : anonymousId()), []);

  useEffect(() => {
    // student_opens_card_set — wire PostHog client in S5
    console.info("student_opens_card_set", { set_id: set.id, source });
  }, [set.id, source]);

  async function decide(cardId: string, decision: Decision, skip_reason?: string) {
    const card = set.cards.find((c) => c.id === cardId);
    if (!card) return;
    const ms_on_card = Date.now() - startedAt;
    const res = await fetch(apiUrl("/api/decide"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        set_id: set.id,
        card_id: cardId,
        position: card.position,
        decision,
        skip_reason: skip_reason || null,
        ms_on_card,
        anonymous_id: anon,
        ms_total: Date.now() - startedAt,
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      alert(data.error || "Could not save decision");
      return;
    }
    setChoices((prev) => ({ ...prev, [cardId]: decision }));
    setSkipFor(null);
    if (decision === "apply" && card.source_url) {
      window.open(card.source_url, "_blank", "noopener,noreferrer");
    }
    if (data.summary) setSummary(data.summary);
  }

  return (
    <section>
      {set.cards.map((card) => {
        const choice = choices[card.id];
        return (
          <article className="card" key={card.id}>
            <p className="note">
              {card.position}/5 · {card.source} · {card.field}
            </p>
            <h2 style={{ margin: "0.2rem 0 0.6rem", fontSize: "1.2rem" }}>
              {card.role}
            </h2>
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
                <div>{card.deadline}</div>
              </div>
            </div>
            {choice ? (
              <p className="note">Recorded: {choice}</p>
            ) : (
              <div className="actions">
                <button type="button" className="skip" onClick={() => setSkipFor(card.id)}>
                  Skip
                </button>
                <button
                  type="button"
                  className="apply"
                  onClick={() => decide(card.id, "apply")}
                >
                  Apply
                </button>
              </div>
            )}
            {skipFor === card.id && (
              <div style={{ marginTop: "0.75rem" }}>
                <p className="note">Why skip?</p>
                <div className="actions" style={{ flexWrap: "wrap" }}>
                  {SKIP_REASONS.map((reason) => (
                    <button
                      key={reason}
                      type="button"
                      className="skip"
                      onClick={() => decide(card.id, "skip", reason)}
                    >
                      {reason}
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
                  · deadline {row.deadline}
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </section>
  );
}
