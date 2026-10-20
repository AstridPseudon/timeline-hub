# App automatic-placement real-proxy source review

## Verdict

**REJECT — tree `13c0934b46277524c4b6947f1803947f0184f0af` is not a runnable REAL closed loop.**

The transport and worker portions are source-valid, but production never invokes the durable placement requester after task admission. The browser gate's later managed-output, verified-media, native-capture, commit, recovery, and Undo assertions therefore cannot be satisfied by this source tree.

## Reviewed trees and required pair

- App gate tree: `13c0934b46277524c4b6947f1803947f0184f0af` (`13c0934b4`, `test(video-editor): add real automatic placement proxy gate`).
- Agent/provider reference: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`.
- Runtime/server reference: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- The App integration worktree is currently a separate `tl/integration` snapshot (`41fff23...`), so the gate tree must be composed onto the final integration tree before central launch. The central launcher must also verify that `ASTRID_CHECKOUT` and `ASTRID_RUNTIME_CHECKOUT` resolve to the required Agent and Runtime references.

## Decisive source blocker

`src/tools/video-editor/commands/placementRequester.ts:131-305` defines the durable requester. Its `request`, `resume`, and `recover` paths eventually call `advance`, which performs task discovery, managed-output discovery, verified media lookup, native capture, and commit.

However, production does not instantiate or call it:

- `src/tools/video-editor/commands/commitSession.ts:419-447` only lists `placementContinuations`, displays recovery UI, creates the initial `createEditorImagePlacement(...)` reservation, and on recovery calls `claim(ownerId); await pump();`. It has no import or call to `createPlacementRequester`, `requester.resume`, or `requester.recover`.
- `src/tools/video-editor/commands/nativePlacementCapture.ts:65-72` defines the native capture wrapper, but no production caller wires it into a requester.
- A non-test source search for `createPlacementRequester`, `createNativePlacementCapture`, `readNativePlacementCapture`, and placement-requester invocation finds definitions and supporting storage/host code only; no production completion/reconnect call site exists.
- `src/tools/video-editor/commands/editorImagePlacement.ts:18-121` admits the initial task and records its locator when available. It does not discover a settled task's outputs or commit a generated placement.

Consequently, the real initial task admission may occur, but after settlement the source has no production path to issue `getTask`, `listManagedOutputs`, project media lookup, native capture, or the timeline commit. The gate's assertions for those requests and the subsequent recovery/Undo behavior are unreachable in a genuine production run. A helper existing in the tree is not coverage when no production path invokes it.

## Source-valid portions

- `src/tools/video-editor/contexts/VideoEditorProvider.tsx:911-928,1159` binds an operation host to the editor identity and retires it on lifecycle changes. `src/integrations/runtime/clientLocalAdapter.ts:126-139` adapts the host to the local task client.
- `src/integrations/runtime/operationHost.ts:72-142` binds same-origin operation state through `/runtime-config/v1/operation`, sends `{}` with `Content-Type: application/json`, accepts the 201 handle/identity response, and supports predecessor replacement. `:176-285` enforces operation scope, `X-Astrid-Operation-Handle`, normal task admission, and commit fencing.
- `config/vite/runtimeProxy.ts:46-95` and `scripts/runtime-discovery-proxy.mjs:119-145,324-385` admit the dynamically selected Vite origin, require the expected loopback Host, enforce same-origin fetch metadata where present, accept only `/runtime-config/v1/operation` and its `/runtime/v1/...` descendants, and strip browser-supplied auth/cookie/handle headers. The browser uses the exact `/v1/tasks` admission path with `Accept`, `Content-Type`, and `Idempotency-Key`; it does not inject a bearer or fake Runtime endpoint.
- `src/integrations/runtime/generated.ts` provides the real task, managed-output, task-media-selection, verified-media, retry, and cancellation methods. The managed output schema includes task/run/project/attempt, output port, group/variant, object, digest, media type, ordinal, role, durability, lifecycle, and version.
- `placementRequester.ts:159-186` contains strict task/attempt/output/project/object/durability/lifecycle checks. `nativePlacementCapture.ts:41-61` checks the exact five-key media pin, task locator, original scope/head/document, and calls verified media selection. These guards are present but not reachable from production.
- The gate's temporary executor pack in `tests/e2e/local/auto-real-proxy.spec.ts:97-124` uses the frozen Agent `GenericPackHost`, declares `generated_images` as a file image output with `image/png`, writes a real PNG and output manifest, discovers/registers deliberately, and runs once. The frozen Agent reference exposes the matching `RuntimeProtocolClient`, `GenericPackHost.discover`, `register`, and `run(once=True)` APIs. Runtime reference routes cover task admission, task reads, managed outputs, and verified media. This is source-valid pending central pair validation.

## Assertions and lifecycle review

The gate source does assert raw occurrence/lane/empty-anchor admission, owner and read-closure data, exact task body and idempotency key, managed output/media properties, lost-ACK retry with the same body/key and receipt, reload, Undo, absence of the generated image, operation paths, and no legacy `/api/runtime` POST. The normal task admission/receipt/cancellation APIs remain in use; no fake host or injected Runtime command was found.

The Vite restart and Runtime restart binding replacement is represented by the operation host/proxy lifecycle source and the test harness, including predecessor retirement and same-origin rebinding. But the missing requester invocation means the asserted completion/reconnect closure and zero-legacy traffic cannot be established from this tree. No browser, build, socket, full suite, or TypeScript run was performed, as required for this source-only review.

## Pure controls run

All requested proportionate controls passed:

```text
node --check scripts/runtime-discovery-proxy.mjs                         PASS
node --test --test-name-pattern='^pure:' scripts/runtime-discovery-proxy-operation.test.mjs  PASS (1 test)
node_modules/.bin/eslint --no-cache playwright.auto-real-proxy.config.ts tests/e2e/local/auto-real-proxy.spec.ts  PASS
git diff --check                                                        PASS
```

These controls establish syntax, the pure discovery-proxy operation cases, lint, and whitespace only. They do not overcome the missing production caller.

## Central launch prerequisites and next steps

1. Wire a production `createPlacementRequester` lifecycle into the editor command session using the bound operation host/client and the existing native capture callback. It must invoke `request`/`resume` after initial admission and invoke `recover`/`resume` on reconnect/recovery, while sharing the normal owner/outbox/receipt lifecycle and retiring with the operation host.
2. Compose this App gate tree onto the final App `tl/integration` snapshot; verify the Agent and Runtime worktrees resolve to the exact references above.
3. After the source fix, run the central browser acceptance once with the design launcher environment:

```text
TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
ASTRID_CHECKOUT=/home/user/work/agent \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
npm exec -- playwright test --config playwright.auto-real-proxy.config.ts
```

The current source should not be approved for that browser run as a qualification result; the browser run remains required after the production caller is wired and the final integration snapshot is composed.

