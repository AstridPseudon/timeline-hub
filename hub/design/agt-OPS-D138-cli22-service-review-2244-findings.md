# D138 CLI22 operational/core-path review — FAIL

Reviewed recipe commit `2111f23d356de971b28947ac0ce01f45e429f6d5` against the
G3/G5/P4 and C0 boundary. Only the new `ops-d138-cli22/` surface was changed.

## Finite findings

1. **D138-F1 — blocking: mixed Runtime source.** The reviewed Agent candidate
   is `cd63…` with lock source `ab1e…`; the recipe declares normal Runtime
   `f103…`. The migrated test calls `use_runtime(vendored_runtime_commit())`.
   That helper reads `runtime.lock.json`, then archives the lock commit, so the
   test body selects `ab1e…` and does not select the launcher manifest's
   `f103…` checkout. This is not waived by the 15 lock-file byte matches.

2. **D138-F2 — high: duplicate manifest keys are not refused by the supported
   launcher.** The private fixture appended a duplicate `agent_sha`; the
   unchanged launcher accepted it, reached the fake body, and returned exit
   17 with a second body-call record. Its parser is last-write-wins. The
   private key=value parser rejects duplicates, but that is not the production
   launcher guard. A malformed line is refused before body.

The exact22 source/selector and caller static checks otherwise pass: the
`pytest.mark.integration` marker is exact, all 22 parameterized selectors are
present once, the parser-only sentinel is excluded, and the central parser
appends the requested files without adding the sentinel. The supported
caller remains `TimelineSession.commit_many` → canonical Runtime commit route;
no C0 DTO or product source was changed.

## Separate receiving status

**NOT_READY.** No central row, authentic receipt-rendered manifest, real
profile/schema/interpreter dependencies, per-request receipts/XML/logs, or
actual collection/body execution was available. The shared Agent checkout was
observed at pending U4a merge `41ad…` during review; it was not silently
retargeted or treated as HOME for the reviewed `cd63…`/`ab1e…` candidate.

Focused controls are operational controls only and do not count as original
22-case behavior evidence.
