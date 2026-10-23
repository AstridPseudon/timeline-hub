# Handoff: ap2-P4-cli-sheet-sol-correction-0224

Completed the missing independent raw/sibling preservation witness from review
0221. Base: `a4a2a8d5` (`tl/ap2-P4-cli-sheet-first-return-0218`). Repository
diff is additive assertions only in `tests/sdk/test_p4_cli_sheet_v2.py`.

The test retains complete execution-oracle equality and all authored-at,
derived-marker, request metadata, one-call and idempotency assertions. It now
also checks original clip b directly, the entire ordered clip list against
original clips with only clip a's `at: 5` and exact native-derived app markers
overridden, config directly, and full original-based bundle equality. Thus
clip a params/hold/track/type/ID/strings, unknown fields, raw base payloads,
closure, order and absences (including occurrences) have independent witnesses.

Provenance is the unchanged actual source
`tests/sdk/test_timeline_sync.py::initial_bundle` (clip a at 0, FPS 30), with
one sheet cell edited to `5` for the original CLI `--on 5` intent. No fixture
or product changes, no markers/skips/xfails, and no passing assertion removed.

The earlier claim of a product/G3 defect on this semantic sheet route was
incorrect: contract §1 permits captured `clip.move`, empty submitted step
patch and fields merge. The production parser → handler → NativeSheet /
capture_move → TimelineSession → persisted outbox caller uses this valid
path. Free-document G3 remains separate. The generated transport is still fake.

Exact validation:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_cli_sheet_v2.py tests/sdk/test_p4_commit_cases.py
3 passed, 1 warning in 1.56s; exit 0
/root/.local/bin/ruff check tests/sdk/test_p4_cli_sheet_v2.py
All checks passed!; exit 0
/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_cli_sheet_v2.py
Success: no issues found in 1 source file; exit 0
git diff --check
PASS, no output; exit 0
```

The existing warning is unknown pytest `timeout`. Tool caches and scratch
use `/tmp/w-45466e140f`, identified by the worker's `tmpdir` pointer. No
full/native matrix/Runtime/browser/socket/runner/install was run.

Limits: this preserves the accepted semantic request's existing ABI1 scope,
r0/pub0 base, commands, label, step ID/label/intent/tags/ordinals/empty patch,
fields merge, source, absent top-level reads, dry_run false and exact
Idempotency-Key checks. It does not establish the full request variant matrix
(optional step/request reads, atomic merge) or Runtime wire acceptance.
Reply checks remain presence-only for canonical document/digest/revision/
commands and receipt. Full accepted/merged canonical closure/digest/head/
receipt/authoritative commands/steps/dependencies/merge_mode; conflict
reason/head; invalid code/path/hint/suggested command; preview would_status/
history; CLI show/history; and ten-note end-to-end remain separate evidence.
No H3/P4DONE claim. Earlier reviewed P4 provider13 and fn3 proofs remain scoped;
a pending collection manifest does not mean all ten-note work was unexecuted.

No blockers. Next: independent narrow review and normal integration queue.
Detailed report: `workers/ap2-P4-cli-sheet-sol-correction-0224/report.md`.
