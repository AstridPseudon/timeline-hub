# D17 return — BLOCKED; bounded lost-ack repair passes

D17 is **FAIL / not qualified**. Repeated-copy guarded whole undo/redo is still red, and a new mandatory raw-parent fidelity positive is red. No skip, xfail, reversed expectation, waiver, or 58-test qualification remains. Independent review `design/agent-D17-independent-1009.md` is FAIL and has been read.

## Changes delivered

- First removed the strict xfail from `test_repeated_source_copy_real_port_idempotency_and_guarded_inverse`. Its complete success/idempotency/inverse assertions remain active.
- Repaired `timeline_duplicate.py` cleanup after an ambiguous commit outcome. An unresolved durable flight without an authoritative conflict now raises a specific copy-outcome error and retains the destination. Definitive refusals still archive through the existing wrapper. No writer, request carrier, authority, manifest, history, inverse, or Runtime guard was replaced.
- Added real-service lost-ack regressions for disconnect before acceptance and disconnect after acceptance. Both reopen through public `timeline.open`, flush the persisted flight with its exact body/key, verify one accepted publication, clear the outbox, and preserve the source. The accepted-before-disconnect case checks the original receipt on retry.
- Strengthened all 11 existing source-authority/claim negatives with complete SQL-dump equality in addition to their unchanged document/history assertions.
- Added a mandatory raw-parent config-presence positive. It exposes that a source with raw `parent.clips=[]` and no `parent.config.clips` acquires `config.clips=[]` during copying. It remains an ordinary failing test.
- Removed the inherited extra EOF blank line in `native_timeline_duplicate.py` so the cumulative D17 diff check passes.

The two original restructure nodes and every assertion in them are unchanged by this continuation. Authentic trusted source setup and actual media ingestion are preserved. The production route remains `duplicate_timeline -> _duplicate -> _commit_bundle -> normal durable submit`.

## Causal diagnosis and ownership handoff

The repeated-copy test initially reaches copy acceptance and exact replay, then fails whole undo at `parent/config`: the original authored write records config **without** `clips`, but the accepted head contains `config.clips=[]`. `_recording.Recording` initializes `mirrored_clips` from the empty destination; replacing its parent config does not update that flag. `compile_mirrors()` therefore appends a derived config mirror. The aggregate config inverse guard correctly sees different bytes.

A temporary diagnostic change recomputed that flag from the source's actual authored topology, without creating a mirror. That made the final candidate preserve raw source config, but initial copy then failed `provider intermediate parent lacks an effect image`. The complete candidate, effect bindings and source boundary are captured in `/tmp/w-87d955f7bb/mirror-topology-candidate.json`. This diagnostic product change was **reverted**; it is not delivered.

The exact second cause is Agent `_commit_patch.effect_diff.logical_parent`: it pops top-level `clips`/`registry` into config aliases on both boundaries. It thereby erases mirror-presence changes. The candidate after-config lacks `clips`, while projecting its advertised patch over the destination leaves the old `config.clips=[]` intact. Its projected parent digest therefore matches neither the bound after image nor the final candidate. Runtime's refusal is appropriate. **No genuine Runtime authority defect has been demonstrated.** Do not send this as a request to relax Runtime authentication or duplicate the separately reviewed Sol0940 stage-auth implementation.

Deterministic offline replay through the unchanged Runtime:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-1365e4b1 /home/user/work/venv-agent/bin/python /tmp/w-87d955f7bb/projection_probe.py
```

Result: expected `CommitRejected: provider intermediate parent lacks an effect image`; assertions verify that only `config.clips` presence differs. The probe captures the unmodified projection's locals using tracing; it injects no state or cached provider input. `projection-mismatch.json` contains both full parent images and the complete patch. `guard.json` and `guard-stack.txt` contain the first aggregate-guard mismatch.

**Agent R1/R2 normalizer ownership is needed next.** `_commit_patch.py` is outside this brief's seven allowed files. The smallest sound next change must preserve raw topology in effects and their exact bindings, together with the existing authored/derived inverse guards. The continuation did not edit that file or fabricate an alternate effect/authority path within a permitted file. A further source-backed risk, not yet reached dynamically after fixing config, is that shared physical shot aggregate roots are re-opened as per-occurrence working aliases; normalizing inverse root guards must keep the authenticated physical sharing and source links. Do not claim that risk has been tested or fixed here.

## Exact evidence

Working directory for every Agent command below: `/home/user/work/wt/agt-D17-return-1009`.
Common test environment:

```sh
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/home/user/work/wt/rt-pin-1365e4b1
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-1365e4b1
```

All direct tests use the real in-process RuntimeService/store/provider, not localhost, daemons or browser fixtures. Runtime HEAD is `1365e4b17b31c4a7093d5943674637067fd2bab4`, tree `6c69c3dc47822fffbaf27cd63815d2895155ffaa`, clean before/after. Base Agent is `80680fab5`. Baseline stack traces and final `final-origins.json` identify Runtime modules in the exact pin worktree and Agent modules in this assigned worktree; `evidence-summary.json` hashes the evidence files.

Initial, immediately after removing xfail:

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-87d955f7bb/pytest-before tests/editing_conformance/test_commit_runtime_source_copy.py::test_repeated_source_copy_real_port_idempotency_and_guarded_inverse tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter tests/sdk/test_timeline_restructure.py::test_duplicate_commit_keeps_a_repeated_shot_shared
```

**1 failed, 2 passed in 2.82s** (`before.log`). Repeated-copy undo is the actual FAIL; both exact original nodes PASS. No xfail qualification.

