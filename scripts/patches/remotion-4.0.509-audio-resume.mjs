#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { lstat, readFile } from 'node:fs/promises';
import { join, resolve } from 'node:path';

const EXPECTED_VERSION = '4.0.509';
const PACKAGE_RELATIVE = join('node_modules', 'remotion');
const TARGETS = [
  {
    relativePath: join('dist', 'cjs', 'audio', 'shared-audio-tags.js'),
    sha256: '949ccec3419398183e8e22f63820a4a57cb8379befb184fbac9a3acde040c5b8',
    requiredSnippet:
      'resumePromise.then(() => (0, wait_until_actually_resumed_js_1.waitUntilActuallyResumed)(ctxAndGain.audioContext, logLevel, abortController.signal).then(resolve), () => {});',
  },
  {
    relativePath: join('dist', 'esm', 'index.mjs'),
    sha256: '5a1584f7660fa8fffa7eb8fe016b82a4d719e67d4b7904d4fa4f299eb1355f28',
    requiredSnippet:
      'resumePromise.then(() => waitUntilActuallyResumed(ctxAndGain.audioContext, logLevel, abortController.signal).then(resolve), () => {});',
  },
];

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

async function preflight(projectRoot) {
  const packageRoot = resolve(projectRoot, PACKAGE_RELATIVE);
  const packageJson = JSON.parse(await readFile(join(packageRoot, 'package.json'), 'utf8'));
  if (packageJson.name !== 'remotion' || packageJson.version !== EXPECTED_VERSION) {
    throw new Error(
      'Refusing Remotion ' +
        (packageJson.name ?? '(unnamed)') +
        '@' +
        (packageJson.version ?? '(unknown)') +
        '; expected remotion@' +
        EXPECTED_VERSION,
    );
  }

  const verified = [];
  for (const target of TARGETS) {
    const absolutePath = join(packageRoot, target.relativePath);
    const [bytes, fileStat] = await Promise.all([readFile(absolutePath), lstat(absolutePath)]);
    if (!fileStat.isFile() || fileStat.isSymbolicLink()) {
      throw new Error('Refusing non-regular Remotion audio file at ' + absolutePath);
    }
    const digest = sha256(bytes);
    if (digest !== target.sha256) {
      throw new Error(
        'Refusing unknown content at ' +
          absolutePath +
          ' (sha256 ' +
          digest +
          '); no files were written',
      );
    }
    if (!bytes.includes(Buffer.from(target.requiredSnippet, 'utf8'))) {
      throw new Error('Known Remotion 4.0.509 bytes lack the native-resume fence at ' + absolutePath);
    }
    verified.push(target.relativePath + '=' + digest);
  }
  return verified;
}

function parseArgs(argv) {
  let action;
  let projectRoot = process.cwd();
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--help' || arg === '-h') return { help: true };
    if (['--apply', '--check'].includes(arg)) {
      if (action) throw new Error('Choose exactly one of --apply or --check');
      action = arg.slice(2);
      continue;
    }
    if (arg === '--root') {
      const value = argv[index + 1];
      if (!value || value.startsWith('--')) throw new Error('--root requires a project root path');
      projectRoot = resolve(value);
      index += 1;
      continue;
    }
    throw new Error('Unknown argument: ' + arg);
  }
  if (!action) throw new Error('Choose one of --apply or --check');
  return { action, projectRoot };
}

function usage() {
  return [
    'Usage: node scripts/patches/remotion-4.0.509-audio-resume.mjs --apply|--check [--root <project-root>]',
    '--check is read-only; both actions accept only the exact known 4.0.509 CJS and ESM files.',
    '--apply verifies the upstream fix and writes nothing; Remotion 4.0.509 already contains the audio-resume fence.',
  ].join('\n');
}

async function main(argv = process.argv.slice(2)) {
  const args = parseArgs(argv);
  if (args.help) {
    process.stdout.write(usage() + '\n');
    return;
  }

  const verified = await preflight(args.projectRoot);
  process.stdout.write(
    (args.action === 'apply' ? 'Verified; no patch needed' : 'Read-only preflight passed') +
      ' for remotion@' +
      EXPECTED_VERSION +
      ': ' +
      verified.join(', ') +
      '\n',
  );
}

main().catch((error) => {
  process.stderr.write('Remotion 4.0.509 audio-resume guard refused/failed: ' + error.message + '\n');
  process.exitCode = 1;
});
