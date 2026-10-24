# PASS_SOURCE

Implemented `F-D85` in `tests/editing_conformance/test_native_batch_ingress.py`:

- Rewired helper through real `timelines commit` parser → `commit_document`.
- Preserved captured files, pins, retries, and all original test AST content.
- No legacy aliases or direct `commit_many` shortcut remains in the CLI helper.
- Wrote commit message and `DONE` marker.

Checks passed:

- Baseline/candidate in-memory compile
- Baseline/candidate Ruff
- Baseline/candidate mypy
- `git diff --check`
- AST map identical: `6f170cc8…6c787c`
- Candidate source hash: `c3ece031…49da3f53`

No pytest, service, build, or full suite run per D85.

Product seam to log: current `commit_document` uses detached-document G2 emission, which may produce `doc.patch` and defaults Runtime source metadata through Python; retained native-command/`via=cli` behavioral assertions therefore remain functionally unverified pending existing CLI capability.