# R2r leaf inverse 1338 — narrow Runtime PASS; whole undo/redo readiness FAIL

Implemented the real retained two-stage inverse, with no guard waiver. Both stages now authenticate, the requested three-file lane passes, and normal public whole undo restores the entire canonical document exactly. Public redo remains refused by Agent compilation at a distinct boundary. **Do not mark whole undo/redo ready.** No plan or contract decision was changed.

## Candidate and scope

- Fresh parent: `8592822fd11275540f596562f43c715676f2bc0f`, tree `ed9856f43a4e44a058bf2230badea2c4c7080050`.
- Prospective candidate tree, calculated from Git object encoding without writing the index: `3675f446c82c455ef5635ae725409eb6076a4f83`.
- Own commit is pending the harness; only this worker's commit is requested. No commit/merge/rebase/checkout/push was run. Held `6e256`/`432` are not parents.
- Production change: only `runtime_protocol/timeline_commit_auth.py::_inverse_stage_boundaries`.
- Tests: append-only additions to `tests/test_timeline_inverse_stage_authentication.py`; one durable JSON fixture, `tests/fixtures/timeline_leaf_inverse_1246.json`.
- No Agent/App/port/store/config/generated/client/schema/pin/source-authority/allocation changes. No original test was changed, deleted, skipped, or weakened.

The failed `6e256` product function was inspected read-only as an allowed scoped helper port: its owner/digest/paired-edge checks provided useful starting code. Its synthetic helper and tests were never imported. The new implementation additionally validates source-history attribution and source effect-image pins, handles the actual fork's canonical source pair, and translates only the exact internal pin of a previously authenticated turnover in later aggregate captures. `_inverse_stage_root_equal` is unchanged: there is no general permission to discard a claimed pin.

The actual fork native capture's restored `shot_id` is an older authoring alias, while the accepted canonical source effects name its physical shot identity. The fix requires the exact reversed accepted native capture and then restores the exact source-history `shot_id`/`shot_revision_id` pair. It does not take this pair from `stage_after`. Leaf materialization requires the source binding's exact owner, owner set, base/head/step/ordinal, revision, digest and paired internal/shot edges; restored full payloads must agree. Complete stage payload-map equality, strict sequential observations, native membership/ranges, per-effect binding checks, and final output equality remain active.

## Lossless capture and offline proof

`ORCH` = `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`.
`E` = `ORCH/workers/rt-R2r-leaf-sol-1338/evidence`.

The fixture is the **entire exact original package**, 426,995 bytes; no extraction, normalization, fabricated history, or replacement closure occurred. Its raw SHA-256 is `1123978b7b18c59d280f73c9ad9155b5ba18d0c64b24e45b8bdd02af30a887b0`. Manifest SHA-256: `803c11e3e9bd1c4a8794365f7ce11574a7224bd2f735aaafc7ec2ce942cdfc74`. Pattern scanning found zero bearer tokens, API keys, private keys, or nonempty credential fields; the package's original credential scan/custody metadata is retained too.

- Request compact SHA-256: `9513a98ac9413e4395632693701c664db3557c61e5ed150ca1875a4885e50b5b`.
- Prepared compact SHA-256: `bd78bb8ffa030ccadddeebe62bec56ab9fa7623232c6e0c4d759523048d92afa`.
- History compact SHA-256: `0122a97346985a270f38b2e9f49819a28399f4f7faa3e9821622d85b2447897e`.
- Source publication: `txn-1c5db05293e34736a5207e6f07c3818f`.
- Actual first stage: `fork-edit-1`, source command ordinal `[1]`, native `[0,1]`, effects `[0,5]`; before/after exactly match the captured five-root maps, 9,059/9,052 compact bytes.
- Actual second stage: `fork-edit-0`, source command ordinal `[0]`, native `[1,3]`, effects `[5,9]`; starts at that exact first-stage output and reaches the complete retained final canonical closure.

`E/verify.py` loads the original auth module with `git show` and validates the identical full packet: old rejects `inverse stage native writes do not cover its authenticated effect image`; new passes. `E/actual-stage-images.json` retains every per-effect physical boundary. `E/verification.json` records hashes and custody checks.

The new offline cases cover owner and mixed-owner pairs, wrong edge/digest/history step/ordinal/base/head, wrong aggregate pin, native before/after mismatch, unrelated aggregate payload, swapped native/stage order, wrong range, extra effect, unrelated output payload, combined effect-image+binding forgery, equal-payload foreign-owner swap, and equal-payload foreign-root identities. All refuse `invalid_records` without mutating their inputs. These are authentication-only tests; do not represent them as new persisted-store negative journeys. Existing store no-write negatives are included in the passing lane.

## One public journey and retained remaining owner

Normal production Agent checkout: `/home/user/work/wt/agt-pin-bfcf78db`, commit `bfcf78db998868e4a7d92779a83cd3aaba82a98a`, tree `31af8a966328d313506919df9c073d4681854f0c`, clean. Runtime imports point at this candidate worktree. Setup was recorded before the call. Before/after module origins were captured separately at each public boundary, with Git-source/hash verification (203 modules around undo; 71 before redo provider load, 144 after the redo refusal). See `E/public-setup.json`, `E/public-resume-setup.json`, `E/public-origins-*.json`, `E/origin-verification.json`.

The exact Agent 1246 regression setup performed preview and accepted normal fork+free-edit. Public whole undo was accepted, restored the entire original canonical document including original revision IDs, and retained the source history and authoritative steps. Publications:

