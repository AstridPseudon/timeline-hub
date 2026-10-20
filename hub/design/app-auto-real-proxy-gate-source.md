# App M2 automatic placement — real operation-proxy gate source

Status: source-ready for central browser qualification. No automatic-placement retirement or live pass is claimed here.

## Exact source/tree

- App worktree: `/home/user/work/wt/app-m2-auto-real-proxy-gate-source`
- Added launcher: `playwright.auto-real-proxy.config.ts`
- Added bounded representative source: `tests/e2e/local/auto-real-proxy.spec.ts` (under 500 lines)
- Production binding is unchanged from the approved candidate (`VideoEditorProvider.tsx`, `VideoEditorRuntimeContext.tsx`, `useTimelineSave.ts`).
- Source pair required by the independent review: Agent/provider `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`; Runtime/server `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.

## Real handler and start path

The source starts the real processes used by `dev:local`, with no fake host or App command injection:

1. `node scripts/runtime-discovery-proxy.mjs` with `ASTRID_WORKSPACE_DISCOVERY`, `ASTRID_RUNTIME_PROXY_PORT`, and `ASTRID_RUNTIME_OPERATION_ORIGIN`. This is the actual `createRuntimeProxyServer()` handler; it acquires `/runtime-config/v1/operation` and forwards bound data under `/runtime-config/v1/operation/runtime/v1/`.
2. `node_modules/vite/bin/vite.js --config config/vite/vite.config.ts --host 127.0.0.1 --port <fixed> --strictPort`, with the actual Vite operation proxy, admission plugin, same-origin composer, product credential file, and discovery identity.
3. A temporary executor pack is written only beneath `DirectHarness.tmp`. It registers `generation.generate_image` through the frozen Agent `GenericPackHost`, then writes a real immutable PNG and output manifest through the Runtime task machinery. It is not an App transport and does not replace the Runtime handler.

The central launcher is:

```sh
TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
ASTRID_CHECKOUT=/home/user/work/agent \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
npm exec -- playwright test --config playwright.auto-real-proxy.config.ts
```

The central service should run that command from the final App integration snapshot, after verifying those integration worktrees resolve the two declared heads. The source does not run the browser or central service itself.

## Bounded journey covered

The single case opens the real seeded occurrence-image editor path, observes the initial unchecked approval, checks it explicitly, and supplies the raw `occurrence:<id>`, raw lane, and explicit empty raw anchor. Before allowing `POST /v1/tasks` through, it reads the real IndexedDB outbox and asserts the original owner, anchor, saved canonical basis/read closure, and exact task body/key reservation.

It then performs the real task admission and managed-output discovery, restarts Runtime and Vite on the same browser origin, reconnects, and runs the real worker. The first placement commit is allowed to reach Runtime but its browser ACK is aborted. The source checks canonical occurrence-image acceptance directly, restarts/reconnects again, recovers the owner through the visible recovery control, and asserts the exact commit body, idempotency key, and receipt on retry. It reloads, checks readback again, performs toolbar Undo, and verifies the generated occurrence image is absent while the seeded occurrence remains.

Captured browser traffic must include the operation path for task admission, task completion, managed outputs, verified media selection, and timeline commit. The source asserts no automatic-placement `POST` reaches `/api/runtime`; anonymous unchecked intent is never submitted or confirmed. Hosted/remote negotiation is not used.

## Source controls run here

```text
node_modules/.bin/eslint --no-cache playwright.auto-real-proxy.config.ts tests/e2e/local/auto-real-proxy.spec.ts
PASS

node --check scripts/runtime-discovery-proxy.mjs
PASS

node --test --test-name-pattern='^pure:' scripts/runtime-discovery-proxy-operation.test.mjs
PASS: 1 test file, 0 failures (pure launcher/discovery lane)

git diff --check
PASS
```

No browser, build, localhost/socket, TypeScript, install, full suite, or central execution was run under the worker restrictions. The next step is the one centrally registered browser suite using the matched Agent/Runtime pair above; its result must decide activation.
