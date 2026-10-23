# G5 rendering skill documentation review

## Verdict

**PASS — bounded documentation-only review of draft `003013fa1`, over parent
`c59a75177`.** The draft remains **DRAFT ONLY / P1 NO-GO**; this is not merge or
activation approval.

## Exact diff scope

`git diff --name-status c59a75177..003013fa1` reports exactly:

```text
M  astrid/packs/rendering/docs/SKILL.md
```

The diff is `62 insertions, 16 deletions`, limited to the CLI editing guidance
at current lines 213–280. Existing unrelated SKILL sections are unchanged.
No test code changed. No schema, generated client, pin, Runtime guard,
environment, daemon, or Git-internal file changed.

## What was verified

The current parser and handlers support the documented caller forms:

- `show <timeline> --project <project> --json`: read-only current scope/head
  lookup (`cli.py:_cmd_show`).
- `edit <timeline> ... --clip ... --on ...`: numeric move dispatches through
  `TimelineSession.move`; the trim form with `--trim-in/--trim-out` dispatches
  through the existing trim/session path.
- `apply <timeline> ... <sheet-file> ...`: connected clip/track sheets use
  `NativeSheet.load(session).apply`.
- `undo <timeline> ... --commit <receipt-id>` and `redo ... --commit
  <undo-receipt-id>` use the guarded existing `TimelineSession.undo` inverse
  route; `--steps` accepts the documented receipt-to-step JSON map.
- `commit <timeline> ... --file <candidate.json> -m ...`: the detached
  document is sent through the existing `TimelineSession` commit boundary.
- `timelines --help` contains the documented command families. The examples'
  flags parse against the current parser, including project/ref order,
  idempotency keys, JSON output, trim flags, sheet path, commit receipt, step
  map, detached file, message, and dry-run-capable parser surfaces.

The prose accurately states the v2 request/reply contract at lines 246–280:
exact outbox body/key, original-base retry and no recapture after ambiguous
acknowledgement, terminal refusal versus exact retry, preview with
`would_status` and `receipt: null`, accepted/merged canonical document and
full receipt, recorded history/records/dependencies/effects, and structured
refusal/conflict details with path/head/current/hint/suggested command.

The changed guidance contains no stale `timelines publish`, `apply --native`,
native edit subparser, `undo/redo --publication`, three-way, commands-file, or
`publish_bundle` recommendation. The remaining generic uses of “publish” in
the surrounding skill describe normal Runtime commit/publication semantics or
explicitly say that the held whole-candidate writer is not a fallback route.

## Commands and results

The first parser attempt was environment-only and stopped before parser
construction because `runtime_protocol` was not on `PYTHONPATH`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 - <<'PY' ... build_parser(None) ... PY
=> ModuleNotFoundError: No module named 'runtime_protocol'
```

No handler or mutation ran. The corrected offline parser/help check was:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime python3 - <<'PY'
... build_parser(None); parse --help; parse show, edit(move+trim), apply,
    undo, redo, commit; assert handler names/flags; invoke no handlers ...
PY
=> PASS: help + six command families parsed offline; handlers not invoked
=> checked: show, edit(move+trim), apply, undo, redo, commit
```

The other permitted checks were:

```text
git diff --check c59a75177..HEAD
=> PASS

git diff --unified=0 c59a75177..HEAD -- astrid/packs/rendering/docs/SKILL.md \
  | rg '^\\+' | rg -i '<credential patterns>'
=> 0 high-confidence credential matches in added lines

for pattern in 'timelines publish' 'apply --native' 'edit move' \
  'edit track-label' 'undo --publication' 'redo --publication' \
  'three[-_ ]way' 'commands-file' 'publish_bundle'; do
  rg -n -i "$pattern" astrid/packs/rendering/docs/SKILL.md
done
=> all nine patterns ABSENT
```

The first command above is the only parser check that needed the shared
Runtime checkout; it was read-only. No HTTP, browser, socket, full suite,
static broad test, original test body, or mutation invocation was run.

## Reused evidence and limits

Per brief, source-184 and source-22 results were reused, not rerun:

- `design/agent-G5-current-review-1732.md`: exact donor/source preservation
  with `184 collected; 184 passed in 50.01s`.
- `design/agent-R2-ABA-partition-sol-1833.md`: final source-22 ABA evidence,
  19 final cases plus targeted public 3-case selection; the report explicitly
  records the diagnostic combined-run limitation.

Those results do not expand this review into a product qualification and do
not override the plan's P1 gate. Frozen `34e`, `d106`, and `819acf` surfaces
were not changed by this one-path documentation diff.

Permanent source inputs, module hashes, line-source map, reused-evidence
identities, and credential scan are in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-docs-review-1852/evidence/`

No product files were edited by this review. Recommended next step: retain the
draft-only disposition and let the orchestrator decide any later P1-gated
integration or qualification work.
