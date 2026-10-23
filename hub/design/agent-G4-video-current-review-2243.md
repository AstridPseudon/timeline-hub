## Verdict: FAIL

Candidate reviewed: `d31ffc7819e9e50d367f85bbf789d813ac766920` (`70a5b10d…` tree), against `c36ca8c94`.

Finding: genuine ordinary after-insert compatibility regression.

- Frozen `c36` accepts a schema-valid fully authored after-anchor row with different `at`, `hold`, `nullable`, and `opaque` values; inserts it unchanged, preserves sibling `C.at == 5`, and keeps order.
- Current candidate refuses the identical request with `capture_mismatch`.
- `capture_clip_add_media` rewrites the caller row into a normalized anchor clone (`at=3`, `hold=2`, source metadata), violating the old literal-carrier behavior.
- Relevant code: `native_parent_media_commands.py:63-71`, `:108-141`, `:189-198`.

Tests/checks:

- Scoped prepared-video + neighbors: **12 passed, 1 deselected**
- Ruff: passed
- Private mypy: passed
- Vendor lock check: passed
- Artifact manifest: passed
- `git diff --check c36..HEAD`: passed
- Public Runtime preview/accept/retry/undo body: **not run**, per the brief’s instruction to stop without an unneeded public body after compatibility failure. No suite row was added.

Pins/origins remained unchanged and clean: Runtime `8ea0766f` / tree `6047ac3`; frozen producer `34eac004` / tree `9853574`; App facts `e99cde635` / tree `2620ff7`; integration Agent remained `c36ca8c9`.

Recommended next step: return this candidate for correction, preserving literal ordinary after-insert semantics while keeping normalized UI migration separate.