#!/bin/bash
set -euo pipefail
cd /tmp/vw-m3-scene-carry-public12-proof.Od7E6n
export EXPECTED=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-scene-carry-public12-proof-agent-theme.json
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --input-type=module - <<'NODE'
import fs from 'node:fs';
import assert from 'node:assert/strict';
const root = await import('@banodoco/timeline-composition');
const modules = {
  root,
  evaluation: await import('@banodoco/timeline-composition/evaluation'),
  themeApi: await import('@banodoco/timeline-composition/theme-api'),
  registry: await import('@banodoco/timeline-composition/registry.generated'),
  effects: await import('@banodoco/timeline-composition/effects.generated'),
  animations: await import('@banodoco/timeline-composition/animations.generated'),
  transitions: await import('@banodoco/timeline-composition/transitions.generated'),
  registries: await import('@banodoco/timeline-composition/registries'),
  packageJson: await import('@banodoco/timeline-composition/package.json', {with: {type: 'json'}}),
};
const required = ['DEFAULT_THEME','TimelineComposition','prepareCompositionScene','prepareScene','querySceneFrame','compileCanonicalTransitions','toRuntimeTheme','resolveElementRegistries'];
for (const name of required) assert.ok(name in root, `missing root export ${name}`);
for (const [name, module] of Object.entries(modules)) assert.ok(Object.keys(module).length > 0, `empty ${name}`);
assert.equal(modules.packageJson.default.version, '0.0.12');
const agentTheme = JSON.parse(fs.readFileSync(process.env.EXPECTED, 'utf8'));
assert.deepEqual(root.DEFAULT_THEME, agentTheme, 'public DEFAULT_THEME differs from Agent BUILTIN_DEFAULT_THEME');
const explicit = structuredClone(root.DEFAULT_THEME);
explicit.id = 'owner-explicit';
explicit.visual.color.bg = '#112233';
explicit.visual.type.families.heading = 'Georgia';
explicit.visual.canvas = {width: 640, height: 360, fps: 24};
const runtime = root.toRuntimeTheme(explicit);
assert.equal(runtime.id, 'owner-explicit');
assert.equal(runtime.visual.color.bg, '#112233');
assert.equal(runtime.visual.type.families.heading, 'Georgia');
assert.deepEqual(runtime.visual.canvas, {width: 640, height: 360, fps: 24});
console.log(JSON.stringify({packageVersion: modules.packageJson.default.version, rootExports: Object.keys(root).sort(), subpathExportCounts: Object.fromEntries(Object.entries(modules).map(([k,v]) => [k, Object.keys(v).length])), defaultTheme: root.DEFAULT_THEME, agentDefaultThemeEqual: true, explicitThemePreserved: runtime}, null, 2));
NODE
