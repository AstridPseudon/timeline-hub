# App M2 final-root parent-delete qualified candidate

## Result

Composed approved 11a9e3236c9172933774397e193a4692fddbc0d4 onto the b1-based native product 82dd3d769b3490b2d463b4543cbf727bc44f1adb.

Added the review follow-up in the existing parent-delete spec:
- exact native S2 whole-row and collection reads, three selections, occurrence collection-owner binding, and empty created IDs;
- matching Runtime record reads, selections, binding, and created assertions;
- a second real journey that holds the App delete request, publishes an Agent clip.move on the same parent/clip:f2-app-clip, releases the delete for a real 409, and checks original request identity/commands and draft retention across reload and explicit recovery.

All original 149 narrow product case bodies/fixtures plus the original three-products 7 cases remain; the label 4-case file and grouped-delete positive at useClipEditing.test.ts:261 were not edited. No product contract, fallback-after-capture, provider fake, App command injection, or parent-owner binding was added.

## Tree and pinned inputs

- Candidate App tree from current bytes: 530019d089acc3cdb36f3624bcfa98dcd9726df9 (computed without writing the read-only Git index; the harness commit should produce this tree).
- Agent: /home/user/work/wt/app-m3-agent013-current-pair-source at d8749a9ce12a699672faf3ad96b4e4cbea9245c2.
- Runtime/producer: /home/user/work/wt/app-m3-runtime013-producer-source at 2c4ac180c2220bdad966bc01e95ad230e99ce26a.
- Runtime client 0.2.13; producer sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56.
- Composition 0.0.12, 77 files, sha256:0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3.
- Private12 overlay: /tmp/app-coherent-deps12/node_modules (read-only). Short temp: /tmp/tl13-e2e-5300.

Cache identity:

    parent-delete-tree530019d089acc3cdb36f3624bcfa98dcd9726df9-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-client13-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-runnerda7944483b16fbd6f880a4958c4761eb62b17dae894b63ee5aec8cf3c3088abf-helper82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901

## Tests

- node --experimental-vm-modules scripts/testing/current013-parent-delete.test.mjs — 7 passed.
- node scripts/testing/current013-integration.test.mjs — 15 passed.
- Playwright discovery for playwright.clip-delete.config.ts — 2 parent-delete cases listed; no browser/build/setup run.
- Playwright discovery for playwright.three-products.config.ts — original 7 cases listed.
- Scoped ESLint over the new launcher/config/spec and harness — passed with no diagnostics.
- git diff --check — passed.
- Vitest narrow parent-delete/session/hook cohort, six files — 116 passed.

The first bare Vitest invocation failed at the repo config's known __dirname preload requirement; rerunning with the existing worker preload passed. No browser execution, localhost/socket run, build, project TypeScript check, install, full suite, or central request was run.

## Legacy boundary and next gate

The single-parent native capture/session/UI path is mounted and has no fallback after capture/submit failure. This does not retire unrelated legacy writers: group, multi-clip, occurrence, and prepared-media branches remain unsupported by this native port and retain their existing refusal or legacy behavior until separately qualified. Group case 261 remains intact.

After primary current-pair approval, commit this candidate and queue the central short-temp browser lane with literal App tree 530019d089acc3cdb36f3624bcfa98dcd9726df9, Agent d8749a9ce12a699672faf3ad96b4e4cbea9245c2, Runtime 2c4ac180c2220bdad966bc01e95ad230e99ce26a, private overlay /tmp/app-coherent-deps12/node_modules, and short temp /tmp/tl13-e2e-5300. The child command is:

    env -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST NODE_PATH=/tmp/app-coherent-deps12/node_modules TIMELINE_CURRENT013_SHORT_TMPDIR=/tmp/tl13-e2e-5300 TIMELINE_CURRENT013_RUN=1 TIMELINE_CURRENT013_APP_TREE=530019d089acc3cdb36f3624bcfa98dcd9726df9 TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_CACHE_ID=parent-delete-tree530019d089acc3cdb36f3624bcfa98dcd9726df9-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-client13-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-runnerda7944483b16fbd6f880a4958c4761eb62b17dae894b63ee5aec8cf3c3088abf-helper82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901 node scripts/testing/current013-parent-delete.mjs

Do not claim writer retirement until this real gate proves mounted acceptance, same-property 409 and draft retention, lost ACK/restart/recovery, inverse restoration, exact RAW/mirror/opaque/registry/closure preservation, and zero legacy traffic.
