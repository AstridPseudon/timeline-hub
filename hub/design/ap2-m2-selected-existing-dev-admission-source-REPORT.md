# AP2 M2 selected existing DEV admission source

## Result

Blocked before adding a journey source. The current App integration branch has the normal local DEV project-pack admission machinery, but it does not yet have the selected-PARAM UI/capture seam that can accept a pack-owned element and create retained P1. Adding a test journey now would require a synthetic or bypassed P1, which is prohibited.

No product source was changed and no hosted pass is claimed.

## Existing authority seam

The normal DEV path is genuine and remains exact-pin based:

- `src/tools/video-editor/runtime/admitted-elements.ts:39-66` gates scoped admission to DEV, `runtimeOrigin() === ''`, and the existing `/api/astrid-element-admissions` request. `:86-93` accepts only the exact digest/module URL and exact requested refs; `:128-135` projects the admitted descriptor without rewriting its revision.
- `config/vite/vite.config.ts:87-110` wires the existing Runtime client, project-pack/artifact roots, and a canonical resolver into the admission plugin. It requires `ASTRID_ELEMENT_ARTIFACT_ROOT`, `ASTRID_PROJECT_PACKS_ROOT`, and `ASTRID_ELEMENT_RESOLVE_COMMAND`; it does not create a new transport or DTO.
- `config/vite/projectElementSelection.ts:32-90` reads the existing project-pack document, matches the exact `{packId, kind, id, revision}`, verifies the Runtime binding/document version/content digest, and verifies the retained snapshot closure. This is the path that can carry the normal editable project-pack revision `sha256:8e3abb6e6b92ec703d32997ad758537efe63cd9b1bd00b715d95fefcf2b62387` from the prerequisite report. The hosted built-in revision `sha256:2a9b21e82fc08b9222d553e680883c190dc0e9d7751e46b3fd5320c54841ac4e` is not substituted or aliased.

## Missing current seam

The current integration tree has no selected-PARAM source or UI references: these files are absent:

- `src/tools/video-editor/commands/clipParamsCapture.ts`
- `src/tools/video-editor/commands/clipParamsGesture.ts`
- `src/tools/video-editor/runtime/selectedParamAuthority.ts`
- `src/tools/video-editor/runtime/selectedParamPort.ts`

More importantly, `src/tools/video-editor/commands/elementCapture.ts` still fails closed for pack-owned captures:

- `:69-75` rejects selected project-pack element capture without authoritative Agent schema capture.
- `:220-221`, `:233-234`, `:264-265`, and `:283-287` reject selected `schema_source`/pack-owned element and parameter capture.

Therefore the real product cannot currently accept the normal admitted 8e descriptor as selected P1, much less preserve it through the requested later P2 refusal, retry/reload/undo, and zero-legacy assertions.

## Smallest patch request

The App selected-PARAM owner should land the already-qualified selected carrier/mounted path on this integration branch: native `clip.set-element`/`clip.set-params` capture through an authoritative retained `DocumentPin`, retained reads through commit/restore, and the existing PropertiesPanel → ClipPanel → AstridElementParams forwarding. The current fail-closed checks should only be relaxed as part of that authoritative carrier implementation.

This request does not require a new route, provider, DTO, catalog revision, capture-port injection, gateway, owner stripping, or public pin. After that seam lands, the local-DEV journey owner can add one ephemeral Vite/Runtime fixture that initializes and admits a real project pack, configures the existing resolver/root environment, and exercises exact 8e through the existing `/api/astrid-element-admissions` path.

## Checks

- `node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/runtime/admitted-elements.test.ts src/tools/video-editor/runtime/admitted-elements.hosted.test.ts src/tools/video-editor/commands/elementCapture.test.ts` — **passed**, 3 files / 15 tests.
- `node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/runtime/admitted-elements.ts config/vite/projectElementSelection.ts config/vite/astridElementAdmissions.ts src/tools/video-editor/commands/elementCapture.ts tests/e2e/local/three-products.spec.ts tests/e2e/local/support/harness.ts` — **passed**.
- `node_modules/.bin/playwright test --config playwright.three-products.config.ts --list` — **passed**, collected 9 existing tests; no browser or socket run.
- `git diff --check` — **passed**; worktree remains clean.

The actual local Runtime/project-pack admission and browser journey are intentionally unverified because the current product seam is missing and the task forbids local browser/socket/full runs. A later central targeted run is required after the owner patch lands.
