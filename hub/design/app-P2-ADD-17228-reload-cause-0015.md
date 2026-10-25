## Result: actual17228

No App source correction is justified. The retained trace proves the missing post-reload occurrence is downstream of pending Runtime internal timeline-revision reads, not a proven App rendering defect.

Reached in source order:

- Readiness: PASS.
- Initial shared-occurrence popup, dialog, shot editor, and current-time checks: PASS.
- Mutation/commit assertions, canonical acceptance, media commands, and canonical-document equality: PASS.
- Post-commit history/publication/canonical-head checks: PASS.
- Reload parent composition and shot-revision reads: HTTP 200.
- Two internal timeline-revision reads began after reload and remained unfinished (`status -1`) until teardown.
- `openPopup` then failed at `three-products.p2-popup.spec.ts:356`, after its 5.05s visibility wait.
- Post-reload selection, edit, history, and inverse-undo checks were not reached. The SWAP case was not run.

Safe attribution:

- Phase: post-reload canonical shot-composition loading.
- Pending duration: approximately 10.1s until teardown; the occurrence locator itself waited 5.05s.
- Correlation: none emitted; no trace/idempotency correlation header was present.
- Immediate source owner: Runtime internal timeline-revision reads. App’s loader was awaiting that input; no rendering defect was proven.

Hashes verified:

- Worktree HEAD: `fd2f843a6957deef0a059a97d36671cee9d39e91`
- Protected source blobs matched: `three-products.p2-popup.spec.ts`, mounted-readiness spec, `support/app.ts`, `support/harness.ts`, `support/astrid.ts`, and `support/p2-element-diagnostic.ts`.
- `git diff --check`: PASS.
- Worktree: clean.

No product files were changed. No oldRED/currentGREEN run, TypeScript, ESLint, or full suite was run because this is a readonly attribution finding. No ledger paragraph applies.

Recommended next step: Runtime ownership should investigate why the two internal timeline-revision reads do not complete and add safe server-side correlation if needed; rerun the retained flow only after that external state changes.