# Native sheet omission review

**APPROVE — bounded to the committed parent-clip omission slice.** This is an independent read-only review; no Agent source, integration worktree, branch, dependency, or fixture was changed. The existing detached legacy omission consumer remains in place, so this report does not claim AG03 or the legacy writer deleted.

## Exact identities

| Item | Identity |
|---|---|
| Candidate Agent commit | `b24144d9759641980c0d072ddaa80373733d7308` |
| Candidate Agent tree | `0aa7cb3288564f70e1689266b9c9289c23cab4c1` |
| Actual current Runtime | commit `c45cbc6ba3772ac2cebb5a5c94f91be24231e2d5`, tree `c431abc5025bcadae5355da8229289af797187ec` |
| Central profile | `/home/user/work/venv-agent/bin/python`, Python `3.13.16`, pytest `9.0.2`, Node `v20.19.4`; `ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-current`; `ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages` |

## Decision and source review

`NativeSheet.preview` compares the retained export's bound `# ref` keys. It permits omission only for an original `clips` row whose binding is `parent/clip:<id>`; it does not infer by display name or row order. Additions, track/occurrence omissions, and section rebinding are refused before `commit_many`. The omitted row is captured with the existing `capture_clip_delete`, executed against the working bundle, and sent through the normal `TimelineSession.commit_many` outbox. No three-way merge, second writer, new operation, schema, DTO, route, or legacy writer bypass was added.

The focused tests preserve an unrelated sibling's opaque fields, authored collection order and track state; verify the original pinned basis; exercise lost acknowledgement, restart, changed-key refusal, exact retry body and no recapture; prove disjoint-row rebase; and prove touched-membership conflict leaves the accepted document unchanged. The CLI test uses the actual native export/apply entrypoint and checks delete plus inverse. Existing positive ordinary sheet tests remain intact. The detached `apply_sheet`/`_apply_parsed` omission path is still present and was not represented as deleted.

## Evidence

Local focused candidate tests:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_sheet_native.py::test_omitting_native_clip_row_deletes_exact_bound_clip_and_preserves_sibling_state \
  tests/sdk/test_timeline_sheet_native.py::test_omitted_native_clip_row_uses_normal_commit_retry_undo_redo_and_rebases \
  tests/sdk/test_timeline_sheet_native.py::test_omitted_native_clip_row_rebases_over_unrelated_row_edit \
  tests/sdk/test_timeline_sheet_native.py::test_omitted_native_clip_row_refuses_membership_change_without_accepting \
  tests/packs/timeline/test_cli_native_sheet.py::test_clip_row_omission_is_native_delete_and_keeps_other_rows
5 passed in 3.87s
```

Central actual-current HTTP qualification, source tree `0aa7cb3288564f70e1689266b9c9289c23cab4c1`:

- Exact marked command executed by request `agt-review-native-sheet-delete-live-commit-integration-1020145324-29338`:

  ```text
  env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/editing_conformance/test_native_sheet_current_runtime.py tests/editing_conformance/test_native_sheet_ordinary_runtime.py tests/editing_conformance/test_native_sheet_current.py
  ```

- `agt-review-native-sheet-delete-live-commit-integration-1020145324-29338`: **19 passed, 38 deselected**, exit 0. This used the marked `commit-integration` command with `tests/editing_conformance/test_native_sheet_current_runtime.py`, `test_native_sheet_ordinary_runtime.py`, and the original `test_native_sheet_current.py` neighbor. All 9 native-sheet HTTP nodes (5 current, 4 ordinary) ran; the extra 10 passed nodes are the suite's existing M1 integration file.
- Exact no-filter command executed by request `agt-review-native-sheet-delete-live-native-script-current-integration-1020145219-8390`:

  ```text
  env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/usr/local/bin:/usr/bin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-current ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-current/node_modules /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_native_sheet_current_runtime.py tests/editing_conformance/test_native_sheet_current.py
  ```

- `agt-review-native-sheet-delete-live-native-script-current-integration-1020145219-8390`: **43 passed**, exit 0. This used the new no-`-m` current-profile lane and ran the current HTTP file plus the original current neighbor, including unmarked tests.

The earlier incomplete request `agt-review-native-sheet-delete-live-commit-integration-1020145217-22186` also passed 15/15 but omitted the ordinary runtime file; it is superseded by the corrected request above and is not the gate result.

Additional read-only checks:

```text
git diff --check HEAD^ HEAD                         # passed
git status --short --branch                         # clean
```

## Gaps and scope

The current HTTP files qualify the real export/commit/reload/undo/redo/retry transport path for ordinary native-sheet edits, but they do not contain an omission-specific Runtime HTTP case. The omission-specific exact-delete, disjoint-rebase, membership-conflict/no-accepted-write, and retry assertions are therefore source-level/fake-client evidence, not a claim that a live HTTP omission test ran. No new test or matrix was added under the review brief. A future small test may close that transport-specific gap if the orchestrator requires deletion itself to be exercised through the HTTP fixture.

No full or `full*` suite was requested. No App/browser, renderer, macOS, or legacy-writer deletion qualification was performed or claimed.
