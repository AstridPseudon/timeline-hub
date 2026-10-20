# Native sheet on the ordinary Bundle2 SDK

Worker `agt-m2-native-sheet-current`, base Agent `027bd16d96010544331c953c0e1014e161786e71`, unchanged normal Runtime lock `4c145dc62192f0e942e3ee3922a11488aefe9b41`. M2 integration remains HELD. This is a bounded editable-view adapter, not whole Gate 1 or registry coverage. Historical `ecdf018f` tests/results do not qualify this tuple.

## Path and retained intent

`show TL --as sheet --native` creates `NativeSheet.export(session)`. The existing realm/actor/project/timeline-scoped outbox retains one original immutable bundle and its exact revision/publication pair. Export refuses pending/in-flight work before replacement. The adapter copies the input; it never invokes Checkout, journal, publisher or a fallback writer. Its rows reuse the established cut-sheet tokenizer, alignment and JSON literal grammar, with stable owner/ID bindings in `# ref` comments. Native rows cannot enter legacy `apply_sheet`.

`apply TL FILE --native` loads that artifact rather than reconstructing it from current state. Preview diffs the complete row set and emits the registered native command batch once through `execute(original_bundle, raw_commands)`. Commit supplies the captured commands to ordinary `TimelineSession.commit_many`; verification checks existing claims without refreshing them. The optional `base` argument fences the original revision/publication pair under `_stage`'s existing lock, including the retry-matching path. Its post-capture state comparison remains intact. No DTO/schema, endpoint, provider operation or new outbox kind is introduced.

Existing batch/flush mechanics retain the exact flight body/key, retry the original prefix before any suffix, refuse a changed key or changed pending batch, and preserve pending work on conflict. Edited text is never overwritten. Returning the file to unchanged export text cannot hide an outstanding request. A retained export is never promoted to a new basis after acceptance/undo/reload.

The reviewed conservative CLI stale-export behavior is retained: if opening the ordinary session obtains a newer base, apply refuses with the original export/text kept for resolution. A session that still holds the original base can use the existing server's disjoint rebase; no client rebase is added. Local preview continues to describe the original export.

## Bounded cells

* Clip absolute start gutter -> `clip.move` (including existing parent/occurrence behavior).
* Parent track `label=...` -> `track.set`; unquoted `label=clear` removes presence, `label=""` sets the empty string, and `label="clear"` sets a literal string.
* `hold=NUMBER` -> `clip.set` in exact source seconds. `hold=clear` removes hold only when the existing command can retain a source window. Existing timing/occurrence boundaries and compiler quantization remain authoritative; hold is not legacy timeline-duration `for`.
* `asset=clear` and `transition=clear` -> explicit raw field removal through `clip.set`. Assignment, null and empty-string substitution are not supported. Hidden/opaque transition contents survive unless explicitly cleared.
* Plain known built-in literal params -> `clip.set-params`. Existing pure `to_canvas`/`from_canvas` helpers retain canvas-unit semantics. `text=clear`, `text="clear"`, `text=""` and `text="null"` remain distinct. Invalid JSON values fail the existing command schema/value checks.

Omitting a shown property refuses; it never silently clears a value. Unknown and complex parameter values, unsafe parameter names, reserved raw-field parameter collisions and opaque sibling data remain in the original bundle. Opaque/new/selected-pack parameter edits, complex value edits and formula-bound param edits refuse before any queue write. Expressions are not interpreted as literal success. Asset/media assignment and selected-pack inputs remain unsupported on this base; the committed sibling `agt-m2-native-client-inputs` adapter is not an ancestor here and is NOT copied. Future selected inputs must use that adapter and its exact-source restrictions, including the unresolved historical public DocumentPin-read gap.

## Legacy replacement/deletion requirements

All existing `tests/sdk/test_timeline_sheet.py` positive tests remain unchanged and passing. No legacy writer is deleted: coverage below is required first. `apply_sheet`/Checkout remain legacy-only; native requests cannot fall through to them. This is the AG03 deletion mapping, not a claim that AG03 is complete.

| Named requirement before deletion | Existing positive coverage | Current native behavior / replacement needed |
| --- | --- | --- |
| Named-cut script projection, narration gutters, notes and chapter labels | `test_the_sheet_reads_like_a_script`, golden tiny sheet, cut-note tests | Flat bound clips/tracks only; frame/structure edits refuse. Restore a lossless named-cut projection before replacing legacy render. |
| Fragment/range edits and occurrence/cut isolation | fragment, range-list, words/times/cuts tests | Complete export required; CLI selectors refuse. Stable occurrence bindings work, but scoped native fragments need their own proof. |
| Narration text/gaps and transcript/source moment bindings | text/verb/code equivalence, words-of formula, narration tests | Narration/word expressions and formula-bound params refuse. Needs admitted binding commands, not string guessing. |
| Layer/cut add, split, removal, rename and retrack | new-layer/new-cut, Python split, orphan/no-cut and same-name removal tests | Exact bound row set/identity required; additions/removals and ownership/type changes refuse. Existing native operations need thin grammar mapping and distinct positive parity tests. |
| Readability for long/complex values and component JSON edits | `test_detail_prints_long_values_as_editable_json_and_round_trips` | Unknown/complex data preserved; changed complex values refuse. Restore typed literal complex edits before retiring detail editing. |
| Omission clears for look/params and layer deletion | visual look omission-clear, same-name omission deletion tests | Requires explicit clear; omission refuses. Preserve old expectations until an approved lossless replacement supports their behavior. |
| Source trim/slip and sound-row creation | music-bed, independent/anchored sound, sound trim tests | Unsupported row/clauses refuse before queue. Native trim/media creation must be wired and proven without alternate writers. |
| Timing relations and film/music policy | on/until/for, film-end/music-policy tests | Gutter absolute move/source hold only; relational clauses, end/music/scope changes refuse. Needs native intent/compiler support. |
| Audio/visual look, fade curves, and transition authoring | visual looks and curve-only audio-fade tests | Raw incoming transition CLEAR only. Other raw looks/transition assignment/media fade params refuse. No new DSL/op invented. |
| Selected media KEY=HANDLE and custom pack params | named-media and param/key collision tests | Refuse; must consume the active exact-input adapter once composed, never local media/schema authority. |
| Old-export three-way intent merge | legacy versioned merge suite | Native exports keep exact pins/guards and use server rebase or visible stale refusal; no client merge/recapture. Preserve legacy tests until replacement coverage is approved. |

The ~120-line increment target was exceeded because this ordinary base has none of the reviewed native adapter: approximately 170 reviewed adapter lines plus thin CLI/parser support were required before the bounded property widening and atomic basis fence. Final product diff is about 285 added lines across four existing Python files; generated CLI/manifest changes are separate. No new framework/operation/registry claim offsets this coverage gap.

## Evidence and coordination

Exact commands, central result IDs and limitations are in `workers/agt-m2-native-sheet-current/notes/report.md`. Local fakes prove deterministic commands, source-unit clear, presence distinctions, opaque preservation, occurrence/rebase neighbors and inverses. Only the central service runs actual Runtime HTTP/daemon tests. Its matching ordinary Bundle2 cohort is the current-pair evidence; historical source's 20 HTTP cases are not counted. Literal clip.add cannot create a source window: native HTTP hold-clear on a newly added title is correctly unsupported; positive source-window clear is proven in own-repo conformance and existing current-pair scalar-provider cases, without inventing media authority.
