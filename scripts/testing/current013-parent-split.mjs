#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import { checkCurrent013Sources, CURRENT013_COMPOSITION, readCurrent013Inputs } from './current013-integration.mjs';

export const CURRENT013_PARENT_SPLIT_AGENT = 'd8749a9ce12a699672faf3ad96b4e4cbea9245c2';

export function parentSplitCacheIdentity(input) {
  const hash = (url) => createHash('sha256').update(readFileSync(url)).digest('hex');
  return `parent-split-tree${input.appTree}-agent${input.agentSha}-runtime${input.runtimeSha}-client13-public12-${CURRENT013_COMPOSITION.sha256.slice(7)}-runner${hash(new URL(import.meta.url))}-helper${hash(new URL('./current013-integration.mjs', import.meta.url))}`;
}

export function runCurrent013ParentSplit() {
  if (process.env.TIMELINE_CURRENT013_RUN !== '1') {
    throw new Error('Supply the manager-approved current013/native parent-split composition before running this lane');
  }
  const input = readCurrent013Inputs();
  if (input.agentSha !== CURRENT013_PARENT_SPLIT_AGENT) throw new Error(`parent-split requires Agent ${CURRENT013_PARENT_SPLIT_AGENT}`);
  if (process.env.TIMELINE_CURRENT013_CACHE_ID !== parentSplitCacheIdentity(input)) {
    throw new Error('TIMELINE_CURRENT013_CACHE_ID must identify this exact parent-split App tree, pair, client/public archive and launcher/helper bytes');
  }
  const before = checkCurrent013Sources(input);
  try {
    process.exitCode = spawnSync('npm', ['run', 'test:e2e:three-products', '--', '--config', 'playwright.clip-split.config.ts'], {
      cwd: input.app,
      env: {
        ...process.env,
        ASTRID_CHECKOUT: input.agent,
        ASTRID_RUNTIME_CHECKOUT: input.runtime,
        ASTRID_PYTHON: input.agentPython,
        ASTRID_RUNTIME_PYTHON: input.runtimePython,
        TIMELINE_BUNDLE_AGENT_HEAD: input.agentSha,
        TIMELINE_BUNDLE_RUNTIME_HEAD: input.runtimeSha,
      },
      stdio: 'inherit', shell: false,
    }).status ?? 1;
  } finally {
    const after = checkCurrent013Sources(input);
    if (JSON.stringify(after) !== JSON.stringify(before)) throw new Error('current013 parent-split sources changed during the browser gate');
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) runCurrent013ParentSplit();
