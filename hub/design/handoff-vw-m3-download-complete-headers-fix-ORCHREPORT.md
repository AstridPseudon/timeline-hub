# Complete request-header observer fixed; no actual run / no grant

Read PLAN first. Assigned completed base: 952992d7875d03704a73711e10bc342eb9dd6c1a. Only tests/e2e/timeline/viewing-parity/download.ts and download.test.ts changed. The seven approved fda6b92e3 product paths are byte-identical. Strict assertDownloadTransfer is byte-identical, including actual page Origin equality, GET/fetch/HTTP200/noRange/noRedirect, exact location/project/object/size/digest/body and native same-page blob. Spec, four original cases, diagnostics, task/provenance, codecs, comparator, frame/body/audio checks, source/package/schema/client/provider/auth/pins unchanged. No existing expectation lost, skipped or weakened.

## Cause proof from the SAME retained requests

Ran own inspect-retained.py against /tmp/viewing-download-blob-diagnostic-EVPPA3 and predecessor central result 1020043712-5716. It reads retained data only and writes retained-safe-projection.json (no headers, tokens, location paths or task bodies dumped). Original archive/saved files preserved.

For EACH of the three failed exports it correlates the exact page/goto Origin, unique Download click, same-frame post-click project-location then exact output-object GETs, and native blob download event. Exactly those two requests have complete/raw Origin equal to the actual hosted page Origin, no Range, CORS fetch, HTTP200, no redirect. The location identity/size, object response bytes, succeeded task MP4 digest/size and saved final-export.mp4 bytes match exactly (1,109,353 bytes in each case). Central source pre/post passed with identical selected sources. Each original failure is download.ts line30: undefined observed Origin versus actual page Origin. The strict loop reaches LOCATION first; the old provisional OBJECT Origin was not asserted, and we do not claim it was independently observed missing.

Installed Playwright 1.60.0 implementation, node_modules/playwright-core/lib/coreBundle.js:

- 54756–54759: Request.headers returns _provisionalHeaders (unless route fallback overrides).
- 54761–54772: allHeaders awaits _actualHeaders -> channel.rawRequestHeaders.
- 50325–50326 and 13608–13616: channel serves the server request raw-header promise.
- 35323–35328: Chromium requestWillBeSentExtraInfo patches that response.request's raw headers.
- 24772–24774: HAR/trace recording awaits the SAME request.rawRequestHeaders promise.
- Frozen Runtime runtime_protocol/door.py:509–530 checks the single Origin against door.origin before routing and refuses hosted_origin_required/403 on mismatch. No door/auth changes.

This is direct contradictory observation of the same location request (old provisional observation undefined, raw trace has exact Origin), with the installed raw-header API path verified. HTTP200 alone was not taken as proof and no request was replayed or modified. Safe projection records local implementation and door hashes. Saved-byte evidence is retained-run evidence only, not proof that unexecuted downstream decode/parity assertions passed.

## Minimal fix and decisions

Await request.allHeaders() and response.body() together; synchronously append the read promise on response arrival so async completion cannot reorder location/object. Retain only Origin/Range and existing safe fields. Header/body failures remain rejection evidence for finish() and are caught provisionally to prevent interim unhandled rejection. No provisional fallback, synthetic/injected request Origin, tolerance, whitelist or auth waiver. Unit mocks reject any call to headers(); asynchronous complete headers supply the actual observed fields. New negatives reject absent/wrong complete Origin, Range, and complete-header failures on either read. Existing missing/repeated/reversed reads, body failures, status/auth/body/blob checks retained.

## Exact commands and results

All run in /home/user/work/wt/vw-m3-download-complete-headers-fix. Absolute managers/viewing/QUIET.md was absent before CPU checks (controller checks it itself too). Variables expand as follows:

