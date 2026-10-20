# Remaining App baseline: external proposal only

Product App is unchanged at `18becfbede00038830b97e63345445eeef54fa42` (tree `44d514b44c864ff9dbb3b99aba2b0a41891af83f`). This task produced a two-file patch outside the repository and a targeted virtual-source probe. **Owner review and an explicit ownership grant are needed before any application.** This is not repository acceptance or a green full-suite result. Full 21209 and its separate classifier are outside this task; no outcome is assumed.

- Proposal: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-remaining-baseline-proposal.patch`
- Probe sources/config/controls/logs: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-remaining-baseline-proposal/notes`
- Worker report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-remaining-baseline-proposal/notes/report.md`

## Exact failures and unchanged source

Read PLAN.md and the prior full 11559 classification plus its original failure log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-post-batch-current-full-source-full-post-opaque-standard-deps-m1-compat-integration-1020070734-11559/log.txt`

The three nodes reproduced here are:

1. `src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx > HoverScrubVideo with gateway media > asks for CORS when only the poster is a gateway URL, even before the video has a src`
2. `src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx > HoverScrubVideo with gateway media > asks for CORS for a gateway video, and leaves other media without the attribute`
3. `src/shared/contexts/__tests__/AuthContext.gated.test.tsx > AuthProvider on the hosted build > is loading while the permission is read, then anonymous and not loading when the Runtime is not reachable`

`git diff --exit-code 1be0efdde HEAD --` for the two proposal files, AuthContext.tsx, the two failing test files, and the bundled managed-media-policy.ts returned 0 with no differences. These files are unchanged since the source used for 11559. Historical classification remains historical; this task does not reclassify a baseline as zero failures or infer a full result from targeted tests. The SDK and ACP fixes are not changed or tested here.

## CORS cause and minimal proposal

HoverScrubVideo already calls `mediaCrossOrigin(displaySrc) ?? mediaCrossOrigin(posterUrl)`, and `getDisplayUrl` passes the absolute URLs through unchanged. The problem is the helper's sole predicate, `isManagedObjectUrl`. The bundled shared predicate accepts only `/api/(astrid|runtime)/v1/objects/:id` (relative or HTTP(S) loopback); the original failing inputs end in `/objects/p/content` and `/objects/v/content`. Neither matches, so React omits the `crossorigin` attribute. Both original failures receive null instead of anonymous.

The proposal changes only `src/shared/lib/media/mediaCrossOrigin.ts`: use the existing `isGatewayUrl(url) || isManagedObjectUrl(url)` in both mediaCrossOrigin and mediaFetchCredentials. The former supplies anonymous CORS; the latter omits browser credentials for the same configured-door URLs. All original URLs, poster behavior, canonical managed-route recognition, and standalone external/custom media credential choices are preserved. No shared Agent predicate, renderer, film data, Runtime endpoint or route authorization changes.

This distinction follows current Runtime code, read only at `/home/user/work/runtime/runtime_protocol/door.py`: `_admit` (approximately lines 512–541) checks exact hosted Origin before route admission, sends CORS headers for allowed-origin refusals, and refuses browser Authorization/Cookie on admitted routes. The product credential supplies authority; Origin only supplies browser admission. The proposal corrects the helper's misleading authority comment as well. Absolute URLs on the configured door origin need that transport behavior whether or not their path is currently authorized. Other ports/origins retain their current mode, except canonical managed objects already covered by the unchanged predicate. No URL is rewritten.

**URL limitation:** Runtime's current byte route is `GET,HEAD /v1/objects/:` (door.py line 178); `/objects/:id/content` is not an allowed route. The unchanged failing tests prove DOM CORS attributes and URL preservation, not successful media retrieval. The proposal intentionally does not promote `/content` into a canonical byte route or add a Runtime endpoint. It allows the door to send its normal CORS-readable route refusal. Any live-media URL migration is separate owner work if an actual producer is found to emit that shape. No live fetch was attempted here.

## Hosted auth cause and minimal proposal

AuthContext.tsx maps a hosted session from the real RuntimeConnectionProvider: only `isConnected` grants LOCAL_USER_ID/authentication, and `isBooting` supplies loading. Permission starts null. Granted permission starts the first probe; the stubbed fetch failure settles as a silent outcome with failedReadings=1. RuntimeConnectionProvider's final branch nevertheless returns `isBooting: true` until failedReadings reaches 2. The next normal reading is scheduled 3000ms later. The original test's normal waitFor finishes sooner and sees loading=true. This is boot-loading semantics, not a missing mock, an auth credential problem, or a reason to lengthen the test.

The proposal changes only the final connecting branch in `src/integrations/runtime/RuntimeConnectionProvider.tsx`: `isBooting: outcome === null`. That matches its existing interface comment: permission or **first** probe pending. Permission-null and initial pending probe still load. Prompt/denied remain anonymous, stop loading and send no fetch. After the first settled failure, loading ends anonymously while state stays connecting; the second reading still decides set_up/not_running. Poll intervals, timeouts, outcomes, permission checks, retries and connection requirements are unchanged.

