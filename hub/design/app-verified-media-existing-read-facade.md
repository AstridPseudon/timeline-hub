# App verified-media existing read facade

Implemented the App-owned read facade required by App2's prepared-media
consumer.

Exact peer-facing signature:

```ts
getProjectVerifiedMedia(
  projectId: string,
  selection: MediaSelection,
): Promise<VerifiedMedia>
```

The implementation uses the generated 0.2.13 `getProjectVerifiedMedia` read
through the normal authenticated local Runtime client. It copies and freezes
the five original selection fields before any asynchronous work, rejects a
project mismatch before transport, rejects a Runtime response whose returned
selection is not the exact original pin, and lets the existing Runtime error
pass through unchanged. It does not refresh the selection, consult metadata,
write canonical timeline state, or add a DTO/endpoint/store.

Changed files:

- `src/integrations/runtime/client.ts`: exposes the existing generated read
  through the normal session wrapper.
- `src/integrations/runtime/dataProvider.ts`: adds the project-scoped facade.
- `src/integrations/runtime/dataProvider.test.ts`: exact route, no-write,
  scope, mutation, mismatch, and failure-propagation controls.

Evidence: the direct provider/client Vitest run passed 99 tests across 2 files;
focused ESLint and `git diff --check` passed. No full, browser, install,
TypeScript, or consumer-activation run was performed. App2 still owns the
prepared video `addClip`/session/outbox consumer and no writer cut is claimed.
