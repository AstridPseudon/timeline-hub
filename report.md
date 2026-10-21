# Runtime M2 Gate 2 / Gate 4 current evidence

Date: 2026-10-21 UTC

This replaces the stale present-tense `public013` / “not integrated” wording.
The current Runtime integration is `b92d3e7a05eec65c142294ef4873edd059e9b31d`
(tree `6abc2f117391de8e7e35c0283f575a002199894d`), a descendant of the
immutable published Runtime 0.2.14 producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
(tree `d3a290b407fa61e6ab2d476f50c068073f70df00`). The publication was made
at `2026-10-21T02:51:25Z`; Agent adopted it in `091aa23ec83ea05ffd3b0115a640230d51c8c429`
(tree `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`) and App adopted the pin in
`3be3c116610c4ffdf019cba447464280fd7b8e06` (tree
`d030e4b8b41a1d5ec46de1c0c245111cafa7e98a`). The published protocol is
`0.2.14`; its producer/version digest is
`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
The App’s native `timeline.init`
initializer remains dormant; its separate create/init/restart/lost-response
qualification is not Gate 2 or Gate 4 evidence.

The current Runtime also contains the approved launcher merge `30413e3` and
the approved Speech merge `40708263`; both precede `b92d3e7`. The current
full result after those changes is `runtime-full-retained-owned-temp-integration-1021035028-28646`:
**6002 passed, 26 skipped, 15 xfailed, 12 warnings**, exit 0, on tree
`6abc2f117391de8e7e35c0283f575a002199894d`. This is current Runtime evidence,
not a new Gate 2/4 targeted run.

## Gate 2 — atomic acceptance

The seven affected final6ef cases remain valid only within their original
scope. On the exact Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb` /
Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` pair, the initial run
`rt-m2-gate2-final6ef-affected-http-crash-gate2-final6ef-affected-http-crash-1021004534-27309`
passed five cases and failed two final baseline assertions because copied
legacy `parent_composition.publish` receipts had expired and compacted to
`__runtime_idempotency_result_expired_v1`. The repair run
`rt-m2-gate2-final6ef-two-aged-fixtures-gate2-final6ef-two-aged-fixtures-1021005203-2115`
reran only those two selectors and passed both in 3.67 seconds.
Its fixture helper refreshed copied legacy receipt timestamps before startup;
it did not alter receipt bodies, accepted rows, history/events, or production
expiry guards. This is **5 + 2 historical evidence**, not a new 51-case run.

Git read comparison against Gate2 proof tree `36082cf3701de2328d47855bb4cd37455ef4cf57`
binds that evidence to current `b92d3e7` as follows:

- the Gate2 acceptance, execution, crash, routes, response-lock, generated-
  client, and parity source files are byte-identical to the proof snapshot;
- the selected integration bodies — disjoint rebase/conflict, concurrent
  disjoint-door moves, and lost-ack exact retry — have identical source hashes
  in current `b92d3e7` and the Gate2 proof tree;
- current `b92d3e7` adds the Gate4 admission body and an unrelated door-audit
  ordering repair, but neither changes the selected Gate2 bodies;
- the current full `runtime-full-retained-owned-temp-integration-1021035028-28646`
  covers the complete current Runtime Python tree,
  including these current acceptance and integration tests.

Therefore Gate 2 is standing evidence for the named atomic/rebase/crash/retry
scope. It is not a claim that the seven historical cases were rerun on b92,
and it does not claim App/native or four-product journey qualification.

## Gate 4 — door, transport, and generated clients

The named Gate4 result (proof tree
`183dbcf45a6b3a25f7437415df10100101ef8bbd`):
`rt-m2-gates2-and4-parallel-proof-track-gate4-door-integration-1020213206-10752`
remains **29 Python passed in 16.01 seconds;
61 TypeScript generated-client tests passed**, but its proof snapshot predates
the published 0.2.14 generated package. The following Python route/transport,
acceptance, generated-client, and parity test bodies are source-identical to
current `b92d3e7`: origin/auth/preflight, two-project isolation, response lock,
real commit admission, lost-ack retry, Python generated-client smoke/parity,
and recoverable-snapshot projection. The named suite paths and selectors still
exist and are executable; the current full covers their Runtime Python side.

The TypeScript generated inputs are not source-identical: current b92 changes
the package from 0.2.13 to 0.2.14 and updates `src/generated.ts`,
`src/contract-metadata.ts`, `src/timeline-commit-types.ts`,
`test/public-api.mts`, and the lockfile. The two runtime test modules are
unchanged, but that is insufficient to transfer the complete 61-test result
to the current generated package. Accordingly, the 61-test result is retained
as historical 0.2.13 evidence only; current 0.2.14 TypeScript generated-client
validation is an explicit remaining Gate4 gap. No replacement run was
requested in this worker.

Gate4 therefore has current Runtime/Python transport evidence within the
listed source scope, while the current generated TypeScript package still
needs one authorized targeted run before it can be called current. No new
transport behavior gap was inferred from the source diff.

## Checks and limits

The existing `gate2-atomic-integration` and `gate4-door-integration` entries in
`ORCH/tests/suites.conf` were statically checked: all referenced files exist
and all named pytest selectors resolve on current b92. No suite was submitted
or rerun. No full, browser, render, macOS, live-socket, or zero-test result is
claimed here. No Runtime product or test file was edited; this is a report-only
handoff.

