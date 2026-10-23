# P1 anchor/operand audit — 2026-10-23

## Result

No authentic source binding was omitted during P1 conversion. The original
shared-child scalar fixture intentionally contains unresolved authored timing
declarations that are unrelated to the parameter edit:

```text
app.astrid.on     = "old-anchor"
app.astrid.until  = "end"
app.on            = null
```

The fixture has no transcript, word, anchor, or pin binding for those values.
Its complete `source_mapping.shots` has two placement-local entries, both
pointing to `shot_id: s`, `revision_id: sr`, `internal_timeline_id: main`, and
`internal_timeline_revision_id: ir`, with an empty `item_id_map`. There is no
transcript/word source object or binding to carry into a test setup.

## Provenance and intent

- `tests/editing_conformance/fixtures/recipe_m2_scalar_disjoint.json` and the
  three sibling scalar fixtures first appeared in `84db8bde` (the first scalar
  fixture commit). The `old-anchor`/`end`/`null` declaration was already in
  the initial fixture; it was not introduced by P1 conversion or the current
  V2 repair.
- The P1 corpus copy was added in `c241aeca`; `doc_patch_requests.json` and
  real-provider execution were added in `edcd1b2b`. The P1 request tests verify
  the canonical and source SHA-256 values match, so conversion did not alter
  this declaration.
- The scalar child baseline is byte-for-byte the same authored clip as the
  baseline clip in `tests/editing_conformance/fixtures/recipe_m1_move.json`.
  The M1 fixture treats the old timing fields as authored values to retain,
  not as a transcript-backed timing case. `84db8bde` also states that capture
  commands and output bundles retain Bundle1 byte parity.
- The source recipe is
  `tests/editing_conformance/test_recipe_scalar_commands.py::test_portable_scalar_capture_goldens[...]`.
  `capture_clip_set_params` reads identity/occurrence/source and parameter
  schema basis (`astrid/sdk/timeline/_scalar_commands.py:68-95`); it does not
  bind or consume timing declarations. The four P1 operands are all
  `internal-revision:ir` child paths.

## Retained assertions

The source and P1 tests preserve the original successful behavior:

- `params-absent-to-explicit-values`: absent `params` becomes the explicit
  object, including empty, dotted/bracketed, and null keys.
- `params-null-to-object`: a present `params: null` container becomes the
  explicit object, distinct from a child null.
- `params-remove-and-preserve-opaque`: removes only `old`; retains `null`,
  `x`, `y`, and opaque values.
- `disjoint-field-merge`: rebases `x: 1 -> 2` over a competing `y: null ->
  false`, preserving `y` and opaque data.

Across these cases, `app`, timing fields, placements, and shared-child alias
identity remain unchanged. The source recipe retains inverse/redo, reload and
replay assertions; the P1 provider retains canonical round-trip, shared alias,
opaque-value, accepted/merged status, and disjoint-head assertions. No
success was changed to refusal here.

## Policy gate for the orchestrator

**Under C0 as currently written, unchanged unresolved known timing declarations
are not automatically permitted to pass an unrelated `doc.patch`.** The
contract requires provider timing validation against the completed candidate
(§1 and §2); it does not contain a legacy-unresolved exemption. The source
evidence nevertheless demonstrates that these original scalar fixtures were
deliberately authored as unrelated-field preservation cases, not as valid
timing-binding cases.

Therefore the four original P1 successes cannot be preserved against the
current timing validator by inventing a binding, changing a declaration, or
bypassing validation. If the orchestrator intends to preserve this original
behavior, it needs an explicit contract/policy clarification scoped to
untouched unresolved legacy timing declarations. No Agent V2 repair or fixture
change was made or proposed here.

## Production caller / wire scope

The production Agent provider is `RuntimeCommitService` in
`astrid/sdk/timeline/commit.py:757,892`; `create_runtime_commit_service()` at
`:1143` returns it. Its v2 path calls `_commit_patch.rebase_patch` at `:897,1063`,
replays through `execute` at `:1067`, runs `validate_final_candidate` at `:1088`,
and sends the authenticated candidate to `port.preview`/`port.accept` at
`:1109-1115`. The normal SDK caller is `TimelineSync._flush` at
`astrid/sdk/timeline/sync.py:421-452`, which sends the request through
`client.timelines.commit` with `Idempotency-Key`.

This audit does not establish an App mount or full Runtime/App wire journey.
The direct P1 provider tests call the Agent provider through `_service_call`
(`tests/sdk/test_p1_doc_patch_provider.py:131-147`) and use detached port
fixtures. Full v2 ABI-1 wire coverage—scope/base revision+publication,
commands, label, steps (`id`, `label`, `intent`, `tags`, `command_ordinals`,
patch, optional reads), `merge`, `reads`, `dry_run`, idempotency; and accepted,
merged, conflict, invalid, preview/history reply envelopes—is therefore
outside this source/operand audit and remains unverified. No H3 go/no-go is
claimed.

## Checks

Run from the assigned worktree, with no product changes:

- `git diff --exit-code` — pass (exit 0)
- `git diff --check` — pass (exit 0)
- `/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py` — pass
- `/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py` — pass
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_requests.py -k 'params or disjoint'` — 1 passed, 11 deselected; one existing unknown-`timeout` config warning

No broad provider matrix, Runtime/App/browser/socket/full suite, install,
launcher, or owner V2 repair run was performed.
