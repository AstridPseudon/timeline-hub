# D132 protected review commands and results

All source checks ran in `/home/user/work/wt/app-D132-graph-protected-own9-1632`.

- `git diff --stat 20177e66564f9f91735ed1a11bac821682d60edf -- tests/sdk/test_timeline_commit_graph_roots.py tests/editing_conformance/test_recorded_graph_roots.py` — PASS; 2 files, 7 insertions, 1 deletion.
- `git diff --unified=0 20177e66564f9f91735ed1a11bac821682d60edf -- tests/sdk/test_timeline_commit_graph_roots.py` — PASS; exactly six v2 metadata additions (`label`, `steps`, `merge`, `reads`).
- `git diff --unified=0 HEAD^ HEAD -- tests/editing_conformance/test_recorded_graph_roots.py` — PASS; exactly one `gain: None` to `gain: 1` line.
- AST/input conservation script — PASS; fixture 22 bodies/90 assertions/6 parametrizations and graph 11 bodies/33 assertions/7 parametrizations are unchanged; test-body, assertion, and parametrization ASTs are equal; fixture source is equal after canonicalizing only the approved gain literal.
- Actual Agent D60 path check in `/home/user/peteromallet/astrid-agent` — PASS; commit `92443771676ef2bbb547d0a103d708fa8bec4c63` exists and both graph paths are absent from its tree.
- Frozen R4 SDK path check — PASS; `origin/codex/handover-timeline-r4-20261019-candidate-sdk` resolves to `11caf1d9de291d76f491cf69f7942606b7471d7a` and both graph paths are absent.
- Fixture history check — PASS; introduction `84db8bde88f695fede81f32a2fddb30622c6781f` adds the fixture path and its parent lacks it.
- Consumer purpose census — PASS; the graph consumer and `semantic_reservations`/`created_root_stage_redo` contain no gain/null-purpose assertion.
- `ruff check tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py` — PASS (`All checks passed!`).
- `MYPY_CACHE_DIR=/tmp/w-6ebd901b0a/app-D132-graph-protected-own9-1632/mypy-cache /home/user/work/venv-agent/bin/mypy --cache-dir /tmp/w-6ebd901b0a/app-D132-graph-protected-own9-1632/mypy-cache tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py` — PASS (`Success: no issues found in 2 source files`).
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-6ebd901b0a/app-D132-graph-protected-own9-1632/pycache /usr/bin/python3.11 -m py_compile tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py` — PASS.
- `git diff --check` — PASS.
- `git status --short --branch` — PASS; worktree clean.

Pinned Runtime verification: `/home/user/work/wt/rt-pin-5e9ad1c6` is clean at commit `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree `de2954a0ceadb4455903d9abdfec3b773318a50f`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D132-graph-protected-own9-1632/evidence/own9.xml tests/sdk/test_timeline_commit_graph_roots.py::test_typed_roots_are_valid_local_creations_and_retired_roots_are_reserved tests/sdk/test_timeline_commit_graph_roots.py::test_bad_typed_creation_history_refuses[shot-owner] tests/sdk/test_timeline_commit_graph_roots.py::test_bad_typed_creation_history_refuses[occurrence-owner] tests/sdk/test_timeline_commit_graph_roots.py::test_bad_typed_creation_history_refuses[kind] tests/sdk/test_timeline_commit_graph_roots.py::test_bad_typed_creation_history_refuses[ref] tests/sdk/test_timeline_commit_graph_roots.py::test_bad_typed_creation_history_refuses[claim] tests/sdk/test_timeline_commit_graph_roots.py::test_trusted_inverse_recreation_keeps_identity_reservation tests/sdk/test_timeline_commit_graph_roots.py::test_authenticated_root_creation_reload_inverse_redo_exact_closure tests/sdk/test_timeline_commit_graph_roots.py::test_authenticated_created_child_stages_reload_inverse_redo_exact_closure
```

- Exact own9 command — RUN; preflight available space was 5,042,114,560 bytes and postflight was 5,041,680,384 bytes. All 9 exact nodes failed in 13.61s.
- Own9 failure class — all failures reached the registered `astrid` provider and were refused by the frozen Runtime `PreparedCommit` schema at `runtime_protocol/timeline_commit_validation.py:173`; the underlying path was `canonical_document.shot_revisions[1].payload.metadata`, with `None is not of type object`. The caller surfaced `prepared commit does not satisfy the frozen schema`.
- Own9 node disposition — all nine requested nodes failed: one unparameterized reservation test, five `test_bad_typed_creation_history_refuses[...]` cases, and the three trusted/inverse/closure tests. See private `own9.xml` and `own9.log` for raw details.

No source fix, retry, alternate route, ambient Runtime, or additional suite was used after failure. No pytest family/full/browser/native/P2/P4/collector/profile/service suite was run.
