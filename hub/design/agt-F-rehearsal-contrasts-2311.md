Implemented F setup correction.

- Root cause: service ran under `env -i` without `PATH`; `git`, `ffmpeg`, and `ffprobe` were unavailable. The `basis` KeyError was downstream of missing ffprobe/ffmpeg, not a product regression.
- Added the owned exact-18 rehearsal row with genuine tool PATH and `/usr/bin` preflight guards.
- Updated CAS helper to install only the requested owned row while preserving unrelated registry bytes.
- No product code or test expectations changed.

Validation:

- Exact-18 central rerun: `18 passed in 12.70s`.
- `python3 -m py_compile tools/install_p4_launcher.py` — pass.
- `bash -n tools/p4-d73-pinned-launch.sh` — pass.
- `git diff --check` — pass.
- Lossless XML comparison: 7 prior failures + 11 errors, all 18 upstream-pass; rerun positive-once and poison-zero confirmed.
- Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-rehearsal-contrasts-2311/evidence/`

No blockers. No full-suite or gate credit inferred. Commit message and `DONE` marker created.