import Link from "next/link";
import { StudentCardSet } from "@/components/StudentCardSet";
import { getLatestPublishedSet } from "@/lib/cards";

export const dynamic = "force-dynamic";

export default async function HomePage({
  searchParams,
}: {
  searchParams: { src?: string };
}) {
  const source = searchParams.src || "other";
  let set = null as Awaited<ReturnType<typeof getLatestPublishedSet>>;
  let error: string | null = null;

  try {
    set = await getLatestPublishedSet();
  } catch (e) {
    error = e instanceof Error ? e.message : "Could not load cards";
  }

  return (
    <main>
      <p className="note">CareerCards · student view</p>
      <h1>Five openings. One decision each.</h1>
      <p>
        Read who can apply, experience, hours, pay and deadline. Tap Apply or Skip —
        you should not need to open the original post just to see if you qualify.
      </p>
      {error ? (
        <div className="card">
          <p className="error">{error}</p>
          <p className="note">
            Set <code>DATABASE_URL</code> and publish five cards from{" "}
            <Link href="/admin/REPLACE_WITH_ADMIN_TOKEN">/admin/TOKEN</Link> (Sprint 1 ·
            S1). Until Neon is connected, use the clickable prototype in{" "}
            <code>02-design/prototype/</code>.
          </p>
        </div>
      ) : !set ? (
        <div className="card">
          <p>No published set yet.</p>
          <p className="note">Curator: publish five cards from the admin page first.</p>
        </div>
      ) : (
        <StudentCardSet set={set} source={source} />
      )}
    </main>
  );
}
