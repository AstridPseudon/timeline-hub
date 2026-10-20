# Runtime F3 claim identity final review — APPROVE

Reviewer `rt-m3-alias-identity-final-review`, 2026-10-20. The assigned independent review is complete and unblocked. No repository source or tests were edited, and no merge is requested.

**APPROVE the bounded F3 successor `e6abb5bd181a80eb553f99bff82b158b41589955`, tree `2c90024da09f310eeae2eb7333e62a0acd48f3cc`.** The original six F3-R1 preservation probes now pass unchanged, alongside the outer-context forgery controls. This closes F3-R1 from `design/runtime-alias-final-review.md`; no new blocking finding was found within this unit. Compose it with independently approved basis `082a90506cb0d2a64dfc939f7a87ae377c6664ce` and the Agent-owned approved source `92427b3af0bfaba2ff604791cf3e5165125b6d54`, or separately qualified descendants. This approval does not certify the old candidate-authority implementation still present on the isolated alias branch.

## Reviewed source and behavior

Read PLAN, COMMON, current Runtime STATUS (10:35:07Z), original capture authority and alias rejections, approved candidate-basis review, source-worker report, complete changed code/tests, and adjacent admission, snapshot and host consumers. The corrected branch was resolved after its harness completed (`DONE` and actual commit inspected), and still resolves to the same SHA at final verification. The review checkout stayed clean at `8609333456b9537339ee1a5dfc7ffd9609242de8`; all execution used private exact-source archives rather than that unrelated checkout.

`e6abb5bd` changes only `runtime_protocol/capture_validation.py` and adds `tests/test_capture_claim_identity.py` relative to rejected `aa784ab8`. Actual diff: product 11 insertions/5 deletions; new tests 172 lines. Capture-validation SHA256 is `d0cc21c10968433fd96d18dc3f46f3200f41b09b041f3f40a159195e3d1f855e`. All other top-level functions, including `_candidate_document` and `validate_capture`, are AST-identical to `aa784ab8`.

The failed-claim map and recursive replacement now use `(alias_ref_key, canonical_json(full_reference))`. Revision ID/digest, working-copy candidate/publication/base bindings, scope, source kind and other reference fields participate. Object digest alone no longer makes independently verified claims collide. Reordered dictionary keys remain the same claim through canonical JSON. The existing two-context inspection, per-alias validation, exception-to-UNCERTIFIED behavior and recursive dictionary/list/JSON-copy traversal remain.

The committed six-case regression module positively checks a capable provider and successful validation before exercising failure. Three saved cases use the existing pre-validator store seam, then public `claim_next`; three working-copy cases use the actual Agent SDK candidate/projector and pure claim view. Every alias has a failed outer and successful nested reference sharing CAS bytes. The tests keep valid references and their filmstrip JSON intact, downgrade the rejected claim's copies, retain caller data, and check saved stored-spec/history/CAS/staging and exact retry. No passing expectation was removed, weakened, skipped or xfailed.

Independent probes additionally check revision, digest, project, timeline and kind differences in both context orders; every working-copy binding field; reordered failed-reference keys; JSON/list copies of both claims; idempotent relabeling; and plain inputs. The legitimate saved/candidate claim is accepted by the capable provider before the bad claim is tested. Explicit CAS remains UNCERTIFIED unchanged. Provider absence is never the explanation for a successful certification control.

The original 36-node corpus preserves all three aliases, inferred/explicit revision kinds, supported outer/nested contexts, inline/ref normalization, multicarrier distinct-digest results, semantic saved forgery refusals, saved/native controls and actual candidate positives. Six original preservation cases plus the original baseline differential assertions are unchanged byte-for-byte. Public legacy-claim probes keep immutable task-spec rows, canonical/history/closure rows, CAS/staging bytes and original-spec exact retry intact. Claim attempts/events/leases may change normally; this is not a claim that a public claim performs no SQL writes.

Consumer precedence is unchanged: snapshot rewriting and the Agent host prefer a nested dictionary, otherwise outer; store validation falls back when nested is empty. Both contexts are inspected by the claim function, so a non-preferred outer claim is still downgraded. Exact duplicate filmstrip references remain checked against the selected host context. This change does not add authority to a claim or alter admission/host validation.

## Independent commands and results

