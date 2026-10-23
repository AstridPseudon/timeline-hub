# Agent R2 redo media closure 1404 — source PASS; public redo FAIL

Base `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`. Source repair and focused regressions are ready for independent review. Overall whole undo/redo remains incomplete; G5 P1 remains NO-GO. No guard waiver, plan/contract decision, pin or adoption change.

## Diagnosis and repair

Consumed PLAN R2/§2, C0 §2/§5, Runtime 1338/1354, the 1356 redo export and owner-announced Runtime merge/proof at `cfa0af0d476e6954df041c08d7ef378fd6782932` (tree `3675f446c82c455ef5635ae725409eb6076a4f83`). The original 426995-byte inverse package was not substituted for the new redo packet.

New redo packet `runtime-R2r-redo-1338-9603ca432b1c9d1c.json` SHA-256 `9603ca432b1c9d1c1b16908f00547d26da6d04df3ad681308cbae5f3e57635d1`: all 53 members verified byte-for-byte. Exact offline production-provider replay through ordinary `RequestCommitPort` reproduces the original `invalid_document` with SQL unchanged.

The complete failing child payload AND internal timeline match the accepted forward canonical source exactly, with complete owner set `{f2-occurrence}`. Native inverse reconstruction restores a plain `_created: true` shot, losing its baseline provenance. The media guard then compares the retained `{visual, voiceover}` shot metadata against an empty baseline and rendered `{visual}`; it correctly refuses that representation. This is historical child reconstruction, not an incomplete root-order transient or a reason to relax media validation.

The repair uses the existing native copied-shot carrier pattern. `_commit_patch.py` recognizes a reconstructed child only when its complete payload/internal pair and complete owner set match a verified same-scope historical canonical closure. It attaches `_RestoredShot` provenance outside authored JSON to both stage and final native state. `authoring_bundle.py` revalidates that canonical source, current source/base, scope and complete owners and supplies the accepted baseline to the existing compiler. No authored field, source mapping, immutable pin, digest, physical owner or allocation is replaced. No whole parent/root is restored. JSON roundtripping strips native authority and still refuses. A new competing selection after recovery still refuses.

`compile_authoring_candidate` is byte-identical to base, including every media/selection guard. `commit.py`, `_doc_patch.py`, `inverse.py`, `_root_inverse.py`, vendor lock and artifact manifest are unchanged. Current `_doc_patch.py` and compiler were byte-identical to captured bfc; the earlier atomic union fix in `_commit_patch.py` is preserved. No old bfc wholesale port. The temporary `commit.py` hunk request was withdrawn: this repair needs no edit there and does not overlap 1403's sequential capture or 1416's inverse orientation.

The new main-suite fixture is a genuine bounded extraction: exact retained redo before SQL/document/head/history, full request, expected forward document and failing stage/source closures. It is 912201 bytes, SHA-256 `a20636115ffb6e986ad7731d57bc90dd7ed98a2330b65d3dc71b83a3707ddb37`. Original deterministic media bytes from `seed_shared_occurrence_parent` match both retained SHA-256 pins; no media/history/pin/source was fabricated. The test never attempts acceptance.

## Exact source control and single public journey

Original archived base is RED at the original media guard; current source is GREEN to a schema-valid prepared redo with entire expected forward canonical document, including all revision IDs, exactly equal. Ordinary-port offline state remains unchanged. Scope is compiler success, not Runtime acceptance.

After the Runtime owner announced reviewed/merged/proven cfa0, one new public in-process service journey used the exact original fork+free-edit body and retained pre-forward SQL. This restores the original realm identity/source rows; it does not provision a realm, credentials, environment or daemon. Public service route, production provider loader, ordinary port and real durable acceptance all ran. The convenience Python Timeline wrapper was not separately exercised.

- Preview predicted accepted and did not change the canonical document.
- Forward ACCEPTED: `txn-7d039d147e1b4c5ba6cc7ca912b95cba`; canonical document exactly equals preview.
- Whole undo ACCEPTED: `txn-75285c95600949c8b1267a71f8e71a9d`; entire original canonical document including IDs restored.
- Exact original undo request/key retry returned identical reply with unchanged full SQL/document/head/history.
- Redo passes Agent compilation, then Runtime cfa0 refuses `invalid_records: inverse stage write differs from its sequential input` at `timeline_commit_auth.py:971`. Full SQL/document/head/history remain unchanged. STOPPED; no redo retry, body change, Runtime patch or guard waiver.

Actual next mismatch: native `occurrence:f2-occurrence`, path `[shot_id]`, before is working alias `shot-placement-90b9827beed9a42dfba309ec7e05837ada743a57e18dd5f26704de552870c382`; sequential canonical input holds physical `document-diff-e0c6162a4844471b99fd8d1076df92e9-shot`. After is `selected-shot`. This is evidence of a concrete native-before/canonical mismatch, not a Runtime guard bug. New actual redo prepared/source/history/physical stage maps were obtained by offline replay of the retained new public snapshot, with production authentication and no acceptance; the same refusal reproduces. Coordinate inverse-source/orientation owner 1416 with Runtime before deciding the next source repair.

