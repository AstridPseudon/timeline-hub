# App A4 remaining positive mounted after-anchor cases

PASS: appended four bounded mounted prepared-media witnesses to the existing App persistence test. No production code, old test, generated file, schema, lock, pin, or other test file changed.

The cases are old video missing hold, explicit null hold, subminimum duration, and incoming transition. They run through the actual `addClip` prepared-media caller, preview normalization, `useTimelineSave`, local outbox/session, `RuntimeDataProvider`, generated transport, and accepted canonical adoption. Assertions retain source opaque/null/absence behavior, created IDs, registry identity, order, V1 ripple, V2 sibling stability, and the exact serialized v2 `doc.patch` request.

The subminimum case exposes an App-specific normalization boundary: input hold `0.01` becomes source hold `0` on the frame grid, the inserted clip becomes `0.0667`, the later clip becomes `5.0667`, and the request carries the source hold patch. This is recorded as observed App behavior; it is not substituted for the old raw-provider positive or claimed as Python acceptance.

Synthetic exact input packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-A4-after-positive-mounted-2019/a4-after-positive-input-packet.json`. Packet safety and SHA checks passed.

Evidence: cumulative targeted Vitest 7 files/53 tests PASS; scoped ESLint PASS; App, Node, and root TypeScript PASS under the required shared lock and 4096 MB heap; `git diff --check` PASS. No full/browser/live/service/P1/P2/P3 suite was run. Branch remains HOLD pending independent review and the plan’s P1 gate.
