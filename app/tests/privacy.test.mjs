import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import helperModule from '../lib/posting-client.ts';
const { getPostHog, normalizeSource } = helperModule;
const posthog = createRequire(import.meta.url)('posthog-js').default;

test('anonymous analytics bootstrap matches API identity and strips URL/contact properties', () => {
  globalThis.window = {};
  process.env.NEXT_PUBLIC_POSTHOG_KEY = 'test-only';
  let config;
  posthog.init = (_, options) => { config = options; return posthog; };
  getPostHog('anonymous-test-id');
  assert.equal(config.bootstrap.distinctID, 'anonymous-test-id');
  assert.equal(config.bootstrap.isIdentifiedID, false);
  assert.equal(config.disable_session_recording, true);
  assert.equal(config.person_profiles, 'never');
  const scrubbed = config.before_send({ event: 'student_opens_card_set', $set_once: { email: 'private' }, properties: {
    distinct_id: 'anonymous-test-id', set_id: 'set-1', source: 'friend',
    $current_url: 'https://example.com/admin/private-token', email: 'someone@example.com',
    $set_once: { $initial_referrer: 'https://example.com/?name=private' },
  } });
  assert.deepEqual(scrubbed.properties, { distinct_id: 'anonymous-test-id', set_id: 'set-1', source: 'friend',
    $geoip_disable: true, $process_person_profile: false, $ip: null });
  assert.equal(config.before_send({ event: '$autocapture', properties: {} }), null);
  assert.equal(scrubbed.$set_once, undefined);
  assert.equal(normalizeSource('someone@example.com'), 'other');
  assert.equal(normalizeSource('groupchat'), 'groupchat');
});
