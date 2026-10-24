Implemented the Runtime-owned correction in [timeline_commit_auth.py](/home/user/work/wt/rt-R2r-historical-image-sol-0353/runtime_protocol/timeline_commit_auth.py) with a separate [regression file](/home/user/work/wt/rt-R2r-historical-image-sol-0353/tests/test_timeline_inverse_historical_image.py).

The genuine standalone capture isolates **redo**, after accepted placement and undo. Runtime’s native projection contains only `parent`; the effect projection also restores two authenticated physical roots. The first missing root is:

```text
internal-revision:authoring-timeline-revision-f910933b73f56ce54527d7f6c40e60bb75e2c7771837f26dd29933e285ca9aed
path: []
native: absent
effect payload: {"clips":[],"output":{},"registry":{"assets":{}},"tracks":[]}
```

Owner: `occurrence:return-owner/shot`. Evaluation boundary: inverse of accepted undo `txn-3f933f9b2e154c4990f16b4e27e2690a`, step `owner-boundary`, command `[0]`, native range `[0,1]`, effect range `[0,3]`.

The fix recognizes this sealed single-stage occurrence retirement and restores only payloads, immutable pins, and owners matching authenticated source history. Native counts and range checks remain strict. An initial draft changed nine existing refusal-message paths; narrowing the condition restored those assertions unchanged.

Validation:

```bash
ASTRID_CHECKOUT="$TMPDIR/agent" PYTHONPATH=. \
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= \
-p no:cacheprovider tests/test_timeline_inverse_historical_image.py \
--basetemp="$TMPDIR/qualified-current" --tb=short
```

**13 passed.** Covers real `timeline.inverse`, preview, retry, unchanged source, native/effect counts and values, physical pins, ownership, coherent image forgery, mutable source claims, and no-write refusals.

```bash
PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q \
-p no:cacheprovider \
tests/test_timeline_inverse_occurrence_retirement.py \
tests/test_timeline_inverse_stage_authentication.py \
tests/test_timeline_commit_authentication.py \
tests/test_timeline_history_authenticated_read.py \
tests/test_timeline_source_duplicate_authority.py \
--basetemp="$TMPDIR/qualified-controls" --tb=short
```

**243 passed, 74 deselected** by configured integration/live selectors.

Additional evidence:

- New regression on base: **1 failed** at the demonstrated projection mismatch.
- Exact 61,298-byte capture replay: **old RED / new GREEN**; SHA-256 `2a157e975c3c8f022e119375bf67fe8fbc2153282549c88500c5b8f965379131`.
- All **11** retained manifest artifacts matched. Both 0236 captures still pass; both parent-owner captures remain rejected.
- `ruff check --no-cache runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_historical_image.py`: passed.
- Scoped Pyright parent/final: **0 → 0 diagnostics**, no NEW identities or multiplicities.
- `PYTHONPATH=. /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check` and `git diff --check`: passed.
- All **502 protected tracked files** match base, including store, existing tests, contracts and generated files. Aggregate SHA-256: `75de7fb81b97ba2320751d61c6b0fa3da9cc8fb6c0a15552fc8e5ea95d26ce3e`.

Origins:

- Runtime HEAD: `36760ee0ad4b064a849edb3fc6e5a60a43fe8f48`; tree `11389911c2eec5acc901ab3b70e234fad9e1bc5d`.
- Exact readonly Agent archive: `12701589abffd840054515996612d0ed0dd33af0`; tree `efad939c87b5805f2a6f45827ec1a17db3eac5f4`.
- Projected final Runtime tree: `40eb05d5a51b8d7b31cbfad8a38afeb3318fbd44`.

The fresh five-field source reference and capture are under `/tmp/w-3031a908e5/`; they are temporary standalone evidence. **The original 0339 private packet remains uncertified**, so original-case recovery is unverified. No original-family, full, HTTP or browser run occurred.

Wrote `commit-msg` and `DONE`. Recommend independent review, then orchestrator-authorized original-case qualification.