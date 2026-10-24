Restored strict admission between layers by removing both root-only caches. The two registry files now exactly match `bc38aa3`; only those files and `test_catalog_scan_once.py` changed.

Added coverage for the exact review mutation (`local/pack.yaml` → `schema_version: 2\nid: forged\n`), valid definition changes, resource bytes with unchanged size/mtime, resource and ancestor symlinks, escaping links, missing resources, distinct roots, provenance, and successful unchanged shared-root loads.

The old code produced **14 failures and 2 passes** on the new between-layer controls. The repaired catalog file passes **24 tests**.

All pytest commands used:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f
export ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f
P=/home/user/work/venv-agent/bin/python
```

Exact targeted commands and results:

```bash
$P -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 tests/core/rendering/test_catalog_scan_once.py -k between_layers
# Old code: 14 failed, 2 passed, 8 deselected

$P -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 tests/core/rendering/test_catalog_scan_once.py
# Repaired: 24 passed

$P -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 tests/core/rendering/test_catalog_scan_once.py tests/core/timeline/test_transition_catalog_lazy.py tests/timeline/test_type_resolve.py tests/timeline/test_timeline_elements_catalog.py tests/core/rendering/test_registry.py tests/packs/test_pack_discovery_metadata.py
# 81 passed

$P -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 tests/core/test_elements_registry.py tests/core/test_element_kind_registry.py tests/core/rendering/test_registry_matrix.py
# 76 passed, 7 subtests passed

$P -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 tests/core/rendering/test_installed_registry_security.py tests/core/test_project_packs.py tests/core/test_project_pack_inputs.py tests/packs/test_canonical_pack_v2.py tests/packs/test_canonical_pack_v3.py tests/core/pack/test_v3_core_worker_luna.py
# 129 passed
```

Static checks:

- `$P -m ruff check . --no-cache --output-format json`: **2,147 identical parent/current diagnostic identities**.
- `/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes`, with separate private caches: **1,911 identical identities**.
- `$P scripts/artifact_manifest.py --check` and `git diff --check`: passed.

Decision: revert the unsafe optimization because no complete immutable-admission guard exists within these registry boundaries. Duplicate strict admission cost remains. Further optimization must preserve actual source, definition, configuration, inventory, and custody checks under their existing owners.

Vendor checker remains stopped pending **0206**. No timing probe, original render, full suite, browser, provisioning, or installed-child qualification ran; no performance acceptance claim.

Commit message and empty `DONE` written. Next: independent review, then manager-owned performance qualification.