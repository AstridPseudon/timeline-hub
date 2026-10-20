# App media CORS authorized current

Completed the one bounded shared-media CORS unit on App refreshed-main base
`35dbb0eb12d75dc2c1becf7a9d8ac914758c05c7` (tree
`74d6c8033b1e006e8dbd4accc361b4e1288093e9`). The approved proposal patch was
applied to `src/shared/lib/media/mediaCrossOrigin.ts`; permanent direct
regressions were added only to its existing test file.

## Source behavior

- Configured absolute `http:` and `https:` gateway URLs now use anonymous CORS
  and omit browser credentials.
- The existing `isManagedObjectUrl` predicate remains unchanged and retains its
  anonymous/omit behavior for canonical relative and managed absolute routes.
- Blob, data, custom, signed external, protocol-relative, and other-origin
  media retain their existing mode; configured-origin blob URLs are explicitly
  covered.
- No auth/provider, Runtime handler, content route, fetch/routing, or authority
  policy changed. The original HoverScrubVideo gateway tests and inputs are
  untouched.

## Exact final delta

Changed paths:

```text
src/shared/lib/media/mediaCrossOrigin.ts
src/shared/lib/media/mediaCrossOrigin.test.ts
```

Diff: `48 insertions / 6 deletions`; binary patch SHA-256:
`9dfb56e95cd6da0dda5bb394b73c7c898f4bd939ee26bd64281142659e1bbcb1`.

Final file SHA-256 values:

```text
d90c2383739f5c179f542c2c8e50ee32389b83bacdeb533d6d3117609a43f312  src/shared/lib/media/mediaCrossOrigin.ts
a6c2c150b25b9b26e15b7cbbbc412d8f08d1d3bcf416ae244f441b159bb8f65c  src/shared/lib/media/mediaCrossOrigin.test.ts
```

## Verification

Final bounded command, from the App worktree, using read-only shared
dependencies, one worker, no file parallelism, runner config loading, and no
Vitest cache:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-media-cors-authorized-current/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/shared/lib/media/mediaCrossOrigin.test.ts src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx
```

Result: **2 files / 23 tests passed, exit 0**, Vitest 4.1.5. `git diff
--check` also passed. A direct invocation without the preload failed before
test collection because this legacy config references `__dirname` under the
runner loader; the preload is the established non-product compatibility fix.

No full suite, build, browser, socket, localhost service, TypeScript check,
install, or shared dependency/cache edit was run. No successful media byte
retrieval or liveness claim is made.
