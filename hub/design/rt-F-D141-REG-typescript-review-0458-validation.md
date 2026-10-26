# Validation

## Identity and scope

- Commit: `4a66dee1ab34f260ea64bd58aa30cf7ac66c3ae3`
- Tree: `caed21305ca483591ed60d5d2bebd8b30b525d5b`
- Exact parent/base: `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`
- `git diff --name-only 6a011d58e6..HEAD`: exactly `conformance/typescript/contract-metadata.ts` and `conformance/typescript/generated.ts`.
- `git diff --check 6a011d58e6..HEAD`: PASS.
- Worktree status after review: clean.

## Tests and checks

1. `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_typescript_generator.py::test_typescript_conformance_generator_is_byte_stable tests/test_typescript_generator.py::test_typescript_generator_check_rejects_client_and_manifest_mutation --basetemp=/tmp/rt-F-D141-typescript-review-ls1SvF/basetemp -o cache_dir=/tmp/rt-F-D141-typescript-review-ls1SvF/cache`
   - PASS: `2 passed in 0.42s`.
2. `node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --check --source-root "$PWD" --fixture-root "$PWD/conformance/fixtures"`
   - PASS, exit 0.
3. `node --check tools/generate_typescript_conformance.mjs`
   - PASS, exit 0.
4. `tsc --noEmit -p conformance/tsconfig.json`
   - PASS, exit 0.
5. Normal generation to a private `/tmp` output root using the same contract/schema/component inputs.
   - PASS: both checked-in TypeScript outputs are byte-equivalent to normal generation.
   - Generated manifest SHA-256: `c7199949394b2594567c484f7500dc53e6e1b0b79eacb3a1240c50660dbb53d6`.

The first attempted pytest invocation used the task-provided `.../tmpdir` path. That path is a regular-file sentinel in this worker environment, so pytest setup failed with `NotADirectoryError`; no test executed and no source was touched. The exact tests were rerun successfully with a private `/tmp` directory.

## Contract review

`contract/commit-v2.md` was read against the requested C0v2 surface. The reviewed contract specifies the base revision/publication pair, semantic and `doc.patch` commands, label, per-step patches and ordinals, `fields|atomic`, declared reads, `Idempotency-Key`, `dry_run`, source/rationale/group annotations, accepted/merged/conflict/invalid/preview replies, canonical authenticated closure and receipt bindings/effects/dependencies/history/guarded undo, conflict reason/head, invalid code/path/hint/suggested command, and preview with no mutation. This generated-output fix does not alter that contract.

The prior REG join remains the evidence for the original two TypeScript-generator failure nodes. This review makes no claim that the full Runtime/P5 suite was rerun on the new head.
