# RT07 / ordinary014 release-prerequisite handoff

Date: 2026-10-20. This is a reviewable merge handoff only. It grants no
permission to merge, release, pin, activate, or publish, and it does not mark
RT07 deleted.

## Exact current identities

- RT07 code-only retirement candidate: Runtime commit
  `40e7dc7cd627c6c4e2bffb482926bb9b037f0143`, tree
  `a7c86e8514c1cc095635e1484b71c98928debe01`, parent
  `b88a56feb2e1879455b9f1eb2403e171aa125f3c`. It removes legacy publication
  writes while retaining authority parsing, replay-only reads, and the approved
  native behavior mappings. It has not merged.
- ordinary014 current Runtime candidate: commit
  `202074110717146fc7f08af2306a8dd7f695b0b1`, tree
  `ee39286bd0eb27d4075074cc4785d6d15e33f243`. It is unpublished Runtime
  0.2.14. The exact producer is `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
  tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`; raw schema is
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
  artifact version is
  `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`;
  manifest is 75 entries with digest
  `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
- The ordinary014 candidate does not yet contain the owner-strict `cd0`
  marker transition. The carry is test-only and must not alter the producer,
  schema, generated clients, artifacts, or version metadata.
- The latest current-preserving Agent source evidence is commit
  `3c4f6de4fa777323b3386c01c7266b619b86af6d`, tree
  `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`. The separately reviewed normal
  pin candidate is `e86f44d04e0a5f183d82d4d1ac307951dd32c44`, tree
  `5b4ec03d6d3081f9a3b96676f10ca051c4e9775e`; neither is a public pin or
  release, and Agent must reconcile the current source with the final cohort.

## Evidence already available

- RT07 current-base finalize: central Runtime targeted evidence is 19 passed,
  6 deselected, and 1 existing strict xfail; the integration lane is 6 passed
  and 20 deselected. The xfail is the obsolete legacy prepare/write seam and
  is not native replacement evidence.
- The corrected retained full on exact Runtime `86ce14f` recorded 5,540
  passed with 7 established baseline failures and no new failures. The later
  seven-fixture repair was approved and merged through `d6ae19b` / merge
  `5c32832`; this is background qualification, not a new RT07 deletion or
  ordinary014 release.
- ordinary014 has bounded native/HTTP evidence on its exact candidate, but no
  complete same-cohort adoption. Its carried test is the pre-`cd0` form.

## Remaining prerequisites and owners

1. **Agent: current consumer/source.** Requalify the registered requester ->
   settled proposal -> requester outbox -> `/v1` commit path on a current
   Agent source. Account for `generic_host.py`, `runtime_stitch.py`,
   `sdk/remote.py`, and `sdk/workspace_client.py`; prove both original native
   positives and clean custody teardown, with no legacy publication traffic.
2. **Agent: stale-consumer failures.** Do not call old Agent `7b3` current.
   Its catalog/history failure is the missing already-merged
   `TimelineSession.restore` facade and belongs to the current Agent consumer
   owner. The hold-clear failure is an Agent semantic-capture refusal before
   any Runtime request and likewise belongs to Agent; Runtime must not add a
   projection or hold override for it.
3. **Agent + Runtime: ordinary014 boundary.** Carry the exact owner-strict
   `cd0` transition onto the final ordinary014 cohort. Preserve the current
   public-013 parent refusal and the complete positive body under the narrow
   strict xfail until the 0.2.14 parent-ownership source is actually present.
   Requalify the exact source/artifact tuple afterward.
4. **App: consumer adoption.** Consume the same Agent/Runtime tuple, update
   only the normal014 client/vendor source needed for that tuple, and run the
   parent-media acceptance plus Gate 5 journey. Existing private checks do not
   constitute adoption. Public 0.2.13 stays immutable; no public pin, release,
   or activation is in scope.
5. **Runtime: final retirement.** After the consumer proofs and unchanged
   three legacy positives requalified as native equivalence, merge the
   code-only RT07 candidate. Only that actual merge permits a later ledger
   transition from `OPEN` to `DELETED`.

Required coordinated order: **Agent current consumer/source -> App normal014
consumer adoption -> Runtime ordinary014 requalification -> Runtime RT07
code-only retirement**. The order keeps the old writer available until its
consumers have moved.

## Lifecycle and future contract item

Runtime catalog archive/unarchive remains a catalog lifecycle operation.
Historical flat-film recovery is the native `timeline.restore` command; it is
not an excuse to revive the old RT07 route or to classify stale `7b3` as
current.

The advertised `/v1/attempts/{attempt_id}/publish-timeline-render` operation,
OpenAPI entry, and generated Python client cleanup remain a separate future
contract artifact/version item after caller migration. They must not be
silently removed or rewritten as part of the RT07 code-only retirement, and
must not mutate the ordinary014 producer or its 75-entry artifact.
