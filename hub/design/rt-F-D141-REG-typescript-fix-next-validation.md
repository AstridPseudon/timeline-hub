# D141 REG TypeScript generator validation

Base: `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` (Runtime frozen cut).

## Repair

The existing generator was run normally with the current contract, schema manifest, and component manifest. It produced a private output tree; only these checked-in outputs changed:

- `conformance/typescript/contract-metadata.ts`
- `conformance/typescript/generated.ts`

The diff is four digest-line replacements: `CONTRACT_SHA256` and `SCHEMA_DIGEST` in each output. No contract, schema, component manifest, fixture, test, generator, package, pin, or unrelated path changed.

## Acceptance commands

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_typescript_generator.py::test_typescript_conformance_generator_is_byte_stable tests/test_typescript_generator.py::test_typescript_generator_check_rejects_client_and_manifest_mutation --basetemp /tmp/w-906c0582b8/rt-typescript-pytest.XVpTue` — **PASS**, 2 passed in 0.41s.
- `node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --check --source-root $PWD --fixture-root $PWD/conformance/fixtures` — **PASS**.
- `node --check tools/generate_typescript_conformance.mjs` — **PASS**.
- `tsc --noEmit -p conformance/tsconfig.json` — **PASS** (configured TypeScript check available).
- `git diff --check` — **PASS**.

## Byte and scope checks

- Normal generator output manifest SHA-256: `c7199949394b2594567c484f7500dc53e6e1b0b79eacb3a1240c50660dbb53d6`.
- `contract/openapi/workspace-v1.yaml`, `contract/manifest.json`, `contract/component-manifest.json`, and all listed schema inputs match HEAD byte-for-byte.
- All 15 recorded canonical client inputs match their recorded SHA-256 values and HEAD byte-for-byte.
- Current generated output hashes: `conformance/typescript/contract-metadata.ts` = `954f20745963fe246d27aa6eca810d26541ec77e326b2d44b110468e1f2bc1ce`; `conformance/typescript/generated.ts` = `285dbb51ea89c7b1a6cac6d68e9a4566231ec1b8ceaf9c6c551c4ba3d6ea16f8`.
- `git diff --name-only` contains exactly the two allowed output paths.
- Static TypeScript AST/type validation passed through the existing `conformance/tsconfig.json` check.

No full suite, duplicate pristine run, body, package installation, or contract change was performed.
