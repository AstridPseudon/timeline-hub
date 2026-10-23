# Runtime G5 native-order public qualification — R2r report

## Verdict

**Whole public inverse: FAIL.** The reviewed Runtime `e3159` correction is exercised on the exact Agent `91ac…` caller and passes the meaningful physical-occurrence seam during forward restructure and whole undo. The unchanged original body then reaches a distinct redo boundary and refuses with `original authored guard changed`; no repair or retry was attempted.

G5 remains P1-gated. This does not claim a whole-journey pass, the later overlap refusal, or historical 503 behavior.

## Exact source and preflight

- Agent: `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`, tree `ac1251cdc911b99d690d303cdd777fe14643bdb1`, clean before/after.
- Runtime: `9ce4242bc01f100bab9efc51032a73985cefb2b2`, tree `92ab1f5f739ffdfedf7b25fbd2a7b46ae42c5d1a`, clean before/after. This is the reviewed merge of `e3159e353c6184e146dde4e759db24f2e9ffc66b`.
- Original test source was unmodified. The target function body is 6,798 bytes with SHA-256 `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d` before and after.
- Public method signature: `_PublishMixin._commit_restructure(self, message: str, *, idempotency_key: str | None, client: Any, force: bool) -> dict[str, Any]`.
- Non-inverse real-fixture preflight: `2 passed in 24.16s`. It verified `local == base`, a real current base pair and digest, three native inputs, full-v2 request/reply shapes, and module origins. Captures are in the evidence directory; hashes and pair details are in the manifest JSON.

## One unchanged original-body result

Command (run from Agent `91ac…`):

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-G5-native-order-public-1456 PYTHONPATH=/home/user/work/wt/agt-pin-91ac58a9:/home/user/work/wt/rt-G5-native-order-public-1456:/home/user/work/wt/rt-G5-native-order-public-1456/packages/python /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=60 tests/sdk/test_timeline_restructure_guarded_runtime.py::test_restructure_whole_inverse_redo_and_intervening_overlap_refusal
```

Result: `1 failed in 11.56s`.

Observed progression:

1. Forward restructure was accepted.
2. Whole undo was accepted through the corrected Runtime physical `parent/occurrences` authentication/projection seam.
3. Redo stopped before its assertions. Runtime returned `code=conflict`, message `original authored guard changed`, with no receipt; Agent `_response` raised `WorkspaceClientError`, then `TimelineSession._flush` mapped it to `CommitConflict` at `astrid/sdk/timeline/sync.py:558`.

The distinct boundary is Agent-side authored-guard replay at `astrid/sdk/timeline/_recording.py:286`, reached from `astrid/sdk/timeline/commit.py:_check_reservations` while Runtime replays history through `RequestCommitPort.revision_closure`. This is not the reviewed Runtime physical-pin seam. The test therefore did not reach its later intervening-overlap refusal or no-write assertions.

## Evidence and limits

Evidence is under `workers/rt-G5-native-order-public-1456/evidence/`; the bounded manifest is `design/handoff-runtime-G5-native-order-public-1456.manifest.json`. `git diff --check` passed and both assigned worktrees remained clean.

An observer attempt is retained but explicitly invalid for acceptance: tracing caused a pytest timeout during Runtime history replay after 61.59 seconds. The completed uninstrumented result above is authoritative for the qualification. Because the body stopped at redo, post-redo SQL/history/canonical no-write equality and historical 503 behavior remain unverified. No code, test, pin, source port, guard, or product behavior was changed.

Recommended next step: manager-owned follow-up for the Agent authored-guard/redo replay boundary, preserving the passing physical-occurrence correction and rerunning the unchanged original body only on a reviewed fix.