Definitions for all commands below:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W=$ORCH/workers/rt-m3-alias-identity-final-review
cd "$W"
```

Sources were reconstructed with read-only git archives using the retained script:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python prepare_sources.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python verify_sources.py
```

Both passed. The final verification additionally checks every exported Runtime/Agent file against its git blob, original probe byte equality, unchanged non-claim functions, and all three central snapshots/exits. Frozen original Agent is `df2739f903edac02bd36b4446deeea847524c040`; approved paired Agent is `92427b3af0bfaba2ff604791cf3e5165125b6d54`, tree `525bdabe863a42bc177f5ff331560133f77ce634`.

Exact corrected original-corpus run with the original frozen Agent, including all six formerly failing assertions:

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD/runtime-copy:$PWD/runtime-copy/tests:$PWD/agent-copy" \
  ASTRID_CHECKOUT="$PWD/agent-copy" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --confcutdir=. --basetemp=private-original-corrected \
  test_original_alias_probes.py test_final_alias_review.py
```

**36 passed, 3 warnings in 5.75s**, exit 0 (`original-probes-corrected.log`). Original rejection was 6 failed/30 passed against `aa784ab8`.

Fresh independent identity controls on exact corrected Runtime, original frozen Agent:

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD/runtime-copy:$PWD/runtime-copy/tests:$PWD/agent-copy" \
  ASTRID_CHECKOUT="$PWD/agent-copy" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --confcutdir=. --basetemp=private-edges test_identity_edges.py
```

**43 passed, 3 warnings in 14.09s**, exit 0 (`identity-edges.log`). These comprise 30 saved identity/context-order cases, 12 candidate-binding cases and one plain-input control.

After private preparation renamed the original Agent export and placed the approved `92427b3a` export at `agent-copy`, the committed six cases and existing alias regressions ran directly:

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD/runtime-copy:$PWD/runtime-copy/tests:$PWD/agent-copy" \
  ASTRID_CHECKOUT="$PWD/agent-copy" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  -m integration --confcutdir=. --basetemp=private-paired-corrected \
  runtime-copy/tests/test_capture_claim_identity.py \
  runtime-copy/tests/test_capture_candidate_actual.py::test_all_capture_aliases_label_each_uncertified_carrier_without_rewriting \
  runtime-copy/tests/test_capture_candidate_actual.py::test_outer_legacy_aliases_are_labelled_without_rewriting_admission \
  runtime-copy/tests/test_capture_candidate_actual.py::test_claim_checks_nested_and_outer_aliases_with_mixed_results
```

**25 passed in 22.20s**, exit 0 (`paired-probes-corrected.log`). All 25 executed; no deselections or absent-provider positives.

## Composition with basis082

The retained `prepare_composition.py` reconstructs exact basis082 in a private directory and applies the complete `git diff 6023cfb e6abb5bd` for the three F3 files using ordinary `patch`, without any git mutation. Patch application succeeds with only a line-offset adjustment. The composed file retains the basis `_candidate_document`, `validate_capture` and all other non-claim functions unchanged; it uses the corrected F3 claim function and required `SNAPSHOT_KEYS` import. Composed capture-validation SHA256: `572d4c8ec61e2705ce56aa3d5733b500c64ba06b9e5addca885bd457388f6b75`.

Private composed execution uses the approved real Agent provider/verified-source host, without a prototype method or substitute verifier:

```bash
env PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$PWD/runtime-composed:$PWD/runtime-composed/tests:$PWD/agent-copy" \
  ASTRID_CHECKOUT="$PWD/agent-copy" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --confcutdir=. --basetemp=private-composed \
  test_original_alias_probes.py test_final_alias_review.py test_composition.py
```

**81 passed, 5 warnings in 38.63s**, exit 0 (`composed-probes.log`). This is the original 36-node corpus, 25 committed alias/identity cases, eight actual saved/native/parent-child working-copy inline/ref host positives, and 12 saved/working-copy semantic forgery refusals before writes. The first module's ten original controls deliberately load the exact F3 module; the remaining controls use the composed production module. The composed claim function is identical to that F3 function. This is private function-composition evidence, not a future integrated-tree central gate.

Warnings in private-root runs are imported modules' unregistered `integration` markers. They do not suppress execution.

Static checks:

```bash
/home/user/work/venv-agent/bin/ruff check --no-cache \
  runtime-e6/runtime_protocol/capture_validation.py \
  runtime-e6/tests/test_capture_claim_identity.py
