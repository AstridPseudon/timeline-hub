# P4 single CLI/sheet current-integration port — PASS

## Scope and decision

This is a bounded test-only port onto the current Agent integration head. The
only repository change is
`tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`; no old stage
branch or donor ancestry was merged.

The exact final donor blob is
`033482ec2b94c5ae4a6b5c456e2d9fab3f454022`, from donor commit
`7a62327b75840f3a45e83719d52e57422946d920` (tree
`b07b812ac26d793f26b2edf37efd724d94a0ac3a`, parent
`d8ab46e235e1ab5d2a1f9f9a37e0508235c5b2de`). The working file hash is exactly
the same. This preserves the reviewed 66-assertion single-edit oracle,
including full commands/records/dependencies/bindings/effects/steps,
canonical/authored payload and cache/source boundaries, show, history, full
receipt, head, and stored readback. The faithful provider-boundary correction
constructs `expected_plan` from the original verified `base_document` while
passing the full recorded request and evaluated head.

## Base and tree

- Dispatch record base: `f94a3a032a52153262cefa92053438e15aff4f54`, tree
  `d11f11e3c3703b3c6437613381cc1a0f9061f3fa`.
- Actual target `tl/integration` / worker HEAD:
  `6131704b36807e165575fa944ba984cc847059c8`, tree
  `b4a194abe8601470ea7fa9b38ea54e258dc673c3`.
- `git log tl/integration..HEAD` is empty before the harness creates the
  eventual own commit.
- Working diff is one file: 89 insertions and 11 deletions.

## Evidence

All commands passed:

```text
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q -m integration tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
1 test collected in 0.93s (existing unknown timeout-option warning)

/root/.local/bin/ruff check tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py
Success: no issues found in 1 source file

git diff --check
PASS
```

The donor hash proof passed, and `git diff --name-only` outside the target file
was empty. The retained source path uses the actual CLI parser, sheet export,
`TimelineSession`, and generated `timelines.open_bundle`/`history` callers.

## Limits and next step

No live HTTP/socket/service body, full suite, browser, build, or central test
service was run here, as explicitly required. The existing staged service PASS
is not integrated-P4 credit. Independent Luna review must precede the manager's
own-commit log check and remote request; the manager then runs the original
one-node service test on the integrated head.
