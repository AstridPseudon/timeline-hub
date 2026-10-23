# P4 service execution gain handoff

Updated only the existing agent p4-v2-http-nodes row in:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf

The row now executes against the kept checkout:

~~~text
/home/user/work/wt/rt-pin-1cf5562f
HEAD  1cf5562f8d2eddb6ee26cbec5155f94098e057b8
tree  f74b016ea837f8148db4a602c972073a226ed177
status clean
~~~

Receipt: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/checkout-runtime-1cf5562f8d2eddb6ee26cbec5155f94098e057b8 (detached exact SHA, KEEP).

The row adds exact SHA/tree/clean checks and a bounded pre-pytest Python probe. Runtime package imports must originate under the 1cf checkout. The normal vendored client imports must originate under the Agent worktree, preserving the frozen 34e source/client boundary. The original pytest suffix is unchanged:

~~~text
/home/user/work/venv-app2-native/bin/python -m pytest -q -m integration
~~~

Before/after evidence:

~~~text
config bytes: 89540 -> 90710
config SHA-256: 8e2dac65bce1aa345c156ff2cce370ccdb4bd60bfac88ea73fd91cd8ebc453d -> 64f7942bb3faec060ae3e9f34c753f3c84d8afc30269d3a1a3765a1c172e8b25
target row bytes: 209 -> 1379
target row SHA-256: d3be1fa1385fb003fe395ec84704f10ef14d6e5feb9b6340fa5ac60c4160ac96 -> 2ff0bb94d75defeee99267b073369406f3069726728704ea135453b4234f7cc0
outside-row bytes: 89331 -> 89331
outside-row SHA-256: d9591c5ece20defe0c0e77dbb1f61169dcd221413c55bfa100c634c79397fa5e3 -> d9591c5ece20defe0c0e77dbb1f61169dcd221413c55bfa100c634c79397fa5e3
~~~

Checks passed:

~~~text
bash -n of the parsed target row
exact ten-note read-only collection: 1 test collected
runtime.lock.json against frozen producer 34eac004: ok / matches producer manifest
git diff --check
~~~

The rerun test was not present in this worktree, so the required alternative collection was the exact ten-note node only. No HTTP/body/socket/service/browser/full/build run occurred. No original P4 body was requested; manager must retain the Runtime independent/integrated proof and independent row-review gate before requesting it.

Next: independent Luna review of this row, then manager request of the exact original ten-note node followed by a separate rerun request.
