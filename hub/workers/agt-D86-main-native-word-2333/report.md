# F-D86 D86-native-word report

Blocked; no source changes made.

- Exact base verified: `5d4ae93c833cc1adee109b28405276210165c0db`.
- Assigned files remain byte-identical; diffstat is empty.
- Source seam:
  - `tests/editing_conformance/native_word_anchor_fixture.py:67-119` seeds via retired `publish_parent_composition`.
  - D72 source is an audio child track.
  - Current native media setup requires an active visual child track at `astrid/sdk/timeline/native_occurrence_media_commands.py:191-196`.
  - Replacing this with synthetic acceptance, aliases, or the retired publisher violates the settled plan; fixing it requires widening ownership/product changes.

Static checks:

- `py_compile`: exit 0
- `ruff check`: exit 0
- `mypy`: exit 0, no issues
- `git diff --check`: exit 0
- No pytest/full/browser/service runs performed.

AST conservation against exact base: unchanged. Native file: 29 tests / 120 assertions; recipe file: 19 tests / 85 assertions. Complete 46-selector manifest and evidence are under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D86-main-native-word-2333/evidence/`

Prepared commit message and `BLOCKED` marker; no `DONE` marker. Proposed ledger entry: `F-D86 D86-native-word — blocked at existing fixture/product seam; no source diff.`

Recommended next step: assign the fixture/bootstrap seam to the appropriate owner, then rerun this source-only migration with the approved real-provider setup.