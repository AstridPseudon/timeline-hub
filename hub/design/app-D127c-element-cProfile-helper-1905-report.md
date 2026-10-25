## Completed

- Added opt-in stdlib `cProfile`/`pstats` profiling for only mounted `clip.set-element` commits at `RuntimeHandler._timeline_commit`.
- Added bounded TOP40 function data and caller→callee edges with redacted paths and private raw-stat support.
- Preserved existing helper behavior and privacy/lifecycle semantics.
- Added focused predicate, exception, privacy, bounds, and permission tests.
- Modified only the two assigned files.

## Validation

- Central targeted suite: **26 passed**.
- Offline focused suite: **24 passed, 2 deselected**.
- Python 3.11 compile: passed.
- Ruff on both files: passed.
- `git diff --check`: passed.

The two local socket tests were blocked by sandbox `EPERM`; central testing passed them.

Evidence and commit message are in the required worker directory. The manager-independent privacy/selection review remains required before normal integration.