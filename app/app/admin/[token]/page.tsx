"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { CuratorForm } from "@/components/CuratorForm";
import { apiUrl } from "@/lib/api";

export default function AdminPage() {
  const params = useParams<{ token: string }>();
  const [allowed, setAllowed] = useState<boolean | null>(null);

  useEffect(() => {
    // Token is checked on the Python publish endpoint; page itself is reachable
    // with any path token so the curator can open a bookmark. Wrong token → 404 on Publish.
    setAllowed(Boolean(params.token && params.token !== "REPLACE_WITH_ADMIN_TOKEN"));
  }, [params.token]);

  if (allowed === null) return null;
  if (!allowed) {
    return (
      <main>
        <p className="error">Set a real ADMIN_TOKEN in the backend and open /admin/&lt;token&gt;.</p>
        <p className="note">API: {apiUrl("/health")}</p>
      </main>
    );
  }

  return (
    <main>
      <p className="note">CareerCards · curator (Python API)</p>
      <h1>Publish this week&apos;s five cards</h1>
      <p>
        Fill eligibility, hours, pay and deadline so a student can decide without
        opening the original post.
      </p>
      <CuratorForm token={params.token} />
    </main>
  );
}
