import { StudentCardSet } from "@/components/StudentCardSet";
import { getLatestPublishedSet } from "@/lib/cards";

export const dynamic = "force-dynamic";

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<{ src?: string | string[] }>;
}) {
  const query = await searchParams;
  const source = typeof query.src === "string" ? query.src : "other";
  let set = null as Awaited<ReturnType<typeof getLatestPublishedSet>>;
  let error: string | null = null;

  try {
    set = await getLatestPublishedSet();
  } catch (e) {
    error = "Could not load opportunities. Please refresh and try again.";
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
          <p className="error" role="alert">{error}</p>
        </div>
      ) : !set ? (
        <div className="card">
          <p>No published set yet.</p>
          <p className="note">Curator: publish five cards from the admin page first.</p>
        </div>
      ) : (
        <StudentCardSet key={set.id} set={set} source={source} />
      )}
      <p className="note">
        CareerCards is a student project. We record anonymous decisions and completion times.
        With analytics enabled, we also count visits and card views. We do not ask for names or contact details.
      </p>
    </main>
  );
}
