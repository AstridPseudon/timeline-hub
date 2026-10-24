## F-App-full report

- Source verified unchanged: App `be98aac54e275282467d85f79d3beb4665416039`, tree `2839c7e7841d1c0897fd8e7c12f0c848d94e3979`, parents `d24ed69dcd...` and `94d89d36e...`.
- Same-ID request: `app-P2-P3-e68-current-pure-target-1409-full-1024144535-8158`.
- Command: `npm test -- --maxWorkers=3`.
- Result: exit `1` after `1203s`; Vitest duration `1197.12s`.
- Counts: `1341 passed, 1 failed` files; `19256 passed, 1 failed` tests. Node suite was not run because `test:app && test:node` short-circuited on the Vitest failure.
- Failure: `src/integrations/runtime/installManifestSkew.test.ts:17`, installer digest `sha256:3605a9c517d92031d7702307e256223905784e0800bcd09c87005ce21ee53a47` is absent from `RUNTIME_ACCEPTED_SCHEMA_DIGESTS`.

Classification: non-core release/installer regression; not environmental, preexisting, dead, or unproven. The same node passed in retained full run `16138` on tree `3311baa...`; current `public/install-manifest.json` changed from accepted `53bc...` to `3605...`.

Historical Node evidence remains separate: 36 repaired nodes passed; exactly two extension nodes remain environment failures due `ssh-keygen ENOENT`. No current Node result is claimed.

Quality guards passed before Vitest: no smoke tests, no raw skips, no unauthorized expected failures, and skip registry valid. Production source still contains the mounted save funnel, outbox, `commitTimeline`, and `Idempotency-Key` handling. This full suite is not a live-gate claim.

Artifacts:

- `summary` SHA256 `7343a49d...`
- `snap` SHA256 `a4d282a...`
- `log.txt` SHA256 `6b2b18a...`
- Node report SHA256 `024f698...`

No product, test, generated, pin, registry, or design files were changed. Worktree is clean. Commit message and `DONE` marker created.