# AP2 M2 ordinary owner-joined real gate

## Result

Added the reviewed Composition 0.0.13 ordinary central runner and its
Chromium launch smoke helper:

- scripts/testing/run-central-m2-ordinary.sh
- scripts/testing/chromium-launch-smoke.mjs

The runner creates one private per-run Agent/Runtime checkout and private
node-bin graph, uses EXIT cleanup, honors the incoming TMPDIR as the
temporary-root base, and runs only:

~~~
npm run test:e2e:three-products -- --grep "M2 ordinary extension batch"
~~~

It preserves exact Agent 8130a401bf44a518d5a40ae274d398b8c560be55 /
tree 236c3e57e0265c52b81ba8085de3193026176bff, Runtime
2c4ac180c2220bdad966bc01e95ad230e99ce26a / tree
7ab412cc4bcbe517efcfa806e092336390312e18, Composition 0.0.13 archive
895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
and tarball 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738,
Runtime lock producer/version/source guards, private graph/bin guards, and
authority-variable rejection.

The current App source was verified to contain both required ancestors:
7d42fcd3a (stale TimelineOps fix) and 8c0e1f799 (reviewed row-local
marker producer and five-member/10-command journey). No old 17655 checkout
or unjoined fixture was used. No product source, public pin, schema, API,
dependency, or shared install was changed.

## Targeted evidence

Passed:

~~~
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism --config config/testing/vitest.config.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/commands/ordinaryMoveMember.test.ts src/tools/video-editor/commands/ordinaryScalarMember.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts
# 6 files, 116 tests passed

node_modules/.bin/eslint src/tools/video-editor/dev/scene-phase-markers/extension.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/hooks/useTimelineOps.ts src/tools/video-editor/commands/genericPatchCapture.test.ts --ext ts,tsx --max-warnings 0 --no-cache
# passed

node --test scripts/testing/current013-integration.test.mjs
# 1 test passed

node_modules/.bin/playwright test tests/e2e/local/three-products.spec.ts --config playwright.three-products.config.ts --list
# 11 tests collected; ordinary journey present

git diff --check
sh -n scripts/testing/run-central-m2-ordinary.sh
node --check scripts/testing/chromium-launch-smoke.mjs
# passed
~~~

## Central gate

Submitted through the central service, not by invoking the runner directly:

~~~
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-owner-joined-real-gate e2e-m2-ordinary-integration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
~~~

Result: FAIL, request
ap2-m2-ordinary-owner-joined-real-gate-e2e-m2-ordinary-integration-1020211638-9958,
exit 1, one test selected. Exact central tree:
889677a90dc5649a5d6b8edf4ade95fd31f7e1c6.

The exact source preflight, hosted build, and Chromium smoke passed. The first
causal product failure was before the requested action:

~~~
tests/e2e/local/three-products.spec.ts:1153
expect(page.getByTestId('scene-markers-summary')).toContainText('2 markers')
Error: element(s) not found
~~~

The Scene Markers action was not clicked. Consequently there was no ordinary
capture, no command request, no ten-command assertion, and no retry/restart/
undo evidence. This is not a command refusal and provides no basis for a
guessed fix. The exact retained diagnostic is in
[central-first-failure.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-owner-joined-real-gate/central-first-failure.md);
the central service log and summary remain at its result directory.

## Decisions and next step

The runner was copied from the already reviewed ordinary Composition 0.0.13
runner because it was absent from the current composed App source. The only
runner adjustments were explicit App lock/artifact checks and using the
provided TMPDIR as the private browser-temp base. No product behavior was
altered.

The App owner/manager should inspect why the mounted Scene Markers panel is
absent on current source 8c0e1f799, apply a reviewed source fix if needed,
and submit the same named central ordinary suite once. Do not claim the
10-command, atomic ownership, retry, restart, or undo assertions from this
run.
