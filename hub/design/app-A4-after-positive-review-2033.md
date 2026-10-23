# App A4 after-positive mounted review — PASS

Candidate `001145ce1dcba562ab082620e965e73bac1857d1` is a scoped PASS for the four positive mounted prepared-media cases and safe emitted-input custody.

The candidate is exactly the donor parent `da7f25f0546ada65c224c650488a79a9ff0e1440` plus 213 appended lines in `src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx`. No product implementation, old tests, generated files, schemas, locks, pins, or other mounted test files changed.

The independent run passed the actual mounted `addClip` → `useTimelineSave`/local save session/outbox → `RuntimeDataProvider.commitTimeline` → generated transport → accepted canonical adoption path. It covered missing hold, explicit null hold, subminimum `0.01` normalization (source `0`, inserted `0.0667`, later `5.0667`), and incoming transition. Registry identity, created ID, base pins, ordered insertion, ripple, sibling stability, exact request-body serialization, and accepted canonical adoption were retained. No detached executor or direct-capture substitute was used.

Author packet manifest:

| case | bytes | request SHA-256 |
|---|---:|---|
| missing hold | 2368 | `38afc0473df1616da071f35c3362fcfb7a01dc3fe904a0a7b49b2a0c66c738a1` |
| explicit null hold | 2452 | `a422aaf915d72edb848029e74a394a8ba43897bc3551882a7982b00e268269f1` |
| subminimum duration | 2656 | `99cf8093817631e9df49a4093c3086522419009f58e855fc287bcb62603f17f5` |
| incoming transition | 2416 | `e1f05b38f044d4557f0e28c12c644d077f85e617590a1b2b9050fb4c93527ae5` |

The independent packet regenerated with the same byte lengths and case/change mapping; each case self-verified its serialized bytes, length, and SHA. Hashes vary across runs because the step ID is generated per test. Packet safety scan found no credentials, auth material, or full URLs.

Evidence passed:

- Targeted Vitest: 7 files, 53 tests.
- Scoped ESLint with zero warnings.
- App, Node, and root TypeScript checks under the shared lock and 4096 MB heap.
- Candidate-vs-parent `git diff --check`.

The author’s first focused attempt saw a stale recovery-draft barrier in the four new tests; the clean rerun passed 53/53, and my independent run passed as-is.

Remaining gaps are explicit: App-only synthetic transport evidence; no raw-provider/Python equivalence, live Runtime HTTP, browser, whole-A4, merged/rebased, invalid, preview, history/undo, or expanded reply-envelope proof. P1 and deletion remain HOLD. No merge or product change is recommended from this review.

