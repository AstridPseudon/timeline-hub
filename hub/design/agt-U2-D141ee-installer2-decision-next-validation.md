# U2 D141ee installer2 validation

Result: `PASS`. Exactly the two owner-approved definitions were removed from `tests/test_installer_schema.py`; no other Git path changed.

## Decision and scope

- Owner approval: `agent-D141ii-installer-owner-approval-1300.md`, SHA-256 `2f844fc0fdd8286d1743bfed0a114f0ebe255411f735ec602b39da7d6a9b442a`, typed `2026-10-26T13:00:57Z`.
- The verbatim quote is repeated once per ID in `per-id.json` and `retirement-ledger-entries.md`.
- Retired IDs are exactly `test_staging_installs_the_npm_locked_schema_before_declaring_services` and `test_remotion_lock_pins_the_transitive_schema_package`.
- No package lock, installer, schema, generated client, provenance pin, product file, writer, force path, old endpoint, cache/hook/trust surface, or other test was changed.

## Static conservation checks

The AST check compared the working file with `git show HEAD:tests/test_installer_schema.py`, removed only the two approved top-level definitions from the comparison tree, and passed. It also verified both original function source hashes from the scope record, that every retained function/assertion AST is identical, that both target definitions are absent, and that `git diff --name-only` is exactly `tests/test_installer_schema.py`.

Collection passed with exactly four retained selectors:

```text
tests/test_installer_schema.py::test_staging_verifies_the_local_schema_before_declaring_services
tests/test_installer_schema.py::test_local_schema_verification_rejects_a_changed_schema
tests/test_installer_schema.py::test_remotion_lock_pins_the_immutable_composition_public_entry
tests/test_installer_schema.py::test_d66_upstream_remotion_lock_pins_the_transitive_schema_package
```

## Tests and checks

Final targeted command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-U2-D141ee-installer2-decision-next:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -n 3 --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2-D141ee-installer2-decision-next/evidence/targeted.xml --basetemp=/tmp/w-58ac648fba/basetemp-final -o cache_dir=/tmp/w-58ac648fba/cache-final tests/test_installer_schema.py
```

Result: `4 passed in 1.82s`.

- `PYTHONDONTWRITEBYTECODE=1 ... pytest --collect-only -q -o addopts= tests/test_installer_schema.py`: 4 tests collected.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/test_installer_schema.py`: passed.
- `git diff --check`: passed.
- Typecheck: N/A; this is a tests-only deletion and no applicable repository typecheck lane was requested.
- No full, core, browser, install, render, child-body, package-install, force, or live-socket suite was run.

## Retained controls and supported caller

The actual supported Agent caller is `astrid/installer/backend.py::Backend.stage`, which calls `_verify_local_timeline_schema` before the ordinary two Python installs, then `install_remotion_dependencies` against the locked local Composition path, then service declaration. The Runtime contract schema remains the canonical source through `runtime.lock.json`, and Runtime remains the sole film writer. These controls were not adapted or weakened.
