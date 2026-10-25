# OPS portable fixture final review

Verdict: **FAIL**.

## Actual source identity

Git resolved the reviewed final source to commit `2fffe593175338ffb8144705bb70c9542fa4459f`, tree `516da69731401037b6845f1e14ea11b4c9135628`, parent `674d13e26ce40ce9a158a7e50b226c247fbc9588`. The author’s `674d` label is the historical parent/input, not the final reviewed source. The runner SHA-256 is `f02fdcca8ad7c9484866b1817bb67272212933c4576d2212c2d163a07edf1c96`.

The final source diff against `674d` contains only:

```text
M ops-child-custody/tests/e2e_inventory.py
A ops-child-custody/tests/test_e2e_inventory.py
```

## Findings

1. The added test fails scoped Ruff:

   ```text
   /root/.local/bin/ruff check --no-cache ops-child-custody/tests/test_e2e_inventory.py
   exit 1
   I001 import block is un-sorted
   RUF059 unpacked variable `maker` is never used
   ```

   The runner’s two Ruff diagnostics (I001 and PLW1510) are also present in the `674d` baseline; the new test’s RUF059 is new. The combined scoped command therefore fails and cannot be accepted as a clean final review.

2. The complete-census guarantee still has an uncaught malformed-manifest path. With `roles.dependency-dot` set to a JSON list and a wheelhouse supplied, `check_only` raises `AttributeError: 'list' object has no attribute 'get'` from `fixture_wheel_pins()` rather than writing/returning the complete census. The probe used only a private temporary manifest and missing prerequisite paths; it started no setup, Git mutation, Store, maker, or body.

The two independent1847 findings are fixed: clean carrier committed blobs are hashed with `git cat-file` against manifest hashes, and missing/malformed source files are accumulated in the normal missing-file control. `tests/suites.conf` is still written before the two unchanged `Store.initialize` calls.

## Validation commands

| Command | Result |
| --- | --- |
| `git show -s --format='%H %T %P' HEAD` | PASS; `2fffe593… 516da697… 674d13e…` |
| `git diff --check 674d13e..HEAD -- ops-child-custody/tests/e2e_inventory.py ops-child-custody/tests/test_e2e_inventory.py` | PASS, exit 0 |
| `git diff --check f6b9d4d..HEAD` | EXIT 2, exactly the two disclosed frozen-maker EOF diagnostics |
| Manifest source/mode, maker, helper, dependency, verifier-block hash script | PASS, 37 checks |
| New census controls (two exact unittest methods) | PASS, 2/2 |
| `PYTHONDONTWRITEBYTECODE=1 python -m py_compile` on changed Python files | PASS, exit 0 |
| AST parse on changed Python files | PASS |
| `/root/.local/bin/ruff check --no-cache` on both changed files | FAIL, exit 1; new test I001/RUF059 plus baseline runner I001/PLW1510 |
| Changed test only Ruff | FAIL, exit 1; I001/RUF059 |
| `/root/.local/bin/pyright` on new test | PASS, 0 errors |
| `/root/.local/bin/pyright` on runner | 5 errors at unchanged pre-existing helper/optional-value sites; no new test diagnostics |
| Malformed `dependency-dot` role census probe | FAIL; uncaught `AttributeError` |

The author1855 evidence retains its 42/42 targeted regression PASS; this review did not duplicate those unrelated 40 controls. No full suite, genuine whole-maker E2E, Store initialization, production install/request, package acquisition, network/socket, browser, provider/core, ZIP, or D130 action was run. Available-space admission remains below the unchanged `5905580032`-byte reserve; the `4000000000`-byte stop line was not changed.

## Immutable input accounting

Parent maker SHA-256 is `0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`, candidate maker SHA-256 is `c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e`; both remain mode `100755`. The protected Store helper is `123bb93c…b7adfe2`, dependency helper `116b4e6b…d7bfe2`, and parent/candidate verifier blocks are identical with hash `f7c7ebcc…5eda209`. The two historical EOF whitespace diagnostics remain disclosed and were not trimmed.
