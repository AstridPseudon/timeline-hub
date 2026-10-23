# P4 service-envelope review handoff

## Review result

PASS. The existing `agent p4-v2-http-nodes` row in
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`
has exactly the official Runtime34e source:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004
PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-34eac004
/home/user/work/venv-app2-native/bin/python -m pytest -q -m integration
```

The independent before/after SHA-256 proof is:

```text
before 3a70311e8ab18cdfed3acde55b3a82885992491d978986c45a6417740d44779b
after  abf937839dd2d3ebc384a69552c3b11027b7c0d14930e088aee768160ec5f935
```

The sole diff is the 780da6d6 → 34eac004 checkout and matching Runtime
`PYTHONPATH`; every other row and command byte is unchanged.

Runtime `/home/user/work/wt/rt-pin-34eac004` is clean at commit
`34eac0041b0891e9011966b39bcbd26053fde5bc`, tree
`9853574865f25e08284e82ffb26c0bdecaa16a30`. The original executable
`/home/user/work/venv-app2-native/bin/python` is executable and reports Python
3.12.3.

The actual `*-nodes` missing-`--files` guard returned exit 2. The literal row
command, with only `--collect-only` appended, collected exactly:

```text
tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back
```

It collected 1 test and exited 0. No body, socket, browser, full, heavy, or
new-launcher run occurred. The test service's actual snapshot implementation
was inspected: it makes a detached snapshot, runs from that snapshot with
`PYTHONPATH=$SNAP`, and the row's `$PWD` expands to the snapshot root.

## Exact later request

Only once compatible normal34e + G3/R2 owner source is ready, replace the
literal `OWNER_JOIN_WORKER` with that actual owner worker name and run this
first permitted body request against the current Runtime34e checkout:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test OWNER_JOIN_WORKER p4-v2-http-nodes --files 'tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back') && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \"$R\"
```

The production caller is still unexecuted. Preserve the full v2 request/reply
contract qualification, including `rebased_onto` when present. Do not recycle
the historical 0307 source worker, and do not claim P4 acceptance from this
collection-only proof.
