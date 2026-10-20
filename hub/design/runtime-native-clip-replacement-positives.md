# Runtime D04/RT02 native clip-replacement positives

## Result

Added native Runtime integration coverage in `tests/test_timeline_clip_replacement.py` using the prepared ordinary Agent source and the normal Runtime bootstrap path. The fixture creates a real project/timeline, imports real project-owned video/audio through Runtime media import, creates an occurrence with native `occurrence.create`, and adds a real occurrence-owned clip before exercising native media swap.

The native route tuple is:

```text
(project=<Runtime-created project UUID>, timeline=film,
 occurrence=native-occurrence, occurrence_clip=native-clip,
 parent_clip=native-parent-clip, track=picture/overlay,
 clipType=video, at=2, hold=3, from=1, to=4,
 occurrence_duration=5,
 old=(asset=old variant_id, generation_id, variant_id, object_id, catalog_digest),
 new=(asset=new variant_id, generation_id, variant_id, object_id, catalog_digest))
```

The media tuple is always the exact five-field Runtime selection plus the separately read verified-media record; no fake provider, SQL acceptance, inline authority, or schema overlay is used. Occurrence edits are explicit `occurrence` ownership, exclusive, translation-only (`source_offset=0`, `speed=1`), and project-scoped. Parent replacement uses `clip.swap-media` with explicit `parent` ownership and a separate parent-owned overlay track.

## Original-to-native mapping

| Original test | Native replacement | Result |
| --- | --- | --- |
| `test_replace_timeline_clip_is_atomic_cas_and_exactly_replayable` | `test_native_clip_swap_is_atomic_cas_and_exactly_replayable`; parent route also covered by `test_native_parent_clip_swap_route_replaces_parent_media` | Qualified on candidate; exact retry, changed-key conflict, and stale-head refusal asserted |
| `test_replace_timeline_clip_rejects_cross_project_source` | `test_native_clip_swap_rejects_cross_project_source_without_mutation` | Pass; no SQLite dump changes |
| `test_replace_timeline_clip_rejects_malformed_source_without_mutation` | `test_native_clip_swap_rejects_malformed_source_before_native_commit` | Pass; real media import rejects undecodable bytes before native commit |
| `test_replace_timeline_clip_rejects_tampered_cas_without_mutation` | `test_native_clip_swap_rejects_tampered_cas_without_mutation` | Strict xfail retained; candidate selection currently does not rehash tampered CAS bytes |
| `test_replace_timeline_clip_rejects_wrong_stream_without_mutation` | `test_native_clip_swap_rejects_wrong_stream_without_mutation` | Pass; video target refuses audio selection |
| `test_replace_timeline_clip_rejects_too_short_source_without_mutation` | `test_native_clip_swap_rejects_too_short_or_end_short_source[1]` | Pass |
| `test_replace_timeline_clip_requires_source_to_reach_authored_end` | `test_native_clip_swap_rejects_too_short_or_end_short_source[3.5]` | Pass |
| `test_replace_timeline_clip_generic_visual_media_requires_video_stream` | `test_native_generic_visual_media_requires_video_stream` | Pass; native capture refuses audio with the strong `image/video` error |
| `test_replace_timeline_clip_replays_after_intervening_edit_and_reopen` | `test_native_clip_swap_replays_after_intervening_edit_and_reopen` | Pass; exact replay survives intervening native edit and Runtime reopen |
| `test_replace_timeline_clip_public_http_route` | `test_native_clip_swap_public_http_route` | Pass through the public HTTP `/commit` route |

Raw counts: 10 original cases remain unchanged; 10 candidate native non-HTTP cases (the duration/end pair is parameterized) produced 9 passes and 1 strict xfail; the final public HTTP node produced 1 pass. On unchanged public Runtime 0.2.13, the parent route is conditionally xfailed because its request schema still excludes `ownership=parent`; the prepared 0.2.14 candidate passed that route.

## Ledger state and exact open request

D04 remains held for the tampered-CAS proof. Exact counterexample: import and select `old`, read its verified selection, overwrite `service.cas.path_for(old.object_id.removeprefix("sha256:"))` with `b"tampered"`, then submit the captured native `occurrence.swap-media` with the unchanged exact selection. The candidate's Runtime selection/acceptance path does not detect the byte mismatch, so the strong refusal expectation remains a strict xfail. Agent/Runtime owners should add immutable CAS-byte rehashing to the selected-media acceptance proof before removing that xfail.

The original legacy bodies and strict retirement markers remain unchanged; no retired-writer test was made green by weakening its expectation.

## Test evidence

- Candidate direct native lane: `9 passed, 1 xfailed` (tampered CAS only), using Runtime candidate archive `candidate-0.2.14` and prepared Agent source archive.
- Local public-runtime native lane: `8 passed, 2 xfailed` (parent schema gap and tampered CAS).
- Untouched legacy non-HTTP lane: `9 xfailed`, with the original D04 strict expectations intact.
- Central final HTTP node: `1 passed` via `marked-integration` with explicit file `tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route`.
- `py_compile` and `git diff --check`: passed.

No full/broad/render suite was run. An attempted frozen HTTP lane was unavailable because `/home/user/work/wt/agt-m2-bundle2-official-pin` does not exist; the available central marked-integration lane supplied the final HTTP evidence.
