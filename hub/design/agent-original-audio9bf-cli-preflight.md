# Agent native trim preflight handoff

Date: 2026-10-20

## Change

The native CLI trim adapter now routes a no-pending trim through the existing
`TimelineSession.trim` helper. That helper is the established queue/flush path:
it performs the client WAV read only as a non-authoritative preflight, captures
the media duration read, and leaves Runtime to recompute the descriptor from
the exact original-base declared media pin. Pending retries continue through
the same helper, and selector/error fallback behavior is unchanged.

No Runtime fixture, guard, endpoint, DTO, schema, provider, timing math,
registry duration, media adoption, or success assertion was changed.

## Exact source

- Worktree: `/home/user/work/wt/agt-m2-cli-trim-verified-preflight`
- Base commit: `dbb34e2124a7f8196f27b7ee5625b81818bd3666`
- Base tree: `99ce6cb23d21252c348df2c899fc04aea302b637`
- Changed source: `astrid/packs/timeline/cli_native.py`
  SHA-256 `ab683e9dd7080fc4a3ef2e2732694c75b2f21ec30cfddbd1f6c9615118dc1463`
- Regression: `tests/packs/timeline/test_cli_commit_trim.py`
  SHA-256 `1727b13a9ad929cc51aabe3899d06f46483a8880dcd459ebcde110f0d8e30af0`
- Two-file binary patch SHA-256:
  `a5b3fcc00bcb3d209cee55d0ce0222d3d9b95faf33157c0fa98c819c698d3fd4`

The harness commit SHA is not available until worker exit; the tuple above
identifies the exact current source plus patch.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/timeline/test_cli_commit_trim.py tests/editing_conformance/test_recipe_m2_clip_trim.py`
  — **138 passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/timeline/test_cli_commit_move.py tests/sdk/test_timeline_native_frontends.py tests/sdk/test_timeline_sync.py`
  — **79 passed**.
- `git diff --check` — passed.

## Runtime request

Runtime should rerun only the two unchanged strict-positive original nodes
(`historical-audio` and `literal-media`) from the original-audio9bf CLI pair
once, using normal Runtime `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e` and this
new Agent source. The unchanged control node already passed and need not be
duplicated. Runtime owns the actual journey and should report the normal-door,
provider-authenticated result; no comprehensive suite is requested here.
