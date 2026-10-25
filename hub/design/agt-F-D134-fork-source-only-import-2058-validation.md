# D134 validation

## exact source and AST conservation
PASS: full-file donor equality
PASS: AST equality and expected function/assertion/input-conservation nodes
sha256=3fef15b5862e044942f2d0164b37f6f9281f86d378345d8a0b262c64870af8a4
git_blob=512c806487049c1b86a9d47bcafeb3dcb0ade60c
assert_nodes=31

## Python 3.11 private compile
PASS: /usr/bin/python3.11 compile(source, filename, exec)

## ruff
All checks passed!

## mypy baseline
ERROR: mypy failed to execute (exit 2): astrid/core/element/project_packs.py:23: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/element/project_packs.py:23: note: Hint: "python3 -m pip install types-PyYAML"
astrid/core/element/project_packs.py:23: note: (or run "mypy --install-types" to install all missing stub packages)
astrid/core/element/project_packs.py:23: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
astrid/core/execution/generic_host.py:336: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/model_catalog/registry.py:169: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/pack/agent_index.py:28: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/pack/canonical.py:21: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/pack/cli_basic.py:18: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/pack/loader.py:11: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/pack/manifest.py:9: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/pack/validate.py:25: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/pack/validate_first_party.py:14: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/timeline/clip_fields.py:19: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/timeline/scene_roles.py:64: error: Library stubs not installed for "yaml"  [import-untyped]
astrid/core/scaffold.py:121: error: Library stubs not installed for "yaml"  [import-untyped]
/home/user/work/venv-agent/lib/python3.13/site-packages/numpy/__init__.pyi:737: error: Type statement is only supported in Python 3.12 and greater  [syntax]
Found 14 errors in 14 files (errors prevented further checking)

## git diff check
PASS: git diff --check

validation_exit=0

## mypy baseline (private Python 3.11 typecheck environment)

## mypy baseline (private Python 3.11 typecheck environment, bounded 180s)
Mypy findings: current=1902 baseline=1902
mypy_typecheck_env_exit=0
Mypy findings: current=1902 baseline=1902
mypy_typecheck_env_exit=0
