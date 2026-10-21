# Report: actual-current Viewing census

## Outcome

The approved Viewing census boundary was remeasured against the actual home
`tl/integration` refs. The prior partial result was corrected: it used current
Composition `4788…` but stale Agent `01ee…` and App `a12…` snapshots.

The complete-current tuple is:

| scope | files | bytes | physical lines | nonblank lines |
| --- | ---: | ---: | ---: | ---: |
| exact Main baseline | 140 | 2,000,415 | 49,247 | 45,182 |
| actual current home integrations | 197 | 2,227,916 | 53,657 | 49,316 |
| current minus Main | +57 | +227,501 | +4,410 | +4,134 |

Detailed per-slice counts and source trees are in `CENSUS.md`.

## Current-head verification

- Composition `4788e107f183e0523a740b691a20eb8261d7183c`, tree
  `585e8c4784ee78ccbfbff4b6ce26f577b8eda05e`: matches the Viewing manager
  `STATUS.md` and both local and hub integration refs.
- Agent `57d6635616f2982b814cfcc059b670ea1a7c9f2c`, tree
  `0174fd49bd175a726a44542d1d6e31bca13c0f02`: matches the advertised current
  snapshot and both local and hub integration refs.
- App `813a85106ecb4abbaf224081abe6c33b8dab0df7`, tree
  `2a19a78bb1bdfb3fd779f568a1b513b094318982`: matches the latest home-parent
  evidence and both local and hub integration refs.
- Runtime `9d1c43c647301da48a6e86ad82e466b501bd2418`, tree
  `50e74e3243c5da4cf77b6e6cc76605fae8aeb649`, was verified but is outside the
  approved Viewing boundary and therefore omitted from the count.

No newer advertised head was missing from the available home mirrors. No
unmerged donor was counted. Older external test tuples were retained as test
inputs only and were not mistaken for current source.

Peer evidence read: Viewing manager `STATUS.md` at 2026-10-21 01:20 UTC;
Agent current-head evidence in
`design/runtime-gate7-current-integration-dryrun.md`; App current-parent
evidence in
`design/peer-app-to-app2-runtime-20261021T0104-parent-ready-nativeproof.md`.

## Evidence and limits

The existing read-only census manifest was reused. It enumerates committed Git
blobs, excludes generated/tests/untouched infrastructure under the approved
boundary, and reports physical plus nonblank lines. No product files were
changed. No tests, build, browser, renderer, install, full suite, or new
scanner was run, as required for this census-only task.

The canonical design document was not overwritten. Manager acceptance is still
required before publication there; this report makes no foundation-complete or
owner claim.

## Recommended next step

Manager review should accept or reject the complete-current proof, then publish
the accepted `CENSUS.md` values into the canonical design document if desired.
