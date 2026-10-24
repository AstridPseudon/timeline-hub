## Verdict: FAIL / do not apply

The proposed patch is not a faithful Runtime-restart proof.

Findings:

- `harness.restartRuntime()` stops the old Runtime and starts on a different port (`tests/e2e/local/support/harness.ts:684-690`).
- The patch stages the retry before restart, then calls `releaseStagedRetry()` afterward. That route retains the old request URL, so `route.fetch()` cannot prove delivery to the restarted Runtime.
- It calls `expectConnected(reopened)` immediately after restart. Existing restart behavior requires the page’s Reload action first (`three-products.spec.ts:731-746`); the patch omits that.
- Thus `observed[2]` is a pre-restart retry, not a post-restart automatic retry. The exact key/body checks are preserved but do not establish the required restart boundary.
- The original D53 `[A,A] / forwarded[A] / zero-B` guard remains statically preserved. B ordering, request fields, reads, history, canonical closure, legacy traffic, and undo assertions are also retained statically, but remain behaviorally unverified because the new lifecycle cannot reach them correctly.
- The new `armRecoveryRetry` branch is not covered by the three focused classifier controls; those controls pass independently.
- `fullproposal.md` is absent. No missing hash or evidence was invented.

Hashes:

| Region | Actual | Virtual proposal |
|---|---|---|
| Full spec | `a6468188ff21c4fd8bd397ff242b0260ee92ab6f2f90ac94786973eaf3c1e99a` | `29808a244deb5e28060a8046e467cd5a3a4d8298adf0ac0f94b38c481374e66c` |
| `faultFirstCommit` | `0ac6ab0f91cfc9fee0136ec90f408584e2a7755f245b7aea2f85f06c8c316c31` | `ac1f5e84db27a88a5eff68dbf748b60b6d93dd2ef3789521d53976843cd5ccf7` |
| Reopen/restart block | `3eb9feee0aa8485830b7305981d58f65617b0aeac523c4b08615e87c095bd2bd` | `1598e21e616fdbaf9a3790e70fa46c5b0a92bb9b9ff3d5a99ed44a8ccc283fd2` |

Checks:

- `git apply --check proposed.patch` — PASS.
- Node20 Gate5 controls — PASS, 3/3.
- Node20 ESLint on virtual patched file — PASS.
- Proposal artifact `git diff --check` — FAIL: trailing whitespace at patch lines 40 and 65.
- No browser, Runtime service, full suite, trace export, or private collector run.

No source files were edited. Required `commit-msg` and `DONE` markers were created.

Recommended next step: revise the proposal so restart occurs before the reopened-page production retry, reconnect/reload the page through the real lifecycle, and observe a retry sent to the new Runtime origin.