# P2 automatic-placement proof repair handoff

Repair complete; ready for independent no-weakening review, not browser-qualified.

Base `fb1ee88f060e4823a22fc4e0cc108083f15efb63`; only `tests/e2e/local/auto-real-proxy.spec.ts` changed. Final source blob `a8b411b0686d94f375185c0012f3308d0090cba2`.

- Exact accepted-null / merged-previous-head assertions replace the contradiction.
- Inverse waiter requires actual production v2 Undo metadata and retains exact core request checks; missing metadata fails.
- `undo_steps` is exact null for whole inverse, exact validated selection map for per-step inverse. Receipt/history/command/step correspondence is exact.
- All Runtime history items are checked against the unchanged seed prefix plus the real placement/inverse publications; every new writer receipt must be `timeline.commit`. Incomplete pagination and network legacy traffic fail.
- Corrected missing head-helper import and nested receipt/publication-vs-key oracle errors. Original journey and canonical/custody assertions remain.

PASS: exact Playwright list (1), scoped ESLint, actual App/Node typechecks, 75 browser-free causal matcher probes, read-only private 819acf Composition `0.0.14` resolution, scope/diff/EOF controls. Supplemental spec-inclusive TypeScript check remains red on 4 pre-existing harness errors; baseline comparison finds zero new errors and resolves 3 missing imports. No product/fixture/pin/generated/dependency changes, Git writes, browser/HTTP/build/full/service runs or requests.

Exact commands, decisions, probe provenance, logs and limitations: [worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P2-auto-proof-sol-return-1045/report.md).

Next: independent source review, then separately authorized central real-journey qualification. No plan decision changed; no repair blocker.
