const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export function apiUrl(path: string) {
  return `${API_URL.replace(/\/$/, "")}${path}`;
}

export { API_URL };
