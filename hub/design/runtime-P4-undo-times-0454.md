# P4 per-note undo timing supplement

This is a read-only supplement to the already completed original P4 run. It
does not replace or add gate credit to the original GO result.

## Correlation basis

- Captured run: original ten-note selector, one passing test.
- Original timing guard: 45 s.
- Retained XML suite duration: 28.101 s; testcase duration: 27.485 s.
- The retained run has suite/request/completion-level timing only. It has no
  per-operation start/end records and no operation-level timing counter.
- Source identifies the first `session.undo(...)` in the loop as the per-note
  inverse call, in fixture order `note-01` through `note-10`. The second
  `session.undo(...)` in each loop is a separate redo call and is not included
  in the table.

Source path: `tests/editing_conformance/test_p4_ten_note_v2_runtime.py`
(captured Agent source `786385631b8096e50e66b8ecff1e7034c5bc1da9`).

Retained timing source: `evidence/body/d97-original-body-0445.xml`.

## Per-note intervals

| Ordinal | Note | Operation | Start/end retained | Duration |
|---:|---|---|---|---|
| 1 | `note-01` | per-step undo | UNKNOWN | UNKNOWN |
| 2 | `note-02` | per-step undo | UNKNOWN | UNKNOWN |
| 3 | `note-03` | per-step undo | UNKNOWN | UNKNOWN |
| 4 | `note-04` | per-step undo | UNKNOWN | UNKNOWN |
| 5 | `note-05` | per-step undo | UNKNOWN | UNKNOWN |
| 6 | `note-06` | per-step undo | UNKNOWN | UNKNOWN |
| 7 | `note-07` | per-step undo | UNKNOWN | UNKNOWN |
| 8 | `note-08` | per-step undo | UNKNOWN | UNKNOWN |
| 9 | `note-09` | per-step undo | UNKNOWN | UNKNOWN |
| 10 | `note-10` | per-step undo | UNKNOWN | UNKNOWN |

## Preserved run metadata

- Agent: `786385631b8096e50e66b8ecff1e7034c5bc1da9`
- Runtime: `0c62dfa63db9ff608ac9338388431e31a814e080`
- App: `1e34f8eac5e3d5a54dbba12d538a7f3bf8509b66`
- Composition: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`
- Original test hash: `728c826d9afdc92b5deffda0b276193d1db600794c87c8efac883aa17c43731b`
- Original result: PASS, 28.101 s < 45 s.
- Preserved independent review: GO for the original run; this supplement gives no second verdict.

No total-wall decomposition, historical curve, profiling, timestamp
manufacture, or second run was used.
