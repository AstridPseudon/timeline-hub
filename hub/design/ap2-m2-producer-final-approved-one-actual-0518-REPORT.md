# AP2 M2 producer final approved one actual — 0518

## Result

The one authorized original producer actual was submitted exactly once from the exact frozen source worker. It failed before the hosted build, browser launch, or producer test body:

- Central result:
  \`ap2-m2-producer-frozen-delta-luna-resume-0453-ap2-m2-producer-literal-hash-first-cause-repair-0516-actual-1021052003-6793\`
- Exit: \`2\`
- Request packet:
  \`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-frozen-delta-luna-resume-0453-ap2-m2-producer-literal-hash-first-cause-repair-0516-actual-1021052003-6793/\`
- Actual test count: **0 collected; 0 executed**.
- First failing request packet/body path: the external gate rejected the literal \`run\` argument before invoking its child and printed:
  \`usage: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh preflight|list\`
- \`runner.log\` was empty; no build, browser, request body, assertion, reload, retry, undo, or zero-legacy evidence was produced.

The exact reviewed command submitted was:

\`\`\`text
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh | cut -d' ' -f1)" = 460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7 && test "$(sha256sum -- scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-frozen-keeper-review-0501/final-keeper-gate.sh run
\`\`\`

No retry or repair was performed. The failure exposes a settled-command defect: the approved external gate accepts only \`preflight|list\`, while the independently approved actual registration ends in \`run\`. The actual must not be rerun until the orchestrator resolves that command/gate inconsistency.

## Mandatory prerequisites and custody

- Hash-first repair report:
  \`ap2-m2-producer-literal-hash-first-cause-repair-0516-REPORT.md\`; its offline controls passed and its repaired source-only central preflight passed once:
  \`ap2-m2-producer-literal-hash-first-cause-repair-0516-ap2-m2-producer-literal-hash-first-cause-repair-0516-preflight-1021051918-19123\`, exit \`0\`, \`public13 preflight PASS checks=10\`.
- Independent literal-command review:
  \`ap2-m2-producer-final-literal-command-review-0516-REPORT.md\`, decision **APPROVE**, with the exact actual command above.
- Frozen source worker:
  \`/home/user/work/wt/ap2-m2-producer-frozen-delta-luna-resume-0453\`
- Frozen HEAD/tree:
  \`17d2518c341c47a2d8634047b400399886da3a2a\` /
  \`d63fe4f1e1f32a01acfc9d11cda6c29066fce162\`; clean before and after the request.
- External gate SHA-256:
  \`460d097995bd1d09938aeea54daeb6699030a20289eda78929132185961f26e7\`
- Committed wrapper SHA-256:
  \`87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0\`
- Required frozen-source \`KEEP\` marker was present.
- Final pre-submit checks passed: exact source/tree/clean state, both hashes, advisory browser lock free, and disk above 10 GiB (\`13,594,672 KiB\` free at postflight). The wrapper's original one-test collection guard remains unchanged; it was not reached by this actual.
- Pins retained: Agent \`8130a401bf44a518d5a40ae274d398b8c560be55\`, Runtime \`2c4ac180c2220bdad966bc01e95ad230e99ce26a\`, producer artifact \`sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56\`.
- Composition labels are intentionally distinct: private graph archive \`895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30\`; official Composition 13 archive \`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738\`, package \`0.0.13\`, 77 files.
- Historical result \`14352\` remains separate: it was the earlier external hash-binding actual that reached hosted build and failed Chromium launch with \`SIGTRAP\`; it is not this run's result and was not retried.

## Exact live callers (unchanged)

The frozen-source inspection found these App live callers for the producer/legacy timeline seams:

- \`src/integrations/runtime/dataProvider.ts\` — \`saveTimelineInOrder\` callers at the existing runtime persistence path.
- \`src/tools/travel-between-images/components/ShotTimelinePreview.tsx\` — \`ShotTimelineMediaProvider\` consumer.
- \`src/tools/travel-between-images/pages/LocalTimelineShotBrowser.tsx\` — \`ShotTimelineMediaProvider\` consumer.
- \`src/tools/travel-between-images/pages/ShotEditorView.tsx\` — \`ShotTimelineMediaProvider\` consumer.

The producer proof itself is test-only and unchanged:
\`tests/e2e/local/producer-ownership-current-pin.spec.ts\`,
\`tests/e2e/local/support/producer-ownership-current-pin.ts\`, and
\`playwright.producer-ownership-current-pin.config.ts\`.

No product, source, live-caller, wrapper, gate, pin, assertion, option, timeout, dependency, graph, or central-suite changes were made by this worker. No local build or test suite was run.

## Exact commands and results

\`\`\`text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-producer-literal-hash-first-cause-repair-0516-ap2-m2-producer-literal-hash-first-cause-repair-0516-preflight-1021051918-19123
# PASS exit 0; public13 preflight PASS checks=10

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-frozen-delta-luna-resume-0453 ap2-m2-producer-literal-hash-first-cause-repair-0516-actual --no-cache
# queued exactly once; result ID ...1021052003-6793

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-producer-frozen-delta-luna-resume-0453-ap2-m2-producer-literal-hash-first-cause-repair-0516-actual-1021052003-6793
# FAIL exit 2; external gate usage rejection; 0 tests collected
\`\`\`

Recommended next step: the orchestrator should reconcile the approved \`run\` actual registration with the immutable gate's accepted mode list, then perform a fresh prerequisite review. This worker must not submit another actual.

