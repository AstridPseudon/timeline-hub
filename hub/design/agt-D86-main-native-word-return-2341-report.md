# F-D86 D86-native-word report

Implemented the genuine migration in [native_word_anchor_fixture.py](/home/user/work/wt/agt-D86-main-native-word-return-2341/tests/editing_conformance/native_word_anchor_fixture.py:69).

- Replaced retired `publish_parent_composition` seeding with Runtime `create_timeline` + native `timeline.init`, track/clip/occurrence commands.
- Added admitted-media `doc.patch` bootstrap preserving the original audio track, source window, word data, pins, opaque fields, and literal 2000ms placement.
- Production visual-child guard remains unchanged.
- Assigned test files were untouched.

Source evidence: existing live bootstrap in `test_commit_runtime_first_clip.py:24-99`, public commit bootstrap in `astrid/sdk/remote.py:482-595`, generic patch media admission in `_doc_patch.py:331-356`, and preserved visual guard in `native_occurrence_media_commands.py:191-196`.

Verification:

- `py_compile`: passed
- Ruff: passed
- mypy: passed
- `git diff --check`: passed
- AST conservation: passed; assigned tests unchanged byte-for-byte
- No pytest, collection, service, build, or full suite run.

Diffstat: 1 file, `+95/-29`.

Hashes:

- Fixture: SHA-256 `ac5caefbedfad319f795ba5bdb151baed338209ec39a4b9a46dfdfde069508dc`; base blob `af7407a5a2d42bb63b5cc11ba4a4924d3186c607`
- Native test: unchanged; SHA-256 `ab07f5b9cda3a42d0c9273917b46d9486c39b453b979d2ad5d39df5528d4179f`
- Recipe test: unchanged; SHA-256 `4722227e6e347778bb491f4f660e0a8d049ee074026b23e43de939a65d47142a`

Exact 46-selector manifest remains the D86 family manifest: 37 native-anchor selectors and 9 word-binding selectors, unchanged from base. Main manager should run the single later batched affected-node qualification. Commit message written; `DONE` created.