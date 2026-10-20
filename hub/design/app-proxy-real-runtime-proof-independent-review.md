# Same-origin proxy real-Runtime proof: independent review

**APPROVE the bounded prepared source at `5e0d5de2b6ecc40baa8be8f36491420e22bc602d`, tree `0127342f38c0e9f655ea2b25ccd34484555ed91c`. HOLD live qualification and requester activation.** No blocking source defect found. This is a source review plus narrow local checks, not a passing real-Runtime experiment.

Reviewed PLAN, `runtime-app-proxy-operation-agreement.md`, `app-proxy-response-regression-final-review.md`, `runtime-current-tuple.md`, and `app-proxy-real-runtime-proof-source.md`. No settled decision was changed. No product, test, configuration, lock, dependency, venv or source-worktree file was edited.

## Exact scope and approved-port comparison

Compared the candidate to normal-pin root `171a259acbeb3ced855ca8f72fed0943a2f5a5cb` and approved proxy source `ad05c5bd3554cc7b86c2ba3e7b8c0fb7a38e69ca` (approved diff starts at `7bb885b63883`). A Python `subprocess.check_output(['git', ...])` byte comparison found:

- Nine approved paths are byte-identical: `config/vite/runtimeProxy.ts`; `scripts/dev-local-workspace.mjs`; `scripts/runtime-discovery-proxy-operation.test.mjs`; `scripts/runtime-discovery-proxy.d.mts`; `scripts/runtime-discovery-proxy.mjs`; `scripts/runtime-operation-host-integration.test.mjs`; `src/integrations/runtime/dataProvider.ts`; `src/integrations/runtime/operationHost.test.ts`; `src/integrations/runtime/operationHost.ts`.
- The tenth approved path, `config/vite/vite.config.ts`, retains the current root's changes. Its entire diff from171a is the approved helper import, operation proxy route and admission plugin.
- Exactly three additional paths exist beyond that port: `scripts/runtime-operation-host-real-runtime.test.mjs`, `scripts/runtime-operation-proof-inputs.mjs`, `scripts/runtime-operation-proof-inputs.test.mjs`. All three were read in full.
- Runtime lock, package and package-lock, generated Runtime files, `tests/e2e/local/three-products.spec.ts`, and the existing `support/harness.ts` / `support/astrid.ts` are unchanged from171a. Original passing behavior tests were not rewritten, removed, skipped or weakened.

The original actual-Vite X-First/X-Second nomination and credential-response negatives remain byte-identical (`runtime-discovery-proxy-operation.test.mjs:529–539`). Their previously recorded363-case result is historical evidence; this review did not rerun it.

## Real acceptance and exact retry path

The new case imports the production admission/proxy helpers and credential-owning proxy (`real-runtime.test.mjs:8–10,82,124–142`), and Vite SSR loads the actual browser host, decoder, command session, outbox and track-label capture. It creates no synthetic acceptance envelope. The minimal Vite configuration exercises the production helpers without loading the whole product configuration or UI.

The existing harness starts the real Runtime module from the explicit checkout with Runtime-first PYTHONPATH. After normal seeding, `enableTimelineAuthoring(inputs.agentPython)` restarts it with `--authoring-profile astrid` (`harness.ts:443–474`). The later restart preserves this profile and interpreter. Static inspection of Runtime2c4's `daemon.py:225–235` confirms that profile loads the installed timeline semantic provider before admission. Agent preflight checks the imported Agent source, paired schema and real realm/actor/instance; the test also checks both source heads (`real-runtime.test.mjs:53–68`). No pending Agent SHA was guessed or replaced by the frozen semantic producer.

The basis is an actual Agent-native captured move, then an App session captures the Unicode label edit. The sender adapter reads the existing outbox reservation by key and passes its original serialized body into `operation.transmit`; it does not serialize a replacement body (`:156–163`). This traverses the production outbox reservation/claim/completion logic and command-session guards. It is a test adapter, not qualified production requester wiring; that separate activation remains held.

The fault adapter dispatches immediately using native fetch, consumes a real response, requires HTTP200, checks scoped history's publication against the response receipt, and only then throws the lost-ACK error (`:105–115`). The ensuing retry state, persisted pending request, publisher/key, accepted label, prior move, opaque config and child closures are asserted (`:178–191`). This is an injected response loss after observed acceptance, not a packet-loss or power-loss experiment.

After a real Runtime stop/start with a distinct instance, the old operation and old page reconnect refuse, the retired server handle returns410, and the saved request remains equal (`:206–217`). A fresh Vite SSR lifetime negotiates health, handshake and realm with the restarted Runtime (`:218–230`). Recovery must be explicitly chosen; the test asserts exactly one POST before recovery and exactly two afterwards. Both ingress buffers equal the saved UTF-8 bytes, both keys match, the persisted acceptance and both returned complete envelopes equal the original response, and history has exactly one additional publication (`:231–248`). These assertions occur on the ordinary awaited test path; there is no unconditional return, skip or swallowed top-level failure that can turn incomplete recovery into a pass.

## Authority and original fences

The browser host is unchanged from the approved source. It captures authenticated response bytes before generated mutable handshake assignment, validates types/scopes/schema/product actor, keeps a private copied identity, and exposes neither the client nor public handshake state as authority (`operationHost.ts:139–195,207–218`). Transmission preserves scope/body/path checks, the ordinary pre-write instance health fence, retirement checks around awaits, and the production acceptance decoder (`:226–251`). The narrow host tests cover mutable-handshake attacks and these lifetime fences.

