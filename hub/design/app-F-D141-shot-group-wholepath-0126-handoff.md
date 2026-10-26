# D141 handoff — normal-033-shot-group-pack

## Sol / orchestrator action

Consume `verdict.json` as `productREG` for this one finite comparison.

The minimal source explanation is:

1. `shot-group-pack-commands.ts` is byte-identical on cut and pristine, so the caller is preserved.
2. The exact test title/input/purpose is preserved and the pristine receipt passes all six tests in the file.
3. Cut `placementService.ts` changed the mutation implementation from one `loadTimelineDocument` cycle to canonical command-basis authoring with a pre-authoring re-read. That extra production read changes this test's observed count from 2 to 3.
4. The cut test mock's commit-side basis read is explicitly cancelled (`runtime.loads -= 1`), so it is not the cause of the +1.

No source repair, test adaptation, writer addition, or contract change is proposed by this packet. Do not broaden this finding into the stopped B022/Element/SWAP/profile investigations.

## Custody and limits

The exact normal and pristine source heads/trees and raw result IDs are in `source-map.json` and `verdict.json`. The prior 0120 custody packet remains immutable. Its pristine run used the exact frozen source tree under a synthetic service commit; this is adequate for the source-byte join, while dependency-byte and Node-phase limitations remain global receipt caveats, not an UNKNOWN for this exact case.

This case exercises the accepted commit path in the cut mock (`base_revision_id`, `commands[0].args.changes`, accepted canonical document, accepted head, and receipt). It does not independently exercise every request/reply contract branch listed in the brief; no claim is made beyond this caller/path qualification.

## Recommended next step

Carry the `productREG` finding into the central D141 result and assign product diagnosis to the placement-service authoring/read-count regression. Preserve the active non-default timeline and no-relational-storage assertions; do not “fix” this packet by weakening the expected behavior test.
