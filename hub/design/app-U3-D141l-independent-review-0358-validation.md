# U3 D141l independent validation

## Source identity

- Candidate: `8f278b91accec5852e39bb84822e99124fccb81d`, tree `99d79cb47496c0ca682b0cd42aa911177761bb31`.
- Parents: `520d7e4fc12a03392afaed3f486aba34a2b5c319` and
  `d822d2f5d2bd05187b4ff5b6071c3e13945d4747`.
- Upstream tree: `2af40a015057779ceb4e4b37cad62e1469aa7e36`.
- Four conflict paths are exactly the brief's manifest, AgentChat source/test,
  and RemotionPreview source. Candidate has no conflict markers.
- Fifteen paths differ from the local parent; with the manifest conflict this
  is the full 16-path upstream accounting. No unrelated path drift was found.

## Commands and results

All commands ran against the pinned candidate with supported Node 20.

```text
PATH=/opt/node20/bin:$PATH npm run test:app -- --no-cache --maxWorkers=1 \
  src/shared/components/conversation/conversationExport.test.ts \
  src/tools/video-editor/components/AgentChat/AgentChat.test.tsx \
  src/tools/video-editor/components/AgentChat/TourChatPanel.test.tsx \
  src/tools/video-editor/components/PreviewPanel/RemotionPreview.playback.test.tsx \
  src/tools/video-editor/components/PreviewPanel/previewPlaybackPreferences.test.ts
exit 0; 5 files, 116 tests passed
```

```text
PATH=/opt/node20/bin:$PATH node node_modules/eslint/bin/eslint.js \
  src/shared/components/RuntimeConnection/EmptyEditorShell.tsx \
  src/shared/components/conversation/actionGroupLogs.ts \
  src/shared/components/conversation/conversationExport.test.ts \
  src/shared/components/conversation/conversationExport.ts \
  src/tools/video-editor/components/AgentChat/AgentChat.test.tsx \
  src/tools/video-editor/components/AgentChat/AgentChat.tsx \
  src/tools/video-editor/components/AgentChat/AgentChatComposer.tsx \
  src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx \
  src/tools/video-editor/components/PreviewPanel/PreviewTransport.tsx \
  src/tools/video-editor/components/PreviewPanel/RemotionPreview.playback.test.tsx \
  src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx \
  src/tools/video-editor/components/PreviewPanel/previewPlaybackPreferences.test.ts \
  src/tools/video-editor/components/PreviewPanel/previewPlaybackPreferences.ts \
  src/tools/video-editor/lib/themeTokens.ts \
  --report-unused-disable-directives --max-warnings 0
exit 0
```

```text
PATH=/opt/node20/bin:$PATH flock -w 600 /home/user/work/.app-tsc.lock \
  node node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json --pretty false
exit 0
PATH=/opt/node20/bin:$PATH flock -w 600 /home/user/work/.app-tsc.lock \
  node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json --pretty false
exit 0
```

```text
PATH=/opt/node20/bin:$PATH node scripts/installer/update-manifest.mjs \
  --runtime-checkout /home/user/work/wt/rt-pin-6a011d58 \
  --agent-checkout /home/user/work/wt/agt-pin-28e56cac --write
exit 0; qualified Agent/Runtime/schema values unchanged
PATH=/opt/node20/bin:$PATH node scripts/vendor-lock.mjs check runtime.lock.json \
  --producer /home/user/work/wt/rt-pin-6a011d58
exit 0
PATH=/opt/node20/bin:$PATH node --test scripts/installer/manifest.test.mjs \
  scripts/installer/update-manifest.test.mjs
exit 0; 4 tests passed
git diff --check
exit 0
```

The preview tests emit non-failing React `act(...)` warnings from the shared
Base UI Slider. No full, browser, journey, localhost, or live-socket suite was
run; targeted evidence is not full-suite proof.
