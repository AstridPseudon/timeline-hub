# R2 authenticated occurrence landing fold

Bounded result: PASS. The exact retained offline redo now passes the landing `parent.occurrences` guard with exactly the canonical one-row `occ-film` state. Complete offline redo still refuses at the subsequent historical scratch guard; no accepted redo output or complete public redo is claimed.

Base: `257f0a853720d431ab9c9d2a9bd2c73842253b8b` (`tl/agt-R2-source-history-sol-1637`). Only `astrid/sdk/timeline/inverse.py` and `tests/editing_conformance/test_captured_registry_redo.py` changed. Product delta: 42 additions / 2 deletions; tests: 130 additions. No helper, commit/plumbing, Runtime, forward G5, wire, pin, dependency, generated file, or identity allocation changes.

## Change and authentication

For an AcceptedRecords batch with the existing authenticated physical resolver, `coalesce` projects later occurrence-root writes from the SAME command into its earlier aggregate after-image. It resolves by the recorded `occurrence_id`, checks the exact alias before-row, rejects duplicate/missing/mismatched identities, and replaces/removes in recorded order without sorting. It preserves the aggregate before-image and retains every native alias write for reservation/order/source restoration, guard scans and reversal. The resolver, complete history checks, and source callback are unchanged. Plain records and accepted records without the physical resolver retain their original aggregate.

The landing guard compares that exact projected aggregate with physical bundle `placements`; it refuses any contradictory `parent.occurrences` storage (including null, empty object or equal rows), rather than overwriting it. Canonical bundle storage excludes occurrences from editable `parent`.

No initial contradiction waiver, membership/order relaxation, ABA exception, shot-id analogy, equal-byte source mapping, broad logical-address alias, dropped native/effect fact, or replay of the original forward public body was introduced. Direct registry/config storage and ABSENT/null/empty-object distinctions remain unchanged.

## Exact NEXT boundary and correction to prior diagnosis

The prior review correctly identified the missing three-to-one fold. Its diagnosis omitted that the generic State reader actually returns ABSENT at `parent.occurrences`, because physical rows live in `placements`; it does not return the one-row list. This is visible in both the retained original failure and the new trace.

After the landing fix, all landing guards pass. Historical scratch reversal restores the two chapter occurrences and the intermediate film row. Its ordered `placements` EXACTLY equal the raw aggregate after-image `[occ-film, chapter-shot-837324ae5797370162ac-occ, chapter-shot-3f756cd1547d015ebd4b-occ]`. The next unchanged `guard(scratch, ...)` still reads `parent.occurrences` as ABSENT and raises `inverse_conflict`, `original authored guard changed`, before public mutation. This is a historical storage-access continuation, not evidence of changed row values, membership, order, source identity or a shot-id common cause. `guard-trace.json` contains expected, actual and scratch placements; `audit.py` asserts exact equality of expected rows and actual physical scratch rows.

I stopped at that boundary as requested instead of expanding this landing-fold patch into historical aggregate guard/write routing. The next owner should route that historical physical storage consistently through guard, restoration and recorded reads/writes, preserving the native/effect history, and re-run the exact retained packet. Do not waive the scratch guard or claim complete redo from this result.

## Targeted evidence

All commands run from `/home/user/work/wt/agt-R2-occurrence-fold-sol-1651`. Python invocations use read-only shared dependencies and private caches. `tmpdir` in the worker folder is a file containing `/tmp/w-a25d1e8de2`; an initial Ruff cache attempt treated that pointer as a directory and failed with ENOTDIR, then was corrected to its actual path. No permission/classifier rejection occurred.

