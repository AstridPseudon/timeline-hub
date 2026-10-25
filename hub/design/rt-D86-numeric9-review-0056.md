## FAIL_SOURCE — F-D86 numeric9

Found one bounded source failure: the fixture registers the Runtime provider at line 27, then registers it again at line 82. Pinned Runtime `732c48c6f5…` enforces startup-only registration and raises `ValidationError` before the tests can run.

Checks:

- In-memory AST parse/compile: passed
- Ruff: passed
- Mypy: passed
- `git diff --check`: passed
- Nine selectors, parameters, decorators, and assertion counts conserved
- No pytest, collection, fixture execution, service, or build run

No source files were changed. Evidence: [source-review.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D86-numeric9-review-0056/evidence/source-review.md).

Recommended next step: author removes the duplicate registration, then requeues the original author through the normal Agent path. `DONE` and the required commit message are present.