# P4 single CLI/sheet integration-test port

## Result

PASS for the bounded source port. The only worktree product change is
`tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`, replaced with the
mandated final donor blob. No donor branch was merged and no product, helper,
schema, generated, pin, lock, suite, launcher, or fixture file was changed.

## Exact source identity and provenance

- Requested dispatch base: `f94a3a032a52153262cefa92053438e15aff4f54`, tree
  `d11f11e3c3703b3c6437613381cc1a0f9061f3fa`.
- Actual target integration HEAD used by this worker: `6131704b36807e165575fa944ba984cc847059c8`, tree
  `b4a194abe8601470ea7fa9b38ea54e258dc673c3`. It is the current
  `tl/integration` ref and has no commits ahead of that ref.
- Mandated donor provenance: commit
  `7a62327b75840f3a45e83719d52e57422946d920`, parent
  `d8ab46e235e1ab5d2a1f9f9a37e0508235c5b2de`, tree
  `b07b812ac26d793f26b2edf37efd724d94a0ac3a`.
- Mandated donor path blob and resulting working blob:
  `033482ec2b94c5ae4a6b5c456e2d9fab3f454022` (exact match).
- Current uncommitted diff: 89 insertions, 11 deletions, one file only.

The donor retains the full single-edit oracle: command, label, step patch and
reads, merge and dry-run/key fields; accepted canonical document, digest,
heads, receipt, complete records/dependencies/bindings/effects/steps, show,
history, head, and stored readback assertions. Its provider-boundary oracle
builds `expected_plan` from the authenticated original `base_document` while
retaining the recorded request and evaluated head.

## Checks

All commands exited zero:

1. `PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q -m integration tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`
   — exactly 1 test collected. Pytest emitted only the existing unknown
   `timeout` config warning; the test body was not run.
2. `/root/.local/bin/ruff check tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`
   — All checks passed.
3. `/root/.local/bin/mypy --follow-imports=silent tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`
   — Success, no issues found.
4. `git diff --check` — PASS.
5. Donor/outside-scope proof — working hash equals
   `033482ec2b94c5ae4a6b5c456e2d9fab3f454022`, and the exclusion diff for every
   path other than the target file is empty — PASS.

The retained caller path is exercised by the collected test and remains wired
through `build_parser`, `TimelineSession.open`, `NativeSheet.export`, and the
generated client calls to `timelines.open_bundle` and `timelines.history`.

## Limits

Per the task, no original HTTP/socket/service body, full suite, browser,
build, or central test-service run was performed. The staged service PASS is
not claimed as integrated P4 credit. Independent review and the manager's
own-commit log check remain required before remote request/merge; the eventual
integrated-head one-node run remains the manager's step.