Final requested lane:
```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-e6a84469 PYTHONPATH=.:/home/user/work/wt/rt-pin-e6a84469 /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider tests/editing_conformance/test_captured_registry_redo.py tests/editing_conformance/test_captured_nested_redo.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py
```
**113 passed in 11.28s** (registry 45, nested 32, stage images 1, step undo 35); log `focused-final.log`. Original tests/expectations were retained. The 26 added cases include two positive capture regressions, 22 strict no-write attacks and two resolver-authority controls. Attacks cover changed row/owner, missing/extra/duplicate membership, contradictory parent storage, alias before/owner, changed aggregate row/order, missing/duplicate native alias, ABSENT/null/empty aggregate, forged source publication/step/negative or extra ordinal, native range and effect range. Existing captured tests still cover changed registry/config, effect forgery, missing boundary, digest forgery, intervening ABA and all six nested source-identity refusals.

Causal old-RED used the unchanged base inverse module only, then ran the two new positive tests; **2 failed in 0.40s**. Exact invocation (same environment as final lane):
```python
import subprocess, pytest
from astrid.sdk.timeline import inverse
source = subprocess.check_output(['git', 'show', 'HEAD:astrid/sdk/timeline/inverse.py'], text=True)
exec(compile(source, 'retained_inverse.py', 'exec'), inverse.__dict__)
raise SystemExit(pytest.main(['-q', '-oaddopts=', '-pno:cacheprovider',
 'tests/editing_conformance/test_captured_registry_redo.py::test_captured_occurrence_guard_folds_same_command_aliases',
 'tests/editing_conformance/test_captured_registry_redo.py::test_captured_redo_passes_canonical_occurrence_landing_guard']))
```
The new source passes both as part of the 113-test final lane. `causal-old.log` retains the failures. Exploratory runs preceded final changes: 1 failed / 87 passed exposed the separate physical-storage issue; 102 passed preceded the extra source-partition controls; 108 passed preceded final storage/authority controls. No test was skipped, weakened, deleted or marked expected-failure.

Checks (all final PASS):
```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-a25d1e8de2/ruff /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/inverse.py tests/editing_conformance/test_captured_registry_redo.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-e6a84469 /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/inverse.py tests/editing_conformance/test_captured_registry_redo.py --cache-dir /tmp/w-a25d1e8de2/mypy-scoped --hide-error-context --no-pretty
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-a25d1e8de2/ruff /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-e6a84469 MYPY_CACHE_DIR=/tmp/w-a25d1e8de2/mypy-baseline /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```
Scoped Ruff: all checks passed. Scoped mypy: success, 2 source files. Normal Ruff baseline **2149/2149**, private mypy baseline **1912/1912**. Official vendor source remains `34eac0041b0891e9011966b39bcbd26053fde5bc`; lock OK; artifacts current; diff clean. No full or service/browser suite requested or run.

Offline audit (same final Python environment):
```sh
/home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-occurrence-fold-sol-1651/audit.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-presence-sol-1617/audit_packet.py
```
Own audit PASS: exact landing, next scratch boundary, all 22 attack tests and unchanged input bundle/capture/records. Retained audit PASS: 320 contiguous payload hashes, lossless captured source subset, original no-write canonical/head/history/SQL. Embedded supplement equals actual packet source history (including event 164); no fabricated compact history.

Runtime code imports are from `/home/user/work/wt/rt-pin-e6a84469/runtime_protocol/`; Agent inverse/commit imports are this worktree. Read-only `git diff --stat e6a84469 d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` confirms only deletion of Runtime root `report.md` (53 lines). No Runtime execution source differs.

Independent predecessor review is terminal PASS: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-source-history-review-1649/report.md`. It reports cumulative 103 PASS, attack 40 PASS, source callback/native-only/R1/private carrier preservation and unchanged baselines. Those files/hunks remain byte-identical here; source hashes below. This author result does not substitute for independent review of this new delta.

## Custody and hashes

Retained full packet is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-redo-budget-sol-1605/evidence/agent-G5-redo-budget-1605-7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15.packet.jsonl`, SHA-256 `7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15`. Retained input is the unchanged `agt-R2-registry-presence-sol-1617/captured-input.json` (events 154/264/266); the test embeds those exact bytes.

