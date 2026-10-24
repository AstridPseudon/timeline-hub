## Report

- Updated only `tests/test_timeline_null_speed_retained.py`.
- Adapted all six legacy cases (null, `[3, 2]`, `"3/2"` × child/parent) to assert:
  - status `410`
  - code `retired_route`
  - reason `timeline_commit_required`
- Preserved inputs, full SQL/CAS no-write assertions, and all other retained tests unchanged.
- No production, schema, generated, or shared files changed.

Evidence:

- Targeted pytest: `14 passed`
- Ruff: passed
- In-memory compile: passed
- `git diff --check`: passed
- Pyright: 11 pre-existing diagnostics; zero diagnostics on changed lines.

Source: HEAD `458595850c354f4403dabc58a72b98bebbc2c3a3`, tree `703b1aac733ad3c977399e67cd4e23d6ae85e7bb`.

The prior full census recorded these six cases as failures caused by R5 retirement; no full rerun was requested. Commit message and `DONE` marker created. Recommended next step: independent review, then home merge queue.