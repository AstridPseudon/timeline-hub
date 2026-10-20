# Runtime sealed-capture version review

2026-10-20 · worker `rt-m2-sealed-capture-version-review` · LIGHT review complete.

**Proposal ACK: YES, for the FINAL 13-operation refinement. Final committed Agent version-boundary source: APPROVE within this review's scope. Native pair/adoption/publication: HELD.** These are separate decisions. No approval of moving WIP, no freeze of parent `9cab2ad3`, and no claim that detached provider tests prove Runtime acceptance.

## Exact reviewed sources

- Plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`, including the owner ruling on obsolete captures; FINAL design: the adjacent `agent-materialization-version-boundary.md` and its final coordination refinements.
- Agent **commit `3730d0bd51686a1692450359482205df64dcc839`**, tree `3892a10bcffa9bf520b4c79591637cf3259d6724`, parent `9cab2ad36ff6c99c05b42d16d54dfa82e7e86d5e`. Inspected with `git show/diff`; probes/tests use an archive of that commit in this worker's shared scratch directory, not another worker's editable source. Candidate schema SHA-256 `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`.
- Public S2/013 floor SHA-256 **`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`**. Complete floor containment passes the existing Runtime conservative checker. All 48 definitions and 22 operation clauses remain. Exactly 12 changed clauses retain the complete old v1 branch and add a copy changing only version to `2`; existing unversioned `track.create` args remain unchanged. No fixture bytes changed.
- Exact counterexamples: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-materialization-current-recovery/legacy-capture-counterexamples.json`, SHA-256 **`f8a0227cd8dc90c9a042594b5db31f5fc9858a8417708d29771b9d65e2d4ef8e`**.
- Runtime assigned baseline `129493b2aff614560d9b7ac2577957e799cf30ec`, tree `330ea3969cb9cce77271404f31793c21abd5993f`: read request syntax/ledger ordering and normal generators. Recovered carrier counterpart statically reviewed at **`3c917378a6dc2b48362fd1bc152cb13a5fd6b84a` / tree `853c122f2713fd6970164ff6c471550700257e8f`**, without checkout. Secondary-ID successor `ade60f3225aa3b6b6db1aee683bc33e09084a4fa` / tree `06a68e47968f1c64774e05608e004d8edbf7ca65` has the same request-private join; its separate occupancy fix is outside this version review's approval.

## Findings and proposal agreement

1. **Version selects recording format, never authority.** Agent `commands.py:87,155,175,216,220` validates the supported versions, uses the same handlers, checks sealed-v2 completeness and exact submitted capture, and branches only on version (plus authenticated inverse handling). There is no binding-presence authority submode. `_materialization.py:8,16,157` limits v2 to the agreed 13 ops, chooses native v2 while authoring a verified virtual occurrence slot, and verifies the original source closure. Parent-only clip add/delete/trim/split and inverse/restore stay semantic v1. No new DTO, field, `capture_version`, args, seed, endpoint or provider.
2. **Complete public v1 remains a positive.** The exact counterexample placement retains all 103 reads, 3 selections, submitted command, records, authored output and empty `id_map` under the default full-closure ingress. Its version-only upgrade to v2 refuses with `capture_mismatch`; fresh native v2 authoring succeeds with source-bound mapping. Downgrading the current sealed v2 placement to v1 also refuses. Neither flip manufactures proof or silently replaces submitted claims.
3. **25/3 is materially different from 27/4.** The obsolete private add lacks reads of `occurrence:occ-a/source` at `app.astrid.pool` and `parent` at `config.pinnedShotGroups`, both recorded absent in the current example. It also lacks `placement.owners` membership/order/boundary proof for `occurrence:occ-a` and its destination shot. These facts, not counts or version labels, explain the distinction. The original 25/3 capture refuses at both versions, unchanged, with an explicit re-author pointer; the equivalent freshly authored 27/4 v2 succeeds. Exact missing facts are saved in the worker's `missing-add-proof.json`.
4. **Accepted history remains separate from NEW admission.** In recovered Runtime, `timeline_commit_store.py:848,855` looks up accepted identity before head/destination/semantic validation; the execution coordinator also looks up before constructing the port/provider path. `_verify_accepted:120` and `_check_inherited_allocations:182` authenticate retained facts; they are not a new-command version dispatcher. Agent inverse retains accepted allocation facts. The 3 accepted-private-v1 JSON-reload/inverse/redo/restore cases and durable outbox refusal/restart case pass in the detached lane. Real SQL accepted-private-v1 lifecycle on this exact Agent/Runtime pair remains unverified here.

## Minimal Runtime counterpart

**No additional version-specific Runtime product change is needed beyond the already proposed carrier counterpart and normal schema packaging.** In recovered Runtime `RequestCommitPort._materializations:437`, allocation joins require the exact private captured parent closure and sealed request bindings; changing a version cannot bypass that join. Keep that boundary and authenticated history handling unchanged. The Agent report already statically reviewed this exact `3c917378` counterpart; that bounded review does not cover an arbitrary successor.

