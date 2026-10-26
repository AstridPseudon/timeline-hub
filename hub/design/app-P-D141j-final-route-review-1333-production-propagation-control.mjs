#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { writeFile } from 'node:fs/promises';

const appRepo = '/home/user/banodoco/reigh-app';
const appCommit = '04545a1e52c58a5fa938cb4aa0a060328e8d3efc';
const observationKey = 'TIMELINE_D141J_VISIBILITY_CAPTURE';
const expectedOccurrenceId = 'f2-occurrence-copy';
const expectedValue = JSON.stringify({ expectedOccurrenceId });
const source = execFileSync('git', ['-C', appRepo, 'show', `${appCommit}:scripts/testing/d66-plain-stack.mjs`]);
const rootLine = "const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');";
const replacement = `const root = ${JSON.stringify(appRepo)};`;
const sourceText = source.toString();
if (!sourceText.includes(rootLine)) throw new Error('immutable D66 root locator changed');
const runnable = sourceText.replace(rootLine, replacement)
  .replaceAll('fileURLToPath(import.meta.url)', "'/never-run/d66-plain-stack.mjs'");
const mod = await import(`data:text/javascript;charset=utf-8,${encodeURIComponent(runnable)}`);

const baseEnv = {
  [observationKey]: expectedValue,
  D66_RUNTIME_LOG_DIR: '/should-be-removed-by-real-builder',
  D66_RUNTIME_PHASE_LAUNCH_ORDINAL: '99',
};
const launchEnv = mod.playwrightLaunchEnv({
  suite: { verificationOnly: false, retainRuntimeLogs: false },
  suiteName: 'p2-popup-add',
  output: '/tmp/d141j-production-propagation-control',
  junit: { readiness: '/tmp/readiness.xml', original: '/tmp/original.xml' },
  stage: 'p2-popup-add',
  baseEnv,
});
if (launchEnv[observationKey] !== expectedValue) throw new Error('real playwrightLaunchEnv dropped observation env');
if (launchEnv.D66_RUNTIME_LOG_DIR !== undefined || launchEnv.D66_RUNTIME_PHASE_LAUNCH_ORDINAL !== undefined) {
  throw new Error('real playwrightLaunchEnv did not retain its normal deletion behavior');
}

const result = {
  schema: 'timeline.app.d141j.production-propagation-control.v1',
  status: 'PASS_REAL_D66_PLAYWRIGHT_SEAM',
  source: { repo: appRepo, commit: appCommit, path: 'scripts/testing/d66-plain-stack.mjs' },
  intercepted: true,
  executed: false,
  input: { observationKey, value: expectedValue },
  output: {
    observationValue: launchEnv[observationKey],
    playwrightOutputDir: launchEnv.PLAYWRIGHT_OUTPUT_DIR,
    junitOutput: launchEnv.PLAYWRIGHT_JUNIT_OUTPUT_FILE,
    runtimeLogDir: launchEnv.D66_RUNTIME_LOG_DIR ?? null,
    runtimeLaunchOrdinal: launchEnv.D66_RUNTIME_PHASE_LAUNCH_ORDINAL ?? null,
  },
  sideEffects: { service: false, browser: false, request: false, native: false },
};
await writeFile(new URL('./production-propagation-results.json', import.meta.url), `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify(result, null, 2));
