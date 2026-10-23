R1 complete atomic scope union — ready for independent review

The refusal is Agent-owned. The existing complete-JSON script writer emitted an authentic atomic `doc.patch` request, but `CommitPatch.finish()` constructed atomic dependencies before recording authoritative effects/materializations. Runtime's completed-record scope check correctly rejected the incomplete union. This conclusion follows from the prepared records, not the location of the exception.

Agent source base: `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`. Paired Runtime: `/home/user/work/runtime`, clean at `3b926efab2eed122d374540baee297d4cdcec62a` before and after qualification. No integration merge or Git mutation was performed. Read PLAN §3 R1/G3/G4, C0 request/addressing/conflict rules, the full guidance1158 report and donor206d0f8b's three workflow tests. No donor ancestry or guidance changes were imported.

Changed only:

- `astrid/sdk/timeline/_commit_patch.py`: build the batch scope union after effect and materialization bindings exist; retain reads, writes, derived writes and every physical binding in that union. If any step cannot represent that union in its input closure, use the existing conservative timeline fallback for every step. Capture each scope from that step's stored input, with its original base/head/step/ordinal provenance.
- `tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py`: three narrow regressions using the current provider and real in-process Runtime service. The preexisting saved-source fixture supplies immutable setup; every tested edit executes through the real commit service and strict authentication. No replacement executor, fabricated prepared acceptance, journal/cache injection, auth relaxation, `reads: []` workaround or alias retargeting.

The first regression runs the actual complete-JSON script's `check` and `publish` commands. This base names the existing parser `publish`; renaming it belongs to guidance ownership. Its production body calls `TimelineSession.commit_many`, already with exact base pair and atomic mode. The test loads/exports a complete Checkout JSON, adds parent `config.app.astrid.slots = {}` and internal `inside.params.x = 15`, then checks accepted receipt, complete canonical readback, records, input captures, local retry, actual Runtime retry and unchanged history. This reconstructs guidance1158's retained two-change request: one command, one step, six authoritative effects, with no request-level `reads` supplied.

On archived d1fa, the dependencies covered `parent` and `internal-revision:internal-film`; the completed records also touched `shot-revision:shot-film` and both newly materialized child revisions. Exactly those three physical refs were uncovered. With the fix, the conservative timeline dependency and three authentic original input captures cover the completed union. The generated successor IDs differ between independent fixture projects; their physical roles and exact values are retained in the evidence.

The second regression covers a native occurrence deletion followed by a parent patch while another physical shot/internal pair survives. This independently exposes the batch fallback requirement: the later step's timeline capture introduces surviving roots into the final batch touched union; d1fa's earlier step lacks those two scopes. Applying the fallback to every step closes the union. It preserves the untouched physical images exactly. The third regression verifies two sequential patch steps, a step read of the preceding name edit, input digests at each step, source/rationale/group ID, preview without durable changes, real acceptance and exact retry.

A separate exploratory `doc.patch` membership-deletion probe was correctly refused with `closure membership and edges require semantic commands` (`evidence/removed.log`). The supported removal regression uses the existing native occurrence-delete command. No managed-edge guard was changed.

Durable evidence is under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-atomic-scope-1216/evidence`

- `red/auth-1.json`, `red-exact.log`: authentic complete-JSON request and current-base refusal. Includes request, prepared records, input/source/base canonical documents, output canonical document, steps, dependencies, effects, physical bindings, history argument and module origins.
- `red-removed-root/auth-1.json`, `red-removed-root.log`: independent d1fa sequential-removal RED, with the same retained facts.
- `green/auth-1.json`: script acceptance; `green/auth-11.json`: removal acceptance; `green/auth-16.json`: sequential preview; `green/auth-17.json`: sequential acceptance. Other `green/auth-*.json` retain authentic lookup/history/retry validations. `green/history-*.json` retain readback history, including receipts and complete records.
- `scope-classification.json`: exact requests, touched physical refs, dependencies/effects and uncovered scopes calculated using the pinned Runtime's own `images`, `native_site` and `covers` functions. Every final GREEN step has zero uncovered scopes.
- `provenance.json`: exact heads, module-file hashes and final changed-source hashes. Auth snapshots name actual Agent and Runtime module origins. `production.diff`, source/test copies, `atomic_evidence.py` and `inspect_evidence.py` make the retained investigation reviewable. The evidence plugin copies arguments and forwards unchanged to the original Runtime validator; plain final tests also pass without it.
- Gate logs and raw Ruff/mypy base/current output; identity summaries show zero additions and zero removals, ignoring source line movement.

Exact successful commands (all run from the assigned Agent worktree unless a different cwd is stated):

```sh
W=/home/user/work/wt/agt-R1-atomic-scope-1216
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
E=$O/workers/agt-R1-atomic-scope-1216/evidence
T=/tmp/w-c6d28215e6
PY=/home/user/work/venv-agent/bin/python

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= $PY -m pytest -q -o addopts= -p no:cacheprovider --basetemp=$T/plain-final tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py
# 3 passed in 4.05s; plain-final.log

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= $PY -m pytest -q -o addopts= -p no:cacheprovider --basetemp=$T/final-impacted tests/editing_conformance/test_doc_patch_v2.py tests/editing_conformance/test_doc_patch_mirrors.py tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/sdk/test_timeline_commit_v2_errors.py
# 211 passed in 22.43s; final-impacted.log
# Includes original atomic fallback/explicit refusals, outside-closure read,
# forged native captures, membership/order/previous-value checks, later-head
# and dependency writes, same-value/ABA, no-write errors, step reads and undo.

