# D100/R1 receiving recipe

Carrier: `/home/user/work/wt/rt-Agent-D100-test-return-1914`

Current source carrier: base commit `9486cbb06e2ab53402086772e6c2bc18bc4849fc`, base tree `0919e511bd28b3d3af76bb18155efda12c3e94f6`. The final harness commit/tree are intentionally pending (`PENDING_HARNESS_COMMIT`); use the harness-produced values in the next handoff.

## Required order

1. Independently review the exact test delta with protected-source scope. Verify the product blob remains `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3` and no non-test path changed.
2. When ordinary free space is at least 5,000,000,000 bytes, run the bounded targeted Agent test against the current source and pinned Runtime input. Do not substitute a new fixture, provider body, or environment.
3. Accept only a faithful result in which the two direct custody cases and the direct shared-owner case pass while all existing refusal/no-write assertions remain active. If it fails, report the first boundary; do not weaken equality or change product semantics.
4. After the corrected 27-node Agent result is GREEN, App owns the meaningful whole-path receiver proof and the exact `f53b` original-9 run. App must remain the sole behavior receiver.

## Commands not authorized by this handoff

No source merge/release request, product edit, Runtime edit, fixture/pin update, old TEN/full/P4/browser/profile/collector/network/acquisition/Store/install run, or D130 action. Source remains HELD until the bounded result and required independent review are supplied.

## Contract/call-path reminder

The production comparator remains Runtime `commitTimeline` → registered Agent provider → `commands.execute` → `doc.patch` → `State` item projection. The direct shared-owner test is only a custody guard comparator with admitted default source offset; it does not certify non-default trim support.
