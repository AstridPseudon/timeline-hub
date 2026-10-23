# Agent V2 / P1 timing review

**Base:** `tl/agt-V2-R3-meta-forward-0110`, `1a0ea1a40b18084c74f4e40e79b51bef9101acbf`  
**Comparison:** pre-V2 seam `ae68a1bea`  
**Verdict:** **FAIL**

## Qualification result

The original aggregate P1 attribution remains **249 PASS / 5 FAIL**. With the
required Runtime environment, the source provider file reproduces **17 passed,
5 failed**. The Runtime checkout used for every pytest subprocess was the
existing `/home/user/work/wt/rt-pin-27f0306b` (verified present), via
`ASTRID_RUNTIME_CHECKOUT` and `PYTHONPATH`.

The five failures are:

1. `created-track-and-clip-list-inserts`: final validation rejects the
   authored `parent.clips['first-clip'].from: null` as nonnumeric.
2. `params-absent-to-explicit-values`: final timing validation rejects
   `ambiguous cut identity across occurrences`.
3. `params-null-to-object`: same timing rejection.
4. `params-remove-and-preserve-opaque`: same timing rejection.
5. `disjoint-field-merge`: the competing accepted head write reaches the same
   timing rejection before the required merged disjoint-field result.

## Line-level findings

### Parent created clip

`astrid/sdk/timeline/commit.py:1087-1095` calls
`validate_final_candidate` after execution/rebase and before acceptance. The
validator enters `_clip_duration` at `validation.py:124-158`; line 137 always
passes `clip.get("from", 0)` to `_number`. An explicitly present JSON null is
therefore rejected, even though this is an optional source-window field and
the clip has an authored positive `hold`.

The intended film is explicit in the source fixture:
`tests/editing_conformance/test_recipe_m2_clip_add.py:45-49` creates the text
clip with `from: None`, and the canonical P1 output retains that null. The
timing evaluator’s `_value` helper at `_timing_evaluators.py:54-55` already
uses the semantic zero default for a null timing operand. This is a validator
adapter mismatch, not a valid contract refusal.

Smallest correction: use zero only in the validator’s arithmetic view when
`from` is absent or null, including the asset-bound arithmetic at
`validation.py:195`; leave the candidate JSON untouched so null remains
distinct from `remove`/absent.

### Four shared-child failures

Each params/disjoint fixture has two occurrences (`o`, `sibling`) whose pinned
source mapping points to the same physical child revision `internal-revision:ir`.
Both child copies contain clip `c` and the same authored `app.astrid.cut` value
`old-cut`. The requested effects are parameter-only: absent→object,
null→object, remove-one-key while preserving an opaque object, and a disjoint
`x` write rebased over a head-only `y` write.

The current join creates the failure as follows:

- `authoring_bundle.py:462-501` gives each placement an independent authoring
  shot and copies the shared child in memory.
- `authoring_bundle.py:1015-1027` then materializes each changed copy as its
  own authoring internal revision.
- `_commit_timing_validation.py:25-36` compiles that materialized projection.
- `_timing_evaluators.py:282-290` groups clips by cut alias and rejects when
  the group contains more than one `shot_id`.

Thus the timing kernel sees two authoring shot identities and reports
`ambiguous cut identity across occurrences`, although the submitted root is
the one exact shared `internal-revision:ir` image. This is precisely the
closure distinction in commit-v2: equal payloads must not be guessed as one
image, but two occurrences pinned to one verified image are one physical
match. The adapter has lost that source-image identity while constructing its
detached timing view.

Smallest correction: preserve the exact pinned shared internal-revision
identity in the detached timing view, or equivalently normalize cut ownership
from the verified source mapping before invoking the existing kernel. Do not
remove or broadly weaken the kernel’s ambiguity refusal for genuinely distinct
revisions with the same cut alias. Do not turn this into an implicit
occurrence-local fork; the intended film is a shared revision edit and the
P1 test requires both occurrences’ preserved child result.

## Evidence

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-27f0306b \
PYTHONPATH=.:/home/user/work/wt/rt-pin-27f0306b \
/home/user/work/venv-agent/bin/python -m pytest -q \
tests/sdk/test_p1_doc_patch_provider.py
→ 5 failed, 17 passed in 16.11s
```

The dedicated V2/contract/metadata/preview/error/doc.patch set passed:

```text
... pytest -q \
tests/editing_conformance/test_commit_timing_validation.py \
tests/editing_conformance/test_commit_v2_validation.py \
tests/sdk/test_timeline_commit_v2_errors.py \
tests/editing_conformance/test_doc_patch_v2.py \
tests/timeline/test_meta_validator.py
→ 136 passed in 42.18s
```

Ratchets: `PY=/home/user/work/venv-agent/bin/python make ruff` →
`current=2151 baseline=2151`; `PY=/tmp/astrid-u2-typecheck/bin/python make
mypy` → `current=1915 baseline=1915`. No product/test edits, no full suite,
browser, live socket, shared dependency or git write was performed.
