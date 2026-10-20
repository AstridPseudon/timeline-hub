# Real Delete handler diagnosis — central tracing handoff

**Status: blocked pending a fresh committed central diagnostic run. The first false guard is not yet proven. No product fix or root-cause claim is made.**

## Source and prior evidence

Started on App `f732a73a4ee35cc9510f53b6f0e4f69dc8486702`, tree `3d7ec25cb5f37b8c21647009e563fd6235facee4`, as assigned. Read PLAN.md, COMMON.md, the repo CLAUDE.md/.cursorrules, the video-editor architecture document, and `design/app-delete-marquee-owner-committed-gate.md`.

The relevant prior central test is:

`app-m2-delete-marquee-owner-committed-gate-e2e-parent-delete-marquee-owner-committed-tree3d7ec25c-appf732a73-agent8130-runtime2c4-public13-e2e-integration-1020183936-2909`

It passed all source/dependency/browser guards and failed the first real case at 0 POST. I read its preserved trace ZIP without launching a browser:

`/tmp/tl-marquee-owner-parent-delete-run.0jjpib/browser-artifacts/clip-delete-command-M2-cur-9193a-rse-restore-raw-opaque-clip/trace.zip`

The focused `f2-app-clip` role button is inside the one visible command-ready editor shell in `after@call@41` (95380.242 ms). The Delete dispatch follows; `after@call@43` (95394.532 ms) reuses the prior DOM tree. This proves neither the listener guard values nor a specific native capture refusal. The preserved console output does not identify that branch. The 90-second error-context snapshot cannot establish whether a transient toast appeared earlier.

## Exact source path and the verified omission

| Step | Existing source | What is established |
|---|---|---|
| Clip input | `ClipAction.tsx:573` | Its React key handler handles Enter/Space; Delete returns and can bubble. The real test selected and focused this role button. |
| Native listener | `useKeyboardShortcuts.ts:208` | The window listener first checks `runtime.shellRootRef.current` containment, then editable target; Delete requires captured `hasSelectedClip`. Their live values are absent from the old trace. |
| Scoped selection | `TimelineEditorCore.tsx:505`, `useTimelineState.ts:808` | Core selection forwards the mounted owner; the shell's selection is assembled from `useTimelineSelection` with that owner. A selected DOM clip alone does not expose the shell listener's captured boolean. |
| Shell callback | `TimelineEditorShellCore.tsx:337` | Data-item selection returns first; a group mutation uses applyEdit; ordinary selection forwards to `editorOps.handleDeleteClips`. |
| App Provider/store | `VideoEditorProvider.tsx:752` | The Provider replaces the ops slice via `syncOpsSlice`. This assembly omits `clipDelete` (also `clipMove` and `element`), although `useTimelineState.ts:1181` includes it. **This is a concrete omission, not a proven explanation of this keyboard failure.** |
| Direct delete callback | `VideoEditorProvider.tsx:781`, `useTimelineState.ts:905`, `useClipEditing.ts:292` | The same Provider does preserve `handleDeleteClips`; that callback receives the native port directly from the mounted command session. Its direct path does not read `store.ops.clipDelete`. Therefore fixing only the ops property cannot be called the keyboard root cause from current evidence. |
| First deletion guards | `clip-editing/useClipDeletion.ts:22` | Requires current data, valid IDs, permission to delete pinned members; native single-parent branch then checks editability and captures/finishes/submits. Exceptions become an error toast. |
| Port wrappers | `useTimelineCommandSession.ts:197`, `commitSession.ts:336` | The mounted port checks pending snapshot work, then the raw-authoring/session identity and command guards. None of these actual invocations is recorded by the old browser trace. |

No production code was changed. No absent port was injected. No delete callback, command service, capture, or submit was invoked by the new tracing code.

## Change ready for harness commit

Only two App test files change:

- `tests/e2e/local/support/delete-keyboard-trace.ts`: opt-in, read-only DevTools inspection of the installed window Delete listener, its closure callbacks and existing native ports. It records original function source, lexical values, target/editable/root-focus data, selected IDs, current head/metadata/groups, callback/port presence, actual breakpoint entries and caught exceptions. It uses existing function-call breakpoints and side-effect-checked inspections; it installs no DOM listener or replacement handler/state/port.
- `tests/e2e/local/clip-delete-command.spec.ts`: brackets each original real Delete and its original first-POST assertion with optional trace collection and a failure-safe Playwright attachment. `TIMELINE_DELETE_KEYBOARD_TRACE=1` enables it. The attachment is `delete-keyboard-listener-scopes`.

