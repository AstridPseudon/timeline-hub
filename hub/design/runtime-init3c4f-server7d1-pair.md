# Runtime 7d1 / Agent 3c4f initializer qualification

Date: 2026-10-20 UTC

## Exact source tuple

This is a bounded consumer qualification, not a Runtime product change, pin,
release, or full-suite run.

| Role | Exact value |
| --- | --- |
| Runtime server | `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e` |
| Agent test source | `3c4f6de4fa777323b3386c01c7266b619b86af6d` |
| Runtime artifact producer | `a0dca16975dfe8f5e762703b99d9791a16cf7fd7` |
| Artifact version | `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0` |
| Runtime schema digest | `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59` |
| Artifact manifest entries | 75 |
| Agent source checkout | `/home/user/work/wt/agt-pin-3c4f6de4` |
| Runtime source checkout | `/home/user/work/wt/rt-m2-init3c4f-server7d1-pair` |

The qualification wrapper verifies both source HEADs and clean worktrees before
overriding the Agent test helper's Runtime selector. It compares all 75 server
artifact bytes with producer `a0dca169` and checks the Agent lock/schema tuple.
The producer identity remains `a0dca169`; `7d1` is only the server under test.

## Exact proof bounds

Only these four original initializer positives are run against normal Agent
SDK/provider code and the archived Runtime 7d1 source:

1. `tests/sdk/test_timeline_pristine_initialize_runtime.py::test_pristine_init_crash_resume_reload_undo_retry_and_redo`
2. `tests/sdk/test_timeline_pristine_initialize_runtime.py::test_pristine_init_real_provider_preserves_disjoint_opaque_row_after_reload_undo_redo`
3. `tests/editing_conformance/test_next_command_cohort_runtime.py::test_pristine_init_first_birth_reload_undo_and_missing_word_source[image]`
4. `tests/editing_conformance/test_next_command_cohort_runtime.py::test_pristine_init_first_birth_reload_undo_and_missing_word_source[video]`

The existing assertions remain unchanged: all four opaque values
`[null, false, [], {}]`, disjoint-row preservation, reload/restart, inverse and
redo, exact retry, pristine refusal, birth/reload, and missing-source refusal.
The broader 143-test cohort, 8+2 NativeSheet lane, and M1 lane are explicitly
outside this task and are not repeated here.

## Runner boundary

The central test service runs the approved
`tests/runtime-current-http-cli.sh` source-selection pattern. Its guards run
before the one helper override, and the Runtime is extracted privately under a
temporary directory. No shared dependency, cache, Runtime artifact, Agent
checkout, health/auth path, or product repository file is modified.

No full, pin, release, or browser qualification is included.

## Evidence

Central test-service request:

```text
rt-m2-init3c4f-server7d1-pair-current-http-cli-durability-1020165500-1047
```

Command:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  rt-m2-init3c4f-server7d1-pair current-http-cli-durability
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  rt-m2-init3c4f-server7d1-pair-current-http-cli-durability-1020165500-1047
```

Result: **4 passed in 4.58s**, central Runtime snapshot tree
`ac693097189637d3bd0fc3a39299d9b166758853`. The log records the 7d1 server
HEAD, 3c4f Agent HEAD, `a0dca169` producer, and the 75/75 artifact-byte proof.

Local wrapper syntax check:

```sh
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/runtime-current-http-cli.sh
```

Passed. The temporary Runtime archive was removed by the wrapper trap.
