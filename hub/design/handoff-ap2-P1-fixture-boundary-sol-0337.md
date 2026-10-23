# P1 fixture-boundary correction handoff — 2026-10-23

Result: **static source correction complete; execution NOT READY; not H3 GO/body PASS**.

On integrated App base `9eda8e907`, imported only the reviewed
`tests/e2e/local/three-products.p1-chain.spec.ts` from Sol source
`4fa831be1`. The spec is the only worktree file changed.

The proof now follows the current product source at the original boundary:
the numeric-hold seed splits at 2 by changing hold/at/ID while preserving
source windows and authored app state; Source In is located through its
existing normal DOM container; and the refusal branch compares the complete
post-refusal canonical parent/closure to the accepted Agent move baseline,
including native `app.astrid.fixed_start` and duration-based `for`.
All original scenario boundaries and strict accepted/merged/refused,
raw/null/absence/foreign/order/guard/retry/receipt/history assertions remain.

The strict merged proof remains in the source and is explicitly marked
execution NOT READY. Current `timelineLocalSaveHandoff` omits authoritative
reads/intent metadata, so `localSaveSession` conservatively sends omitted-read
`doc.patch` as `merge: atomic`; the required merged trim after the
same-parent Agent label cannot succeed until the App-owned existing
authoritative read/intent seam exists. No inferred reads, forced fields,
request injection, expected-status rewrite, executor/port, or product fix was
made.

Static checks passed: exact Playwright list (2 tests), `npx tsc --noEmit`,
scoped ESLint with max warnings 0, and `git diff --check`. No browser,
socket, body, full, heavy, source-ready, or H3 run was performed.

Recommended next step: App owner supplies the authoritative existing
read/intent seam, then central service qualification runs this exact spec;
independent review follows.

