# Runtime catalog-text current-tree resolution

## Exact inputs and resolved-tree rule

- Current parent: `a51af885ea631c695a857985239c7fe7bf2e871f`
  - tree: `7c6ab6700307309a7942e64eb4d0c6c7cc42b681`
  - parents: `81f8c7e0b22c34804015c054762af3d737e4698a`, `3021a5b79102e9c0873f70df46f5a686bd1276ff`
- Approved candidate: `63e761e29e7e51fc5fa71cc01cd1fe0cf5952125`
  - tree: `7e1b71ac53312ddbbceefa32b40a919d467b5002`
  - parent: `d037368d22373be92c1e4c1a821315a1130fdcff`
- Candidate/common base: `16acbb6ef94a6d8e226ccdc351ba0d96e0b09ea5`
- Approved candidate source delta: `d037368d` (unplaced catalog-shot text set/rebind) plus `63e761e` (receipt-first replay identity).

The resolved tree starts from current `a51`. It retains current promotion and
revision helpers, selected-media CAS verification, native historical retry,
audit/shell/fresh/connector changes, and public 0.1.3 artifact bytes. It then
restores only the approved catalog-shot text binding implementation/replay
semantics and the corresponding authority tests. No repository merge, rebase,
commit, branch update, or full suite was run.

## Source inventory

Intended text delta over current `a51`:

| Path | Added | Removed | Reason |
| --- | ---: | ---: | --- |
| `runtime_protocol/service.py` | 299 | 2 | reviewed text set/rebind, UTF-8/CAS/event helpers, unplaced guard, replay-before-live checks; remove retired aliases |
| `tests/test_shot_text_bindings.py` | 78 | 10 | restore original positive binding assertions and restart replay regression |
| `tests/test_timeline_shot_authority.py` | 42 | 4 | retain promotion authority assertions while adding text scope/auth/replay coverage |

The current-root files restored while resolving the candidate lineage were
verified byte-identical to `a51`:

`runtime_protocol/store.py`, `runtime_protocol/timeline_commit_port.py`,
`runtime_protocol/timeline_commit_store.py`,
`tests/test_shot_candidate_promotion.py`,
`tests/test_timeline_clip_replacement.py`, and
`tests/test_render_native_historical_retry.py`.

The last file was absent from the candidate checkout but restored from current
`a51`; it is not a new product change. No reject files, conflict markers,
bytecode, cache, or build output remain in the worktree.

## Resolution decisions and limits

- Keep the current `promote_project_shot_candidate` implementation and its
  current authority tests; do not accept the candidate's retired-promotion
  version of the authority fixture.
- Keep current consumed-media CAS verification and all independent current
  files listed above.
- Make only the reviewed text writers active. They require exact project scope,
  unplaced project-library shots, deterministic binding identity, UTF-8 bytes,
  SHA-256 identity, empty text as present content, append-only events, and
  idempotent receipts. Film-history shots and missing shots remain refused;
  retired CRUD writers remain refused.
- Replay derives the request identity and checks the durable receipt before
  resolving mutable binding state. Exact set replay therefore survives a later
  rebind and restart without new events or CAS writes.
- Text payload limit remains `TEXT_BINDING_MAX_BYTES` (1 MiB); no schema, DTO,
  endpoint, framework, fixture, matrix, pin, or new API was added.
- Full suite was explicitly not requested. Targeted evidence was run centrally
  with explicit file lists only.

## Evidence

AST validation:

```text
PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import ast
from pathlib import Path
for name in ('runtime_protocol/service.py', 'tests/test_shot_text_bindings.py', 'tests/test_timeline_shot_authority.py'):
    ast.parse(Path(name).read_text(encoding='utf-8'), filename=name)
PY
```

Clean central targeted lane:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_shot_text_bindings.py \
  tests/test_shot_candidate_promotion.py \
  tests/test_timeline_shot_authority.py \
  tests/test_timeline_text_binding_clear.py \
  tests/test_timeline_text_legacy_custody.py \
  tests/test_timeline_text_selection.py \
  tests/test_timeline_clip_replacement.py \
  tests/test_render_native_historical_retry.py
```

Result: **181 passed, 15 deselected, 10 xfailed** in 89.60 seconds.
The additional nine-file lane also included `tests/test_project_reference_catalog.py`:
the same 182 passing tests and 10 xfails were reached, but 34 cases errored
before execution because the central runner lacks `/home/user/work/astrid`.
Those errors are environment-dependent Astrid checkout setup failures, not
assertion failures in this resolution.
