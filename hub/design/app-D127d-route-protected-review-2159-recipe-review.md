# D127d descriptor/recipe/CLI review

The new descriptor is recognized by the existing D66/D73 machinery. It keeps
the exact original file, count 1, grep selector, and `retainRuntimeLogs: true`
from `p2-element`, and adds only `verificationOnly: true`.

`playwrightLaunchEnv()` sets `D66_ELEMENT_VERIFICATION_ONLY=1` only for the
normal `p2-element-verify` stage; readiness clears it, and pairing the
verification descriptor with another suite name throws. `main()` independently
requires agreement between the suite and this explicit env arm. A no-env
`p2-element-verify --submit` probe therefore exits before `submit()`, which is
the intended fail-closed invalid combination. The registered D73 preflight and
normal recipes explicitly set the env for the valid route.

The safe recipe probe used four synthetic complete SHA/tree pairs and absolute
checkout paths. It confirmed 12 pin assignments (SHA, tree, checkout for all
four roles), the verification selector, and an empty capture watchdog. With
the reviewed helper path and SHA supplied, the recipe also carried both helper
identity variables; the service-side `main()` retains its default helper
identity validation. No old manifest or mismatch waiver is used.

The harness verification arm creates the existing private stream directory,
but does not allocate a phase-capture sink. `runtimeEnv()` gives each spawned
Runtime child a fresh env with all measurement variables explicitly undefined,
including inherited activation/sink/helper/hash/watchdog/log/phase values and
the verification selector. It also omits the phase bootstrap directory from
`PYTHONPATH`. Teardown retains only ordinary private stdout/stderr streams.

The D127d targeted test exercises two spawned offline Runtime incarnations and
asserts their child envs plus private stream modes/bytes. It is not a Runtime
candidate or browser qualification.
