import { test, expect } from "@playwright/test";

const api = "http://127.0.0.1:55440";
test.describe.configure({ mode: "serial" });

test("empty database displays the real empty state", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("No published set yet.")).toBeVisible();
});

test("existing Lab 5 prototype is served by the production build", async ({ page }) => {
  await page.goto("/prototype/index.html");
  await expect(page.getByText("Sample opportunities, not real job offers", { exact: false })).toBeVisible();
  for (let i = 0; i < 5; i++) await page.locator(`[data-index="${i}"][data-choice="apply"]`).click();
  await expect(page.getByText("All five reviewed!")).toBeVisible();
  await page.getByRole("button", { name: /Start again/ }).click();
  await expect(page.getByText("0 of 5 reviewed")).toBeVisible();
});

test("mobile curator → five real saved decisions → completion → resume", async ({ page, context, request }) => {
  // Synthetic opportunity destinations are fulfilled locally; no employer or analytics traffic.
  await context.route("https://example.com/**", route => route.fulfill({ body: "Opportunity test fixture" }));
  await page.goto("/admin");
  await page.getByLabel("Admin token").fill("test-admin");
  await page.getByRole("button", { name: "Open publish form" }).click();
  const facts = [
    ["Role", "Engineer"], ["Company", "Example"], ["Field", "IT"], ["Source", "Example"],
    ["Source URL", "https://example.com/job/"], ["Experience required", "None"],
    ["Hours", "Part time"], ["Pay", ""], ["Deadline (YYYY-MM-DD)", "2027-01-01"],
  ];
  for (let i = 0; i < 5; i++) {
    for (const [label, value] of facts) {
      const content = label === "Source URL" ? value + i : label === "Role" ? (i === 0 ? "A".repeat(180) : `${value} ${i}`) : value;
      await page.getByLabel(label, { exact: true }).nth(i).fill(content);
    }
  }
  await page.getByRole("button", { name: "Publish", exact: true }).click();
  await expect(page.getByText(/Published: 5 cards/)).toBeVisible();
  expect(page.url()).not.toContain("test-admin");
  await page.goto("/?src=friend");
  const cards = page.locator("article.card");
  await expect(cards).toHaveCount(5);
  await expect(cards.first().getByRole("button", { name: "Apply", exact: true })).toBeEnabled();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);

  async function apply(index: number) {
    const popup = context.waitForEvent("page");
    await cards.nth(index).getByRole("button", { name: "Apply", exact: true }).click();
    const listing = await popup;
    await listing.waitForLoadState("domcontentloaded");
    expect(listing.url()).toBe(`https://example.com/job/${index}`);
    await listing.close();
    await expect(cards.nth(index).getByText("Applying ↗")).toBeVisible();
  }
  async function skip(index: number) {
    await cards.nth(index).getByRole("button", { name: "Skip", exact: true }).click();
    await cards.nth(index).getByRole("button", { name: "Hours don't fit", exact: true }).click();
    await expect(cards.nth(index).getByText("Skipped", { exact: true })).toBeVisible();
  }
  await apply(0);
  await skip(1);
  await page.reload();
  await expect(cards.nth(0).getByText("Applying ↗")).toBeVisible();
  await expect(cards.nth(1).getByText("Skipped", { exact: true })).toBeVisible();
  await apply(2);
  await skip(3);
  await skip(4);
  await expect(page.getByRole("heading", { name: "Your apply list" })).toBeVisible();
  await expect(page.locator("section.card li")).toHaveCount(2);
  await page.reload();
  await expect(page.locator("section.card li")).toHaveCount(2);
  await expect(page.locator("article button")).toHaveCount(0);
  const anonymousId = await page.evaluate(() => localStorage.getItem("cc_anon"));
  const persisted = await (await request.get(`${api}/test/state/${anonymousId}`)).json();
  expect(persisted.decisions).toBe(5);
  expect(persisted.completions).toHaveLength(1);
  expect(persisted.completions[0].qualifies).toBe(true);
  expect(persisted.completions[0].environment).toBe("test");
  const completionEvents = persisted.events.filter((event: { event: string }) => event.event === "student_completes_card_set");
  expect(completionEvents).toHaveLength(1);
  expect(completionEvents[0].properties.ms_total).toBe(persisted.completions[0].ms_total);
});

test("restore and write outages never display unsaved success", async ({ page, context, request }) => {
  await context.route("https://example.com/**", route => route.fulfill({ body: "Opportunity test fixture" }));
  await page.route("**/api/sets/*/decisions?*", route => route.abort());
  await page.goto("/");
  await expect(page.locator("main").getByRole("alert")).toBeVisible();
  await expect(page.locator("article button").first()).toBeDisabled();
  await page.unroute("**/api/sets/*/decisions?*");
  await page.reload();
  await page.route("**/api/decide", route => route.fulfill({ status: 503, json: { detail: "Saving unavailable" } }));
  const first = page.locator("article.card").first();
  await first.getByRole("button", { name: "Skip", exact: true }).click();
  await first.getByRole("button", { name: "Other", exact: true }).click();
  await expect(page.locator("main").getByRole("alert")).toHaveText("Saving unavailable");
  await expect(first.getByText("Skipped", { exact: true })).toHaveCount(0);
  const anonymousId = await page.evaluate(() => localStorage.getItem("cc_anon"));
  const beforeRetry = await (await request.get(`${api}/test/state/${anonymousId}`)).json();
  expect(beforeRetry.decisions).toBe(0);
  await page.unroute("**/api/decide");
  await first.getByRole("button", { name: "Other", exact: true }).click();
  await expect(first.getByText("Skipped", { exact: true })).toBeVisible();
});
