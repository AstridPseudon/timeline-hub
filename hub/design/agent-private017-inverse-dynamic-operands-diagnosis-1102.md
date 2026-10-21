# PRIVATE017 ordered12634 inverse refusal: Agent mutation identified and fixed

Date: 2026-10-21 UTC. Worker: `agt-m2-private017-inverse-dynamic-operands-diagnosis-1102`.

## Disposition and source

**Agent-owned defect, reproduced with the exact refusal in a fresh source-created namespace.**
The 1050 HOLD report's static retrieval comparison is correct at retrieval time, but its
Runtime-owned disposition is contradicted by the dynamic operand capture below. Agent inverse
scratch staging subsequently mutates the retrieved record. No Runtime persistence change is
needed to explain this refusal.

- Worktree: `/home/user/work/wt/agt-m2-private017-inverse-dynamic-operands-diagnosis-1102`.
- Base commit: `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`.
- Base tree: `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`.
- Final source tree: `a6126ed13a7b4dad8124894ebced1cf1b5977d5f`.
  Computed read-only using Git object hashing over tracked files plus the new test;
  the same algorithm first reproduced the base tree. No index/object/ref writes or commit.
- Read-only Runtime import source `/home/user/work/runtime` observed at
  `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`. The reproduction uses the detached
  provider port, not a running Runtime.

Only three repository files changed: one product line in
`astrid/sdk/timeline/_command_state.py`, two immutability assertions/setup lines in
`tests/editing_conformance/test_recipe_m2_project_data.py`, and the 39-line
`tests/editing_conformance/test_project_data_accepted_inverse.py`.

## Actual fresh reproduction and live call sequence

The existing `DetachedRealm` runs real native command execution, provider reconstruction and
acceptance CAS; only the Runtime ABI exceptions/metadata are stubbed by its existing fixture.
The test starts from `document_fixture()`, accepts a three-command `project-data.write` batch
creating namespaces in order `before`, `com.example.compiler-canary`, `after`, then accepts
removal of the middle namespace's sole key `gone=False`, then submits `timeline.inverse`
targeting that accepted removal. No accepted history/records were invented, imported or edited.
Every history/revision read returns detached JSON through the existing port.

The native removal produces these exact writes:

```json
[
  {"ref":"parent","path":["config","app","com.example.compiler-canary","gone"],
   "before":{"state":"present","value":false},"after":{"state":"absent"}},
  {"ref":"parent","path":["config","app","com.example.compiler-canary"],
   "before":{"state":"present","value":{}},"after":{"state":"absent"},
   "insertion_order":["before","com.example.compiler-canary","after"]}
]
```

Live callers, with line numbers on this base/final source (the product fix changes no line count):

1. `DetachedRealm.call()` (`tests/sdk/test_timeline_commit_provider.py:101-103`) calls
   `create_runtime_commit_service().commit(context, DetachedPort(...))`.
   The service's preliminary migration check retrieves records at `commit.py:976`.
   It loads the base, head, target history, ancestry and exact before/after boundaries.
2. `commit.py:1047-1048` constructs `AcceptedRecords(accepted, _records(...), load_boundary)`.
   `_records()` (`613-628`) deep-copies the accepted command list. Both operands are equal here.
   The captured four `_records()` returns are the preliminary migration read, the inverse
   accepted read, the per-target suffix-check read, and its empty intervening suffix.
   `check_intervening()` (`1054-1058`) validates that suffix before reversal.
3. The provider collects source closures and authenticated inverse replacement pins,
   calls `_hydrate()` (`1105-1106`, including `coalesce()`), builds `_schema_resolver()`
   (`1107-1108`), and calls `commands.execute()` (`1109-1113`). Both operands are still
   equal at execution entry. There are no document/schema source pins for this command.
4. `commands.execute()` deep-copies the candidate bundle, consumes inverse materialization
   context, creates `Recording`, verifies claims, runs the resolver, and calls
   `apply_inverse()` at `commands.py:309`. Both operands are equal at inverse entry.
5. `apply_inverse()` (`inverse.py:449-465`) checks intervening and prior staged writes,
   coalesces copies of changes, captures the immutable input, checks order/value guards,
   and constructs a deep-copied scratch bundle. It then reverses the original accepted
   record's writes (`473-490`), passing each original `write['before']` into
   `_set_recorded()` (`100-102`) and then `State.set()`.
6. The first scratch assignment restores the empty namespace with `insertion_order`.
   `State.set()` first deep-copies the incoming value (`_command_state.py:563`), but the
   ordering reconstruction previously overwrote that detached copy with the raw
   `state['value']` (`582`), installing it at `584`. The scratch namespace and
   `records[0]['writes'][1]['before']['value']` are now the **same mutable dictionary**.
   Both operands still compare equal because that dictionary remains empty.
7. The next scratch assignment restores `gone=False` within that namespace at
   `_command_state.py:563`, via `inverse.py:490 -> _set_recorded():101 -> State.set()`.
   **This is the first operand change.** It also inserts `gone` into the accepted-record
   copy through the alias. The right operand, the port-returned accepted history entry,
   remains unchanged. The captured stack identifies this scratch call, before public
   inverse installation or any publication/reconstruction.
8. Scratch mirror/input checks complete, public reversal installs coalesced copies,
   and execute finishes its input/mirror/materialization/record validation. The changed
   inverse input survives both `apply_inverse()` and `execute()` returns.
