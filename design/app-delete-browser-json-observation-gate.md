# Parent-delete browser JSON observation gate

Date: 2026-10-20

This is a bounded observation-helper fix and browser-gate record. It does not change stored outbox data, command production, delete semantics, or claim writer retirement.

## Exact source tuple

- App branch: `tl/app-m2-delete-browser-json-observation-gate`
- App HEAD SHA: `ccf537dd409259c4a88d0938675bf3e4deb32553`
- App source tree including the helper hunk and design note: `2e68d77eb8da9a19ecdda166f363d157897084f3`
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Runtime artifacts: 75
- Public Composition: 0.0.12, 77 files, `sha256:0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
- Chromium: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`
- Runner: `scripts/testing/current013-parent-delete.mjs`
- Central suite: `e2e-parent-delete-observation-final-tree2e68d77e-agent8130-runtime2c4-e2e-integration`
- Cache identity: `parent-delete-tree2e68d77eb8da9a19ecdda166f363d157897084f3-agent8130a401bf44a518d5a40ae274d398b8c560be55-runtime2c4ac180c2220bdad966bc01e95ad2303a09e7c0219144cc4b07467977f0f1a3-runnera71c71b3613f34d4b382a73959bf798271c7d646c380c011f1725a217e399bc7-helper82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901`

## First-loss proof and bounded fix

The prior central run on the corrected candidate reached the real parent-delete case and failed at the owner-intent equality assertion: the raw commit request contained own `__proto__` fields, while the direct `page.evaluate` return used by `commandOutboxes` omitted them. The missing values included `value.__proto__.raw`, `value.app.canonical.__proto__.literal`, and corresponding nested state values. The conflict case passed on that run.

The active worker’s final source traced the first loss to Playwright’s by-value serializer. The only ported hunk is `tests/e2e/local/support/app.ts`: the readonly IndexedDB records are filtered in the browser and returned as `JSON.stringify(...)`; the caller performs `JSON.parse(...)`. IndexedDB contents and production commands are unchanged. The existing delete assertions are the meaningful regression: they require raw `__proto__` preservation in the request, persisted owner intent, Runtime readback, reload/restart recovery, and inverse restore.

## Registered central results

Final test ID:

`app-m2-delete-browser-json-observation-gate-e2e-parent-delete-observation-final-tree2e68d77e-agent8130-runtime2c4-e2e-integration-1020160344-32098`

Result directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-delete-browser-json-observation-gate-e2e-parent-delete-observation-final-tree2e68d77e-agent8130-runtime2c4-e2e-integration-1020160344-32098/`

Result: exit 0; both unchanged cases passed. The central runner used two fresh Playwright processes because the existing spec’s worker-scoped seed is intentionally shared: running both cases in one process after the first now passes exposed test-state contamination in the second case, before any commit request was held. The source-guarded two-case runner isolated that harness concern without changing the spec or product.

- `M2 current013 real parent DELETE: lost ACK, reload, Runtime restart, exact retry and UI inverse restore raw opaque clip` — passed (raw mirror/opaque/registry closure, reload, lost ACK, restart, exact request body and idempotency key, receipt identity, Runtime inverse/Undo, and zero legacy writes).
- `M2 current013 parent DELETE conflict: same-property Agent move wins while the original delete request is held and draft is retained` — passed (real 409, kept original intent/request, additive conflict state, reload/recovery, and zero legacy writes).

The isolated conflict confirmation also passed under test ID `app-m2-delete-browser-json-observation-gate-e2e-parent-delete-observation-conflict-tree06121fff-agent8130-runtime2c4-e2e-integration-1020155541-5006`.

## Local checks

- `node --experimental-vm-modules --test scripts/testing/current013-parent-delete.test.mjs` — 1 passed. The plain `node --test` invocation was a launcher setup error because this Node build requires the VM modules flag.
- `./node_modules/.bin/eslint tests/e2e/local/support/app.ts --max-warnings 0` — passed.
- `git diff --check` — passed.

No full suite, TypeScript check, install, or local browser/socket run was performed. No production fix, key ban, fixture stripping, guard weakening, merge, or ledger deletion claim was made.
