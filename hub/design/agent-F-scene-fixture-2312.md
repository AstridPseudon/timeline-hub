PASS — migrated the scene fixture to an authenticated Runtime/Agent semantic-command path.

- Retired `publish_parent_composition` removed from fixture setup.
- Preserved all existing capture/admission/claim/host and negative assertions.
- Scene pins now use captured timeline/revision IDs.
- Source authority: Runtime-verified generated CAS media, accepted via `timeline.init`, track/occurrence creation, and `occurrence.add-media`; no DB/store injection or fabricated receipts.

Tests:

- Capture runtime: `27 passed`
- Scene dispatch contract: `4 passed`
- Ruff: passed
- Targeted mypy: passed
- Full mypy baseline was environment-blocked by missing `types-PyYAML` and incompatible NumPy stubs; no code errors observed.
- Full suite not run per instructions.

Audit source contained 1 parent, 1 occurrence, 1 unique shot, 1 internal revision, 1 managed media object, and 6 authenticated timeline-history entries.

Commit message written; `DONE` created.