New lost-ack tests before the product repair:

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-87d955f7bb/pytest-ack-before tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_unknown_outcome_retains_destination_and_exact_retry
```

**2 failed in 1.99s** (`ack-before.log`): wrapper archived the destination in both ambiguity cases. After the repair, the same node plus `::test_production_duplicate_caller_uses_authenticated_semantic_and_archives_failures`, with basetemp `pytest-ack-after`: **3 passed in 2.78s** (`ack-after.log`).

Strengthened negatives and the new raw-fidelity positive:

```sh
/home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-87d955f7bb/pytest-guards tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_refuses_bad_authority_or_claims_without_writes tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_rejects_project_wide_occupied_shot_without_writes tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_real_port_preserves_raw_parent_config_presence
```

**1 failed, 12 passed in 7.32s** (`guards.log`). Raw config fidelity is FAIL; every strengthened guard is PASS.

Final passing selection, with public-open restart path:

```sh
PYTHONPATH=.:/home/user/work/wt/rt-pin-1365e4b1:/tmp/w-87d955f7bb /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider -p capture_origins --timeout=45 --basetemp=/tmp/w-87d955f7bb/pytest-final tests/sdk/test_timeline_restructure.py::test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter tests/sdk/test_timeline_restructure.py::test_duplicate_commit_keeps_a_repeated_shot_shared tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_unknown_outcome_retains_destination_and_exact_retry tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_real_port_receipts_preview_undo_redo tests/editing_conformance/test_recipe_timeline_source_copy.py
```

**15 passed in 3.88s** (`final-targeted.log`). The origin-capture plugin only records loaded file paths/digests. This selection is not an all-green D17 suite: the two red positives above were not re-run without relevant semantic changes. No full, broad58/native14, HTTP, browser, P1 or P4 suite was requested or run.

Quality/preservation:

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-87d955f7bb/ruff-final PYTHONPATH=. /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
# PASS: current=2149 baseline=2149
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-87d955f7bb/mypy-qualified PYTHONPATH=. timeout 180 /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
# PASS: current=1912 baseline=1912
/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline_duplicate.py tests/editing_conformance/test_commit_runtime_source_copy.py tests/editing_conformance/test_recipe_timeline_source_copy.py
# PASS: All checks passed
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
# PASS: ok runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# PASS: artifacts.json is current
git diff ef851 --check
# PASS after EOF whitespace fix
```

The initial standard venv mypy attempt failed on missing YAML stubs/incompatible NumPy stubs; the existing read-only typecheck venv supplied the final exact-count result. No dependency was installed/changed. The independent review's four test-only Ruff findings in `test_timeline_restructure.py` are inherited and unchanged here; scoped lint including that entire file still reports them. The exact-count product gate remains 2149. No quality baseline was rewritten.

## Mandatory behavior inventory and limits

| Behavior | Actual evidence / status |
|---|---|
| Original chapter IDs/order/distinct roots, repeated physical sharing/raw edges | Both exact original nodes PASS before and after; unchanged assertions |
| Source unchanged, opaque data, raw shot/internal payload content | Pure controls and original nodes PASS; parent config presence has separate mandatory FAIL |
| Idempotency | Single-shot exact retry PASS; repeated-copy test passes its retry/receipt assertions before its undo FAIL; lost-ack before/after acceptance exact request retry PASS |
| Guarded whole undo/redo | Single-shot PASS; repeated physical-root undo FAIL; repeated redo not reached |
| Preview | Single-shot no-write preview/would_status PASS |
| Foreign/outside/pair/digest/same source | Existing real-port variants PASS, now with unchanged complete SQL dump |
| Occupied IDs | Both local-source and project-wide occupied-shot negatives PASS |
| Invalid identity map/sharing/order/created claim; caller media injection | Existing real-port and pure negatives PASS |
| Archived/stale source | Archived-source real-port variant PASS; changed-after-capture stale source not independently exercised through Agent here |
| Forged physical media pin | Caller `args.media` injection is rejected; independent physical media/captured-byte forgery remains Runtime authority evidence, not new Agent qualification |
| Retained media/documents | Pure manifest/dependency preservation PASS; real retained-input undo/redo remains unverified, including releasing source-only retained pins |
| Lost ack / unknown outcome / restart | Both real-service ambiguity cases now PASS via public open and durable exact flush; no process-kill or HTTP qualification |
| Archive cleanup | Known refusal archive control PASS; ambiguous outcomes now retained; archive-operation failure remains unverified |
| Full v2 requests/replies/history/inverse stage guards | Existing implementation preserved; this slice adds no field projection and claims no broad v2 requalification |
| G5 writer retirement | Still gated; old duplicate writer and other legacy routes preserved |

## Integration and next steps

The manager supplied staged merge-forward repairs to 14 other files while this task ran. They were preserved without direct worker edits. `git diff ef851 --name-only` now lists **only the seven allowed D17 paths**: commands.py, commit.py, native_timeline_duplicate.py, timeline_duplicate.py, the two source-copy test files, and the authentic restructure fixture/test hunk. This demonstrates later non-D17 ef851 repairs are present in the working source, but HEAD itself remains saved80680 until the harness/manager performs its Git work. This worker ran no git writes, commits, fetches, merges, checkouts, branch operations, shared installs or daemons.

Recommended next action: manager review the bounded lost-ack repair, keep D17 and G5 blocked, and explicitly authorize the required existing normalizer path for the same semantic repair ownership. Preserve the two red positives. Require lossless parent effects/bindings and shared-root guarded whole undo/redo to pass before any D17-ready statement or G5 deletion. Runtime Sol0940 review remains separate and must not be duplicated. Retained-input inverse and isolated captured-source/physical-media negative evidence remain outstanding. Harness commit message intentionally describes the bounded repair, not completion.
