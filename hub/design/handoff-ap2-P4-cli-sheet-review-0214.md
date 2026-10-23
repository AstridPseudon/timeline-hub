# Handoff: ap2-P4-cli-sheet-review-0214

**Verdict: FAIL.** The candidate `tl/ap2-P4-cli-sheet-0210` must not be
accepted or receive P4/H3 credit. Reviewed source commit: `c71628f1`.

## Reviewed source and exact evidence

The candidate adds only `tests/sdk/test_p4_cli_sheet_v2.py`; the source handoff
is `design/handoff-ap2-P4-cli-sheet-0210.md` in the Timeline hub. The mandated
run was executed exactly:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q --runxfail tests/sdk/test_p4_cli_sheet_v2.py tests/sdk/test_p4_commit_cases.py
FAIL: 1 failed, 2 passed, 1 warning in 2.69s
```

The failure is the candidate's expected `doc.patch` command, nonempty step
patch, and `merge: atomic`. The actual request captured by the same test is a
valid semantic `clip.move` with `on: 5`, captured reads/effects, `Apply sheet`,
one `sheet-1` step with `patch: []`, `merge: fields`, `source: {"via": "sheet"}`,
the exact `r0/pub0` base, and the requested idempotency key. The edit and all
checked unrelated closure fields pass before that wire mismatch.

Other checks:

```text
/root/.local/bin/ruff check tests/sdk/test_p4_cli_sheet_v2.py
PASS: All checks passed!
/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_cli_sheet_v2.py
PASS: Success: no issues found in 1 source file
git diff --check
PASS: no output
```

The one pytest warning is the existing unknown `timeout` config option. No
full/browser/live-socket/Runtime acceptance suite was run.

## Contract and caller review

Contract §1 explicitly permits existing semantic commands (`clip.move`,
`clip.trim`, etc.) or `doc.patch`. For semantic commands, submitted
`steps[].patch` may be empty; the provider fills authoritative effects. Native
captured reads make `merge: fields` valid. Therefore a test cannot require
`doc.patch` and `atomic` merely to manufacture a G3 gap.

The installed production caller is:

```text
cli._cmd_apply
  -> cli_native.commit_edit(sheet=True)
  -> NativeSheet.load(session).apply
  -> NativeSheet.preview (native clip.move capture)
  -> TimelineSession.commit_many
  -> TimelineSession._flush / client.timelines.commit
```

Exact source facts: `astrid/packs/timeline/cli.py:3586-3604` routes native
sheet rows; `astrid/packs/timeline/cli_native.py:197-202` invokes
`NativeSheet.load(...).apply`; `astrid/sdk/timeline_sheet.py:755-765` captures
semantic commands and `:877-881` submits empty semantic step patches. This
caller does not invoke `Timeline._capture_free_edits` or
`emit_document_commands` for the tested move. It is valid semantic behavior,
not proof that a free-document G3 emitter is used.

The strict xfail is not proof and must not be merged as proof. With
`--runxfail` it fails; without it, it is only an expected failure.

## Remaining unproven behavior

- The `connected.Generated` object in `tests/sdk/test_timeline_sync.py:40-122`
  is a generated-client transport fake. It exercises the command engine and
  compiler but supplies no Runtime acceptance or H3 evidence.
- No installed Runtime proof covers the complete v2 ABI1 request (scope/base
  pair, commands, label, steps, optional reads, merge, dry-run and
  `Idempotency-Key`) or complete accepted/merged replies (canonical closure,
  digest/head/receipt, authoritative commands/steps/dependencies/merge_mode).
- Conflict reason/head, invalid code/path/hint/suggested command, preview
  `would_status`/history, and real `show`/`history` readback are absent.
- `test_p4_commit_cases.py:97-134` and `cases.json` explicitly retain
  `execution: pending`; the ten-note one-commit, independent per-step undo,
  conflict, and bounded re-run are not proved. Full ten-note acceptance is
  pending.
- The 5-second witness changes its baseline: `document_fixture` starts
  `clip-a.at` at `1` and FPS at `30000/1001` (`tests/sdk/test_timeline_commit_provider_document.py:22-28`),
  while the candidate changes FPS to `30` (`test_p4_cli_sheet_v2.py:46-57`)
  and edits the literal token `"5"` (`:61-64`). This avoids rational-FPS
  quantization and proves `1 -> 5` on the mutated fixture, but it does not test
  a `5s` token or preserve the original rational-FPS provenance. The P4 case
  manifest separately promises `before: 0 -> after: 5` (`cases.json:57-69`),
  so this is not the original single-edit corpus witness.

## Smallest correct first return

Keep this real parser/sheet/session/outbox test, but assert the contract-valid
semantic request: exact scope/base, one `clip.move` selecting
`parent/clip:clip-a` with `on: 5`, `Apply sheet`, `sheet-1` with ordinal `0`
and empty submitted patch, `merge: fields`, `source: {via: sheet}`,
`dry_run: false`, and the exact idempotency header. Continue asserting the
intended edit and unrelated raw/opaque/closure preservation. Do not force
`doc.patch` or `atomic`; retain G3 `doc.patch` proof for a genuine free bundle
edit through `Timeline._capture_free_edits`.

After that, add actual Runtime/CLI accepted and merged replies, conflict and
invalid cases, preview, `show`/`history`, and the ten-note commit with guarded
independent step undo. Until those run against installed Runtime and restore
the original corpus/provenance witness, P4/H3 remains pending.

No product code, tests, generated files, or fixtures were changed by this
review. Full review details are in the harness worker report at
`workers/ap2-P4-cli-sheet-review-0214/report.md`.
