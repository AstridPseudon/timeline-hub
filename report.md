# V2 / P1 timing review

## Verdict

**FAIL.** Retain the original aggregate attribution: **249 passed, 5 failed**;
the direct rerun of `tests/sdk/test_p1_doc_patch_provider.py` on this tree was
**17 passed, 5 failed**. The five failures are source defects at the V2 final
candidate validation seam, not a renderer-off or Runtime-checkout setup issue.

## Reproduction

The required Runtime checkout exists at
`/home/user/work/wt/rt-pin-27f0306b`. The original provider file was run with
the actual checkout/import environment:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-27f0306b \
PYTHONPATH=.:/home/user/work/wt/rt-pin-27f0306b \
/home/user/work/venv-agent/bin/python -m pytest -q \
tests/sdk/test_p1_doc_patch_provider.py
→ 5 failed, 17 passed in 16.11s
```

The scoped V2, contract, metadata, preview/error and doc.patch checks pass:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-27f0306b \
PYTHONPATH=.:/home/user/work/wt/rt-pin-27f0306b \
/home/user/work/venv-agent/bin/python -m pytest -q \
tests/editing_conformance/test_commit_timing_validation.py \
tests/editing_conformance/test_commit_v2_validation.py \
tests/sdk/test_timeline_commit_v2_errors.py \
tests/editing_conformance/test_doc_patch_v2.py \
tests/timeline/test_meta_validator.py
→ 136 passed in 42.18s
```

Quality ratchets are unchanged: `PY=/home/user/work/venv-agent/bin/python
make ruff` reports `current=2151 baseline=2151`; `PY=/tmp/astrid-u2-typecheck/bin/python
make mypy` reports `current=1915 baseline=1915`. The default `make ruff`
wrapper was not usable because `/usr/bin/python3` has no Ruff; the scoped
command above is the qualifying result.

## Exact attribution

| Original failure | Evidence | Attribution | Smallest correction |
| --- | --- | --- | --- |
| `created-track-and-clip-list-inserts` | `FinalCandidateError: candidate.parent.clips['first-clip'].from: must be a finite number` at `astrid/sdk/timeline/validation.py:137` | V2 validator defect. The authored row intentionally contains `from: null`; the source fixture and `tests/editing_conformance/test_recipe_m2_clip_add.py:45-49` require that null and the expected output retains it. The timing kernel already treats a null optional source start as its zero default in `_timing_evaluators.py:54`. | In `_clip_duration` (and the asset-bound check at `validation.py:195`), treat nullable/absent `from` as the default zero source start for interval arithmetic; never rewrite the authored null. |
| `params-absent-to-explicit-values` | `FinalCandidateError: candidate.timing: ambiguous cut identity across occurrences` at `validation.py:440-443`, from `_timing_evaluators.py:282-290` | V2 timing-adapter defect, not a valid parameter refusal. The request changes only `internal-revision:ir` params. The fixture has occurrences `o` and `sibling` pointing to the same physical internal revision `ir`, and expects the shared edit, opaque value and accepted result to be preserved. | In `_commit_timing_validation.py:25-36`, retain the shared source-image identity in the detached timing view (derive cut ownership from the pinned internal revision, or an equivalent exact source binding) before calling the kernel. Keep the kernel’s ambiguity refusal for genuinely distinct physical revisions. |
| `params-null-to-object` | Same `ambiguous cut identity across occurrences` stack | Same shared-physical-child adapter defect. The only intended change is `params: null` to the explicit object; the contract requires absent/null distinction and preservation. | Same single timing-adapter correction. |
| `params-remove-and-preserve-opaque` | Same `ambiguous cut identity across occurrences` stack | Same shared-physical-child adapter defect. The intended film removes `params.old`, adds explicit values, and preserves `params.opaque`; it does not alter timing or cut ownership. | Same single timing-adapter correction. |
| `disjoint-field-merge` | The first competing accepted write reaches final validation and fails with the same `ambiguous cut identity across occurrences` before the disjoint `x/y` merge can be accepted | Same shared-physical-child adapter defect. This is the required merged-head proof, not a legitimate conflict: only sibling `y` is changed at the head while the request writes `x`. | Same single timing-adapter correction; do not weaken merge/conflict checks. |

The production path is present and exercised: `RuntimeCommitService.commit`
calls `validate_final_candidate` at `astrid/sdk/timeline/commit.py:1087-1095`
after command execution/rebase and before `document_from_bundle`/acceptance.
The V2 tests prove that caller and timing/structure/parameter validation are
wired; the P1 failures prove the current adapter rejects valid preserved
closure films before receipt creation.

## Contract/ancestry conclusion

The review was made against `1a0ea1a40` (`tl/agt-V2-R3-meta-forward-0110`),
with the pre-V2 seam at `ae68a1bea` used for comparison. The R3→meta→V2
current join is present, including current-head validation and the production
caller. The failure is not fixed by accepting ambiguous aliases wholesale:
the correction must distinguish the exact shared `internal-revision:ir` image
from two different revisions that happen to contain equal JSON. Likewise,
`from: null` must remain null in the authored candidate; only validation’s
numeric view may default it for arithmetic.

No product or test files were edited. No full/browser/live-socket suite was
run.
