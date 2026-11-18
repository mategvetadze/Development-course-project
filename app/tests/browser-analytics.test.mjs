import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';

test('real browser SDK preserves ingestion token and identity after privacy filtering', () => {
  const result = spawnSync(process.execPath, ['--import', 'tsx', 'tests/fixtures/browser-sdk.mjs'],
    { encoding: 'utf8', timeout: 10_000 });
  assert.equal(result.status, 0, result.stderr || result.error?.message);
});
