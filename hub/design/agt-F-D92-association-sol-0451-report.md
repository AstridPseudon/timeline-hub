Updated only [test_authoring_media.py](/home/user/work/wt/agt-F-D92-association-sol-0451/tests/timeline/test_authoring_media.py:538).

- Bootstrap now consumes the genuine catalog association.
- A adds the audio consumer alongside the original graph; B removes that addition through normal edits.
- All 207 original assertions remain; two assertions now verify restored graph and unused-pin state.
- Independent protected review: **PASS_SOURCE**. No product, admission, schema, lock, or ledger changes.

Checks passed on baseline and candidate:

- Scoped Ruff and mypy.
- In-memory AST parse/compile and assertion preservation.
- `git diff --check`.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D92-association-sol-0451/evidence/checks.txt). No pytest, collection, fixtures, services, probes, or suites ran.

Current source explicitly retains prior CAS pins, supporting the D92 setup correction rather than legacy retirement. Functional reachability remains unverified; actual6058’s failure phase is **UNKNOWN**.

Next: orchestrator delivery of the [existing-artifact phase request and exact three-case MAIN handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D92-association-sol-0451/evidence/peer-safe-phase-request.md).

Commit message written with F-D86/D92; `DONE` created.