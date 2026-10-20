# App TrackInspector private-cache verification

## Verdict

PASS for the bounded three-file verification on source commit
`d821e5587e4d428e9e3e3dfbe5b7195e192bd00e`, tree
`aedee085ec20135e896a6d258dc1845cc352f423`. The worktree was clean before
and after; no product, guard, assertion, or test source was changed.

## Exact source and test scope

The command covered exactly:

- `src/tools/video-editor/components/PropertiesPanel/TrackInspector.test.tsx`
  (159 lines)
- `src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx`
  (2528 lines)
- `src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx`
  (871 lines)

Result: **3 files passed, 120 tests passed, exit 0** with Vitest 4.1.5.
This preserves the real TrackInspector command/capture/guard/refusal behavior,
the phone/tablet Canvas selection boundary, and the TrackList reference.

The brief's `181 PASS` number is not the count for this exact three-file
allowlist. The prior 181-test run included two additional files,
`TrackLabel.command.test.tsx` and `PropertiesPanel.test.tsx`; it is not claimed
as evidence for this bounded run. The prior independent standard bundled-loader
run of the exact three-file allowlist reported 120 passed; it was not rerun
because that loader may write shared Vite cache state.

## Primary command

The worktree-local `node_modules` overlay linked package entries read-only from
`/tmp/app-coherent-deps12/node_modules`; its cache directories were owned by
this worktree. The exact runner-loader command was:

```sh
env TMPDIR="$RUN/tmp" XDG_CACHE_HOME="$RUN/xdg-cache" npm_config_cache="$RUN/npm-cache" NODE_PATH="$PWD/node_modules" \
  node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
  node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/components/PropertiesPanel/TrackInspector.test.tsx \
  src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx \
  src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx
```

The preload supplied the missing CommonJS `__dirname` required by the config
under `--configLoader=runner`. No bundled-config fallback was used for the
primary result.

## Cache guard

Before and immediately after the primary run, recursive snapshots of shared
`/home/user/work/app/node_modules/.vite` and `.vite-temp` recorded file types,
byte sizes, mtimes, and file SHA-256 values. Both snapshots had 643 records
and the same SHA-256:

`d61bbb12c0d386fc9ce694aa6e8f678348d2d4f99d35ffae46c09cf44fdfa37c`

Therefore the primary run did not change shared cache state. The owned overlay
and its private caches were then removed, and the worktree's original
`node_modules -> /home/user/work/app/node_modules` symlink was restored.

After that immediate guard, a later read observed unrelated external drift in
shared `.vite` (a temporary dependency bundle disappeared and the root mtime
changed). No active Vite/Vitest writer was present when checked. The shared
cache was not repaired or modified; this later drift does not change the
before/after result for the primary run but should be considered when relying
on shared cache state.

## Limits

No fallback rerun, full suite, build, browser/e2e, TypeScript check, install, or
product edit was performed. The 120-test result is the verified result for the
requested exact three-file scope.
