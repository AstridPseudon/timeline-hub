# ap2-m2 ordinary structural review

## Verdict

**ACCEPT — no blocking finding.** The two-file App member is structurally aligned with the current Agent native `track.create`, parent `clip.add`, and parent `clip.delete` contracts for the reviewed scope. It preserves raw authored rows and opaque fields, reserves created IDs once, records parent membership/order selections, uses sequential ordinals and derived-write causes, and refuses unsupported media/selector/timing/dependency cases before submission. The bounded projection updates authored structural collections only; it does not become normalized-row authority or alter display data lanes.

## Evidence

- Focused App lane:

  `node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/ordinaryStructuralMember.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts`

  **PASS — 4 files, 91 tests.**

- Project checks:

  `node_modules/.bin/eslint src/tools/video-editor/commands/ordinaryStructuralMember.ts src/tools/video-editor/commands/ordinaryStructuralMember.test.ts --max-warnings 0`

  **PASS.**

  `node_modules/.bin/tsc --noEmit --pretty false --incremental false`

  **PASS.**

  `git diff --check`

  **PASS.**

- Locked private App graph, using the recorded graph/source identity and private Composition 0.0.13 dependency, with the current structural source overlaid: the fresh TypeScript probe matched the current Agent engine byte-for-byte for full commands, records, and bundles for `track.create + clip.add` and for `clip.delete`. App records also matched Agent replay records/bundles.

  Artifacts: `app-ap2-m2-ordinary-structural-current-parity.ts`, `app-ap2-m2-ordinary-structural-agent-parity.py`.

- Agent inverse qualification: feeding the App-captured records and bundles into Agent's real `timeline.inverse` executor produced the same inverse records and bundles as Agent-native captures for both add and delete.

- The exact parity covers raw parent scope, reserved `parent/track:<id>` and `parent/clip:<id>` identities, membership/order selections, absent/present guards, destination-track reads/binding, opaque row retention, mirror derived writes, sequential ordinals, and no partial local mutation on collision/refusal.

## Not run / limits

- The requested Agent pytest lane was not executable in this environment: `/home/user/work/venv-agent/bin/python` does not exist, and `/usr/bin/python -m pytest` reports `No module named pytest`. No dependency installation or shared-environment mutation was attempted.
- No full, browser, localhost, live-socket, Runtime-door, or cross-product suite was run.
- The earlier installed-Composition `computeMediaTrim` limitation is not unresolved here: the fresh parity run used the locked private graph with the required export.

## Scope

No App source, tests, shared dependencies, pins, generated files, Git refs, ledger, or integration worktrees were modified by this review. The verdict is limited to the assigned ordinary structural member; wiring it into the live generic ingress remains outside this review.
