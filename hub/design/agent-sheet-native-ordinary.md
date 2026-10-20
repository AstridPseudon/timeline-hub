# Agent ordinary native sheet

This is a bounded port onto Agent `ba5f2756` (assigned integration base), following PLAN.md. That base contains the typed recipes and Session batch ingress but not the previously reviewed NativeSheet. The adapter/parser/CLI seam from `b77d7b5a` is ported into the same existing modules, then extended. There is no new view framework, operation, DTO, schema, SDK alias, client merge, publisher, or restore implementation. AG03/WC7 deletion is **not complete**.

`show TL --as sheet --native` retains the untouched authoring bundle and exact revision/publication in the existing realm/actor/project/timeline outbox before emitting text. `apply TL FILE --native` parses that same view, captures commands against that original, and uses Session.commit_many. `--dry-run` is local preview. The file stays untouched on success and refusal. `# ref` metadata supplies parent or explicit occurrence ownership and clip identity; display IDs are not decoded into identities.

Supported ordinary cells:

| Edit | Existing recipe / semantics |
| --- | --- |
| Start gutter | clip.move, absolute timeline seconds |
| trim=IN..OUT | clip.trim, literal parent media only; source seconds, registry duration and identity retained; scientific notation accepted |
| hold=SECONDS / hold=clear | clip.set, source seconds; clear requires a surviving source window |
| asset=clear / transition=clear | clip.set, removes presence; transition means incoming |
| Built-in scalar literal param / key=clear | clip.set-params, existing declared schema and canvas-unit conversion |
| Parent track label / label=clear | track.set; null, empty and literal "clear" remain distinct |

A multi-cell edit captures each recipe over its preceding local commands, then verifies the complete batch against the original. Session's original-base fence runs under the staging lock, including retry matching. One accepted batch is one publication/undo step. A lost acknowledgement retains its exact body/key across restart; a changed draft cannot replace it. There is no whole-parent write for a no-op. Unchanged numeric spellings do not coerce stored integers/floats. Unknown/namespaced data, opaque parameter JSON, null versus absent fields, source units and rational FPS survive projection and supported edits.

`--clip ID` exports one parent clip; `--occurrence ID [--clip ID]` exports explicit occurrence rows. Selection is retained with the original in the existing outbox and reconstructed on load. Omission of a bound row is refused, rather than treated as deletion. These fragments do not flatten shared shots; sibling occurrences remain unchanged. Named-cut/time/word ranges continue to be positive requirements on the original view and are not claimed for native fragments.

Server rebase is tested for a still-original Session after a disjoint concurrent edit; relevant source-window or parameter conflicts retain pending commands, original pin, flight and file. Conservative existing CLI policy remains: opening an idle Session after another author has moved head refreshes its base, so applying an older export visibly refuses; it does not silently recapture. This is a remaining coverage gap for first-apply CLI stale exports, not AG03 closure. Explicitly original-pinned Sessions and in-flight retries retain their bases.

Still-old callers and requirements, kept for coordinated replacement:

- `astrid/packs/timeline/cli_show.py:print_sheet` -> `timeline_sheet.render_sheet`: named cuts, narration, carried layers, why/deliberate holds, music/end policy, cut/time/word ranges.
- `astrid/packs/timeline/cli.py:_cmd_apply` without `--native` -> `timeline_sheet.apply_sheet` -> `_apply_parsed`, `_apply_sound`, `_update_layer`, `_add_cut`, `_add_layer`; then Checkout.save through the existing working transaction. This is the remaining sheet candidate/client-three-way path.
- `timeline_sheet.apply_sheet` -> `merge_sheet` / `find_version`: old version-based exports and client-side merge. Native rows are explicitly refused at this entry.
- `astrid/packs/timeline/cli.py:_cmd_publish` -> `timeline/publish.py:_PublishMixin.publish` -> `timeline/store.py:publish_bundle` (and `publish.py:_publish_narration`): still-old detached publication after legacy sheet edits. This worker does not change publication, reconciliation or history/restore ownership.
- Held native replacements: narration/gaps; cut/layer creation/deletion/reordering; cut notes and deliberate holds; relational on/until/for, sequences, formulas and moments; sound/look/fades/music/film-end policy; slip; selected media assignment; custom-pack exact-input params; complex parameter authoring; occurrence trim (canonical clip.trim v1 is parent-only); named-cut/time/word fragments; stale first-apply CLI exports.

Original positive legacy tests stay passing and unchanged. Unsupported native edits fail before staging and retain the draft; no generic root replacement supplies missing intention. Bridge/Clip model methods and selected-input infrastructure remain sibling-owned. Retire the listed legacy callers only when their original positive behavior is covered through commands, with the original tests retained.

Validation and exact results are in `workers/agt-m2-sheet-native-ordinary/notes/report.md`. No full suite, integration-worktree changes, push, installation, shared dependency writes or ledger changes are part of this worker.
