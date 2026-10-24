Implemented the three-checker `no_ci` restoration in [tests/test_skip_registry.py](/home/user/work/wt/rt-U1-D69-three-checkers-1633/tests/test_skip_registry.py:337).

- All 3 checker bodies now exactly match upstream `d4f496ec4`.
- Required suite: **29 passed**.
- Compile and diff checks passed.
- Ruff: only inherited B023 diagnostics.
- Pyright: inherited diagnostics only; none affect changed lines.
- `tests/lanes.py` and `tests/test_skip_guard.py` match policy-1616.
- Evidence: [all29.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-D69-three-checkers-1633/evidence/all29.xml), [source-hashes.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-D69-three-checkers-1633/evidence/source-hashes.txt).
- Commit message written; `DONE` marker created.
- No full suite run.