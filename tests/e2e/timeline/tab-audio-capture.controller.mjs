import { createHash } from 'node:crypto';
import { closeSync, existsSync, openSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const PROFILE = 'native-codec-chrome155';
export const BROWSER_EXECUTABLE = '/opt/google/chrome/chrome';
export const BROWSER_VERSION = '155.0.8059.84';
export const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
export const SOURCE_FILES = [
  'tests/e2e/timeline/tab-audio-capture.analysis.mjs',
  'tests/e2e/timeline/tab-audio-capture.probe.ts',
  'tests/e2e/timeline/tab-audio-capture.config.ts',
  'tests/e2e/timeline/tab-audio-capture.controller.mjs',
  'tests/e2e/timeline/setup-tab-audio-capture.sh',
];

const ORCH_ROOT = process.env.ORCH_ROOT
  ?? '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch';
const QUIET_FILES = [join(ORCH_ROOT, 'QUIET.md'), join(ORCH_ROOT, 'managers/viewing/QUIET.md')];

function sourceFingerprint() {
  const hash = createHash('sha256');
  const files = SOURCE_FILES.map((relative) => {
    const path = join(REPO_ROOT, relative);
    if (!existsSync(path)) throw new Error(`Missing probe source: ${relative}`);
    const bytes = readFileSync(path);
    hash.update(relative).update('\0').update(bytes).update('\0');
    return {relative, sha256: createHash('sha256').update(bytes).digest('hex'), bytes: bytes.length};
  });
  // The final commit SHA is supplied by the manager grant. Keeping this
  // fingerprint filesystem-only lets preflight run while the harness still
  // has a read-only .git view.
  return {sourceDigest: hash.digest('hex'), files};
}

function assertQuietAbsent() {
  const present = QUIET_FILES.filter((path) => existsSync(path));
  if (present.length > 0) throw new Error(`QUIET guard is active: ${present.join(', ')}`);
}

function requiredEnv(name) {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required guard environment: ${name}`);
  return value;
}

function readGrant() {
  const path = requiredEnv('TAB_AUDIO_GRANT_PATH');
  const grant = JSON.parse(readFileSync(path, 'utf8'));
  const fingerprint = sourceFingerprint();
  if (grant.approved !== true) throw new Error('Tab-audio grant is not approved');
  if (grant.profile !== PROFILE || grant.browserExecutable !== BROWSER_EXECUTABLE || grant.browserVersion !== BROWSER_VERSION) {
    throw new Error('Tab-audio grant does not name the approved Chrome155 profile');
  }
  if (grant.backendOrder?.join(',') !== 'tab,private-pulse') {
    throw new Error('Tab-audio grant must preserve tab capture before private PulseAudio fallback');
  }
  if (grant.sourceDigest !== fingerprint.sourceDigest) throw new Error('Tab-audio grant source digest is stale');
  if (!grant.finalSha || grant.finalSha !== requiredEnv('TAB_AUDIO_FINAL_SHA')) {
    throw new Error('Tab-audio grant final SHA does not match TAB_AUDIO_FINAL_SHA');
  }
  if (!grant.environmentApprovalReference) throw new Error('Tab-audio grant lacks environment approval reference');
  return {grant, fingerprint};
}

function ensureFlock() {
  if (process.env.VIEWING_BROWSER_FLOCK_HELD !== '1') {
    throw new Error('The central browser flock is not declared held');
  }
}

function preflight() {
  assertQuietAbsent();
  ensureFlock();
  const {grant, fingerprint} = readGrant();
  if (!existsSync(BROWSER_EXECUTABLE)) throw new Error(`Pinned Chrome executable is missing: ${BROWSER_EXECUTABLE}`);
  const browser = statSync(BROWSER_EXECUTABLE);
  if (!browser.isFile() || (browser.mode & 0o111) === 0) throw new Error('Pinned Chrome executable is not executable');
  const statePath = requiredEnv('TAB_AUDIO_PREFLIGHT_PATH');
  writeFileSync(statePath, JSON.stringify({profile: PROFILE, grant, fingerprint, browser: {size: browser.size, mtimeMs: browser.mtimeMs}}, null, 2), {flag: 'wx'});
  return {status: 'READY_GRANTED', profile: PROFILE, sourceDigest: fingerprint.sourceDigest};
}

function claim() {
  assertQuietAbsent();
  const markerPath = requiredEnv('TAB_AUDIO_RUN_MARKER');
  const {grant, fingerprint} = readGrant();
  const markerFd = openSync(markerPath, 'wx');
  closeSync(markerFd);
  writeFileSync(markerPath, JSON.stringify({profile: PROFILE, finalSha: grant.finalSha, sourceDigest: fingerprint.sourceDigest, pid: process.pid}, null, 2));
  return {status: 'RUN_STARTED', markerPath, sourceDigest: fingerprint.sourceDigest};
}

function postflight() {
  assertQuietAbsent();
  const state = JSON.parse(readFileSync(requiredEnv('TAB_AUDIO_PREFLIGHT_PATH'), 'utf8'));
  const fingerprint = sourceFingerprint();
  if (state.fingerprint.sourceDigest !== fingerprint.sourceDigest) throw new Error('Probe source changed during capture');
  if (!existsSync(requiredEnv('TAB_AUDIO_RUN_MARKER'))) throw new Error('One-shot run marker was not retained');
  return {status: 'POSTFLIGHT_OK', sourceDigest: fingerprint.sourceDigest};
}

const command = process.argv[2] ?? '--fingerprint';
if (command === '--fingerprint') console.log(JSON.stringify(sourceFingerprint(), null, 2));
else if (command === '--preflight') console.log(JSON.stringify(preflight(), null, 2));
else if (command === '--claim') console.log(JSON.stringify(claim(), null, 2));
else if (command === '--postflight') console.log(JSON.stringify(postflight(), null, 2));
else throw new Error(`Unknown controller command: ${command}`);
