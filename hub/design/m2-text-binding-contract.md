# M2 text-binding contract (Agent)

Status: design + executable spike, 2026-10-20. Owner: Agent. Decision: orchestrator 01:28Z `project-catalog-and-text-source`, item 2.
Branch: `tl/agt-m2-text-binding-design` (worktree `agt-m2-text-binding-design`). Nothing in product code changed; the spike is test-local.
Spike: `tests/editing_conformance/test_recipe_text_binding_spike.py` (22 pass, 1 strict xfail for the Runtime part).

Keeps main's capability: **exact project-owned UTF-8 text CAS binding, including empty text.**
Agent owns a `text-binding.set` command over the **existing** immutable descriptor. Runtime adds scoped exact UTF-8 text selection through the **existing** media-input validation and retention, plus a recorded before/after binding projection for live readers. No new HTTP endpoint, no new table, no inline text authority, no fake `.config`.

Sources: `managers/runtime/notes/text-binding-projection-seam.md` ("seam note" below), `design/edit-recipe.md`, `design/pack-snapshot-custody.md`, `design/runtime-coordination.md`. Anything not cited is a proposal.

---

## 1. Ground truth (what exists now)

| Fact | Where |
|---|---|
| Binding rows live on the shot: `payload.text_bindings[]`, each `{binding_id, project_id, shot_id, kind, slot, media_id, content_hash, byte_size, mime_type, head, event_stream_id, created_at, updated_at}`. `kind` is prompt, voiceover_script or transcript; `slot` is allowed only for prompt. | seam note §Fields; `astrid/sdk/timeline/publish.py:173-189` pins the full row into the payload |
| Text object: `media_id == content_hash == sha256:<digest of UTF-8 bytes>`, `byte_size`, `mime_type`. Empty text is present (size 0); absent means no row. ≤ 1,048,576 bytes, strict UTF-8, no newline normalization. | seam note §Fields |
| Runtime's `selected_media` rejects text MIME and zero-byte objects. First-use text cannot reach sole acceptance today (counterexample C1). | seam note C1 (`timeline_commit_port.py`, cited there as port.py:560) |
| Binding history is not persisted by `_persist_closure`; a current-row upsert cannot reproduce the event chain (C2). Promotion/historical reuse can repoint live projections (C4). | seam note C2, C4 |
| Writers in use: `RemoteShots.set_text_binding` / `rebind_text_binding` (`astrid/sdk/remote.py:2446,2456`); `Timeline.pin_narration` (`publish.py:173`); `timeline_document.py:179`; `timelines shots text` (`astrid/packs/shots/cli.py:135`). | grep |
| Readers: `timelines script` / `RemoteShots._text_binding_content` (pinned, CAS); render admission (`sdk/invocation.py:1345`); live `list/show_text_bindings` (relational). | seam note §Supported reads |
| Main's authoring fixture still carries an **inline** row `{"slot": "voiceover", "text": "hello"}` (`tests/timeline/test_authoring_bundle.py:120`). It has no `kind` and it carries text. | grep; the spike hit it |

## 2. The command

- Operation: `text-binding.set`, `version: "1"`, `schema_version: 1`.
- `select`: `occurrence:<id>`. **Deviation from the brief, for the orchestrator to confirm:** the brief says "clip/element ref by stable id". In main, text is owned by the *shot* (`ShotPayload.text_bindings`, natural key `(shot, kind, slot)`), so a clip cannot own it without a new authority field on clips. The occurrence is the stable placement reached through the owner shot, and the command reads `occurrence:o/shot` for ownership.
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
- **selections**: none in v1 (singleton). Order is open (O4).
- **bindings**: none. Text is not an anchor.
- **rebase**: the same key with different content refuses (`dependency_changed`). A disjoint key rebases. A head that already holds the identical row passes, because the guard is equality.
- **accepted inverse**: restores the prior tagged state exactly, guarded by the target write. Any intervening write to the key refuses (`intervening_write`), including an A→A write. This follows the recipe's ABA rule and is separate from the dependent-handoff rule.
- **redo**: a new guarded inverse, not a snapshot replay.

## 4. Gaps the spike found (each is a named change, not a workaround)

| Id | Gap | Where | Status |
|---|---|---|---|
| G-SCHEMA | Scoped-ref patterns (`TargetKey`, `ScopedId`, `EntityRef`) admit only clip, track, shot and registry. `occurrence:o/text-binding:<key>` is refused by the top-level validator before any handler runs. The popup worker reported the same gap for `occurrence:…/asset:…`. Runtime's byte-identical pinned copy must regenerate with it. | `astrid/core/timeline/schema/edit-command.schema.json` | Spike widens the patterns in its own validator copy only. |
| G-STATE | `State.entity` / `State.set` have no keyed-row kind over `payload.text_bindings`. | `_command_state.py:146-252` | Spike patches it test-locally. |
| G-OP | `validate_command` allowlist and `operations()` have no text op. Intent must equal the op's fixed intent. | `commands.py:34-38,62,136-138` | Spike patches it test-locally. |
| G-INV1 | Undoing a removal of a path-`[]` entity goes through `ctx.create`, which requires an authored collection. A keyed singleton has none, so undoing a clear would fail. | `inverse.py:144-146`; `_recording.py:86-87` (read, not run) | Spike restores by assignment through a test-local `create`. Product fix: restore keyed singletons by assignment. |
| G-INV2 | `apply_inverse` crashes on a recorded absent→absent write at path `[]` (`KeyError: 'value'`). This is generic: any explicit no-op removal of an absent entity. | `inverse.py:146` (reproduced by the spike before the design change) | **Not** patched. This op avoids it by refusing clear-of-absent. The generic fix is a separate item. |
| G-LEGACY | Legacy inline rows (`{slot,text}`) are refused as `unsupported_shape`. They are not authority. Migrating them is a recorded command, not designed here. | `tests/timeline/test_authoring_bundle.py:120`; spike `test_legacy_inline_row_is_refused_not_read_as_authority` | Open (O6). |
| G-RT1 | No scoped exact UTF-8 text selection on Runtime (§5, P1). | seam note C1 | Strict xfail in the spike. |

