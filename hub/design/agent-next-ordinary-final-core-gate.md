# Agent next ordinary final core gate

Preparation-only candidate for the current Agent source union. This page does not authorize integration, public freeze, schema release, Runtime publication, consumer pin changes, or normal-release authorization.

## Candidate identity

| Item | Exact value |
| --- | --- |
| Base commit | `ce3e647f10f6b7950de19e4219da6d55af4d3939` (`tl/agt-m2-next-ordinary-source-union`) |
| Base/candidate source tree before this gate | `260f2615b869b5e0d8ab236d6c1fbc952c0f6186` |
| Candidate source tree | `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a` |
| Candidate working patch SHA256 | `af725bd415ce5d53b1fd4d0081611ae1557af2223f2a533101a6d691765ae129` |
| Schema raw SHA256 | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Schema canonical JSON SHA256 | `63ac77b3c3e2c582f76ab4b2499be5011ea4836e8c92264b1938632b3bfacba7` |
| Schema inventory | 55 definitions / 29 operations |

The source tree is a working-tree content identity, not a commit SHA. The harness assigns the eventual commit. The 55/29 schema bytes and all S2 clauses remain byte-identical to the source-union base.

## Bounded port

Only the independently reviewed F1 inverse staged-write guard from `8e310785` / `fa156464` and the approved media fixture migration from `134f1c27` are present.

F1 implementation changes:

- `astrid/sdk/timeline/commands.py`: pass earlier same-batch records to inverse validation as `staged_records`.
- `astrid/sdk/timeline/inverse.py`: reject an inverse when earlier staged records touch its guarded writes/selections, including equal-state ABA; preserve disjoint staged writes and later explicit writes.

F1 tests are byte-exact ports in `tests/editing_conformance/test_recipe_scalar_commands.py` and `tests/sdk/test_timeline_selected_schema_runtime.py`.

Fixture changes are byte-exact ports in `tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py` and `tests/helpers/trusted_seed.py`: two real historical media nodes are reused, the current six-field media descriptor is seeded only through the trusted setup boundary, and the seed command records `created: []`. No PARAM authority, carrier, producer, action, outbox, or public artifact source was imported.

## Acceptance evidence

- F1 portable inverse unit regressions: 5 passed.
- Native F1 negative/disjoint/reverse-positive Runtime cases: 25 passed.
- Real media manifest add/swap inverse fixture: 2 passed.
- Source-union birth + two text rows, grouped inverse, clear/restore order, undo/redo/reopen/retry: 2 passed.
- Parent-auto anchor/fallback subset: 2 passed.
- Ruff on all six changed files and `git diff --check`: passed.

The private Runtime pair was generated in a disposable `/tmp` overlay from Runtime `b748ae723b51c6d578ba7a393209ce37d6e2b0c3`, with the ordinary Agent schema input. Python generation, artifact manifest generation/check, and generated-source checks passed. Expected unchanged private-pair identities remain schema digest `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59` and artifact identity `sha256:7e8fe2e485f036741369eed62ccc7a389e27719a166fd70b0009a161c9c7240d`, inherited from the source-union normal generation report.

No full/full* suite, browser/socket/HTTP lane, App journey, renderer/pixel/audio lane, owner-film review, or macOS claim was made. Independent review of this narrow candidate, final schema freeze, Runtime publication, consumer qualification, and release authorization remain pending.
