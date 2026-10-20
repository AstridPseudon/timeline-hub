# Agent 0.0.12 current adoption — qualified source, harness commit pending

Supersedes the previous BLOCKED report from `agt-m3-consume12-current`. Its R1/N1 fix was committed as `94091f05`; its merge-forward operation failed because Git metadata was read-only. This worker instead ports the reviewed worktree delta onto current integration, without any ancestry mutation. The orchestrator has also aligned the shared 0012 lock; neither previous blocker remains.

## Result and scope

Base/parent: `c456b3281497653cecf44f61acd6fa30565d83c8`, branch `tl/agt-m3-consume12-port-current`. Ported only the reviewed 33-path cohort from `94091f05`; actual change is **25 paths, 485 insertions, 28 deletions**, including the binary archive replacement and original selected-cut PNGs. Every cohort path other than the separately regenerated manifest is byte-equal to `94091f05` (including absent obsolete archive).

R1 serializes the real Python `BUILTIN_DEFAULT_THEME` into the test project and compares public `DEFAULT_THEME` with that parsed object. No copied navy expectation remains. N1 uses exact SHA256 equality. The explicit historical black/Georgia theme remains, and `presenter_ssr_before.json` is byte-unchanged with all **286** SSR expectations exercised.

Preserved current SDK/client/schema, Runtime pin and response fixtures, current Remotion host and smoke source, final-props/source carry, and presenter product files. `artifacts.json` was regenerated; it is byte-unchanged because current integration already has the identical presenter product and manifest entries. Manifest: 162 artifacts, version `sha256:ad0b7b331cfce0bcc6c5779993b1004b0d87f63212f819cb5988ba3ad7407d41`.

No normal PCM/source activation, package rebuild, shared dependency mutation, push, direct integration edit, commit, merge, rebase or checkout. No test expectations were weakened or disabled.

## Exact source and pair

- Qualified Agent source tree: `42d59104ef24fc745a56c55d81694a1cdb932f91` (both central lanes).
- Harness-produced Agent commit: pending worker exit; verify its tree equals the qualified tree above. This worker cannot truthfully report a SHA for a commit that has not yet been created.
- Runtime consumer pin, unchanged: `94114269d1ce23ab3224d7eca5a85138ce2b5fed`; vendor verification against `/home/user/work/wt/rt-pin-94114269` passes for every locked consumer artifact.
- Composition `0.0.12`, release preparation `4b9f2eee4dda960dc3a38aeba8943368c0fed3d5`, integration release merge `5e06f40146573a529896cc812229eb890c53c81a`.
- Archive SHA256: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 58,444 bytes; exact blob from `94091f05`.
- Archive integrity: `sha512-490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==`.
- Exact committed lock source: `94091f05:remotion/package-lock.json`; Git blob `5d3c765daa707065e8da5db94f3f06d21d37b7a2`, SHA256 `cca94d49f4bae0b3f16198d70ad08cd963f7d6061554d4276310deb6fe87f597`. Worktree and shared `/home/user/work/runtimes/agent-remotion-0012/package-lock.json` match these bytes exactly, including libc fields.
- Worktree and shared package.json SHA256: `58460ce59e2473d74f44238a2e5e78e2d4bd8a79a0bd94e430f7ae5eb6c2778a`.
- Observed integration heads for context only: Runtime `6023cfb10307b4c0004642b5fa1995d72ba4f6d1`, App `18becfbede00038830b97e63345445eeef54fa42`, Composition `e80c46baf5aa4b50a10b77a5ceadcb7ec4ab27ab`. This is Agent/Composition package qualification, not qualification of those other integration heads.

Exact binary diff: [final.patch](../workers/agt-m3-consume12-port-current/final.patch), SHA256 `2c54de69f47e08e8678bcc97e6c58ead82f3bfea78649ed46b98cb36f89443dc`. `git apply --check --reverse` succeeds against the final worktree.

```text
A	remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz
A	tests/fixtures/presenter_selected_cut/README.md
A	tests/fixtures/presenter_selected_cut/frame-0.png
A	tests/fixtures/presenter_selected_cut/frame-3.png
A	tests/fixtures/presenter_selected_cut/frame-4.png
A	tests/fixtures/presenter_selected_cut/frame-5.png
A	tests/fixtures/presenter_selected_cut/inspection.json
A	tests/fixtures/presenter_selected_cut/sha256.json
A	tests/packs/rendering/presenter_selected_cut_query.mjs
A	tests/packs/rendering/presenter_series_inspection.mjs
A	tests/packs/rendering/test_presenter_selected_cut_aggregate.py
A	tests/packs/rendering/test_presenter_series_inspection.py
D	remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz
M	astrid/core/rendering/remotion_runtime.py
M	remotion/package-lock.json
M	remotion/package.json
M	tests/core/timeline/test_clip_fields.py
M	tests/journeys/test_journey_plumbing.py
M	tests/packs/rendering/presenter_crop_geometry.mjs
M	tests/packs/rendering/presenter_scene_capability.mjs
M	tests/packs/rendering/test_composition_package.py
M	tests/packs/rendering/test_presenter_scene_capability.py
M	tests/packs/rendering/test_render_export_task_adapter.py
M	tests/packs/rendering/test_scene_answers.py
M	tests/packs/rendering/test_scene_host.py
```

