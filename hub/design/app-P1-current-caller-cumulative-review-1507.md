## Verdict: FAIL

Reviewed commit `8bbae64e21c5bcf252d4e854509fa2fe505a66d9` (two artifacts only). No worktree changes made.

Findings:

- `assert_locks()` checks the App lock at `HERE` instead of authenticated production `APP` ([p1-current-caller.py:179-188](/home/user/work/wt/app-P1-current-caller-cumulative-review-1507/p1-current-caller.py:179)).
- The emitted production command consumes `ASTRID_REMOTION_PROJECT_DIR` at an unauthenticated bench path, while validation hashes a different Composition graph ([p1-current-caller.py:247-256](/home/user/work/wt/app-P1-current-caller-cumulative-review-1507/p1-current-caller.py:247), [p1-current-caller.py:454](/home/user/work/wt/app-P1-current-caller-cumulative-review-1507/p1-current-caller.py:454)).
- The consumed schema path is not origin/digest-bound. Current installed schema hash is `5592…86f`, while the authenticated vendored schema is `4d74…b3d`; `--dry-source` still passes.
- The served App `dist` is not hashed or explicitly bound; the harness may reuse an unpinned build.

Evidence passed:

- `py_compile`, normal and `-O` source-only admission
- JSON validation
- Generated shell `bash -n`
- All requested negative controls: wrongsource, tree, parent, lock, target, body, poison
- Additional client/import/interpreter/graph/stage refusals
- `git diff --check`
- Exact P1 body/blob and two-case titles remain unchanged
- Live App/Agent/Runtime refs, trees, parents, and clean states match facts

The emitted shell invokes the real two-case P1 command and retains source/environment/original stage files, but the actual P1 journey was intentionally not run (no browser/service/HTTP/native/full execution).

Source concurrency is correctly fail-closed at the current exact heads; advancing source requires refreshed facts, not a waiver.

Recommended next step: fix the consumed-path/schema/dist bindings, then repeat this independent review.