9. At the unchanged head the provider selects `original`, checks reservations, and calls
   `document_from_bundle()` (`commit.py:1141-1142`). Conversion compiles the candidate,
   selects historical identities, handles transcript/document pins, and calls
   `_inverse_media_removals()` at `362`. Its equality guard (`181-183`) sees the changed
   left operand and raises exactly **`media inverse records differ from accepted history`**.
   There is no intervening Runtime accept/retry or history rewrite.

## Before/after operand evidence

First differing path: **`[0].writes[1].before.value.gone`**.

| Capture point | Left namespace `before.value` | Right namespace `before.value` | Equal |
| --- | --- | --- | --- |
| Retrieval / execute entry / inverse entry | `{}` | `{}` | yes |
| Scratch namespace restoration, after `State.set()` | `{}` | `{}` | yes; mutable alias installed |
| Scratch leaf restoration, before `State.set()` | `{}` | `{}` | yes |
| Scratch leaf restoration, after `State.set()` | `{"gone": false}` | `{}` | **no** |
| Inverse return / execute return / media guard entry | `{"gone": false}` | `{}` | **no** |
| Same stages after fix | `{}` | `{}` | **yes throughout** |

On the left the new member is present, type `bool`, value `False`; on the right it is
absent. Both parent values remain dictionaries. The record/write/path list orders,
tagged presence states, command claims and optional `insertion_order` member are unchanged.
This is neither member-order equality nor a lost carrier. Persistent `realm.entries`
remain unchanged even when the original inverse refuses.

Full unfiltered operands, before/after each observed inverse/staging call and guard,
including stacks and an identity check for the restored namespace, are retained at:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-private017-inverse-dynamic-operands-diagnosis-1102/operands-before-fix.json`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-private017-inverse-dynamic-operands-diagnosis-1102/operands-after-fix.json`
- Reproducer: same worker directory, `test_diagnose.py`.
- Source hashes: same worker directory, `source-identity.json`.

## Fix and regression

At `_command_state.py:582`, copy the incoming value during ordered reconstruction,
just as the ordinary assignment at `563` already does. The mutable namespace identity
check changes from true to false, and subsequent scratch leaf restoration no longer
changes either operand. This preserves all fields, optional order metadata, identities
and guard semantics. No media exemption, field normalization or history repair.

The existing reload/order roundtrip test now asserts its input records stay unchanged.
The new provider test creates its namespace through native commands, removes it, and
undoes/redoes/undoes through real reconstruction and the accepted-record equality guard.
Each step checks the exact canonical document, namespace order and prior accepted history.
Both regressions failed before the product fix and passed afterward.

## Exact commands and results

All commands below ran from the assigned worktree. No full suite or central suite was requested.

Red-to-green regression command:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --tb=short tests/editing_conformance/test_recipe_m2_project_data.py::test_remove_pruned_namespace_restores_exact_order_after_reload_and_redo tests/editing_conformance/test_project_data_accepted_inverse.py
```

Before fix: **2 failed in 1.48s**, record immutability assertion and exact media/history
refusal respectively. After fix: **2 passed in 1.28s**.

Operand capture command before fix:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" DIAG_OUTPUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-private017-inverse-dynamic-operands-diagnosis-1102/operands-before-fix.json /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-private017-inverse-dynamic-operands-diagnosis-1102/test_diagnose.py
```

Result: **1 failed in 1.40s**, exact refusal reproduced. Repeating that command after
the fix with `DIAG_OUTPUT=.../operands-after-fix.json`: **1 passed in 1.11s**.
Both external diagnostic invocations report one existing unknown `integration` mark
warning because they run outside the repository's pytest configuration root.

Targeted neighboring lanes:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_project_data.py tests/editing_conformance/test_project_data_accepted_inverse.py tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_grouped_clip_cache_inverse.py tests/editing_conformance/test_occurrence_media_manifest_inverse.py tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_materialization_version_boundary.py tests/editing_conformance/test_materialization_map.py tests/sdk/test_timeline_commit_provider.py
```

Result: **560 passed, 1 failed in 53.90s**. The only failure was
`test_move_reload_and_inverse_import_no_renderer`: its subprocess calls the Runtime
locator, which lacked `ASTRID_RUNTIME_CHECKOUT`. No product assertion failed there.
Reran only that failing test with the required source locator:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer
```

Result: **1 passed in 1.65s**. Thus all **561 selected tests** have passing evidence.
These lanes retain staged inverse/ABA refusals, source/media/owner safety, optional
order/absent-key behavior and accepted private-v1 inverse/redo/restore compatibility.
Real Runtime ledger-first accepted-v1 retry is unmodified but was not rerun.

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_command_state.py tests/editing_conformance/test_project_data_accepted_inverse.py tests/editing_conformance/test_recipe_m2_project_data.py
git diff --check
```

Results: **All checks passed**; diff check **exit 0**.

## Decisions, limits and next step

Chose the single assignment-site deep copy because the ordered setter itself discarded
its ordinary detachment guarantee. Copying at retrieval or exempting non-media inverses
would leave the corrupting primitive in place. No plan/contract decision changed.

No blockers. No original lost-ACK/restart node, native/HTTP/socket/browser suite, full,
outer or render replay ran; no project/artifact, pin, client, shared dependency or other
worktree was changed. The no-renderer unit probe only checks that imports remain absent.

**Recommended next step:** review/integrate this Agent tree, then Runtime performs its
already-owned final qualification of original private017 ordered12634 with the exact
client/source/pin identities preserved. This report establishes the dynamic Agent cause
and fresh red-to-green reproduction; it does not claim that original node is qualified.
