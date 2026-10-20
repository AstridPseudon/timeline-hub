# Same-origin proxy real-Runtime proof source

Prepared on App `171a259acbeb3ced855ca8f72fed0943a2f5a5cb` (normal Runtime 0.2.13 pin, public Composition 0.0.12). Worker: `app-m2-proxy-real-runtime-proof-source`. **Source preparation complete; real-Runtime execution and activation remain held for the published matched Agent 0.2.13 consumer SHA.** No Agent substitute was selected.

Read PLAN, `runtime-app-proxy-operation-agreement.md`, `app-proxy-response-regression-final-review.md`, and `runtime-current-tuple.md` before editing. No settled decision was changed or contradicted by the source review.

## Approved port

Applied only the ten-path approved proxy/browser-host diff `7bb885b63883..ad05c5bd3554cc7b86c2ba3e7b8c0fb7a38e69ca`. Nine paths are byte-identical to the approved source. `config/vite/vite.config.ts` preserves the current root's alias/comment cleanup and adds exactly the approved operation route, admission plugin and imports. The shared acceptance decoder is the approved extraction, with provider caching unchanged.

The original `X-First` / `X-Second` Connection nomination and response credential-header negatives remain byte-identical, including Authorization, Proxy-Authorization, Cookie, Set-Cookie and operation-handle stripping. No passing behavior test was changed, skipped, weakened or replaced. No journal, automatic placement requester, framework, endpoint, wire DTO, browser bearer or activation was added. Runtime lock, generated files, package/lock files and three-products journey remain unchanged from the assigned root.

## One bounded integration case

`scripts/runtime-operation-host-real-runtime.test.mjs` uses the existing `DirectHarness.start`, `seedThreeProducts`, normal authoring-profile startup, `AstridCli.preflight`, `commitCaptured`, Runtime restart and source-identity helpers. It starts the existing harness's unused hosted fixture and door as part of that helper; it neither builds assets nor opens a browser or requests that hosted fixture. There is no new launcher, relay, Runtime replacement or synthetic accepted envelope.

The case creates a minimal Vite server with the **production** operation admission and proxy option helpers, through the real credential-owning operation proxy into the pinned Runtime. It loads the actual browser host, acceptance decoder, command session, gesture capture and outbox with Vite SSR. This exercises the operation route, rather than loading the entire product Vite config or rendering the App UI. Node native fetch dispatches immediately; the adapter supplies Origin/Fetch Metadata that Node does not enforce itself.

The assertions are prepared to cover:

- A native Agent-captured move establishes a real immutable basis, with children and opaque seed data. An App session captures a Unicode track-label edit over that basis.
- Discovery changes to another endpoint, credential and instance after negotiation. The already-owned operation still accepts under the original product publisher.
- Fault injection consumes the real 200 response only after scoped Runtime history confirms its publication, then throws before the browser host receives it. The outbox retains the original request bytes and key. This is an injected lost acknowledgement after durable acceptance, not a real packet-loss experiment.
- Actor, realm, project and timeline storage scopes remain separate; incorrect transmission scopes fail before Runtime dispatch. Retired browser callbacks refuse and a retired server handle returns 410.
- Runtime restarts with a new endpoint/instance. The old page cannot silently reconnect across that instance fence. A fresh Vite module lifetime models page relaunch and explicitly proves new health/handshake/realm negotiation. Recovery is explicit, never an automatic resend.
- Both real proxy-ingress POST buffers equal the original persisted UTF-8 request; both keys and complete Runtime acceptance envelopes/receipts match. History has one added publication, and the accepted label, prior move, children and opaque data survive.
- Node-simulated page traffic has no server credential; response headers omit credentials/private handles. Handles appear only in acquisition replies and operation headers, never URLs, request bodies or persisted records. There is no `/api/runtime` fallback. The existing synthetic actual-Vite negatives remain the direct observation of stripped upstream headers; the new Runtime case observes proxy ingress, not a new Runtime-side request recorder.

**Storage limit:** this uses `vendor/fake-indexeddb/index.js` (`0.0.0-local`) and an in-process exclusive-lock set. The same fake factory survives the modeled page relaunch. It does **not** establish native IndexedDB transactions, browser locks, browser reload, process-crash or disk durability. Real Runtime SQLite acceptance/restart is the proposed live evidence; none has yet run here.

**Narrow sender seam:** the current command session calls `send(parsedRequest, key)`, whereas the operation host accepts persisted `OutboxRequest` bytes. The test adapter retrieves the already-reserved request by key from the existing outbox, verifies its parsed value against the session callback, and passes the original bytes to the host. No production sender API was changed. Production requester wiring still needs to consume this exact-byte reservation under its reviewed ownership fences; this source does not activate it. The existing harness can traverse the host without a broad rewrite.

