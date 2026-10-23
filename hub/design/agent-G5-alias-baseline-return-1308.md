# G5 occurrence-local test migration — baseline return 1308

**DRAFT ONLY. Source is ready for an owner-bound first-acceptance/dry-run witness. Combined whole undo remains an unresolved Runtime dependency; P1 remains NO-GO.** No integration merge, central original-body request, full suite, daemon, browser, socket, or unchanged whole-undo retry was performed.

Read PLAN.md, G5 1225, A3 source-baseline 1232, independent baseline review 1246, and R2 fork/emitter inverse diagnosis 1246. The independently reviewed retained-source baseline is imported exactly; no new production fix or guard change was made.

## Exact imports and draft identity

Base HEAD remains `6120c25492574353ac12279f184b2355b53c4828`, tree `3ed568fbd57a7732712bdd3558edc6f5ba008282`. No Git mutation was performed. The harness must assign the final commit SHA; it is not available during this worker turn.

Exactly three complete blobs were read from `bfcf78db998868e4a7d92779a83cd3aaba82a98a` and written byte-for-byte into the draft:

| Path | Git blob | SHA-256 |
| --- | --- | --- |
| `astrid/core/timeline/authoring_bundle.py` | `c00323f0755d2d6b2409df952a61c9e154c85d95` | `c10f47a7f3caf42db2060c9b146a95aafc21bd8740823b074a60085f0bfa7c59` |
| `astrid/sdk/timeline/native_occurrence_duplicate.py` | `4338045a2272765dd1e35ff17bbca357ccc4fe04` | `f2936a59859e2069169b6371669e2faf2cdc6def3a2c067a8bf08fa452986f86` |
| `tests/editing_conformance/test_occurrence_fork_source_baseline.py` | `dad27a538885ab45dd03242ee1670e00ff615dd3` | `cd921e3ff19d694c16bae2d7b647d2df10fbbcab1fa7ddc9ade473003f3c9ad0` |

Only `tests/editing_conformance/test_native_sheet_current_runtime.py` changes beyond those imports. Its final Git blob is `0a23991cb98ce270da7c6bb7bdd9ec73e2ff402e`; SHA-256 is `2dd71d0be3d2f455427de6f96f8926a9d0095d2dd244a5426e9367a598e697c4`.

The prospective source tree is `48e3c3facecda7adb51c9b6e9ba3cc10da6f0666`. This was computed read-only from HEAD's recursive tree with those four file updates, using Git's tree object encoding; the same calculation first reproduced HEAD's tree exactly. No tree object or index was written. Identities are also retained in `/tmp/w-97ddd96ac5/identities.json`.

Runtime stayed clean at `/home/user/work/wt/rt-pin-3b926efa`: commit `3b926efab2eed122d374540baee297d4cdcec62a`, tree `b794170504544b259781e50d7ca4d61b6729e67c`. No Runtime, schema, generated client, contract, dependency, pin, fixture JSON or artifact change. No ancestry import. R1 `dcb4cee322` was **not** imported: pure preparation of this exact three-command batch demonstrates an atomic `timeline` scope on every step already, so no missing-scope dependency was established.

## Test change and assertion mapping

The test captures the registered `occurrence.fork` from the authenticated original bundle, projects its normal document through `document_from_bundle`/`bundle_from_document`, and emits against that unique selected physical source. It submits fork + both emitted patches in **one original transaction**. It does not broadcast alias edits, write managed edges, fabricate pins/private caches, or inject recorder authority.

The seed helper was renamed from `seed_emitter_parent` to `seed_document_diff_parent` without changing its body. The exact approved regression imports the latter name; restoring that name keeps the imported blob unchanged. No other test caller uses the former name.

| Requirement | Source assertion in final target file |
| --- | --- |
| Authenticated exact base pair, public/private closure separation and digest | Lines 269–296, plus submitted base pair checks at 373–374 |
| Registered selected fork; normal projection; explicit occurrence addressing | Lines 299–307 |
| Malformed `params.text=None`; exact raw guarded patch; provider code/path/hint; unchanged head/history and one request | Lines 309–336; fork and invalid patch are submitted together |
| Parent/child hold absence, removed text, raw `from`/`to`, parent track label | Exact four emitted changes at 351–363; accepted values at 385–390 |
| Full command capture and complete v2 history recorder equality | Lines 364–375 and 413–417 |
| Full canonical document and persisted bundle equality | Lines 377–382 |
| Opaque/null-bearing source retention | Explicit opaque assertions at 388–390; full original shot/internal image membership at 401–403 |
| Fresh target shot/revision/internal pin and exact unchanged sibling pin/entity | Lines 391–400 |
| Placement order, track, placement, speed, duration, source offset | Lines 404–411 |
| Restart/reload, exact persisted closure and target pin | Lines 419–427 |
| Original undo restoration and redo canonical equality | Lines 429–436 (positive expectations retained; not executed here) |

