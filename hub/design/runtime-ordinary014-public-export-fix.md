# Runtime ordinary014 public-export repair

Status: corrected in the worker worktree; final commit SHA is pending the harness commit.

## Source and identity

- Rejected candidate parent: `806636baf42e9ed1e4c7f9fe76c3e14d7330fcc1`.
- Corrected worktree tree: `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Corrected commit SHA: pending harness commit (the worker cannot commit by policy).
- Corrected working patch SHA-256 relative to the rejected parent: `9f19160ea6ffbd44105e615432bb9b2f44c0a258799a200ba5c362d60d58c7dc`.
- Frozen Agent source remains `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`; raw schema remains `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Runtime schema digest: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- New artifact manifest version: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.
- `contract/artifacts.json` file SHA-256: `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.

## Changes

- Updated the authoritative Python package initializer template and regenerated `astrid_runtime_client.__init__` to export and identity-match all seven added schema definitions: `AssembledTargetArgs`, `ClipAddMediaArgs`, `TimelineInitArgs`, `WordAnchor`, `ClipAnchorArgs`, `OccurrenceCreateArgs`, and `TextBindingSetArgs`.
- Restored the unconditional public export assertion in `tests/test_timeline_current_union_contract.py`.
- Replaced the candidate’s subset/count operation assertion with exact set equality: the frozen 22-operation set plus the seven explicit additions (`timeline.assembled-target`, `clip.add-media`, `timeline.init`, `clip.anchor`, `occurrence.create`, `clip.swap-media`, `text-binding.set`).
- Normal regeneration and artifact refresh changed only the four intended paths: `contract/artifacts.json`, `generators/python_client_init_template.py`, `packages/python/astrid_runtime_client/__init__.py`, and `tests/test_timeline_current_union_contract.py`. Public fixture/pin/schema source and all other candidate blobs are unchanged.

Actual counts: 55 schema definitions, 29 command operations, 133 HTTP operations, 75 artifacts, and 7 newly public definitions.

## Evidence

- `python generators/generate.py --check`: PASS.
- `python scripts/artifact_manifest.py --check`: PASS.
- `node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --check --source-root "$PWD" --fixture-root "$PWD/conformance/fixtures"`: PASS.
- Public Python import smoke for all seven new definitions: PASS.
- `tests/test_timeline_current_union_contract.py`: **64 passed**.
- Focused neighboring contract/export/generator files: **271 passed**; 5 `tests/test_generated_client.py` socket cases could not create localhost sockets in the worker sandbox (`PermissionError`), with socket coverage supplied by the central lane below.
- Local TypeScript package build, strict compile, and Node tests: **2 passed**.
- Central `commit-integration` on corrected tree: **9 passed**.
- Central `ts-client-check` on corrected tree: **61 passed, 0 failed**.
- Frozen Agent ordinary native cohort against corrected Runtime (`test_next_command_cohort_runtime.py`): **11 passed**.
- `git diff --check`: PASS.

No full suite, broad matrix, new fixture, pin, publication, merge, or release activation was performed. The candidate remains unpublished pending final independent review.
