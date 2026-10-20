# AP2-M2 bootstrap audit/scope review gate

## Result

**REQUEST CHANGES.** The bounded-source assertion conversion is not safe to
qualify, so I did not submit the central gate. The candidate is otherwise
test-only, but it introduces a shared helper regression outside the narrowed
bootstrap path.

## Blocking finding

`tests/e2e/local/three-products.spec.ts:153` changes `timelineBase` from using
`harness.seed.projectId` to reading `seed.projectId`:

```ts
const timelineBase = (_harness: DirectHarness, seed: ThreeProductsSeed) =>
  `/v1/projects/${seed.projectId}/timelines/${seed.timelineId}`;
```

`ThreeProductsSeed` in
`tests/e2e/local/support/harness.ts:311-327` declares `projectSlug` and
`timelineId`, but no `projectId`. Existing callers pass the normal `seed3`
object at lines 395, 821, 852, 957, 989, 1004, 1098, 1125, 1299, 1328,
1347, 1379, 1391, 1398, 1430, 1486, 1512, 1531, 1547, 1562, 1588, 1609,
1646, 1667, and 1687. At runtime those calls now construct
`/v1/projects/undefined/timelines/<timeline>`; statically, the property is
also absent from the declared type. The bootstrap test's
`bootstrapSeed = { ...seed3, projectId: ... }` supplies the property only
dynamically and masks the regression in that single selected test.

The intended created-project history lookup can be retained, but it needs a
scoped helper/type or an explicit project-ID argument that leaves the existing
seeded callers on `harness.seed.projectId`. This is required before approval;
I made no source edit because this task is review-only.

## Review disposition

The rest of the delta was inspected against preserved `80ac5f4ba` and the
original bootstrap assertions. The Runtime-door audit plus `waitForAudit`
approach is non-circular and uses exact created-project/selected-timeline
paths; accepted Runtime history retains the init command/version/order claim;
the create-before-init, outbox scope, retry/reload/restart/recovery, guarded
undo, opaque, and zero-legacy controls remain present. No fabricated product
observer or arbitrary POST selector was found.

Because of the blocking helper regression, the required unique central
bootstrap suite was **not requested**. Consequently there is no central
`--list` or browser result to report, and no qualification claim is made.

## Checks

- Read-only `git status --short --branch`: clean at `d1f7d1320`.
- Read-only diff inspection: exact candidate delta is the test-only
  `d1f7d1320` change over preserved `80ac5f4ba`.
- No local runner, browser, socket, dirty-tree test, full suite, or central
  test was run, per task constraints and because review did not approve the
  candidate.

## Next step

Repair the project-scope helper without changing the preserved seeded behavior,
then repeat this independent review. Only after that review approves should a
single central request be registered and dispatched with the unique bootstrap
substring and pre-build one-test collection proof.