```sh
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
OWN=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-download-complete-headers-fix
python "$OWN/inspect-retained.py"
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/download.test.ts
"$NODE" --import tsx tests/e2e/timeline/viewing-parity/diagnostics.test.ts
"$NODE" --import tsx --test tests/e2e/timeline/viewing-parity/authority.test.ts tests/e2e/timeline/viewing-parity/compare.test.ts tests/e2e/timeline/viewing-parity/admission.test.ts tests/e2e/timeline/viewing-parity/harness.test.ts tests/e2e/timeline/viewing-parity/bootstrap.test.ts
"$NODE" node_modules/eslint/bin/eslint.js tests/e2e/timeline/viewing-parity/download.ts tests/e2e/timeline/viewing-parity/download.test.ts --max-warnings 0
"$NODE" node_modules/typescript/bin/tsc --project tests/e2e/timeline/viewing-parity/tsconfig.json --noEmit
```

Retained evidence PASS; download 58/58 PASS (49 originals +9 new), diagnostics 141/141 PASS, five neighbor files PASS, lint PASS (all exit0). Typecheck exit2: only unchanged tests/e2e/local/support/harness.ts:630 TS2352 clips/never[] diagnostic; full output byte-identical to predecessor typecheck.log. No new changed-file error. Logs in own download-test.log, diagnostics-test.log, neighbors-test.log, lint.log, typecheck.log. No full requested. Neighbor bootstrap uses mocked child streams; no host was launched.

```sh
"$NODE" "$OWN/run-download-complete-headers-diagnostic.mjs" --freeze
ASTRID_CHECKOUT=/home/user/work/wt/vw-m3-host-agent-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/vw-m3-runtime-source-lease2 TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/composition ASTRID_REMOTION_PROJECT_DIR=/home/user/work/wt/vw-m1-ssr-snapshot/remotion ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell "$NODE" --import tsx "$OWN/run-download-complete-headers-diagnostic.mjs" --verify-sources
ASTRID_CHECKOUT=/home/user/work/wt/vw-m3-host-agent-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/vw-m3-runtime-source-lease2 TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/composition ASTRID_REMOTION_PROJECT_DIR=/home/user/work/wt/vw-m1-ssr-snapshot/remotion ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell "$NODE" node_modules/playwright/cli.js test --config playwright.viewing-parity.config.ts --list
"$NODE" --check "$OWN/run-download-complete-headers-diagnostic.mjs"
bash -n "$OWN/setup-download-complete-headers-diagnostic.sh"
git diff --check
```

All PASS exit0: content freeze/preflight, exact clean b70/9f9/f816/ff053 peers, all77 Composition members and six Remotion/Player hashes per consumer, exact installed8/browser/Node selections; four original tests collected (not executed); controller/setup syntax and diff whitespace pass. scope-check.json records exact seven approved product hashes, only two allowed path changes, strict assertion unchanged and identical baseline typecheck output. All temporary evidence/controllers/reports outside repo; no build output or untracked worktree files.

Prepared App content: 5950 files / SHA256 6a6304af9a73f37552dc12c40a0adf7e0cb2c79a86c698c5dab56daf39c7f07a. This is this worker's final bounded source, NOT a manager-approved combined codec/header candidate. README.md documents the new unique grant/one-shot and proposed manager-only suite registration/request. Controller requires manager review flags for BOTH header and result-preview codec fixes plus exact final frozen App fingerprint. Retains full source/package77/six guards, frozen DIAGNOSTIC b70/9f9/8, QUIET, actual flock, foreground sourceSnapshot identity and finally/postflight even after failure. Neither grant nor run marker exists. No suite registration/request/network/browser/socket/render/install/full/service performed.

## Remaining hold / next steps

No implementation block in assigned scope. Actual full four-case evidence is UNVERIFIED and MUST REMAIN UNGRANTED until separate vw-m3-result-preview-codec-triage and this observer fix are resolved/reviewed. Manager combines only reviewed changes, re-fingerprints the final source AFTER review and updates fixed controller identity if changed, repeats source preflight/collection, then alone may issue a fresh one-shot grant and central request. Do not reuse predecessor consumed grant or claim observer unit success closes nativeMediaError/ERR_ABORTED. No current merge/public10/11/continuous PCM/gate6/M3 qualification; frozen diagnostic only. DONE denotes completion of this bounded fix/preparation.
