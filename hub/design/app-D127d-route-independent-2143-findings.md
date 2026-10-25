# D127d independent review

## Verdict

- Scope: `PASS`. This review stayed read-only and inspected the committed App
  head plus the named Runtime helper/contract source. No source, test,
  generated file, pin, checkout, service, browser, socket, or product request
  was run or changed.
- Custody: `PASS`. App HEAD/tree are the recorded D127d normal tuple
  (`b5c9eadfa1950f46feac50d7d6a89c47f27f4881` /
  `8e10af0976b012205f27a18a432c750a27de0725`); the four previously recorded
  App source blob/hash identities match. Runtime COST-CANDIDATE remains
  `PENDING`; no candidate receipt is claimed.
- Route authorization: `FAIL` for a normal no-hooks candidate body. The
  existing `p2-element` route retains Runtime streams and, for an authoring
  run with its retained-log directory, currently allocates a phase-capture
  sink and starts the helper. There is no source-supported normal arm that
  keeps the route but disables that measurement.
- Acceptance: `NOTRUN`; this packet grants no functional credit.

## What the source actually does

1. `scripts/testing/d66-plain-stack.mjs` marks `p2-element` as one selected
   body with `retainRuntimeLogs: true`. Its normal launch environment sets a
   private Runtime-log directory and launch ordinal. Its normal source path
   resolves and pins the existing helper for retained suites.
2. `tests/e2e/local/support/harness.ts` creates the retained directory, and
   `startRuntime()` passes a capture sink when authoring is enabled. The
   Runtime child receives the explicit capture environment. Teardown writes
   the child stdout/stderr into the same private directory. Thus plain stderr
   retention and phase measurement are coupled in the current harness, but
   they are not the same behavior.
3. `scripts/testing/sitecustomize.py` only loads the helper for the explicit
   capture environment and the Runtime CLI `start` argv seam. The Runtime
   helper's `start()` installs process/thread tracing and a sampler; its
   handler boundary arms request-scoped cProfile, and its dispatch lifecycle
   owns watchdog captures.
4. `p2-runtime-phase-bootstrap.test.ts` positively accepts the normal and
   reviewed helper identities and negatively rejects wrong helper hash/path.
   That is a custody/provenance guard, not a disabled-helper arm. The
   `d66-plain-stack` environment tests cover retained suites and non-retained
   readiness/other suites, not a normal retained `p2-element` run with the
   helper disabled.

## A2/A3/P2 and C0 sections 1-5/7

The committed production caller is `useTimelineSave` creating
`createLocalSaveSession`; this is the path used by element saves, popup media
saves and registerAsset persistence. The separate `createTimelineCommandSession`
also constructs the same canonical commit route, but it is not the production
caller found by the source search. The production local-save builder:

- bases each request on the exact revision/publication pair;
- persists original commands/guards and supplies label, steps, source `app`,
  and `dry_run: false`;
- carries full-v2 merge/read metadata when the generated contract is accepted;
- preserves ordered `doc.patch` changes and previous values from the verified
  closure, with omitted-read conservative fallback;
- chains dependent outbox entries after the predecessor and advances their
  ready base only from the accepted Runtime head;
- retains the exact pending request/key for uncertain outcomes and marks a
  refused predecessor/dependent suffix for explicit resolution;
- sends the mutation with `Idempotency-Key`, decodes accepted/merged replies
  (while retaining compatibility with historical `rebased`), and refuses a
  preview as an accepted mutation;
- emits whole-commit `timeline.inverse` through the same commit/outbox path.

The source is consistent with C0 sections 1-5 and 7 at the App boundary.
Runtime-side closure binding, conflict detection, authoritative effect
attribution, receipt authentication, and history persistence remain Runtime
authority and are not functionally qualified by this static review.

## Corrected finite recommendation

Keep the candidate `PENDING`. After Runtime independently qualifies the cost
candidate and provides the immutable source receipt, make one bounded harness
change at `tests/e2e/local/support/harness.ts`:

- leave the existing private `runtimeLogDirectory` and teardown stream writes
  intact so ordinary stderr remains available;
- for this one candidate route, pass no `captureSink` to `runtimeEnv()` and
  therefore do not set the explicit phase-capture environment;
- retain the existing helper identity and fail-closed positive/negative guards;
- add only the narrow static/fixture assertions needed to prove that the
  candidate authoring launch has no observer environment while plain stream
  retention remains enabled.

Then the manager may use the existing one-body D66 `p2-element` route with
the original five-second assertion, canonical readback/history/reload/guarded
Undo checks, and the D130 SWAP/WAL/recovery/full-tour hold. No profiling,
sampling, helper trace, preflight, bootstrap, service, submission, browser, or
body is authorized by this packet.