There is one essential deployment constraint: `service.commit_timeline` calls `validate_request` **before** ledger lookup. Current public S2 syntax rejects private item references and new v2 commands. The future matched PRIVATE resource bundle must therefore contain the full agreed schema union, including syntactic acceptance of old private v1 carrier requests. Otherwise exact retries would never reach the ledger. Old syntax passing does not authorize NEW semantic acceptance; the Agent still refuses obsolete v1 claims.

A private scratch probe fed the committed Agent schema through the existing `timeline_commit_resources.render(root)` and validated exact public v1, obsolete/private v1, complete/private v1 and new native v2 request syntax, without changing any input. This confirms the ordinary generator can carry the union. Existing `timeline_commit_types.render()` produces **identical Python and TypeScript DTO source** with this schema; its string version field already supports the additive versions. Both generated Python outputs compile/import. No generator edit or handwritten DTO union is needed. No TypeScript compiler or published client qualification was run in this review.

Any additional Runtime counterpart change or composed successor must return to Agent review. Keep public schema/floor/artifacts/pins/activation unchanged until both final source reviews and the normal private pair pass.

## One-to-one retirement ledger

Existing `design/deletion-ledger.agent.md` rows AG-MAT-V01–V03 are present and HELD until merged. Exact IDs reviewed:

| Row | Obsolete-version refusal | Equivalent current-version positive |
| --- | --- | --- |
| AG-MAT-V01 | `tests/editing_conformance/test_recipe_m2_placement.py::test_private_carrier_placement_v1_refuses_without_refreshing_original_claims` | `tests/editing_conformance/test_recipe_m2_placement.py::test_parent_and_occurrence_golden_capture_replay_reload_inverse_redo[fixture_path1]` |
| AG-MAT-V02 | `tests/editing_conformance/test_recipe_occurrence_media.py::test_private_carrier_swap_v1_refuses_without_refreshing_original_claims` | `tests/editing_conformance/test_recipe_occurrence_media.py::test_portable_goldens[swap-fixture_path2]` |
| AG-MAT-V03 | `tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_v1_refuses_original_claims_with_draft_kept` | `tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_equivalent_reauthored_v2_succeeds` |

V03 names the retired `test_portable_goldens[add-fixture_path3]`; its equivalent success is now the explicit separate node above. Original golden data remain immutable. Public original behavior is retained by `test_complete_public_s2_v1_keeps_original_capture_records_output_and_map[placement/add/swap]`, not converted into refusal.

## Exact new evidence

All outputs below are under the absolute worker directory defined here. Dependencies and caches remained read-only; no product edits, live sockets, full/broad service suite, public generation or pin change.

```bash
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-sealed-capture-version-review
cd "$W/agent-source"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-m2-sealed-capture-version-review/packages/python /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_materialization_version_boundary.py tests/editing_conformance/test_recipe_m2_placement.py::test_private_carrier_placement_v1_refuses_without_refreshing_original_claims tests/editing_conformance/test_recipe_m2_placement.py::test_parent_and_occurrence_golden_capture_replay_reload_inverse_redo tests/editing_conformance/test_recipe_occurrence_media.py::test_private_carrier_swap_v1_refuses_without_refreshing_original_claims tests/editing_conformance/test_recipe_occurrence_media.py::test_portable_goldens tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_v1_refuses_original_claims_with_draft_kept tests/editing_conformance/test_recipe_occurrence_media.py::test_obsolete_carrier_add_equivalent_reauthored_v2_succeeds
```

**34 passed in 8.31s, exit 0.** `targeted-agent-corrected.log`. Initial same command without the Runtime client path: 29 passed / 5 failed, all `ModuleNotFoundError: astrid_runtime_client`; preserved in `targeted-agent.log`. No test or product change to fix that environment error.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$W/review_probe.py"
```

**PASS, exit 0**, six explicit checks in `review-probe-final.log`: committed identity/floor/branches/fixtures; both version flips; exact public and obsolete proof; pre-ledger schema packaging; unchanged generated DTOs/Python import. Probe setup diagnostics were a missing verified-media argument (correctly refused by the engine), then a Python `tests` package path collision; only the private probe setup changed before this final pass. `review-probe.log` retains the first diagnostic.

`git diff --check` and `git status --short` in the assigned Runtime worktree: exit 0, clean. Source tests reported by Agent (866/1237/96 lanes) were read as existing evidence, not rerun or claimed as this worker's new results.

## Remaining gate

This LIGHT review is complete and has no blocking version-boundary finding. Integration/native adoption remains HELD: obtain the independent Agent final source review, agree the exact Runtime successor, then use the normal matched PRIVATE generation and central pair checks for real ledger-first retry after restart, inverse/redo/restore, stale/sibling/own-slot/global-item occupancy, native dependent-edit/ACK and draft preservation. Do not activate or publish from this report alone.