- Accepted fork+edit: `txn-f73af2c66fa248c69eae159c3e4a8a64`.
- Accepted whole undo: `txn-f962cd740f864c8e9449fbd22407853a`.
- Exact original undo request/key retry returned the same reply; head/document/history and full SQL dump were unchanged.

A diagnostic harness error followed the successful undo assertion: the regression's local `calls` list shadowed the observer's call log. This was a `ValueError`, not a product refusal. Its exact executed script, log and result are retained. The continuation reopened **the same persisted realm**, checked exact original restoration, replayed only the exact undo idempotency request, and attempted redo once; it did not repeat preview, edit or undo production execution.

**Redo FAIL, narrow remaining owner: Agent R2 inverse/redo closure compilation.** The normal redo request targets the accepted undo and passes request schema validation, then raises `invalid_document`:

```text
shot 'selected-shot' has competing selected media between shot items and internal clips
```

The retained causal stack is Agent `commit.py:1072` → `commands.py:258` → `_commit_patch.py:387` / `inverse_closure:222` → `_doc_patch.py:117` → `document_from_bundle` → `authoring_bundle.py:1127`. This is before a redo prepared result reaches Runtime acceptance. It is not evidence that the repaired Runtime stage guard still fails, and is not proof of an invocation/D18 defect. The full v2 redo body, error details/traceback, before/after head, canonical document, history and database are in `E/public-service-05-*`; all four states are unchanged after refusal. Public execution stopped immediately. There was no retry or guard relaxation after the product refusal.

`E/public-undo-auth.json` and `E/public-undo-stages.json` retain the actual successful caller packet and complete stage images. `E/public-summary.json` identifies all five calls (preview, forward, undo, exact undo retry, refused redo). No redo canonical restoration, redo retry, merged/conflict journey, or new later-history ABA qualification is claimed. The existing later-history scan is untouched. Separate G5 original 503 / Agent closure 1319 was not rerun or assumed to share this cause.

## Exact commands and results

All commands run from the assigned Runtime worktree unless explicitly using an Agent path. `E` abbreviates the evidence path above; `TMPDIR=/tmp/w-e61bdbb673` is the private scratch directory named by the worker's tmpdir file.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py -k actual --basetemp=/tmp/w-e61bdbb673/offline-tests-4
# 21 passed, 52 deselected in 1.64s (offline-tests.log)

PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python TMPDIR=/tmp/w-e61bdbb673 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_source_duplicate_authority.py
# 182 passed in 57.37s; all marks included; no skips (acceptance.log)

/root/.local/bin/ruff check runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py
# All checks passed (ruff.log)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /root/.local/bin/pyright runtime_protocol/timeline_commit_auth.py
# 0 errors, 0 warnings, 0 informations (pyright.log); zero added identities against documented base 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python E/verify.py
# PASS: actual old RED/new PASS, exact stages/custody, 17 original definitions, frozen77, prospective tree

git diff --check
# PASS

PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-e61bdbb673 PYTHONPATH=/home/user/work/wt/agt-pin-bfcf78db:/home/user/work/wt/rt-R2r-leaf-sol-1338 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-R2r-leaf-sol-1338 timeout 35 /home/user/work/venv-agent/bin/python E/public_probe.py
# exit 1 after successful public whole undo: observer local-variable collision (public-probe.log)

PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-e61bdbb673 PYTHONPATH=/home/user/work/wt/agt-pin-bfcf78db:/home/user/work/wt/rt-R2r-leaf-sol-1338 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-R2r-leaf-sol-1338 timeout 35 /home/user/work/venv-agent/bin/python E/public_resume.py
# exit 1: exact undo retry PASS, single redo refused invalid_document (public-resume.log)
```

Development-only test setup errors were corrected before qualification: the full package's non-auth metadata does not universally reserialize to its source compact hash after package key sorting, so only the exact auth/stage hashes plus the entire raw package hash are asserted; a mistaken exception import was corrected. No captured data was modified to fit a hash, no product failure expectation was changed. Early log content was replaced by the final passing offline run; the complete worker tool transcript retains these attempts.

All 17 original top-level test function/fixture ASTs match fresh base. All production bytes outside the authorized function and all port bytes match `9c694858e36eefe2c005141ee8fbcdfbc8403943` (`E/source-allocation-byte-proof.json`). The real 77-path manifest from worker 0844, reused by child-source reviewer 1303, has SHA-256 `1182681d20a2503ffb96bfcff2efac25ab598fc9a42d38c72aea1cf977a31fc7`; every path matches fresh base. Its schema/client/generator subset also matches `34e`; the contract prose itself had preexisting changes relative to `34e`, so no false full-manifest-to-34e equality is asserted. `d106` edit schema digest is unchanged. No tuple or adoption changed.

Module SHA-256: `46f79f095d5ab4e9b6e50350e3664c2f19991cc6f18cf1b6cb49c9b3e1ee3bd1`.
Test SHA-256: `bfa16a4da58aacc1cdfed24c66d7559f584b38dade8d702a8694fe8280652a80`.

No full suite, 58/40/281 lane, native14, original20, P1–P4, browser, duplicate tour, daemon/socket or environment build ran. Shared dependencies were read-only. Standalone public probes used the normal in-process service; pytest `--net` was not applicable because no network/socket test was run.

Recommended next step: independent review of this narrow Runtime candidate, then an Agent R2 owner should inspect the retained redo compilation baseline/provenance without weakening media validation. After a meaningful source fix, qualify redo and its exact retry plus the outstanding later-history ABA behavior. Overall acceptance remains FAIL until that public positive succeeds.
