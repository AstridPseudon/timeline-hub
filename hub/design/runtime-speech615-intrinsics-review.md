# Runtime speech615 intrinsics review

Date: 2026-10-20 UTC

## Decision

**REJECT** `615a95a63c2ae79c6a47400ffc79a72dedd0bc5f` against base
`e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd`.

Candidate tree: `4acc1ff65a3b5dddc5b0dc885a0a5449b9b9c287`.

The exact-replay ordering and the normal valid-WAV path are correct, but the
candidate violates the settled missing-only rule at an explicit-null boundary
and does not fail closed for a malformed zero-rate WAV.

## Findings

1. **Blocking — explicit output `duration_seconds: null` is not preserved.**
   The new guard in `runtime_protocol/store.py:4869-4884` can only preserve the
   field if it reaches `_apply_settlement_effect`. The existing settlement
   normalizer in `runtime_protocol/service.py:7643-7644` emits
   `duration_seconds` only when its value is non-null, so an explicit output
   null is erased before the new code runs. On the candidate tree, a valid WAV
   with output `duration_seconds: null` produced variant metadata
   `duration_seconds == 1.0` from the header. This changes the old refusal into
   an accepted media selection and violates “fill only if the key is absent;
   preserve explicit null”. The fix must retain presence separately from value
   through settlement, or otherwise make the enrichment see that the key was
   explicitly supplied.

2. **Blocking — zero-rate WAV raises instead of remaining unknown.**
   `runtime_protocol/cas.py:140-151` catches parser errors but not
   `ZeroDivisionError` at `frames / rate` (`rate == 0`). A structurally readable
   but malformed WAV with a zero sample rate therefore aborts settlement rather
   than returning no duration. The bounded design says malformed/unsupported
   WAVs remain duration-unknown and selection keeps the existing refusal.

## Verified positives and scope

- `settle_attempt` checks `_command_replay` before lease validation, staging,
  CAS access, or settlement enrichment. An exact replay returned the stored
  result while `ContentAddressedStore.open` was patched to fail, proving no
  second CAS read. A changed body under the same key also conflicted before CAS
  access.
- A normal 8 kHz mono WAV settled through the real Runtime service path and
  yielded the expected `1.0` second duration, exact five-field selection, and
  unchanged canonical timeline row counts.
- The patch changes only `runtime_protocol/cas.py`, `runtime_protocol/store.py`,
  and `tests/test_generation_publish_v1_settlement.py`. No new effect, schema,
  DTO/API, table, ffprobe/framework, raw-adoption path, receipt rewrite,
  catalog-digest rewrite, or timeline write was introduced. Variant append is
  untouched; no regeneration claim is made for that path.
- This is Runtime `generation.publish_v1` proof only. The current Real Speech
  SDK has no settled speech intent/effect in scope, so this is not voiceover or
  Agent API proof.

## Evidence and limits

Candidate test file, run from an archived copy of the exact candidate tree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$tmp" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  "$tmp/tests/test_generation_publish_v1_settlement.py"
12 passed in 1.85s
```

Independent boundary probe, also against the exact candidate tree, reported:

```text
missing-null: variant duration = 1.0
exact-replay-with-CAS-open-forbidden: succeeded
zero-rate-malformed-WAV: ZeroDivisionError
```

The supplied prior evidence of `33 + 28 + 61` neighbouring tests was not
repeated here. No full suite was requested or run. The candidate's added tests
cover valid, invalid-byte, and explicit-value cases, but not explicit output
null presence or zero-rate WAV handling.

## Required follow-up

Carry explicit-null presence through settlement and treat zero/invalid WAV
rates as unknown, then add regression tests for both boundaries before asking
for re-review.
