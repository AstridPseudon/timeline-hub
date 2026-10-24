## Done

- Adopted Runtime producer `becfe6db88b2…` from the clean sanctioned checkout.
- Updated 15 mapped files via `vendor_lock.py`; all hashes match.
- Regenerated `artifacts.json` (unchanged).
- Updated generated client metadata/digest and schema pin.
- Updated the indispensable stale fixture mapping to canonical `commit_conflict_409`.
- No provider, authoring, Runtime, Composition, or unrelated changes.

Producer facts:

- Manifest: 79 entries, `sha256:65085756…`
- Contract schema digest: `sha256:4118b1…`
- OpenAPI: `sha256:30252350…`

Tests/checks:

- Targeted vendor/client/schema tests: 62 passed, 1 expected stale-fixture assertion failure.
- Schema selectors: 73 passed.
- Ruff: `current=2145`, baseline `2145`.
- Mypy: `current=1902`, baseline `1902`.
- Vendor check, artifact check, compile, and `git diff --check`: passed.
- Central live-runtime target selected no tests (exit 5; 39 deselected).

The remaining failure is bounded: the preserved legacy caller still emits `/composition-revisions`, while the canonical fixture records `/commit`. Tests were not altered. Commit message and `DONE` marker are prepared.