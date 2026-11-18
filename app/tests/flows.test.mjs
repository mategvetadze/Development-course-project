import { afterEach, beforeEach, test } from 'node:test';
import assert from 'node:assert/strict';
import React, { act } from 'react';
import { createRoot } from 'react-dom/client';
import { JSDOM } from 'jsdom';
import { createRequire } from 'node:module';
const posthog = createRequire(import.meta.url)('posthog-js').default;
import studentModule from '../components/StudentCardSet.tsx';
import curatorModule from '../components/CuratorForm.tsx';
const { StudentCardSet } = studentModule;
const { CuratorForm } = curatorModule;

globalThis.React = React;
globalThis.IS_REACT_ACT_ENVIRONMENT = true;
const cardSet = { id: 'set-1', cards: Array.from({ length: 5 }, (_, i) => ({
  id: `card-${i}`, set_id: 'set-1', position: i + 1, role: `Role ${i}`, company: 'Example',
  source: 'Example', field: 'IT', source_url: `https://example.com/${i}`, students_ok: true,
  experience: 'None', hours: 'Part time', pay: '', deadline: '2027-01-01',
})) };
const empty = { choices: {}, complete: false, summary: null,
  analytics: { environment: 'test', is_internal: false }, started_at: null, session_exists: false };
const response = (data, ok = true) => ({ ok, json: async () => data });
let dom, root, container, requests, opens, events, observer;
let getState, submit, startSession;

beforeEach(() => {
  dom = new JSDOM('<div id="root"></div>', { url: 'http://localhost/' });
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.localStorage = dom.window.localStorage;
  localStorage.setItem('cc_anon', 'student');
  requests = []; opens = []; events = [];
  getState = async () => response(empty);
  startSession = async () => response({ started_at: new Date().toISOString(), analytics: empty.analytics });
  submit = async () => response({ complete: false, decision: 'apply', summary: null });
  globalThis.fetch = async (url, options = {}) => {
    requests.push({ url, options });
    if (url.endsWith('/start')) return startSession();
    return options.method === 'POST' ? submit(JSON.parse(options.body)) : getState();
  };
  window.open = (...args) => { opens.push({ args, requests: requests.length }); };
  globalThis.IntersectionObserver = class {
    constructor(callback) { observer = this; this.callback = callback; this.elements = []; }
    observe(el) { this.elements.push(el); }
    disconnect() {}
    view(ratio = 0.5) { this.callback(this.elements.map(target => ({ target, isIntersecting: true, intersectionRatio: ratio }))); }
  };
  process.env.NEXT_PUBLIC_POSTHOG_KEY = 'test-only';
  posthog.init = () => posthog;
  posthog.identify = () => {};
  posthog.register = () => {};
  posthog.capture = (...args) => events.push(args);
  container = document.getElementById('root');
  root = createRoot(container);
});
afterEach(async () => {
  await act(async () => root.unmount());
  dom.window.close();
  delete process.env.NEXT_PUBLIC_POSTHOG_KEY;
});
async function renderStudent() {
  await act(async () => root.render(React.createElement(StudentCardSet, { set: cardSet, source: 'other' })));
}
async function click(element) {
  assert.ok(element, 'button exists');
  await act(async () => element.click());
}

test('reload restores saved choices and completed summary from API', async () => {
  getState = async () => response({ ...empty, choices: Object.fromEntries(cardSet.cards.map(c => [c.id, c.id === 'card-0' ? 'skip' : 'apply'])), complete: true,
    summary: [{ role: 'Saved role', deadline: '2027-01-01', source_url: 'https://example.com/saved' }] });
  await renderStudent();
  assert.match(requests[0]?.url || '', /\/api\/sets\/set-1\/decisions\?anonymous_id=student/);
  assert.match(container.querySelector('[data-card-id="card-0"]').textContent, /Skipped/);
  assert.match(container.textContent, /Saved role/);
});

test('StrictMode restores state and captures open once', async () => {
  await act(async () => root.render(React.createElement(React.StrictMode, null,
    React.createElement(StudentCardSet, { set: cardSet, source: 'other' }))));
  assert.equal(container.querySelector('.apply').disabled, false);
  assert.equal(events.filter(e => e[0] === 'student_opens_card_set').length, 1);
});

test('restore failure blocks new writes and exposes API detail', async () => {
  getState = async () => response({ detail: 'Database unavailable' }, false);
  await renderStudent();
  assert.match(container.querySelector('[role="alert"]')?.textContent || '', /Database unavailable/);
  assert.ok([...container.querySelectorAll('button')].every(button => button.disabled));
});

