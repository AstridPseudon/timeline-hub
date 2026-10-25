Implemented the D107 custody-only correction.

- Added [correction.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D107-custody-correction-1644/evidence/correction.json) and [validation.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D107-custody-correction-1644/evidence/validation.md).
- Corrected the protected SHA-256 to `23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041`.
- Preserved original 1550/1640 artifacts byte-exact.
- Retained `UNKNOWN`, `EXACTMISSING`, both failed journeys, and non-GO behavior status.
- JSON validation, exact hash checks, invariance checks, and `git diff --check`: PASS.
- No product or behavior tests run; static-only evidence task.
- Wrote commit message and `DONE` marker.