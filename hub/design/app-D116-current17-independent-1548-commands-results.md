# D116/D118d commands and results

Working directory: `/home/user/work/wt/app-D116-current17-independent-1548`.

## Identity and custody

```text
git rev-parse HEAD
20177e66564f9f91735ed1a11bac821682d60edf

git show -s --format='%H%n%T%n%s' HEAD
20177e66564f9f91735ed1a11bac821682d60edf
68433c5f77be90063b1f43d3e8f1407346a50675
Merge tl/agt-D124-current-word-root-1428
```

JSON parsing, exact 27-minus-10 ordinal difference, selector equality, AST
function/case matching, alias/provider seam checks, and source SHA-256 checks
were run with Python 3.11/3.13 read-only scripts. Result: ordinals, selectors,
AST/cases, and seven of eight recorded hashes PASS; one supplied scalar hash is
malformed/mismatched. Full details are in `verdict.json` and
`source-custody.json` in this directory.

## Scoped static checks

The seven mapped files were exactly:

```text
tests/editing_conformance/test_commit_runtime_native_checkout.py
tests/editing_conformance/test_commit_runtime_native_frontends.py
tests/editing_conformance/test_commit_runtime_parent_track_batch_inverse.py
tests/editing_conformance/test_commit_runtime_parent_track_label.py
tests/editing_conformance/test_commit_runtime_scalar.py
tests/editing_conformance/test_owned_move_publish_runtime.py
tests/editing_conformance/current_word_baseline_fixture.py
```

Commands and results:

```text
PYTHONPYCACHEPREFIX=/tmp/w-99c7676352/app-D116-current17-independent-1548/pycache311 \
  /usr/bin/python3.11 -m py_compile <the seven files>
PASS

PYTHONPYCACHEPREFIX=/tmp/w-99c7676352/app-D116-current17-independent-1548/pycache \
  /home/user/work/venv-agent/bin/python -m py_compile <the seven files>
PASS

/home/user/work/venv-agent/bin/ruff check <the seven files>
All checks passed!

/home/user/work/venv-agent/bin/mypy --follow-imports=skip \
  --cache-dir /tmp/w-99c7676352/app-D116-current17-independent-1548/mypy-cache \
  <the seven files>
Success: no issues found in 7 source files

git diff --check
PASS

git status --porcelain=v1
empty
```

No pytest, central test service, Runtime service, socket, browser, native,
P2/P4, full, family, probe, collector, build, profile, replay, or acquisition
command was run, per task scope.
