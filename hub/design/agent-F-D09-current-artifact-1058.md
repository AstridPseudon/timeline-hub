# F D09 current Composition artifact fixture alignment

## Result

Updated only `tests/integrations/test_d09_managed_scene_only.py`. The D09
fixture now accepts the established `ASTRID_REMOTION_PROJECT_DIR` profile
binding and defaults to the existing normal Composition14 profile path. The
original two D09 test bodies are unchanged at the AST level.

The fixture's Composition admission is now tied to the current Agent
manifest and lock, not a free version string:

- dependency: `file:artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`
- archive: 73,451 bytes, 80 regular members
- archive SHA-256: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`
- lock SRI: `sha512-Ajl7lyCbJqbbOpHKEr2xlhFw85hWyirlTU1Dq63BNNUdHYfqgzLXljmudP359uKH6yBxSBMPTDoHLxgiDt65oQ==`

Setup verifies the copied profile's dependency and lock resolution, archive
hash/size/member count, package version, and byte equality of all 80 installed
Composition files against the approved archive. No validator, guard, pin,
production caller, or D09 assertion was changed.

## Evidence

Commands run from the worker worktree:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/integrations/test_d09_managed_scene_only.py
3 tests collected in 1.07s

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m ruff check tests/integrations/test_d09_managed_scene_only.py
All checks passed!

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m mypy --config-file pyproject.toml tests/integrations/test_d09_managed_scene_only.py
Success: no issues found in 1 source file

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_installer_schema.py::test_remotion_lock_pins_the_immutable_composition_public_entry
1 passed in 0.72s

python3 AST comparison of HEAD and current D09 test functions
original test function AST bodies unchanged: 2

git diff --check
PASS
```

Read-only custody comparison found the named existing profile is stale despite
declaring version 0.0.14: its archive is 72,134 bytes with SHA-256
`21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`, its
dependency is the old `file:artifacts/...-0.0.14.tgz` name, and its installed
package is therefore not the approved `635f4de` artifact. It occupies about
377 MiB / 21,425 files. No runtime, shared node_modules, wheel, or install was
modified.

## Blocked / next step

The live D09 body was intentionally not run in this author turn, as required.
The central activation needs a newly prepared immutable normal profile from
the current Agent V3 source (`b56828de538c10584030cc1a0c3c2ac39fc6cc14`) and
its current `remotion/package-lock.json` SHA-256
`f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`, carrying
the approved 73,451-byte archive and its 80 installed files. The existing
`agent-remotion-composition14-255b6856` profile must not be repointed or
mutated. After that profile is available through `ASTRID_REMOTION_PROJECT_DIR`,
run the one authorized central D09 activation.
