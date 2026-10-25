# U1/D135 final review validation

## Exact canonical bounded checks

All commands were run against candidate `a2b289dd732db7af10d5c8d375f6dad5e21c9fc8`
(`tree 2b78abf70de620a47451aba655de1635143b8e3f`). No alternate Ruff binary,
config, or scope was used.

- `/root/.local/bin/ruff --version` → `ruff 0.16.8`.
- `/root/.local/bin/ruff check --config /home/user/banodoco/banodoco-workspace-runtime/pyproject.toml ops-u1-farm-preflight/preflight.py` → PASS (`All checks passed!`).
- `/home/user/work/venv-agent/bin/python -m json.tool ops-u1-farm-preflight/source-manifest.json` → PASS.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<private-tmp> /home/user/work/venv-agent/bin/python -m py_compile ops-u1-farm-preflight/preflight.py` → PASS.
- `git diff --check` and `git diff --check HEAD^ HEAD -- ops-u1-farm-preflight` → PASS.
- Frozen object audit using the manifest’s exact Runtime/Agent commits → `SOURCE_HASHES=21/21 AST_MANIFESTS=7/7`; all seven actual-module hashes match the frozen Runtime object.

## Negative prerequisite censuses

- `/home/user/work/venv-agent/bin/python ops-u1-farm-preflight/preflight.py ... --expected-interpreter /home/user/work/venv-agent/bin/python` against the current non-receipted Runtime/Agent directories → exit 1, 7 imports attempted, 4 import failures, 39 accumulated findings, exact source identity mismatches retained, `body_authorized=false`, `test_body_run=false`.
- `/usr/bin/python3 ops-u1-farm-preflight/preflight.py ... --expected-interpreter /home/user/work/venv-agent/bin/python` → exit 1, 7 imports attempted, 4 import failures, 41 accumulated findings, interpreter mismatch and missing `pytest-timeout` retained, `body_authorized=false`, `test_body_run=false`.

Both controls used private temporary output directories. They did not run
pytest collection or any test body.

## Recipe controls

The recipe’s single-suite, child-only multiple-suite, malformed XML, and
missing XML probes all passed: `2`, `5/1/1/1`, nonzero, and nonzero
respectively. The exact six-file argv, `-o addopts=`, `-p no:cacheprovider`,
`--timeout=45`, durable XML/log/exit/collection outputs, fixed interpreter
binding, source tuple, dependency aggregation, local-origin checks, and
side-effect AST controls were inspected.

## Scope and result

The current mounted directories were used only as negative controls. The
actual receipt-bound Farm preflight and authorized six-file body are **NOTRUN**;
source-only controls do not qualify Farm. No Runtime/Agent/App product or test
files, pins, generated files, live configuration, kit, provider, socket, Store,
acquisition path, full suite, core suite, or D130 action was run or changed.

The remaining failure is D135-FINAL-1: the six test hashes are present in
`actual_modules` but `_manifest_checks()` validates only path/import AST
content, while `_source_checks()` hashes only the separate 21-file list.