test('apply opens synchronously, blocks duplicate taps, and uses canonical decision', async () => {
  let finish;
  submit = () => new Promise(resolve => { finish = resolve; });
  await renderStudent();
  const button = container.querySelector('.apply');
  await act(async () => { button.click(); button.click(); });
  assert.equal(requests.filter(r => r.url.endsWith('/api/decide')).length, 1);
  assert.equal(opens.length, 1);
  assert.equal(opens[0].requests, 1, 'open happens after restore but before POST');
  assert.deepEqual(opens[0].args, ['https://example.com/0', '_blank', 'noopener,noreferrer']);
  await act(async () => finish(response({ decision: 'skip', complete: false, summary: null })));
  assert.match(container.querySelector('[data-card-id="card-0"]').textContent, /Skipped/);
});

test('failed decision stays retryable and displays FastAPI detail', async () => {
  submit = async () => response({ detail: 'Card does not belong to this set' }, false);
  await renderStudent();
  await click(container.querySelector('.apply'));
  assert.match(container.querySelector('[role="alert"]').textContent, /Card does not belong/);
  assert.equal(container.querySelector('.apply').disabled, false);
  submit = async () => response({ decision: 'apply', complete: false });
  await click(container.querySelector('.apply'));
  assert.match(container.querySelector('[data-card-id="card-0"]').textContent, /Applying/);
});

test('skip includes reason and empty completion renders all-skipped summary', async () => {
  submit = async body => {
    assert.equal(body.decision, 'skip');
    assert.equal(body.skip_reason, 'not_my_field');
    return response({ decision: 'skip', complete: true, summary: [] });
  };
  await renderStudent();
  await click(container.querySelector('.skip'));
  await click([...container.querySelectorAll('button')].find(b => b.textContent === 'Not my field'));
  assert.match(container.textContent, /You skipped all five/);
  assert.equal(opens.length, 0);
});

test('first-view timing survives remount and view analytics fires once per card', async () => {
  const realNow = Date.now;
  let now = 1000;
  Date.now = () => now;
  try {
    await renderStudent();
    act(() => { observer.view(); observer.view(); });
    assert.equal(events.filter(e => e[0] === 'student_views_card').length, 5);
    await act(async () => root.unmount());
    root = createRoot(container);
    now = 5000;
    await renderStudent();
    act(() => observer.view());
    now = 6000;
    await click(container.querySelector('.apply'));
    const body = JSON.parse(requests.find(r => r.url.endsWith('/api/decide')).options.body);
    assert.equal(body.ms_total, 5000);
    assert.equal(body.anonymous_id, 'student');
  } finally { Date.now = realNow; }
});

test('views require 50 percent visibility and server context tags every browser event', async () => {
  getState = async () => response({ ...empty, analytics: { environment: 'production', is_internal: true } });
  await renderStudent();
  act(() => observer.view(0.1));
  assert.equal(events.filter(e => e[0] === 'student_views_card').length, 0);
  await act(async () => observer.view(0.5));
  assert.equal(events.filter(e => e[0] === 'student_views_card').length, 5);
  assert.ok(events.every(e => e[1].environment === 'production' && e[1].is_internal === true));
  assert.equal(requests.filter(r => r.url.endsWith('/start')).length, 1);
});

test('failed session start prevents a decision and remains retryable', async () => {
  startSession = async () => response({ detail: 'Could not start this set' }, false);
  await renderStudent();
  await click(container.querySelector('.apply'));
  assert.equal(requests.filter(r => r.url.endsWith('/api/decide')).length, 0);
  assert.match(container.querySelector('[role="alert"]').textContent, /Could not start/);
  startSession = async () => response({ started_at: new Date().toISOString(), analytics: empty.analytics });
  await click(container.querySelector('.apply'));
  assert.equal(requests.filter(r => r.url.endsWith('/api/decide')).length, 1);
});

test('curator displays field validation errors instead of generic failure', async () => {
  submit = async () => response({ detail: [{ loc: ['body', 'cards', 0, 'deadline'], msg: 'Invalid date' }] }, false);
  await act(async () => root.render(React.createElement(CuratorForm, { token: 'test-admin' })));
  await click(container.querySelector('button'));
  assert.match(container.textContent, /cards\.0\.deadline: Invalid date/);
  assert.equal(requests[0].options.headers['X-Admin-Token'], 'test-admin');
  assert.equal(container.querySelector('button').disabled, false);
});
