# App2 M2 mounted selected-param setup classification

## Result

This was fixture readiness, not a missing HOME/shared port. The failure was the
second test in `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx`:

```text
refuses a mounted edit whose retained read completes after the command session is gone
  await waitFor(() => expect(latest.current?.commands.clipParamsPort).toBeDefined())
```

On the prior source, the full file failed at that readiness wait while the
direct late-read test passed when run alone. The command state reached `saved`,
but the mounted hook could render once before its async session wrapper was
assigned, leaving the fixture's `latest.current` surface stale. The real port
was present: `commitSession.ts:784-...` constructs `clipParamsPort`, and
`useTimelineCommandSession.ts:199-231` wraps it before returning it at line 449.

The smallest correction is test-helper-only: `MountedForm` performs one local
refresh when the command session has left `loading` but the real port has not
yet appeared on the returned hook surface. This waits for the existing
production port; it does not manufacture or substitute a port.

No HOME shared seam patch is required. No Provider, session, `useTimelineOps`,
or other shared source was edited. All late-read, missing-carrier, and
dirty-draft assertions remain unchanged.

## Actual live callers

- `AstridElementParams.ts:54-70` reads `editorOps.selectedParam` (or the
  equivalent `selectedParamProp`), resolves the original authority, captures
  the clip, prefetches retained inputs, and submits `clip.set-params`.
- `useTimelineState.ts:1146` publishes `save.commands.clipParamsPort` as
  `selectedParamPort`; `useTimelineState.ts:1237` places the same port in
  `editorOps.selectedParam`.
- `useTimelineCommandSession.ts:199-231` applies the late-read/cleanliness
  wrapper and `:449` exposes the wrapped port.
- `commitSession.ts:784-848` is the underlying capture/prefetch/finish/submit
  implementation; it requires the admitted owner-qualified element and the
  retained schema source. Its missing-carrier refusal remains intact.

## Verification

Before the fix, the full mounted file reproduced **1 failed / 1 passed**;
running only the late-read test passed, identifying test-order/setup readiness
rather than a product port absence.

After the fix:

```text
TMPDIR=/tmp/ap2-m2-element-mounted-param-setup-source-0055-tmp \
node /home/user/work/app/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx \
  -t 'uses the production selected carrier|refuses a mounted edit whose retained read completes after the command session is gone'
Result: 1 file, 2 tests passed.
```

Also passed:

```text
node /home/user/work/app/node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx
git diff --check
```

No browser, localhost, live socket, full suite, pin/activation, new carrier,
or central qualification was run or claimed. Shared dependencies remained
read-only.
