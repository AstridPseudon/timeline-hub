## Report — app-P1-split-whole-path-1600

Cause proven: App’s full-v2 admission gate rejects the adopted Runtime schema.

- D66 Runtime/Agent schema: `867f…`
- App generated metadata: `867f…`
- `supportsFullV2Commit()` only admits `35c2…` and `4118…`
- `localSaveSession.ts:160–162` therefore changes the session `dirty → blocked` before `box.dispatch`; no commit POST is attempted.
- Split reached capture and persistence: `schedule → capture-called → capture-resolved → dirty → blocked`.
- The observer’s `traffic.posts=0` means zero matching commit-route POSTs, not zero unrelated POSTs. Source proves zero commit POST at the save boundary.
- Readiness, seed, identity, and history passed. The retained 503/outbox-read diagnostics are secondary environment noise.

Historical 18,792 passed with generated schema `35c2…`. U4p-D62 changed `generated-contract-metadata.ts` to `867f…` without updating `contract-metadata.ts`.

Validation:

- Focused contract test: 8 passed, 1 failed as expected — actual D39 expected full-v2 support but returned false.
- `git diff --check`: passed.
- Retained P1 test hashes match before/after manifest hashes.
- No source, test, config, generated, pin, browser, full-suite, or new collection changes.

Smallest Sol repair: update `src/integrations/runtime/contract-metadata.ts` to admit the qualified `867f…` digest; generated metadata already matches Runtime/Agent.

Commit message written and `DONE` marker created.