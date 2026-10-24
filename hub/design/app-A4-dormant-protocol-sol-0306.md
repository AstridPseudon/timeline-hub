**Disposition: dormant under existing D37.** No production caller reaches the remaining legacy chain/native-label session or TS executor. No source, tests, helpers, or ledger files changed.

Reviewed HEAD `a64587176d4132bf2ad3a05ab0fe656913625c8d`, tree `21ecf5b9360c2169febc745daaf752eca5e54a10`.

Production graph:

- `VideoEditorPage:140,841` → `VideoEditorProvider` → `useTimelineState:620` → [useTimelineSave:223](/home/user/work/wt/app-A4-dormant-protocol-sol-0306/src/tools/video-editor/hooks/useTimelineSave.ts:223) → `createLocalSaveSession` → `provider.commitTimeline`.
- Production imports contain no value edge into `commitSession.ts` or `runner.ts`. `trackLabelCapture` is reached only from dormant `commitSession` and `genericPatchCapture`; `trackLabelGesture` has no production value caller.
- The separate live writer remains [VideoEditorProvider:324](/home/user/work/wt/app-A4-dormant-protocol-sol-0306/src/tools/video-editor/contexts/VideoEditorProvider.tsx:324) → agent-chat registration → [element-adapter:101](/home/user/work/wt/app-A4-dormant-protocol-sol-0306/src/tools/video-editor/runtime/element-adapter.ts:101) → `saveTimelineAtHead` → `publishParentComposition`. Leave its migration with element-writer0306.

Manager-copy records for the existing ledger; every row’s status is exactly **`dormant: no production caller; follow-up deletion for owner review`**:

| Proposed ID | Bounded retained scope | Required closure |
|---|---|---|
| APP-A4-D37-SESSION-CHAIN | `commands/commitSession.ts`; remaining non-label and explicit-resolution declarations in `commitSession.test.ts`. Entry function at `:177` has no production caller. | Preserve `__tests__/commitSessionEnvironment.ts`, all five existing `commitSession*.test.ts` files, their capture/gesture dependencies and fixtures. Retain exact pending body/key, fresh dependent key, restart, raw closure, refusal, history and undo assertions. |
| APP-A4-D37-NATIVE-LABEL | `commitSession.ts:713` native label port; `trackLabelCapture.ts`, `trackLabelGesture.ts`; original label declarations at `commitSession.test.ts:640`. | Preserve both label helper test files, the session environment, and generic-patch/ordinary-member support tests. Native presence/clear, observed/unobserved remote actions, guarded history/undo and canonical closure assertions remain unchanged. |
| APP-A4-D37-EXECUTOR | `runner.ts`, whose exported execution functions have no production caller. | Preserve `runner.test.ts` and its existing fixtures. No replacement executor or provider operation. |

These apply D37 without introducing an exception or authorizing helper deletion. Shared production helpers remain retained.

**Identity checks:** all **35 remaining declarations** are byte-identical to original `5ad7907e86`; zero changed declarations. SHA-256 of their source slices, joined with newlines:

`105b609181c83ec7f9a6505c348c3261ff1626991a49da2cba3c7206ef23cbc0`

D31/D37 protected implementation/test blob identities match `5ad7907e86`:

| Subset | Implementation blob | Test blob |
|---|---|---|
| Transcript | `bd14f45cbcd10292ca00246072949264d9127a91` | `5c39a293009df59f796fe476e107a0a9900244d7` |
| Track reorder | `81ec771ab972da61654b96e45caa9506e8a797e7` | `61d123e0b63d3f3321afaa1218eda9ecef7e3292` |
| Raw after-anchor birth | `2703ff50624c41b40369969a7b5aa573df66f4ab` | `346ae62eac5936e946266924f5e79e27df8dab54` |

Separate migrated credit remains bounded:

- Replay merge `9e83160c0e`: uncertain-A/unsent-B replay only.
- Label-refusal merge `a64587176d`: close, pending-label identity and invalidated-typing cases; original ownership/display-basis/mixed-preview declarations remain.
- Historical packet results were 138 and 128 targeted passes respectively; neither qualifies the whole family.
- `git merge-base --is-ancestor 107abbd3e0 HEAD` and the same command for `a73c11121d` both returned **1**: failed packets remain unmerged.

Verification: read-only `rg` and TypeScript import/declaration audits completed. `git diff --check`, `git diff --exit-code`, and `git diff --cached --exit-code` passed; `git status --porcelain=v1 --untracked-files=all` was empty. Generated wire types are unchanged. No tests, build, browser, backend, service or provisioning runs were performed, as instructed.

No blocker to this disposition. Manager should copy the bounded records; whole A4 remains open until the separately owned live writer is cut. Commit-message metadata and `DONE` were written.