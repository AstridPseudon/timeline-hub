# A3 SWAP created-claim report

Implemented the minimal App fix:

- New replacement alias absent from the verified pre-edit registry now claims `occurrence:<id>/asset:<alias>`.
- Reused aliases emit `created: []`.
- Added focused new/reused SWAP tests.

Files changed:

- [shotTimelineDataProvider.ts](/home/user/work/wt/rt-A3-SWAP-created-2343/src/tools/travel-between-images/components/shotTimelineDataProvider.ts:865)
- [shotTimelineDataProvider.a3.test.ts](/home/user/work/wt/rt-A3-SWAP-created-2343/src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts:396)

Checks:

- Vitest: 37/37 passed using Node 20 private navigator shim.
- ESLint scoped to both files: passed.
- `git diff --check`: passed.
- Protected six-file diff/hash check: passed.
- TypeScript: blocked by pre-existing missing generated Composition exports (`animations/effects/transitions.generated`), unrelated to this change.

Evidence retained under the assigned worker evidence directory. Commit message written with subject `fix(app): declare created asset for popup swaps`.

Independent core diff review remains pending for the manager/orchestrator; I did not self-approve it.