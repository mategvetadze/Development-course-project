import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { JSDOM } from 'jsdom';
import { createServer } from 'node:http';

async function verify() {
  let received;
  const receipt = new Promise(resolve => { received = resolve; });
  const server = createServer((request, response) => {
    const chunks = [];
    request.on('data', chunk => chunks.push(chunk));
    request.on('end', () => {
      const text = Buffer.concat(chunks).toString('utf8');
      if (text) {
        try {
          const encoded = new URLSearchParams(text).get('data');
          const data = JSON.parse(encoded ? Buffer.from(encoded, 'base64').toString('utf8') : text);
          const events = Array.isArray(data) ? data : data.batch || [data];
          const event = events.find(item => item.event === 'student_opens_card_set');
          if (event) received(event);
        } catch { /* GET/configuration probes are not event receipts. */ }
      }
      response.setHeader('Access-Control-Allow-Origin', '*');
      response.end('{"status":"OK"}');
    });
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const dom = new JSDOM('<p>SDK fixture</p>', { url: `${origin}/?src=private` });
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.location = dom.window.location;
  process.env.NEXT_PUBLIC_POSTHOG_KEY = 'phc_synthetic-test-only';
  process.env.NEXT_PUBLIC_POSTHOG_HOST = origin;
  const posthog = createRequire(import.meta.url)('posthog-js').default;
  const init = posthog.init.bind(posthog);
  posthog.init = (key, config) => init(key, { ...config, request_batching: false, disable_compression: true,
    advanced_disable_flags: true, disable_external_dependency_loading: true, opt_out_useragent_filter: true });
  const { getPostHog } = createRequire(import.meta.url)('../../lib/posting-client.ts');
  try {
    getPostHog('anonymous-test-id');
    assert.equal(posthog.config.request_batching, false);
    const event = posthog.capture('student_opens_card_set', { set_id: 'set-1', source: 'friend',
      environment: 'test', is_internal: false, email: 'private@example.com' });
    assert.ok(event, 'real SDK must accept, not drop, the event');
    assert.equal(event.properties.token, 'phc_synthetic-test-only');
    assert.equal(event.properties.distinct_id, 'anonymous-test-id');
    assert.equal(event.properties.email, undefined);
    assert.equal(event.properties.$current_url, undefined);
    assert.equal(event.properties.$process_person_profile, false);
    const ingested = await Promise.race([receipt, new Promise((_, reject) =>
      setTimeout(() => reject(new Error('No local SDK transport receipt')), 3000))]);
    assert.equal(ingested.properties.token, 'phc_synthetic-test-only');
    assert.equal(ingested.properties.distinct_id, 'anonymous-test-id');
    assert.equal(ingested.properties.$current_url, undefined);
  } finally {
    posthog.opt_out_capturing();
    posthog._requestQueue?.stop();
    dom.window.close();
    server.closeAllConnections();
    server.close();
  }
}

// The browser SDK owns long-lived timers. Isolate it in a child process and exit
// only AFTER all assertions; failure must propagate to the parent test runner.
verify().catch(error => { console.error(error); process.exitCode = 1; })
  .finally(() => process.exit(process.exitCode || 0));
