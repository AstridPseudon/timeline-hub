# App normal014 owner-ready triage

## Verdict

`app-normal014-integration-e2e-gate5-1020174558-6901` reached the browser with
the exact normal014 source tuple after the private Vite/bin repair and a
passing hosted build. It failed before the first gesture while waiting 90s for
a new durable command owner (`received {ready:false}`, expected `{ready:true}`).

This is not evidence of a Runtime owner bug, lock collision, handshake
mismatch, stale session, or bad fixture: the App never created its command
session, so none of those downstream guards ran.

## First guard and root cause

`useTimelineSave.ts:100-103` passes
`initialReadReady: commit.data !== null && initialRecoveryChecked` to the
command-session hook. `useTimelineCommandSession.ts:44-45` returns before
session creation while it is false. The durable owner/outbox therefore remains
absent, exactly matching the central predicate failure.

The source trace identifies a normal-path race introduced by
`b77ccaf2dbf2da85d7ba5828e5114627325cdea6` (`fix(timeline): await verified
initial editing readiness`). The initial draft check captures the recovery
generation at `useTimelineSave.ts:183`; canonical reload calls
`onCanonicalReloadStart` at `useTimelinePersistence.ts:1306-1311`, incrementing
that generation. If reload occurs while the draft read is pending, the
`.finally()` guard at `useTimelineSave.ts:243-247` refuses to set
`initialRecoveryChecked`. The effect has already marked the scope checked at
line 178 and will not retry, leaving the editor permanently behind the command
bootstrap gate. The run log has no internal React-state trace, so the specific
generation mismatch is a diagnosis from the complete source/evidence trace,
not a directly logged browser exception.

## Evidence

- Hosted build passed (`npm run build:hosted`, 5,569 modules, 1m18s).
- Artifact/lock checks passed: 75 manifest entries, Runtime `0.2.14`, artifact
  `f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`, manifest
  `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
- Browser source tuple: App `d87e29a5ca4b91a3c06da21af4714815f1463acd`, Agent
  `3c4f6de4fa777323b3386c01c7266b619b86af6d`, Runtime
  `202074110717146fc7f08af2306a8dd7f695b0b1`; vendor/schema/wire checks passed.
- Historical current013 base (`0ea368432267f1f3e712c91822d6ea4961d40e78`,
  tree `8d8a10b057ed31fed69517e18a23b8ec3811447a`) predates b77, and the
  corrected unique-C central lane passed 3/3 product tests. Existing parent
  acceptance remains unchanged.

Full central evidence:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-normal014-integration-e2e-gate5-1020174558-6901/log.txt`.

## Handoff

App owner: make invalidated initial recovery checks retryable for the current
scope/generation, retaining the existing cancellation and recovery safety
guards. Add a focused initial-draft-read/canonical-reload regression. After
that source fix, rerun the exact normal014 Gate 5 central lane once. No fixture
repair, public pin change, guard/timeout weakening, activation, or release is
justified by this run. No central diagnostic rerun was requested because the
first guard and owning source delta are already identified.

Local focused validation: the six existing App hook suites passed, 75 tests
total. No local browser, localhost/socket, or full suite was run.