## 5. What Runtime must add (proposal for the Runtime owner)

**P1. One internal port method, no HTTP route.** Shaped like the five-field `selected_media` read, minus catalog fields. The project comes from the authenticated commit scope, never the body.

```text
text_selection(selection: TextSelection) -> VerifiedText        # RuntimeCommitPort, internal
TextSelection = {object_id: Digest, digest: Digest, size: int 0..1048576, media_type: "text/plain; charset=utf-8"}  # closed
VerifiedText  = {object_id, digest, size, media_type, utf8: true}                                          # closed, no bytes
```

Checks: managed project CAS object; `object_id == digest == sha256(bytes)`; size equal; exact media type; strict UTF-8 decode; size ≤ 1 MiB; zero size allowed. Validation and retention go through the existing media-input path, with no new table. Re-verified at acceptance. Missing, foreign or mismatched objects get the existing refusal reasons. Runtime owns the port declaration in `runtime_protocol/timeline_commit.py` (custody doc §8).

**P2. Recorded before/after binding projection, derived by the server.** For each accepted `text-binding` write, Runtime, in the same acceptance transaction:
- resolves the owner occurrence to its accepted shot identity from the accepted closure, and refuses if that differs from the one the command read;
- compares the before state with the current live row and refuses on mismatch (the server-side guard; no silent overwrite);
- writes the live row or removes it, advances the binding's stream head by one (unchanged on A→A), and appends `shot.text_binding` to `binding_id + ":shot.text_binding"` with the publication id;
- undo and redo produce their own projection events. History is never rewound (seam note).

No client-supplied projection field. The projection is derived, not trusted.

**P3. Authored rows carry identity only.** `head` is known only after acceptance, so an authored row cannot contain it. Pinned readers (`timelines script`, render) use the immutable identity (CAS bytes). Live readers (`list/show_text_bindings`, a generic open) take `binding_id` and `head` from the projection, which keeps the seam's rule that a generic open selects the current binding and a pinned script keeps its historical descriptor. This changes main's pinned rows, which currently include `binding_id` and `head` (`publish.py:186`). See O1.

**No new endpoint, no new table, no retired-service call.** Runtime reuses `_persist_closure` and the existing binding tables and read validators (seam note step 2). Historical reuse does not repoint global projections (manager clarification, seam note line 56).

## 6. Writers to retire (deletion ledger)

Replaced by `text-binding.set` (rebind is a `set` with a new descriptor; the `rebound` event is Runtime's projection):
- `RemoteShots.set_text_binding` / `rebind_text_binding` (`astrid/sdk/remote.py:2446,2456`);
- `Timeline.pin_narration` (`astrid/sdk/timeline/publish.py:173-189`), which becomes recorded commands in the same commit;
- `astrid/packs/rendering/docs/scripts/timeline_document.py:179-185`;
- `timelines shots text` (`astrid/packs/shots/cli.py:135`).

Nothing is deleted by this design. The row in `design/deletion-ledger.agent.md` is `held`.

## 7. Open decisions (orchestrator)

- **O1.** Authored rows are identity-only (P3), not main's current pinned rows with `binding_id` and `head`. Recommended. It is a compatibility change for `timelines script` and pinned readers.
- **O2.** MIME string. The brief says `text/plain; charset=utf-8`. Main's preview uses `text/plain` (`astrid/sdk/media_open.py:331`). Runtime must confirm which exact string it stores for text objects. The spike uses the brief's.
- **O3.** `select` is the occurrence, not a clip or element (§2). The brief's wording is not met literally.
- **O4.** Order of `text_bindings`. Undoing a clear must restore the row's position. Recommended: canonical order by `(kind, slot)`, so presence alone fixes position. Alternative: a recorded membership selection. Not spiked.
- **O5.** Shared-chapter ownership (`ownership: "shared"`) is deferred until it has fixtures showing the sibling effect.
- **O6.** Owner and timing of migrating legacy inline rows (G-LEGACY), as a recorded command.
- **O7.** Runtime owner ACK for P1 and P2, and regeneration of the pinned schema with G-SCHEMA.

## 8. Evidence

Run from the worktree, venv Python (`/home/user/work/venv-agent/bin/python`):

- `pytest -q tests/editing_conformance/test_recipe_text_binding_spike.py` → **22 passed, 1 xfailed** (`test_runtime_port_declares_exact_text_selection`, strict, raises ImportError/AssertionError; reason names G-RT1).
- `pytest -q tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_recipe_text_binding_spike.py tests/editing_conformance/test_runner_selftest.py` → **108 passed, 1 xfailed** (the seam does not leak).
- `ruff check --isolated --select E4,E7,E9,F,I,BLE` on the spike → passed.

What the spike proves: the command's closed arguments, exact round trip, dependency record, exact inverse and redo, empty-vs-clear-vs-absent, same-value recording, intervening-write refusal, guard refusal and disjoint rebase. Each on the real recipe harness, with a stub descriptor.

What it does not prove: Runtime acceptance, CAS bytes, relational projections, App, or any `ASTRID_RUNTIME` journey. The one Runtime-dependent assertion is a presence check, not an acceptance proof.
