# R2 split inverse mirror repair

The bounded Agent repair is implemented and independently reviewed. Requested targeted acceptance is green: **206 passed**, including **35 new regressions**. Full production qualification remains **blocked by a pre-existing Runtime authentication gap for whole multi-step inverses**. No authorization check was bypassed or weakened.

## Exact source and repair

- Worker/worktree: `agt-R2-split-inverse-0826`, `/home/user/work/wt/agt-R2-split-inverse-0826`.
- Base: `b8e5076250cc37cadf88c1ce699f2a05511fb909` (`tl/agt-R1-sequential-mirror-0811`). No Git writes, fetch, commit, merge, checkout, reset, branch/ref deletion, or push were performed.
- Runtime checkout used by acceptance and supplemental authentication: `/home/user/work/runtime`, observed HEAD `eb13b2051d4d30a4d8b7df8878bb7451701eab5a`.
- Product diff: **five added lines**, only `astrid/sdk/timeline/inverse.py`. `_restore_write` synchronizes existing mirrors after each native `parent/clip:` restoration; the scratch reverse-write validation loop synchronizes at the same boundary before checking the next authored write.
- New main-suite file: `tests/editing_conformance/test_inverse_clip_mirrors.py` (35 collected cases). No existing tests, fixtures, assertions, baselines, clients, schemas, generated artifacts, dependencies, pins, Runtime, App, Proof, or recorder implementation changed.
- Final SHA-256: `inverse.py` = `267b1b1589c0254345a13bf802df8b40301f70020389c223c91f4b14808f336d`; new regression = `7cec273a0fe7bd73be794e11bc54bbd1f222455112bb9b3d87e9e08b4f474b81`.

Read PLAN §3 and the R1 handoff's “Pre-existing inverse limitation” under `$ORCH/design/agent-R1-sequential-mirror-0811.md`. The original `/tmp/w-7886052a6e/base_inverse_probe.py` had been removed; its exact 51-line source was recovered/read from the R1 worker log (around lines 15763–15814). Its source-derived proof concerns the prior integration base, **not upstream main**. No original P1 request, realm, HTTP trace, or fixture was available or modified.

The failing boundary was `apply_inverse`'s per-record scratch guard (`inverse.py:648` before this repair): native leaf reversal restored `hold`/`label` while `config.clips` still held the final storage mirror. The earlier authored aggregate config-list guard correctly refused those mismatched bytes. Calling the existing `Recording.compile_mirrors()` after each restored native clip write fixes the representation at the boundary where the guard executes. Installation uses the same boundary so its derived writes retain the exact reverse chain and original causal attribution. Command-end compilation remains in place.

Aggregate authored guards, landing/coalesced checks, sequential authored execution, equal writes, ABA/history scans, declared dependencies, physical bindings, initial contradictory-mirror validation, and the recorder's `mirrored_clips` eligibility condition are retained. No second executor, reordered user commands, effect suppression, or history rewrite was introduced.

## Main-suite proof

The new tests call the real `create_runtime_commit_service().commit` provider with existing `DetachedRealm`/`DetachedPort` immutable-history/CAS fixtures and existing `timeline.inverse`. These fixtures substitute Runtime ABI exceptions/metadata and in-memory persistence; they do **not** establish live Runtime authorization. Supplemental real authentication below explicitly exposes that limit.

Original split requests include API version, project/timeline, base revision/publication, commands, label, complete step metadata/patch/reads, merge, request reads, context idempotency, dry-run, source, rationale and group. The complete existing shared-child/opaque/app/null/media fixture is retained. The tests check exact canonical documents, unchanged shared closure/manifest, accepted history and original entries, undo step selection, exact sequential native writes, the four derived mirror writes and their complete reverse before/after chain, and exact inverse stage native/effect ranges.

New cases cover:

