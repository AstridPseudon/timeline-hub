# PASS — G2/P4 public-command integrated readonly proof

Bounded proof passed on the actual integrated Agent source.

- Agent `HEAD`: `e49a6e76b3ab363e312c55b313714af1f845f54b`
- Agent tree: `6ba7770dac3843b4d24d933521893277139d5ba1`
- Reviewed tree: `6ba7770dac3843b4d24d933521893277139d5ba1`
- Runtime `HEAD`: `a5d4258312c979024865ee704da2d632ca5b2730`
- Existing reader `bd23946157d863b39a8c0e3c41ea489455e08b1b`: unchanged
- Relevant source hashes: equal to reviewed tree

Exact targeted command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_public_command.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_remote_timeline_owner_scope.py
```

Result: **30 passed in 8.32s**, exit 0.

Production import origins were the assigned worktree for `astrid`,
`astrid.sdk.timeline`, `commit_session`, and `_remote_timeline`; `runtime_protocol`
came from `/home/user/work/runtime`. `timeline.open`, `Timeline.command`,
`Timeline.commit`, and `_execution_bundle` all resolved to the mounted
`astrid.sdk.timeline.commit_session` implementation.

Confirmed through existing tests: portable public bundle; exact-pair
authenticated private hydration; sequential and child staging; function
conflict recomputation; preview `would_status` and unchanged base; accepted
adoption; shared-alias refusal; and negative scope/pair/digest/previous,
outside-closure, foreign-owner, and no-sibling-broadcast behavior. Existing
request/reply assertions retain C0 fields and `{data, receipt}` forms,
accepted/preview/conflict/invalid details, ten-step metadata/history and
per-step undo.

Reused identical-tree static proofs: independent review **151 passed**,
Ruff **2149/2149**, Mypy **1912/1912**, vendor lock and diff check passed.
The local fixture uses the real SDK provider/service with a fake local
`RemoteTimelines` transport; no live HTTP acceptance is claimed. No HTTP,
native14, crash24, browser, localhost/live-socket, or full-suite run was made.
No product or Git changes were made.
