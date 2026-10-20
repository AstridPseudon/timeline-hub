# App provider service five type narrowings

## Result

PASS. Fixed only the five diagnostics reported by `app-current-cap-provider-assembly-gate` in `src/tools/video-editor/hooks/useTimelineCommandsService.ts`.

## Source change

- Kept the existing `addClip` overload API and implementation behavior, while expressing its synchronous and asynchronous paths through a typed overload function.
- Added a typed provider capability intersection for `getProjectVerifiedMedia` and narrowed the nullable project ID before constructing `parentMediaRuntime` in both service hooks.
- Preserved existing captures, guards, records, payload bytes, port calls, and runtime behavior for valid inputs. No App2 Generic/membership implementation was changed; no `any`, suppression, or coercion was added.

## Evidence

- `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/dirname-preload.cjs /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/private13/node_modules/vitest/vitest.mjs run --config vitest.private13.tmp.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx`: exit 0, 6 files and 156 tests passed.
- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/useTimelineCommandsService.ts --report-unused-disable-directives --max-warnings 0`: exit 0.
- `git diff --check`: exit 0.
- `flock -x /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/private13/node_modules/typescript/bin/tsc --noEmit -p tsconfig.private13.tmp.json`: exit 0. The mapped Composition package was 0.0.13 (all77/archive9412).

No full suite, browser, install, build, or shared dependency/cache writes were performed.
