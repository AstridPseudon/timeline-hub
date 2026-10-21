# WC5 original22 positive preservation map

Date: 2026-10-21 UTC. This is a source-to-proof map only. It does not change
the original tests, activate the requester, run the outer action, or claim a
Runtime commit.

## Bound source versions

| source | exact identity | role |
| --- | --- | --- |
| Original positive file | R4 candidate SDK `11caf1d9de291d76f491cf69f7942606b7471d7a`; file blob `89f2ae1213e158b8b2042bbb9fc19fe2400926b3` | `tests/packs/video_editing/test_draft_voiceover.py`; 22 collected cases (the two- and five-way parametrizations included) |
| Dormant requester source | f07 `f07d97715fbe4efcb80e2db40ef4597e81f75547`; tree `fb785ef2f9b4bafcfde9b15eacb5f8e3025e3e17` | reviewed source join |
| Current requester source | 8a6 `8a6f1024651b9ecb481e2a6cf5258c7598f65deb`; tree `3d0c76ec570046036979b93794e517744a9a3301` | f07 join on the current safety base |
| Repaired real fixture | 2242 `2242bf7d401de86019fc39d110bab64fc0ccd240`; tree `cd4df494d9eabf563400a2040d9fe7ef6e0a6cc1`; fixture blob `9f1bf6e43900af35086d9ef359d3f27be01927dd` | source/preflight-approved outer lifecycle carrier |
| Runtime counterpart named by the fixture | `42a7203f49bb89f299ec854cfbf2b1444e815a7c`; tree `1f220b3d3a27e8eb061b15c944bad784c8fdb82e` | exact Runtime source expected by the later selector |

The six f07/8a6 requester feature blobs are byte-identical: the action
context, outer action runner, `pack.yaml`, `draft_voiceover.py`,
`settled_voiceover_input.py`, and `voiceover_requester.py`. The public wrapper
does not set `requester_entry`; no live public caller is established by these
sources.

## The one-to-one carrier chain

```text
original candidate + pinned script
  -> outer video_editing.sync_draft_voiceover
  -> requester-owned inner generation.generate_speech results
  -> Runtime task/result/managed-output reread
  -> exact five-field media selection + verified WAV bytes/size/hash/intrinsic duration
  -> one CAS settled_speech_input descriptor
  -> normal outer admission and settled timeline/authoring-proposal output
  -> proposal validation (six keys, digest, rationale, outer producer/target)
  -> TimelineSession.queue_proposal -> durable outbox -> flush
  -> producer.guard + proposal commands -> accepted revision/publication receipt
  -> history/readback -> guarded inverse
```

The inner identity is only `generation.generate_speech` task/run/attempt/output
provenance. The outer producer identity is the host-fenced
`video_editing.sync_draft_voiceover` task/run/attempt and its admitted
project/timeline/base revision/base publication. The source never equates the
two. `_read_authoritative_media_info` is the authority for selection and
intrinsic duration; the JSON settled bundle is only an ordered locator and
does not supply either value.

The outer source path is concrete in 8a6:

- `draft_voiceover._sync_draft_voiceover(..., requester_entry=True)` forwards
  the candidate, pinned scripts, four-field admitted target, timing policy,
  selection options, padding, and outbox path.
- `voiceover_requester._prepare_requester_speech_inputs` invokes the inner
  speech capability, rereads the exact task/output/media facts, and imports
  one ordered CAS bundle.
- `_requester_sync_draft_voiceover` admits the registered outer executor,
  observes exactly one managed `authoring_proposal`, validates its target and
  proposal digest, opens `TimelineSession`, queues the unchanged proposal, and
  flushes once.
- `capture_draft_voiceover` emits existing native commands for literal
  occurrence timing, audio add/swap, and the `draft_voiceover` metadata leaf;
  `build_producer_batch` adds the one outer `producer.guard` at submission.

2242 statically checks this chain and its source prerequisites. Its later
selector is `test_wc5_real_runtime_outer_lifecycle`; the source/preflight
test explicitly asserts that it is not executed during preflight. The review
result was **1 source/preflight test passed**, fresh pinned Runtime import and
collection passed, and no daemon/host/HTTP/native/model/render/body ran.

