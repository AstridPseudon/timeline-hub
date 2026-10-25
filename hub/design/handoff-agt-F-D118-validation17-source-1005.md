# D118 — exact 17 current-replacement source proposal

## Verdict

`PASS_SOURCE_PROPOSAL`, not functional qualification and not retirement. The 17 selectors outside approved D107ten remain historical/archive-read cases until a selector-specific current replacement passes source review and real current execution. The shared Runtime pre-cut-v31 fixture is intentionally authored unpinned; no generator pin-loss defect was found.

The retained D108 run is the exact source of membership: XML SHA-256 `72872c77087719a692bff4b48b8d85ea62b9931d59a502c8e246daee0c81c18a`, 9,269 testcase nodes, D108 outcomes JSON SHA-256 `c180c1c153264d09e2ae79e0ad63007d9551e43e7b72e87973f0927140a6e2eb`. Every row below is an `error` at `astrid/sdk/timeline/validation.py:650`; no current success is inferred from the error count.

## Source conclusion and current path

The original callers use Agent `test_commit_runtime_m1.py`’s `film`/`m1.film` path, Runtime `timeline_commit_film_fixture.py` → `precut_realm_fixture.py`, and the retained archive. The archive retains transcript/text-binding/media/reference/publication/receipt rows, but the historical baseline’s `dependency_manifest.documents` is `[]`; the authored `word:word-1` input therefore intentionally has no authenticated baseline document pin. This is not pin loss by a setup generator.

The genuine current construction is Agent `native_word_anchor_fixture.seed` plus `test_native_word_anchor.py`/`test_word_binding_recipe.py`: Runtime creates the media and transcript, the current provider performs the C0 commits, and a real `clip.anchor` commit carries the exact transcript pin, word IDs and binding. `test_current_pair_reader.py` and `test_m1_legacy_archive_read.py` retain the independent historical/current archive reads. D116’s source correction (commit `45daf7d872ab39c91a1a0d3360d5ec7b15f38b3a`, tree `a878e3fa77fe921600ba1849cd72eccb810b5ba4`) is owned elsewhere and remains sample-blocked; it is a conditional baseline, not proof.

D107’s existing candidate (commit `2e3331ee2f035e302f5ca52488832cd0e22bb3aa`, tree `15876086c532d048c82e32e1b5b1abc6f548fe2f`, candidate hash `7c8a4cc3a0383542999d95762ae77b6ce9468414e3313562b09f0f4c9018cbfc`) has one parametrized current test (two cases). Its actual assertions cover the D107 M1 journey: current pin/binding, independent music-bed/music-other topology, CLI/canonical readback, durable lost-ACK flight, dependent outbox command, restart/realm/actor guards, disjoint/touched conflict, merged retry, inverse/redo/history/inspection. It does not contain any of the exact 17 selectors or their native/frontend/owned/track/scalar predicates.

## Exact per-selector scope

For each row, keep the original selector and original historical/archive read unchanged. Add a new current companion in one new Agent test file, proposed as `tests/editing_conformance/test_d118_current_equivalent.py`, with selector-specific functions/IDs below. The file may share only the D116 current seed after that seed passes source review; it must not share the old `m1.film` baseline. Each companion must submit the same sequence through the registered C0 provider, preserve all original guards/assertions and literal authored words/timing, and independently assert the exact current transcript pin plus authenticated word binding on the actual affected target. No row is approved for retirement by this proposal.

### Native checkout — source `test_commit_runtime_native_checkout.py` (SHA `cf0adf68aa3f1509ea82899c85549d4bed3b32ad84f6c552ce2e026138a29461`)