The server registry captures endpoint, credential and Node dispatch primitive only at acquire; bound forwarding does not rediscover (`runtime-discovery-proxy.mjs:158–195`). The new test changes endpoint, credential and instance metadata after negotiation and still requires acceptance under the original publisher (`real-runtime.test.mjs:169–184`). Wrong actor/realm/project/timeline sends refuse before Runtime dispatch, and outbox lookup remains separately scoped (`:198–205`). No new public mutable authority or bypass around the original guards was introduced.

## Input and cache checks

`parseProofInputs` requires explicit absolute checkout/interpreter/dependency/cache paths, exact SHA-shaped Agent/App inputs, and exactly Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`. It returns the supplied interpreter paths unchanged: the venv's `bin/python` symlink is not resolved to a system interpreter.

`assertProofSources` checks clean App/Agent/Runtime sources and exact App HEAD tree / Agent HEAD / Runtime HEAD; both normal consumer lock source commits and artifact identities; installed public Composition0.0.12 and all six React/Remotion peer versions; dependency-root realpath identity; and an existing cache root outside the enumerated source/dependency/venv roots (`proof-inputs.mjs:23–47`). The live case calls it before launching the harness and again at the end (`real-runtime.test.mjs:27,265`). Vite caches are temporary children of the explicit cache root and cleaned by teardown. Choose a worker-owned cache root; the exclusion list is not a general filesystem ownership verifier.

The handoff correctly requires a new immutable input JSON filename containing the final Agent SHA and App tree, plus a literal service-owned command (including `TSX_DISABLE_CACHE=1` and the explicit execution flag). The helper does not make an external JSON file immutable or incorporate its bytes into the test-service cache key. Therefore freezing that filename/content and command is an operational prerequisite, not a passing parser assertion. No service suite was registered or submitted in this review.

## Assertion limits and claim boundaries

- The vendored fake IndexedDB factory and in-process lock set survive the modeled relaunch. The storage object also comes from the first page module lifetime. This exercises explicit session recovery and real Runtime restart/replay; it proves no native IndexedDB, browser locks, browser reload, disk durability or process-crash durability. The source and handoff state this limit correctly.
- The new `upstream` recorder observes proxy ingress, not Runtime-side HTTP bytes. Its X-First/X-Second absence checks have no corresponding injected headers in this new case. Meaningful planted header-stripping evidence remains the unchanged actual-Vite synthetic tests; do not assign those negatives to the new real-Runtime run alone.
- `globalThis.fetch` routes only relative URLs to `pageFetch` (`real-runtime.test.mjs:121`). The real workspace-config loader uses an absolute same-origin URL (`workspaceRuntimeConfig.ts:18–19`), so that request bypasses the `browser` recorder. The final secret/no-fallback scan consequently covers recorded operation traffic, not every page-origin request. Narrow that wording in any qualification report; if a complete page-traffic claim is needed, record same-origin absolute page requests too while leaving harness control traffic native. This does not block the bounded operation acceptance/retry proof.
- The one pure input test exercises `parseProofInputs` only. It does not execute `assertProofSources` or prove its real-environment rejection branches. No such execution is claimed here. A successful future live case must reach both source guards.

## Executed checks

Cwd: `/home/user/work/wt/app-m2-proxy-real-runtime-proof-independent-review`.

| Exact command | Result |
| --- | --- |
| `node scripts/runtime-operation-proof-inputs.test.mjs` | Exit0;1 test passed,0 failed/skipped/cancelled. |
| `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/runtime/operationHost.test.ts` | Exit0;1 file,59 tests passed. Local byte fixtures only. |
| `git diff --check` | Exit0; clean. |
| `git status --porcelain --untracked-files=all` | Empty at review start and completion. |

The worker's existing node_modules link resolves to read-only `/home/user/work/app/node_modules`; that root currently has Composition0.0.10 and the six expected peer versions. Thus the59-case result is narrow host evidence, not public12 live qualification. Read-only package inspection confirms `/tmp/app-coherent-deps12/node_modules` has public12 plus all six expected peers. No link or package was changed. No socket, real-Runtime, browser, build, full suite, tsc, install or broader test lane ran; no shared cache, dependency or venv write was requested.

## Corrections / next step

No code correction is required for bounded source approval. Keep live execution and requester activation held. Before the single central named run:

1. Publish and retain the exact normal Agent0.2.13 consumer SHA; do not substitute a moving checkout or frozen producer.
2. Retain an actual clean checkout at Runtime2c4 and use its explicit path. The handoff's `/home/user/work/wt/rt-m2-pin-2c4ac180` is absent in this review environment (`git -C ...` returned “No such file or directory”); its documented availability cannot currently be assumed. No alternate Runtime was selected.
3. Freeze the final App tree, immutable input JSON filename/content, worker-owned cache root, public12 dependency resolution and literal central-service command. Merely exporting env around `request-test` is insufficient.
4. Run only the bounded registered central case, inspect that it executed one case through the final source guard, and report the exact tuple/result. Keep browser durability and production requester ownership/wiring as separate gates. State the recorder limits above when reporting traffic evidence.

Review complete. No KEEP.
