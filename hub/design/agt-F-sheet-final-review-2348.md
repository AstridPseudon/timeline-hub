## PASS_SOURCE — F-D85/D86

Reviewed `351cc76478` cumulatively against `a7056a277` and the current production caller.

- Only assigned file changed.
- All 7 test bodies, decorators, and parameter expansions preserved.
- Sequential `track.create` capture/apply repaired.
- Internal registry uses genuine tagged `ABSENT`.
- No synthetic seed, SQL/history fabrication, retired writer, or weakened assertion.

Checks:

- In-memory compile: PASS.
- Scoped Ruff candidate/baseline: PASS.
- Scoped mypy candidate/baseline: PASS; no issues.
- `git diff --check`: PASS.
- No pytest, service, build, render, or function execution run.

Normal merge completed: `672250b4be`. Source, home integration, and review blobs match: `164fc9406b6a2703cdf131087b7770bd2748d404`.

Functional qualification remains pending the single affected-node batch on MAIN. Shared native-batch blocker remains with its existing owner. `DONE` created.