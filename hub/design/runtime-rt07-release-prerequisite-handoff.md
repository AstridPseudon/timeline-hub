# RT07 / ordinary014 release-prerequisite handoff

Date: 2026-10-20. This is a reviewable merge handoff only. It grants no
permission to merge, release, pin, activate, or publish, and it does not mark
RT07 deleted.

## Exact current identities

- Current Runtime integration is `b88a56feb2e1879455b9f1eb2403e171aa125f3c`,
  tree `da4153287f1513ca662757440127ed5ab6f1cf7d`.
- RT07 code-only retirement candidate: Runtime commit
  `40e7dc7cd627c6c4e2bffb482926bb9b037f0143`, tree
  `a7c86e8514c1cc095635e1484b71c98928debe01`, parent
  `b88a56feb2e1879455b9f1eb2403e171aa125f3c`. It removes
  legacy publication writes while retaining authority parsing, replay-only
  reads, and the approved native mappings. It remains held and has not merged.
- The committed ordinary014 Runtime candidate is
  `fcf4c3d5e9444bf9e221d05aa8fa8d203fb27bd3`, tree
  `69abf4e2a8340d7d39a955d71d08afbf3a311a35`, parent
  `616d2111f35937f311330ffebc8610d21bf80f74`. It carries the owner-strict
  `cd0` boundary as a test-only change and has the exact three-case native
  result: **3 passed in 3.11s**. Its ordinary producer is
  `a0dca16975dfe8f5e762703b99d9791a16cf7`, tree
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`; raw schema
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
  artifact `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`;
  75-entry manifest digest
  `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
  It is unpublished and is not an adoption or release decision.
- Current86 is Runtime `86ce14f144a740d9002d8758f952bdb4324847d8`, tree
  `c3333a08dbb09d51ee4fedd8c7ec455775374315`. Its compatible ordinary014
  rollback descendant is `28ccd9507e0a37767914a5edb685675eb70e9202`, tree
  `2e336dbaf94898d6fa0eda4ca8360d8c2c02cf21`, parent
  `86ce14f144a740d9002d8758f952bdb4324847d8`. It retains
  current process/retention/auth code, the exact `a0`/`f021` artifacts, the
  `cd0` boundary, and the approved RT02 rollback/retry node. Its affected lane
  was **347 passed, 2 skipped, 3 xfailed, 3 failed, 3 errors**; failures/errors
  were outside the affected ordinary014 cases. It is not adoption evidence.
- Current Agent integration is `81873ccf270e1c099c9f76b86103ccf3c9275cf4`,
  tree `5164f267bb08eafc497ae19e081861eabec9bb67`. The 21:59 Agent ACK says
  that one ordinary014 descendant will be staged while preserving this source,
  the merged restore/read fixes, and immutable `a0`/`f021`. No descendant SHA
  was published in that ACK; do not invent one or relabel old `7b3` as current.

## Evidence already available

- Agent registered cohort `7012` is an exact historical proof on Agent
  `7b3e1205a374443c46bad6b18753ef146e1e42c6`, tree
  `7d807bc27b1b237de7138c13672d2fa814a22f3f`: **2 passed in 300.96s**.
  App2 Gate `58973` is the exact historical consumer proof on Agent
  `3c4f6de4fa777323b3386c01c7266b619b86af6d`, tree
  `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`: **1 passed in 32.4s**. These
  gates remain valid exact evidence and must not be rerun merely for staging;
  they do not authorize a pin or adoption.
- The corrected current86 full result `21387` is **5,540 passed, 7 inherited
  baseline failures, 18 skipped, 18 xfailed**, with no new assertion or storage
  failures. The earlier `8649` result remains environment-invalid because of
  storage-floor exhaustion. Neither is an all-green release gate.
- The earlier `202074110717146fc7f08af2306a8dd7f695b0b1` candidate is
  superseded; it is not the latest ordinary014 identity and is not a blocker.

## Only genuine remaining blockers

1. **Startup-stop/environment qualification.** Reviewed startup-stop source
   `9c53a985072d3b1171502722ac0074226cf6b2ed`, tree
   `da4153287f1513ca662757440127ed5ab6f1cf7d`, and one safe current full
   qualification remain pending. The environment-invalid `8649` run is not a
   product or release pass.
2. **Current consumer hold-clear.** The current-preserving Agent descendant
   must be staged and qualify the exact semantic capture hold-clear refusal
   that occurs before any Runtime request. This is Agent-owned; Runtime must
   not add a projection or hold override. The old `7b3` missing
   `TimelineSession.restore` failure is historical, not a current blocker,
   because the restore facade is already in current source.
3. **Exact coordinated adoption decision.** Once the current source and
   environment boundary are settled, Agent, App2, and Runtime need one
   coordinated decision on the exact ordinary014 tuple (`fcf4c3d5`/`a0`/`f021`
   and its current-compatible descendant). This handoff does not authorize a
   pin, release, activation, or merge.

No renderer, browser, or unchanged registered-render positive is outstanding
for rerun. The recorded `7012` and `58973` evidence remains attached to its
exact historical tuples. RT07 code-only `40e7` remains held; only a later
actual merge can change the ledger status.

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
