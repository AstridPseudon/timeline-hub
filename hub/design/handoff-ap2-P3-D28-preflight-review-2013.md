# Handoff: P3/P2 D28 mounted preflight independent review

**Verdict: FAIL.** Reviewed author commit `407c23990c9cefdfcd0d9130950af85af4550e7a`, tree `7366435697bcf2451fe138b5b7505211252b665c`, with sole new blob `3bd89781664523d656a9e06173e03635e35bad0f` (SHA-256 `82efba128301f947e90382465cb0df7d7b2f74c5004300bf64a47fe6ebcac3e4`).

Blocking findings:

1. `commandOutboxes()` returns `[]` when the scoped IndexedDB database is absent (`support/app.ts:203-205`). The leaf marks that outcome as `initialOutboxRead = true` (`three-products.mounted-readiness.spec.ts:206-221`), builds an empty `previousOwnerIds`, and later accepts any settled owner as fresh (`:247-249`). Unavailable/absent baseline must remain `UNKNOWN`, never empty-set proof.
2. The `connected-selection` snapshot after `openSeededTimeline()` (`:239-243`) reuses the pre-selection `connectionSummary` and sets `actualConnected: true` without a fresh status read. A drop during selection can therefore be reported as connected. Re-read or record `UNKNOWN`.

The real deferred/native fixture, hosted origin, production helpers, original owner predicate, 90-second ceiling, no-gesture boundary, and assertion rethrow are otherwise aligned. No runtime result is claimed. Farm packet `31814/15659` remains historical with lost traces and environment equivalence not proven.

Static evidence on the unchanged review tree: root/app/node TypeScript no-emit, named ESLint, new Playwright list (1), original P1 list (2), original P2 list (8), Gate-5 list (1), and `git diff --check` all PASS. No browser/test-service/full run was performed.

Next: correct only the new preflight/helper seam, rerun these static/list checks, and then let Farm run the report-only mounted suffix after the unchanged native/history prefix. Static PASS is not mounted GREEN or Gate GO.
