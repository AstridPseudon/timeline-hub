**Tests qualified; no new performance repair.** At parent `8a8dbf2d4e`, `astrid/core/timeline/validators/timeline.py` already contains the `2b2c1a02f0` lazy guard, byte-identically. No justified source change remained at the assigned seam.

Current cold call trace:

- Empty timeline: zero registry loads.
- Media-only clip: two loads through `is_visual_clip_element()` and catalog type resolution.
- Transition-bearing clip: those same loads, then `_transition_ids()` using the existing catalog.

The retained eager-transition diagnosis therefore does not describe current no-transition execution. This trace does **not** establish the original timeout’s cause.

Imported only `tests/core/rendering/test_catalog_scan_once.py` from `29f3ab9db5`, with exact blob equality (`8ee8bf822fe05aad40f6a8d8d048b1af61458742`). Added five authentic-catalog controls for lazy loading, acceptance, unknown refusal, and changed references. Product files remain unchanged; unsafe `b8959a06ee` is not an ancestor.

All pytest runs used:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f
export ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f
P=/home/user/work/venv-agent/bin/python
```

Exact commands and results:

```bash
$P -m pytest -q -oaddopts= -p no:cacheprovider tests/core/rendering/test_catalog_scan_once.py tests/core/timeline/test_transition_catalog_source.py tests/core/timeline/test_transition_catalog_lazy.py tests/timeline/test_type_resolve.py tests/timeline/test_timeline_elements_catalog.py tests/core/rendering/test_registry.py tests/packs/test_pack_discovery_metadata.py
# 86 passed; includes all 24 imported admission controls

$P -m pytest -q -oaddopts= -p no:cacheprovider tests/core/test_elements_registry.py tests/core/test_element_kind_registry.py tests/core/rendering/test_registry_matrix.py
# 76 passed, 7 subtests passed

$P -m pytest -q -oaddopts= -p no:cacheprovider tests/core/rendering/test_installed_registry_security.py tests/core/test_project_packs.py tests/core/test_project_pack_inputs.py tests/packs/test_canonical_pack_v2.py tests/packs/test_canonical_pack_v3.py tests/core/pack/test_v3_core_worker_luna.py
# 129 passed

PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f:$TMPDIR $P -m pytest -q -oaddopts= -p no:cacheprovider -p pre_lazy_plugin tests/core/timeline/test_transition_catalog_source.py -k no_transition
# Historical pre-2b2 body: 2 failed, 3 deselected
```

Historical RED/current GREEN verifies the **existing** repair.

Static checks:

- Parent/current `$P -m ruff check . --no-cache --output-format json`: **2,145 identical diagnostic identities**.
- Parent/current `/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid scripts/reshape --cache-dir "$TMPDIR/mypy-{parent,current}" --hide-error-context --no-color-output --no-pretty --show-error-codes`: **1,909 identical diagnostic identities**, using separate caches.
- Focused-file Ruff: passed.
- `$P scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`: passed.
- `$P scripts/artifact_manifest.py --check`: passed.
- `git diff --check`: passed.

No original timeout, full, renderer, browser, benchmark, or provisioning run occurred. Disk ended at **6.9 GB**, below the probe threshold. **Original performance remains unqualified.** Recommend independent review of the type-resolution path and installed-child source identity before authorizing further repair or measurement.

Commit message and `DONE` written. Nothing deleted.