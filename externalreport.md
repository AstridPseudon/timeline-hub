# F environment final review 0901

## Result: PASS

The post-exit durability gate passes for the Agent `full` and `targeted`
service rows. Both rows use the durable private projection
`/home/user/work/agent-runtime-projection-0856/site-packages`; the old
`/tmp/w-5829dd9212/site-packages` path is absent. The projection contains
`runtime_protocol` as a symlink to the read-only current Runtime checkout
`/home/user/work/runtime/runtime_protocol`.

The actual service targeted run was submitted after the 0856 author exited:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  agt-F-env-final-review-0901 targeted --files \
  'tests/core/execution/test_generic_host_actions_v3.py::test_static_discover_admit_dry_run_and_owned_child')
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R" 30
```

Result: request `agt-F-env-final-review-0901-targeted-1023090117-4730`, Agent
tree `b7889d80cb59b97726a964312a377e794e582592`, exit 0, **1 passed in
10.90s**. The service command used the existing sanitized environment with
`PYTHONPATH="$PWD:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages"`,
`ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`, the existing Composition14
runtime, Node20 executable, schema path, and normal renderer node_modules.

## Independent post-exit evidence

- Static `awk` parsing found exactly two Agent rows (`full`, `targeted`), and
  `bash -n -c` passed for both commands.
- Comparing the current rows with the actual pre-change rows read immediately
  before the accepted 0856 replacement shows only the authorized
  `/tmp/w-5829dd9212/site-packages` to durable projection substitution. The
  current counts are `old_path_count=0`, `durable_path_count=2`.
- With only `PYTHONPATH="$PWD:/home/user/work/agent-runtime-projection-0856/site-packages"`
  (no Runtime source path), the post-exit import probe returned:

  ```text
  astrid /home/user/work/wt/agt-F-env-final-review-0901/astrid/__init__.py
  runtime_protocol /home/user/work/agent-runtime-projection-0856/site-packages/runtime_protocol/__init__.py
  astrid_runtime_client /home/user/work/wt/agt-F-env-final-review-0901/astrid_runtime_client/__init__.py
  banodoco_timeline_schema /home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema/__init__.py
  ```

- Missing-source negative preflight (`PYTHONPATH="$PWD"`) exited 1 with
  `ModuleNotFoundError: No module named 'runtime_protocol'`, as required.
- Node22 negative preflight exited 0 only because the existing resolver
  refused Node `v22.22.0`, citing the Remotion pin `v20.19.4`.
- The exact current Runtime pointer is HEAD
  `7ca1a227815404252fec1e4768e550610f9c5705`, tree
  `b88df06a20c2b67fd185dab9ae65c0de8fb9f49f`, with a clean worktree.
- The normal renderer graph remains Node `v20.19.4`, Remotion `4.0.509`,
  esbuild `0.28.1`, Composition `0.0.14`, React/React DOM `18.3.1`;
  `node_modules` is a real directory. The lock hash is
  `b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0`, the
  0.0.14 archive hash is
  `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`, and
  the reviewed normal Composition identity remains
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- The exact D09 path `/home/user/work/runtimes/agent-remotion-0013` remains
  absent. No alias or fake fixture was created.

The reviewer worktree is clean and no source, test, pin, schema, contract,
shared dependency, launcher, process-rule, sanitizer, selector, or full-v2
request/reply change was made. The prior four representative causal-group
PASSes from request `agt-F-env-return-0856-targeted-1023085807-14726` were
reused; no duplicate four-node body, full suite, P1/P4 HTTP, native14,
crash24, heavy journey, browser, or render run was made.

## Limits

The original full result remains `16388 passed, 240 failed, 140 errors, 40
skipped, 5 xfailed`, exit 1; no full rerun was requested. This is a PASS for
the durable environment gate only, not a claim that the full suite or the
separate D09 exact0013 fixture is complete.
