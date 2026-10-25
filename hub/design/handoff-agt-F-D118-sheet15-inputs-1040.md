D118 READ-ONLY HAND-BACK — exact15 current-sheet15

No source or test changes were made. The exact 15 reserved IDs were confirmed against the retained XML (9,269 nodes; XML SHA-256 `72872c…c18a`).

| Ordinals | Safe retained classification | Source frames |
|---|---|---|
| 1262 | `KeyError` | `test_native_sheet_current_runtime.py:340` → test `:544` |
| 1264 | `CommitConflict` | `sync.py:569` / `_flush`, caller `sync.py:556`; test `:777`, `undo` `:462` |
| 1268 | `KeyError` | test `:123` → `tiny_cut_parent`, test `:817` |
| 1271, 1273, 1275, 1276 | `KeyError` | test `:123` → `seed_labeled_tiny_cut_parent:228`; tests `:871`/`:933` |
| 1277 | `KeyError` | test `:123` → `seed_tiny_cut_parent:219`; test `:992` |
| 1279, 1281, 1283 | `KeyError` | test `:123` → `seed_rational_tiny_cut_parent:241`; test `:1051` |
| 1285, 1288, 1291 | `KeyError` | test `:340` → test `:1129` |
| 1299 | `AssertionError` | test `:1238` |

All 15 retained `phase`, `PreparedCommit`, accepted-boundary, records, bindings, effects, dependencies, history, undo, and inverse fields are `EXACTMISSING`; no boundary reconstruction was performed. Original failure-text hashes were preserved from the allocation packet.

Current public caller comparison: `TimelineSession._flush:556` → remote `commit` → `WorkspaceClient.commit_timeline:485` → generated client `commit_timeline:963`. Passing comparison nodes are retained ordinals 1294, 1302, and 1315; this confirms caller shape only, not the failing fixtures’ missing boundary records.

Custody hashes:

- XML: `72872c…c18a`
- outcomes JSON: `c180c1…e2eb`
- retained body log: `0f3470…f001`
- sheet15 source blob: `3d391f…b8b7`
- source AST assertions: 248, byte-identical to Agent `e9e3b8f`

Checks:

- `git diff --check` — PASS
- static XML/JSON membership validation — PASS
- AST/hash comparison — PASS
- Tests, pytest, imports, lint, and typecheck — not run per task

The retained diagnostics are sufficient to identify the fixture/media setup seam and public flush seam, but not to justify an App edit or Runtime fault claim. `DONE` and the D118 commit message were created.