# FAIL — A3/P2 review

Candidate `380bf712e85c6646df626229871de4f17e6d97a8` is not approved or applied. The clean worktree remains unchanged.

Findings:

1. **Locked oracle contradiction.** Actual host window is `[0,12)`, input is `4.5`, and hold duration is `5`, so the intended raw clip is `[4.5,9.5)`, not the author-reported `[4.5,9)`. The existing semantic oracle still computes `trySnapToEdge(..., 4.5, 5)` as `9`, yielding `[9,14)` and rejecting at Runtime. Existing mounted assertions also expect `9`.

2. **Policy predicate is insufficiently scoped.** The new policy activates on `canonicalComposition.occurrenceIds.length === 1` plus a visual pointer track. It does not prove current occurrence ownership, project/timeline scope, head, or canonical-owner identity. A singleton parent composition could satisfy this predicate. The policy also bypasses collision/snap resolution, authorizing overlap with existing `[3,6)` and `[6,9)` clips without a bounded owner predicate.

3. **Insufficient full-path evidence.** The only new test changes the unit expectation from `9` to `4.5` and adds singleton metadata. It does not prove the managed preview → `dropAsset` → prepared media → capture/outbox semantic request path, nor add policy-specific wrong-owner, absent, or ambiguous guards. The unchanged protected oracle therefore remains incompatible.

Candidate commit files/blobs reviewed:

- `useAssetManagement.ts` — `3eb297a02d05b50187007d9acb7b4bf95ccc38b4`
- `drop-position.test.ts` — `e6a98af4f2ebba4450be2e536a0374d3832fbc03`
- `drop-position.ts` — `375b0340b73ae7fe892d044c2c8f12fcae230083`
- `external-drop-utils.ts` — `6f55982963d742d4537dccafef81d8a85f4387dc5`

Recommended minimum correction for the author:

- Raw placement should require an explicitly verified child occurrence owner/scope/head, exactly one matching canonical occurrence, matching active non-source visual track, and the managed-image path.
- Missing, wrong, or ambiguous ownership must retain existing `trySnap` behavior.
- The semantic oracle should use raw `4.5` only under that same proven predicate; all ordinary/parent cases must continue expecting `9`.
- Add faithful preview-to-outbox coverage and negative policy cases.

Tests:

- Targeted clean controls: **3 files, 54 tests passed** (`drop-position`, `mountedFileDrop`, `media`).
- Direct semantic-oracle test invocation: no test files collected under the configured include paths.
- Candidate diff check passed.
- No full/browser/service/build/install run, per instructions.

`DONE` and the required commit message were created.