No public redo restoration, redo retry, new public later-history ABA, merged/conflict journey or overall R2/G5 readiness is claimed. Existing source-level later-history/ABA tests pass unchanged.

## Durable evidence

`E = ORCH/workers/agt-R2-redo-media-closure-sol-1404/evidence` retains complete original export members, offline scripts/results, new public requests/replies/errors and before/after states, actual prepared/authentication/stage maps and module origins. All imported Agent/Runtime module origins before and after redo hash-match the final source files. Private baseline archive and tool caches are in `/tmp/w-7e2dc905b1` (the worker's named tmpdir); shared dependencies were read-only.

Bounded FLAT packet: `design/agent-R2-redo-media-1404-a29df82beb548306.json`, 1481631 bytes, SHA-256 `a29df82beb548306683ab64d738eb776a519587fdb30cad3e997e91468621ef8`. It contains full requests/metadata/receipts, exact complete redo before/after SQL/document/head/history, actual prepared/source/history, physical mirror map, full origins, source diff and checks. Credential-token scan: zero matches. No credentials were created or copied.

## Commands and results

All commands below run from this assigned Agent worktree unless noted. `E` and `TMP=/tmp/w-7e2dc905b1` abbreviate the paths above; these are not omitted source inputs.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-cfa0af0d timeout 40 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_captured_redo_media_closure.py tests/timeline/test_authoring_bundle.py::test_timing_is_admitted_but_competing_selected_media_fails_before_publish --basetemp=/tmp/w-7e2dc905b1/final-focused
# 10 passed in 2.45s; exit 0. Earlier new-file-only run: 9 passed in 3.49s.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime timeout 40 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -m 'not integration' -p no:cacheprovider tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py tests/sdk/test_timeline_inverse_binding.py --basetemp=/tmp/w-7e2dc905b1/inverse-neighbors-fixed
# 74 passed, 1 integration deselected in 13.48s; exit 0. Existing test unchanged.

/root/.local/bin/ruff check --no-cache astrid/core/timeline/authoring_bundle.py astrid/sdk/timeline/_commit_patch.py tests/editing_conformance/test_captured_redo_media_closure.py
# All checks passed; exit 0.

PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-7e2dc905b1/ruff /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
# current=2149 baseline=2149; exit 0; all changed paths have zero diagnostics.

PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-7e2dc905b1/mypy /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
# current=1912 baseline=1912; exit 0.

PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-7e2dc905b1/mypy /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes > /tmp/w-7e2dc905b1/mypy-current.txt
# expected exit 1, 1912 existing findings. Same command from untouched git archive HEAD
# with cache mypy-base and output mypy-base.txt: 1912. Exact (path,message,code)
# diagnostic multisets equal; zero added/removed identities, excluding shifted lines.

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
# ok runtime.lock.json; exit 0.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# artifacts.json is current; exit 0.
git diff --check
# exit 0.

# Untouched archived source replay; working directory /tmp/w-7e2dc905b1/base:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/w-7e2dc905b1/base:/home/user/work/wt/rt-pin-cfa0af0d:/home/user/work/wt/agt-R2-redo-media-closure-sol-1404 timeout 40 /home/user/work/venv-agent/bin/python E/offline.py
# captured invalid_document RED; SQL unchanged; observer exits 0 after saving result.
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d timeout 40 /home/user/work/venv-agent/bin/python E/offline.py --prepared
# PreparedReached sentinel: full canonical exact restoration GREEN; SQL unchanged;
# exits 0 after capture. Acceptance never invoked.

PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-7e2dc905b1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-cfa0af0d timeout 40 /home/user/work/venv-agent/bin/python E/public_positive.py
# exit 1 at the one redo attempt: Runtime invalid_records sequential-input mismatch.
# Preview/forward/whole undo/exact undo retry pass before refusal.
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d timeout 40 /home/user/work/venv-agent/bin/python E/offline.py --prepared --new-public
# exact new redo compiles, Runtime authentication reproduces refusal offline;
# SQL unchanged, exits 0 after recording the expected diagnostic exception.
```

Harness-only failures: a first neighbor command lacked the Runtime import path and failed conftest before tests; corrected invocation is above. Initial baseline archive replay lacked the standalone generated client path; corrected invocation is above. First public snapshot admission lacked its staging directory and failed before any public call; restored that directory and resumed the same exact pre-forward SQL snapshot. No product guard or assertion was changed for these invocation repairs.

No full/original40/281/58/native14/P1/P4/browser/D17 lane, daemon, socket, new credential/realm provisioning, dependency install, Git mutation, or push ran. No test was weakened/skipped/deleted. Conventional commit message written; harness owns commit. `BLOCKED` records the distinct next public boundary; no DONE/whole-redo success marker.

Next: independently review/commit this narrow compiler repair, then have inverse-source/orientation and Runtime owners inspect the exact newly retained native-before mismatch. Do not retry public redo until a meaningful reviewed source fix addresses that exact packet. Qualify public redo exact retry and later-history ABA only after acceptance succeeds.
