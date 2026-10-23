# P4 local test-service route handoff

## Source-readiness PASS

Registered exactly one new named allow-list row in the existing absolute
`tests/suites.conf`:

```text
agent p4-v2-http-nodes env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-780da6d6 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-780da6d6 /home/user/work/venv-app2-native/bin/python -m pytest -q -m integration
```

The row uses the official clean Runtime 780 checkout at
`/home/user/work/wt/rt-pin-780da6d6`:

- commit: `780da6d605033ca71dbe2ad48c10ec2870ea4865`
- tree: `a2850bcaf0b37bd04613b02f071457b66f0987e3`
- interpreter: `/home/user/work/venv-app2-native/bin/python` (Python 3.12.3)

The exact source-readiness command selected one positive test and exited 0:

```text
1 test collected in 0.83s
```

Full output, including the actual interpreter and environment values, is in
the worker harness report/log at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P4-local-service-route-0305/report.md` and its `tmpdir` evidence file.

## Deferred owner join

Once compatible normal780 + G3/R2 owner source is ready, request the named
route with only the original node:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test OWNER_JOIN_WORKER p4-v2-http-nodes --files 'tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back') && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The current source-review0242 PASS is retained as independent source review
only. No HTTP/socket execution, body test, P4 acceptance, or H3 go decision
was made here. Existing default targeted and old-0247 missing-venv commands
were not altered or silently aliased.