AuthContext and AuthGate are not patched or mocked by the source probe. Authentication remains tied to connection success. Layout.tsx lines 58–64 wraps LayoutShell in RuntimeConnectionGate; that gate uses isConnected, so stopping boot loading cannot mount protected content. The supplemental tests exercise actual AuthProvider/AuthSession/RuntimeConnectionGate with only browser permission and fetch stubbed, including a deferred permission, a deferred first probe, first and second failures, prompt, and denied. Protected query owners never mount during these failures. Existing successful connection, recovery and same-origin/sessionless-auth tests also pass.

## Exact targeted evidence

Commands ran from `/home/user/work/wt/app-m4-remaining-baseline-proposal` on Node v22.22.0 / Vitest 4.1.5. A private overlay at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-remaining-baseline-proposal/deps/node_modules` links package entries to the **standard physical** `/tmp/app-m2-coherent-deps8/node_modules`; .vite, .vite-temp and .cache belong to the private overlay. Only this worker's ignored node_modules link was temporarily redirected to it and then restored. Shared dependency directories, caches, runtimes and venvs were not modified. No dependency install or substitution was performed.

The external config imports the repository's normal config and changes only cacheDir, inclusion of the external supplemental controls, and an opt-in two-source-file load plugin. With APPLY_PROPOSAL unset it loads every product source unchanged. With APPLY_PROPOSAL=1 it supplies the proposed file contents at their original module IDs (preserving relative imports). The actual AuthProvider and source dependencies remain in use; the provider source change itself is explicitly part of the proposal. This virtual-source result is not an applied repository patch or independent environment acceptance. The Agent browser imports use the repository's bundled vendor/astrid-browser source via normal config; ASTRID_CHECKOUT, ASTRID_RUNTIME_CHECKOUT, ASTRID_PUBLIC_CHECKOUT and VITEST_LANE were unset. No Agent provider was swapped to make tests green.

Red, original two failing files, exit **1**, **3 failed / 2 passed**, 3.77s (`notes/red.log`):

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
  node_modules/vitest/vitest.mjs run \
  --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-remaining-baseline-proposal/notes/probe.config.ts \
  --configLoader=runner --no-cache \
  src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx \
  src/shared/contexts/__tests__/AuthContext.gated.test.tsx --maxWorkers=1
```

Green, proposal probe plus necessary controls, exit **0**, **7 files / 76 passed**, 10.85s (`notes/green.log`). This includes **all 72 original tests in six files**, with every input/assertion preserved, plus four external supplemental tests:

```sh
APPLY_PROPOSAL=1 node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
  node_modules/vitest/vitest.mjs run \
  --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-remaining-baseline-proposal/notes/probe.config.ts \
  --configLoader=runner --no-cache \
  src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx \
  src/shared/components/__tests__/HoverScrubVideo.test.tsx \
  src/shared/lib/media/mediaCrossOrigin.test.ts \
  src/shared/contexts/__tests__/AuthContext.gated.test.tsx \
  src/shared/contexts/__tests__/AuthContext.test.tsx \
  src/integrations/runtime/RuntimeConnectionProvider.test.tsx \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-remaining-baseline-proposal/notes/supplemental.test.tsx --maxWorkers=1
```

The green log explicitly lists only the two proposed product source IDs. Controls prove CORS/credential omission for the original /content paths while the canonical managed-route predicate still refuses them; signed external media, another loopback port, blob/data/protocol-relative external URLs retain caller credentials and no forced CORS attribute. Original tests cover same-origin canonical objects, external sources/posters, hook behavior, connected auth, query invalidation, sessionless modes, permission transitions, recovery, and gate mounting.

Other checks, all exit **0**:

```sh
git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-remaining-baseline-proposal.patch
git diff --check
git status --porcelain=v1
```

The last command has empty output. Patch numstat: mediaCrossOrigin.ts +8/-6; RuntimeConnectionProvider.tsx +2/-1. No original test, assertion, URL or auth policy was rewritten. No markers, skips, suppressions, timeout edits, baseline allowlist edits or test weakening were added. No full suite, browser/e2e, build, tsc, install, real auth/network, localhost listener or live socket was run. No broader or live-media result is claimed.

## Ownership, decisions and next steps

Completed the authorized diagnosis/proposal; no blocker to this task. Product implementation is deliberately unapplied. The manager/orchestrator should obtain the relevant shared-media and hosted boot/auth owner review/grant for the **two exact paths** before any worker applies it, then run original targeted tests on the applied tree with the standard dependencies. Both paths are treated as outside this worker's owned timeline area per its brief; this report does not expand ownership. No permission request was sent to the human.

Recommended review decision: accept the transport-origin check independently of canonical URL validity, and accept first-outcome completion of boot loading while keeping connection gating. Keep Runtime's current URL/auth policy and all original tests unchanged. For permanent coverage, fold the four external controls from `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-remaining-baseline-proposal/notes/supplemental.test.tsx` into the owners' appropriate suites after grant; those controls are review material, not a silent repository test change. Full-suite disposition must come from the separate current full/classifier and subsequent authorized service qualification, never from this probe.
