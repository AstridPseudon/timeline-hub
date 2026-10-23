# App A4 after-anchor mounted return — 1954

## Result

The assigned persistence test now proves the mounted prepared-media caller through the real App runtime boundary:

`useTimelineCommandsService.addClip({ preparedAsset, afterClipId })` → mounted `useTimelineSave` → local save session/outbox → `RuntimeDataProvider` → `AstridRuntimeClient` → generated `WorkspaceClient` transport.

The accepted case checks the exact guarded v2 request and serialized wire body, route, headers, and idempotency key. Its accepted envelope carries the canonical document, digest and identity pairs, authoritative command/step/merge metadata, and receipt with `receipt.result` equal to `data`; the mounted state adopts the returned canonical closure.

The refusal case returns the contract-shaped 409 with `details.current`, structured path/hint/suggested command, and no invented `details.head`. The mounted state revalidates against that returned canonical head, removes the optimistic prepared duplicate, retains the rejected durable intent, and exposes the conflict message.

## Evidence

- Targeted Vitest: 3 files / 29 tests passed (`useTimelineCommandsService.persistence.test.tsx`, `media.test.ts`, `parentAfterAnchorCapture.test.ts`).
- App, Node, and root TypeScript checks passed under `/home/user/work/.app-tsc.lock`.
- Scoped ESLint passed with zero warnings; `git diff --check` passed.

No full, browser, live service, P1/P2/P3, or benchmark suite was run. Keep this branch HOLD until P1GO and the broader A4 coverage gate.