- **1143** `test_attached_move_trim_lost_ack_restart_original_suffix_and_guarded_undo[False]`: preserve `music-bed` move `on=1`, queued trim `(1,4)`/hold `3`, lost ACK flight/body/key, restart exact retry, disjoint `music-other on=2`, suffix acceptance, reload, undo/redo and guarded second undo. Missing current input is a current-authenticated binding for the actual `music-bed` target plus the current media/topology baseline; D116 currently supplies only the source/pin path, not this target sequence.
- **1147** same selector `[True]`: identical input/assertions, but preserve the touching-peer trim `(0,5)` and conflict/no-write path (`from=1` remains). It needs the same target binding and a source-approved current conflict baseline; do not collapse it into 1143.
- **1152** `test_attached_param_commands_keep_exact_cli_ingress_and_unchanged_write_history`: preserve `_allow_new` opaque literal `[None, False, 0]`, commands-file CLI ingress, unchanged setter as a distinct authored write, clear, undo restoration, and conflict against the first publication. Missing current input is the authenticated target document/binding plus a current parent carrying the exact opaque field; no current D107 predicate covers CLI parameter ingress.
- **1159** `test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable`: preserve Gate3’s occurrence-free/text-card baseline, stopped-renderer tripwire, authenticated `on=1`, reload/undo, and exact `rendering.timeline_visualize` unavailable response. Missing current input is a pinned/bound current baseline compatible with Gate3’s occurrence removal; renderer-off and capability assertions remain unchanged.

### Native frontends — source `test_commit_runtime_native_frontends.py` (SHA `06da641ccf0f3bfcda9b12b3940dea3850d79afbc4fa9be96fab551dc530d4e2`)

- **1165** `test_sheet_lost_ack_attached_suffix_restart_exact_retry_and_peer_guards[False]`: preserve sheet export/edit/apply of `parent/clip:music-bed` to `1`, lost ACK and immutable draft, queued trim suffix with reads/bindings, restart without recapture, disjoint peer, one rebased suffix request, exact bases, and draft bytes. Missing current input is the current target binding plus native-sheet adapter input under the same authenticated document; current D107 is SDK/outbox only.
- **1171** same selector `[True]`: preserve all 1165 assertions but with the touching peer trim and conflict/pending state. It needs its own current target/peer conflict source proof; it is not covered by 1165’s disjoint case.
- **1180** `test_checkout_first_refuses_sheet_suffix_keeps_draft_and_pending_intent`: preserve checkout-first export/apply refusals while an ACK is pending, exact outbox/bundle/draft byte preservation, then exact retry key/body and post-ack original-basis refusal. Missing current input is the authenticated current target plus a native-sheet pending-intent refusal setup; no new refusal reason or guard relaxation is permitted.

### Owned moves — source `test_owned_move_publish_runtime.py` (SHA `7f1860c3a9075d26b5ee80cae68a530b48fcdb60d6450801d5970ea3d22bae70`)

- **2913** `test_http_original_sdk_parent_asset_clear_lost_ack_reload_retry_undo`: preserve trim-ready media baseline, `clip.set clear=['asset']`, exact rationale/key/body, lost-ACK retry and undo to the complete original clip. Missing current input is a current pinned/bound source carried through the trim-ready parent variant.
- **2923** `test_http_original_sdk_parent_transition_clear_lost_ack_reload_retry_undo`: preserve transition `crossfade/.25`, disjoint peer move, `clear=['transition']`, exact retry/rationale, peer preservation and undo. Missing current input is the same authenticated pin/binding on the transition variant; do not use 2913’s variant.
- **2927** `test_http_original_sdk_parent_trim_stale_rebase_lost_ack_reload_retry_undo`: preserve peer move, literal trim inputs `1.0000004`/`4.0000006`, quantized `1.0`/`4.000001`/`3.000001`, lost ACK/rebased receipt, peer preservation and undo. Missing current input is a pinned/bound trim variant with these exact numeric inputs.
- **2940** `test_http_original_sdk_parent_split_stale_rebase_lost_ack_reload_retry_undo`: preserve speed `2`, split at `1`, right id `music-bed-right`, created list, right clip `from=2,to=5.5,hold=3.5`, peer label, rebase, undo removal and peer label. Missing current input is an authenticated split variant retaining exact source window/speed and target binding.
- **2958** `test_http_original_sdk_parent_delete_stale_rebase_lost_ack_reload_retry_undo`: preserve occurrence-free delete variant, exact `clip.delete`, lost ACK/rebase, peer `music-other=2`, absence, undo restoration and peer preservation. Missing current input is the current pin/binding on the occurrence-free variant.
- **2996** `test_http_ambiguous_owner_and_mixed_edits_keep_original_draft`: preserve duplicate display ID across parent/occurrence owners, ambiguous unqualified selection refusal, qualified parent move plus text mixed edit refusal, unchanged outbox/bundle and unchanged history head. Missing current input is an authenticated pinned current closure with the same duplicate-owner topology; this is a negative ownership predicate, not covered by D107’s positive M1 path.