All following semantic hashes use canonical sorted JSON with compact separators except capture/supplement/source-file hashes, which hash exact bytes. The retained canonical-after hash describes the expected input head, NOT a newly accepted redo result.
- `capture_sha256`: `b55cca41df4ee9490c537e01e77742310fc198729f9c4c7acb595da8d833a266`
- `source_history_sha256`: `40ea0dda05c20e01bf38eabac35688fbf71d774657a0f9557efe02714fd4e683`
- `request_sha256`: `42afcdffb6aa4ab18cc60ec68d0b132931a19713ff4e500fcfcdd2983e0e3465`
- `before_sha256`: `9c0d1b08599c0c0f8fb895c65a18bca29ca3dab4fff8c21307032fadb882b312`
- `canonical_after_sha256`: `fb065813884e247d4946426017a360224a9367e515aac6eb7cbe7d24763d6a2e`
- `guard_trace_sha256`: `b22b90b77ff06302f9055f0e606197bd3f6a9129fb63db5eb1936f213ef74865`
- `security_cases_sha256`: `ff55d8a81f19f3c7224505107e56a97930304fd46e5a21974c069ffc6636ece9`

Exact source file SHA-256:
- `astrid/sdk/timeline/_commit_patch.py`: `b971050c92b14304bbc037ed775ddb7ddfa6cf5a233cd2075f92ba68725c3163`
- `astrid/sdk/timeline/_recording.py`: `85aefe0328a7c9787a18c2b7e19eb8b3e4220a1c53627d1e16102b42b29c8b43`
- `astrid/sdk/timeline/_root_inverse.py`: `0d81d995582622367cca770855d7604735d3a707a7e8d6d6d5d6102367c4949a`
- `astrid/sdk/timeline/_step_undo.py`: `206f13ac5991ed6abecbc0b1fbde24f2526cb3bf2f47f57f9b91c66aa43fa1dc`
- `astrid/sdk/timeline/commit.py`: `a4d612aeadfd66011258b9003d3b7d9a4f33c4fa387c50b65bf4fa79bafb4e91`
- `astrid/sdk/timeline/inverse.py`: `0638e98f11a96230246f8c9685b48096abea6524a5308f9cce787bb69989380a`
- `tests/editing_conformance/test_captured_nested_redo.py`: `d7567b519698bd9ae36b44f1747ad26dd0e394dd7f1cdaaf3b83866ed2b7f8d4`
- `tests/editing_conformance/test_captured_registry_redo.py`: `9779118aaf953b1bee428fddf27690bb1a2bfcbbf63defcd4945cf661d64e1c2`

Artifact raw-file SHA-256:
- `source-checks.json`: `926a97f0688aeff0a283a099fd8105e09bb6ac977210d0b4ee05757a1090fd80`
- `guard-trace.json`: `8185277b0cb69856af9dd8736c1441125486b410ee7d01c5eb8ab85ddb267a81`
- `security-cases.json`: `dd9bb5c38482761da1d534ee9e9d73922fb9ce95668ad8b8d0d5f9aa792c47a3`
- `audit.py`: `7faffb844c7eea845e8cabe2d066c4df5b410ff341434d3f25631cc1222f8b67`
- `focused-final.log`: `ef1415f3040987c9124dd53b70c1368abbf63117eaed126f0cce72a909593d93`
- `causal-old.log`: `6698db392ea6fb5fd9e03fb8887c65ebf383bbc006e00260b4ddf9ebcea363e7`

## Limits and next steps

The complete retained offline redo and public redo remain unverified past the documented scratch boundary; no canonical redo result was emitted. No joint public redo, c271/original forward body, P1/P4, full184, 40/281/58/native14, browser, daemon or body-duplicate execution occurred. No Git mutation, push, commit, merge, checkout, ref deletion or integration-worktree write occurred.

Request manager independent cumulative review of this two-file delta, then assign the historical physical aggregate storage continuation to the unique inverse owner. Only after meaningful cumulative independent PASS should the manager assign any actual full-body execution. Commit message is in this worker folder; the harness owns committing.
