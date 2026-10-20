# Bounded native sheet: actual Runtime qualification

Worker: `agt-m2-sheet-real-proof`. Agent base `6970b9a2`, worktree `/home/user/work/wt/agt-m2-sheet-real-proof`. Runtime tested at clean `/home/user/work/runtime`, exact HEAD `9f9b25c000485e919f30f1411831fe2d5a3c1316`. **HELD on the M2 branch until PLAN records M1 exit.**

Only repository change: `/home/user/work/wt/agt-m2-sheet-real-proof/tests/editing_conformance/test_sheet_runtime.py` (13 integration cases). No product, sync, pin, generated client, schema, CLI, Runtime or integration-worktree changes. The existing private atomic sheet/outbox seam was sufficient; no approved sync ingress overlay was needed. No adapter defect or generic batch-seam counterexample was found in these cases.

## Actual boundary exercised

The generated Python client's transport callback supplies memory HTTP streams to actual `RuntimeHandler._dispatch`. Its framing, credential checks, route dispatch, service, `load_timeline_commit_provider("astrid")`, native execution/rebase/inverse, SQLite/CAS storage and receipt replay are real. `AstridClient.open` performs normal health validation and a real authenticated handshake with a Runtime-issued owner credential. The in-process harness supplies the handler's daemon-instance health field; it does not alter any contract identity, response or provider result. Disabling the credential gives HTTP 401 even for a previously accepted commit retry, and the outbox remains intact.

Project creation uses `client.projects.create`; timeline creation uses the existing public WorkspaceClient `create_timeline` operation through its `/v1` handler (accessed from the client transport). It installs Runtime's empty verified head. Native `track.create` and `clip.add` commands then seed two literal parent clips, with opaque/null fields, through the public commit operation. There is no legacy seed. `RemoteTimelines.create_empty` still attempts a separate legacy publication in this Agent base and was deliberately not used.

The sheet is built from a public immutable bundle read plus the actual session/history revision+publication pair. Preview and unchanged apply make zero transport calls and leave the outbox bytes unchanged. A clip move plus parent-track label become two original captured commands in **one accepted publication**, with exact stored parent revision, dependency manifest, bundle-codec readback, publisher, records and receipt checks. Accepted inverse and inverse-of-inverse restore exact authored parent state, including unrelated opaque data.

An already-open session sends the sheet's original base pair and guards after another commit. A disjoint move rebases on the server and survives sheet undo. A relevant move conflicts atomically: no label half-write, no history change, original commands/base/flight retained. Changing the sheet header's publication, substituting a changed original bundle, or supplying unrelated pending intent refuses without altering draft bytes, the outbox or accepted history.

**Fresh-session stale-sheet rule:** both a new outbox and reopening the original empty outbox refresh the session to the current head. Applying the old `NativeSheet` then raises `SheetError("sheet and session must share the original project, timeline and basis")`, with no transport calls during apply and no outbox/draft changes. Both disjoint and relevant intervening moves are tested. A tripwire forbids fetching the fresh session bundle in this path. This adapter chooses visible refusal; it does not reconstruct the old sheet over the current bundle or recapture current guards.

Lost acknowledgement is injected only after actual acceptance. RuntimeService is closed/reopened over the same realm, the provider is loaded again, and a fresh public authenticated client and TimelineSession reopen the persisted outbox. Direct `sheet.apply` retries the identical original path/key/body and receives the original receipt without adding history. With a newer local suffix, `sheet.apply` visibly refuses that different pending batch; `session.flush()` retries the stored prefix first. The suffix keeps its original value+identity guards byte-for-byte and is then submitted with the prefix's accepted revision+publication, rebasing across a disjoint peer or conflicting across a relevant one. Changed retry keys refuse locally; a valid changed payload under the original key refuses in the actual Runtime. Exact receipt retry succeeds while provider execution is forbidden.

Renderer calls/imports, `Checkout` construction/save, `publish_bundle`, and Runtime legacy parent publication are tripwired throughout setup, acceptance, readback and inverse. No client three-way merge, fallback writer or renderer is used.

## Evidence

Run from `/home/user/work/wt/agt-m2-sheet-real-proof`, using only the shared Agent venv:

```sh
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_sheet_runtime.py tests/sdk/test_timeline_commit_provider_runtime.py
```

**15 passed in 7.04s** (13 new sheet cases, 2 existing real provider/restart cases).

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_sheet.py tests/sdk/test_timeline_sheet_native.py tests/editing_conformance/test_sheet_native_commands.py tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_recipe_scalar_commands.py tests/sdk/test_timeline_sync.py tests/packs/timeline/test_cli_commit_move.py
```

**323 passed in 11.28s.** Existing CLI/Python/sheet portable goldens, occurrence isolation and guarded undo/rebase remain unchanged.

```sh
/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_sheet_runtime.py
git diff --check
```

Both passed. No tests skipped, disabled, weakened or marked xfail. No full suite, make check, central suite request, socket, browser, install, commit, merge or push was run.

Limits: this new real-service sheet lane exercises parent moves and parent labels; native occurrence moves retain offline/golden coverage rather than a new real-service occurrence journey. Restart means actual service/store close+reopen and new SDK objects in one process, not daemon process death or socket transport recovery. It does not qualify CLI sheet import/export wiring or all legacy sheet operations. Existing broader M1 process/socket lanes were not rerun by this task.

## Capture/export and CLI follow-up

Current import surfaces are `astrid.sdk.timeline_sheet.NativeSheet`, `astrid.sdk.timeline.sync.TimelineSession`, and `astrid.sdk.timeline.capture.capture_move`. The sheet's label capture is `astrid.sdk.timeline._scalar_commands.capture_track_set`; it is **not** exported from `timeline.capture` or the legacy `timeline.__init__` surface. `capture_track_create` is already in `timeline.capture`, and setup's `capture_clip_add` remains in `_clip_commands`. This task adds no exports or convenience methods. The bounded sheet still atomically queues with private `_state`, `_bundle`, locked `outbox` and public `flush`; there is no public generic batch ingress on this base. The CLI/session owner should settle/adopt that batch API rather than duplicate or bypass its rules.

The production CLI consumer remains `/home/user/work/wt/agt-m2-sheet-real-proof/astrid/packs/timeline/cli.py::_cmd_apply` (`apply_sheet` then `Checkout.save`). `cli_show.py::print_sheet` and `timeline_address.py::describe_target` still consume the legacy read projection. Converting apply requires a retained or reconstructible **original immutable bundle and revision+publication pair**, scoped row bindings, one captured batch, durable flight retry before suffix submission, and visible refusal with the edited text kept when the original basis cannot be used. Exported text alone cannot reconstruct the pinned NativeSheet; no persistence format was invented here. Never rebuild a stale edited sheet using a newly fetched current bundle. Keep the existing human/read output compatible when adding the opt-in native export path.

Do not delete legacy `apply_sheet`, its merge helpers, CLI/save consumers or conformance scenarios until all consumers and distinct supported behaviors have native command coverage (or the prescribed strict expected-failure restoration tests). This bounded move+label qualification is not that deletion gate. Recommended next step: the CLI/session owner wires original-basis native export/apply and the batch ingress under its own bounded task; retain this branch hold until the orchestrator records M1 exit.
