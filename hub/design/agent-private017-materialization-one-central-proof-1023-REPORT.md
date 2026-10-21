# Agent private017 materialization central-proof preflight

Date: 2026-10-21

## Result

The authorized 1014 test commit is clean and passes the aggregate preflight.
No central integration body was run because the configured test service has no
suite that can satisfy all three required constraints at once: Runtime 42a,
explicit integration selection, and only the new placement node.

## Exact source and pin

- Agent HEAD: `bc025570899739418168077083c46e8d9dca239c`
- Agent tree: `188077bcaccae136aa3cf429d0b32ac3098b0639`
- Base 6c: `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`
- Runtime: `/home/user/work/wt/rt-pin-42a7203f`
- Runtime commit/tree: `42a7203f49bb89f299ec854cfbf2b1444e815a7c` /
  `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`

The only diff from 6c is the authorized
`tests/editing_conformance/test_commit_runtime_identity.py` addition. All
other source bytes are unchanged. The Runtime checkout is clean.

## Preflight evidence

Passed:

- `runtime.lock.json` source commit = Runtime 42a and producer =
  `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
- All 15 locked Agent artifact hashes match.
- Runtime `contract/artifacts.json`: 76/76 artifact hashes match; producer is
  `astrid-runtime` with version `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
- Agent and Runtime EditCommand schema bytes both hash to
  `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`.
- Normal vendored client imports from the Agent worktree, Runtime imports from
  the explicit 42a checkout, and client `CONTRACT_VERSION` is `0.2.17`.
- The public ordinary/occupancy floor remains present; source-byte equality
  against 6c outside the new test also protects it.
- `pytest --collect-only -m integration` explicitly collected exactly one
  target node:
  `tests/editing_conformance/test_commit_runtime_identity.py::test_fresh_shared_placement_materializes_own_slot_reload_inverse_and_exact_retry[fresh]`.
- `ruff check tests/editing_conformance/test_commit_runtime_identity.py` passed.
- `git diff --check 6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79 HEAD` passed.

Static target guards confirm the module-level `integration` marker, explicit
`use_runtime()`, `RuntimeService`, and
`load_timeline_commit_provider("astrid")` registration. There is no
`PreparedProvider`, fake, mock, or stub provider in the target file. The body
was not executed locally.

## Central-suite blocker

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`
has no private017 or Runtime-42a entry. The closest configured suite is:

```text
agent projection-occupancy-integration env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ... -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/editing_conformance/test_commit_runtime_identity.py
```

It selects the wrong Runtime (`/home/user/work/runtime`, not 42a) and runs
the whole M1 and identity files. The generic `agent targeted` suite can take
the exact node, but defaults to `not integration` and has no Runtime checkout
environment. Requesting either would not be valid evidence, so no central
request was submitted and no retry/body was attempted.

The next step is for the orchestrator/test-service owner to register one
named light suite whose command pins
`ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-42a7203f`, sets
`PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-42a7203f"`, uses the normal
vendored `0.2.17` client, selects `-m integration`, and names only the target
node above. Then run that one suite once; preserve the first failure and do
not retry automatically.
