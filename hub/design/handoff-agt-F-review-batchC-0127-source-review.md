# F-D89 independent protected source review

## Verdicts

- Numeric cumulative delta (`993e1e9d98463a1bfa35c611d45dd7b21e32e783` -> `ec76fa69e6cc8af424ec397512b9422968b7eaf5` -> `2ec37ccebbd07b3d0ae96aadd3f8d621b0aafd07`): `PASS_SOURCE`.
- CLI trim cumulative delta (`0ae146e1b0acc6e4a82ba6b4f905d88bad48320c` -> `034f9375c3d52139a2119387680b4aa699aa83c1` -> `c13c74678e317fe537f75996a2936bd1f6dad3b6`): `PASS_SOURCE`.

These are separate verdicts; no pooled PASS. Candidate ancestry is own-only for each two-commit path, and the only changed paths are the assigned numeric pair and `test_cli_trim_runtime.py`.

## Numeric map

- Sole provider registration is in the shared `numeric_film` fixture, before `case.submit`; the per-test duplicate registration was removed from `numeric_move` and `numeric_params`.
- The provider is the genuine pinned Runtime provider loaded with `load_timeline_commit_provider('astrid')`; `use_runtime(commit=vendored_runtime_commit())` selects the vendored Runtime. Pinned Runtime `732c48c6f5a9441a65c61b24595d454a1cd3e180` retains startup-only rejection when a commit has started or a provider is already installed.
- Removed setup mapping: `copy` import; source/parent/shot/internal deep-copy and revision rewiring; legacy `publish_parent_composition`; and the second `create_runtime_commit_service()` registration. Replacement is native `capture_clip_set` plus `case.submit` using the full v2 envelope. No no-op replacement.
- Both original selectors remain: `parent/clip:music-bed` and `occurrence:occurrence-1/clip:clip-1`. The `scope` 2-way and `start,on` 3-way parameterizations remain. Numeric opaque values `[None, False, 1, 1.0]`, exact-type assertions, canonical/history/dependency assertions, no-op history assertion, decorators, and all test assertions remain. The params file retains both refs, all five before/after pairs, exact type checks, inverse/redo assertions, and decorators.
- No `pytest.raises` existed in these two original tests; no raise expectation was lost.

Source SHA-256: move baseline `51f6df318fbba81f66512c94a9ce60ef6eda6d930e3c8c27c5fe6ab8e4a2cca1`, candidate `1de81ce9485b5ee2492da5ca88f413c980ab6302c3d3c10cc57e20635f485ae1`; params baseline `8f1020a2ce363abbc11f7fc47b8287a48f963c7d4de3a88b5e5f86a757f6788c`, candidate `1ced4d39f8c2da4972863500b20aa67da1ee458f20ee9f4c86be152fd716b5d6`.

## CLI map

- `c13c746` adds the guarded `doc.patch` with `ref: parent`, path `config/output`, `before: absent`, and value `{'fps': 30}` immediately after the empty timeline is opened and before track/clip capture. The call goes through `TimelineSession.commit`, which builds the current v2 commit request and uses the Runtime-registered provider.
- Original parent values retained in source: literal/title IDs, track `picture`, timing `at=0/from=1/to=6/hold=5/speed=2`, `app.astrid.for=2.5`, opaque `[None, False]`, extension `keep=True`, title text `Keep me`, media filename/type, duration `10`, and authored output `fps=30` (now explicit again). Empty child topology remains: no shot, internal-timeline, or occurrence fixture is introduced.
- Original selectors remain: `parent/clip:literal` (`REF`), `parent/track:picture`, and `parent/clip:title`; the trim and move test bodies are unchanged from the true original. Assertion counts remain 28 and 9; retry, lost-ack/restart, disjoint rebase/undo, relevant conflict, and undo branches remain.
- The migrated media bytes are a valid 1x1 PNG required by the current admitted-media path; the authored opaque clip values and graph topology are retained. This is not treated as baseline-equality proof.

Source SHA-256: CLI baseline `2e9426ff8b4cd3484d5d1513846493bfa30bdf6e724bfd0f7ad0ede2e68bb1df`, candidate `13048d0bedfa98ecf7c79959413eedc0c7587153f9df4b3561c00abb961b6a1d`.

## Static evidence

- In-memory `ast.parse` + `compile`: passed for all six true-original/candidate source texts.
- Ruff 0.12.0: passed for numeric baseline/candidate and CLI baseline/candidate.
- Mypy `--follow-imports=silent`: identical environment diagnostic on every side, from NumPy stub `Type statement is only supported in Python 3.12 and greater`; no candidate-specific diagnostic.
- `git diff --check`: passed for both cumulative deltas.
- No pytest, collection, test/helper/fixture execution, service, browser, build, render, or probe was run. Functional MAIN proof remains owed; this is source closure only.
