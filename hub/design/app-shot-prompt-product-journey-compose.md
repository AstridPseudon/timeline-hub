# App M2 native prompt producer and real journey composition

Status: source composed; focused checks passed; central browser qualification is
prepared but not run.

## Source

The producer was already committed at App `baffad17c6648849b81c12c0ab67e2c4f111a270`
(tree `399781d07f6a88a14ab7b687e217abbfdf084c7d`). The independent journey
source is the committed test-only change `717892fb418a42eaf131d97d0b5be67124146008`
on the same parent (`b66a94006f31e8832870a1d4b8db1a2a0648ab24`).

I applied only its new spec hunk:

`tests/e2e/local/shot-settings-prompt-command.spec.ts`

The composed working-tree spec is 305 lines with SHA-256
`3fa7af87d611b514b8ee5d30306cfa6fb6a332a1675a9190a0634a25bb489672`.
No support fixture, default seed geometry, old whole file, or product rewrite
from the test branch was copied. The producer's existing producer/name,
opaque-root, and dirty-draft guards remain unchanged. The whole settings row
remains open.

The harness will create the final App commit after this worker exits. Therefore
the final App commit SHA and tree are intentionally not guessed here. The
central request must snapshot this exact working tree, record its resulting
full App SHA/tree, and use those values in the wrapper key. Using
`baffad17c...` or its committed tree would omit the new spec and is stale.

## Focused evidence

Passed:

```text
VITEST_CACHE_DIR=/tmp/tl-app-m2-shot-prompt-vitest-cache node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/shotSetSession.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/travel-between-images/providers/VideoTravelSettingsProvider.test.tsx
4 files, 107 tests passed

node_modules/.bin/eslint src/tools/travel-between-images/hooks/settings/useVideoTravelSettingsHandlers.ts src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/travel-between-images/pages/ShotEditorView.tsx src/tools/travel-between-images/providers/VideoTravelSettingsProvider.test.tsx src/tools/travel-between-images/providers/VideoTravelSettingsProvider.tsx src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/shotSetGesture.ts src/tools/video-editor/commands/shotSetSession.test.ts tests/e2e/local/shot-settings-prompt-command.spec.ts --ext ts,tsx --max-warnings 0
passed

git diff --check
passed

TMPDIR=/tmp/tl-app-m2-shot-prompt-discovery3 PLAYWRIGHT_OUTPUT_DIR=/tmp/tl-app-m2-shot-prompt-discovery3-output node_modules/.bin/playwright test --config playwright.shot-prompt.discovery.config.ts --list
1 test in 1 file; no browser launched
```

The temporary discovery config was removed after collection. An initial
repository-config discovery attempt failed before collection because its
isolated-port allocator could not find a port; the direct private config then
collected the one case successfully. No browser, localhost journey, full
suite, TypeScript check, build, install, or shared dependency/cache write was
run.

## Central single-case handoff

Register a new named `e2e-integration` case after the harness has supplied the
final App SHA/tree. It must run only
`tests/e2e/local/shot-settings-prompt-command.spec.ts`, with a private config
that spreads the existing `playwright.direct.config.ts` and sets
`testMatch: 'shot-settings-prompt-command.spec.ts'`. Do not reuse the
shot-name case, the moving integration worktree, or the old current013
three-products wrapper as the qualification identity.

Frozen paired inputs:

- Agent commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Runtime client `0.2.13`, schema
  `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`,
  producer manifest
  `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`,
  exactly 75 artifacts.
- Composition public13 archive
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  exactly 77 regular members.
- Public-source guard
  `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`;
  setup guard
  `88888d44ddd375caacb7b45b74001b70428bf4404b76fe11c84a83f8b05a6cfa`;
  Composition resolver guard
  `f49918bcfc3862f2ebad37d74ad0ae80a5535491949b2bfdbc8e4e4f19081881`.
- Chromium 141 binary SHA-256
  `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`.

The wrapper must require full 40-character App/Agent/Runtime identities and
verify, both before and after the one case:

- exact App snapshot SHA/tree and clean snapshot source;
- clean Agent/Runtime/producer checkouts at the pins above;
- Runtime lock, schema, 75-artifact manifest, and public13 77-member archive;
- public source and resolver/setup guards, peer versions, and Chromium identity;
- private public13 module overlay plus isolated Playwright/Vite/npm/XDG
  caches, with cache snapshots unchanged post-run;
- `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST` unset.

Use the existing short-TMP and browser paths:

```text
ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent8130-safety-source-keeper
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source
TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source
ASTRID_PYTHON=/home/user/work/venv-agent/bin/python
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python
TIMELINE_BUNDLE_AGENT_HEAD=8130a401bf44a518d5a40ae274d398b8c560be55
TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a
PRIVATE13_NODE_MODULES=/tmp/app-public13-pcm-complete-source-tsc-leaf13.01Xcjn/node_modules
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
```

The central key must include the final App SHA/tree, both frozen pair SHAs,
public13 archive SHA, Chromium SHA, and the new wrapper SHA. The wrapper must
not claim qualification until its preflight and postflight both pass.

## Assertions held constant

The real case keeps the existing production UI prompt input and asserts the
native `settings.prompt` producer, accepted raw settings/unknown preservation,
reload, Runtime undo, lost-acknowledgement restart retry with the exact request
body/key/receipt, relevant 409 dirty-draft retention, and zero legacy writes.
Those assertions were not changed.

