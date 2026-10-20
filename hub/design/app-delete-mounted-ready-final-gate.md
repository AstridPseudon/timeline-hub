# App M2 mounted-ready committed parent Delete gate

Status: failed qualification; no retirement claim.

## Exact source and guards

- App commit `59830d2e80b9653547c101e9d2d0db15a0db1601`, tree `bc7ae9f57e77f8013f7f95edaba4a58671ff40bc`.
- Parent `089065dd5`.
- Agent commit/tree `8130a401bf44a518d5a40ae274d398b8c560be55` / `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime commit/tree `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Public13 archive SHA `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; public source SHA `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`.
- Chromium SHA `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`.

The strict wrapper retained the all75/77/public13/Agent8130/Runtime2c4/source/cache/peer guards and ran both real-case patterns without focus bypass, direct handler calls, injected state, weaker source guards, or snapshot fallback. The new wrapper waited for `[data-command-session-ready="true"]` and a fresh empty owner before each case.

The exact new committed delta is limited to the readiness invariant: `TimelineEditorShellCore` exposes `data-command-session-ready="true"` only when the command-session state is `saved`; its focused unit test asserts that marker, and `openCommandTimeline` waits for the marker plus a fresh empty owner. No other gate assertions were changed.

## Results

Central run 1, suite ID `app-m2-delete-mounted-ready-committed-final-gate-e2e-parent-delete-mounted-ready-committed-treebc7ae9f5-app59830d2e-agent8130-runtime2c4-e2e-integration-1020175054-12215`, failed after 305s. All source, public13, vendor, runtime-lock, and peer pre/postflight checks passed. The first real case (`real parent DELETE: lost ACK`) timed out at `tests/e2e/local/clip-delete-command.spec.ts:222:55`: expected one Runtime POST, received zero. The strict wrapper correctly did not run case two.

The same suite was rerun once with `--no-cache` for diagnostics, ID `...-1020180158-15028`, and failed identically after 170s. It preserved:

`/tmp/tl-mounted-ready-parent-delete-run.NEDGHT/browser-artifacts/clip-delete-command-M2-cur-9193-rse-restore-raw-opaque-clip/trace.zip`

and `error-context.md`. The trace shows readiness changing false to true, the fresh-owner wait completing, the raw parent clip being clicked and asserted `data-selected`, focus being asserted, and `Delete` being pressed. The trace has no `/commit` POST; `wire.posts.length` remained zero. The final page snapshot has an empty Notifications region and no alert/toast. Case two was not run because the wrapper is strict.

Focused tests passed:

```text
Test Files  2 passed (2), Tests 145 passed (145)
Test Files  4 passed (4), Tests 47 passed (47)
```

The first direct Vitest invocation hit the known config-loader `__dirname` issue; the existing snapshot-preload runner then passed the focused suites. No full suite, tsc, install, local-browser run, or shared-cache/dependency write was performed.

## Source-path diagnosis

The Delete key is wired through `useKeyboardShortcuts` to `TimelineEditorShellCore`'s `handleKeyboardDelete`. That handler first tries `buildKeyboardDeleteMutation`; for the raw parent clip it should fall through to `editorOps.handleDeleteClips`, whose single-parent path uses `clipDeletePort`. The command-session wrapper requires `legacyClean`, captures/finishes/submits the native command, and the readiness marker is based on the session being saved.

The concrete new evidence is a reachability/state mismatch after readiness, not another readiness delay: the DOM selection and focus assertions passed, but no Runtime request or notification followed `Delete`. The likely cause is that the window keyboard callback did not reach the native `clipDeletePort` branch (for example, its captured `hasSelectedClip`/selection state did not match the rendered DOM), although the trace cannot distinguish that callback condition from an earlier handler branch. This is an inference from the source path and trace, not a claimed fix.

Group assertion 261 is unchanged. This gate is not qualified and no retirement claim is made.
