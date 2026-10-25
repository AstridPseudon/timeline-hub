# D73 / D139 independent review findings

## Verdict: FAIL

The current-source identity and historical conservation checks pass, but the
production admission boundary required by D73/D139 does not.

1. **BLOCKING — production manifest guard is absent.** The candidate rows in
   `ops-d73-exact-nodes/suites.conf` invoke the unchanged pinned launcher
   directly. The central `test-run` parser only extracts the row and appends
   selectors; it does not call `check.py`. `check.py` therefore remains a
   source-check-only guard.

   The launcher accepts duplicate keys because its associative-array parser
   overwrites the earlier value. It also creates the manifest/request/runmanifest
   artifacts before executing preflight. A bounded private invocation of the
   actual launcher confirmed that a duplicate `format` key returned 0 and
   created all eight launcher artifacts. A second bounded invocation with a
   preflight command forced to exit 9 still created five artifacts.

2. **BLOCKING — refusal controls are not production controls.** In
   `test_recipe.py`, duplicate, malformed, wrong-source, and wrong-lock cases
   are parsed in memory and then checked against an output path that was never
   passed to the launcher. Only the separate source-SHA poison case invokes the
   parsed command. These tests cannot prove zero launches/artifacts for the
   named-row production route.

The exact four-plus-one selectors, marker names, `run --` argv, per-ID junit
binding, current f103 lock selection, and C0 field conservation were verified.
The protected launcher, selected4 test, fork1 test, focused launcher-control
test, and `tests/helpers/runtime.py` are byte-identical to 2eca. Runtime lock
canonical file bytes remain identical and only its source commit is retargeted
to f103. No historical receipt or identity was retargeted.

## Separate receiving status: NOT_READY

Receiving is independently `NOT_READY`, not a source PASS:

- current Agent and Runtime checkout receipts are not supplied;
- no rendered receipt-backed manifest exists;
- App/Composition receipt-derived identities and environment/schema/profile
  inputs are absent;
- neither d73-f103 row is installed in the central registry;
- no fresh per-ID XML/raw logs or submit/end disk witnesses exist;
- no real interpreter import, preflight, product body, or central request ran.

Historical 2eca/ab1e qualification remains preserved as historical evidence.
