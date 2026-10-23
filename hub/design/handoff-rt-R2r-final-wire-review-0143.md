# FAIL — R2r final wire review

Runtime producer: `623c4ad18737628e1f2c9e85a07098da469d6a4d`  
Tree: `a3174823ba115531e1ca0227d8292431197a3e52`

Concrete defect: dry-run success omits required `would_status`.

- Contract requires `would_status: "accepted" | "merged"`: `contract/commit-v2.md:1339-1344`; executable assertion at `:4715`.
- Canonical schema omits and does not require it: `contract/schemas/timeline-commit.json:1069-1134`.
- Runtime producer omits it: `runtime_protocol/timeline_commit_store.py:988-1004`.
- Generated Python/TypeScript types also omit it: `runtime_protocol/timeline_commit_types.py:97`, `packages/typescript/src/timeline-commit-types.ts:95`.

Minimum fix: add the required enum field to the canonical schema, emit the correct accepted/merged value from the preview producer, regenerate all clients/bundles/manifests, and add the corresponding behavior assertion.

Validation:

- Targeted service `rt-R2r-final-wire-review-0143-targeted-1023014535-23575`: **109 passed**.
- `npm run build --prefix packages/typescript`: **passed**.
- `python generators/generate.py --check`: **passed**.
- `node tools/generate_typescript_conformance.mjs ... --check`: **passed**.
- `python scripts/artifact_manifest.py --check`: **passed; manifest current**.
- `git diff --check`: **passed**.
- Ruff 0.16.8: **75/75**, 20 identities, **0 new** against auth baseline and integration.
- Pyright 1.1.414: **76/76**, 10 identities, **0 new** against auth baseline and integration.

Schema/source identities:

- Canonical Agent edit schema source: commit `7689fd97b72d93061b50d3d85922b33a13703cd5`; SHA-256 `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- Python/TypeScript `SCHEMA_DIGEST` values agree: `sha256:f9f9e42cecd5ab788e53725eb2468caea630c4631f50cf21d4f9d5e07283f1bb`.
- Normal route/coordinator/port/store paths and generated artifacts are present; no alternate executor or overlay was found.
- Working tree remains clean; no accidental untracked files.

No full/browser/P5/native14 suites were run. Production acceptance/P1/H3 remains gated pending the dry-run wire fix and integrated proof.