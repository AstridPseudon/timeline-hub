## Report

- Read PLAN §3, commit-v2, guard control, prior reports, and exact test bodies.
- Verified Runtime pin: `2b49da8d6d8dbb8245a1a7cc8d7eee7d3bdaae65`, tree `40eb05d5a51b8d7b31cbfad8a38afeb3318fbd44`.
- Ran the two exact selectors once with external instrumentation.

Result: **instrumentation failure; original test bodies unobserved**.

The probe raised `TypeError: _write() got multiple values for argument 'kind'` during fixture setup at the setup `track.create` commit. Runtime surfaced `CommitUnavailable`; both store snapshots showed no write. No retry was made.

Evidence:

- [capture-manifest.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-source-copy-observe-0447/evidence/capture-manifest.md)
- [actual-events.jsonl](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-source-copy-observe-0447/evidence/actual-events.jsonl)
- [test-run.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-source-copy-observe-0447/evidence/test-run.log)

Checks: AST/compile passed, `git diff --check` passed, worktree clean, original test/source hashes unchanged.

Source ownership remains unknown until a corrected single capture obtains actual boundary facts. Prior static proposal remains Agent `_recording.py:283-287` and inverse callers, with Runtime owning source/input/effect/history authority boundaries.