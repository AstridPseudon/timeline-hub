# R2r nested inherited-range authentication — source-qualified candidate

Task `rt-R2r-nested-range-1543`, base `9ce4242bc01f100bab9efc51032a73985cefb2b2`. No commit/merge/checkout/push or integration worktree changes performed. Harness may commit this worktree. Independent review is still required.

## Result and scope

Implemented one strict private authentication change in `runtime_protocol/timeline_commit_auth.py`: `_inverse_stage_inherited` derives reverse partitions from a store-authenticated immediate inverse source; `_inverse_stage_history`, `_inverse_stage_ranges`, and `_inverse_stage_boundaries` bind those partitions to the immediate source identity. Incoming native captures must equal reversed accepted source captures byte-for-byte (before/after exchanged), and canonical set/remove observations must exactly reverse the accepted source effects. Ranges must partition all native/effect observations in order. Removing all stage annotations is refused. Authenticated source canonical edges reconcile inherited native aliases and old native pins; complete payloads and physical owners must still agree at each boundary.

Only those three original private functions change; the added helper remains in their section. No edits to `validate`, atomic scope, store `_verify_accepted`, execution/port plumbing, contracts, public shapes, schemas, generated clients, pins, or Agent. Original tests are AST-identical. One bounded test addition and a 140,275-byte fixture containing an actual immediate accepted history entry plus an auth-only inverse projection are included. No fake history entries or provider acceptance receipts were constructed.

## Source verification and causal result

Read PLAN, the complete staged-redo packet, nested1515 review, export1525 manifest, and peer1525/1530. Packet size/hash verified: 4,790,931 bytes / SHA-256 `3a718d9537faec492723efcd0b49a86675054ae03cfa580361058c58ba780c09`. Embedded 444,166-byte retained1404 source verified against `9a47bb934b879efa0f6147d673038cee76299ba4e30ab22b6d5bcb1377ade589`. Packet versions of all three inverse auth helpers match base HEAD AST exactly. Early source-owner/private-interface/causal handoff was published before implementation qualification.

The same retained-fact auth-only input produces old RED (`inverse stage provenance does not match authenticated history`) and new GREEN through complete `validate`. Immediate source is `txn-75285c95600949c8b1267a71f8e71a9d`, step `undo-0`, command ordinals `[0]`. One outward inverse step carries two internal ranges: native `[0,2]` / effect `[0,4]`, then native `[2,3]` / effect `[4,9]`. This is not a production-provider PreparedCommit capture, compiler run, public redo, or whole R2 acceptance result.

There are 33 new test cases: retained real-range/native ordering, complete retained-boundary validation, twenty retained-input forgery cases, and an actual Runtime-store accepted nested inverse plus ten complete-SQL no-write refusal controls. Existing ownership, native membership, effect digest, read basis, source identity and boundary controls remain green.

## Exact commands and results

Run from `/home/user/work/wt/rt-R2r-nested-range-1543`:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_source_duplicate_authority.py tests/test_timeline_source_document_boundary.py
```

Exit 0: **241 passed in 69.03s**, final tree. `evidence/targeted-verified.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -m integration -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_source_duplicate_authority.py tests/test_timeline_source_document_boundary.py
```

Exit 0: **56 passed, 185 deselected in 49.39s**. `evidence/integration-qualified.log`. This explicitly exercises the marked nodes; the first command also includes them because addopts is cleared. The subsequent only test edit asserted non-null error details in an unmarked new test.

```sh
/root/.local/bin/ruff check --no-cache runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py
/root/.local/bin/pyright --outputjson --project /tmp/w-708b8d3db2/pyright-baseline.json
/root/.local/bin/pyright --outputjson --project /tmp/w-708b8d3db2/pyright-current.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python /tmp/w-708b8d3db2/check_nested_source.py
git diff --check
```

Ruff exit 0: baseline/current 0/0. Scoped Pyright exits 1/1: baseline/current six identical pre-existing OptionalSubscript diagnostics in original tests, **0 added / 0 removed**; production auth module has zero diagnostics. Configs (two explicit files, same import paths and shared dependency venv), JSON output, and exact comparison log are retained in worker evidence. The source-integrity command exits 0: causal old RED/new GREEN, original function/test AST checks, frozen77. Diff check exit 0.

Frozen77 matches this task's base HEAD **77/77**. Compared with the older0922 manifest, only CI workflow and pyproject differ before this task; neither is edited here. Frozen schemas/clients/contract/pin surfaces remain unchanged. Diagnostic exploratory runs are retained but not used as qualification: an early single-stage source-copy regression was fixed by keeping existing one-range behavior; two early forgery mutations were corrected because they were no-ops; a Pyright configuration with absolute include paths was rejected by Pyright and its broad scratch analysis is excluded in favor of the corrected two-file comparison.

## Limits and exact next steps

- **Source qualification only. No public redo PASS.** No public redo, full suite/matrix, browser, journey, native bundle, host/daemon/provision, or duplicate public body was run.
- Strict new support covers one authenticated immediate source inverse command with multiple retained stage ranges and canonical set/remove observations. It refuses unsupported multi-command nested sources rather than flattening them. Existing one-range sources keep their previous authentication path.
- The immediate history entries must come from the existing store `history_entry` / `_verify_accepted` path. Direct dicts passed to the helper are not a replacement for that sealing/ancestry contract. Existing read/ABA/intervening-history and foreign/future/cycle controls are not bypassed or changed. No separate ABA behavioral qualification was run in this task.
- Agent representation is still needed: current Agent `_step_undo.inverse_stages` emits one flattened group. Emit the two internal ranges above using the same immediate publication / `undo-0` / `[0]` identity while retaining one outward public command/step. Keep exact source native/effect correspondence and current-request commit.effect attribution. The early handoff carries this interface; no Agent edits made.
- The existing **competing-media compiler refusal remains a separate cause**, unchanged. Fix/qualify Agent's private representation and compiler cause, obtain independent review of both sides, then let the orchestrator authorize any public redo attempt. No fresh public retry is justified by this source-only result.

## Durable artifacts and hashes

Worker evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-nested-range-1543/evidence/`.
Flat shared-design exports: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-R2r-nested-range-1543-{source.patch,tests.py,auth-input.json,checks.py,integrity.log,baseline.log,targeted.log,integration.log}`.
Early handoff: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-R2r-nested-range-1543.md`.

- `runtime_protocol/timeline_commit_auth.py` SHA-256 `b1660f777dec9657dfb737a1e686dd682d6d514a5c2ed76efd3c1f4ca56222c0`
- `tests/test_timeline_inverse_stage_authentication.py` SHA-256 `bbafddf6a0ca7f8e644cbc35a35445371f43776a7f4ade3bb11b757c864a2f01`
- `tests/fixtures/timeline_nested_inverse_1543.json` SHA-256 `8798a4b3a66b6922367add8cae44183a112dea54e4ec15b4e67a47ae7e8b6a13`
