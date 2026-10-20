# AM snap-plate preserved fill guard

## Scope

- Base: `d7c03af259abe7169e05996a3adce0a3838af6e1` (`tl/agt-m3-plate-current-artifact-gate`).
- Changed repository path: `tests/packs/test_am_snap_plate_fill.py` only.
- Restored `AmSnapPlateFillTest::test_component_renders_without_an_asset_when_fill_is_set` with all four original assertions unchanged.
- The source fixture now joins the 156-line `component.tsx` and 23-line extracted `surface.ts` (179 source lines total), so the guard/JSX assertions remain covered while `FILL_TOKENS` and the background fallback are read from their current helper location.
- Production source was not changed: `component.tsx` 156 lines, `surface.ts` 23 lines, `scene.ts` 22 lines.

## Test counts

- `tests/packs/test_am_snap_plate_fill.py`: 3 passed.
- `tests/packs/rendering/test_am_snap_plate_scene_capability.py`: 14 passed, including the registered actual SSR lane (10 variants × 9 frames) and explicit fill/background precedence.
- No assertions were removed, skipped, weakened, or marked expected-to-fail.

## Exact evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= --tb=short tests/packs/test_am_snap_plate_fill.py
3 passed in 0.50s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-current/node_modules ASTRID_TEST_COMPOSITION_ARTIFACT="$PWD/remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= --tb=short --basetemp=/tmp/agt-m3-plate-preserve-fill-guard-scene tests/packs/rendering/test_am_snap_plate_scene_capability.py
14 passed in 48.13s

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/packs/test_am_snap_plate_fill.py
All checks passed!

git diff --check
pass

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python scripts/gen_element_catalog.py --check
pass

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current
```

## Protected bytes

The normal catalog, manifest, and checked-in public12 Composition artifact are unchanged from base:

```text
astrid/packs/rendering/elements/catalog.ts
e981170d497f9483aa4682bee9defba367b6fdb155071420a19e8e827f59dcba
artifacts.json
6963e3393d22b8e46d1df5f2cb81f401bee7080407bd3f61f108560a2ef9a176
remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz
0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3
```

The existing private peer tree was used read-only. No public13 artifact exists in this Agent repository; no public13 or Composition artifact was changed. No full suite, new matrix, integration, browser, live socket, install, or git mutation was run.