- `clips` and `config.clips`, output before/after split/list insertion, native leaf transitions, exact whole undo/redo.
- Two-step whole/split-only/note-only undo/redo, retained unrelated state, and immutable original history.
- Split followed by an actual `clip.move` targeting the new right clip; whole and move-only undo/redo.
- Later changed field, equal write, field A→B→A, changed list order, order A→B→A, declared consumer, and same-publication surviving consumer: refusal with unchanged head, entries, documents, prepared candidates and acceptance state.
- Stale-base merged split inverse restores the head where it landed and redoes exactly. The existing detached fixture's historical `rebased` reply spelling is asserted without changing reply behavior.
- Missing accepted history, commands, or selected-step history: `history_unavailable`, with no writes.

The unchanged `test_doc_patch_mirrors.py` also proves initial contradictory mirrors still refuse, malformed original operands/order/reads refuse, and stale same-field conflicts persist.

Failing-before command, before the five-line product edit, exit **1**, **4 failed in 2.31s**; all four positive spellings/orders failed at the existing aggregate reverse guard:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_inverse_clip_mirrors.py
```

After the repair, those same four positive cases passed (**4 passed in 2.26s**). During new-test development, the initial boundary assertion omitted the provider's existing `effect_range`; the assertion was corrected to require its exact `[0, 2]` value. An exploratory negative that removed only `doc.patch` annotations still allowed native parent reversal; such removal does not establish missing native history, so the final unavailable-history tests remove actual commands/history/steps. No original passing behavior expectation was changed. Intermediate runs were **1 failed, 32 passed** and **1 failed, 203 passed** at that new exploratory negative; after correction the 33-case focused run passed. Two further focused cases brought the final count to 35.

Final requested targeted acceptance, exit **0**, **206 passed in 26.33s**:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_doc_patch_mirrors.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py tests/sdk/test_timeline_inverse_binding.py tests/editing_conformance/test_inverse_clip_mirrors.py
```

Exact collection command, exit **0**, **206 tests collected in 1.78s**:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --collect-only tests/editing_conformance/test_doc_patch_mirrors.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py tests/sdk/test_timeline_inverse_binding.py tests/editing_conformance/test_inverse_clip_mirrors.py > /tmp/w-05c53d40b2/collection.txt
```

All exact node IDs were inspected and retained in `/tmp/w-05c53d40b2/collection.txt`. Per-file counts:

| File | Count |
| --- | ---: |
| `test_doc_patch_mirrors.py` | 13 |
| `test_inverse_clear_batches.py` | 101 |
| `test_step_undo_v2.py` | 35 |
| `test_provider_step_undo_v2.py` | 18 |
| `test_timeline_inverse_binding.py` | 4 |
| `test_inverse_clip_mirrors.py` | 35 |
| Total | 206 |

The new collected function names/counts are `test_split_leaf_output_undo_redo_exact_document_and_causal_records` (4), `test_split_step_undo_retains_other_step_and_redoes_exactly` (12), `test_split_then_native_leaf_command_restores_each_command_boundary` (2), `test_later_clip_writes_order_aba_and_consumers_refuse_without_writes` (12), `test_same_publication_surviving_declared_consumer_blocks_split_step` (1), `test_merged_split_inverse_restores_landing_head_and_redoes_exactly` (1), and `test_unprovable_split_history_refuses_without_writes` (3). No skips or xfails were added.

## Lint, types and artifacts

All final commands below exit **0**:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/inverse.py tests/editing_conformance/test_inverse_clip_mirrors.py
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-05c53d40b2/ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-05c53d40b2/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Exact results: scoped Ruff `All checks passed!`; baseline Ruff `current=2149 baseline=2149`, no regression; Mypy `current=1912 baseline=1912`; `ok runtime.lock.json`; `artifacts.json is current`; empty diff-check output. No budget changed.

The harness's named `workers/.../tmpdir` is a **text pointer file** containing `/tmp/w-05c53d40b2`, rather than a directory. The first scratch write failed with a path error; the first Ruff baseline command using the literal pointer path exited 2 (`Not a directory`), and Mypy ran without a usable cache at that path. Reading the pointer and rerunning with its actual private target resolved this. These were filesystem path errors, not safety/approval denials. Shared dependencies/caches were not modified.

## Real Runtime authentication and unresolved authority

Supplemental diagnostic command (not a main-suite test and not live store/HTTP proof):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python /tmp/w-05c53d40b2/auth_probe.py > /tmp/w-05c53d40b2/auth_probe.log
```

