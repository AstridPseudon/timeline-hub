# ap2-m2-selected-normal-catalog-fixture-prerequisite

## Result

No App source or e2e fixture was added. The requested selected-PARAM case is
blocked on a real normal catalog carrier, not on the App command path.

The frozen hosted App catalog declares the built-in
`audio-reactive-colour` entry as:

```text
kind=effect packId=rendering id=audio-reactive-colour
revision=sha256:2a9b21e82fc08b9222d553e680883c190dc0e9d7751e46b3fd5320c54841ac4e
publication=published
```

The normal Agent project-pack admission path computes a different descriptor
revision because it calls `load_element_definition(... editable=True,
priority=100)` for project-pack declarations. The reviewed normal admission
is therefore `sha256:8e3abb6e6b92ec703d32997ad758537efe63cd9b1bd00b715d95fefcf2b62387`,
not the hosted built-in `2a9b...` entry. Treating 8e as 2a, or making a
synthetic P1 record that claims 2a, would violate the settled task boundary.

## Existing App API finding

The existing project-pack facade is real but local-development-only:

- `src/tools/video-editor/runtime/admitted-elements.ts:41` enables scoped
  admissions only when `import.meta.env.DEV`, the virtual admission module is
  configured, and `runtimeOrigin() === ''`.
- `src/tools/video-editor/runtime/admitted-elements.ts:62-67` reads the
  existing `/api/astrid-element-admissions` Vite route only in that mode.
- `src/tools/video-editor/runtime/admitted-elements.ts:128-135` projects an
  admitted descriptor to the existing catalog view with its actual
  owner/kind/id/revision, `published` state, schema, defaults, and
  renderability.
- `src/tools/video-editor/runtime/astrid-element-components.tsx:100` merges
  those exact admitted descriptors into the installed host, and
  `VideoEditorProvider.tsx:262-272` scopes/refetches only non-built-in exact
  refs.
- The hosted build deliberately skips that route and keeps the compiled
  catalog. The focused hosted test proves this: with a gateway origin,
  `refreshAdmittedElements()` makes no fetch and no project admission becomes
  observable.

Thus an actual 8e project entry could be observed by the App only in the
local DEV admission path, but the frozen hosted three-products journey cannot
observe it. The built-in 2a entry has no existing retained schema-source
carrier that can turn it into the missing normal admitted P1. The selected
PARAM UI already requires the existing retained authority port and emits the
native `clip.set-params` command once it has a real owner-qualified clip and
pin; no App capture-port injection is appropriate.

## Exact peer request

See `peer-app2-to-viewing-d10-selected-normal-catalog-carrier.md`. This is a
source/owner dependency request, not permission to edit the public catalog,
add a route/DTO, or pin a new release.

## Verification

- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --no-file-parallelism --pool=threads src/tools/video-editor/runtime/admitted-elements.hosted.test.ts`
  — **PASS**, 1 file / 3 tests.
- `node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/runtime/admitted-elements.ts src/tools/video-editor/runtime/astrid-element-components.tsx src/tools/video-editor/contexts/VideoEditorProvider.tsx tests/e2e/local/three-products.spec.ts tests/e2e/local/support/harness.ts`
  — **PASS**.
- `git diff --check` — **PASS**.

No browser, localhost, live socket, full suite, dependency install, product
source edit, public-catalog hash edit, or synthetic admission was performed.
