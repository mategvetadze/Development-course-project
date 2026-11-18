
"use client";

import { useState } from "react";
import { CuratorForm } from "@/components/CuratorForm";

export default function AdminPage() {
  const [draft, setDraft] = useState("");
  const [token, setToken] = useState("");

  return (
    <main>
      <p className="note">CareerCards · curator</p>
      <h1>Publish this week&apos;s five cards</h1>
      <p>
        Fill eligibility, hours, pay and deadline so a student
        can decide without opening the original post.
      </p>

      {token ? (
        <CuratorForm token={token} />
      ) : (
        <form
          onSubmit={(event) => {
            event.preventDefault();
            setToken(draft);
            setDraft("");
          }}
        >
          <label>
            Admin token{" "}
            <input
              type="password"
              autoComplete="off"
              required
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
            />
          </label>{" "}
          <button className="apply" type="submit">
            Open publish form
          </button>
        </form>
      )}
    </main>
  );
}
