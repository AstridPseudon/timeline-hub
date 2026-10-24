## Result

Qualified cause: the exact two-shared-occurrence path reaches the production caller, but Agent’s inverse/materialization stage emits native-site membership that does not match Runtime’s authenticated source/effect stage. Runtime’s refusal at `timeline_commit_auth.py:1160` is legitimate; no guard waiver or identity inference is justified.

The retained log records:

- Single-occurrence offline control: passes.
- Exact two-occurrence control: `2 failed, 52 deselected`.
- Both failures: `invalid_records: inverse stage native write membership differs from its authenticated stage`.
- The stale expected “ambiguous item path” classification is not the current failure.

Production path confirmed:

`timeline_document.py:281-283` → `emit_document_publish_commands` → `capture_occurrence_swap_media` → `TimelineSession.commit_many` → v2 `_flush` request → Runtime authentication. Undo follows `TimelineSession.undo` → `_flush` → the same Runtime guard.

## Boundary comparison

- Single control removes the second occurrence and recomputes the parent digest. The source-count is one, so no shared-placement fork is materialized.
- Two-occurrence control retains both occurrences sharing `shot-1`. Authoring materialization creates distinct placement-local shot/item mappings for the shared source root.
- The published item path is identity-qualified (`item_id:item-1`); this is not evidence that the current failure is the old numeric-path ambiguity.
- Source arithmetic gives six forward native writes for this fixture: four binding writes, one item-media write, and one final asset write. The inverse should match the authenticated reverse membership.
- Exact native ordinals, ranges, effect tuples, and physical owner/revision tuples were not retained, so they cannot be claimed precisely. Selection is unchanged in the retained fixture; no selection divergence was demonstrated.

The exact missing fact is one retained authenticated prepared/capture packet containing source-stage `native_sites`, inverse-stage binding and ranges, effect sites, recorded writes, and materialization bindings. No new Runtime request is needed; peer 0624 is the existing finite fact request.

## Unapplied scope

For Sol0622: normalize the Agent inverse/materialization/native-stage emission across shared placement-local roots while preserving owner, revision, identity-map, selection/order, ABA, history, and effect attribution guards.

Separately, `assets` and `audio_bindings` still use numeric-index paths and remain counter-scope; no broad audit is warranted.

## Verification

- Source target `1a983fa7c22aec5bc1b6db98d46d8aaed1e6fe03` inspected.
- Source hashes recorded for all four changed files.
- AST/path/effect arithmetic and retained-log consistency checked.
- Worktree remains clean.
- No tests, probes, Node, pytest, browser, full, or gate runs were performed per task restrictions.
- Required `commit-msg` and empty `DONE` markers created.