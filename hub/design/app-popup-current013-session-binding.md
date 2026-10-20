# App D01 popup current013 session binding

## Source and tree

App worker tree: `/home/user/work/wt/app-m2-popup-current013-session-binding`.

Base source: `b1ef4b9b910ba72375c34cf319692f90d22edc25` (`tl/app-m2-popup-current013-session-binding`). The worktree is intentionally uncommitted for the harness. The source candidate adds the occurrence capture/session plumbing, Runtime selection/verified-media adapters, popup controls, and the parent-to-popup wiring listed by `git status`; no shared serializer/projection file was changed.

The native capture implementation was ported from the approved app source branch `tl/app-m2-popup-core-qualify` at `309cb7a463833126e3af730fb3c6ff536d9e457c`. The popup control shape was reviewed against the frozen R4 candidate at `8f0c2484463e9b666d184a744d52e252984e551a`; its nested writer was retained only as the fallback, not copied as the qualified native path.

## Installed caller path

The qualified caller is the parent Astrid editor:

`AstridTimelineEditor.tsx` → `LocalTimelineShotBrowser.tsx` → `ShotEditorView.tsx` → `ShotTimelinePreview.tsx` → `ShotTimelineEditorSurface` → `ShotTimelineMediaControls.tsx`.

The parent passes the existing `occurrenceMediaPort`, parent `TimelineDataRef`, Runtime `getProjectMediaSelection/getProjectVerifiedMedia`, and Runtime `prepareMediaImport`. The session port captures against the parent data reference, not the popup's projected display data. The popup builds requests only from the explicit occurrence route and projected canonical owner/clip identity; it does not derive ownership from shot IDs, display IDs, or `(shotId, trackId)`.

ADD/SWAP uses the existing five-field selection, verified-media read, reserved child identity, create-or-require registry binding, original graph/basis/guards, native occurrence command, and the existing occurrence preview/outbox path. Capture/read/finish errors stay errors; there is no fallback after native capture begins.

## Replaced and remaining branches

For the qualified Astrid parent, popup ADD/SWAP now takes the native occurrence branch. The old prepared-media `commands.addClip` branch remains in `ShotTimelineMediaControls` for callers without the qualified parent port and for unsupported provider capabilities.

Remaining unqualified callers include the standalone `AstridTravelRoute.tsx` construction of `LocalTimelineShotBrowser`, tests/direct popup mounts, and any local/shared/ambiguous caller that does not provide the internal parent session port. The nested shot timeline persistence writer and other popup edits remain unchanged. This is not a claim of full popup writer retirement.

## Tests and checks

- Targeted runner command: `NODE_PATH=/tmp/app-coherent-deps12/node_modules node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.test.ts src/integrations/runtime/dataProvider.test.ts`: **141 passed / 141**.
- Session neighbor command: `NODE_PATH=/tmp/app-coherent-deps12/node_modules node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx`: **39 passed / 39**.
- Popup smoke command with the same private runner, `ShotTimelinePreview.test.ts -t "does not pass current-time mirroring"`: **1 passed / 1**.
- Targeted ESLint over all touched source files: **passed**.
- `git diff --check`: **passed**.
- A broader popup/local/Astrid invocation was not accepted as evidence: the runner-loaded repository test setup omitted Testing Library matchers, producing baseline `Invalid Chai property: toBeInTheDocument/toHaveTextContent` failures. The initial run also caught and fixed a product `mediaImportProvider` reference error; the focused popup smoke rerun is green.

## Actual next gate

This is source-candidate evidence only. The next gate is root/cap readiness followed by the central acceptance/reload/undo/retry/legacy-zero qualification against the current b1/S2/d874/Runtime2c4/public12 integration, including real Runtime verified-media reads and the browser/socket path. No full suite, browser, live socket, project TypeScript, build, or install was run here.