## Tests and exact commands

All commands run from the assigned worktree. Shared venv and runtime dependencies remained read-only. A private, ignored `remotion/node_modules` copy (375 MB, copied with `cp -a --reflink=auto`) supplied local tests and central snapshot peers. No install or tool cache wrote to shared dependencies. The private copy is removed before completion.

Local presenter/package/manifest command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_presenter_scene_capability.py tests/packs/rendering/test_presenter_crop_equivalence.py tests/packs/rendering/test_presenter_series_inspection.py tests/packs/rendering/test_presenter_selected_cut_aggregate.py tests/packs/rendering/test_composition_package.py tests/test_artifact_manifest.py
```

**47 passed, 5 tar extraction deprecation warnings, 34.19s.** Includes the actual host-theme equality and historical SSR comparisons.

Local neighboring tests:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/core/timeline/test_clip_fields.py tests/packs/rendering/test_scene_answers.py tests/packs/rendering/test_scene_host.py tests/journeys/test_journey_plumbing.py::test_renderer_install_problem_names_the_missing_install_and_the_fix
```

**148 passed, 30.27s.**

Central final owner lane:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m3-consume12-port-current composition12-owner-integration --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R" 1
```

Run `agt-m3-consume12-port-current-composition12-owner-integration-1020093050-23242`: **47 passed, 5 warnings, pytest 36.35s, service 40s, exit 0**. The named lane explicitly clears addopts; all 47 cases execute. Full resolved command is retained in its `summary` and `log.txt` under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/`.

Central readiness and neighbors:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m3-consume12-port-current remotion-0012-nodes --no-cache --files 'tests/core/rendering/test_node_pin.py tests/reshape/test_remotion_gate.py tests/journeys/test_journey_plumbing.py::test_renderer_install_problem_names_the_missing_install_and_the_fix tests/core/timeline/test_clip_fields.py tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_scene_answers.py tests/packs/rendering/test_scene_host.py tests/packs/rendering/test_render_export_task_adapter.py')
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R" 1
```

Final run `agt-m3-consume12-port-current-remotion-0012-nodes-1020093220-18764`: **292 passed, 62 warnings, pytest 46.09s, service 49s, exit 0**. Covers package positive/negative readiness, launch binding, Node pin, gate validation, scene host/answers, export adapter and changed receiving-default neighbors. This lane keeps the normal integration filter; integration-marked presenter/package cases are separately covered by the 47-case owner lane.

Additional checks:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-94114269
git diff --check
git apply --check --reverse /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-consume12-port-current/final.patch
```

All pass. Read-only byte comparisons also verify shared package/lock equality, all reviewed cohort paths, and no changes to protected current paths.

## Initial setup failure and decisions

The first local/central owner attempts used an ignored directory of per-package symlinks. The fixture correctly refused it: real peer files resolved outside that directory (`17 passed, 30 setup errors`; central run `...composition12-owner-integration-1020092931-3922`). Replaced only this private dependency setup with the physical copy, preserving the containment assertion and every test. A no-cache named rerun was necessary because the service caches failures by source tree and does not hash dependency provisioning.

An earlier readiness run `...remotion-0012-nodes-1020092957-6729` passed **292 tests, 62 warnings, 43.10s**, but overlapped the private dependency reprovisioning. The final named readiness run above repeats it after provisioning is stable. Source tree stayed identical throughout; no product or test changes were made after the narrow port.

No plan decisions changed. Used an ordinary worktree-only forward port because it preserves current integration and requires no Git ancestry mutation. No full suite, make-check aggregate, browser render, physical pixel/audio parity, normal PCM/source activation, or cross-product journey is claimed.

## Handoff

No remaining task blocker. Harness should commit the worktree using the supplied commit message, confirm the resulting commit tree is `42d59104ef24fc745a56c55d81694a1cdb932f91`, then submit that exact descendant through the orchestrator's normal merge queue. App pairing/normal source activation remains separate work.
