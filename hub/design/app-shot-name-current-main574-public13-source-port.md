# App M2 embedded shot-name port to current MAIN574/public13

Status: source port complete in the assigned App worktree. No browser or full-suite
qualification was run here. The central browser wrapper must be created only after
the harness commits this worktree and can provide the exact resulting App commit
and tree.

## Exact source and target mapping

| role | commit | tree | identity |
|---|---|---|---|
| qualified frozen App source | `a817718c168a2bd0b893724836dd3e79c4efdcf8` | `c037e8f9a4d751eebfd5b86b77c6d2974338ece3` | old MAIN17/public12 source; central shot-name pass |
| source product port | `8f27c052b6ba6cdeb70066f188d5d5aa72d617ef` | source ancestor of the qualified slice | native embedded shot.set session |
| source history/dependency qualification | `e245125168979218ebc0fcc880b59769250a4039` | included in `c037e8f9a4d751eebfd5b86b77c6d2974338ece3` | accepted history dependency assertion |
| current target base | `3e24e0632669375a84e75c8ff0da315bdc88a45c` | `99b5824907f8d3a1081398733028adc3670f020d` | current MAIN574/public13 App2 root |
| new current candidate | harness-generated after this worker exits | not yet knowable | must be committed before any strict current-root browser wrapper |

The source gate's central synthetic final tree is the qualified source tree
`c037e8f9a4d751eebfd5b86b77c6d2974338ece3`; it is not a claim about the new
current-root tree.

## Ported delta

- Added the occurrence-owned `shot.set` capture/finish/submit command and its
  conformance/session tests.
- Added accepted-receipt completion settlement and refusal propagation to the
  durable command session. The name editor closes only on accepted intent
  completion and restores the exact untrimmed draft on refusal.
- Added current-root `shotSet` wiring alongside, not instead of, the existing
  element, generic-patch, and track-label ports.
- Ported the mounted embedded `ShotEditorView` name capture and optimistic
  display behavior, plus the hook lifetime/shot-scope guards.
- Added the real embedded browser case, production-specific shot-name locator,
  and seed provenance/opaque shot payload.

No public13 package, lockfile, settings surface, gallery writer, standalone
activation, or row-deletion behavior was changed.

## Required current-case wrapper after harness commit

The new wrapper must use the harness-generated App commit and full tree, with a
strict declared commit -> tree guard. It must not run against a dirty source
snapshot, moving `/home/user/work/app`, or a placeholder SHA. Keep the frozen
Agent/Runtime pins and the current private public13 Composition artifact
qualification in the wrapper. Register exactly the one shot-name test through
`playwright.shot-name.config.ts); do not bypass the declared source guard.

## Evidence run in this worker

All Vitest runs used a private extracted public13 package overlay (artifact SHA256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`), an own
runner preload, `--configLoader=runner`, `--no-cache`, one worker, and private
cache/output paths. Shared `node_modules` and caches were not modified.

```text
eslint --max-warnings 0 [all touched source/test/e2e/config files]
PASS

Vitest focused shot/session/editor lane:
7 files, 132 tests passed

Vitest focused neighbouring ShotEditor/project/direct-control/projection lane:
7 files, 41 tests passed

node_modules/.bin/playwright test --config playwright.shot-name.config.ts --list
PASS: exactly 1 discovered test in 1 file

git diff --check
PASS
```

Not run: full suite, browser/localhost/socket journey, Runtime HTTP acceptance,
TypeScript check, build, install, or central test-service browser request.

## Remaining writers / boundary

The bounded embedded parent-mounted `ShotEditorView` path is the only name
writer activated by this port. These remain intentionally outside the slice:

- `src/tools/travel-between-images/components/VideoGallery/VideoShotDisplay.tsx`
  gallery/list `useUpdateShotName` mutation.
- `src/tools/travel-between-images/pages/ShotEditorView.tsx` fallback
  canonical publisher and ordinary legacy mutation when no mounted shot port is
  present, plus its separate canonical settings writer.

The row is therefore partial by design; no zero-legacy-writer or settings/gallery
claim is made. The next owner step is the dedicated current-root browser executor
after the harness commits and records the exact new App SHA/tree.
