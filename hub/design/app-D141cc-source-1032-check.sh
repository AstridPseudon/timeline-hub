#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CONTROLLER="$ROOT/controller.py"
CASES="$ROOT/cases.json"
PRIVATE_TMP="${TMPDIR:-/tmp}/d141cc-private-controls-$$"
mkdir -p "$PRIVATE_TMP"

printf '%s\n' 'controller self-test'
PYTHONPYCACHEPREFIX="$PRIVATE_TMP/pycache" python3 "$CONTROLLER" --self-test

printf '%s\n' 'python AST and private-cache compile'
PYTHONPYCACHEPREFIX="$PRIVATE_TMP/pycache" python3 -m py_compile "$CONTROLLER"
python3 - "$CONTROLLER" <<'PY'
import ast
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
tree = ast.parse(path.read_text(encoding="utf-8"))
assert not any(isinstance(node, (ast.Import, ast.ImportFrom)) and any(
    alias.name in {"subprocess", "socket", "urllib", "requests"} for alias in node.names
) for node in ast.walk(tree)), "controller must remain a harmless in-memory model"
PY

printf '%s\n' 'bash syntax'
bash -n "$0"

printf '%s\n' 'Ruff select F'
ruff check --select F "$CONTROLLER"

printf '%s\n' 'genuine-builder binding and conservation'
python3 - "$CONTROLLER" "$CASES" <<'PY'
import importlib.util
import json
import sys

controller_path, cases_path = sys.argv[1:]
spec = importlib.util.spec_from_file_location("d141cc_controller", controller_path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
assert spec.loader is not None
spec.loader.exec_module(module)
with open(cases_path, encoding="utf-8") as cases_file:
    cases = json.load(cases_file)
assert cases["builder"]["sha256"] == module.BUILDER_SHA256
assert cases["builder"]["git_blob"] == module.BUILDER_BLOB
assert cases["source_tuple"] == module.SOURCE_TUPLE
assert len(cases["dispatches"]) == 7
assert len(set(row["suite"] for row in cases["dispatches"])) == 7
assert len(set(row["output_path"] for row in cases["dispatches"])) == 7
assert len(set(row["plan_path"] for row in cases["dispatches"])) == 7
for row in cases["dispatches"]:
    recipe = module.production_recipe(row["selector"], row["attempt_scope"])
    assert row["suite"] == recipe.suite
    assert row["preflight_suite"] == recipe.preflight_suite
    assert row["source_digest"] == recipe.source_digest
    assert row["command_sha256"] == recipe.command_digest
    assert row["row_sha256"] == recipe.row_digest
    assert row["environment"] == dict(recipe.environment)
    assert len(row["environment"]) == 12
PY

printf '%s\n' 'PASS: private custody controls; no service or body operation was invoked'
