# Independent semantic disposition

Verdict: PASS for the recorded partition. The 17 entries below are genuine
owner decisions, not routine applications of the existing upstream behavior or
the C0 Runtime-only-writer principle. Each combines overlapping source changes
whose order, authorization, identity, cleanup, diagnostics, output identity, or
test contract can change observable behavior. No semantic hunk was exported.

The `changed in both` marker is only a file-level merge-tree status. The exact
22 conflict hunks are the crosswalk below. The separate upstream-only
`runtime_protocol/process_control.py` addition is a clean `added in remote`
record and is not one of the 22.

## Actual unresolved owner decisions

1. `runtime_protocol/daemon.py` `@@ -243,7 +244,14 @@`: choose whether process-control configuration/probe/announcement precedes
   provider loading and registration. This affects startup refusal, cleanup,
   and the C0 writer admission path.
2. `runtime_protocol/door.py` `@@ -139,7 +139,7 @@`: decide whether reserving ACP id `astrid` preserves the intended API-key
   route without changing connection-id authorization.
3. `runtime_protocol/door.py` `@@ -154,6 +154,7 @@`: combine upstream project selection with Runtime timeline/commit/history
   routes and verify their scopes and matcher behavior.
4. `runtime_protocol/door.py` `@@ -199,0 +200,8 @@`: decide whether forwarding the Astrid API key preserves the product-token/
   ACP boundary and intended caller.
5. `runtime_protocol/door.py` `@@ -236,0 +239,7 @@`: decide exact-route reservation versus parameterized fallback for forbidden
   methods, including the new commit routes.
6. `runtime_protocol/platform.py` `@@ -978,7 +981,15 @@`: decide whether the upstream denied-`killpg` member walk remains identity
   safe after ours changes Linux birth IDs to boot-bound values.
7. `runtime_protocol/platform.py` `@@ -1060,8 +1071,192 @@`: choose the authoritative process-control mode and whether sandbox PID
   fallback/member-walk can be admitted without weakening security.
8. `runtime_protocol/platform.py` `@@ -1110,7 +1305,13 @@`: decide the combined boot-bound identity, pidfd-wrapper compatibility,
   ENOSYS fallback, race, and error contract.
9. `runtime_protocol/server.py` `@@ -421,7 +422,12 @@`: decide whether formatted traceback and request method/path diagnostics may
   be emitted while retaining C0 public error envelopes and redaction.
10. `runtime_protocol/service.py` `@@ -7955,9 +7955,11 @@`: decide whether settled output objects use the physical output filename or
    logical port name as `original_name`, including existing media/generated-output callers.
11. `tests/conftest.py` `@@ -14,6 +14,38 @@`: decide whether the process-control option/autouse override is isolated
    across provider and Runtime tests.
12. `tests/conftest.py` `@@ -76,7 +108,9 @@`: decide whether denied group cleanup may swallow `PermissionError` or must
    retain existing leak reporting and cleanup ownership.
13. `tests/conftest.py` `@@ -85,7 +119,7 @@`: decide the authoritative cleanup result when SIGKILL/group cleanup is
    denied: preserve leak diagnostics or treat denial as terminal.
14. `tests/lanes.py` `@@ -32,6 +32,7 @@`: combine `needs_real_pidfd` selection with the existing lane registry and
    ensure only the sandbox CI job deselects it.
15. `tests/lanes.py` `@@ -283,6 +284,10 @@`: add the Linux O_PATH declaration without changing current unit-lane and
    declared-skip semantics.
16. `tests/test_door_routes.py` `@@ -37,6 +37,7 @@`: combine upstream PUT project selection with ours' product-call and commit
    route assertions without weakening auth expectations.
17. `tests/test_door_routes.py` `@@ -110,0 +111,2 @@`: retain upstream forbidden selection methods after route-list combination.

## Non-semantic entries and boundaries

- `.github/workflows/ci.yml`: textual composition only; the result retains the
  upstream `sandbox-process-control` job and ours' Windows matrix/worker-handoff
  family.
- `docs/runtime-portability-testing.md`: documentation-only composition.
- `runtime_protocol/daemon.py` import and `runtime_protocol/server.py` traceback
  import: context-only dependencies of the semantic hunks, not standalone
  resolutions.
- `runtime_protocol/platform.py` module documentation: textual only.
- D130 WAL recovery is outside this ten-file scope and was not classified or
  changed.

The questions are intentionally provisional. They are source evidence for the
future upstream join/patch-export and do not claim a merged or final Runtime.
