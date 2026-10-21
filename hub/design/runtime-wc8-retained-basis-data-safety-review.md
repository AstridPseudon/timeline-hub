# WC8 retained-basis data-safety review

Verdict: **APPROVE** the exact completed candidate for this independent Agent-side data-safety and cross-area authoring review. No concrete data-loss, retry, scope, or unsupported-edit counterexample was found. This approval is not the separately manager-owned live HTTP qualification.

## Candidate identity

The review is against the harness-final implementation, not its implementation base:

- candidate commit: `ac2cdc4ea75e3bd4937b59de139825b4399df42c`
- candidate Git tree: `5efdf07f0a2ac5e1f39f2239e025530a7217368b`
- implementation base (not reviewed as the candidate): `cc37291af12ac6504eb48dd71ea39b9dfdb56d71`, tree `0698a30b3eb42d47db84ed5ed2e21221158795c4`
- candidate branch/worktree was clean and pointed at the candidate commit when checked

Final changed-file SHA-256 values:

```text
89f268acfaf39053467aeee9c0b5d3051d9e96ca8ca831d874853591b9d17bc6  astrid/packs/timeline/cli.py
9d17b60ba5cca1b115763ef7e88ee12ed243948c1af1dfd8c5b23f23bcd54fb8  astrid/sdk/timeline/checkout.py
4cd51a825cf53374558346db8b1d11c1d7c06eb17bb363741edf54861dee8390  astrid/sdk/timeline_sheet.py
c42c1022d0c1c4120b8beba4d95eff395bac88883c19f7b2e0e1830653977446  tests/editing_conformance/test_native_sheet_ordinary_runtime.py
b48b81f221123df1f3689110e960fcf5e538d90cee40d94d84996b5457630ed8  tests/packs/timeline/test_cli_native_sheet.py
7761fee404ac75f0b555354a5c405e94a46d7ae93b74888a197a5dda7ace3c11  tests/sdk/test_timeline_sheet_native.py
```

## Scope and diff review

The exact diff is six paths, `456 insertions / 10 deletions`:

- `astrid/sdk/timeline_sheet.py`
- `astrid/sdk/timeline/checkout.py`
- `astrid/packs/timeline/cli.py`
- `tests/sdk/test_timeline_sheet_native.py`
- `tests/packs/timeline/test_cli_native_sheet.py`
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py`

No source/schema/pin/generated/store/remote path changed. The ordinary-runtime file adds the detached fixture and three detached parameterized cases; its previous ordinary fixture and assertions remain present. No existing positive was removed, skipped, or weakened. The retained legacy `merge_sheet`/`_apply_parsed` consumer remains for the broader local grammar; whole WC8 remains open.

## Safety findings

- Export retention is author-time and bounded to the existing private draft/export/outbox context. A connected checkout must have authenticated Runtime realm/actor, no pending flight, matching verified base parent and equal document content. The outbox retains the native bundle, exact base revision/publication, original sheet text, stable occurrence/clip bindings, and checkout snapshot. No credential or caller authority is serialized.
- The retained slice recognizes only static `am-type` layer duration changes. It requires identical row structure/order and unchanged semantics outside `for`, uses the retained binding, refuses `on`/`until` or nonnumeric/nonstatic shapes, and captures an existing native `clip.set` against the retained bundle. Opaque/null/order fields remain outside the changed semantic cell.
- Unsupported or mixed edits do not become a duration-only Runtime request. They fall through to the existing local sheet grammar; if a retained pending command exists, a changed/unsupported pending text is refused without changing the outbox or draft. The original local-only grammar remains available when no verified retained target exists.
- Save/reload/retry reconstructs the command from the retained native basis and edited text. The existing outbox owns the pending command and exact in-flight body/key; retry does not recapture from a fresh head. Scope checks cover realm, actor, project and timeline, and the original base pair is checked before staging/flushing.
- Same-row conflicts retain the local draft and pending intent. Disjoint edits use the existing guarded Runtime rebase path. Accepted changes retire local draft undo history; undo/redo then use the existing publication/inverse path, not a local rewind.
- CLI routing sends native rows through the existing native path, while the detached duration slice reaches the retained `apply_sheet` bridge. No new writer, store, DTO, API, reconstructed snapshot intent, or fresh-head adoption was introduced. The only replaced consumer is the detached duration seam; broader legacy consumers remain.

## Evidence

Implementation worker final direct command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_sheet.py \
  tests/sdk/test_timeline_sheet_native.py \
  tests/packs/timeline/test_cli_native_sheet.py \
  tests/packs/timeline/test_verbs_working_copy.py \
  tests/sdk/test_timeline_checkout_history_boundaries.py
```

Result: **142 passed in 21.55s**. The direct tests cover retained export/bindings, reload, lost-ACK exact retry, same-row conflict draft retention, disjoint rebase, inverse/redo, local-undo retirement, changed scope, invalid/changed pending text, CLI routing, and local grammar preservation. The worker also recorded `git diff --check`, AST/scope/import/pin/structure checks, and Ruff regression comparison passing.

The corrected integration file collected seven tests (three new detached cases plus four unchanged neighbors), but the obsolete central request `...native7d-sockets-integration-1021052000-2321` exited 4 before collection because its isolated `PYTHONPATH` omitted Runtime. Therefore no live HTTP retry/rebase/inverse result is claimed here.

## Remaining issue / next step

Run the separately manager-owned named lane `rt-wc8-current14-integration` exactly once on this candidate against the current Runtime b92 / published95 artifacts, using only the three new detached-duration nodes. That result is required before any source ACK claims native HTTP qualification. Do not substitute the failed 2321 lane or repeat the prior 142/219 direct runs. No full, browser, renderer, or whole-WC8 closure is claimed.

Independent review complete: **APPROVE**, with the live HTTP qualification and broader legacy-consumer migration still open.
