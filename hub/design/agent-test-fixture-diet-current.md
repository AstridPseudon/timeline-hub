# Agent fixture diet: scalar M2 recipe family

## Scope and decision

Selected one family only: the five `recipe_m2_scalar_*` portable capture
cases consumed by `tests/editing_conformance/test_recipe_scalar_commands.py`.
The cases remain distinct: `track`, `params_absent`, `params_null`,
`params_object`, and `disjoint`. No product, schema, Runtime pin, published
schema floor, frozen M1 capture, or exported shared handoff fixture changed.

The four clip-parameter JSON captures repeated the same large timeline input
and nearly the same full after-document. The absent-params capture remains the
single shared hand-authored input source. The other three retain their full
independent command/request/read/expectation goldens and now carry only an
independent expected patch. `fixture_loader.py` expands that patch into a full
expected document by copying the input and applying literal path assignments;
it never calls production capture, execute, compiler, or capture-provider code.
The object case records deletion of `params.old` explicitly, preserving the
absent-vs-null distinction.

## Exact paths and physical size

Changed paths:

- `tests/editing_conformance/fixture_loader.py`
- `tests/editing_conformance/test_recipe_scalar_commands.py`
- `tests/editing_conformance/fixtures/recipe_m2_scalar_params_absent.json`
- `tests/editing_conformance/fixtures/recipe_m2_scalar_params_null.json`
- `tests/editing_conformance/fixtures/recipe_m2_scalar_params_object.json`
- `tests/editing_conformance/fixtures/recipe_m2_scalar_disjoint.json`

`tests/editing_conformance/fixtures/recipe_m2_scalar_track.json` was not
changed. No fixture path was deleted. Removed JSON data is the repeated
`after_bundle` from all four changed files, and the repeated `bundle` from the
null/object/disjoint files; the loader reconstructs the same complete values.

| case | before bytes | after bytes | before lines | after lines |
|---|---:|---:|---:|---:|
| params_absent | 10,763 | 6,667 | 1 | 1 |
| params_null | 10,805 | 2,447 | 1 | 1 |
| params_object | 10,730 | 2,724 | 1 | 1 |
| disjoint | 18,806 | 10,339 | 1 | 1 |
| track (unchanged) | 2,606 | 2,606 | 1 | 1 |
| **total** | **53,710** | **24,783** | **5** | **5** |

Net fixture reduction: 28,927 bytes (53.9%). The selected consumer test grew
from 448 to 450 physical lines; the shared loader grew from 78 to 127 lines.

## Equivalence and tests

Before editing, the selected consumer baseline passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_scalar_commands.py tests/editing_conformance/test_fixture_loader.py
75 passed in 11.49s
```

After editing, the same selected family and portable subprocess parity lane
passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_scalar_commands.py tests/editing_conformance/test_fixture_loader.py
75 passed in 12.76s
```

An independent comparison loaded each compact fixture through the new loader
and compared it to the pre-edit `HEAD` JSON for all five cases:

```text
params_absent expanded-equivalent
params_null expanded-equivalent
params_object expanded-equivalent
disjoint expanded-equivalent
track expanded-equivalent
all 5 scalar expanded fixtures exactly match pre-edit JSON
```

Additional checks:

```text
ruff check tests/editing_conformance/fixture_loader.py tests/editing_conformance/test_recipe_scalar_commands.py
All checks passed!

pyright tests/editing_conformance/fixture_loader.py
0 errors, 0 warnings, 0 informations

git diff --check
pass
```

No full or localhost suite was requested. No remaining uncertainty is known
within this selected fixture family.
