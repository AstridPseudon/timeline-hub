# RT07 accepted-retry upgrade review

## Verdict

**APPROVE for the requested accepted-publication replay upgrade only.** The
other two legacy positives remain OPEN, and the RT07 deletion remains held
pending normal014 adoption and current-base composition, as directed.

Reviewed the held branch `tl/rt-m2-rt07-legacy-retry-success-preserve` at
`1cfab2e` against its `1740514` parent and current `tl/integration`.

## Review findings

- The new setup is authoritative. It archives the exact pre-retirement Runtime
  commit `a020a1c77a07aa657efb60b0442450209e55e470`, runs its existing
  `_ready_authoring_attempt` fixture and public `publish_timeline_render`, and
  serializes the actual body/result/task/attempt identifiers. The candidate
  does not fabricate a publication row, result, receipt, history entry, or
  provider.
- The old positive's assertions map one-to-one: real a020 acceptance; current
  `TimelineCommitStore.bootstrap` canonical-head retarget; current canonical
  cancellation; Runtime close/reopen; existing task-spec and timeline archival
  fault injection; exact replay; changed-payload refusal; and unchanged SQLite
  plus CAS/staging state. The current retired method returns only the stored
  published checkpoint result after request-hash and stored-target checks; it
  does not run the removed writer or consult the live target on that path.
- The changed-payload and no-write assertions remain active. No blanket/new
  xfail, fake `PreparedProvider`, new writer, or bypass was added. The other
  legacy positives are unchanged/open.
- No external ORCH/worktree path is embedded in the test. The temporary
  archive is under pytest's temporary root and the source root is derived from
  the test file.

## Portability prerequisite

The setup has a real Git-object dependency: it invokes `git archive a020a1c`
at test time. `a020a1c` is **not an ancestor of the held branch** (ancestry
check exit `1`), although it is present in current `tl/integration` (exit
`0`). A shallow checkout or patch-only delivery that does not retain that
object will fail before exercising the test. Preserve the object in the
current-base bundle/delivery, or replace this setup with a committed portable
fixture before any standalone delivery. This is a delivery boundary, not a
replay-logic defect.

## Evidence

Existing worker evidence was not rerun, per the explicit instruction:

- `PYTHONPATH="$PWD:/home/user/work/venv-runtime/lib/python3.11/site-packages" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_render_publication_authority.py -k exact_published_checkpoint_replays_before_live_target_changes`
  — **1 passed, 20 deselected**.
- The worker's narrow authority command selecting
  `retired_writer or published_checkpoint or exact_published_checkpoint` —
  **4 passed, 17 deselected**.
- The worker also recorded `compileall`, `git diff --check`, and a final
  cache-free targeted replay run as passing; no full suite or renderer run.

Independent static checks:

- `git show --check --oneline 1cfab2e` — passed.
- `git diff --check tl/rt-m2-rt07-native-final-deletion-join..tl/rt-m2-rt07-legacy-retry-success-preserve` — passed.
- `git diff --check tl/integration..tl/rt-m2-rt07-legacy-retry-success-preserve` — passed.

No product or test files were changed by this review.