The script captures actual provider-prepared candidates from the positive new regressions, restores the fixture ABI shim, then calls the real `/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py:validate` against complete request/input/base documents. **53 candidates pass; 5 fail**. Final script exits **1** to preserve that failure. Raw failures, annotations, and summary are retained at `/tmp/w-05c53d40b2/auth_probe.log`, `auth_failure.json`, and `auth_summary.json`.

All four single-step split requests, their exact undo/redo, selected split/note/move undo/redo, and the merged split path pass real annotation authentication. The five failing candidates are whole multi-step undo: four alias/order variants of split + unrelated note, and whole split + native move. Each fails `invalid_records` / `provider binding differs from its authenticated input image`.

The provider retains ordered inverse stages and intermediate full-image effect bindings. In the native case, move-stage effects cover `[0, 2]` and split-stage effects `[2, 4]` inside the enclosing `edit` step. Runtime `timeline_commit_auth.py:357-367` checks every effect's `before` binding against that enclosing step's single input and every `after` against its final output; it does not consume inverse-stage effect ranges. Its full-image digest/revision check at lines 388–391 rejects the first intermediate `after` annotation. For split + note this is `unknown.note`; for split + move it is `config.clips/id:clip-right/app/astrid`.

Pre-existing control, exit **0** with the expected explicit rejection diagnostic:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python /tmp/w-05c53d40b2/base_auth_probe.py
```

This loads exact `git show b8e507625:astrid/sdk/timeline/inverse.py` into an isolated in-process namespace and temporarily binds that unchanged function. It commits **only two disjoint unknown-field patches**, then whole-undoes them exactly through the provider. Forward real Runtime authentication passes; unchanged-base inverse real authentication rejects the intermediate `commit.effect after` at `unknown.two` with the identical message. Its annotation names intermediate revision `authoring-parent-revision-372b4253e16db9ce82f098c86278875ed07a5a979b7ef6e24320957374cacf9d`, while Runtime expects final `parent-1`. This is source-derived prior-integration proof, not an upstream-baseline or live production claim.

Runtime's multi-stage authentication support is outside this task's allowed files. Rewriting stage provenance, coalescing away effects, inventing a weaker guard, or bypassing Runtime authorization would violate the brief. No such workaround was attempted. Therefore the bounded inverse repair is ready for review/home queue, but **full whole-multi-step R2 integration qualification is blocked** pending a Runtime-owned repair and integrated proof. No production whole multi-step acceptance is claimed.

## Review, decisions and next steps

Independent Luna read-only review **PASS**, no correctness blocker in the five-line Agent repair or regressions. A follow-up independent review confirmed the Runtime intermediate-boundary mismatch and its authorization implications. Its initial coverage note about contradictory mirrors is covered by the unchanged requested R1 regression, which passed in the 206-test run.

No settled PLAN decision was changed. The only implementation choice was synchronizing existing mirrors at restored native-write boundaries in both scratch and installation, preserving the authored/derived distinction. The decision to stop at the Runtime seam follows the explicit file/scope restriction and prohibition on weakening authentication.

Recommended next steps: Runtime owner repairs authentication of intermediate inverse-stage images while retaining exact causal effect ranges/bindings; Agent home queue merges only this worker's own delta after R1's home merge, then runs integrated targeted proof. Recheck the 58-candidate auth matrix after the Runtime fix. Harness owns the commit; conventional message naming R2 is written. `BLOCKED` records the remaining integration authority gap; no `DONE` is claimed for full qualification.

No full suite, test-service request, original P1, P4 HTTP, native14, crash24, browser duplicate, live socket, or original lost-ACK/restart journey was run. Home merge/integrated-head proof and original P1 remain unverified. C0 request/reply/preview/error behavior is unchanged; no new broad contract qualification is claimed.
