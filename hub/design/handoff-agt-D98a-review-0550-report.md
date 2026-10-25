PASS_SOURCE

Reviewed `a09ebcbd80` against parent/current normal `bde578505c` (`tl/integration`). One test file changed; no parent conflicts.

The replacement is source-correct:

- Uses registered `capture_occurrence_create`.
- Preserves exact inputs: `chapter-shot`, `occ-a`, `Chapter One`, `picture`, `on=8`, `duration=10`.
- Recorder provenance yields `created = ["shot:chapter-shot", "occurrence:occ-a"]`.
- Runtime provider and unchanged `validate_claims` remain authoritative.
- Local `execute` is only sequential capture/preview state; no hand-filled authority.
- All structural data, opaque values, pins/media, steps/reads, preview/history, refusal, ABA, inverse, retry, and no-write assertions are preserved.
- All four test-function ASTs are structurally identical to parent.
- Complete affected selector set: 48 nodes across the four tests (`4 + 24 + 4 + 16`), unchanged from the existing manifest.

Source identities:

- Parent blob `b42079e3b350212109b63aa86bd0eb145444843b`; SHA256 `e177f56a9a26b07e4d074961e5fa78d8941b379b4c3efb241aaca5a03c0c9537`
- Candidate blob `c4f54e34536dabbf196fd9a17c337b78394506e3`; SHA256 `cf73444ebe59c7a5e62f29cff072d3c3dea87ead85043d92ef632d433cb110a1`

Checks:

- In-memory AST/compile: PASS
- Ruff parent and candidate: PASS
- Mypy parent and candidate: PASS
- `git diff --check bde578505c HEAD`: PASS
- Pytest/imports/services/full suites: intentionally not run.

Commit message written and `DONE` created.