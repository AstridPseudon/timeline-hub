# Runtime handoff: R2r historical review 1604

## Verdict

**PASS** for exact source `1948d06a3c931210efe425ae5e0cf7a079433c38`, tree `5a8594a623dc07c0cb61c45000523eac427d3a7a`, including inherited `85b2feeb58bc54174ac7b89fda4805883865d3b2`. No Runtime product edits were made. The review worktree is clean.

This handoff covers source-review approval only; it does not approve the separately held current-only landing worker or merge ancestry.

## Review result

The candidate's private sequential capture is retained only after accepted validation and is not used as its own authority. On historical verification, the Runtime reloads the accepted record/data and checks real context, request identity, realm, publisher, idempotency, invocation, BASE/HEAD, prepared data, accepted events, and public payload before independently reconstructing original inputs from BASE plus preceding authenticated effects and landing inputs from HEAD. It replays against actual continuations/history. Public history verifies first and removes `_sequential_execution`, so the private proof is not returned publicly. Preview does not retain it.

The existing fail-closed paths and auth/native/ABA/strict guards remain covered. The five strict negatives resolve to `value_conflict`, `value_conflict`, `selection_changed`, `outside_closure`, and `history_unavailable`. The source's auth and core commit modules are byte-identical to `85b2`.

## Evidence

- `git diff --name-status cfa0af0d476e6954df041c08d7ef378fd6782932..1948d06a3c931210efe425ae5e0cf7a079433c38`: six expected files; stat 1279 insertions / 37 deletions.
- Candidate versus `85b2`: only `runtime_protocol/timeline_commit_port.py`, `runtime_protocol/timeline_commit_store.py`, and `tests/test_timeline_commit_sequential_verifier.py`.
- Manifest verification: all 80 manifest entries matched declared size/SHA-256; all 78 frozen-artifact and client34e/schema/d106 preservation assertions remain true. Original Agent test bytes and AST match the manifest.
- Author handoff, manifest, prior 1512 FAIL, and causal 1534 report were read. The author evidence included 27 reports and 23 captures; the independent fresh evidence is at `/tmp/w-d7703655db/original9-independent-final` and contains 23 captures and 27 reports.
- Runtime exact nine-file command: **366 passed, exit 0**.
- Independent author-exact original9 command: **9 passed in 166.57s, exit 0**, with all report phases passed and no credential-bearing observer fields.
- Private moved-service close/reopen check: **1 passed in 5.88s, exit 0**.
- Ruff: 22 baseline / 22 candidate, zero normalized additions/removals; Pyright: 80 / 80, zero normalized additions/removals. Both raw tools retain their baseline exit 1. `git diff --check` exit 0.

The exact commands and full findings are in the worker report:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-history-review-1604/report.md`.

## Limits

No full/browser/live-socket, native14/40/281/58, benchmark, provision, daemon, Git-write, or current-only integration suite was run. Keep the current-only 2593942 worker separately reviewed.