## Original22 map

Status terms:

- **preserved/offline**: the original path remains in the unchanged public
  preparation source and was previously covered by the original focused lane;
  this is not outer Runtime proof.
- **carrier-described**: 8a6 and/or 2242 contain the actual outer/requester
  carrier for the fact, but the 2242 lifecycle body has not run.
- **not covered**: the 2242 source does not assert this original fact, or the
  exact source fixture differs. It must not be inferred from a source string,
  a mocked offline test, or a different native fixture.
- **semantic gap**: the current native command source cannot represent the
  original authored change. It remains a visible gap; no assertion is removed
  or converted to refusal here.

| case | original positive assertion/path | existing carrier and exact preservation meaning | outer proof / gap |
| --- | --- | --- | --- |
| 1 | `test_exact_words_voice_and_selected_identity_reuse`: unchanged text yields no jobs and both `reused`; changed first text yields one job; settings change yields two; changing the second selected media identity yields two. | `plan_draft_voiceover` binds the exact pinned script row, normalized settings, selected audio identity, occurrence, and old media. The requester repeats the same plan before creating ordered inner speech inputs. | **Not covered** by 2242's one-occurrence `New narration` seed. The 2-occurrence reuse/selection matrix needs a later body assertion; no source gap found. |
| 2 | `test_missing_audio_regenerates_and_legacy_is_explicit`: missing audio creates two jobs; unowned audio is protected; ambiguous adoption refuses; explicit `o1` adoption and then `o2` adoption each create one job. | The public planner preserves protected/final/ambiguous rules. For a genuinely absent child, native capture has the existing `track.create`/`occurrence.add-media` path; for an existing child it uses exact old/new selection. | **Not covered** by 2242, which seeds one existing audio clip. The new-child and explicit-adoption outer paths need a real assertion; no implementation/schema change is justified. |
| 3 | `test_adoption_rejects_clip_ids_reused_across_occurrences`: reused clip id without an occurrence pin refuses as ambiguous. | Planner-level ownership/selection guard; requester accepts only the resulting ordered plan and does not invent occurrence identity. | **Not covered** by 2242. Preserve as a refusal guard; do not use a refusal-only outer test as positive qualification. |
| 4 | `test_empty_missing_multiple_and_stale_script_handling`: empty/multiple rows produce `empty_script`/`blocked_script`; a script revision different from the candidate parent refuses. | `plan_draft_voiceover` checks the exact script/base revision before requester admission. No speech root or outer task is created for these rows. | **Not covered** by 2242. This is a pre-admission public guard, not a proposal/outbox proof. |
| 5 | `test_failure_never_changes_input_candidate`: failure on the second synthesis raises and the original candidate is byte-equal to its deep copy. | `prepare_draft_voiceover` works on a copy; the managed path passes the prepared result to native capture and never writes the source candidate. | **Not covered** by 2242. A later body must assert source immutability on a real failure if that node is required; no snapshot-diff reconstruction is allowed. |
| 6 | `test_ripple_updates_placements_stills_and_spanning_parent`: first placement `3000 -> 4150` ms, next start `3000 -> 4150` ms, still hold `3 -> 4.15`, audio `to 2 -> 4`, parent hold/config `6 -> 7.15`, and detached input remains `3000` ms. | Existing capture can carry occurrence resize/start and visual `clip.set` hold, and it carries the provenance leaf. The exact 4150/4150/4.15 consequences are literal, not recomputed at replay. | **Mixed.** The reviewed source has a **semantic gap** for the original existing-audio source window `from/to/hold` change (`2 -> 4`): `occurrence.swap-media` changes selection only and `_capture_timing` refuses an unrepresented source-window change. It also has a **semantic gap** for parent `config.duration` (`6 -> 7.15`): `native_voiceover._capture_timing` explicitly refuses because no current literal parent-duration carrier exists. Agent owns the smallest follow-up: reuse an already-valid parent/config and audio-window carrier if one is approved; do not add a new schema/API or weaken the refusal. |
| 7 | `test_regenerated_audio_keeps_authored_selector_and_updates_source_mirrors`: preserve `asset='voice'` with no bare `media_id`; update internal registry media/duration; update payload asset object/digest/source media; update item media. | The reviewed native swap preserves the authored selector and exact old selection, then emits `shot.set` only for `payload.metadata.draft_voiceover`. | **Semantic gap.** The reviewed swap-plus-metadata path does not emit the original `payload.assets`/`payload.items` mirror writes or the registry duration/source-window changes. Agent owns the smallest existing-carrier review: use existing media/shot carriers only if they already record these exact mirrors; otherwise keep this original positive held rather than silently dropping fields. |
| 8 | `test_ripple_accepts_canonical_untrimmed_rational_placement_fields`: zero source offset and rational speed `1/1` still produce `4150` ms. | Native capture retains the exact occurrence timing commands and validates the existing source/quantization guards. The prepared ripple result is lowered literally. | **Not covered** by 2242's source fixture. Existing focused native proof covers the rational form offline; the outer body still needs this source-form assertion. |
| 9 | Param case `test_ripple_rejects_nondefault_canonical_placement_fields[source_offset]`: nonzero source offset refuses with the untrimmed/speed-1 guard. | Existing planner/native capture refuses unsupported source maps before proposal construction; no partial proposal is valid. | **Not covered** by 2242. Keep as a refusal guard, not an outer positive. |
| 10 | Param case `test_ripple_rejects_nondefault_canonical_placement_fields[speed]`: speed `2/1` refuses. | Same fail-closed timing carrier boundary; no duration or selection is guessed. | **Not covered** by 2242. Keep as a refusal guard. |
| 11 | `test_preserve_rejects_overflow_without_retiming`: overflow under `preserve` refuses; a short `2.5` s result preserves placements and parent exactly. | `timing_policy` is passed through the requester and retained in native capture; preserve has no ripple retiming. | **Not covered** by 2242, which runs only the planned ripple shape. The later body must distinguish refusal from successful short preserve; no outer status may be inferred from `proposal_ready` source code. |
| 12 | Param case `test_unsafe_ripple_is_rejected[overlap]`: overlapping placements refuse. | Planner/prepare validates placement safety before the outer proposal. | **Not covered** by 2242. Preserve the refusal and unchanged-input expectation. |
| 13 | Param case `...[speed]`: unsafe occurrence speed refuses. | Existing timing validation rejects non-translation maps; no native command is emitted. | **Not covered** by 2242. Preserve the refusal. |
| 14 | Param case `...[source_offset]`: unsafe source offset refuses. | Existing timing validation rejects the source map before capture. | **Not covered** by 2242. Preserve the refusal. |
| 15 | Param case `...[other_audio]`: an unrelated audio clip refuses. | Existing single-voiceover selection/ownership checks prevent changing another audio row. | **Not covered** by 2242, whose seed has only the target audio lane. Preserve the refusal. |
| 16 | Param case `...[parameterized]`: parent clip phases/parameterized timing refuses. | Existing timing carrier is literal and fail-closed; it does not reconstruct derived parent timing from arbitrary parameters. | **Not covered** by 2242. Preserve the refusal. |
| 17 | `test_coordinator_noop_and_plan_do_not_synthesize_or_publish`: unchanged is `status=unchanged`; plan-only is `status=planned`; neither invokes synthesis or publishes. | Public `sync_draft_voiceover` keeps the no-op/plan-only path; requester entry is only selected when jobs exist and is forbidden for plan-only. | **Not covered** by the outer fixture. The 2242 chain is a changed-job path; this remains public coordinator evidence, not requester/outbox evidence. |
| 18 | `test_coordinator_detects_concurrent_head_and_cas_failure`: changed head refuses before publication; CAS failure is surfaced and bound target is not published. | Managed source rereads head and publication after preparation; Runtime commit/outbox is the final CAS boundary. | **Not covered** by 2242. The later lifecycle must retain both stale-head and commit refusal paths; neither is a successful outer proposal proof. |
| 19 | `test_coordinator_publishes_once_with_provenance`: changed text publishes once and generated text is `New`. | The replacement is the existing outer `authoring_proposal` plus one `producer.guard`, then `queue_proposal`/`flush`; the outer proposal rationale is the existing exact string `Insert settled managed voiceover WAV and preserve its frozen script binding`. | 2242 source asserts proposal keys and command/guard ordering, but **does not assert the exact rationale value or recomputed digest in a real body**. Original `Bound.publish` is not evidence for the requester path. |
| 20 | `test_coordinator_regenerates_missing_fresh_audio_and_surfaces_other_read_errors`: `not_found` regenerates/publishes both; `forbidden` propagates and does not publish. | Public media read policy remains missing-object regeneration versus visible authorization/integrity failure. Settled requester media reads are stricter: Runtime verified selection/WAV/duration must be present. | **Not covered** by 2242. Its fixture uses a successful authoritative read path only; no missing/forbidden outer branch is proved. |
| 21 | `test_synthesizer_verifies_managed_provenance_and_fresh_request_context`: exact managed speech bytes/manifest, text/settings/duration, stable repeated idempotency context, fresh context on a new synthesizer, and hash corruption refusal. | Inner `generation.generate_speech` remains separate. The requester rereads task/result/output and exact Runtime media facts; settled speech output uses `output_port=speech`, not a guessed name, and does not carry claimant duration. | **Not covered** by 2242 as an original assertion. Its offline speech fixture is deterministic and its source review proves the selector, but no real body has verified the original manifest/context/hash loop. |
| 22 | `test_invalid_timing_policy_fails_even_noop`: invalid policy refuses even when there is no job. | `_sync_draft_voiceover` validates `preserve|ripple` before planning, admission, or publication. | **Not covered** by 2242. This is an early public guard and must remain unchanged. |

