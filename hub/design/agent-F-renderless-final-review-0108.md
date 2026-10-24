## Verdict: PASS

Reviewed `b150041aa` cumulatively against rejected `f5023e960`.

- Public `open_composition()`/`show()` retain all six timing fields.
- `_RemoteTimelineRevisionMixin.open_bundle()` forwards `_raw_projection=True` through the actual authoring/save path.
- Raw projection remains renderer-free and preserves native diagnostics/summary.
- Closure round-trip test passed.

Tests/checks:

- Targeted facade/save/timing: **75 passed**
- Closure round-trip: **1 passed**
- Direct six-field identity probe: **passed**
- Vendor lock, artifact manifest, diff check: **passed**
- Mypy: **12 errors, exactly matching f502 parent baseline**
- Ruff: changed neighboring files pass; `remote.py` retains existing baseline diagnostics.
- Current-pair archive tests unavailable: `ASTRID_AUTHENTIC_LEGACY_ARCHIVE` is unset.
- Existing normal-publish fixture evidence remains **52 passed, 6 known closure-membership failures**, originating at `publish.py:249`; not renderer-related.

Clean import plan: do not cherry-pick the f502 ancestry. Apply the verified final-state diff `ca93d63bd..b150041aa` to the clean current agent head; `git apply --check` passed.

No worktree changes or merge performed.