# Runtime project-data root export preparation

Implemented the normal generator-path fix for future canonical command Args.

The Python package root template now contains render-only markers. `generators.generate.render_python_package_init()` reads the canonical Agent schema definitions and appends only new top-level names ending in `Args`, in source order, to the existing import and `__all__` sections. Existing ordered exports remain untouched; generated internal `Variant` names do not end in `Args` and are not projected. The current 55-definition/29-operation source therefore renders byte-identically.

Added one focused in-memory regression covering synthetic `ProjectDataWriteArgs` and `FutureArgs`, rejecting `EditCommandVariant1`, and checking both the import and `__all__` projections.

Evidence:

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_timeline_commit_type_generator.py` — 9 passed (one pre-existing pytest config warning about unknown `timeout`).
- `PYTHONDONTWRITEBYTECODE=1 python generators/generate.py --check` — passed; existing frozen generated files unchanged.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/artifact_manifest.py --check` — passed; 75 artifacts, manifest version `sha256:b397e5fdb9fc25502bbda9ad5011e82dd2d63330d5af373834d31e6761276e20`.
- `git diff --check` — passed.

No source pin, schema, generated artifact, release, ABI, or integration change was made. No full/native/broad suite was run.
