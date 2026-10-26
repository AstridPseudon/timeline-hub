# Validation

- `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test tests/e2e/local/support/d141j-visibility.test.ts`: PASS, 3 tests.
- `npm exec -- eslint tests/e2e/local/support/d141j-visibility.ts tests/e2e/local/support/d141j-visibility.test.ts --max-warnings 0` under pinned Node20 PATH: PASS.
- Locked App typecheck, direct pinned TypeScript entrypoint: `flock -w 600 /home/user/work/.app-tsc.lock ... tsc --noEmit --incremental false -p tsconfig.app.json`: PASS, exit 0.
- Locked Node typecheck, direct pinned TypeScript entrypoint: `flock -w 600 /home/user/work/.app-tsc.lock ... tsc --noEmit --incremental false -p tsconfig.node.json`: PASS, exit 0.
- Existing source controls: pinned Node20 + Vitest 4.1.5, `--no-cache`, `src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.test.tsx`: PASS, 13/13.
- Positive checker control on retained synthetic source artifact: PASS, readCount 2, resultGroupCount 5.
- Negative checker control on retained stale-association artifact: expected FAIL, rejected `accepted-read-2` active association.
- `git diff --check`: PASS. Worktree changed only the two bounded support files.

The first collector-suite attempt used the pre-existing worker `tmpdir` regular-file sentinel as an artifact parent and failed with ENOTDIR; it was corrected by using this worker's evidence directory. No source failure was involved. No full, browser, socket, service, native-body, or test-service suite was run.
