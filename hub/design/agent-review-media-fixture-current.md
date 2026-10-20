# Review: Agent media-manifest fixture migration

## Verdict

**APPROVE — bounded fixture migration.** The reviewed commit preserves the two
positive add/swap manifest-inverse nodes and moves only their setup off the
retired descriptor/shot-text/direct-publication path. It does not qualify a
production popup/native operation, browser/App journey, renderer, or timing
cutover.

## Reviewed source

- Commit: `134f1c276a11b4703c7a76f25cbf13158e4a4416`
- Tree: `bca60e5b02db470cd3b983d3924bb8452f7a9360`
- Parent/base: `537c2ecd28f92b391c79e383e0e045fd71b3258f`
- Changed paths: `tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py`,
  `tests/helpers/trusted_seed.py`
- Target hashes: test `1bc4b5ad61d5f96e59655ce5a8b75cc66b567232e6f68eadc240eac5ab0ec1e7`;
  helper `abb72b1e947972b92321c2023cd1b7461dbc8c5d6eeb20dd0d3dcc2599f5f7ba`

The diff has no product, schema, public generated artifact, lock, or pin path.
AST comparison against the parent retains all 15 original assertion expressions;
the migration adds eight independent checks.

## Findings

- The fixture reuses the existing historical native parent-media helper. Its
  separate historical interpreter creates settled, project-owned red/blue PNG
  selections through normal APIs; current Runtime reads the resulting chain.
- The current baseline is installed through the approved `seed_trusted_parent`
  test-only boundary. The six-field descriptor is sourced from the real retained
  transcript binding and its actual `A chapter` CAS bytes; no inline text
  authority or fabricated SQL/history is used.
- The trusted-seed correction adds `created: []` to the placeholder command
  before hashing/acceptance. This makes command metadata truthful and enables
  the later identity-history scan; it claims no reservation or semantic birth.
- The custom `test.media-provenance` operation remains explicitly test-only and
  uses the existing provider/port seam. It is not evidence for a production
  popup/requester operation.
- Existing complete-document inverse, closure, exact manifest delta, retry
  without semantic execution, changed-payload 409, retained selection,
  immutable history/GET, dependency receipt, redo, and integrity assertions are
  retained for both add and swap. Numeric 24 fps and legacy window treatment
  remain unchanged.

## Independent evidence

Using an ephemeral private copy of the reviewed tree and a private Runtime
schema overlay (shared dependencies and source worktrees remained untouched):

- `...test_commit_runtime_media_manifest_inverse.py`: **2 passed** in 7.36s.
- `...test_commit_runtime_identity.py`: **3 passed** in 4.86s.
- Saved-closure projection neighbors in `test_timeline_capture_projection.py`:
  **3 passed, 40 deselected** in 3.79s.
- Ruff targeted check: passed.
- `git diff --check 134f1c27^ 134f1c27`: passed.
- Private Runtime normal generation, `--check`, artifact generation, and
  artifact `--check`: all passed.

The worker report additionally records **155 targeted service tests** and **130
portable neighbors** passing. I did not rerun a full suite, browser/live-socket
suite, or any released-pair/native-cutover qualification.

No defect or blocker was found. Recommended next step: let the orchestrator
integrate this bounded test change and retain the explicit non-production scope
in the milestone evidence.
