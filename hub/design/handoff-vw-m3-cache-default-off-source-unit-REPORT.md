# vw-m3-cache-default-off-source-unit

## What changed

- Kept public scene-payload cache writes opt-in through the existing injected
  `FrameCaptureCache` owner.
- Kept the normal `RemotionFrameProvider(cache=None)` path PNG-only, so a new
  provider reuses persisted PNG bytes without trusting persisted scene rows.
- Added a direct transport regression proving two default providers sharing a
  cache directory hit the same PNG bytes, make one capture only, perform no
  second scene query, and retain the legacy label fallback.
- Preserved the existing same-owner payload, stale/forged-row, mutation,
  cross-owner, failed-batch, fallback, and cache-cap coverage.

## Tests

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_scene_cache_payload.py tests/packs/rendering/test_scene_source_carry.py -k 'transport'`
  — 58 passed, 39 deselected.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_composed_frame_capture.py tests/packs/rendering/test_bounds_plumbing.py tests/packs/rendering/test_scene_cache_payload.py tests/packs/rendering/test_scene_source_carry.py -k 'not native'`
  — 95 passed, 22 deselected in 9.36s.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check --no-cache astrid/packs/rendering/actions/timeline_visualize/composed_frame.py tests/packs/rendering/test_scene_cache_payload.py tests/packs/rendering/test_scene_source_carry.py`
  — passed.
- `git diff --check` — passed.

No full suite, browser, localhost, network, install, or real Remotion render was run.

## Decisions and boundaries

The normal filmstrip caller still omits `cache=`, so it is deliberately not a
qualified public-payload caller. No caller change or new store was invented.
An injected existing cache owner remains the explicit opt-in seam used by the
qualified same-owner tests. Cross-owner/process payload reuse remains a miss by
design; ordinary PNG reuse remains available.

No D09 deletion, private fallback deletion, Composition change, SDK change,
global store, signature/certificate, durable trust, DTO, or authority flag was
added. Independent gate review and Agent-owner merge remain next steps before
any public payload caller is qualified.
