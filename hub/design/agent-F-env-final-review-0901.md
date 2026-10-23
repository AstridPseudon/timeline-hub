# Agent F environment final review 0901

## Verdict: PASS

Independent post-exit review confirms that the current Agent `full` and
`targeted` rows resolve `runtime_protocol` through the durable
`/home/user/work/agent-runtime-projection-0856/site-packages` projection.
The projection link resolves to `/home/user/work/runtime/runtime_protocol`;
`/tmp/w-5829dd9212/site-packages` is absent. The current Runtime pointer is
`7ca1a227815404252fec1e4768e550610f9c5705`
(`b88df06a20c2b67fd185dab9ae65c0de8fb9f49f` tree), clean after the author
process exited.

The one authorized service run was:

```text
request-test agt-F-env-final-review-0901 targeted --files \
  tests/core/execution/test_generic_host_actions_v3.py::test_static_discover_admit_dry_run_and_owned_child
```

Request `agt-F-env-final-review-0901-targeted-1023090117-4730` passed with
exit 0: **1 passed in 10.90s**. Its sanitized command retained the current
Runtime pointer, durable projection, Composition14 runtime, Node20.19.4,
installed schema path, and normal renderer dependencies.

The static/env audit passed: exactly two Agent rows parsed, both passed
`bash -n`, no old `/tmp` path remains, and the durable path occurs twice.
The actual pre-change rows immediately before the 0856 accepted replacement
were compared; selectors, pytest commands, runtime/renderer paths, and
security sanitizer settings were unchanged apart from the authorized
projection path.

Post-exit module origins with only the worktree and durable projection on
`PYTHONPATH` were:

```text
astrid                 /home/user/work/wt/agt-F-env-final-review-0901/astrid/__init__.py
runtime_protocol       /home/user/work/agent-runtime-projection-0856/site-packages/runtime_protocol/__init__.py
astrid_runtime_client  /home/user/work/wt/agt-F-env-final-review-0901/astrid_runtime_client/__init__.py
banodoco_timeline_schema /home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema/__init__.py
```

The missing-source negative import exited 1 with the expected
`ModuleNotFoundError`. The Node22 negative guard exited 0 after refusing
`v22.22.0` because the renderer pins `v20.19.4`. The normal graph remains
Remotion `4.0.509`, esbuild `0.28.1`, Composition `0.0.14`, React/React DOM
`18.3.1`, with real `node_modules`; lock hash
`b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0`, archive
hash `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`,
and normal identity
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

No source edits were made by this reviewer; the worktree is clean. No full
suite was run. The prior full result remains `16388 passed, 240 failed, 140
errors, 40 skipped, 5 xfailed`, exit 1. D09 exact0013 remains an unmet,
unfaked separate need. Prior representative14726 PASS4 was reused; no
duplicate bodies, full/P1/P4HTTP/native14/crash24/heavy journey/browser/render
run was performed.
