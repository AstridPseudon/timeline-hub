`realpath node_modules` → `/home/user/work/app/node_modules`

Targeted command:

`TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-queued-seek-existing-callback-producer-0935 ./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/components/PreviewPanel/RemotionPreview.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.mailbox.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.audioFailure.test.tsx`

Result: **47 passed**.

`./node_modules/.bin/eslint src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.mailbox.test.tsx --report-unused-disable-directives --max-warnings 0` → **passed**

`git diff --check` → **passed**
