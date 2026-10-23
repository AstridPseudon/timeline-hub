# Handoff: P4 single current-port review

Result: **FAIL**.

Candidate `ca1f2228c2343d95402b18d3f6d11eae68cc2867` is based directly on the
exact actual base `6131704b36807e165575fa944ba984cc847059c8` (base tree
`b4a194abe8601470ea7fa9b38ea54e258dc673c3`) and has candidate tree
`30c9d1106a1acdaa3c60726c744cc20a04cc814e`. The mandated donor is
`7a62327b75840f3a45e83719d52e57422946d920` (tree
`b07b812ac26d793f26b2edf37efd724d94a0ac3a`); its commit is not an ancestor,
and its required test blob
`033482ec2b94c5ae4a6b5c456e2d9fab3f454022` exactly equals the candidate test
blob. The donor has no `report.md`.

The candidate nevertheless changes two paths:

    report.md
    tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py

The extra tracked root `report.md` violates the explicit one-file test-only
scope and “NEVER trackedreporeport” requirement. The review worker did not
alter it and made no commit.

The port file has 66 assertions and retains the required ordinary CLI
`build_parser`, `TimelineSession.open`, `NativeSheet.export`, CLI apply,
Runtime `open_bundle`/`history`, provider-boundary expected-plan comparison,
full v2 request/response/history/readback fields, and stored-read checks.

Commands run:

    PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q -m integration tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
    /root/.local/bin/ruff check tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
    /root/.local/bin/mypy --follow-imports=silent tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
    git diff --check 6131704b36807e165575fa944ba984cc847059c8 HEAD

Collection found 1 test with the existing unknown `timeout` config warning;
Ruff, mypy, and diff check passed. No HTTP/socket/service body, full suite,
browser, build, or central test service run was performed. No merge request or
integrated-head one-node run is authorized from this FAIL result. Recommended
next step: remove the tracked report from the candidate and rerun the
independent review.