## Required immutable inputs and central command

The new pure helper `scripts/runtime-operation-proof-inputs.mjs` requires every input below, with no checkout/interpreter/cache defaults. It checks clean source identities, the App source tree, both normal consumer pins to the published Runtime SHA/artifact, installed public12/six-peer versions, dependency-root identity and an existing cache directory outside source/dependencies/venvs. Agent preflight additionally verifies the imported Python source and the real contract/realm/instance. Source guards run again at completion.

The orchestrator must retain the final matched **normal** Agent consumer source and choose a unique, immutable input JSON filename containing that SHA and the final App tree. Do not fill the Agent field with a moving integration checkout or frozen semantic producer. Do not reuse an input filename with changed contents: the central cache keys commands, not arbitrary external file contents. Get `appTree` from the harness-created final worker commit, or the exact composed source that is to run; do not use the base root's tree after adding this test.

```json
{
  "agentCheckout": "/absolute/retained-normal-Agent013-checkout",
  "agentHead": "PENDING_PUBLISHED_NORMAL_AGENT013_FULL_SHA",
  "agentPython": "/home/user/work/venv-agent/bin/python",
  "runtimeCheckout": "/home/user/work/wt/rt-m2-pin-2c4ac180",
  "runtimeHead": "2c4ac180c2220bdad966bc01e95ad230e99ce26a",
  "runtimePython": "/home/user/work/venv-runtime/bin/python",
  "appTree": "FINAL_CANDIDATE_OR_COMPOSED_TREE_FULL_SHA",
  "dependencyRoot": "/tmp/app-coherent-deps12/node_modules",
  "cacheRoot": "/absolute/worker-owned-existing-cache-directory"
}
```

After the pair is published, the orchestrator may register a bounded named service suite with **literal** input/cache choices in its service-owned command, for example:

```sh
env TIMELINE_PROXY_REAL_RUNTIME_RUN=1 \
  TIMELINE_PROXY_PROOF_INPUTS=/absolute/immutable-inputs-AGENT_SHA-APP_TREE.json \
  TSX_DISABLE_CACHE=1 \
  node --import tsx --test --test-concurrency=1 scripts/runtime-operation-host-real-runtime.test.mjs
```

Use that registered named suite through `request-test app-m2-proxy-real-runtime-proof-source <registered-suite>` and then `wait-test` on the returned ID. **No suite was registered or submitted here.** Caller environment is not forwarded by `request-test`; setting the above variables only around the request command is insufficient. The service snapshot must resolve its own node_modules to the declared read-only private12 root (the worker's own ignored link is already pointed there). All Vite caches for this case are temporary children of `cacheRoot`, removed on teardown; TSX cache is disabled. No install, project typecheck, build, full suite, socket or browser rerun is authorized by this source-only handoff. The old 363 synthetic-case lane was not rerun.

## Executed verification

All commands ran from `/home/user/work/wt/app-m2-proxy-real-runtime-proof-source`, with its own node_modules link pointing to the existing read-only `/tmp/app-coherent-deps12/node_modules`.

| Exact command | Result |
| --- | --- |
| `node scripts/runtime-operation-proof-inputs.test.mjs` | 1 pure test passed; verifies every missing input, wrong Runtime SHA, pending Agent SHA and relative dependency path refuse. |
| `node --test-name-pattern='^pure:' scripts/runtime-discovery-proxy-operation.test.mjs` | 7 pure cases passed; zero failures/skips. No socket cases selected. |
| `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/runtime/operationHost.test.ts` | 1 file / 59 cases passed; exit 0. Pure local bytes only. |
| `node --check scripts/runtime-operation-host-real-runtime.test.mjs` | Syntax passed; no execution of the real-Runtime case. |
| `node node_modules/eslint/bin/eslint.js scripts/runtime-operation-proof-inputs.mjs scripts/runtime-operation-proof-inputs.test.mjs scripts/runtime-operation-host-real-runtime.test.mjs` | Exit 0, no findings. |
| `git diff --check` | Clean. |

A Python byte comparison verified the nine identical approved paths and unchanged protected lock/generated/package/journey paths; the Vite diff was inspected separately. Early `node --test` invocations reported file-level passes without individual case counts, so the counts above use direct Node test execution. An attempted `--test-isolation=none` flag was unsupported by this Node version and provided no evidence; the direct supported command above supplied the seven pure-case results.

No socket/browser/build/full/install/typecheck or real-Runtime proof ran. No shared dependency, venv, Runtime, borrowed worktree or cache was modified. No build output or temporary source files remain. `DONE`, worker report and commit message finish the source task; `KEEP` retains it only for the imminent matched-pair qualification. Next step: provide the normal Agent013 SHA, freeze the exact service input file/command, then run this one bounded central case. Browser durability and requester activation remain separate gates.
