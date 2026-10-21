# Runtime PRIVATE017 exact6c shared-fixture repair

Date: 2026-10-21 UTC

## Disposition

The common fixture setup defect was diagnosed and repaired with the smallest
permitted change. The first corrected central node reached its semantic body
but failed on the first existing order assertion. Per the task stop rule, the
second corrected node was not requested. No qualification, adoption, merge,
release, or activation claim is made.

## Cause and repair

`tests/test_timeline_owned_reference_integration.py` imported only the
existing `agent` fixture object from
`tests/test_timeline_commit_integration.py`:

```python
from test_timeline_commit_integration import agent
```

That fixture is defined as `agent(film, astrid_importable, monkeypatch)`.
`astrid_importable` is registered by `tests/conftest.py`, but `film` is a
module-local fixture in `test_timeline_commit_integration.py`. Importing the
fixture object alone made `agent` visible to pytest without registering the
defining module's `film` fixture. Pytest collection therefore succeeded, and
fixture lookup failed later during setup with `fixture 'film' not found`.

The narrow repair imports the existing fixture alongside `agent`:

```python
from test_timeline_commit_integration import agent, film  # noqa: F401 (shared fixtures)
```

This reuses the normal `film` implementation and its original semantics. No
fixture was copied or reimplemented.

## Exact diff and assertion/body proof

The only diff is one import line:

```diff
-from test_timeline_commit_integration import agent  # noqa: F401 (shared fixture)
+from test_timeline_commit_integration import agent, film  # noqa: F401 (shared fixtures)
```

`git diff --unified=0 -- tests/test_timeline_owned_reference_integration.py`
reports exactly one removed and one added import line. There are no changes to
either target's assertions, body, selector, marker, expectation, product
source, schema, generated file, lock, or suite configuration.

## Preflight

The successful all-prerequisite preflight used the exact normal tuple:

- Runtime `42a7203f49bb89f299ec854cfbf2b1444e815a7c` (tree
  `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`), with Runtime worktree source
  under test at base `aa0c26e0dafc6a749a1c8aae5ccfe971a1ce27d4`;
- Agent `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79` (tree
  `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`) at
  `/home/user/work/wt/agt-pin-6c1989ad`.

The read-only checks passed:

- Runtime artifact manifest current: 76 artifacts,
  `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`;
  Agent consumer lock: 15 files, exact producer bytes and commit;
- schema raw SHA-256
  `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`,
  canonical SHA-256
  `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`,
  65 definitions and 37 `EditCommand.allOf` clauses;
- Runtime/client metadata version `0.2.17`, schema digest
  `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd`;
  imports resolved from this Runtime worktree, the exact Agent checkout, and
  the Agent-vendored Runtime client; `authoring_profile=astrid`, provider
  interface 1 and matching contract digest;
- `pytest`, `jsonschema`, `referencing`, `filelock`, `Pillow`, and `PyYAML`
  resolved from `/home/user/work/venv-agent`;
- private temporary directory creation/removal passed; `/home/user/work` and
  `/tmp` each reported 10,597,472 KiB available; pinned external checkouts
  were clean and shared dependencies were not modified.

Exact one-node collection passed for each unchanged selector, with `1 test
collected` each. The no-body setup plans passed and showed the complete
closure for both nodes:

```text
tmp_path_factory -> tmp_path -> film
monkeypatch -> astrid_importable
film, astrid_importable, monkeypatch -> agent
```

`--setup-plan` reported `no tests ran` by design; it did not execute a
semantic body.

## Central results

The two prior unchanged-tree setup failures were:

- ordered node:
  `rt-m2-private017-ordered-exact6c-1006-private017-agent6c-integration-1021100753-27437`;
- original unplaced-reference node:
  `rt-m2-rt03-original-exact6c-1006-private017-agent6c-integration-1021100802-11493`.

Both stopped before the target body with `fixture 'film' not found`.

The one authorized corrected request made before the stop rule was:

```text
rt-m2-private017-shared-fixture-repair-1009-private017-agent6c-integration-1021101149-30759
```

It used the unchanged ordered selector, with central snapshot tree
`176558a5abda7f53ee786e86f22a935f4e54b463`, and ran:

```text
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6c1989ad PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo
```

The central command reported:

```text
1 failed in 1.15s
```

The fixture setup succeeded and the test entered its body. The first actual
failure was at line 263, before the remove/retry/inverse/redo assertions:

```text
assert list(original_app) == ["before", _ORDERED_TARGET, "after"]
E AssertionError: assert ["after", "before", "com.example.compiler-canary"] ==
  ["before", "com.example.compiler-canary", "after"]
```

Thus this result is semantic evidence of an ordering mismatch, not a fixture
failure. No body assertion was changed to accommodate it. The original
unplaced-reference corrected request was intentionally not submitted after
this first further failure. No third attempt or alternate selector was run.

## Blocker and next step

The corrected fixture repair is proven, but the requested pair of workflow
proofs is blocked by the first actual failure: seeded `config.app` key order
does not match the existing expected order. The Runtime/Agent manager should
decide whether that mismatch is an existing product behavior defect or an
invalid expectation in the unchanged test. Any follow-up must preserve the
existing assertions and separately authorize a new run; this worker made no
speculative rewrite.
