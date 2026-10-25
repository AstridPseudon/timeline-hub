# F/D134 progress

- Reviewed the settled plan, source-preparation evidence, original core-command
  design, and actual 0811/2234 control provenance before execution.
- Confirmed the frozen tuple and source conservation for Agent `a4e016b6`,
  Runtime `5e9ad1c6`, App `d8a1cd40`, and Composition `635f4de0`.
- Used the supported normal D73 maker recipe to generate a fresh positive
  manifest from the verified source/profile/environment bindings. Created its
  poison copy with only `agent_sha=000...000`.
- Independently verified the existing positive stub full hash and ran only the
  two authorized DRY controls with fresh counters.
- Positive: launcher preflight 0, stub exit 17, exactly one call.
- Poison: deliberate Agent SHA guard exit 1, zero calls.
- No full body, collection, request-test, package acquisition, child build,
  profile build, guard bypass, alternate environment, production Store, or
  suite-row mutation was performed. This remains preflight evidence only.

- Superseding MAIN19:24Z / AgentINBOX2026-10-25T19:07:26Z START NOW was
  consumed with `OPEN`, `NOT_GREEN`, and `AUTHORIZED` bindings. The first
  normal-service submission `agent-agent-core-full-1025191109-29996` stopped
  before launcher/body with exit 126 because the recipe file was not
  executable; no pytest collection or body ran.
- Corrected only the invocation to `bash` the byte-identical recipe. The sole
  measurement service is now submitted as
  `agent-agent-core-full-1025191128-18455` at 2026-10-25T19:11:28Z via the
  normal `integration:agent` route. Fresh admission was 6639108096 bytes,
  above the 4700000000-byte named-suite floor; no other heavy body was live.
- The service reached terminal at 2026-10-25T19:34:51Z, exit 1, after one
  normal launcher preflight exit 0 and one unfiltered body. Measured summary:
  8926 passed, 190 failed, 180 errors, 86 warnings, and 173 subtests passed
  in 1379.05s. XML digest and exact-node comparisons are in `outcomes.json`;
  `core_open_n`/`reg_open_n` remain UNKNOWN pending independent review.
