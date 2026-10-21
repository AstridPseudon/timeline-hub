# Runtime PUBLIC018 final generator/release review

## Verdict

**APPROVE.** Independent review of the complete candidate finds no concrete
blocking defect in the normal PUBLIC018 generation, artifact/version transition,
or the minimal boolean-subschema generator repair. Publication and consumer-pin
coordination remain separate, as requested; this review does not claim App
activation or those downstream preconditions.

## Identity and health

- Candidate: `8ed79a31e66d02e2e2e7062b9a368e3266cea9db`
- Candidate parent: `d6d21d8d305549c9b0f8540be994bba974e93204`
- Integration comparison point: `b92d3e7a05eec65c142294ef4873edd059e9b31d`
- Parent-to-candidate generator repair: 6 files, 62 insertions, 19 deletions.
- Full `b92d3e7..HEAD` candidate: 22 files, 238 insertions, 53 deletions; the
  additional changes are the expected PUBLIC018 transition/digest/version and
  regenerated conformance artifacts. No private017 operations, material-source
  changes, new endpoint/authority, or unrelated DTO changes are present.
- Worktree was clean after checks; no tracked or untracked build output remains.

## Schema and artifact identity

- Canonical `contract/schemas/edit-command.json`: 71,022 bytes,
  `sha256:9397d5faf66776c0a27d3611def6af42d9526dd965ad60eef11dc52bd3dd3e3a`.
- Raw `runtime_protocol/schemas/timeline-commit-bundle.json`: 156,225 bytes,
  `sha256:5eb9775e2c46ab08a41d1e3044632854354f021efd0f48ea960f082524c0bb4c`.
- `contract/artifacts.json`: 76 artifacts,
  version `sha256:afd65ccf54aa1c27fac95840235d50fa93da0e951b2b03adceaf47d391cd996c`.
- Generated Python DTOs (both copies):
  `sha256:c629dcc309f8c5824e4fb106e01116ed370b2b7d39fc2fbb111f2867de3e7c92`.
- Generated TypeScript DTOs:
  `sha256:7f9897e576823dd16d888284a24ff54a2571dbef93662e8319625083ba5c440b`.

The generator now handles JSON Schema booleans at refinement, nested-property,
and expression boundaries: `false` renders as Python `Never`/TypeScript `never`,
while `true` renders as Python `Any`/TypeScript `unknown`. Existing object
constraints and JSON-shaped open fields remain present; the four transition
keys are explicitly impossible rather than converted to numeric/broad values.
The optional `content_digest` remains optional in the document schema, and the
candidate diff leaves accepted-result/ledger logic byte-for-byte outside the
approved transition changes.

## Evidence

All commands ran against this candidate without a temporary shim:

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_commit_type_generator.py` — **6 passed**.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python generators/generate.py --check` — **passed**.
- `/opt/node22/bin/node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --fixture-root conformance/fixtures --check` — **passed**.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check` — **passed; manifest current**.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_command_schema_compatibility.py::test_normal_generation_preserves_all_current_artifact_bytes` — **2 passed**.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_generated_client.py::test_generator_is_reproducible` — **1 passed**.
- `tsc --noEmit --strict --module NodeNext --target ES2022 conformance/typescript/smoke.ts` — **passed**.
- `tsc --noEmit -p packages/typescript/tsconfig.json` — **passed**.
- `git diff --check b92d3e7..HEAD` — **passed**.
- Python AST parsing of both generated Python DTO modules — **passed**.

The author’s historical logs were inspected but not replayed: the pre-repair
run was `140 passed, 2 deselected, 3 errors` from the generator crash, and the
bounded corrected run was `22 passed`. Per the brief, I did not rerun the 140,
22, full, HTTP, browser, live-socket, renderer, native, keeper, or real-journey
suites. No new blocker or smallest repair is recommended.

## Recommended next step

Manager may proceed with the separately coordinated publication/consumer-pin
review, retaining this candidate and its exact artifact manifest identity.
