## Review report: PASS (qualified source-cause review)

- Original 46 test ASTs: unchanged; all 46 matched the parent commit exactly.
- Exact ten redo cases: separate `history_unavailable` fixture/authentication failure, not the new guard regression.
- New collection regression: genuine live-path defect. `doc.patch list.remove` records the entire mirrored collection via `closure.install`; `check_intervening` then falsely overlaps edits to surviving rows.
- Native `clip.delete` comparator: PASS; surviving-row edit remains disjoint.
- Production chain: emitter → `execute` → compiler/final validation → Runtime commit/rebase/undo paths confirmed by source inspection. Production callers use the emitter.
- C0 semantics support the diagnosis: removal guards the removed item plus collection membership/order; surviving-item fields remain mergeable in `fields` mode. Explicit `reads: []` does not authorize whole-collection capture or fallback guessing.
- No candidate R1 hunk or product change was applied. All history, owner, pin, undo, ABA, and atomic guards remain intact.
- D52 deletion/deprecation is not justified; generic `doc.patch` collection removal remains live.

Evidence reused:

- Exact-ten receipt: `10 failed, 116 deselected`, all at `history_unavailable`.
- New regression receipt: `1 failed`; compiler and final validation passed, `check_intervening` rejected the surviving-row edit.
- Native comparator receipt: exit 0 / PASS.

Read-only checks:

- `git diff --check bfebd359ed^ bfebd359ed`: PASS.
- Production-source diff against `bfebd359ed`: empty.
- Worktree: clean.

Prerequisites: R1 must implement item-scoped removal capture while retaining the complete removed row, collection shape/order guards, mirror handling, and atomic-mode behavior. M1’s authenticated fixture still requires a real accepted provider receipt and physical binding normalization before the ten/126 behavioral cases can qualify.