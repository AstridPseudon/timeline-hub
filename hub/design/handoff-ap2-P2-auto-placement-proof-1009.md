# Handoff: P2 automatic-placement proof

Changed only `tests/e2e/local/auto-real-proxy.spec.ts` on the reviewed App base `1117c15f7e37a087a1175ea0e923958ce8a4132d`.

The existing real operation-proxy generator-placement journey is now a strict full-v2 proof source: it preserves reconnect/lost-ACK/exact retry/reload/guarded undo and adds request/receipt/history, Runtime `/commits`, canonical intended-delta/raw preservation, reload restoration, and inverse-record assertions. The existing exact inverse body assertion and zero legacy traffic assertion remain unchanged.

Static qualification passed: scoped ESLint, App TypeScript check, Playwright `--list` with `playwright.auto-real-proxy.config.ts` (1 selector), and `git diff --check`. No body or service execution was performed.

## Required owner follow-up

The current production seam is not full-v2: `src/tools/video-editor/commands/commitSession.ts:204-211` constructs automatic-placement commits without `label`, `steps`, `merge`, `reads`, `dry_run`, `rationale`, or `group_id`; `src/integrations/runtime/operationHost.ts:285-304` forwards that saved body unchanged. Undo is emitted through `timelineLocalSaveHandoff.ts:140-146` into the same session builder, while the preserved helper exact-matches the old inverse envelope. Repair the existing A2 placement/undo caller to emit the current contract before requesting central body execution. Do not weaken the new assertions or the original inverse matcher.

