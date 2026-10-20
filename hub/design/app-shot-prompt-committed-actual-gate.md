# App M2 committed settings.prompt browser gate

Status: **blocked on the first real product assertion**. The final central run used the committed composed producer + journey source and executed exactly one browser test.

## Source and frozen inputs

- App source commit: `f5fa987f6298bf3d1cb02ecf4e812b84e4ce4ef8`
- App source tree: `e30a482be493831f318a19aa3c911e68e5eb21b2`
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`
- Composition public13 archive: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 regular members
- Runtime producer manifest: 75 artifacts; schema and producer hashes matched the frozen values
- Public-source, setup, resolver, peer, Chromium, and cache guards matched before and after the run
- `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST` were unset

## Central test evidence

Final test ID:

`app-m2-shot-prompt-committed-actual-gate-e2e-shot-prompt-f5fa987f-treee30a482b-agent8130-runtime2c4-public13-wrapper809efb-e2e-integration-1020191958-12106`

Passed before the browser stage:

- pinned source preflight and postflight
- public-source and resolver/setup guards
- public13 overlay, 77-member archive, and peer checks
- Composition resolver tests: **9 passed, 0 failed**
- Playwright discovery: exactly **1 test in 1 file**

Browser result: **1 test failed** after 9.3s. First failure:

`tests/e2e/local/shot-settings-prompt-command.spec.ts:133`

The first call to `editPrompt` could not find `getByRole('dialog').locator('#batchVideoPrompt')`. The Playwright error context shows the real dialog titled `Edit f2-shot` contains the Shot timeline, clip buttons, and navigation controls, but no prompt textbox. The failure occurs before any prompt commit, reload, undo, lost-ACK, 409, or legacy-write assertion can execute.

Postflight passed after the failure, including source equality and dependency-cache immutability. The trace and error context are under:

`/tmp/tl-shot-prompt-public13-809efb-run/browser-artifacts/shot-settings-prompt-comma-24a54-and-relevant-conflict-draft/`

## Wrapper/setup corrections made

Three earlier registrations stopped before the product case and were corrected in fresh registrations:

1. The first suite line had a malformed setup guard value; the wrapper reported the received pins.
2. The generated external Playwright config could not resolve `@playwright/test`; it now uses the verified absolute module path.
3. The spread direct config retained a relative `globalSetup`; the generated config now points to the snapshot's absolute setup file.

These were routine wrapper issues. No product assertion was changed and no browser bypass, injected port, fabricated response, install, local browser, full suite, or TypeScript run was used.

## Blocker and next step

The composed product mounts `ShotSettingsEditor` with `canonicalOnly`, which intentionally omits the legacy generation/settings form containing `#batchVideoPrompt`. The actual embedded canonical dialog therefore has no prompt editing control for this journey. The App owner must decide/implement the real user-facing prompt control in the canonical shot UI, or provide the intended existing UI route that exposes it while retaining the native `settings.prompt` producer. Then rerun this same strict one-case gate with a fresh source/tree and wrapper key. The settings row remains open.

