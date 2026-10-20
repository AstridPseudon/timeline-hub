# Runtime ordinary014 current-server candidate

Status: UNPUBLISHED / REVIEWABLE CANDIDATE ONLY. No integration adoption, consumer pin, publication, release, or activation was performed.

## Composition and identity

- Official producer source: Runtime commit a0dca16975dfe8f5e762703b99d9791a16cf7fd7 (tree 4b7dd0fe44be973c344bab3de568eaf0bdd28476), immutable.
- Current server parent composed: 9f211fcdb66023a577a14111f99c87fb32ef573c, immutable for this task.
- Central candidate source/tree SHA: ea1ffe7e09ebf679abf409b060e753c17bdabe0d (the central test-service snapshot including the retained current test file). Harness commit SHA is intentionally pending.
- Frozen Agent source: 310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3.
- Package version: 0.2.14 (unpublished).
- Frozen Agent raw schema: sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d.
- Runtime wire schema digest: sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59.
- Artifact producer: astrid-runtime.
- Artifact version: sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0.
- Artifact manifest SHA-256: ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815.
- Counts: 75 artifact paths, 55 schema definitions, 29 command operations, 133 unique HTTP operations.

The 75 declared artifact paths are byte-identical to official a0dca16; the manifest has zero byte/hash mismatches. The official producer and artifact identity remain a0/f021; the server candidate has the new source/tree SHA above.

## Exact compatibility diff allowlist

Relative to current server 9f211fc, only the official014 generated/artifact/export compatibility cohort is changed:

    conformance/typescript/contract-metadata.ts
    conformance/typescript/generated.ts
    contract/artifacts.json
    contract/schemas/edit-command.json
    generators/python_client_init_template.py
    generators/release.json
    packages/python/astrid_runtime_client/__init__.py
    packages/python/astrid_runtime_client/contract_metadata.py
    packages/python/astrid_runtime_client/generated.py
    packages/python/astrid_runtime_client/timeline_commit_types.py
    packages/python/pyproject.toml
    packages/typescript/package-lock.json
    packages/typescript/package.json
    packages/typescript/src/contract-metadata.ts
    packages/typescript/src/generated.ts
    packages/typescript/src/timeline-commit-types.ts
    runtime_protocol/contract_metadata.py
    runtime_protocol/schemas/timeline-commit-bundle.json
    runtime_protocol/timeline_commit_types.py
    tests/test_timeline_current_union_contract.py

The current server's CAS, unplaced project-shot promotion/text binding, catalog fence, clip-replacement, door-audit, and shell/runtime changes remain byte-identical to 9f211fc, including tests/test_render_native_historical_retry.py. No private carrier material, version-2 surface, endpoint, release pin, or current tuple change was copied.

## Evidence

Passed normal generation and artifact checks:

    /home/user/work/venv-runtime/bin/python generators/generate.py --check
    /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
    node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --check --source-root "$PWD" --fixture-root "$PWD/conformance/fixtures"

The bounded generated/contract lane passed 300 tests:

    /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_current_union_contract.py tests/test_artifact_manifest.py tests/test_client_release.py tests/test_command_schema_compatibility.py tests/test_contract_fixtures.py tests/test_schema_validation.py tests/test_spec_dedup.py tests/test_timeline_bundle2_contract.py tests/test_timeline_commit_contract.py tests/test_timeline_commit_type_generator.py

Central socket-capable CAS/text/door lane, with explicit node/file selection, passed 77, had 1 deselected and 1 existing strict xfail:

    request-test rt-m2-ordinary014-current-server-compose targeted --files "tests/test_door_transport.py tests/test_shot_text_bindings.py tests/test_shot_candidate_promotion.py::test_candidate_promotion_is_atomic_fixed_point_and_byte_stable_on_replay tests/test_shot_candidate_promotion.py::test_candidate_provenance_is_verified_before_promotion tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_public_http_route tests/test_timeline_shot_authority.py::test_authenticated_http_shot_writes_are_retired tests/test_timeline_shot_authority.py::test_http_auth_and_scope_checks_precede_retirement tests/test_timeline_shot_authority.py::test_http_foreign_project_never_mutates_shot tests/test_timeline_shot_authority.py::test_http_text_binding_auth_and_film_scope_checks_precede_writes"

The existing xfail was test_replace_timeline_clip_public_http_route (retired direct route awaiting commit-path replacement); it was not added or changed here.

Central nine-case commit integration passed:

    request-test rt-m2-ordinary014-current-server-compose commit-integration --files "tests/test_timeline_commit_integration.py"

Result: 9 passed.

The worker-local attempt at the broader touched CAS/text selection reached 57 passed and 9 existing xfailed, but socket-backed cases failed with sandbox PermissionError: [Errno 1] Operation not permitted, and two Agent-dependent cases could not find the default Agent checkout. Those cases are not claimed; the socket cases were rerun centrally above. No full suite was run. Consumer-native qualification remains a later peer task.
