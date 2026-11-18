// Opt in against the isolated backend test server:
// TEST_API_URL=http://127.0.0.1:55440 node --import tsx --test tests/integration.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import React, { act } from 'react';
import { JSDOM } from 'jsdom';

test('real HTTP publish → latest → React decisions → completion → reload',
  { skip: !process.env.TEST_API_URL }, async () => {
    const api = new URL(process.env.TEST_API_URL);
    assert.equal(api.hostname, '127.0.0.1', 'only an isolated loopback backend is allowed');
    process.env.NEXT_PUBLIC_API_URL = api.origin;
    delete process.env.NEXT_PUBLIC_POSTHOG_KEY;
    const dom = new JSDOM('<div id="root"></div>', { url: 'http://localhost/' });
    globalThis.React = React;
    globalThis.IS_REACT_ACT_ENVIRONMENT = true;
    globalThis.window = dom.window;
    globalThis.document = dom.window.document;
    globalThis.location = dom.window.location;
    globalThis.localStorage = dom.window.localStorage;
    const { createRoot } = await import('react-dom/client');
    const curatorModule = await import('../components/CuratorForm.tsx');
    const studentModule = await import('../components/StudentCardSet.tsx');
    const { CuratorForm } = curatorModule.default || curatorModule;
    const { StudentCardSet } = studentModule.default || studentModule;
    localStorage.setItem('cc_anon', crypto.randomUUID());
    window.open = () => null;
    globalThis.IntersectionObserver = class {
      constructor(callback) { this.callback = callback; }
      observe(target) { this.callback([{ target, isIntersecting: true, intersectionRatio: 0.5 }]); }
      disconnect() {}
    };
    const container = document.getElementById('root');
    let root = createRoot(container);
    async function waitFor(predicate) {
      for (let i = 0; i < 100; i++) {
        if (predicate()) return;
        await act(async () => new Promise(resolve => setTimeout(resolve, 20)));
      }
      assert.fail('UI did not reach the expected state');
    }
    try {
      const preflight = await fetch(`${api.origin}/api/publish`, {
        method: 'OPTIONS', headers: { Origin: 'http://127.0.0.1:55441',
          'Access-Control-Request-Method': 'POST',
          'Access-Control-Request-Headers': 'content-type,x-admin-token' },
      });
      assert.equal(preflight.status, 200);
      assert.equal(preflight.headers.get('access-control-allow-origin'), 'http://127.0.0.1:55441');
      await act(async () => root.render(React.createElement(CuratorForm, { token: 'test-admin' })));
      // Native setters + bubbling input events exercise the actual controlled form.
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      const values = ['Engineer', 'Example', 'IT', 'Example', 'https://example.com/job', 'None', 'Part time', '', '2027-01-01'];
      await act(async () => {
        [...container.querySelectorAll('input:not([type="checkbox"])')].forEach((input, i) => {
          const value = i % values.length === 4 ? `https://example.com/job/${Math.floor(i / values.length)}` : values[i % values.length];
          setter.call(input, value);
          input.dispatchEvent(new window.Event('input', { bubbles: true }));
        });
      });
      await act(async () => container.querySelector('button').click());
      await waitFor(() => container.textContent.includes('Published: 5 cards'));
      const cards = await (await fetch(`${api.origin}/api/sets/latest`)).json();
      assert.equal(cards.cards.length, 5);
      // The production Next server is optional; when provided, verify real SSR too.
      if (process.env.TEST_FRONTEND_URL) {
        const frontend = new URL(process.env.TEST_FRONTEND_URL);
        assert.equal(frontend.hostname, '127.0.0.1');
        const page = await fetch(frontend);
        assert.equal(page.status, 200);
        assert.match(await page.text(), /Engineer/);
      }
      await act(async () => root.render(React.createElement(StudentCardSet, { set: cards, source: 'other' })));
      await waitFor(() => !container.querySelector('.apply').disabled);
      for (let i = 0; i < 5; i++) {
        const card = container.querySelector(`[data-card-id="${cards.cards[i].id}"]`);
        await act(async () => card.querySelector('.apply').click());
        await waitFor(() => card.textContent.includes('Applying'));
      }
      assert.equal(container.querySelectorAll('section.card li').length, 5);
      await act(async () => root.unmount());
      root = createRoot(container);
      await act(async () => root.render(React.createElement(StudentCardSet, { set: cards, source: 'other' })));
      await waitFor(() => container.querySelectorAll('section.card li').length === 5);
      assert.equal(container.querySelectorAll('article button').length, 0);
      const saved = await (await fetch(`${api.origin}/api/sets/${cards.id}/decisions?anonymous_id=${localStorage.getItem('cc_anon')}`)).json();
      assert.equal(Object.keys(saved.choices).length, 5);
      assert.equal(saved.complete, true);
      const persisted = await (await fetch(`${api.origin}/test/state/${localStorage.getItem('cc_anon')}`)).json();
      assert.equal(persisted.decisions, 5);
      assert.equal(persisted.completions.length, 1);
      assert.equal(persisted.completions[0].qualifies, true);
      assert.equal(persisted.events.filter(e => e.event === 'student_completes_card_set').length, 1);
      const event = persisted.events.find(e => e.event === 'student_completes_card_set');
      assert.equal(event.properties.ms_total, persisted.completions[0].ms_total);
      assert.equal(event.properties.completion_id, persisted.completions[0].id);
    } finally {
      await act(async () => root.unmount());
      dom.window.close();
    }
  });
