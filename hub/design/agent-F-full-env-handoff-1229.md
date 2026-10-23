# Agent F full environment handoff — current V3 / Runtime3b

Date: 2026-10-23 UTC  
Worker: `agt-F-full-env-handoff-1229`  
Status: **READY FOR INDEPENDENT REVIEW; FARM FULL RUN NOT REQUESTED HERE**

## Why this handoff exists

Farm's plain `full` request `agent-full-1023121504-10362` exited 4 after zero
tests: `tests/conftest.py` could not import `runtime_protocol`. The Farm also
reported that its snapshot did not contain the named `d09-current-v3-1113`
row. The local `tests/suites.conf` did contain that old D09 row, but it bound
the installed f1012 environment and was not a valid current3b full-suite
recipe.

I added exactly one row to the local allow-list, preserving every byte outside
that insertion:

```text
agent full-current-v3-1229 <the exact env-bound command in this row>
```

The production handoff is therefore:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-F-full-env-handoff-1229 full-current-v3-1229
```

Farm must use the command stored by the `full-current-v3-1229` row; it must not
reconstruct the environment from the old `full` or `d09-current-v3-1113` rows.

## Exact environment recipe

The row uses `env -i` with these bindings:

```text
HOME=/root
LANG=C.UTF-8
LC_ALL=C.UTF-8
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-3b926efa"
PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/bin:/bin
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules
ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages
```

There is deliberately no `PYTHONNOUSERSITE` assignment. The pre-body shell
gate checks the Node executable, Python executable, Runtime protocol directory,
profile `node_modules`, and schema site-packages directory with literal paths.
Only after those checks pass does it `exec` the Python process.

The single Python process then:

1. imports `astrid`, `runtime_protocol`, `astrid_runtime_client`, Agent's
   timeline schema, shared `banodoco_timeline_schema`, `pytest`, and `xdist`;
2. asserts exact module origins, Node `v20.19.4`, `PYTHONNOUSERSITE is None`,
   profile lock/archive hashes, and installed Composition version `0.0.14`;
3. prints those origins/hashes and the D09 fixture path; and
4. invokes `pytest.main(["-q", "-n", "3"])`.

Thus Runtime source and module origin checks happen in the same process that
executes the full suite. The exact command is the complete line for
`agent full-current-v3-1229` in:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf
```

## Availability and identity assumptions

| Item | Required identity / availability |
| --- | --- |
| Agent input | Current handoff worktree `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`, tree `ff6c46d0b5ba420e3fb9e912e5a30c7a9a41e27b` |
| Runtime checkout | `/home/user/work/wt/rt-pin-3b926efa`, clean, commit `3b926efab2eed122d374540baee297d4cdcec62a`, tree `b794170504544b259781e50d7ca4d61b6729e67c` |
| Runtime import | `/home/user/work/wt/rt-pin-3b926efa/runtime_protocol/__init__.py`, SHA-256 `4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2` |
| Python/pytest | `/home/user/work/venv-agent/bin/python`, Python 3.13.16, pytest 9.0.2, xdist 3.8.0 |
| Node | `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, `v20.19.4` |
| Composition profile | `/home/user/work/runtimes/agent-remotion-v3-819acf-1110`, installed `@banodoco/timeline-composition` `0.0.14` |
| Profile lock | SHA-256 `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d` |
| Selected Composition archive | `artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`, SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` |
| Fixture | `tests/integrations/test_d09_managed_scene_only.py` in the Agent snapshot |
| Optional isolation | `/home/user/work/venv-agent-child-f1012-installed` remains available as prior custody evidence only; it is not the current3b full executor |

The stale `/home/user/work/runtimes/agent-remotion-composition14-255b6856`
profile and old Runtime `/home/user/work/wt/rt-pin-95bd3c5f` are explicitly
excluded. The exact installed 0.0.14 archive is selected by the profile's
`@banodoco/timeline-composition` dependency; the unrelated 0.0.14-named stale
archive is not selected.

## Bounded evidence

Checks performed without test bodies:

- Suite row count: exactly one `agent full-current-v3-1229` row.
- Extracted command: `bash -n` passed.
- Same-process import/profile check and positive full collection: **exit 0**;
  `16913/17598 tests collected (685 deselected) in 44.96s`.
- Missing Runtime protocol path: the pre-body literal path gate returned
  `rc=1` with zero output; the Python process and pytest did not start.

No full body run, HTTP, browser, live socket, or duplicate D09 execution was
performed here. The full suite and final build remain Farm-owned.

The independent D09 evidence in `agent-R2-D09-integrated-1121.md` and
`agent-F-D09-review-1113.md` remains separate. It does not authorize changing
the current3b full tuple, weakening the `PYTHONNOUSERSITE` guard, or reusing
the stale profile.

## Scope and contract preservation

No Agent product files or tests were changed. No Runtime/App/Composition
worktree was changed. No shared installation, dependency graph, pin, guard,
generated file, schema, or source was changed. The full v2 contract pair and
its required request/reply surfaces (base, commands, label, steps/patch,
reads/ordinals, merge, idempotency, dry-run, source/rationale/group_id,
accepted/merged/conflict/invalid replies and complete effects/history/undo
data) were not touched. No alternate executor, invented reads, skips/xfails,
subprocess alias, Git mutation, or approval workaround was introduced.

The requested independent review must occur before Farm uses this row. No
integration merge is implied; this remains G5 draft evidence only.
