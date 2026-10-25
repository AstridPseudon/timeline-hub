# D118d commands and results

Working directory: `/home/user/work/wt/app-D118d-projection-Sol-protected-review-1616`

## Exact own9 selection

The exact retained nine nodeids were read from the author facts and were not changed:

```text
tests/sdk/test_timeline_capture_projection.py::test_real_saved_projection_config_registry_and_full_pins_golden
tests/sdk/test_timeline_capture_projection.py::test_real_saved_entire_expansion_golden
tests/sdk/test_timeline_capture_projection.py::test_saved_canonical_images_preserve_authored_fields_pins_order_and_read_rows
tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[parent]
tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[child]
tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[new_shot]
tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[duplicate]
tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[remove]
tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[sdk_bundle]
```

Fresh light-run admission was refused before dispatch. `df -B1 /tmp` reported `4,797,657,088` free bytes: `202,342,912` below the required `5,000,000,000` bytes. Ongoing stop was `4,000,000,000` bytes. The exact pytest command was therefore **NOTRUN**; no pytest subprocess, XML, or log was created.

## Static checks

```sh
/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_capture_projection.py
```

PASS, exit 0: `All checks passed!`

```sh
/home/user/work/venv-agent/bin/mypy --cache-dir "$TMPDIR/mypy" --follow-imports=skip tests/sdk/test_timeline_capture_projection.py
```

PASS, exit 0: `Success: no issues found in 1 source file`.

```sh
PYTHONPYCACHEPREFIX="$TMPDIR/pycache" /home/user/work/venv-agent/bin/python -m py_compile tests/sdk/test_timeline_capture_projection.py
```

PASS, exit 0.

```sh
git diff --check
```

PASS, exit 0.

## Read-only source and custody checks

The read-only AST/hash script reported:

- Agent HEAD `d05975c7d6a0ab9eeea2db0f1c6e97ccbe136b6b`, tree `6b7bc811f07abb169dcf8858f316af3fea589b4f`.
- Only `tests/sdk/test_timeline_capture_projection.py` differs from base `20177e66564f9f91735ed1a11bac821682d60edf`.
- Current file SHA-256 `6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436`; base SHA-256 `90c4625a7481fdcd570ec8b85bbe95325f4d3c57f0a3a26017dd405b8269b638`.
- Original assertion count 43, current count 44; original assertion AST multiset is a subset of current.
- There are 11 `test_*` functions in both files and their ASTs are equal.
- Original `saved_closure` statements remain an ordered subsequence.
- Runtime pin HEAD/tree are `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` / `de2954a0ceadb4455903d9abdfec3b773318a50f`; porcelain is empty.
- `git cat-file -e 92443771676ef2bbb547d0a103d708fa8bec4c63:tests/sdk/test_timeline_capture_projection.py` exits 128 because the D120 target is absent.

No source, product, test, generated, pin, or Git files were modified.
