# D118d facts

- The only product change is in `tests/sdk/test_timeline_commit_graph_roots.py`: `RuntimeRealm.call` now supplies current-contract `label`, one semantic `steps` entry covering the submitted command batch, `merge: fields`, and `reads: []`.
- The nine handoff nodes are recorded in `facts.json` with their full node IDs, original source SHA, and failure-text SHA. The handoff failures all pointed at the historical Runtime validator boundary; no current own-node result is claimed.
- AST conservation: 33 assertion nodes before and after; assertion ASTs equal; seven parametrization decorators before and after. All command inputs and existing assertions remain unchanged.
- The target file is absent at upstream commit `92443771676ef2bbb547d0a103d708fa8bec4c63`, as required for this test-only addition.
- Static checks passed: py_compile, Ruff, mypy, and `git diff --check`.
- Exact-nine current Runtime check was NOTRUN because available free space was 4,953,280,512 bytes, below the required 5,000,000,000-byte floor.
