## D30 report — Sol1214 whole-path assessment

No product or test files changed. Worktree is clean.

Source custody:

- Current HEAD: `602f8b1f58593302829fb449d0ded62a91462a22`, tree `a38844975865110cd2c026dc10fd7aa1ea488e71`.
- Actual P2/H36 source: `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4`, tree `542b772e6deed676b917f857708445b7d37a5aa8`.
- Passing P1 source: `f8b15af0a66ed14e7711a4bb7f1ed5b62b4988b5`, tree `dde63bed393f716033baaa3512cd5be379a095c1`.

Actual run `11933`: exit 1, 469s; 0 passed, 3 failed, 5 not run. Element assertion at `tests/e2e/local/three-products.p2-elements-assets.spec.ts:391` missed `applied` after 5s while the button remained `Applying…`.

Retained H36 artifact SHA-256: `08509524d5fd04f181b3fac8d0cdd211a32e2f4a107c4e78807ae4713e8533a4`.

Observed lifecycle was exactly:

`apply-click → request-start → retained`

The request had an idempotency key and remained `pending`. No response, request-failed, requestfinished, receipt, or server outcome was observed. Actual Runtime outcome is therefore UNKNOWN.

Call graph:

- [`ElementsLibraryPanel.tsx:46-107`](/home/user/work/wt/app-A2-element-whole-path-1214/src/tools/video-editor/components/ElementsLibraryPanel.tsx:46): captures the adapter synchronously, executes the element operation, then sets the success message only after execution and query invalidation.
- [`element-adapter.ts:412-497`](/home/user/work/wt/app-A2-element-whole-path-1214/src/tools/video-editor/runtime/element-adapter.ts:412): authority/admission checks, mounted-document read, then `routes.save`.
- [`useTimelineSave.ts:759-796`](/home/user/work/wt/app-A2-element-whole-path-1214/src/tools/video-editor/hooks/useTimelineSave.ts:759): waits for the local owner, captures the element edit into the handoff, and flushes the existing outbox.
- [`localSaveSession.ts:160-200`](/home/user/work/wt/app-A2-element-whole-path-1214/src/tools/video-editor/commands/localSaveSession.ts:160): builds the scoped v2 request and calls `provider.commitTimeline`.
- [`dataProvider.ts:751-767`](/home/user/work/wt/app-A2-element-whole-path-1214/src/integrations/runtime/dataProvider.ts:751) → generated client `/commit` POST with `Idempotency-Key`.

No early producer detachment is established: `request-start` proves the path passed the local owner, handoff, outbox, and provider dispatch boundaries. No late server result is established either.

Diagnostic limitations found:

- [`p2-element-diagnostic.ts:13`](/home/user/work/wt/app-A2-element-whole-path-1214/tests/e2e/local/support/p2-element-diagnostic.ts:13) has no `requestfinished` stage; it records only response, request-failed, and page-close.
- [`support/app.ts:89-97`](/home/user/work/wt/app-A2-element-whole-path-1214/tests/e2e/local/support/app.ts:89) retains and attaches the artifact before closing the page, so later teardown events cannot update the attached snapshot.
- [`p2-element-diagnostic.ts:197-207`](/home/user/work/wt/app-A2-element-whole-path-1214/tests/e2e/local/support/p2-element-diagnostic.ts:197) reads only `[role="status"]`; production reports in-flight state through the Apply button (`Applying…`), while the role-status node is created only after completion. Thus `status: "unknown"` is an evidence limitation, not the cause of the save hang.

P1 comparison:

- P1 passed on the separate tree: 2 tests, 56.3s.
- Accepted split is proven at [`three-products.p1-chain.spec.ts:1438-1454`](/home/user/work/wt/app-A2-element-whole-path-1214/tests/e2e/local/three-products.p1-chain.spec.ts:1438).
- Merged trim and exact retry are proven at lines 1472-1492 and 1543-1558.
- This proves the shared outbox/provider/reply path can handle accepted and merged replies, but it is a different gesture and does not establish element-request latency.

The full v2 request/reply contract remains untouched: scoped IDs, commands, steps, patches/reads, merge mode, source metadata, dry-run, idempotency key, `{data, receipt}`, canonical document/digest/id map, authoritative records/dependencies, accepted/merged/historical rebased, conflict current, and invalid code/path/hint.

Validation:

- `git diff --check` — PASS.
- `git status --short --branch` — clean.
- No targeted or full tests rerun; this was a read-only assessment as requested.

Decision: no product repair, timeout change, guard/body change, executor restoration, or new extractor is justified. Sol1214’s witness must preserve the real mounted caller and classify only an observed response, request failure, or teardown abort; a request still pending at retention/page close remains UNKNOWN.