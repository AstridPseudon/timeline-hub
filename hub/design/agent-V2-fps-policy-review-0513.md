# V2 FPS independent review — `9ea78773` / `e44bdfe`

Date: 2026-10-23 UTC  
Worker: `agt-V2-fps-policy-review-0513`  
Reviewed commit: `9ea78773b99bcc59885ca0545b5f9920e45de87e`  
Reviewed tree: `e44bdfeac0347b82f305bd0e857d05386a92bf3c`  
Parent: `9cf0fde2f57603813d81733ee8b0f7117ffd634c`

## Ruling

**Overall: FAIL / do not merge.**

| Review axis | Result | Finding |
| --- | --- | --- |
| Source security | PASS | Existing finite/positive/type checks remain; malformed, adjacent, nonfinite and distinct-rate controls remain refused. The candidate is not mutated. The production caller invokes this validator before acceptance. |
| Canonical authority | FAIL | `validation.py:109-119` introduces a new whitelist accepting the decimal round trip of `float(Fraction(exact_rate))`. Existing `_fps`/`_time_fraction` and `capture.rate` normalize `29.97002997002997` to `2997002997002997/100000000000000`, distinct from `30000/1001`. No existing canonical normalizer establishes their equality. |
| Contract scope | FAIL | D12 permits untouched pre-existing legacy declarations to survive unrelated edits; it does not approve accepting newly created, modified or invalidating mixed declarations. The authored change broadens final-candidate validity and therefore requires an explicit approved policy. |

This is not an epsilon, new parser, or loose coercion bug: it is a precise but
**new policy**. The comment's reference to existing numeric serialization does
not make that serialization an approved cross-location canonical authority.
The separate Sol D12 repair that preserves the existing normalizers and applies
no-new-invalidity only to untouched legacy declarations is the scoped path; do
not duplicate this whitelist there.

## Production-path and contract review

The production path is wired: `astrid/sdk/timeline/commit.py:1117-1124`
calls `validate_final_candidate(plan.bundle, ...)` immediately before
`document_from_bundle` and `port.accept`/preview. The authored delta changes
only `validation.py` and focused validation tests; it does not alter the v2
request fields, stable idempotency, or `{data, receipt}` reply fields. Those
wire-shape guarantees remain outside this commit, but the changed acceptance
policy is contract-visible.

The 154 focused controls pass, including exact rational timing and negative
controls, but they prove only the authored whitelist and existing guard
behavior. They do not prove the original word-anchor rebase body. The prior
Agent 0453 trace shows the real fixture refusing at the initial `track.create`
with `candidate: all authored fps values must be the same rational rate`,
before the stale-anchor replay. Therefore there is no actual neighbor PASS to
claim.

## Evidence

Pure existing-normalizer witness:

```text
numeric repr:                 29.97002997002997
validation/capture numeric:   2997002997002997/100000000000000
validation/capture rational:  30000/1001
existing-normalizer equality: False
```

The authored implementation instead computes `numeric_rate` from the exact
authority and accepts every value in `(authority, numeric_rate)`. This retains
precision in the exact canvas timing compiler, but it still declares two exact
fractions equivalent for V2 parity. That equivalence is not settled by
`commit-v2.md`, Agent 0453, or Viewing 0502; Viewing 0502 explicitly retracts
that recommendation unless an existing policy already proves it.

## Exact checks

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_commit_v2_validation.py \
  tests/editing_conformance/test_commit_timing_validation.py \
  tests/sdk/test_timing_compiler.py
→ 154 passed in 2.99s

/home/user/work/venv-agent/bin/python -m ruff check \
  astrid/sdk/timeline/validation.py \
  tests/editing_conformance/test_commit_v2_validation.py
→ All checks passed

/tmp/astrid-u2-typecheck/bin/python -m mypy astrid/sdk/timeline/validation.py
→ Success: no issues found in 1 source file

/tmp/astrid-u2-typecheck/bin/python -m scripts.reshape.compare_mypy_baseline
→ Mypy findings: current=1914 baseline=1914
```

The requested normal copies were attempted but cannot run in this worker's
default interpreter: `make ruff` and `make mypy` both fail because
`/usr/bin/python3` has no installed `ruff`/`mypy` module. No full suite,
browser/socket suite, 54-body, native14, or known failing word-anchor body was
rerun.

No product or test source files were changed. No wire PASS or accepted,
merged/rebased word-anchor result is claimed.
