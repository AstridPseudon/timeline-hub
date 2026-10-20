```sh
overlay="$(find /tmp -maxdepth 1 -type d -name 'vw-m3-app-pcm13-actual-consumer-unit-leaf13.*' | sort | tail -1)"
config="$(find /tmp -path '*/vw-m3-app-pcm13-vitest-config.*/vitest.config.ts' 2>/dev/null | sort | tail -1)"
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --config "$config" \
  src/tools/video-editor/compositions/AudioTrack.test.tsx \
  src/tools/video-editor/components/PreviewPanel/RemotionPreview.audioFailure.test.tsx \
  src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx \
  src/tools/video-editor/compositions/continuousPCM.contract.test.tsx \
  src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx
node_modules/.bin/eslint --no-cache --report-unused-disable-directives --max-warnings 0 \
  src/tools/video-editor/compositions/AudioTrack.tsx \
  src/tools/video-editor/compositions/AudioTrack.test.tsx \
  src/tools/video-editor/compositions/continuousPCM.contract.test.tsx \
  src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx \
  src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx \
  src/tools/video-editor/components/PreviewPanel/RemotionPreview.audioFailure.test.tsx
```
