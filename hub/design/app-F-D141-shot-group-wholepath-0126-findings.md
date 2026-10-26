# D141 normal-033-shot-group-pack — productREG

## Verdict

`productREG`: this is a finite cut-only production-path regression, not a test-mock-only side effect and not an own-setup-only change.

The exact case is present on both committed heads with the same title, input, and purpose. It passes in the pristine receipt and fails in the cut receipt because the cut authoring path performs one additional real Runtime command-basis read.

## Exact preserved case

Both test blobs contain:

- `shot-group pack commands > duplicates only the explicitly active non-default timeline and never touches relational storage`;
- `timelineRef: 'active-non-default'`;
- `configVersion: 7`, source `shot-source/V1`, destination `shot-copy`;
- no final video, so no media-task admission;
- derived lineage and group membership `['shot-source', 'shot-copy']`;
- one publication `['rev-2']`;
- no router requests and no relational-surface path.

The cut test is blob `4df8a97cac77b3531cec437e5ae1dc98bebddeff`, title at line 377, assertion at line 397. The pristine test is blob `02589a19ca936e7cac35ee6b59c274ecafbe027f`, title at line 320, assertion at line 340. The 0120 qualified source-presence row is consumed as supporting evidence; complete 32-case membership is not repeated.

## Whole-path source proof

The production caller `src/tools/video-editor/lib/shot-group-pack-commands.ts` is exactly the same blob on both heads: `015ce2d5f182ed711ba51ea8f8bb44af7edd2d0a`. At lines 378–418 it loads the explicitly selected timeline, checks the supplied version, skips task admission when the source has no final video, then calls `mutateTimelineDocument` with `deepCopyShotGroupInDocument`.

The finite source change is instead `src/shared/lib/placement/placementService.ts`:

- pristine `49cdf488ec4037e5c069459a9b4266b2003c7c31` uses `mutateTimelineDocument` → one `loadTimelineDocument` read before save;
- cut `6b5a140fd77cf56ed6661e5d07f269886983bd99` uses the authoring/outbox path. Its `store.load` first calls `loadTimelineCommandBasis`, validates the closure, then calls `loadTimelineCommandBasis` again to detect a changed head before authoring.

For this no-final-video caller, the initial `loadTimelineDocument` is common. The cut-only `store.load` re-read is the additional production read, yielding three observed loads instead of the preserved expectation of two.

## Mock-sideeffect challenge

The cut test mock was migrated from `saveTimelineAtHead` to `loadTimelineCommandBasis` plus `commitTimeline`. Its `commitTimeline` calls the mocked basis loader, but immediately executes `runtime.loads -= 1` with the comment that local response assembly must not count as a caller-side head load. This makes that mock-side increment net zero. The receipt's `received 3` therefore comes from the cut production sequence above, not from the mock's response assembly.

The pristine mock directly implements `saveTimelineAtHead` and has no command-basis commit-side load. This is a finite setup difference, but it does not account for the observed delta after the cut mock's explicit cancellation.

## Receipts

Normal: `app-full-1026004326-12174` (cut `867cb273...`, tree `2b44a46...`) reports the exact case as failed: `expected 3 to be 2` at `shot-group-pack-commands.test.ts:397`.

Pristine: `app-D141-pristine-receiver-0007-full-1026010029-23581` reports `✓ src/tools/video-editor/lib/shot-group-pack-commands.test.ts (6 tests)`; the exact case is not among its 18 failures. The pristine service execution used a synthetic commit, but the prior custody packet proves exact tree `974de7...` and parent `7ca61bb...`; this report does not treat the synthetic identity as the frozen HEAD.

The other full-suite failures, missing Node phase, and dependency-install caveat remain outside this case. They do not erase this exact preserved-case/cut-failure proof, and no source authoring or test adaptation was performed.
