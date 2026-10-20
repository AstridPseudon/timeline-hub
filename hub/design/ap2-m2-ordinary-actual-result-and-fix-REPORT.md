# AP2 M2 ordinary actual result and fix

## Result

The central actual ordinary run failed before Playwright or the ordinary
journey started. This is an environment/test-harness failure, not an ordinary
producer failure. No App source change is justified or made.

- Run: `ap2-m2-ordinary-reviewed-readiness-actual-gate-e2e-m2-ordinary-public13-integration-1020184846-27058`
- Result: exit 1 in 61s; zero journey/test counts
- App source: `01230a5657853be85745566542af6546d254c28c`
- App tree: `c4965a7f5fe818a1cf2f6cb091ec4ff93fcde64a`
- Worktree: clean; no product delta

## First failure and classification

The exact first product command was the hosted App build. Rollup stopped at:

```text
src/tools/video-editor/compositions/playerEvaluation.ts (3:2):
"clipOpacity" is not exported by
"../../app/node_modules/@banodoco/timeline-composition/dist/evaluation.js"
```

The central public13 runner verifies a private locked graph, but its App
snapshot still resolves `node_modules` through the shared
`/home/user/work/app/node_modules`. That shared install is Composition `0.0.8`;
its `dist/evaluation.js` does not export `clipOpacity`. The checked-in App
`package.json` and `package-lock.json` require the public `0.0.13` artifact,
whose recorded tarball SHA-256 is
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` and whose
evaluation entry does export `clipOpacity`.

The locked graph is internally correct:

- private graph Composition version: `0.0.13`
- locked graph archive SHA-256: `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- public13 `dist/evaluation.js`: exports `clipOpacity` and `computeMediaTrim`

The prior public13 preflight `...-1020184006-23865` passed because it only
checked source and graph integrity with `PRELIGHT_ONLY=1`; it did not build the
App. The failure therefore cannot classify any ordinary behavior, including
batching, lost ACK, disjoint Agent edit, local suffix, restart/retry, guarded
undo, opaque preservation, or zero legacy traffic.

## Verification

Read-only checks performed:

```text
central run summary/log inspection: exit 1 before Playwright
checked-in package.json/package-lock.json: Composition 0.0.13
shared App node_modules: Composition 0.0.8 (mismatched)
locked private graph: Composition 0.0.13
git diff --check: passed
git status --short --branch: clean at 01230a565...
```

No targeted behavior test was rerun because this worker made no source
change. No local browser, socket, full suite, dependency install, pin change,
or shared-install mutation was performed.

## Next request

Fix the central runner attachment externally so its verified private graph is
the App snapshot's `node_modules` (or use the already-checked-in private-graph
wrapper `scripts/testing/run-central-m2-ordinary.sh`), then request exactly one
ordinary integration run for this unchanged source:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-ordinary-actual-result-and-fix e2e-m2-ordinary-integration) && \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Source identity for that request must remain App commit
`01230a5657853be85745566542af6546d254c28c`, tree
`c4965a7f5fe818a1cf2f6cb091ec4ff93fcde64a`. Do not rerun the broken
`e2e-m2-ordinary-public13-integration` runner until its private graph is
attached. Do not alter `playerEvaluation.ts` or weaken/mock the Composition
boundary to accommodate 0.0.8.
