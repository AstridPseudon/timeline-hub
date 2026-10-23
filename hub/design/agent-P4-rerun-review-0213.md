# Agent P4 rerun review — PASS

Candidate `b9a640b5d63bb213ce69b1eacbbf78c8b2f20886` is a clean one-file
test-only delta over exact base `70e6d33de527779d8a2a4318b09e4b85a532d347`.
`tests/sdk/test_p4_note_rerun.py` is blob-identical to donor
`755d6e7a4a179e74ce5ed497edab88e8b7a292af` (blob
`80c15e2944b5660a18077aa38f84cf3b3ced09bb`). The prior files remain identical
to `2d21a9891` and `e7385882e`; the P4 collection and fixture are unchanged.
The candidate has no product/generated/pin/dependency paths or imported merge
ancestry.

Evidence:

- `PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_commit_cases.py` — **16 passed**.
- Scoped Ruff over the same four files — **passed**.
- `PYTHONPATH=.:/home/user/work/runtime /tmp/astrid-u2-typecheck/bin/python -m mypy --follow-imports=silent` over the same four files — **passed**, no issues.
- Exact blob/path/parent census and `git diff --check` — **passed**.

The bounded proof preserves the public callback rerun with fresh key/base,
real G3 emitter, fake generated transport, note-04 conflict behavior, ten-note
step undo, collection assertions, and raw/opaque/mirror preservation. It does
not qualify Runtime HTTP/durable lifecycle, CLI/sheet, restart/history/show,
or full P4/H3 behavior. No full suite was run.
