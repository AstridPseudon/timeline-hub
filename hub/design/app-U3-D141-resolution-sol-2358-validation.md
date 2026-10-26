# U3/D141 validation

Source-only conflict resolution is reviewable. No overall PASS. All paths outside the five edited conflict files match WIP4572; TourChatPanel.test.tsx is preserved unchanged and equals frozen upstream. Both required parents are already ancestors of HEAD. No Git mutation was invoked.

## Actual commands and results

- `git diff --check`: exit 0.
- `git merge-base --is-ancestor 5696769dfca056676cde1ab46d8bc94354b3a44a HEAD`: exit 0.
- `git merge-base --is-ancestor 7ca61bb3280beca21d98a854af266a382f7ce5df HEAD`: exit 0.
- Six-path conflict-marker scan: zero; JSON manifests parse.
- Historical generator: `NODE scripts/astrid-landing/refresh-vendor.mjs --astrid-repo /home/user/work/agent --commit ba55ac1e9e70156f03f7e31cc1b1ef040bb75b84 --destination /tmp/w-7d48efe1b0/vendor-ba55-reference`: exit 0, 160 files, historical provenance exactly reproducible. Fresh scratch destination only; no existing files deleted. Historical output copied unchanged, never hand-edited. It DOES NOT qualify the merged vendor.
- `NODE scripts/installer/update-manifest.mjs --runtime-checkout /home/user/work/runtime --agent-checkout /home/user/work/agent --plan`: exit 1, Runtime HEAD 6a011d58 does not equal lock ab1e4f61.
- `NODE scripts/build/verify-astrid-vendor-sources.mjs`: exit 1 after 65 pinned closure files; browser hash mismatch at am-footage/component.tsx. Static census finds two mismatches (also rendering/elements/catalog.ts).
- `NODE /tmp/w-7d48efe1b0/predicates.mjs`: exit 0, STATIC AST only: 15 files, 428 test declarations, 1495 assertion statements, zero worker test edits. All 1455 current and 1322 upstream test-file paths retained. Full details and preexisting assertion/title differences: predicate-map.json. Counts are not executed-test counts.

`NODE` above means /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node.

## Ready checks — NOT RUN

Fresh first admission had 4976873472 bytes; required >=5000000000 and no heavy, stop below 4000000000. No tests/lint/tsc launched. Normal targeted service requires >=5000000000 for a light suite, so no request was submitted below its floor. No admission/suite configuration was changed. Exact argv/cwd/admission values are in checks.json.

Use this exact toolchain and cwd; caches remain disabled and configLoader=runner prevents shared .vite-temp config output:

```sh
cd /home/user/work/wt/app-U3-D141-resolution-sol-2358
export PATH=/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin:$PATH
export NODE_OPTIONS=--max-old-space-size=4096
npm run test:app -- --no-cache --configLoader=runner --maxWorkers=1 src/shared/components/PaneControlTab.test.tsx src/shared/components/RuntimeConnection/RuntimeConnectionPanel.test.tsx src/shared/state/editorTourStore.test.ts src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/TourChatPanel.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.playback.test.tsx src/tools/video-editor/components/PreviewPanel/previewPlaybackPreferences.test.ts src/tools/video-editor/components/TimelineEditorShellCore.test.tsx src/tools/video-editor/hooks/useKeyboardShortcuts.test.tsx src/tools/video-editor/runtime/commandRegistry.test.ts src/tools/video-editor/tour/runner/cardPlacement.test.ts src/tools/video-editor/tour/runner/editorTourTargets.test.ts src/tools/video-editor/components/PreviewPanel/RemotionPreview.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.mailbox.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.audioFailure.test.tsx
node node_modules/eslint/bin/eslint.js src/tools/video-editor/components/AgentChat/TourChatPanel.tsx src/tools/video-editor/components/AgentChat/TourChatPanel.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx --report-unused-disable-directives --max-warnings 0
flock -w 600 /home/user/work/.app-tsc.lock node node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json --pretty false
flock -w 600 /home/user/work/.app-tsc.lock node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json --pretty false
node --import tsx --test --test-concurrency=1 --test-reporter=spec --test-reporter-destination=stdout --test-reporter=./scripts/quality/node-skip-guard-reporter.mjs --test-reporter-destination=stdout scripts/installer/manifest.test.mjs scripts/installer/update-manifest.test.mjs
```

Recheck admission before every command. Those are planned commands, not successful evidence. The two installer node files use normal package:test:node reporter/import conventions. No full suite, browser, live-socket journey, build, ZIP, or child was run.

## Production v2 caller trace (static, unchanged from WIP)

Mounted VideoEditorProvider/useTimelineState -> useTimelineSave.ts:319 createLocalSaveSession -> localSaveSession.ts:168 commands and steps -> commitOutbox durable dispatch -> localSaveSession.ts:192 exact JSON request/key -> RuntimeDataProvider.commitTimeline (dataProvider.ts:751) -> generated Runtime client generated.ts:202 POST /v1/projects/{project}/timelines/{timeline}/commit, Idempotency-Key header.

LocalSaveSession emits api_version/project_id/timeline_id/base_revision_id/base_publication_id/commands{schema_version,op,version,select,args,created}/source; label/dry_run and optional rationale/group_id; full-v2 metadata adds steps{id,label,intent,tags,command_ordinals,patch,optional reads}, merge fields|atomic and optional reads. Only base pair advances, persisted operands/reads/ids remain.

Generated timeline-commit-types.ts:76 retains full C0 v2 request. Lines 88-101 retain normalized commands (wire `commands`), id_map, canonical document/digest, base/previous/accepted/rebased_onto, merge_mode, durable receipt/records/bindings/reads/dependencies/derived writes/steps/history/undo_steps. Client accepts historical accepted/rebased/merged and validates preview would_status with null receipt. dataProvider rejects preview as a persisted save, validates receipt/closure and preserves full response; failure code/path/hint/suggested_command/current head remain structured. localSaveSession classifies rejection versus retry and retains rejected outbox chain while rolling the visible preview back. No transport/response/old-save or historical-outcome source was modified. This trace establishes source custody, not end-to-end runtime qualification.
