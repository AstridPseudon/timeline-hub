# Independent P3 review — PASS

PASS is limited to the retained cause/custody qualification; it is not an absolute correctness claim and does not turn the failed Gate-5 journey into a pass.

## Cause and journey

- Actual run `.../app-P3-current-integrated-0900-ap2-P3-gate5-h6-0348-1024103234-3896`: failed after mounted readiness passed.
- Setup/reset returned 200; A was accepted; Agent C callback completed; ACK loss and retry state were reached.
- Network trace independently showed duplicate A traffic:
  - A upstream response: monotonic `85392.110`, status 200.
  - ACK abort: `108857.998`.
  - Exact retry POST: `109848.929`; same key SHA `6fb7369c...fd1523`, same 8621-byte body.
  - B mouse-down: `109892.527`, before retry fulfillment at `109919.129`.
- `faultFirstCommit` counts every intercepted POST and fulfills retries after the first. The production outbox returns pending A before dispatching B; B receives its base only after A acceptance. Therefore attempts `2` demonstrates A retry, not premature B submission.
- B mouse-up, restart, undo, and the later tail were unreached. No product defect was demonstrated.
- Original P1 held recovery behavior remains unchanged and was not rerun.

Source checks:

- Declared App commit `82cb5c...`, tree `6fa0a0...`.
- Observed launcher commit `1bc3f12...` is a real synthetic commit with parent `82cb5c...` and the same tree; the result `snap` itself authenticates only tree/key metadata.
- Relevant production and test blobs are identical between `82cb5c...` and `d6ed8c...`.
- Full spec SHA256: `26c1ae...165d5b`.
- Static tail hash, lines `1608–1741`: `5ede6f...380912`.
- No source, tests, fault wire, or spec files changed.

## Custody packet

All six allowlisted JSON files passed independent structural, enum, bounds, correlation, security-content, production-projector, and exact-writer checks. Attachment duplicates matched byte-for-byte.

| Absolute origin | Size | SHA256 | Scope |
|---|---:|---|---|
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-P3-current-integrated-0900-ap2-P3-gate5-h6-0348-1024103234-3896/playwright-output/p3/mounted-readiness/three-products.mounted-rea-54c87-ed-owner-before-any-gesture/d21-environment.json` | 5305 | `1a333c...ab1f88f` | Metadata-only, mode 600 |
| Same directory `/attachments/d21-environment-json-90f5eb84b49a2383b1ab65b266edf244221eda71.json` | 5305 | `1a333c...ab1f88f` | Exact duplicate, mode 600 |
| Same directory `/mounted-bootstrap-lifecycle.json` | 224 | `98ef162...e8f9ffde` | Explicit UNKNOWN diagnostics, mode 600 |
| Same directory `/attachments/mounted-bootstrap-lifecycle-json-cf3046721821ea2795c42db75b67b918e42b4ff0.json` | 224 | `98ef162...e8f9ffde` | Exact duplicate, mode 600 |
| Same directory `/mounted-readiness-diagnostics.json` | 926 | `c7ebb1...a6e570d` | Metadata-only; mode 644 from existing writer |
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-P3-current-integrated-0900-ap2-P3-gate5-h6-0348-1024103234-3896/playwright-output/p3/mounted-readiness/worker-0/d21-environment.json` | 5063 | `7375b4...9789bb6` | UNKNOWN readiness metadata, mode 600 |

No raw trace, authentication, URL/query, request body, log, or error-context bytes were exported. The readiness diagnostic is content-safe but not private by file mode; any flatcopy should use an explicit controlled destination with mode 600, for example:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/qualified-custody/app-P3-current-integrated-0900-3896/`

## Verification

- Focused A2 Vitest lane: **6 files, 72 tests passed**.
- Native D21/readiness controls: **19 tests passed**.
- Full P1 diagnostic-control files: **40 passed, 1 failed**. The failure is the existing absolute source-hash assertion at `p1-diagnostic-safety.test.ts:211`: expected `0793024b...`, actual exact-source SHA `78e3c969...`; no product or retained-packet defect.
- Serialized TypeScript checks: `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json` — all exit 0.
- Scoped ESLint for A2 and D21/readiness/projector files — passed.
- `git diff --check` — passed; worktree clean.
- No full/original browser journey, HTTP/backend/native seed, or new service run was launched.

The full C0 request/reply contract remains untouched, including request identity, commands, steps, merge/reads/source metadata, idempotency, and complete `{data, receipt}` reply semantics.