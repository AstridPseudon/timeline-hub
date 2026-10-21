# App2 M2 owned Vite retention/cache review — 0132

## Disposition

**APPROVE the exact two-file hunk at commit `ff5c4c2809b476c82de46efc2b48d815b5609ff0`, subject to the already-required HOME ownership consent before merge.** No source edits were made.

Exact reviewed files and hashes:

- `config/vite/projectElementSelection.ts` — blob `ad5ae0f785e1780d1b13f09dad0744db9e04a074`
- `src/tools/video-editor/runtime/project-element-selection.test.ts` — blob `61295a46f7f36cc0f79a0b2a449bf483e561b5d2`
- Two-file patch SHA-256: `dfcfb591a5f5f6183e61d47d0458916969f215c7f76a81dc91135869d3fabd7e`

The named base is the reviewed commit, so I treated `ff5c4c280` as the requested 0115 retention/cache hunk. The divergent `43aa31739` branch was not used as evidence.

## Review findings

- `selectProjectElements` preserves the selected Runtime admission's exact `snapshot_object` beside the existing resolver `binding`; it does not manufacture an object or replace it with a catalog/latest/system-8e value.
- The resolver cache key includes realm, project, all four ref fields, document ID, document version, document content digest, selected snapshot digest, source binding, manifest, source root, artifact root, and the host version marker. The document content digest is the same stable JSON digest checked against `resolved.binding.contentDigest`.
- Exact project/ref/source checks remain in place: Runtime document identity and project, selected pack/admission, resolver binding, descriptor ref, canonical pack root, snapshot root, and sorted snapshot-closure hash are all checked before verification.
- Cache writes occur only after resolver binding checks, path/closure checks, and `verifyElementAdmissions` succeed. Failures therefore do not populate `resolvedCache`.
- The focused regression mutates document version and `snapshot_object`, then proves a second resolver call and the refreshed object, preventing a mutable-alias or stale-hit after document change. The existing controls cover stale binding, canonical snapshot mismatch, absent old pin without latest substitution, foreign project/source binding, read-only discovery, and unrelated-document isolation.
- The existing virtual-module generator strips `snapshot`/local snapshot paths before serializing `elements`; this hunk adds only the pre-existing binding and typed four-field snapshot-object metadata. No new route, DTO, store, catalog/public authority, credential, save path, or production caller was added. The dormant accessor and f83 consumer remain untouched and inactive.

## Evidence

Passed:

- `TMPDIR="$PWD/.tmp-review" npm exec vitest -- run --config config/testing/vitest.config.ts src/tools/video-editor/runtime/project-element-selection.test.ts --testNamePattern='reads one canonical|invalidates only|loads no artifact|rejects stale|does not substitute latest|rejects a different project' --no-file-parallelism --maxWorkers=1` — 1 file, 6 passed, 1 skipped (the existing localhost Vite-transform test).
- `./node_modules/.bin/eslint config/vite/projectElementSelection.ts src/tools/video-editor/runtime/project-element-selection.test.ts src/tools/video-editor/runtime/admitted-elements.ts src/tools/video-editor/runtime/admitted-elements.test.ts --max-warnings 0` — passed.
- `./node_modules/.bin/tsc --noEmit --pretty false -p tsconfig.node.json` — passed.
- `git diff --check HEAD^ HEAD && git diff --check` — passed.

An attempted direct run of the full focused test file reached the expected sandbox limitation in its one localhost test: 6 passed and the Vite test failed only with `listen EPERM: operation not permitted 127.0.0.1:5173`. No localhost, browser, broad 28-test, or full suite evidence is claimed.

## Merge guard and next step

HOME ownership consent for this exact hunk remains a prerequisite; this review does not grant that consent or authorize a merge. Keep the accessor dormant and do not activate an f83 consumer until the separately required owner/source contract is present.
