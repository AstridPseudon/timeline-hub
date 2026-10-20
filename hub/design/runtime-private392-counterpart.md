# Runtime private392 counterpart

Completed 2026-10-20. This is one unpublished PRIVATE generated counterpart only.

## Tuple

- Base: `8f105c26e3b62f9c2683f717a9773a12bc775a8e`, tree `b7f456d5135cba6049980ebc43a91c7a72ab8f7e`.
- Agent source: `e010e6a3868e963471244491bb6672c3e4a5135e`, tree `70414cf6875d2c97c45f33e0a5158c80bd7391d9`, path `astrid/core/timeline/schema/edit-command.schema.json`.
- Source/raw schema SHA-256: `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`.
- Generated Runtime schema: 56 definitions / 30 operations / 42 command branches / 12 explicit v2 branches.
- Runtime health/schema digest: `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042`.
- Raw bundle digest: `sha256:fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3`.
- Artifact manifest version: `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d`; manifest file SHA-256 `1c684f53582a44b12a7438b79ddeace8696768b4fb98f8f704d58a640fa6cd5f`.
- Harness commit/tree: pending harness commit after worker exit. Central socket-test snapshot tree was `9bf5afce0fa367de1d4cc27ef2d26f36bd385510`.

## What changed

Used the normal generator path with an exact source hash pin and added the approved Python package-root export discovery so `ProjectDataWriteArgs` is exported. Refreshed the generated Runtime/Python/TypeScript/conformance resources and bounded schema/client guards.

Exact e010 minus only `ProjectDataWriteArgs` and the `project-data.write` clause is semantically identical to frozen 613. A structural projection of frozen 613 that removes only the 12 v2 branches and the three additive item-reference alternatives exactly reproduces ordinary `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

No Runtime product guard files changed; catalog/headless/CAS/text/promotion/C4/global occupancy/strict-marker/history behavior remains from the current server. No opacity, group, transition, wire DTO, release/version bump, adoption, pin, consumer activation, native pair, or full suite was run.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_timeline_current_union_contract.py` — 66 passed.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_timeline_commit_type_generator.py` — 6 passed.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_command_schema_compatibility.py` — 131 passed.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_timeline_bundle2_contract.py tests/test_typescript_generator.py tests/test_client_parity.py tests/test_client_release.py` — 43 passed.
- `PYTHONDONTWRITEBYTECODE=1 python generators/generate.py --check` — passed.
- TypeScript conformance generator `--check` — passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/artifact_manifest.py --check` — passed.
- `git diff --check` — passed.
- Central targeted localhost lane `tests/test_generated_client.py` — 73 passed in 20.00s, service exit 0, on snapshot tree `9bf5afce0fa367de1d4cc27ef2d26f36bd385510`.

The first local attempt including `tests/test_generated_client.py` had 6 expected sandbox socket-bind failures; the central run is the qualifying result. No full suite or native392 pair was requested.

## Changed paths

```
conformance/typescript/contract-metadata.ts
conformance/typescript/generated.ts
contract/artifacts.json
contract/schemas/edit-command.json
generators/agent-command-source.json
generators/generate.py
generators/python_client_init_template.py
packages/python/astrid_runtime_client/__init__.py
packages/python/astrid_runtime_client/contract_metadata.py
packages/python/astrid_runtime_client/generated.py
packages/python/astrid_runtime_client/timeline_commit_types.py
packages/typescript/src/contract-metadata.ts
packages/typescript/src/generated.ts
packages/typescript/src/timeline-commit-types.ts
runtime_protocol/contract_metadata.py
runtime_protocol/schemas/timeline-commit-bundle.json
runtime_protocol/timeline_commit_types.py
tests/test_timeline_commit_type_generator.py
tests/test_timeline_current_union_contract.py
```

Reciprocal review should use the harness-assigned commit/tree plus the tuple and digests above. Native392 qualification remains deferred until reciprocal review/pin.

