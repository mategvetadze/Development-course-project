import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

// No shell interpolation of interpreter paths or database credentials.
const child = spawn(process.env.TEST_PYTHON || 'python', ['tests/live_server.py'], {
  cwd: fileURLToPath(new URL('../../backend/', import.meta.url)),
  env: process.env, stdio: 'inherit', windowsHide: true,
});
child.on('error', () => process.exit(1));
child.on('exit', code => process.exit(code ?? 1));
process.on('SIGTERM', () => child.kill('SIGTERM'));
process.on('SIGINT', () => child.kill('SIGINT'));
