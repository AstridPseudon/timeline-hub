# P4 service-envelope successor handoff

The existing `agent p4-v2-http-nodes` row in
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`
now points to the exact official Runtime checkout:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004
PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-34eac004
/home/user/work/venv-app2-native/bin/python -m pytest -q -m integration
```

Readiness was verified at Runtime commit
`34eac0041b0891e9011966b39bcbd26053fde5bc`, tree
`9853574865f25e08284e82ffb26c0bdecaa16a30`, with a clean source checkout.
The exact original node collected one test and exited zero using the new row
environment. The `*-nodes` route refused a missing `--files` with exit 2.
No body, socket, browser, full, or heavy run was executed.

## Exact later request

Only once compatible normal34e + G3/R2 owner source is ready, replace the
literal `OWNER_JOIN_WORKER` below with that actual worker name and run:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test OWNER_JOIN_WORKER p4-v2-http-nodes --files 'tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back') && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

That is the first permitted body run for this route. It must qualify the
complete v2 request and reply envelope through the real CLI/sheet/generated
HTTP/Runtime/show/history path, including accepted/merged metadata,
dependencies and effective merge mode, conflict head/reason/entries,
structured invalid code/path/hint/suggested command, and preview
`would_status`. Preserve the Runtime contract's `rebased_onto` head when
present. This handoff does not claim those body behaviors or H3/P4 acceptance.

The 0307 readiness handoff remains historical and must not be recycled as the
owner source. The production caller is still unexecuted.