git -C /home/user/work/wt/rt-m3-alias-identity-final-review diff --check 6023cfb e6abb5bd
git -C /home/user/work/wt/rt-m3-alias-identity-final-review status --porcelain
git -C /home/user/work/wt/rt-m3-alias-identity-final-review rev-parse tl/rt-m3-alias-claim-identity-fix
```

Passed; worktree clean; corrected SHA unchanged. Final `verify_sources.py` also passed after composition (`source-verification-final.log`).

Harness diagnostics are retained honestly: the first original run was 27 passed/9 setup errors because a symlinked Agent export did not satisfy the fixture's resolved-path assertion. Replacing that private symlink with the actual exported directory fixed the harness without touching probe assertions or product code. The first paired invocation omitted `-m integration` and yielded 25 deselections/exit 5; the corrected invocation above ran all 25. Initial composition bookkeeping omitted F3's required import in the expected text; the fully applied patch was correct, and the expectation was fixed before composed execution. These diagnostics are not product failures or positive evidence.

## Reused central results: exact corrected tree

No central requests were submitted by this reviewer. Inspected each `request`, `snap`, `status`, `exit`, `summary`, `log.txt` and `ext`. All three completed with exit 0 on **tree `2c90024da09f310eeae2eb7333e62a0acd48f3cc`**, equal to the final corrected commit, not the rejected predecessor:

| Request ID | Result |
| --- | --- |
| `rt-m3-alias-claim-identity-fix-targeted-1020104538-14860` | 41 passed, 6 deselected, 6.74s |
| `rt-m3-alias-claim-identity-fix-capture-agent92427b3a-integration-1020104538-32661` | 6 passed, 4.31s |
| `rt-m3-alias-claim-identity-fix-commit-integration-1020104538-24706` | 9 passed, 11.37s |

Exact commands from central summaries, run from their Runtime snapshots:

```bash
/home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_snapshot_authority_refusal.py tests/test_snapshot_preflight.py \
  tests/test_capture_claim_identity.py

A=$ORCH/workers/rt-m3-candidate-source-basis-fix/agent-source
env ASTRID_CHECKOUT="$A" PYTHONPATH="$PWD:$A" PYTHONDONTWRITEBYTECODE=1 \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  -m integration tests/test_capture_claim_identity.py

env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent \
  /home/user/work/venv-agent/bin/python -m pytest -q -m integration \
  tests/test_timeline_commit_integration.py
```

The ordinary lane's six marked cases are deselections, not passes; their evidence is the explicit frozen-Agent lane. Its fixed archive was compared blob-for-blob with the approved exported Agent source. Generic central external records list moving integration Agent `43d567f9d972386dc4cf585fbacc3ad9afc56bdd`; the alias command explicitly uses the pinned archive instead. Commit integration uses the moving checkout, recorded at that SHA before and after its run. Those nine tests qualify the exact Runtime tree against that recorded checkout, not a frozen `92427b3a` commit pair or a complete cross-product release.

## Limits, decision and next step

No full/broad central repeat, new central request, socket, browser, renderer, dependency install, shared dependency/cache mutation, repository edit, git write/checkout/commit/merge, integration edit or other-worker edit occurred. Private source exports, realm/temp trees and patch backups are cleaned after verification; reconstruction/probe scripts and logs remain in this worker's artifact directory. Shared provider archive remains untouched.

The original **four RenderRequest `verified_source` propagation positives remain open external requirements**, as reported by the source worker. They were neither reclassified as refusals nor xfailed; this review does not claim to have repaired or rerun them. The original SDK invocation guards, renderer/Composition/pixel/audio parity, future integrated-tree central gates, ordinary full suites and Gates 1/7 remain outside this bounded approval. Private verified-host positives stop at host materialization and do not establish RenderRequest or actual export behavior.

**Decision: APPROVE F3 claim identity, with no new design decision or blocker.** The orchestrator may compose the approved F3 region with basis082 and the approved Agent source, preserve `_candidate_document` exactly, and qualify the actual resulting integration tree through the existing queue. Keep the Agent verifier until its separately owned removal requirements are fulfilled. No merge or verifier deletion is authorized by this report itself.
