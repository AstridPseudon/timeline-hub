# Report

**Independent fixture / no-weakening result: PASS.**

- Verified target ASTs against fullc36: both functions byte/AST-equivalent in decorators, parameters, and assertions.
- Confirmed mapping uses actual `realm.entries`, revision boundaries, `inverse_address_resolver`, and `select_inverse_records`; no invented authority or guard bypass.
- Collected exactly 22 cases: 16 corruption + 6 retained-document cases.
- Source custody: Agent `2007cf7a…`, Runtime `/home/user/work/wt/rt-pin-2b49da8d` at `2b49da8d…`; source-mode imports verified pre/post.

Qualification command ran once:

```text
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-2b49da8d" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2b49da8d /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider tests/editing_conformance/test_occurrence_media_manifest_inverse.py::test_corrupt_media_boundary_refuses tests/editing_conformance/test_occurrence_media_manifest_inverse.py::test_retained_document_scope_is_required_before_removing_media --junitxml="${TMPDIR}/inverse22.xml"
```

Result: **22 passed in 3.55s**, all named outcomes passed. Negative controls reached their protected boundary assertions.

No product/test edits, full suite, browser run, or installed overlay used. Evidence and JUnit are under the worker evidence directory. Later orchestrator review/count credit remains required.