# P1 vector correction independent

## Base

649ba6481922782346864e3c2ca76a6051b0a7a3

## Donor SHA

d8e1578bd9f717eb975addb50c2654de70815475

## Diff

```
M	tests/sdk/fixtures/p1_feasibility/doc_patch_requests.json
M	tests/sdk/test_p1_doc_patch_requests.py
 .../p1_feasibility/doc_patch_requests.json         | 78 ++++++++++++++--------
 tests/sdk/test_p1_doc_patch_requests.py            | 74 ++++++++++++--------
 2 files changed, 96 insertions(+), 56 deletions(-)
```

Donor/worktree SHA-256:

```
tests/sdk/fixtures/p1_feasibility/doc_patch_requests.json 85518dbec312ba8b02c94cf799e52f53e714492bf3f059b2734d72d3ec63cdbe
tests/sdk/test_p1_doc_patch_requests.py 3b6b33b114ad1e21d1495d206f694b221ec9d109d84bc448e10f84dd3ea9df16
```

Source fixture hash comparison:

```
tests/editing_conformance/fixtures/recipe_m2_clip_trim.json expected=60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c actual=60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c match=True
tests/editing_conformance/fixtures/recipe_m2_clip_add.json expected=cebe45dbf6806c2fb772665ad2c3a416eae172df48d1b0cc48d023cbc80345ff actual=cebe45dbf6806c2fb772665ad2c3a416eae172df48d1b0cc48d023cbc80345ff match=True
tests/editing_conformance/fixtures/recipe_m2_scalar_params_absent.json expected=9687956ee3850c5d873580a28cd6e8354f0b76dcb9a17bf56eb6ae0213f24b36 actual=9687956ee3850c5d873580a28cd6e8354f0b76dcb9a17bf56eb6ae0213f24b36 match=True
tests/editing_conformance/fixtures/recipe_m2_scalar_params_null.json expected=15e945496b805af2554d78777be4585aa684615de575960352376f1dd4eaba74 actual=15e945496b805af2554d78777be4585aa684615de575960352376f1dd4eaba74 match=True
tests/editing_conformance/fixtures/recipe_m2_scalar_params_object.json expected=ae9f96e55432d0cf892f6045285e56265c6adc66058caf146bf4a7d7b1869638 actual=ae9f96e55432d0cf892f6045285e56265c6adc66058caf146bf4a7d7b1869638 match=True
tests/editing_conformance/fixtures/recipe_m2_scalar_disjoint.json expected=0aab88bff6040ad741771fe8ed2198c141347970420ede78a981ba1416f6e866 actual=0aab88bff6040ad741771fe8ed2198c141347970420ede78a981ba1416f6e866 match=True
```

## Commands and logs

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_requests.py tests/sdk/test_p1_case_corpus.py
..................                                               [100%]
25 passed, 1 warning in 4.10s
warning: Unknown config option: timeout

/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_requests.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_requests.py
Success: no issues found in 1 source file

git diff --check
clean (no output)
```

