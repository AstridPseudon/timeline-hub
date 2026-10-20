# App automatic-placement real-response triage

## Scope

This worker used the frozen Agent 8130, Runtime 2c4, and Composition public12
tuple. The gate uses the existing `GenericPackHost`, the normal Runtime
operation, and the real App task/placement path. It does not add a wire,
authority, capability guess, stubbed compose, or polling subsystem.

## Findings and changes

- The harness had to register a canonical temporary generation pack through
  `GenericPackHost`. The pack is derived from the frozen generation action and
  only replaces its invocation with a deterministic one-pixel command. It is
  registered and run through the normal Runtime API.
- The real capability discovery path took more than the App's 10-second compose
  deadline on this tuple. The App deadline is now 30 seconds, which is still a
  bounded request deadline and allows healthy normal discovery to complete.
- A blank anchor was not a valid placement for the seeded occurrence: the
  five-second child could only be appended after the existing V2 clip and would
  exceed the twelve-second occurrence. The valid existing Agent clip is now the
  explicit anchor; the assertion preserves the original approval and intent
  binding.
- The App automatic-capture command previously read each consumed clip as a
  whole object. Agent 8130's normal `_consume` contract reads exactly
  `at`, `at_ms`, `track`, `hold`, `from`, `to`, and `speed`. The App now emits
  those seven normal field reads, fixing Runtime's exact capture check without
  changing the wire or schema. The conformance hashes were updated for this
  intentional request change.
- The harness now pauses task admission until the durable placement continuation
  is observable, so approval/intent-before-admission is tested against the real
  request ordering. It also waits for the registered task and managed output
  before the lost-ack phase.

## Remaining blocker

The first lost-ack commit reaches canonical placement after the field-read fix.
After the next Runtime/Vite restart and reload, however, clicking the persisted
recovery control never produces a second operation commit request. The retained
outbox remains pending with outcome `retry` and error `Failed to fetch`.
The operation trace shows the new operation acquisition and health/handshake/
realm negotiation, but no recovery `/commit`; repeated runs show the same
boundary. This is an App session/operation binding lifecycle failure after
reload, not a Runtime/Agent target, profile, schema, estimate, identity, or
compose failure. Fixing it requires tracing the session host rebinding and its
recovery callback; adding another click, timer, or speculative poller would not
be evidence-based.

Consequently the final retry, reload, guarded undo, and 0-legacy assertions are
not certified by the central gate yet. The original assertions remain intact.
