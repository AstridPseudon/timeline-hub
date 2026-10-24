Implemented **F-render-21** on base `2007cf7aaf`; qualification remains partially blocked.

Changed only `astrid/core/pack/discovery.py` and a new focused test. Reuse requires the built-in scanner’s exact identity and equality of its actual default root with the resolved project pack root. Different roots and injected scanners retain separate calls. No cross-call cache was added.

Controls cover complete discovery records/order, aliases, collisions, priorities, eligibility, project-local semantics, validation guards, and fresh reads. Public `rendering.support()` reaches the optimized discovery through the real registry with transport stubbed.

Commands used `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime` and `/home/user/work/venv-agent/bin/python`:

```bash
python -m pytest -q -p no:cacheprovider \
  tests/packs/test_pack_discovery_single_scan.py \
  tests/packs/test_pack_discovery_metadata.py \
  tests/test_default_registry_scopes.py \
  tests/packs/rendering/test_render_remotion_registry.py::RenderRemotionRegistryGenerationTest::test_main_synthesizes_empty_asset_registry_when_assets_are_absent \
  --basetemp="$TMPDIR/pytest-final" --tb=short
```

**36 passed, 3 subtests passed.** Loading `HEAD:astrid/core/pack/discovery.py` into the discovery module and running the final focused tests produced **6 expected scan-count failures, 12 passes**.

Static checks:

- Scoped Ruff: passed, including the new test.
- Scoped mypy: the same two pre-existing assignment errors; no new findings.
- `py_compile`: both changed/new files passed, outputs under `$TMPDIR`.
- `git diff --check`: passed. No vendor, schema, pin, or artifact changes.

These targeted existing cases both failed because the worktree lacks the installed Composition package:

```bash
python -m pytest -q -p no:cacheprovider \
  tests/packs/rendering/test_render_remotion_registry.py::RenderRemotionRegistryGenerationTest::test_registry_generation_skips_when_state_and_outputs_are_current \
  tests/packs/rendering/test_render_remotion_registry.py::RenderRemotionRegistryGenerationTest::test_registry_generation_regenerates_when_on_disk_outputs_are_stale \
  --basetemp="$TMPDIR/pytest-nonrender" --tb=short
```

Their subsequent inspection invokes Node, forbidden by this brief. No provisioning or workaround was attempted. Written: `commit-msg` and `BLOCKED`.

Next: independent review and completion of those checks in the qualified environment, then normal-home merge before original qualification. The original support body was not rerun. Transition remains execution **6 of 10**; the uncalibrated timing does not establish the watchdog’s cause.