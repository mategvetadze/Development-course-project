"use client";

import { useState } from "react";
import { apiUrl } from "@/lib/api";

const emptyCard = () => ({
  role: "",
  company: "",
  field: "",
  source: "",
  source_url: "",
  students_ok: true,
  experience: "",
  hours: "",
  pay: "",
  deadline: "",
});

export function CuratorForm({ token }: { token: string }) {
  const [cards, setCards] = useState(() =>
    Array.from({ length: 5 }, () => emptyCard())
  );
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  function update(i: number, key: string, value: string | boolean) {
    setCards((prev) =>
      prev.map((card, idx) => (idx === i ? { ...card, [key]: value } : card))
    );
  }

  async function publish() {
    setBusy(true);
    setMessage("");
    try {
      const res = await fetch(apiUrl("/api/publish"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Admin-Token": token,
        },
        body: JSON.stringify({ cards }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Publish failed");
      setMessage(`Published: ${data.card_count} cards (set ${data.set_id})`);
    } catch (e) {
      setMessage(e instanceof Error ? e.message : "Publish failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section>
      {cards.map((card, i) => (
        <div className="card" key={i}>
          <p className="note">Card {i + 1}</p>
          {(
            [
              ["role", "Role"],
              ["company", "Company"],
              ["field", "Field"],
              ["source", "Source"],
              ["source_url", "Source URL"],
              ["experience", "Experience required"],
              ["hours", "Hours"],
              ["pay", "Pay"],
              ["deadline", "Deadline (YYYY-MM-DD)"],
            ] as const
          ).map(([key, label]) => (
            <label key={key} style={{ display: "block", marginBottom: "0.4rem" }}>
              <span className="note">{label}</span>
              <input
                style={{ width: "100%", padding: "0.45rem" }}
                value={String(card[key])}
                onChange={(e) => update(i, key, e.target.value)}
              />
            </label>
          ))}
          <label className="note">
            <input
              type="checkbox"
              checked={card.students_ok}
              onChange={(e) => update(i, "students_ok", e.target.checked)}
            />{" "}
            Students / first-years OK
          </label>
        </div>
      ))}
      <button type="button" className="apply" disabled={busy} onClick={publish}>
        {busy ? "Publishing…" : "Publish"}
      </button>
      {message && <p className="note">{message}</p>}
    </section>
  );
}