The original full recorder equality is retained against a pure execution of the actual submitted v2 request and authenticated evaluation pair. It no longer compares a metadata-free native capture against a v2 history record. The commands themselves are captured through the same existing engine before submission, preserving exact command equality assertions.

An initial **pure**, non-service preparation using the unlabeled mixed default step raised `CommandError: semantic step assertion differs from execution`. The existing `commit_many(label=...)` API already generates per-command steps. Both positive and malformed calls now use that API; no production change, synthetic reads, alternate executor, or weakened assertion was introduced. Repeating only the pure preparation with those actual generated step shapes passed: original four changes, stable recapture, atomic timeline scope on every step, complete unchanged sibling images, selected absence/parameter edit. Supplemental result is `/tmp/w-97ddd96ac5/pure-forward.log`; this is preparation evidence, not Runtime acceptance of the original body.

All nine neighboring test functions (18 parameterized cases) are AST-identical to the base. All 19 Runtime cases and all 33 unchanged authoring-feedback cases collect. Authoring-feedback SHA-256 remains `37ce863249b1cd375064b2297756c4ed0577a9dcd4d74606ae59098a0d95f2e5`. No test was skipped, xfailed, removed or converted from success to refusal.

## Exact commands and results

Commands ran from `/home/user/work/wt/agt-G5-alias-baseline-return-1308`. The harness's `tmpdir` is a pointer file containing `/tmp/w-97ddd96ac5`; scratch and caches used that private directory. Shared dependencies were read-only.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa TMPDIR=/tmp/w-97ddd96ac5 timeout 30 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-97ddd96ac5/final-author tests/timeline/test_authoring_feedback.py
# 33 passed in 3.51s; exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa TMPDIR=/tmp/w-97ddd96ac5 timeout 30 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py
# 52 tests collected in 3.70s; exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa TMPDIR=/tmp/w-97ddd96ac5 timeout 30 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-97ddd96ac5/controls -m 'not integration' tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/editing_conformance/test_native_sheet_ordinary.py tests/sdk/test_timeline_sheet_native.py
# 151 passed, 1 deselected in 17.07s; exit 0 (135 existing controls + 16 new offline cases)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa TMPDIR=/tmp/w-97ddd96ac5 timeout 30 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-97ddd96ac5/source-positive tests/editing_conformance/test_occurrence_fork_source_baseline.py::test_current_runtime_retained_fork_then_emitter
# 1 passed in 4.28s; exit 0

/home/user/work/venv-agent/bin/ruff check --no-cache astrid/core/timeline/authoring_bundle.py astrid/sdk/timeline/native_occurrence_duplicate.py tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_native_sheet_current_runtime.py
# All checks passed; exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --cache-dir=/tmp/w-97ddd96ac5/final-mypy --follow-imports=silent astrid/core/timeline/authoring_bundle.py astrid/sdk/timeline/native_occurrence_duplicate.py tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_native_sheet_current_runtime.py
# Success: no issues found in 4 source files; exit 0

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# artifacts.json is current; exit 0
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
# ok runtime.lock.json (matches producer manifest); exit 0
git diff --check
# PASS; exit 0
```

The one new-source positive is the **unchanged approved source-baseline regression**, using the real startup-loaded provider and in-process RuntimeService, without sockets. It confirms projection, preview/no-write, actual acceptance and sibling closure retention. Its edit is only the child text removal, with its existing explicit reads/steps. It is not a witness of this draft's original four-change HTTP body, malformed HTTP refusal, history equality, reload or combined inverse. It ran before final target-only labeling/recorder expectation changes; its imported three blobs and seed helper body are unchanged afterward. No second service positive or whole-undo execution was run.

## Owner harness rebind and unresolved dependency

Please have the owner harness bind a **new** wrapper identity to the harness-created commit SHA whose tree is `48e3c3facecda7adb51c9b6e9ba3cc10da6f0666`, target file SHA-256 `2dd71d0be3d2f455427de6f96f8926a9d0095d2dd244a5426e9367a598e697c4`, and exact node:

`tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_emitter_null_presence_and_track_roundtrip_is_authenticated`

Target function source SHA-256 is `f4386ff9b454dab1de9f70c5e9f9ec9cd1d7ca7a7353adf1fdbda0084c17c0e5` (UTF-8 complete function lines, including final newline). This is source identification, not independent review/qualification. The existing `g5-emitter-current-runtime-nodes` route still binds the old source; neither its wrapper nor its suite row/prepared replies were edited. No request was submitted against that stale binding. The final commit SHA must be supplied by the harness, never substituted with the unchanged base HEAD.

The existing Runtime owner still needs to address the authenticated leaf physical-turnover inverse boundary documented in `design/agent-R2-fork-emitter-undo-diagnosis-1246.md`. Keep the positive original undo/redo assertions. Arrange any first-acceptance/dry-run witness through the owner-approved binding; defer a repeated whole-undo journey until that dependency meaningfully changes. The source migration is prepared, not qualified for integration, and does not establish merged/conflict or P1 acceptance. No blocker prevented this scoped draft preparation.
