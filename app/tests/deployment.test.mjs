import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';

test('production build config refuses missing API/key and supports EU/US proxies', () => {
  const code = "const c=(await import('./next.config.mjs')).default;console.log(JSON.stringify(await c.rewrites()))";
  function check(overrides) {
    return spawnSync(process.execPath, ['--input-type=module', '-e', code], { encoding: 'utf8',
      env: { ...process.env, APP_ENV: 'production', VERCEL_ENV: '', NEXT_PUBLIC_API_URL: '', NEXT_PUBLIC_POSTHOG_KEY: '', ...overrides } });
  }
  assert.notEqual(check({}).status, 0);
  assert.notEqual(check({ NEXT_PUBLIC_API_URL: 'http://localhost:8000', NEXT_PUBLIC_POSTHOG_KEY: 'synthetic' }).status, 0);
  assert.notEqual(check({ NEXT_PUBLIC_API_URL: 'https://localhost', NEXT_PUBLIC_POSTHOG_KEY: 'synthetic' }).status, 0);
  assert.notEqual(check({ NEXT_PUBLIC_API_URL: 'https://user:private@example.test', NEXT_PUBLIC_POSTHOG_KEY: 'synthetic' }).status, 0);
  assert.notEqual(check({ NEXT_PUBLIC_API_URL: 'https://example.test' }).status, 0);
  const ready = check({ NEXT_PUBLIC_API_URL: 'https://example.test', NEXT_PUBLIC_POSTHOG_KEY: 'synthetic', NEXT_PUBLIC_POSTHOG_REGION: 'us' });
  assert.equal(ready.status, 0, ready.stderr);
  assert.match(JSON.parse(ready.stdout)[0].destination, /us-assets/);
});
