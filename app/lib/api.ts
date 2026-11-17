const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export function apiUrl(path: string) {
  return `${API_URL.replace(/\/$/, "")}${path}`;
}

export { API_URL };

export function apiError(data: { error?: unknown; detail?: unknown }, fallback: string): string {
  if (typeof data.detail === "string") return data.detail;
  if (typeof data.error === "string") return data.error;
  if (Array.isArray(data.detail)) {
    const messages = data.detail.map((item) => {
      const path = Array.isArray(item.loc) ? item.loc.filter((part: unknown) => part !== "body").join(".") : "";
      return typeof item.msg === "string" ? `${path ? `${path}: ` : ""}${item.msg}` : "";
    }).filter(Boolean);
    if (messages.length) return messages.join("; ");
  }
  return fallback;
}
