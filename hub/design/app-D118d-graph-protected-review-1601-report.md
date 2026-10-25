# D118d independent protected review

- Source semantics: PASS. Only the six-line v2 envelope addition exists; AST/input/assertion/decorator conservation verified. Genuine registered Runtime route used; no fake acceptance or source edits.
- Own9 functional proof: FAIL. Exact nine-node run executed once at 5,017,751,552 free bytes; all 9 failed before assertions because Runtime rejects existing `gain: null` as requiring a number.
- Full core: PENDING; not run.

Static checks passed:

```text
ruff check tests/sdk/test_timeline_commit_graph_roots.py
mypy --follow-imports=skip tests/sdk/test_timeline_commit_graph_roots.py
python -m py_compile tests/sdk/test_timeline_commit_graph_roots.py
git diff --check
```

Evidence is recorded under `evidence/`, including `own9.xml`, private `own9.log`, verdict, custody, and command results. Runtime/fixture schema compatibility must be resolved before rerunning own9.