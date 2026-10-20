# AP2 M2 parent negative-response causal evidence

## Result

HOLD: the parent5013 timeout is caused by a shared App consumer gap, so no
qualification gate was justified or run. No App product files were changed in
this worker.

The current prepared-drop path in
`src/tools/video-editor/hooks/useAssetManagement.ts:269-317` always applies a
local `prepared-media` edit. It no longer accepts a native `commands` port or
calls `commands.addClip` for a prepared video carrying `mediaSelection`.
`src/tools/video-editor/hooks/useTimelineState.ts:936-947` supplies no native
media command service. The import preparation still captures and freezes the
five-field selection (`src/integrations/runtime/dataProvider.ts:1601-1618`),
and the verified provider read remains intact (`dataProvider.ts:789-809`).
Thus import and normal selection can succeed, but no verified-media GET is
issued for the negative response waiter. This explains the 90-second timeout
without changing the negative refusal, positive original-200 assertion,
selector, or response interception.

The prior real retained run shows the route is viable when the native consumer
is reached: import 201, normal selection 200, tampered verified selection 404,
second import 201, normal selection 200, positive verified selection 200. The
5013 disposable root was deleted before evidence retention, so its trace,
console, request, and response artifacts are explicitly unavailable rather
than guessed.

## Evidence and wrapper

Created the evidence-first adaptation:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-negative-response-causal-evidence/run-parent-manual-drop-evidence.sh`

It pins the current approved App tree
`78f3784287d78fc92677ebe5eb710d162b0f50ae`, reuses the current exact-three-
path driver/source runner, installs the EXIT trap before preflight, and copies
bounded trace/error-context plus redacted request/response/console summaries
and source identity before disposable-root cleanup. It does not revive the
older `a75e...` source tree. Its forced-failure retention probe passed.

Durable diagnostic records are under the worker's `diagnostic-evidence/`,
including the sanitized prior real-run records, current source identity,
5013 unavailable-evidence record, causal diagnosis, and exact proposed shared
patch. The proposed patch is HOME-only: restore the provider-bound
`parentMediaCommands` construction and pass it to asset management, then add
the prepared-video `commands.addClip` branch. No Runtime, schema, provider,
013/014 adoption, source pin, or driver changes are proposed.

## Custody count mapping

The current checked-in `current013-integration.test.mjs` and the approved
driver copy are byte-identical and contain 15 executable Node subtests; the
independent donor report records 16 for its earlier source-tree inventory.
The 15 current controls cover exact App tree, Runtime publication, all eight
inputs, path/dist rejection, both venv links, executable validation,
same-tree forwarding, three dirty-source cases, mutation, child status,
metadata failure, and byte fingerprints. There is no source diff identifying
a sixteenth current guard. I preserved the current 15 and reported the
unresolved historical one-count discrepancy instead of silently claiming a
missing guard or weakening any control.

## Verification

- `sh -n /tmp/.../run-parent-manual-drop-evidence.sh` — passed.
- `run-parent-manual-drop-evidence.sh probe` — passed; evidence copied before
  disposable-root cleanup.
- `node --test --experimental-test-isolation=none scripts/testing/current013-integration.test.mjs` — 15 passed, 0 failed.
- `git diff --check` — passed; App worktree remains clean.

No full suite, local browser/socket run, central gate, or blind 90-second rerun
was performed. The next step is to apply the exact shared App patch in HOME,
re-run the targeted consumer checks, then spend the single named real gate
only after source/setup/copy-count preflight passes.
