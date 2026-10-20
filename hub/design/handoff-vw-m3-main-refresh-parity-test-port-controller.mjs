import assert from 'node:assert/strict';
import { access, readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const contract = JSON.parse(await readFile(new URL('./handoff-vw-m3-main-refresh-parity-test-port-contract.json', import.meta.url), 'utf8'));
assert.deepEqual(process.argv.slice(2), ['--check-ready'], 'READY-only controller: no launch, freeze, grant or run-marker mode exists');
const app = resolve(process.env.VW_FRAME_APP_ROOT ?? process.cwd());
const tuplePath = process.env.VIEWING_FRAME_SOURCE_TUPLE;
const pending = [];
try {
  await access('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/QUIET.md');
  pending.push('Viewing QUIET marker is present');
} catch (error) { if (error.code !== 'ENOENT') throw error; }
let tuple;
try { if (tuplePath) tuple = JSON.parse(await readFile(tuplePath, 'utf8')); }
catch (error) { pending.push(`source tuple: ${error.message}`); }
if (!tuple) pending.push(...contract.pending_inputs);
else {
  for (const name of ['app', 'agent', 'runtime', 'composition']) {
    if (!tuple.sources?.[name]?.commit || !tuple.sources?.[name]?.tree) pending.push(`${name} committed source pair`);
  }
  for (const name of ['app', 'agent']) {
    if (Object.keys(tuple.peers?.[name] ?? {}).length !== 6) pending.push(`${name} six-file peer manifest`);
  }
  if (tuple.frozen !== true) pending.push('manager final source freeze');
  if (tuple.client?.official !== true) pending.push('official Runtime/client pair');
  if (!tuple.appSource?.sha256) pending.push('final App content identity');
}
if (process.version !== 'v20.19.4') pending.push('Node 20.19.4');
if (!pending.length) {
  try {
    // --import tsx is needed only once a complete owner tuple exists. Importing
    // the helper registers fixtures; sourceVersions performs read-only guards.
    const { sourceVersions } = await import(pathToFileURL(resolve(app, 'tests/e2e/timeline/viewing-parity/harness.ts')).href);
    await sourceVersions('native-codec-chrome155');
  } catch (error) { pending.push(`final source guards: ${error.message}`); }
}
console.log(JSON.stringify({ status: contract.status, actual_run: false, grant: false,
  source_guards_ready: pending.length === 0, pending_inputs: pending,
  next: 'Manager supplies fresh reviewed environment/controller/grant after owner tuple publication. This controller never launches.' }, null, 2));
if (pending.length) process.exitCode = 78;
