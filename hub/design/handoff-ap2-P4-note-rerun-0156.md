# Handoff: P4 note-04 conflict rerun

Source: `5a313eb88e8ddce1e9e033ed9cfde7ef433f7c55` (`hub/tl/agt-G3-R2-resume-sol-0136`).

Added only `tests/sdk/test_p4_note_rerun.py`. It executes the original collected note-04 case through `timeline.open()` and `tl.commit(fn)`, using the real G3 emitter, native command engine, document compiler, and persisted outbox path. The existing `Generated`/`Client` fixture remains an explicitly fake generated transport boundary.

The real document fixture retains its full closure and unrelated content. Nine original note IDs/texts are present at the base; note-04 is absent per `cases.json`. The first callback reads the original base, the first request is forced into the collected same-field conflict with exact peer text `Peer reviewer owns this note`, and the second callback reads `peer-revision` and sends a fresh key with exact `before` equal to the peer value and value equal to `Peer reviewer owns this note — reviewed`. Assertions cover exact bases, steps, label, patch, omitted reads, conservative atomic mode, evaluation count, fresh key, canonical physical-document fields, and completed outbox state.

Evidence:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_commit_cases.py` — `3 passed`, exit 0; only the pre-existing unknown `timeout` pytest-config warning.
- `/root/.local/bin/ruff check tests/sdk/test_p4_note_rerun.py` — pass.
- `/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_note_rerun.py` — pass.
- `git diff --check` — pass.

No Runtime HTTP/provider acceptance, authenticated preview/history, official merged/refused/invalid reply qualification, CLI/sheet/show/history, per-step undo, full suite, or H3/P4DONE claim is made. Those remain unverified by this bounded test.
