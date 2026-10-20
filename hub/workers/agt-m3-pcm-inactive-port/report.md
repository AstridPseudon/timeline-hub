Implemented the approved inactive PCM port: exactly 10 paths, 319 product lines, byte-identical to `tl/vw-m3-pcm-current-landing-batch` (`ab935f77`). Ten-path tree: `174d50cfb58e8d935ef33c8421142f300fbffa6a`.

Tests:

- Python: `103 passed, 2 xfailed` (strict compile-contract xfails preserved).
- Node: `5 + 8 + 4 + 2 = 19 passed`.
- Ruff and `git diff --check`: passed.
- No full suite run.

Private overlay used worktree-owned helpers with read-only public12 dependencies; shared runtimes/node_modules were untouched. The exact central named-lane command is recorded in [central-private-lane-command.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-pcm-inactive-port/central-private-lane-command.md). Central execution remains pending lane registration; the existing lane is the known missing-helper-path failure.

Unresolved by design: source-pair authority validation, malformed trusted-map diagnostics, successful WAV/server lifetime integration, and compile/slice non-commutation. Normal activation, source carry, compiler, pins, DSP, and server lifetime were not changed.

Commit message: [commit-msg](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-pcm-inactive-port/commit-msg). DONE marker created.