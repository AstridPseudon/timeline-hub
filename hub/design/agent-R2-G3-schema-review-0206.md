# PASS — agent R2/G3 schema review

- Exact commit/tree: `68f2b23ff73d901402cdf63931b8662f7e3f1205` / `45bccffd4bb49697b4a5684bc86bea961ba19ee4`.
- True parents: `5a313eb88e8ddce1e9e033ed9cfde7ef433f7c55`, `f2521256c2f705d7baac8e9a4d27fce02b5bc2cc`.
- Exact delta: only canonical `astrid/core/timeline/schema/edit-command.schema.json` and `tests/sdk/test_timeline_composed_schema.py`, `tests/sdk/test_timeline_current_union_schema.py`; no deletions.
- Canonical schema SHA256: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- R2 `4454a7a2f` provider files and G3 public-hydration/compound-inverse guards retained; production caller and v2 request/reply fields remain unchanged.
- Targeted pytest: `77 passed`; scoped Ruff: pass; private mypy: pass; normal ratchets Ruff `2150/2150`, mypy `1915/1915`; `git diff --check`: pass.
- Official Runtime v2 wire/restart remains pending; no full suite, browser, shared dependency write, or Git mutation performed.