### Parent track/scalar — source hashes are `2a75e2a63df99f26134c56b3833628c696f8be43a8d7dd567e7a03c27010690c`, `1e3517c511a1e6f1090d9d15bf212553762de83cfae40ad330ac77749a0edb91`, and `691046ff5ac691974c221ab992cb362b5153a8099f441c5d8dd57661351c9618`

- **3649** `test_grouped_parent_track_create_move_reload_undo_redo`: preserve grouped `track.create` V3 (`opaque=[None,False]`) plus `music-bed on=1`, exact command grouping/readback, then reload undo to the captured baseline and redo to the exact accepted document. Missing current input is a current pinned/bound baseline that retains the group’s full parent topology.
- **3651** `test_move_then_parent_label_reload_inverse_preserves_newer_disjoint_move`: preserve move to `1`, queued parent-track label `Music`, disjoint `music-other=2`, guarded inverse removing only label, all immutable closure/media pins and exact parent equality. Missing current input is the authenticated current target binding plus label/move baseline.
- **3653** `test_native_label_cli_lost_ack_then_python_suffix_keeps_original_claims`: preserve native CLI empty label lost ACK, Python clear-label suffix, restart retry, disjoint move, exact bases/keys, undo restoring empty label and peer. Missing current input is current pin/binding plus native CLI-to-Python suffix setup; it cannot reuse only D107’s Python outbox path.
- **3654** `test_move_then_scalar_outbox_handoff_reload_and_guarded_inverse`: preserve lost-ACK move, queued scalar track label, restart handoff, exact command serialization/readback, undo/redo, occurrence params with literal null/opaque JSON, clear and undo. Missing current input is current pin/binding on the m1 target plus the occurrence parameter topology; no scalar or import change is proposed.

## Follow-up file scope and gate

One future Agent PR should add only the new D118 companion test file and its source-only current baseline helper if, and only if, D116’s current seed first passes its sample gate. It should not edit the 17 originals, `test_m1_legacy_archive_read.py`, Runtime fixtures/archives, validation, manifests, pins, generated files, ledgers, registries, or production bodies/imports. The original historical tests remain read coverage. A D118 companion is eligible only after AST/selector/assertion containment, exact source/hash review, current pin and binding commits through the registered provider, and targeted execution of every exact replacement; otherwise the row stays `legacy_only_exact_missing`.

No tests/typecheck/lint/full suite were run for this read-only proposal. No worktree source was changed. Evidence is in `workers/agt-F-D118-validation17-source-1005/evidence/source-audit.md`.

## Exact trees

- Agent integration: `e9e3b8f78a103331c38b70c008bf020f13c46413` / `b1d90e5f2cfe42858efb7226c56192b948e1108c`
- Runtime integration: `d23a8e0d24` / `6283b5fbb128447f1b333e0e6af334d35637cf69`
- App integration: `28660e72fa` / `59f8bdd20ebfec9850f90f3b428d230589f0f11d`
- Composition integration: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148`
- Frozen R4 references were read only: SDK `11caf1d9de291d76f491cf69f7942606b7471d7a` / `f6f4fad77ded050b1e9c2d802cc3da35b459e610`; Runtime `31c7ac3a00f7a205f507bf5bd4d4625628d429bd` / `73e676f420ba0545b6eebe45870d532344a9e69b`; App `8f0c2484463e9b666d184a744d52e252984e551a` / `26ad064632fac9ff123670aa7d6ed0e3d8f89178`; Composition `c82eb7c459d0a41263954bf007071a6a0e8e0a6a` / `49975e7a54fd594e1b7fc807681fe28611d57864`.
