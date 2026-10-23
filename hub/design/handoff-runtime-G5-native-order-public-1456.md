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

The refusal is a distinct boundary from the reviewed Runtime physical-pin seam, but its dynamic throw site is not retained. The response text has a static Agent candidate at `astrid/sdk/timeline/_recording.py:286`; the only retained `_check_reservations` path is from the invalid observer's forward history replay through `RequestCommitPort.revision_closure`, not the completed redo. The test therefore did not reach its later intervening-overlap refusal or no-write assertions.

## Evidence and limits

Evidence is under `workers/rt-G5-native-order-public-1456/evidence/`; the bounded manifest is `design/handoff-runtime-G5-native-order-public-1456.manifest.json`. `git diff --check` passed and both assigned worktrees remained clean.

An observer attempt is retained but explicitly invalid for acceptance: tracing caused a pytest timeout during Runtime history replay after 61.59 seconds. The completed uninstrumented result above is authoritative for the qualification. Because the body stopped at redo, post-redo SQL/history/canonical no-write equality and historical 503 behavior remain unverified. No code, test, pin, source port, guard, or product behavior was changed.

Recommended next step: manager-owned follow-up for the Agent authored-guard/redo replay boundary, preserving the passing physical-occurrence correction and rerunning the unchanged original body only on a reviewed fix.

## Independent R2r/G5 review correction — 1505

**Verdict remains FAIL for the whole public inverse; this is not a behavior PASS.** The exact Agent `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee` / Runtime `9ce4242bc01f100bab9efc51032a73985cefb2b2` pair and the unchanged target-function body (`6798` bytes, SHA-256 `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`) are retained. The completed uninstrumented run proves forward acceptance and whole undo acceptance, then a redo refusal with `conflict / original authored guard changed`, before redo assertions. Final overlap refusal, post-redo no-write equality, and historical 503 behavior remain unverified.

### Causal ownership and evidence boundary

The prior wording over-locates the redo failure. The completed uninstrumented traceback ends at Agent `astrid/sdk/timeline/sync.py:558`, where the returned error is converted to `CommitConflict`. It contains no provider throw stack, no redo request body, and no Runtime/Agent source frame for the guard that produced the response.

The retained observer is explicitly invalid (`pytest-timeout` after `61.59s`) and its stack is from the initial forward attempt, not redo: Agent `commit.py:1138` → `_check_reservations` → Runtime `RequestCommitPort.revision_closure` → `timeline_commit_store._verify_accepted` → Runtime `timeline_commit_auth.validate`/`site`. It proves neither the redo cause nor `_recording.py:286`; it stopped in Runtime history authentication because tracing overhead caused the timeout.

Static inspection of the exact Agent tree finds the response text only at `_recording.py:286`; the `guard` helper is called by inverse code at `inverse.py:640`, `650`, and `653`. `_check_reservations` does not call `guard`; it scans history and loads Runtime closures (`commit.py:676–786`) and was only a caller/replay path in the invalid observer stack. Runtime `9ce4242` has no matching `original authored guard changed` source text. Therefore the strongest supported classification is: **the provider returned an Agent-shaped authored-guard conflict, with a static Agent `_recording.py:286` candidate, but the actual throwing source/ref/path/base/theirs for redo is unknown from retained evidence.** Do not attribute the redo refusal specifically to `_recording.py:286` or `_check_reservations` as an observed dynamic source.

The exact target body, pins, heads/trees, packet and evidence hashes were rechecked against the retained manifest; the target function slice is byte-equal (`6798` / `c2711a2d…`) and both source worktrees are clean. The packet contains only `body`, `events`, `origins`, and schema metadata—no persisted redo request/reply or complete redo guard details. No credential-like material was found in the retained evidence scan. No product/test/schema/client/pin/contract/config/env/Git file was changed, and no journey was rerun.

Minimal artifact needed for any causal follow-up: one fresh, reviewed reproduction retaining the redo request and complete returned error envelope (including conflict reason and exact guard `ref`, `path`, `base`, and `theirs`), plus the provider traceback/source identity for that redo call. This review makes no repair or Runtime waiver recommendation.