All original real Delete, group261, raw/opaque, reload/undo/restart, exact request/receipt, 409/draft, and 0-legacy assertions remain. No readiness wait, product marker, counter, framework, public API, or wire change was added.

Candidate App tree, computed using Git object hashing without writing Git objects/index/refs:

`2ccb9f864770bc714a8e5ad9f5b28bc8762fb655`

The harness must supply the resulting commit SHA after this worker exits. I cannot create that commit under the task's read-only Git rule.

## Central handoff

The original registered suite is fixed to the old App tree; it was not rerun against changed source. A source-specific handoff is prepared in this worker's `notes/`:

- `suite-registration.txt`: exact new registration row, with `PIN_HARNESS_COMMIT_HERE` placeholders that must be replaced with the literal harness commit whose tree equals the candidate above. It is **not registered or submitted**.
- `run-parent-delete-real-handler-public13.sh` and `parent-delete-real-handler-public13-runner.mjs`: copies of the last strict wrapper, repinned to the exact candidate tree, a new diagnostic cache identity and private paths. The runner requires a full App SHA mapping to that exact tree and descended from f732a73a. It requires tracing enabled.

Preserved tuple: Agent `8130a401bf44a518d5a40ae274d398b8c560be55` / tree `236c3e57e0265c52b81ba8085de3193026176bff`; Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / tree `7ab412cc4bcbe517efcfa806e092336390312e18`; public13 archive SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` / all77; public source `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`; Runtime all75; Chromium 141.0.7390.37 / SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`. Source/public/peer/cache pre/post guards remain.

After pinning and registration, request only:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$($ORCH/bin/request-test app-m2-delete-real-handler-hard-diagnosis e2e-parent-delete-real-handler-diagnostic-tree2ccb9f86-agent8130-runtime2c4-public13-e2e-integration)
$ORCH/bin/wait-test "$R"
```

The existing two-case ordering remains; a terminal first-case failure stops the second. A debugger-assisted pass would be diagnostic only, since pausing changes scheduling. Use the attachment to prove the first false guard or exception, add that focused behavior regression, make only its existing-carrier fix, then run the normal strict two-case gate once on the repaired committed tree with tracing off. Do not declare the omitted ops port or another readiness condition the root cause without that evidence.

## Commands and results

Working directory: `/home/user/work/wt/app-m2-delete-real-handler-hard-diagnosis`.

```sh
NOTES=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-delete-real-handler-hard-diagnosis/notes
node --require "$NOTES/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "$NOTES/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.test.tsx src/tools/video-editor/components/TimelineEditorShellCore.test.tsx src/tools/video-editor/hooks/useKeyboardShortcuts.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/useTimelineOps.clipDelete.test.ts src/tools/video-editor/commands/commitSession.clipDelete.test.ts
```

**6 files / 222 tests passed**, 29.84 s. These are the unchanged neighboring unit suites; they do not exercise the new CDP helper or qualify the failing real journey. The first invocation collected 0 tests because my private alias pointed the package root at a directory and bypassed its subpath exports. I corrected only that private config to use the package's published export targets, then ran the command above successfully. No shared dependency was changed.

```sh
node node_modules/eslint/bin/eslint.js tests/e2e/local/support/delete-keyboard-trace.ts tests/e2e/local/clip-delete-command.spec.ts --max-warnings 0
```

PASS, exit 0.

```sh
node --input-type=module - <<'JS'
import { transform } from 'esbuild';
import { readFileSync } from 'node:fs';
for (const file of ['tests/e2e/local/support/delete-keyboard-trace.ts', 'tests/e2e/local/clip-delete-command.spec.ts']) {
  await transform(readFileSync(file, 'utf8'), { loader: 'ts', format: 'esm' });
  console.log('transpile PASS', file);
}
JS
bash -n "$NOTES/run-parent-delete-real-handler-public13.sh"
node --check "$NOTES/parent-delete-real-handler-public13-runner.mjs"
git diff --check
```

All PASS. A read-only Python tarfile comparison verified the public13 archive SHA and every one of the 77 installed package files used by the private Vitest aliases. The aliases and Vite cache are in this worker's notes directory, outside shared node_modules. Its generated Vite cache is cleaned up.

No full suite, project TypeScript check, install, local browser/socket test, central browser submission, Git commit/merge/checkout, integration worktree modification, or Runtime/Agent edit was performed. The DevTools helper is syntax/lint checked but browser behavior remains unverified. A first-false-guard regression and product fix remain blocked on that actual central observation.
