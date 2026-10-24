## PREPARED FAIL

Reviewed `d11a31c11389186eeb6310a88eeeca0094810a8e` (tree `1c8b2d95`) against `60fedb573` and `fad2ddd1e`.

The candidate does wire accepted `source_ref` and `source_occurrence_id` into the original 16-case historical test, with no fake receipt or `timeline.inverse` setup. Only `tests/test_timeline_legacy_occupancy.py` differs; worktree remains clean.

Blocking findings:

- Reference branch hard-codes the newer edit and source-preservation check to timeline `source`, while the accepted pinned origin is `reference-source`. The actual pinned source closure is therefore not proven unchanged.
- Original inline/reference step-history predicates (`steps` / `undo_steps`) were removed, not preserved.
- Historical result lacks full DTO equality (`receipt.result == data`); only selected response fields are checked.
- Agent/provider handoff for `occurrence.place-shared` and inverse/retirement remains unavailable, so this cannot become ProviderPASS or merge-ready.

Checks:

- `py_compile`: passed.
- Collection: `16 tests collected`.
- Ruff: parent and final both report the same 4 pre-existing diagnostics.
- Pyright: one file checked for each, using the same real `/home/user/work/agent` source path; one unavailable `pytest` import remains in both.
- `git diff --check`: passed.
- No provider, HTTP, original full-file, service, benchmark, or full-suite tests run, per instructions.

Commit message and `DONE` marker created.