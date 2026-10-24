**BLOCKED: no product correction applied.** P4 line 113 expects an ordinary revision read, but its earlier `_bundle()` call explicitly authenticates the revision/publication pair under `d05fcc0766c`. Passing public-session controls require that custody. Exact source/decision seam is recorded in [source-seam.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G2-P4-read-boundary-sol-1639/evidence/source-seam.json).

Added one focused regression file with two passing controls covering ordinary reads, authenticated session/sheet capture, private execution custody, and wrong-pair refusal without writes.

Validation:

- New controls: **2 passed**.
- Targeted neighbors: **53 passed, 2 failed**. Both failures are repeated-source-copy redo cases at line 335: `original authored guard changed`. No broader cause claimed.
- Scoped Ruff: **0 new**, 6 existing findings. Scoped mypy: **0 new**, 1 existing finding.
- Vendor/artifact checks and diffcheck passed; original P4 bytes and all 15 canonical mappings preserved.
- Exact commands/environment: [commands.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G2-P4-read-boundary-sol-1639/evidence/commands.json).

P4 was not repeated on unchanged product source; its existing HTTP verdict remains FAIL.

Recommended next step: resolve the inspection-versus-authenticated-capture contract before authorizing a correction. `commit-msg` and `BLOCKED` were written; no `DONE` marker.