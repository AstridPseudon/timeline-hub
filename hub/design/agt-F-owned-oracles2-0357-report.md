## F-D86/D83 report

Changed only the two authorized originals:

- A: `test_owned_move_publish_runtime.py:174` now expects fresh v2 disjoint landing status `merged`; historical `rebased` behavior remains untouched.
- B: `test_prepared_video_birth.py:249` captures `vendored_runtime_commit()` once, uses `use_runtime(commit=...)`, and asserts qualified Runtime source/tree `6634…` / `47b…`. Frozen schema constants remain unchanged.

Evidence: [predicate-map-d83-log.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-owned-oracles2-0357/evidence/predicate-map-d83-log.md)

Checks passed:

- In-memory AST parse and compile
- Ruff candidate and parent baseline
- Mypy candidate and parent baseline
- `git diff --check`

No pytest, collection, services, or original behavior runs performed per source-only scope. Independent protected review and MAIN proof remain pending/unverified.

Commit message written; DONE marker created.