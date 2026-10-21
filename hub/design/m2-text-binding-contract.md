# M2 text-binding contract (Agent)

Status: settled contract + current frontier, 2026-10-21. Owner: Agent. Runtime response: `runtime-text-binding-P1P2-O1O7-response.md`, against Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d` (tree `6abc2f117391de8e7e35c0283f575a002199894d`).
Historical design branch: `tl/agt-m2-text-binding-design` (worktree `agt-m2-text-binding-design`). Nothing in product code changed by this reconciliation; the original spike remains historical evidence.
Original spike: `tests/editing_conformance/test_recipe_text_binding_spike.py` (22 pass, 1 strict xfail for the Runtime part). Current native/consumer references are listed in §7 and §8.

Keeps main's capability: **exact project-owned UTF-8 text CAS binding, including empty text.**
Agent owns a `text-binding.set` command over the **existing** immutable descriptor. Runtime implements scoped exact UTF-8 text selection through the **existing** media-input validation and retention, plus a recorded before/after binding projection for live readers. No new HTTP endpoint, no new table, no inline text authority, no fake `.config`.

Sources: `managers/runtime/notes/text-binding-projection-seam.md` ("seam note" below), `design/edit-recipe.md`, `design/pack-snapshot-custody.md`, `design/runtime-coordination.md`. Anything not cited is a proposal.

---

## 1. Ground truth (what exists now)

| Fact | Where |
|---|---|
| Retained/pinned binding rows live on the shot: `payload.text_bindings[]`, with Runtime projection fields such as `{binding_id, project_id, shot_id, head, event_stream_id, created_at, updated_at}`. New `timeline.commit` authored rows contain only `{kind, slot, media_id, content_hash, byte_size, mime_type}`; `kind` is prompt, voiceover_script or transcript and `slot` is allowed only for prompt. | Runtime response O1; current Agent `astrid/sdk/timeline/native_text_binding.py:9-12,64-67`; legacy pin path `astrid/sdk/timeline/publish.py:173-189` |
| Text object: `media_id == content_hash == sha256:<digest of UTF-8 bytes>`, `byte_size`, `mime_type`. Empty text is present (size 0); absent means no row. ≤ 1,048,576 bytes, strict UTF-8, no newline normalization. | seam note §Fields |
| Runtime's existing request-scoped `text_selection` accepts exact project-owned UTF-8 text, including size zero, and rechecks the input during acceptance. | Runtime response P1: `runtime_protocol/timeline_commit_port.py:276-283,584-629`; acceptance recheck `:387-403` |
| Binding history and live projection are persisted atomically by the existing acceptance transaction; same-value projection does not advance the live head, while the accepted film record remains. | Runtime response P2: `runtime_protocol/timeline_commit_store.py:712-832` |
| Legacy/native consumers still present: `RemoteShots.set_text_binding` / `rebind_text_binding` (`astrid/sdk/remote.py:2347-2359`); `Timeline.pin_narration` (`publish.py:201-224`); `timeline_document.py:172-200`; `timelines shots text` (`astrid/packs/shots/cli.py:126-138`). | current Agent source |
| Readers: `timelines script` / `RemoteShots._text_binding_content` (pinned, CAS); render admission (`sdk/invocation.py:1345`); live `list/show_text_bindings` (relational). | seam note §Supported reads |
| Main's authoring fixture still carries an **inline** row `{"slot": "voiceover", "text": "hello"}` (`tests/timeline/test_authoring_bundle.py:118`). It has no `kind` and it carries text. | current source; the spike hit it |

## 2. The command

- Operation: `text-binding.set`, `version: "1"`, `schema_version: 1`.
- `select`: `occurrence:<id>`. The settled v1 decision is occurrence ownership: in main, text is owned by the *shot* (`ShotPayload.text_bindings`, natural key `(shot, kind, slot)`), so a clip cannot own it without a new authority field on clips. The occurrence is the stable placement reached through the owner shot, and the command reads `occurrence:o/shot` for ownership.
- `intent`: `{"ownership": "occurrence"}`, fixed for v1. A shared chapter shot affects every occurrence, so `ownership: "shared"` needs its own fixtures and is deferred (O5).
- `args` (closed; the spike's `PARAMETERS` is the executable form):

  ```text
  binding: {kind: prompt|voiceover_script|transcript, slot: null | [a-z][a-z0-9-]{0,63} (prompt only)}
  exactly one of:
    text:  {object_id, digest, size, media_type}
             object_id == digest  (sha256 of UTF-8 bytes; checked by handler)
             size: integer 0..1048576
             media_type: "text/plain; charset=utf-8"   (see O2)
    clear: true
  ```

  No other key is accepted. Neither key, or both, is refused. `clear` is the explicit removal; there is no null sentinel and no universal clear field.

- Descriptor mapping. The command uses the brief's shape, which matches Runtime's closed `VerifiedDocumentObject` (`{object_id,digest,size,media_type}`). The authored row keeps main's field names so existing readers still work:

  | command `text` | authored row (main name) |
  |---|---|
  | `object_id` | `media_id` |
  | `digest` | `content_hash` |
  | `size` | `byte_size` |
  | `media_type` | `mime_type` |

  Plus `kind` and `slot`. `binding_id`, `head`, `event_stream_id` and timestamps are **never authored** (see §5, P3).

### Empty, absent and clear

| State | Command | Authored row | Live (Runtime projection) |
|---|---|---|---|
| absent | none; `clear` on it is refused (`absent_binding`) | no row | no row |
| empty text | `text` with `size: 0`, digest `sha256("")` | row, `byte_size: 0` | present, zero-byte |
| cleared | `clear: true` on a present row | no row | removed; event recorded |

Clear is never encoded as empty text, and empty text is never encoded as absence. The spike asserts all three transitions and that undoing a clear restores the present zero-byte row, not absence.

## 3. Recorded facts, guards, rebase, inverse (edit recipe §4.1 applied)

- **reads**: `occurrence:o/shot` `shot_id` (ownership); `occurrence:o/text-binding:<key>` prior tagged state (absent or exact row).
- **expect / authorship**: the prior tagged row, `direct`, at `occurrence:o/text-binding:<key>::`.
- **writes**: exactly one per command, at its ordinal. An explicit same-value set is still a write with `before == after`.
- **dependencies**: the text object as `{key: "text:<digest>", kind: "media", pin: {object_id,digest,size,media_type}, policy: "exact"}`. This is the scoped, immutable input that Runtime must retain.
- **created**: none. A binding is a keyed singleton, not an allocated identity.
- **selections**: none in v1 (singleton). The recorded collection membership/order is the O4 selection authority.
- **bindings**: none. Text is not an anchor.
- **rebase**: the same key with different content refuses (`dependency_changed`). A disjoint key rebases. A head that already holds the identical row passes, because the guard is equality.
- **accepted inverse**: restores the prior tagged state exactly, guarded by the target write. Any intervening write to the key refuses (`intervening_write`), including an A→A write. This follows the recipe's ABA rule and is separate from the dependent-handoff rule.
- **redo**: a new guarded inverse, not a snapshot replay.

## 4. Gap disposition after the Runtime response

| Id | Gap | Where | Status |
|---|---|---|---|
| G-SCHEMA | The canonical Agent schema admits `occurrence:<id>/text-binding:<key>` and the closed `text-binding.set` args. Runtime ACKs the scoped shape; official Runtime generation, artifact identity and coordinated pins remain separate. | `astrid/core/timeline/schema/edit-command.schema.json:43-69,1842-1865,2575-2660`; Runtime response O7 | Settled semantically; public matched qualification remains open. |
| G-STATE | Keyed rows over `payload.text_bindings` are implemented in the Agent state layer. | `astrid/sdk/timeline/_command_state.py:367-388` | Settled for the current exclusive-occurrence command. |
| G-OP | `text-binding.set` is registered with fixed occurrence ownership and the canonical schema. | `astrid/sdk/timeline/commands.py:58-62`; schema `:1842-1865` | Settled for the current command. |
| G-INV1 | Keyed singleton clear/inverse restores the exact prior row and list position. | `astrid/sdk/timeline/_command_state.py:367-388`; `tests/editing_conformance/test_recipe_text_binding_native.py::test_empty_clear_and_original_noncanonical_order` | Settled for the current command. |
| G-INV2 | `apply_inverse` crashes on a recorded absent→absent write at path `[]` (`KeyError: 'value'`). This is generic: any explicit no-op removal of an absent entity. | `inverse.py:146` (reproduced by the spike before the design change) | **Not** patched. This op avoids it by refusing clear-of-absent. The generic fix is a separate item. |
| G-LEGACY | Legacy inline rows (`{slot,text}`) remain non-authority for the native path. Runtime will not auto-migrate them; existing Main inline/catalog positives and legacy callers stay live/held until an explicit Agent-owned recorded migration preserves them. | `tests/timeline/test_authoring_bundle.py:118`; `tests/editing_conformance/test_recipe_text_binding_spike.py::test_legacy_inline_row_is_refused_not_read_as_authority`; Runtime response O6 | Open (O6). |
| G-RT1 | Runtime now declares exact scoped UTF-8 selection and acceptance recheck; qualification against the matched public tuple remains open. | Runtime response P1/P2; `tests/editing_conformance/test_commit_runtime_text_binding.py::test_runtime_declares_and_captures_exact_text_port`, `::test_text_input_is_reverified_at_atomic_acceptance` | Open only as qualification, not as a shape gap. |

## 5. Settled Runtime boundary

**P1. Existing internal port method, no HTTP route.** Runtime has this method on the existing request-scoped commit port. The project comes from the authenticated commit scope, never the body.

```text
text_selection(selection: TextSelection) -> VerifiedText        # RuntimeCommitPort, internal
TextSelection = {object_id: Digest, digest: Digest, size: int 0..1048576, media_type: "text/plain; charset=utf-8"}  # closed
VerifiedText  = {object_id, digest, size, media_type, utf8: true}                                          # closed, no bytes
```

Checks: managed project CAS object; `object_id == digest == sha256(bytes)`; size equal; exact media type; strict UTF-8 decode; size ≤ 1 MiB; zero size allowed. Validation and retention use the existing media-input path, with no new table. Re-verified at acceptance. Missing, foreign or mismatched objects get the existing refusal reasons. Runtime source: `runtime_protocol/timeline_commit_port.py:276-283,584-629`; acceptance recheck `:387-403`.

**P2. Recorded before/after binding projection, derived by the server.** For each accepted `text-binding` write, Runtime does this in the existing acceptance transaction:
- resolves the owner occurrence to its accepted shot identity from the accepted closure, and refuses if that differs from the one the command read;
- compares the before state with the current live row and refuses on mismatch (the server-side guard; no silent overwrite);
- writes the live row or removes it, advances the binding's stream head by one (unchanged on A→A), and appends `shot.text_binding` to `binding_id + ":shot.text_binding"` with the publication id;
- undo and redo produce their own projection events. History is never rewound (seam note).

No client-supplied projection field. The projection is derived, not trusted. Runtime source: `runtime_protocol/timeline_commit_store.py:712-832`.

**P3. Authored rows carry identity only.** `head` is known only after acceptance, so an authored row cannot contain it. Pinned readers (`timelines script`, render) use the immutable identity (CAS bytes). Live readers (`list/show_text_bindings`, a generic open) take `binding_id` and `head` from the projection, which keeps the seam's rule that a generic open selects the current binding and a pinned script keeps its historical descriptor. This changes main's pinned rows, which currently include `binding_id` and `head` (`publish.py:186`). See O1.

**No new endpoint, no new table, no new journal, no retired-service call.** Runtime reuses `_persist_closure` and existing binding tables/read validators. Historical reuse does not repoint global projections.

## 6. Writers to retire (deletion ledger)

Replaced by `text-binding.set` (rebind is a `set` with a new descriptor; the `rebound` event is Runtime's projection):
- `RemoteShots.set_text_binding` / `rebind_text_binding` (`astrid/sdk/remote.py:2347-2359`);
- `Timeline.pin_narration` (`astrid/sdk/timeline/publish.py:201-224`), which becomes recorded commands in the same commit;
- `astrid/packs/rendering/docs/scripts/timeline_document.py:172-200`;
- `timelines shots text set` (`astrid/packs/shots/cli.py:126-138`).

Nothing is deleted by this design. The row in `design/deletion-ledger.agent.md` remains `HELD`; O6 legacy migration and O7 public generation/pin/qualification are prerequisites for any writer retirement.

## 7. Settled dispositions and remaining proof

- **O1 — settled for new commands.** Authored rows are identity-only. Runtime projection fields remain derived; old pinned rows remain read-only compatibility data. Runtime refs: `runtime_protocol/timeline_commit_store.py:834-856`, `service.py:3662-3689`; legacy pin validation at `service.py:1465-1502` remains pin-oriented.
- **O2 — settled split.** New selections use `text/plain; charset=utf-8`; authenticated retained descriptors may remain `text/plain`. New-input schema: `astrid/core/timeline/schema/edit-command.schema.json:2631-2655`; current legacy read presentation: `astrid/sdk/media_open.py:327-337`.
- **O3 — settled for v1.** The command selects `occurrence:<id>` and Runtime resolves the accepted shot owner. No clip/element text authority is introduced. Agent: `astrid/sdk/timeline/native_text_binding.py:36-45`; Runtime: `timeline_commit_store.py:749-764`.
- **O4 — settled for v1.** Recorded collection membership/order is authoritative; no Runtime canonical sort or order field. Agent: `native_text_binding.py:45-67`; inverse: `_command_state.py:367-388`; current proof refs include `tests/editing_conformance/test_recipe_text_binding_native.py::test_empty_clear_and_original_noncanonical_order` and `tests/editing_conformance/test_commit_runtime_text_binding.py::test_disjoint_first_birth_rebase_keeps_captured_intent_and_actual_order`.
- **O5 — held scope.** Only exclusive occurrence ownership is acknowledged. Shared ownership remains unqualified and must not close this ledger or retire shared/legacy positives. Agent refusal: `native_text_binding.py:39-43`; current negative: `tests/editing_conformance/test_recipe_text_binding_native.py::test_shared_source_is_refused_even_after_authoring_aliases_materialize`.
- **O6 — open owner work.** Runtime will not auto-migrate inline rows or add a writer. Keep Main inline/catalog positives and legacy consumers live/held until an explicit Agent-owned recorded migration preserves them. Exact remaining refs: `tests/timeline/test_authoring_bundle.py:118`, `tests/timeline/test_authoring_media.py:578-615`, `astrid/sdk/remote.py:2347-2359`, `astrid/sdk/timeline/publish.py:201-224`, `astrid/packs/rendering/docs/scripts/timeline_document.py:172-200`, and Runtime `tests/test_shot_text_bindings.py::test_set_is_deterministic_project_scoped_and_replays`, `::test_set_rebind_and_event_order`, `::test_invalid_utf8_and_size_are_zero_write`, `::test_identity_digest_is_sha256`.
- **O7 — ACK, not release authorization.** Runtime ACKs P1/P2 and the current scoped semantic shape. Agent owns canonical semantic source; Runtime owns normal official generation, artifact digest/version and coordinated pins. Remaining proof is the matched public tuple plus native/consumer qualification, not a new schema, DTO, endpoint, port, journal or generation design.

## 8. Evidence

Run from the worktree, venv Python (`/home/user/work/venv-agent/bin/python`):

- `pytest -q tests/editing_conformance/test_recipe_text_binding_spike.py` → **22 passed, 1 xfailed** (`test_runtime_port_declares_exact_text_selection`, strict, raises ImportError/AssertionError; reason names G-RT1).
- `pytest -q tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_recipe_text_binding_spike.py tests/editing_conformance/test_runner_selftest.py` → **108 passed, 1 xfailed** (the seam does not leak).
- `ruff check --isolated --select E4,E7,E9,F,I,BLE` on the spike → passed.

What the native tests prove: the command's closed arguments, exact round trip, dependency record, exact inverse and redo, empty-vs-clear-vs-absent, same-value recording, intervening-write refusal, guard refusal, exclusive ownership and disjoint rebase. Runtime-facing tests additionally cover exact project text selection, acceptance recheck, live projection, retry, restart and retained descriptor behavior. These are source/test references; they are not a claim of matched public-tuple qualification.

What remains unproved: a fresh qualification run on the final matched public Agent/Runtime tuple, coordinated generated artifact/version and pins, and consumer cutover. App/browser/native/live installation/full runs are outside this contract reconciliation. Legacy Main inline/catalog positives and the native original positives remain open until that matched proof.
