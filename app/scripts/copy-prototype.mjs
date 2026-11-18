import { copyFile, mkdir } from 'node:fs/promises';

// Publish the team's existing Lab 5 source with the app; do not duplicate or edit
// the research artifact. Vercel must include repo files outside Root Directory.
const source = new URL('../../02-design/prototype/', import.meta.url);
const target = new URL('../public/prototype/', import.meta.url);
await mkdir(target, { recursive: true });
await Promise.all(['index.html', 'script.js', 'styles.css'].map(name =>
  copyFile(new URL(name, source), new URL(name, target))));
