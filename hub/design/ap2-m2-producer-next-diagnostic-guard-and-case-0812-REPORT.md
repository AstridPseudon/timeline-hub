# Producer diagnostic guard and case 0812

## Static wire-fit preflight

- Source was the assigned App worktree at commit `6b0267c62aa8773132f1496d5014279e6c1edf61`, tree `c1ac3383624322ae8d67b10dee36965670d91cd7`.
- The only live gesture callers in the original case are `transcriptRegenerate()` and `sceneMoveShots()` in `tests/e2e/local/support/producer-ownership-current-pin.ts`, invoked by the unchanged case in `tests/e2e/local/producer-ownership-current-pin.spec.ts`.
- Fixture/bootstrap publication is setup only and was excluded from the mutation-caller count. The live producer caller count is 2; no live caller was changed by this worker.
- Transcript caller: `clip.remove` for the extension-owned stale caption is converted by the native host to `clip.delete`, selector `parent/clip:<transcriptStaleClipId>`, args `{}`. Protected foreign/user rows are filtered out by the extension.
- Scene caller: the owned same-track shot produces `clip.move` intent `{at: 1}` and `clip.update` hold `5`. Native capture serializes these as `clip.move` selector `parent/clip:<sceneOwnedClipId>`, args `{on: 1}`, followed by `clip.set` on the same selector, args `{values: {hold: 5}, clear: []}`.
- The pinned Agent commit `8130a401bf44a518d5a40ae274d398b8c560be55` (tree `236c3e57e0265c52b81ba8085de3193026176bff`) and Runtime commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a` (tree `7ab412cc4bcbe517efcfa806e092336390312e18`) expose the required `clip.delete`, `clip.move`, and `clip.set` operations. Their checked-in edit-command schemas are byte-identical, digest `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.
- No required command or field is absent. No future operation was activated. `timeline.inverse` is framework recovery traffic, not an additional producer caller.
- The original assertion’s `{at: 1}` spelling is retained unchanged; `{at}` is the patch intent while `{on}` is the pinned native wire field. This is an expected diagnostic boundary, not a wire-fit blocker.

## Central-run gate state

The approved retention artifacts are read-only and are checked by the final custody gate. The final service tree must remain `c1ac3383624322ae8d67b10dee36965670d91cd7`; the protected keeper must remain HEAD `6b0267c62aa8773132f1496d5014279e6c1edf61`, the same tree, clean, and marked `KEEP`. Agent/Runtime pins, graph digest/version/list-one/zero-test/child-RC guards, source/helper/spec/config hashes, 10 GiB floor, and two-copy isolation are delegated to the approved gate and runner.

The earlier parent run `31285` is terminal FAIL and selected run `8082` is terminal FAIL, as required. A separate parent investigation was active during the initial preflight; it completed before registration/submission, and the local browser lock was free when the actual suite ran.

## Registration and actual result

- Registered exactly one App suite: `ap2-m2-producer-next-diagnostic-guard-and-case-0812-integration`.
- The registration was generated from the literal gate path and programmatically checked digest `e92ac3920d0f2e197c482444183518629f72e1f83b728fecb68e5553c45a48d0`; shell syntax and the final guard expression passed before submission.
- Submitted exactly once with `--no-cache`: run `ap2-m2-producer-next-diagnostic-guard-and-case-0812-integration-1021081726-17481`.
- Central result: FAIL, exit 1, 78 seconds, App tree `c1ac3383624322ae8d67b10dee36965670d91cd7`, `1` test collected and `1` test executed (`1 failed`). The central log is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-next-diagnostic-guard-and-case-0812-ap2-m2-producer-next-diagnostic-guard-and-case-0812-integration-1021081726-17481/log.txt`.
- First failure boundary: unchanged `tests/e2e/local/producer-ownership-current-pin.spec.ts:92`; expected `transcript-lane-chip` count `2`, received `0` after the 5-second wait. The case stopped before `transcriptRegenerate`, `sceneMoveShots`, any mutation request, lost-ack retry, inverse, or zero-legacy assertions. This result does not establish a producer command cause. It does not reclassify or replay prior run `23671`.

## Evidence and cleanup

The central log recorded the real Playwright paths for `error-context.md` and `trace.zip` under its temporary `.public13-effective-ordinary/browser-output` tree. The run’s cleanup removed that temporary root, and no durable `evidence/failure-*` directory, `child.log`, `identity.txt`, or `SHA256SUMS` was visible under the approved retention worker path after completion. Therefore the required durable error-context/trace/child-log/identity-manifest custody condition could not be verified. No retry was submitted.

This is a blocked evidence handoff, not a product diagnosis: the exact first assertion boundary is known, but the run did not leave the mandated durable packet. The approved source/spec/helper/selector bytes were not changed; the only shared control change was the one unique suite registration above.
