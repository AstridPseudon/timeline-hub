# D127 report

- Verdict: **FAIL** for retained actual result `32016`.
- Preflight `29958`: PASS, exit 0.
- Readiness: PASS, 1/1.
- Original element body: FAIL, 0/1, exit 1.
- First predicate: `three-products.p2-elements-assets.spec.ts:1052` — expected dialog status `"applied"` within 5 seconds; locator was absent.
- Later params/canonical/history/reload/Undo assertions were not reached, therefore UNKNOWN—not refusal or pass.
- Runtime capture was request-bound (ordinal 1, PID/birth/namespace/key hash), completed with HTTP 200 internally; App response, provider outcome, and caller receipt remain UNKNOWN.
- Privacy/custody checks passed; raw key/payload/headers/private capture were not published.
- No source/product/test changes or reruns.

Evidence:

- `verdict.json`
- `findings.md`
- `source-custody.json`
- `safe-profile.json`
- `publication-manifest.json`

Validation: JSON/XML parse, SHA256/Git exact-source checks, `git diff --check`, clean worktree, output mode/hash/privacy checks all PASS. No blockers to this review; the behavioral failure requires coordinator follow-up before any rerun.