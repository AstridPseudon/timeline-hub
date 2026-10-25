Implemented D73/D139/D140 private source fix in `ops-d73-exact-nodes/`:

- Added pre-dispatch validation before the unchanged pinned launcher.
- Integrated it into both named `suites.conf` rows.
- Routed positive and all refusal cases through the actual parsed production row.
- Preserved selectors, argv, timeout, no-cache, IDs, and launcher behavior.
- Kept receiving status separately `NOT_READY`.

Validation passed:

- `python -m unittest discover ...` — 7 passed.
- `./ops-d73-exact-nodes/dry-check.sh --controls` — 7 passed.
- Ruff, Python compile in private `$TMPDIR`, `bash -n`, and `git diff --check` — passed.
- Available disk: 5,199,777,792 bytes.

No product imports, real preflight, central request, install, or full suite ran.

Evidence written to the requested absolute `evidence/` directory. Commit message written to `commit-msg`; `DONE` created.