# D118d independent protected review commands

All source checks ran before the functional test admission.

```text
/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_commit_graph_roots.py
PASS — All checks passed!

/home/user/work/venv-agent/bin/mypy --cache-dir /tmp/w-e7dfb94f4a/mypy --follow-imports=skip tests/sdk/test_timeline_commit_graph_roots.py
PASS — Success: no issues found in 1 source file

PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-e7dfb94f4a/pycache /home/user/work/venv-agent/bin/python -m py_compile tests/sdk/test_timeline_commit_graph_roots.py
PASS

git diff --check HEAD^ HEAD -- tests/sdk/test_timeline_commit_graph_roots.py
PASS

git diff --check 92443771676ef2bbb547d0a103d708fa8bec4c63 HEAD -- tests/sdk/test_timeline_commit_graph_roots.py
PASS

git cat-file -e 92443771676ef2bbb547d0a103d708fa8bec4c63:tests/sdk/test_timeline_commit_graph_roots.py
EXPECTED ABSENCE — target file is not present in upstream reference

Independent AST inventory and conservation comparison against HEAD^:
PASS — 11 test functions, 33 assert nodes, 7 parametrization calls; test bodies, decorators, assertions, inputs, cases, and patches equal.
```

## Exact nine-node run

Command used exactly once after the fresh filesystem check reported 5,017,751,552 available bytes and the clean Runtime pin was verified:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-graph-protected-review-1601/evidence/own9.xml tests/sdk/test_timeline_commit_graph_roots.py::test_typed_roots_are_valid_local_creations_and_retired_roots_are_reserved 'tests/sdk/test_timeline_commit_graph_roots.py::test_bad_typed_creation_history_refuses[shot-owner]' 'tests/sdk/test_timeline_commit_graph_roots.py::test_bad_typed_creation_history_refuses[occurrence-owner]' 'tests/sdk/test_timeline_commit_graph_roots.py::test_bad_typed_creation_history_refuses[kind]' 'tests/sdk/test_timeline_commit_graph_roots.py::test_bad_typed_creation_history_refuses[ref]' 'tests/sdk/test_timeline_commit_graph_roots.py::test_bad_typed_creation_history_refuses[claim]' tests/sdk/test_timeline_commit_graph_roots.py::test_trusted_inverse_recreation_keeps_identity_reservation tests/sdk/test_timeline_commit_graph_roots.py::test_authenticated_root_creation_reload_inverse_redo_exact_closure tests/sdk/test_timeline_commit_graph_roots.py::test_authenticated_created_child_stages_reload_inverse_redo_exact_closure
EXIT 1 — 9 failed in 14.18s
Safe common failure: runtime_protocol.errors.ValidationError; invalid PreparedCommit: None is not of type 'number'; canonical_document.parent_revision.payload.occurrences[2].gain; expected number, observed null.
```

Raw XML and log are retained privately in `own9.xml` and `own9.log`; no payload is reproduced here.

No full suite, family suite, browser, socket, probe, acquisition, or extra functional run was performed.