# cwd /home/user/work/runtime; strict existing rejection tests only:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/runtime:/home/user/work/runtime/tests PYTEST_ADDOPTS= $PY -m pytest -q -o addopts= -p no:cacheprovider --basetemp=$T/strict-auth-agent tests/test_timeline_commit_authentication.py -k 'forged_provider_records_are_rejected_without_writes or read_claims_are_checked_at_input_and_in_dependency_union'
# 32 passed, 41 deselected in 26.65s; strict-auth.log
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/runtime:/home/user/work/runtime/tests PYTEST_ADDOPTS= $PY -m pytest -q -o addopts= -p no:cacheprovider --basetemp=$T/atomic-omission 'tests/test_timeline_commit_authentication.py::test_atomic_mode_requires_authoritative_scope_dependencies[True]'
# 1 passed in 1.15s; atomic-omission.log. Existing intentional forged-provider inputs
# are used only to prove rejection, never as positive semantic evidence.

# Agent cwd again:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. RUFF_CACHE_DIR=$T/ruff make ruff PY=$PY
# PASS 2149/2149; ruff-gate.log
RUFF_CACHE_DIR=$T/ruff-current $PY -m ruff check tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py --output-format concise
# PASS, zero findings; ruff-test.log
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=$T/mypy-gate make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python
# PASS 1912/1912; mypy-gate.log

# Run once from archived d1fa cwd $T/base with STATE=base, once from Agent
# worktree with STATE=current. Private caches; raw tools exit 1 on inherited debt:
RUFF_CACHE_DIR=$T/ruff-$STATE $PY -m ruff check astrid scripts/reshape tests/reshape --output-format json
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=$T/mypy-$STATE /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes
# Ruff 2149 -> 2149; mypy 1912 -> 1912 (252 files / 958 checked).
# Exact path/message/code multisets: zero added and zero removed for both.

PYTHONDONTWRITEBYTECODE=1 $PY scripts/artifact_manifest.py --check
PYTHONDONTWRITEBYTECODE=1 $PY scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
git diff --check
git diff --no-index --check /dev/null tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py
# All PASS; artifact.log, vendor.log, diff-check.log.
```

Exact causal/evidence commands:

```sh
# d1fa was read with git archive into private $T/base. Only the NEW regression
# file was copied there, leaving its Agent production code exactly at d1fa.
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$T/base:$T:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ATOMIC_EVIDENCE=$E/red PYTEST_ADDOPTS= $PY -m pytest -q -o addopts= -p no:cacheprovider -p atomic_evidence --rootdir=$T/base --basetemp=$T/red-exact $T/base/tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py
# At that point the file contained only the complete-JSON case:
# 1 failed in 1.95s, exact union-authentication refusal; red-exact.log.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$T/base:$T:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ATOMIC_EVIDENCE=$E/red-removed-root PYTEST_ADDOPTS= $PY -m pytest -q -o addopts= -p no:cacheprovider -p atomic_evidence --rootdir=$T/base --basetemp=$T/red-removed-root $T/base/tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py -k fallback_union
# 1 failed, 2 deselected in 2.66s; same exact refusal.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:$T:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ATOMIC_EVIDENCE=$E/green PYTEST_ADDOPTS= $PY -m pytest -q -o addopts= -p no:cacheprovider -p atomic_evidence --basetemp=$T/final-regression tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py
# 3 passed in 3.69s; green.log. Plain run above independently passes.
PYTHONDONTWRITEBYTECODE=1 $PY $E/inspect_evidence.py
# Produces scope-classification/provenance/diagnostic identities.
```

The full v2 request/reply machinery is retained: exact base pair, commands, label, steps/patch/reads/ordinals, merge, batch reads, key, dry-run, source, rationale and group ID; accepted/merged envelopes and canonical data, records/dependencies/effects, history/undo_steps, preview/would_status and structured conflict/invalid code/path/hint/command. The regressions exercise the concrete acceptance/preview/history paths above; existing impacted tests retain merged, guarded undo, native captures and structured-error coverage. This bounded result is not a new end-to-end qualification of every contract field or deferred proof suite.

No changes to `_doc_patch.py`, checkout, publish, CLI/guidance, sync, Runtime/auth/schema, generated files, pins or contract. No test expectations were weakened, skipped or xfailed. No full suite, live socket/browser/daemon, P1/P2/P3/P4 journey, native14/original58 or D17 duplicate suite was run/requested. Shared dependencies and caches were not modified. One attempted strict-test command found `/home/user/work/venv-runtime/bin/python` absent before running tests; the same targeted Runtime tests passed using the existing Agent dependency environment. No safety/approval denial occurred.

No blocker remains for this source fix. Recommend independent R1 review before any merge; then the guidance owner can rerun its narrow continuation cases on the reviewed fix. This fix independently restores existing production commit behavior and does not clear the G5 deletion/P1 gates.