## Cross-cut proof obligations not present in the original file

The outer carrier adds important assertions that are not original `Bound`
publication expectations. They are source-described in 2242 but remain
unverified until its one opt-in lifecycle runs:

- normal Runtime admission of the registered outer executor, with the exact
  four-field admitted target and one ordered `settled_speech_input` descriptor;
- outer task/run/attempt and exactly one managed `authoring_proposal`, with
  provenance bound to the outer attempt;
- proposal keys exactly
  `schema_version`, `producer`, `admitted_target`, `commands`, `rationale`,
  `proposal_digest`, with the producer bound to the outer task rather than
  inner Speech;
- exact Runtime five-field media selection
  (`asset`, `generation_id`, `variant_id`, `object_id`, `catalog_digest`),
  verified `audio/wav`, positive size/hash, and intrinsic duration from Runtime;
- requester outbox flight body/key equal to the accepted first commit request,
  then reopening and flushing the persisted flight;
- accepted/rebased status, accepted revision/publication, receipt identity,
  history head, composition readback, and guarded inverse to the admitted base.

Two retry details are still concrete not-yet-covered assertions in the 2242
source: it checks the persisted flight's body/key against the first captured
call, but restores the monkeypatch before the later `session.flush`, so it does
not independently compare a second wire call's body/key; and the reopen is
within one process, not a process restart. Those are qualification gaps, not
permission to claim retry or restart proof.

The source fixture also does not assert zero legacy `bound.publish` traffic,
the exact rationale text, or that every original candidate field survives the
proposal command batch. The source path makes the intended boundary clear;
the later body must provide the evidence or leave the claim open.

## Disposition and owners

No original assertion/test is converted, removed, skipped, or weakened. The
original focused lane remains the preservation baseline; the outer fixture is
an additional carrier, not a replacement test file.

The only genuine semantic source gaps found are Agent-owned native lowering
gaps: existing-audio source-window/mirror updates and parent duration changes.
The smallest permitted next action is to identify and reuse an already
existing exact command carrier for each field (with guarded inverse and
recorded reads/writes); if no such carrier exists, the original positive must
remain held and the owner must decide a later command-carrier change. No new
schema, DTO, API, producer/task identity, snapshot reconstruction, or fixture
is authorized by this map. Runtime owns the later one real outer qualification
and its accepted receipt/history evidence; Agent owns the native-carrier
semantic closure.

