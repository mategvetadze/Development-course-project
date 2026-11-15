import { apiUrl } from "@/lib/api";

export type Card = {
  id: string;
  set_id: string;
  position: number;
  role: string;
  company: string;
  field: string;
  source: string;
  source_url: string;
  students_ok: boolean;
  experience: string;
  hours: string;
  pay: string;
  deadline: string;
};

export type CardSet = {
  id: string;
  published_at: string;
  cards: Card[];
};

export async function getLatestPublishedSet(): Promise<CardSet | null> {
  const res = await fetch(apiUrl("/api/sets/latest"), { cache: "no-store" });
  if (res.status === 200) {
    const data = await res.json();
    return data as CardSet | null;
  }
  if (res.status === 404) return null;
  const detail = await res.text();
  throw new Error(detail || `API ${res.status}`);
}
