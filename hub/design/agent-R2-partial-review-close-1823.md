# Agent R2 partial review closure — 2026-10-23

## Verdict

Source-only result: **FAIL for trusted-history authentication**. The retained
probe found that an accepted nested inverse record can be self-modified into an
ABA mirror chain which `inverse_stages()` and `validate_nested_history()` accept.
This is a real source-level authority gap: `_nested_mirrors()` stops at the
first byte-equal endpoint (`astrid/sdk/timeline/_step_undo.py:163-176`), so an
endpoint can be selected by equality rather than by a uniquely authenticated
stage boundary.

Public caller-reachable forged request: **not established by this evidence**.
The mutation is applied after acceptance to a deep copy of `realm.entries`,
then the validator is called directly. The public Python caller emits only
`timeline.inverse` with publication IDs and optional step IDs
(`astrid/sdk/timeline/sync.py:411-434`). The provider reloads target history
from `port.history_entry`, checks bounded ancestry and records, and constructs
`AcceptedRecords` (`astrid/sdk/timeline/commit.py:997-1045`); caller-supplied
inverse writes do not enter that path. Therefore this is not evidence that a
normal caller can submit forged `derived_writes`. It is evidence that the seam
does not authenticate its input if the trusted Runtime history/store is
already corrupted or mutable. Do not dismiss that condition, and do not label
it public acceptance.

The partial candidate at `8875589f6` is **not mergeable** and receives **no
whole-R2 credit**. Existing unique Sol task `agt-R2-native-partition-sol-1818`
owns the cumulative `_step_undo` repair; this closure adds no competing
implementation.

## Recovered probe and exact result

The recovered probe is preserved at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-partial-review-close-1823/evidence/adversarial_review.py`

It creates a provider-produced two-stage move plus inverse using the test
`DetachedRealm`, deep-copies accepted entries, mutates only the inverse
record's `derived_writes`, and directly calls the two source functions. The
recovered output is in `evidence/retained-probe.log` and the stopped worker's
original log at lines 6056-6068:

```text
baseline: ACCEPTED stages=[4, 4]
missing-mirror: REFUSED history_unavailable: nested inverse mirrors omit accepted effects
duplicate-mirror: REFUSED history_unavailable: nested inverse mirror chain differs from effects
contiguity-gap: REFUSED history_unavailable: nested inverse mirror chain differs from effects
foreign-site: REFUSED history_unavailable: nested inverse derived attribution differs from history
foreign-cause: REFUSED history_unavailable: nested inverse derived attribution differs from history
foreign-source: REFUSED history_unavailable: nested inverse source differs from history
endpoint-value-digest: REFUSED history_unavailable: nested inverse mirror chain differs from effects
aba-endpoint: ACCEPTED (unexpected)
aba-endpoint: source_unchanged=False
```

The direct reproduction is recorded at the original log lines 6127-6139:
`writes[1].after` is replaced with `writes[4].after`, `writes[2].before` is
linked to that value, `inverse_stages()` reports `[6, 2]`, and
`validate_nested_history()` accepts. The mutation preserves immediate
before/after links but changes the first stage's reachable endpoint.

Relevant implementation citations:

- `astrid/sdk/timeline/_step_undo.py:131-177`: checks parent/config.clips,
  cause, effect inputs, sequential before links, and complete partition; it
  breaks on the first `equal(state, target)` at lines 164-171.
- `astrid/sdk/timeline/_step_undo.py:235-269`: validates nested publication,
  step, ordinal, range, and native-write totals against loaded source history,
  but does not reject the self-consistent ABA mutation in the derived chain.
- `astrid/sdk/timeline/_commit_patch.py:959-965`: production inverse address
  resolution invokes `validate_nested_history()` on loaded entries.
- `tests/sdk/test_timeline_commit_provider.py:68-105`: the retained
  `DetachedRealm` harness used by the probe; its entries are test-side
  in-memory state, not a Runtime wire request body.

## Prior evidence actually present

No test body was rerun for this closure. The stopped worker's log and evidence
were recovered, and the exact commands/results are recorded in
`evidence/provenance.md`.

- Focused review lane: `python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_nested_parent_mirror_ranges.py` — **34 passed** (prior log lines 1347-1350).
- Retained neighboring lane: **1 failed, 82 passed, 3 deselected**; the failure was the pre-existing transient-root case in `_root_inverse.py:190` (prior log lines 1296 and 1363-1366), not treated as green.
- Adversarial matrix command: `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=/home/user/work/wt/agt-R2-nested-partial-review-1801:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-nested-partial-review-1801/evidence/adversarial_review.py` — **seven refusals; ABA-endpoint unexpectedly accepted** (prior log lines 6056-6068).
- Scoped mypy — **no issues in 2 source files**.
- Scoped ruff — **all checks passed**.
- Ruff baseline — `current=2149 baseline=2149`.
- Mypy baseline — `current=1912 baseline=1912`.
- Vendor lock — `ok runtime.lock.json`.
- Artifact manifest — `artifacts.json is current`.
- `git diff --check` — succeeded.
- Credential scan over touched source/tests — no matches/output.

Protected-file hashes and unchanged comparisons from the stopped worker are
retained in its log lines 6095-6113. The current closure worktree remained
clean at `8875589f6`; no product, test, schema, client, pin, Runtime, env, or
Git changes were made.

## Limits and required next step

This review does not establish the full request/reply contract, Runtime
storage immutability, a public forged-history route, whole-R2 behavior, or the
original excluded undo suites. It also does not credit the prior focused
green lane as whole-R2 evidence. Missing evidence includes public Runtime
proof, the full R2 cumulative suite, P1-P4, and the excluded original
provider/public redo cases.

Sol1818 should repair the cumulative `_step_undo` seam so a nested mirror
partition requires a unique authenticated endpoint/range rather than the
first equal value, then add a regression through the actual accepted-history
provider path. A fresh independent review and cumulative R2 gate are required
before any merge decision.
