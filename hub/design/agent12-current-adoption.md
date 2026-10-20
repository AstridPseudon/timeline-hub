# Agent 0.0.12 current adoption — BLOCKED

Implemented R1 and N1 on the exact starting cohort `ce2510034f3edebef7430dd018c566101ea298fb`. Only two tracked files changed:
- `tests/packs/rendering/test_presenter_scene_capability.py` imports and serializes `astrid.core.theme._schema.BUILTIN_DEFAULT_THEME` beside `query.mjs`, and checks artifact SHA256 with exact equality.
- `tests/packs/rendering/presenter_scene_capability.mjs` parses that serialized value and compares it to the public package `DEFAULT_THEME`. The copied navy expected object is removed. The explicit historical black/Georgia theme and all 286 SSR expectations remain unchanged.

`artifacts.json` was regenerated normally and is byte-unchanged on this starting tree. No SDK/client/schema/fixture files were restored from an older branch. No normal source/PCM activation; no shared dependency files were changed. The temporary worktree-local `remotion/node_modules` symlink used to borrow read-only peers was removed after testing. No commit, push, integration edit, ledger edit, or full suite was performed.

## Merge prerequisite (blocking)

Exact command:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/merge-forward agt-m3-consume12-current
```

Exit 128: `fatal: update_ref failed for ref 'ORIG_HEAD': cannot lock ref 'ORIG_HEAD': Unable to create '/home/user/peteromallet/astrid-agent/.git/worktrees/agt-m3-consume12-current/ORIG_HEAD.lock': Read-only file system`.

No merge began. HEAD remains `ce2510034f3edebef7430dd018c566101ea298fb`; observed current `tl/integration` is `c456b3281497653cecf44f61acd6fa30565d83c8`. The requested descendant does not yet exist. The sandbox cannot complete the prerequisite ancestry operation. Run the authorized helper outside the sandbox, retain these two test corrections, and resume conflict resolution/qualification. No DONE file is claimed.

## Exact tuple and lock identities

- Cohort/base: Agent `ce2510034f3edebef7430dd018c566101ea298fb` (uncommitted R1/N1 corrections awaiting harness commit).
- Required current Agent parent: `c456b3281497653cecf44f61acd6fa30565d83c8` (not merged).
- Required Runtime producer: `94114269d1ce23ab3224d7eca5a85138ce2b5fed`; `/home/user/work/wt/rt-pin-94114269` has that exact HEAD. Current integration already pins it; keep its bytes exactly.
- Composition: `0.0.12`; artifact `remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz`, SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; SRI `sha512-490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==`.
- Exact committed lock: `ce2510034f3edebef7430dd018c566101ea298fb:remotion/package-lock.json` (worktree path `/home/user/work/wt/agt-m3-consume12-current/remotion/package-lock.json`), SHA256 `cca94d49f4bae0b3f16198d70ad08cd963f7d6061554d4276310deb6fe87f597`.
- Shared `/home/user/work/runtimes/agent-remotion-0012/package-lock.json`, SHA256 `783795c9ebfd9fa9c3aa5c4fb3032f134d2f2887cdf342cab676d423319ec11d`.
- The only JSON difference is eight missing `libc` fields in shared runtime optional native dependencies: four `@remotion/compositor-linux-*` and four `@rspack/binding-linux-*` entries. Exact equality holds after stripping those fields from the committed lock. Both package.json hashes equal `58460ce59e2473d74f44238a2e5e78e2d4bd8a79a0bd94e430f7ae5eb6c2778a`. Do not rewrite the committed npm lock to match the shared runtime. Orchestrator owns shared-runtime reprovisioning; readiness itself was not exercised here.

## Tests and checks

Preliminary evidence below is on the corrected cohort, NOT a current-integration descendant.

Local targeted command (after adding a temporary worktree-local symlink from `remotion/node_modules` to `/home/user/work/runtimes/agent-remotion-0012/node_modules`):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_presenter_scene_capability.py tests/packs/rendering/test_presenter_crop_equivalence.py tests/packs/rendering/test_presenter_series_inspection.py tests/packs/rendering/test_presenter_selected_cut_aggregate.py tests/packs/rendering/test_composition_package.py tests/test_artifact_manifest.py
```

Result: **47 passed, 5 tar extraction deprecation warnings, 24.21s**. This includes all integration-marked presenter/package cases and the 286 historical SSR comparisons.

Central named command:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m3-consume12-current remotion-0012-nodes --files 'tests/packs/rendering/test_presenter_scene_capability.py tests/packs/rendering/test_presenter_crop_equivalence.py tests/packs/rendering/test_presenter_series_inspection.py tests/packs/rendering/test_presenter_selected_cut_aggregate.py tests/packs/rendering/test_composition_package.py tests/test_artifact_manifest.py')
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R" 1
```

Result `agt-m3-consume12-current-remotion-0012-nodes-1020092457-1227`: **13 passed, 5 warnings, exit 0**; snapshot tree `dd0659b9df6ce9d1a447a78962d120e0538ebddd` includes the temporary dependency symlink. The named suite inherits pyproject's `not integration` selection, so the 34 integration cases did NOT run centrally. An earlier request `agt-m3-consume12-current-remotion-0012-nodes-1020092420-15148` attempted `--files '-o addopts= ...'` and was rejected with `bad file arg -o`; it ran no tests. The central command needs an orchestrator-owned correction to clear addopts/include integration before qualifying all 47 cases. No tests were skipped/disabled/rewritten to obtain these results.

Other exact commands:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-94114269
```

Manifest regeneration/check: PASS, 162 artifacts, version `sha256:9c6bc05bef1d7a2c4d76ad3dc62e18437e12e9f9df2947798fdd941e1e715a68`; regeneration leaves no diff. Diff whitespace check: PASS. Vendor check on this unmerged worktree: FAIL as expected because its old Runtime pin remains `6be970633cc82ab412428151e6bf42f3e7fc3081`. It reports producer commit/version plus the four changed client files. This is a missing merge prerequisite, not a reason to restore old Runtime files.

Separately, a read-only Python heredoc extracted `runtime.lock.json` and its 15 consumer paths using `git show c456b3281497653cecf44f61acd6fa30565d83c8:<path>` into a temporary worker-local directory and called `scripts.vendor_lock.check(lock, Path('/home/user/work/wt/rt-pin-94114269'), root=temporary_root)`: **PASS**, all 15 paths match the exact producer. The temporary directory was removed. This establishes that integration already has the required pin; it is not final merged-tree qualification.

## Decisions, remaining work, ledger

Kept this a two-file review correction. No plan decision changed. Did not reconstruct a fake merge or copy current SDK files into an unrelated ancestry, and did not edit shared runtime metadata to erase its mismatch.

Required next steps: run merge-forward externally; resolve the documented cohort conflicts while preserving current SDK/fixtures and Runtime 94114269; regenerate artifacts normally; correct the central named lane selection and run all six files on the merged tree; check the final artifact manifest and vendor lock against the exact producer; publish the harness-produced final Agent SHA here. The coordinated adoption tuple and renderer readiness remain unverified.

Required ledger/coordination update (orchestrator only): record R1/N1 implemented with 47-case preliminary local proof, 13-case limited central proof, merge-forward and central integration-selection blockers, and shared Remotion lock reprovisioning outstanding. Do not mark M3/current adoption accepted or normal source/PCM activation complete from this report.
