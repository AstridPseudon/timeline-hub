# Agent P4 rerun import — 2026-10-23

- Base: `70e6d33de527779d8a2a4318b09e4b85a532d347`.
- Added only `tests/sdk/test_p4_note_rerun.py`, byte-identical to the file at
  `755d6e7a4a179e74ce5ed497edab88e8b7a292af:tests/sdk/test_p4_note_rerun.py`.
- Prior P4 imports remain unchanged and byte-identical to `2d21a989…` and
  `e7385882…`.
- Targeted evidence: four P4 files, **16 passed**; scoped Ruff passed; specified
  private-interpreter mypy passed on all four files.
- Coverage boundary: real public callback rerun + G3 emitter/native engine + fake
  generated transport. No Runtime HTTP, durable lifecycle, CLI/sheet/history/
  restart, P4DONE, or H3GO claim; G3/R2 and official wire remain dependencies.
