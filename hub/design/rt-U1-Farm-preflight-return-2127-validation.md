# U1/D135 source-only validation

Harness result: **PASS** for the private Farm preflight packet. The actual
Farm preflight and six-file body remain **NOTRUN** here.

## Canonical bounded check

The bounded command sequence and captured output are in `canonical-check.log`.
Its exact executable controls were:

```text
/root/.local/bin/ruff check --config /home/user/banodoco/banodoco-workspace-runtime/pyproject.toml ops-u1-farm-preflight/preflight.py
/home/user/work/venv-agent/bin/python -m json.tool ops-u1-farm-preflight/source-manifest.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/d135-canonical-pycache-final2 /home/user/work/venv-agent/bin/python -m py_compile ops-u1-farm-preflight/preflight.py
git diff --check
/home/user/work/venv-agent/bin/python ops-u1-farm-preflight/preflight.py --runtime-checkout /home/user/banodoco/banodoco-workspace-runtime --agent-checkout /home/user/peteromallet/astrid-agent --output-dir /tmp/d135-final2-negative --expected-interpreter /home/user/work/venv-agent/bin/python
/usr/bin/python3 ops-u1-farm-preflight/preflight.py --runtime-checkout /home/user/banodoco/banodoco-workspace-runtime --agent-checkout /home/user/peteromallet/astrid-agent --output-dir /tmp/d135-final2-system-negative --expected-interpreter /home/user/work/venv-agent/bin/python
```

The source hash/AST audit and single/multiple XML helper probes are the
bounded inline Python controls immediately following those commands in the
same run. It used Ruff `/root/.local/bin/ruff` version `0.16.8` with the read-only
Runtime config `/home/user/banodoco/banodoco-workspace-runtime/pyproject.toml`,
private `py_compile` output under `/tmp`, the manifest's frozen Git objects,
both negative prerequisite censuses, and the recipe XML helper controls.

Results:

- Ruff: PASS (`All checks passed!`).
- JSON manifest validation: PASS.
- Private compile: PASS.
- `git diff --check`: PASS.
- Frozen source-object audit: **21/21** hashes and **7/7** AST/import manifests;
  no denied top-level side effects.
- Venv-agent negative census: exit 1, seven imports attempted, four import
  failures, all exact source identity mismatches retained, 38 accumulated
  findings, body authorization false, test body false.
- System-Python negative census: exit 1, 40 accumulated findings including
  interpreter mismatch and missing `pytest-timeout`; all seven imports were
  still attempted before refusal.
- XML helper: single-suite `tests=2`; child-only multiple-suite aggregate
  `tests=5, failures=1, errors=1, skipped=1`; malformed and missing XML both
  exit nonzero with explicit failure JSON.

The current mounted Runtime and Agent directories were used only as a
negative control. Their observed identities were Runtime commit
`31c7ac3a00f7a205f507bf5bd4d4625628d429bd`/tree
`73e676f420ba0545b6eebe45870d532344a9e69b`, and Agent commit
`5249ac07903af36532840d5c5ed3f8960a2fe07c`/tree
`a5d613d07be0dbafed815b6544d503727b5a1acf`; the packet correctly refused
both against the exact required tuple.

## Scope controls

The private packet changes only `ops-u1-farm-preflight/preflight.py`,
`recipe.md`, and `source-manifest.json`. The exact 21 source hashes, seven
module AST manifests, and six-file pytest argv are preserved. Dependency
requirements are recorded as the exact Runtime declarations (`pytest>=8`,
`pytest-timeout>=2.4`, `PyYAML>=6`, `jsonschema>=4`, and `referencing>=0.30`)
and are compared without acquisition.

No Runtime/Agent source, tests, generated files, pins, live configuration,
Farm kit, provider, socket, Store, pytest collection/body, venv build, or
full suite was run or changed. Filesystem free space at final validation was
4,689,172 KiB, above the 4 GiB stop floor.
