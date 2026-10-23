# P4 ten-note corrected source review — PASS

## Scope

Reviewed Agent `HEAD` `81aad71e853fca551163442fcf3bcec6150357b6` (the named
first-return base/tree) and its only product-repository change:
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py`.

Compared with donor `b4f4ba00e`, the test differs only as permitted:

- removes the unused `cast` import;
- changes `session = cast(Any, reloaded.session)` to the directly typed public
  `session = reloaded.session`.

The public bridge is Agent `a568c4ebf804119e3e21a1644b6d6068ed037380`,
`astrid/sdk/timeline/sync.py` blob
`5e7dfeec3b2a7f03849b58e5d09a5456b81a0a7b`. Its public
`TimelineSession.undo(..., steps=...)` validates the selector and emits
`timeline.inverse` through the existing session flush/HTTP path. The test does
not mask the API with `Any`, substitute a provider or transport, or call a
private provider.

The original ten-note coverage remains: one commit with ten ordered commands
and steps, per-step patches and reads, opaque/non-note closure preservation,
history and CLI `show` readback, and each selected step's undo followed by redo
with the other nine notes retained. This is a source review only; no Agent API
product review is claimed here.

## Evidence

- `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 PYTHONPATH=.:/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest -q -m integration --collect-only tests/editing_conformance/test_p4_ten_note_v2_runtime.py`
  — PASS, 1 test collected. Pytest emitted the existing unknown `timeout`
  config warning.
- `/root/.local/bin/ruff check tests/editing_conformance/test_p4_ten_note_v2_runtime.py`
  — PASS.
- `/root/.local/bin/mypy --follow-imports=silent tests/editing_conformance/test_p4_ten_note_v2_runtime.py`
  — PASS, no issues found.
- `git diff --check` — PASS on the clean worktree.
- The commit-range form `git diff --check HEAD^ HEAD` reports a blank line at
  EOF in the newly added donor file. The same bytes are present in donor
  `b4f4ba00e`; it is outside the two allowed edits and was not changed in this
  read-only review.

## Held scope / next step

Actual HTTP-body execution, normal34e/G3/R2 joined acceptance, browser/socket
or service/full runs were not performed and receive no credit here. The next
step is the owner/merge-side run against the compatible joined source and
Runtime `34eac004`.

