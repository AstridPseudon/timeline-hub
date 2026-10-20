# Runtime ordinary014 committed candidate

Status: `UNPUBLISHED` and reviewable only. No consumer pin, merge, publication, or activation was performed.

## Source and candidate identity

- Runtime base: commit `7f6dd8920e1ceec41b137358df5e7fecc304888d`, tree `4cccb2d643194df7df95d624e89a6cd9f6f268fc`.
- Candidate test-service snapshot tree: `06de9476db4a9b7f11f6adeb4cb8003fa942f651`.
- Frozen Agent source: commit `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, content tree `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`, archived at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source` outside the product repository.
- Exact prepared patch SHA-256: `06ecdfcb17cc975f8bed9e3c62677bbcaa8873b5c5cb1e1d65dbf9ff3c1c719`.
- Candidate contract version: `0.2.14` (unpublished).
- Agent raw schema SHA-256: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Agent canonical schema SHA-256: `63ac77b3c3e2c582f76ab4b2499be5011ea4836e8c92264b1938632b3bfacba7`.
- Runtime schema digest: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Artifact version: `sha256:8023c665f0e32835cf06b793c6f5ffa0a278a7ca5aadbfe971d52d163d66c7a3`.
- `contract/artifacts.json` SHA-256: `4ddecda4cd892339cc6f1caaebc2bf4ddde76e422077eae8f8c4d2f059f8146f`.
- Artifact count: 75. OpenAPI operation count: 133, all unique. Command schema: 55 definitions and 29 registered operations.

## Changed-path inventory

The exact prepared patch changed these 17 generated/contract paths:

`conformance/typescript/contract-metadata.ts`, `conformance/typescript/generated.ts`, `contract/artifacts.json`, `contract/schemas/edit-command.json`, `generators/release.json`, `packages/python/astrid_runtime_client/contract_metadata.py`, `packages/python/astrid_runtime_client/generated.py`, `packages/python/astrid_runtime_client/timeline_commit_types.py`, `packages/python/pyproject.toml`, `packages/typescript/package-lock.json`, `packages/typescript/package.json`, `packages/typescript/src/contract-metadata.ts`, `packages/typescript/src/generated.ts`, `packages/typescript/src/timeline-commit-types.ts`, `runtime_protocol/contract_metadata.py`, `runtime_protocol/schemas/timeline-commit-bundle.json`, and `runtime_protocol/timeline_commit_types.py`.

The only additional allowed change is the existing test `tests/test_timeline_current_union_contract.py`: its raw schema digest/counts now describe 29/55, and its historical S2-only assertion compares S1 with the tracked public `agent-26ef2bbb` fixture. No new files, JSON fixtures, matrices, private carrier/version2 references, or hand-written helper/endpoint/DTO paths were added. The worktree has no untracked files or build output.

All other product files, including current commit guards, connector paths, and view signatures, are byte-identical to the Runtime base. Public Agent S2 fixture `agent-26ef2bbb.json` remains unchanged at raw SHA `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`; the older S1 fixture remains unchanged at `30da4fde84c328e7cb44035b50eb53fd2cd9637a14a0c948f4412f6469ce34bd`.

## Reproducibility and tests

Passed normal generation and checks:

```text
/home/user/work/venv-runtime/bin/python generators/generate.py
node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --output-root /tmp/rt-m2-ordinary014-ts.iDOWvf
/home/user/work/venv-runtime/bin/python generators/generate.py --check
node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --check --source-root /home/user/work/wt/rt-m2-ordinary014-committed-candidate --fixture-root /home/user/work/wt/rt-m2-ordinary014-committed-candidate/conformance/fixtures
/home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
```

The private TypeScript generation output matched the checked-in conformance artifacts byte-for-byte.

Passed bounded local contract/schema/retention neighbors (explicit files): **300 passed** in 72.22s:

```text
tests/test_timeline_current_union_contract.py
tests/test_artifact_manifest.py tests/test_client_release.py tests/test_command_schema_compatibility.py
tests/test_contract_fixtures.py tests/test_schema_validation.py tests/test_spec_dedup.py
tests/test_timeline_bundle2_contract.py tests/test_timeline_commit_contract.py
tests/test_timeline_commit_type_generator.py
```

Passed central socket-capable commit lane on the actual candidate snapshot:

```text
request-test rt-m2-ordinary014-committed-candidate commit-integration --files 'tests/test_timeline_commit_integration.py'
```

Result: **9 passed** in 10.64s.

Passed central TypeScript client check on the actual candidate snapshot:

```text
request-test rt-m2-ordinary014-committed-candidate ts-client-check
```

Result: **61 passed, 0 failed**.

Passed the actual frozen Agent 310 ordinary native cohort against this exact candidate Runtime:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-m2-ordinary014-committed-candidate PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source:/home/user/work/wt/rt-m2-ordinary014-committed-candidate /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source/tests/editing_conformance/test_next_command_cohort_runtime.py
```

Result: **11 passed** in 27.08s.

## Limits and decisions

- No full suite was run, per instruction; manager batches full suites after merges.
- A first mixed local command reached 446 passes but included 13 tests requiring an unavailable default Agent checkout and one cross-product acceptance test that also required that checkout. Those tests were excluded from the bounded candidate lane, not weakened or skipped in source.
- The Python package initializer does not re-export the seven newly generated ordinary DTO names; the authorized test-only adjustment now verifies all generated DTOs in the DTO module and preserves identity checks for existing public re-exports. No package API file was added outside the exact prepared patch.
- Consumer pins, merge, publication, and activation remain held pending independent review and peer qualification. Version `0.2.14` is unpublished.
