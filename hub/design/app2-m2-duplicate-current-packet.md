# App2 M2 duplicate — current-root flat packet

Base: `590c19795111fd1891bbd50a5f8d48bef3505a26` (`tl/integration`, current root at refresh).

Patches:

- Shared-port proposal: `app2-m2-duplicate-current-shared-port.patch`, SHA-256 `23a982b5c9299835db530615482a7a288588cc605b86b441005607c5ed1acfee`; exactly four shared files: `commitSession.ts`, `useTimelineCommandSession.ts`, `useTimelineState.ts`, `useTimelineState.types.ts`. App owner applies this through the shared ownership queue.
- Row-local consumer/prerequisites: `app2-m2-duplicate-current-row-local.patch`, SHA-256 `cc11d351cf1867bfea052e172898aa88127843041a03f3c070453383dd1912f1`; seven files: the unchanged approved helper five from `f34054c624f78c4f2f3b73551733f9151fc1b930`, plus `AstridTimelineEditor.tsx` and `AstridTimelineEditor.document-shots.test.tsx`. This worker tree contains only those seven files.
- Reviewed source: `5bb0a9f6383d0598608263644b51af6c69fe325d`; helper prerequisite: `f34054c624f78c4f2f3b73551733f9151fc1b930`.

Exact shared TypeScript port:

```ts
export interface OccurrenceDuplicateCapturePort {
  capture(input: { ownerRef: string; args: OccurrenceDuplicateArgs; current: TimelineData }): JsonObject;
  finish(basis: JsonObject): { command: EditCommand };
  submit(input: { command: EditCommand }): void;
}
```

The row consumer uses `captureOccurrenceDuplicateEdit(port, current, ownerRef, args)` followed by `submitOccurrenceDuplicateEdit(captured)`. The session captures from the raw authored bundle, finishes from the immutable basis, validates generation/bundle identity, and enqueues one outbox intent. No direct Runtime POST, new store, or public generic submit port is introduced.

Gates:

- `git apply --check app2-m2-duplicate-current-shared-port.patch`: passed against current root.
- Row-local patch apply check: passed against current root; approved helper source is unchanged from `f340`.
- Private candidate (current root + both proposals): focused 8-file Vitest lane passed, **188 tests**.
- Private candidate strict TypeScript: `npm run typecheck:strict-probe` passed.
- Private candidate targeted ESLint on all touched/helper/shared files: passed with `--max-warnings 0`.
- No browser, full, localhost, socket, or live Runtime-door suite was run, per task scope. The direct duplicate commit/reload/undo gate remains for App integration.
