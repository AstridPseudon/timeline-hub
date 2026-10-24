## Report

Read-only recheck completed; no repository files changed.

Findings:

- All five assigned names and parameters match the retained receipt:
  - three prior Runtime PASS cases;
  - two fork redo cases, retained as genuine FAIL→PASS.
- Test source files are byte-identical between current Agent `47b744dfe9` and held `e5fa8aac`:
  - source hashes: `526c2c…`, `bfb72c…`, `cd921e…`, `830287…`.
- Current home’s four fork failures are distinct: orders 11, 13, 98, and 99. They were not conflated with the assigned five.
- Relevant Agent and Runtime source refs/blobs were verified, including Runtime `becfe6db`.
- Normal publication is incomplete: `core159-ordinary.xml` and `core159-old276-map.tsv` are absent; only their hashes and aggregate results are recorded. Therefore I did not certify current-home PASS outcomes from aggregate counts.

Checks:

- `git diff --check`: PASS
- Worktree status: clean
- Tests/body reruns, full/gate/HTTP/browser checks: not run, as prohibited.

Blocked on Agent lead publishing the existing actual-home1330 XML and map artifacts at their normal refs. `BLOCKED` marker and commit message were written.