# Runtime semantic questions

Classification is provisional and source-only. The exact tuple is base
`d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`, ours
`e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9`, upstream
`dbcdb97c50afc72bd5e2599cb7ead0fe56bc7c4f`. The questions below are the
17 semantic hunks from the 22-hunk Runtime crosswalk. They must be answered
by the owning Runtime lead during the future upstream join; this worker did
not choose a product resolution.

## `runtime_protocol/daemon.py`

- `@@ -243,7 +244,14 @@`: ours loads and registers the selected timeline-commit provider during
  `RuntimeDaemon._start`; upstream configures process-control policy, probes
  signalling, and announces it before constructing the service. Decide the
  order and failure/cleanup behavior. The choice affects admission of the
  C0 Runtime-only writer and whether a provider import can occur before the
  process-control policy is fixed.

## `runtime_protocol/door.py`

- `@@ -139,7 +139,7 @@`: upstream reserves the literal ACP id `astrid`; decide whether that
  reservation is authoritative for `/acp/astrid/api-key` without changing
  connection-id authorization.
- `@@ -154,6 +154,7 @@`: upstream adds `PUT /v1/projects/selection`; ours adds POST timeline,
  commit, and verified-read routes in the same route table. Confirm the
  combined route set and `projects:write`/`projects:read` scope behavior.
- `@@ -199,0 +200,8 @@`: upstream forwards the Astrid API-key route to the local chat service.
  Confirm the product-token/ACP boundary and intended caller before exposing
  it through the browser door.
- `@@ -236,0 +239,7 @@`: upstream makes exact routes reserve their path before parameterized
  matching. Confirm that disallowed methods cannot fall through to an id
  route, including the new timeline commit routes, while preserving C0 auth.

## `runtime_protocol/platform.py`

- `@@ -978,7 +981,15 @@`: upstream falls back from denied `killpg` to an identity-checked member
  walk in sandbox mode; ours changes Linux birth ids to boot-bound values.
  Decide whether the fallback preserves the existing process identity and
  security contract.
- `@@ -1060,8 +1071,192 @@`: upstream adds strict/sandbox process-control configuration, probing,
  PID fallback, and member walking. Decide whether the sandbox mode and its
  race/error contract are admitted; this is process custody behavior, not a
  textual merge.
- `@@ -1110,7 +1305,13 @@`: upstream permits an ENOSYS PID fallback in `signal_process`; ours
  adds narrow-wrapper compatibility to `pidfd_open` and boot-bound identity.
  Decide the accepted identity/race behavior and error mapping.

## `runtime_protocol/server.py`

- `@@ -421,7 +422,12 @@`: upstream logs formatted traceback, request method, and route to stderr
  for unexpected errors; ours owns strict JSON commit/restore parsing,
  idempotency, auth, and C0 reply behavior in this module. Decide whether
  this diagnostic is allowed under the redaction/security contract and how
  it interacts with commit error responses.

## `runtime_protocol/service.py`

- `@@ -7955,9 +7955,11 @@`: upstream stores the settled output `filename` as `objects.original_name`;
  ours retains the port/logical `name`. Decide which existing managed-output,
  media-list, and generated-output callers are authoritative.

## Test harness and route assertions

- `tests/conftest.py @@ -14,6 +14,38 @@`: upstream's sandbox fixture monkey-patches
  `process_control.configure_from`; ours adds stage-environment setup. Decide
  whether the override is safe and isolated across provider/runtime tests.
- `tests/conftest.py @@ -76,7 +108,9 @@` and `@@ -85,7 +119,7 @@`: upstream
  swallows `PermissionError` during group cleanup; decide whether ours's leak
  reporting and cleanup ownership remain required under sandbox denial.
- `tests/lanes.py @@ -32,6 +32,7 @@`: upstream adds `needs_real_pidfd` selection semantics. Confirm that only
  sandbox CI deselects it and that the existing lane registry remains intact.
- `tests/lanes.py @@ -283,6 +284,10 @@`: upstream adds the Linux O_PATH lane marker. Confirm the declared-skip
  semantics without changing current unit coverage.
- `tests/test_door_routes.py @@ -37,6 +37,7 @@` and `@@ -110,0 +111,2 @@`:
  upstream adds selection-route allow/deny assertions. Confirm they coexist
  with ours's product-call route assertions and preserve auth/security tests.

The five textual/context hunks are recorded in `conflict-classes.json`. The
two complete non-code resolutions are the only exported patch. No semantic
question was silently resolved, and D130 WAL recovery is excluded.
