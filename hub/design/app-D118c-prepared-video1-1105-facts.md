# D118c prepared-video1 facts

- Status: source-aligned; behavior unverified. The retained node remains known red and was not run.
- Only changed path: `tests/editing_conformance/test_prepared_video_birth.py`.
- Setup correction: stale Runtime `6634a17f3ffd885567ba3c91b6c7a560df7375a4` / tree `47b376717ce7a919a697c62133de3e74dc9f6d3a` controls now match `runtime.lock.json`: released source `369ffa7c00bd3d45c610fac7651ff79e7a283a1a`, tree `9bf331d68df8c966e8927a3f083ba03687803c99`.
- The existing caller still uses `runtime_media.media_realm`, registers the `astrid` timeline commit provider, and submits through `runtime_media.commit`; no caller contract, media input, opaque value, timing, authored ID, request field, retry, undo, or no-write assertion was changed.
- Source hashes: retained/original 070dfc/parent `4cc89a0a7bbc4e1020e3ca9c676e7125113ee60c517bfdf5e3cd0821620cdc2c`; current `ba4acbcdee2a42c85ab7070a26983a59915ddcdfc395214761feb727c8e44476`.
- Retained failure-text hash: `8b471510787bc3c5c1ab572e71368d50af920ac7b3e11b3f9a1803d1c59fdf4e`.
- Conservation: `assert` AST identical to parent/original; target function statement count unchanged; diff is 3 insertions/3 deletions of setup identity literals.
- Static checks: Ruff PASS; mypy (`--follow-imports=skip`) PASS; `PYTHONPYCACHEPREFIX=$TMPDIR/pycache python -m py_compile` PASS; `git diff --check` PASS.
- No behavioral/source-functional closure is claimed. Full C0v2 request/reply, authenticated acceptance, prepared records, retry/undo, and no-write behavior still require the authorized later Runtime/Agent qualification run.
