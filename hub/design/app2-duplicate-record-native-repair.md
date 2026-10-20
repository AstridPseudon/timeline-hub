# App2 duplicate raw-record repair

Base/current root: `hub/timeline/app/tl/app-m3-root-cold-current-source-attribution` / `05b6b488d1834650c459c5c565f2530d9bea20e9`
Source unit: `tl/ap2-m2-duplicate-capture-resume` / `a2e6bde1c823aee15601dfa5f11baea2dca3c3f5`
Agent comparison source: `68a51203310eb7b1bad343e50a42cf75c46c5321`

## Change

Ported the reviewed five-file occurrence-duplicate unit onto the current root. The occurrence create now derives the destination shot revision identity from the already-created destination payload/internal closure, then uses the existing stable root factories to rewrite only present top-level `stable_deep_link` and `output_identity` before recording `create_entity`. Missing root fields remain absent. Nested metadata/history/task/association/output-record/unknown values are copied unchanged. No consumer/session/door/editor writer changes were made.

The fixture's raw occurrence-create record and raw after-bundle expectation now contain destination roots. The focused regression checks the raw record and bundle directly, before the compiled-document projection.

## Evidence

- Targeted Vitest: 2 files, 41 tests passed.
- Focused raw-root regression: 1 passed, 33 skipped.
- Targeted ESLint for the four TypeScript files: passed with `--max-warnings 0`.
- Actual current-candidate TS output piped to read-only Agent `68a512…`: full record exact including writes, raw bundle exact, compiled projection exact, reload exact, guarded inverse exact, replay record/bundle exact, created IDs stable. Command SHA-256: `fb341fc784eb919796e5d65b6f2e8331239b3e8d77e6d61884c3ae5a4db91abb`.

## Limits

No full suite, browser, localhost/live socket, Runtime service, shared consumer patch, writer deletion, dependency/pin/generated-file change, or Git mutation was performed. App acceptance/reload/outbox/undo/redo/zero-legacy-traffic gates remain separate and open.

