Fixed both acceptance gaps before writes and composed complete frozen S2 plus word anchors: **50 definitions / 23 operations**. Stable-ID, retained-transcript and revision-only restore cases pass. No pins or other writers changed.

Validation:

- Exact reproducers: **2 failed before**, pass after.
- Final targeted acceptance/kernel tests: **145 passed**.
- Original portable/neighbor tests: **453 passed**.
- Composition/schema tests: **258 passed**.
- Generator, `--check`, changed-file Ruff and whitespace checks passed.

Runtime evidence uses an **unpublished, normally generated private candidate**. No published pair, full suite or live transport qualification is claimed.

[Detailed report with exact commands, hashes and limitations](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-word-anchor-acceptance-fix/notes/report.md).

`commit-msg` and `DONE` are written. No blockers; coordinated consumer qualification remains next.