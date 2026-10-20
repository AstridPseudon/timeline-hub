# M2 Composition 0.0.10 adoption (agt-public10-adoption)

Status: source composed and targeted tests PASS; exact-pair Runtime integration, remotion gate and 0.0.8 tarball removal NOT done (see Unverified).

## Tuple

| Field | Exact value |
|---|---|
| Worktree / branch | `/home/user/work/wt/agt-public10-adoption` / `tl/agt-public10-adoption` |
| Base | `tl/integration` `4a75f68f` |
| Bundle1 source | `tl/agt-m2-bundle1-pin` `3bf9e5368a956ef562c77e1beb0a745addf23daf` (base `fc324e83`, an ancestor of `4a75f68f`); applied as `git diff fc324e83 3bf9e536 \| git apply`, clean, 17 files |
| Runtime | `6be970633cc82ab412428151e6bf42f3e7fc3081`, client 0.2.2, schema `sha256:89a396aa…78d3`, artifact `sha256:3b805d69…9730` (design/m2-writer-bundle-1.md; unchanged, `runtime.lock.json` comes from the bundle1 patch) |
| Composition | `@banodoco/timeline-composition` 0.0.10 |
| Artifact sha256 | `cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7` (matches orch `artifacts/banodoco-timeline-composition-0.0.10.tgz`) |
| npm integrity | `sha512-SmJAoem9f+86D+eO+PvBAz3JydlefpUUwcOOkG7SU9k2ZPKpjXLWKHm/N4424TO5HNQtCHMt5T6Jy2Y5zA6Ycg==` |

## Pin change (same shape as the 0.0.8 adoption, cbd91c3b)

- Added `remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz`.
- `remotion/package.json` and `remotion/package-lock.json`: file spec, `version`, `resolved`, `integrity` (peers unchanged).
- `astrid/core/rendering/remotion_runtime.py`: `_COMPOSITION_PACKAGE_VERSION = "0.0.10"`.
- Tests: `test_composition_package.py` (SHA256, integrity, version, path), `test_render_export_task_adapter.py` (artifact path), `test_journey_plumbing.py` (staged version), `test_clip_fields.py` (comment).
- No other 0.0.8 reference remains (`git grep 0.0.8` empty outside the tarball).

## Commands and results

All with `/home/user/work/venv-agent/bin/python`:

- `-m pytest -q tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_render_export_task_adapter.py tests/core/timeline/test_clip_fields.py tests/journeys/test_journey_plumbing.py tests/packs/rendering/test_remotion_locking.py tests/editing_conformance -p no:warnings` → **580 passed, 4 skipped, 33 deselected**.
- `-m pytest -q tests/packs/rendering tests/sdk/test_timeline_sync_native.py tests/packs/timeline/test_cli_native.py tests/sdk/test_timeline_commit_provider_parent_track_label.py -p no:warnings -k "not real_render and not real_two_second and not stamped_top_layer"` → **1061 passed, 10 skipped, 33 deselected, 1 failed**. The failure is `test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup`: "SSR contract must resolve the Node version pinned by remotion/package.json". It is an environment failure (no pinned Node on PATH), not run again with Node. The central `consumer-regressions-integration` suite lists exactly this node with the Node 20.19.4 env.
- `-m scripts.reshape.import_cycles --baseline scripts/reshape/baselines/import_cycles.json` → OK, no new cycles.

## Unverified / not done

- Exact-pair Runtime integration: suite `bundle1-runtime6be9706-integration` fails in 1s because `/home/user/work/wt/rt-m2-track-public-export` no longer exists. `tl/integration` of Runtime is 11 commits past 6be9706, so I did not substitute it. Needs a Runtime checkout at exactly 6be9706 (or a suite re-pointed at one), then the five files in that suite.
- `scripts/reshape/remotion_gate.py` (install/typecheck/parity) not run: needs `npm ci` and Node 20; not run in the sandbox. `consumer-regressions-integration` / `remotion-env-nodes` need `/home/user/work/runtimes/agent-remotion` reinstalled with the 0.0.10 tarball first.
- `remotion/artifacts/banodoco-timeline-composition-0.0.8.tgz` is still in the tree (unreferenced): `rm` was denied in my sandbox. The adopter should `git rm` it.
- `scripts/vendor_lock.py check` also needs the missing Runtime checkout; the lock bytes are those of the published bundle1 commit.
- No full suite requested.
