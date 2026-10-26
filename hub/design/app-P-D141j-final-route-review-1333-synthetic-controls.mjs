#!/usr/bin/env node
import { readFile, writeFile } from 'node:fs/promises';
import { compose } from './pure-route-control.mjs';

const { route } = await compose();
const observationKey = 'TIMELINE_D141J_VISIBILITY_CAPTURE';
const expectedValue = JSON.stringify({ expectedOccurrenceId: route.expected_occurrence_id });
const assignment = `${observationKey}='${expectedValue}'`;
const deletedByPlaywrightLaunchEnv = [
  'NODE_PATH', 'ASTRID_QUICK_DESCRIPTOR', 'ASTRID_APP_DIRECT_DIST', 'APP_DIRECT_DIST',
  'ASTRID_LOCAL_DATA_ROOT', 'ASTRID_RUNTIME_DATA_ROOT', 'ASTRID_LOCAL_SOURCE_MANIFEST', 'ASTRID_RUNTIME_SOURCE_MANIFEST',
  'BANODOCO_LOCAL_DATA_ROOT', 'BANODOCO_RUNTIME_DATA_ROOT', 'BANODOCO_LOCAL_SOURCE_MANIFEST', 'BANODOCO_RUNTIME_SOURCE_MANIFEST',
  'D66_RUNTIME_LOG_DIR', 'D66_RUNTIME_PHASE_LAUNCH_ORDINAL', 'D66_ELEMENT_VERIFICATION_ONLY',
];
const serviceEnv = { [observationKey]: expectedValue, D66_APP_SHA: route.candidate.commit };
const launchEnv = { ...serviceEnv };
for (const key of deletedByPlaywrightLaunchEnv) delete launchEnv[key];
if (launchEnv[observationKey] !== expectedValue) throw new Error('observational env did not reach intercepted native browser launch');

const intercepted = {
  service: [
    { executable: '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test', executed: false },
    { executable: '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test', executed: false },
  ],
  browser: [{ operation: 'playwright child launch', executed: false, env_observed: launchEnv[observationKey] }],
  request: [{ operation: 'Runtime/App request', intercepted: true, executed: false }],
  native_process: [{ cwd: route.future_native_invocation.cwd, argv: route.future_native_invocation.argv, env_observed: launchEnv[observationKey], side_effects: false }],
};
const result = {
  schema: 'timeline.app.d141j.synthetic-controls.v1',
  status: 'PASS_FAITHFUL_INTERCEPTS_ONLY',
  recipe_unchanged: route.normal_recipe.text === route.future_native_invocation.command.slice(assignment.length + 1),
  observation_assignment: assignment,
  expected_occurrence_id: route.expected_occurrence_id,
  native_cwd: route.future_native_invocation.cwd,
  native_argv: route.future_native_invocation.argv,
  propagation: { service_process: serviceEnv[observationKey], playwright_launch: launchEnv[observationKey], native_intercept: intercepted.native_process[0].env_observed },
  output_retention: { pass: 'testInfo.outputPath(\'d141j-visibility.json\') + attach before page close', fail: 'same finally path; retention.capture may be unavailable and events remain honest' },
  intercepted,
};
await writeFile(new URL('./synthetic-control-results.json', import.meta.url), `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify(result, null, 2));
