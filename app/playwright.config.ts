import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  workers: 1,
  retries: 0,
  timeout: 30_000,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:55441",
    viewport: { width: 375, height: 812 },
    isMobile: true,
    hasTouch: true,
    headless: true,
    channel: process.env.PLAYWRIGHT_CHANNEL || undefined,
  },
  webServer: [
    {
      command: "node tests/start-backend.mjs",
      url: "http://127.0.0.1:55440/health/ready",
      reuseExistingServer: false,
      timeout: 30_000,
    },
    {
      command: "npm run start -- --hostname 127.0.0.1 --port 55441",
      url: "http://127.0.0.1:55441",
      reuseExistingServer: false,
      timeout: 30_000,
      env: { NEXT_PUBLIC_API_URL: "http://127.0.0.1:55440", NEXT_PUBLIC_POSTHOG_KEY: "", NEXT_TELEMETRY_DISABLED: "1" },
    },
  ],
});
