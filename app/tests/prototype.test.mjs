import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { JSDOM } from 'jsdom';

test('existing Lab 5 prototype completes five choices and resets without network access', async () => {
  const html = await readFile(new URL('../../02-design/prototype/index.html', import.meta.url), 'utf8');
  const script = await readFile(new URL('../../02-design/prototype/script.js', import.meta.url), 'utf8');
  const dom = new JSDOM(html, { runScripts: 'outside-only' });
  try {
    dom.window.scrollTo = () => {};
    dom.window.eval(script);
    const document = dom.window.document;
    assert.equal(document.querySelectorAll('.job-card').length, 5);
    for (let i = 0; i < 5; i++) document.querySelector(`[data-index="${i}"][data-choice="apply"]`).click();
    assert.equal(document.getElementById('finish').hidden, false);
    assert.match(document.getElementById('summary').textContent, /5 Apply/);
    document.getElementById('reset').click();
    assert.equal(document.getElementById('finish').hidden, true);
    assert.match(document.getElementById('progressLabel').textContent, /0 of 5/);
  } finally { dom.window.close(); }
});
