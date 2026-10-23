# R2r leaf Sol 1338 independent review

## Verdict

**Narrow Runtime inverse authentication: PASS / producer qualified.**

**Overall whole undo/redo readiness: FAIL / incomplete.** The remaining failure is independently assigned to the Agent redo compiler; it is not a Runtime inverse-authentication failure and must not be reported as complete.

## Candidate and scope

- Candidate `4578bafb0e59f5b12548b3ae91087a42e56e6f1f`, tree `3675f446c82c455ef5635ae725409eb6076a4f83`, fresh parent `8592822fd11275540f596562f43c715676f2bc0f`.
- Candidate diff has exactly three paths: `runtime_protocol/timeline_commit_auth.py`, `tests/test_timeline_inverse_stage_authentication.py`, and `tests/fixtures/timeline_leaf_inverse_1246.json`. The production change is confined to `_inverse_stage_boundaries`; the inverse root equality guard remains unchanged.
- This review made no product, test, fixture, generated, pin, or contract edits; no merge or push was performed.

## Evidence review

The fixture is byte-identical to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-leaf-1246-e97f81ce7c350f08.json`: 426,995 bytes, SHA-256 `1123978b7b18c59d280f73c9ad9155b5ba18d0c64b24e45b8bdd02af30a887b0`. The custody manifest SHA-256 is `803c11e3e9bd1c4a8794365f7ce11574a7224bd2f735aaafc7ec2ce942cdfc74`; every artifact source and compact hash matches. Its credential check is PASS with no copied bearer/auth headers, Codex credentials, or request body; the package capture records `credential_fields_copied=false`.

The actual retained stage images have five roots each and compact sizes 9,059/9,052. The authoritative source history is publication `txn-1c5db05293e34736a5207e6f07c3818f`, with `fork-edit-0` at ordinal 0 and `fork-edit-1` at ordinal 1. The inverse stage ranges are native `[0,1]`/effect `[0,5]` and native `[1,3]`/effect `[5,9]`. An independent 27-check audit passed: custody, manifest, credential scan, source-history authority, ranges, and old-RED/new-PASS were all verified. The fresh parent rejects the exact full packet with `inverse stage native writes do not cover its authenticated effect image`; this candidate accepts it.

All 21 retained strict forgery controls pass, including owner/mixed-owner, edge/digest, history step/ordinal/base/head, aggregate pin/payload, native before/after/order, range/stage order, extra effect/unrelated payload, combined effect-image+binding, equal-payload foreign-owner, and equal-payload foreign-root cases. Refusals remain `invalid_records` and inputs are unchanged.

## Public journey classification

The first public probe’s `ValueError` is an observer call-log shadowing error after successful whole undo assertions, not a product refusal. The continuation reopened the same persisted realm, confirmed exact original restoration, and retried the exact undo request; the retry returned the same reply and left head, canonical document, history, and SQL dump unchanged.

One redo attempt then failed in the distinct Agent checkout `/home/user/work/wt/agt-pin-bfcf78db`, not in the Runtime checkout. The causal path is:

`astrid/sdk/timeline/commit.py:1072` → `astrid/sdk/timeline/commands.py:258` → `astrid/sdk/timeline/_commit_patch.py:387` → `astrid/sdk/timeline/_commit_patch.py:222` → `astrid/sdk/timeline/_doc_patch.py:117` → `astrid/core/timeline/authoring_bundle.py:1127`

The exact error is `invalid_document: shot 'selected-shot' has competing selected media between shot items and internal clips`. This occurs before Runtime `timeline_commit_auth.validate`; no redo retry was run. Before/after snapshots for the redo attempt are identical, and the captured Runtime/Agent origins are separate and hash-verified. No Runtime product finding is raised. The precise remaining owner is Agent R2 inverse/redo closure compilation.

## Reviewer commands

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_source_duplicate_authority.py
182 passed in 59.01s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py -k actual
21 passed, 52 deselected in 1.33s

/root/.local/bin/ruff check runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py
All checks passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /root/.local/bin/pyright runtime_protocol/timeline_commit_auth.py
0 errors, 0 warnings, 0 informations

git diff --check 8592822fd11275540f596562f43c715676f2bc0f --
passed
```

No full suite, browser/socket suite, or separate G5 restructure run was performed. Next step is an Agent-owned redo compilation fix and a fresh public redo plus exact retry qualification; do not claim whole undo/redo readiness until that succeeds.
