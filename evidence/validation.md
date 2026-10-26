# D141 Farm input-producer validation

## Read-only source checks

| Check | Result |
| --- | --- |
| Frozen tuple commit/tree/origin/status readback | PASS for four current worktrees |
| Operational source SHA/size/mode readback | PASS for maker, requester, checker, seed verifier and Farm verifier |
| Frozen runtime lock, D73 launcher and C0 schema hashes | PASS; paths and SHA-256 values match `source-manifest.json` |
| C0 contract and mounted receiver field scan | PASS; no source edits to C0 or product code |
| Historical 2149/2216 distinction | PASS; no historical evidence retargeted |
| D139a installed-vs-source distinction | PASS; actual Farm installed bytes remain MISSING |
| Composition corrected receipt exact filename/content/hash | PASS; venue admission still pending |

## Exact commands and results

```sh
git -C /home/user/work/wt/agt-pin-28e56cac rev-parse HEAD HEAD^{tree}
git -C /home/user/work/runtime rev-parse HEAD HEAD^{tree}
git -C /home/user/work/app rev-parse HEAD HEAD^{tree}
git -C /home/user/work/composition rev-parse HEAD HEAD^{tree}
git -C <each> status --porcelain --untracked-files=all
```

PASS: the four values match `evidence/source-manifest.json`; all four status
outputs are empty.

```sh
sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/{make-child-venv,request-child-venv,check-child-imports,verify_dependency_seed.py,verify_farm_distribution_inputs.py}
stat -c '%n %s %a' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/{make-child-venv,request-child-venv,check-child-imports,verify_dependency_seed.py,verify_farm_distribution_inputs.py}
```

PASS: hashes, byte counts and modes match the source manifest.

```sh
/home/user/work/venv-runtime/bin/python - <<'PY'
import hashlib, json
from pathlib import Path
manifest = json.loads(Path('evidence/source-manifest.json').read_text())
for label, item in manifest['frozen_source_files'].items():
    path = Path(item['path'])
    assert path.is_file()
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']
PY
```

PASS: frozen runtime lock, D73 launcher and C0 schema hashes match.

```sh
bash -n ops-d140-farm/receive-farm.sh
/home/user/work/venv-runtime/bin/python -m json.tool evidence/input-map.json
/home/user/work/venv-runtime/bin/python -m json.tool evidence/source-manifest.json
/home/user/work/venv-runtime/bin/python -m json.tool evidence/qualified-inputs/provenance.json
git diff --check
```

PASS: all five commands. No Farm census was run because the task explicitly
forbids running it and the source packet has genuine missing prerequisites.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider ops-d140-farm/test_recipe.py
```

PASS: `97 passed in 168.38s (0:02:48)`.

```sh
/home/user/work/venv-runtime/bin/python - <<'PY'
import ast
from pathlib import Path
for name in ('ops-d140-farm/receipts.py', 'ops-d140-farm/test_recipe.py'):
    ast.parse(Path(name).read_text(), filename=name)
PY
rg -n 'FARM_INSTALLED_KIT_SUMMARY|SCHEMA_INSTALLED_DISTRIBUTION|SCHEMA_SOURCE_MANIFEST|SCHEMA_RECORD_CLOSURE|SCHEMA_DIRECT_URL|CANONICAL_CENSUS|DEPENDENCY_SEED|CENTRAL_SERVICE|CENTRAL_SUITE|D73_DRY_ROUTE|CORE_ROUTE|PROFILE|DISK_ADMISSION|RETAINED_ROOT|FARM_CURRENT_COMPOSITION_RECEIPT' ops-d140-farm/receive-farm.sh ops-d140-farm/receipts.py
```

PASS: Python AST parsing succeeded; the field scan found every mapped
production binding in the receiver or receipt checker at the line references
recorded in `input-map.json`.

## Not run by design

No child request, imports/product code, services, D134 controls, D124 core,
Store, acquisition/network, install/kit edit, cleanup, full suite, or Git
write was performed. No venue `READY`, finite-source `PASS`, or behavioral
qualification is claimed.
