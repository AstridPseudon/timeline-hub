# Public Trim: existing native-port readiness observation

Date: 2026-10-21

## Closure source

The original fixture remains a mounted production assembly. Its relevant
closure is:

1. `tests/e2e/local/public-trim-mounted-fixture.spec.ts` opens
   `tests/e2e/fixtures/public-trim/index.html` and invokes the existing
   `public-trim-trigger` button. The original Trim body, including its source
   window assertion (`in_s: null`, `out_s: 2.5`), reload, undo, retry, raw
   request, idempotency, credential, timeout, and zero-legacy assertions is
   unchanged.
2. `tests/e2e/fixtures/public-trim/main.tsx` mounts the real
   `BrowserVideoEditor` with the real `RuntimeDataProvider`, the real
   `PUBLIC_TIMELINE_SERVICE_HOOKS`, and the real scoped host-service assembly.
3. `src/tools/video-editor/browser/BrowserVideoEditor.tsx` delegates to
   `BrowserVideoEditorProvider`; `src/tools/video-editor/browser/BrowserVideoEditorProvider.tsx`
   mounts the production `EditorRuntimeProvider`.
4. `src/tools/video-editor/hooks/useTimelineState.ts` receives the production
   command state and publishes `save.commands.clipTrimPort` as
   `editorOps.clipTrim`, then seeds/synchronizes that `editorOps` object into
   the existing `TimelineStore`.
5. `src/tools/video-editor/hooks/useTimelineCommandSession.ts` obtains the
   native `clipTrimPort` from `createTimelineCommandSession` and wraps its
   existing `capture`, `finish`, and `submit` methods with the existing
   session-cleanliness guard before the store receives it.
6. `tests/e2e/fixtures/public-trim/FixtureControls.tsx` is already inside
   that real store. It now reads the existing `useTimelineEditorOps()` value
   and reports whether the existing `ops.clipTrim` has all three native port
   methods. It does not create a Provider, create a port, add a product hook,
   or add a production readiness API.

This distinguishes source wiring from runtime readiness: the browser test
must observe the mounted store value before it clicks the original action.

## Exact command delta

The only behavior assertion added to the original fixture closure is in
`openFixture`, before the existing click:

```ts
await expect(page.getByTestId('public-trim-result'))
  .toHaveText(JSON.stringify({ nativeClipTrimPortReady: true }), CEILING);
```

The existing fixture diagnostic output is extended only when no Trim result
has yet been written:

```tsx
const trimPort = ops.clipTrim;
const nativeTrimReady = !!trimPort
  && typeof trimPort.capture === 'function'
  && typeof trimPort.finish === 'function'
  && typeof trimPort.submit === 'function';

<output data-testid="public-trim-result">
  {result || JSON.stringify({ nativeClipTrimPortReady: nativeTrimReady })}
</output>
```

After the original Trim action runs, `result` still contains exactly the
existing `commands.trimClip({ clipId: clip.id, endTime })` result. The action
and all original assertions remain actual and unchanged.

## Verification command delta

No browser/actual, full suite, build, install, or new graph was run here.
The cheap checks for this source-only fixture delta are:

```bash
git diff --check
env -i HOME=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/home LANG=C.UTF-8 \
  PATH=/opt/node20/bin:/usr/bin:/bin \
  npm_config_cache=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/npm-cache \
  npm_config_offline=true \
  VITE_CACHE_DIR=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/vite-cache \
  XDG_CACHE_HOME=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/xdg-cache \
  npm exec -- playwright test --config playwright.public-trim.config.ts --list

env -i HOME=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/home LANG=C.UTF-8 \
  PATH=/opt/node20/bin:/usr/bin:/bin \
  npm_config_cache=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/npm-cache \
  npm_config_offline=true \
  /opt/node20/bin/node --import ./node_modules/tsx/dist/esm/index.mjs \
  --test tests/e2e/local/support/public-trim-preflight.test.ts
```

The held main command remains the exact direct Playwright command in
`run-on-main-app-public-trim-current.md`; this change supplies only its
existing-fixture readiness observation and does not authorize running it here.
