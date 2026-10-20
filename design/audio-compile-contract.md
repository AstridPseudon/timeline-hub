# Audio compile contract

Status: contract draft for the Agent compiler, from the 2026-10-20 03:17, 03:20 and 04:24 orchestrator decisions. Golden vectors: `tests/editing_conformance/fixtures/audio_compile_contract.json`, run by `tests/editing_conformance/test_compile_contracts.py`.

Owners: Agent (one compiler, export path), App (preview adapter), Viewing (PCM goldens and instrument).

Reference for "audible today": `origin/main` e51595c6. The Python compiler is `astrid/core/timeline/shot_composition_projection.py`. Playback is Composition 0.0.6 `AudioTrack.tsx`, which is what `remotion/package.json:18` pins on main and `docs/reference/timeline-composition-v0.0.6/AudioTrack.tsx` copies.

## Decisions this contract applies

1. **One compiler.** Agent owns the occurrence-to-clip rules. App and Viewing consume the compiled output and carry no second policy.
2. **Gain is multiplicative**: `child x occurrence`. Examples: 0.8 x 0.5 = 0.4; 1.5 x 2 = 3.
3. **`source_offset` and occurrence `speed` follow main's audible playback**, not App's adapter. Main ignores both on the playback path, so the compiler keeps them as metadata. Metadata-only is acceptable here only because main does not change what is heard.
4. **Fades use one continuous, source-time envelope** for App preview and Agent export. The public Composition `applyAudioEnvelope` is the policy (03:20). Until the prepared-source join exists, non-Player fades refuse `ENVELOPE_UNRENDERED`.
5. **Fade `curve=` is HONOURED in the unified path** (orchestrator 04:24Z). The author's `curve=NAME` is kept as `params.fadeInCurve` / `params.fadeOutCurve` and the envelope applies it. Main's playback ignores it, so main's audible fades are always linear. This is a deliberate change for films that use `curve=`; they are listed in `design/owner-film-differences.md`.

## What main actually does (evidence)

| Field | Compiler output on main | Playback on main | Contract |
|---|---|---|---|
| Gain | `shot_composition_projection.py:359-363`: `clip.volume = clip.volume (default 1) * occurrence.gain`, written only when the child has a volume or the gain is not 1 (so an absent volume stays unity, not an invented 1.0) | `AudioTrack.tsx:43-45`: `baseVolume = track.volume * clip.volume`, zero when the track is muted | Multiplicative. **Applied.** |
| Mute | `shot_composition_projection.py:364-365`: `volume = 0` | same `baseVolume` path | Silence. **Applied.** |
| `source_offset` | `shot_composition_projection.py:353`: kept only in `app.astrid_shot_composition.source_offset`. The child window is computed from the child's own `from`/`to`/`hold` (`:316-326`). | `AudioTrack.tsx:75` uses `computeMediaTrim(clip)`, and `lib/trim.ts:4-18` reads only `clip.from` and `clip.to`. The occurrence offset is never read. | Metadata only. **Not applied.** `tests/timeline/test_shot_composition_projection.py:47` asserts `from == 2` while `:50` keeps `source_offset == 7` as metadata. |
| Occurrence `speed` | `shot_composition_projection.py:305-307` says the placement speed is a placement property and the child's speed stays intact. `:316` reads child speed only. `:354` stores the occurrence speed as metadata. | `AudioTrack.tsx:76`: `playbackRate = clip.speed` (child only) | Metadata only. **Not inherited.** |
| Fades (`params.fadeIn/fadeOut`) | The duration is stored as the value. `clip_fields.py:358` drops the curve from the value (`raw, _curve = _audio_fade_parts(raw)`), but the curve itself is persisted at `params.fadeInCurve` / `params.fadeOutCurve` (`clip_fields.py:513-518`, written by `cli.py:3069-3070`; absent means linear). | `AudioTrack.tsx:48-70`: linear only, with a per-frame `volume(frame)` callback (`frame / fadeInFrames`). The stored curve never reaches playback. | Target: continuous source-time envelope (decision 4) with the curve applied (decision 5). This is a deliberate change from main's frame-step, recorded as ledger row VW-AUDIO-STEP. Main's per-frame step can be up to about 0.7 dB off mid-fade. |

`AudioTrack.tsx` is identical between tags `v0.0.6` and `v0.0.7` in the composition repo (`git diff --stat v0.0.6 v0.0.7` is empty). I did not read the pinned 0.0.8 artifact from this sandbox, so for 0.0.8 the statement is unverified.

## Clock inputs for the envelope

The source clock follows what main plays, and nothing else:

- `source_from` = the child's trim start (`from`, the same value `computeMediaTrim` uses).
- `playback_rate` = the child's `speed` (absent means 1).
- The occurrence `source_offset` and occurrence `speed` are **not** clock inputs (decision 3).
- Gain is never part of the clock. Constant base gain (`track.volume * clip.volume * occurrence.gain`) is passed separately from the envelope.

## Curve semantics (decision 5)

The public package already reads the curve from the same place main writes it:

- `composition` HEAD `typescript/src/lib/audio-envelope.ts` (`compileAudioEnvelope`): for each of `fadeIn` / `fadeOut`, the curve is `params[`${name}Curve`] ?? 'linear'`, carried on the keyframe that starts the ramp. Fade length is `Math.round(raw * fps) / fps`.
- Curve names and shapes match the Python registry `astrid/core/timeline/audio_curves.json` and `audio_curves.gain()`: `linear`, `equal-power` (sin), `exponential-fast` / `exponential-slow` (`expm1` form), `s-curve`. A fade-out mirrors progress as `1 - t` in both.
- Compiler output therefore only has to keep `params.fadeInCurve` / `params.fadeOutCurve` on the clip. Linear is the absence of the key, as `clip_fields.py:515-516` already writes it.
- Not verified: the pinned 0.0.10 package's copy of `audio-envelope.ts`. The composition repo HEAD was read instead.

## Golden vectors (14)

Vectors 1-11 are the vectors in `audio_compile_contract.json`. The 03:17 decision says Viewing's 11 goldens should become exactly this set. Viewing's authored set (`vw-m3-audio-projection-goldens2`) was not reachable from this worktree, so vectors 1-11 are reconstructed from the decision text and the 03:17 escalation. **Viewing must reconcile them with its authored 11 before the set is treated as shared.** Vectors 12-14 are added for decision 5.

| # | id | Input (child / occurrence) | Expected | Status |
|---|---|---|---|---|
| 1 | gain-child-x-occurrence | volume 0.8 / gain 0.5 | volume 0.4 | pass |
| 2 | gain-boost-x-occurrence | volume 1.5 / gain 2 | volume 3 | pass |
| 3 | gain-child-absent-is-unity | absent / gain 0.5 | volume 0.5 | pass |
| 4 | gain-unity-keeps-volume-absent | absent / gain 1 | no volume key | pass |
| 5 | gain-zero-is-silent-not-absent | absent / gain 0 | volume 0 | pass |
| 6 | muted-occurrence-silences-child-gain | volume 0.8 / gain 0.5, muted | volume 0, muted true | pass |
| 7 | source-offset-is-metadata-only | trim 0.125..1.125 / source_offset 0.35 | trim unchanged; offset 0.35 as metadata | pass |
| 8 | occurrence-speed-not-inherited | child speed absent / speed 1.5 | speed absent; 1.5 as metadata | pass |
| 9 | child-speed-wins-over-occurrence-speed | speed 2 / speed 1.5 | speed 2; 1.5 as metadata | pass |
| 10 | fade-in-needs-prepared-envelope-source | params.fadeIn 0.5 | `audio.render_source` present | **xfail (strict)** |
| 11 | fade-out-needs-prepared-envelope-source | params.fadeOut 0.5 | `audio.render_source` present | **xfail (strict)** |
| 12 | fade-in-curve-is-kept-on-the-compiled-clip | fadeIn 0.5, fadeInCurve equal-power | `params.fadeInCurve` equal-power | pass |
| 13 | fade-out-curve-is-kept-on-the-compiled-clip | fadeOut 0.5, fadeOutCurve exponential-slow | `params.fadeOutCurve` exponential-slow | pass |
| 14 | linear-fade-has-no-curve-key | fadeIn 0.5, no curve | `params.fadeInCurve` absent | pass |

Vectors 1-9 and 12-14 pass on the current projection. Vectors 1-9 are main's behaviour. Vectors 12-14 pin the curve as metadata that survives compilation. Vectors 10-11 are strict xfails: no producer of `audio.render_source` exists in this tree (grep finds it only in the fixture). Strict means that when the join lands, the xfail flips to a failure and the marker has to come out. The join's envelope must apply the curve. That is a requirement on the join, and this tree cannot yet check it.

The vector test now checks an absent dotted key with `_lookup(...) is None`. The old `key not in clip` check only looked at top-level keys and would have passed for `params.fadeInCurve` regardless of its value.

The occurrence-offset and occurrence-speed rows (7-8) deliberately **do not** match App's current adapter, which applies both. App must drop that application; this is the narrow App repair the 03:17 decision asks for.

### Reconciliation with Viewing's 11 (04:44 item 2): not done, Viewing's originals unreachable

Viewing's authored set, `vw-m3-audio-projection-goldens2`, is not in the orchestrator's `workers/` directory, not in any worktree under `/home/user/work/wt`, and not on any branch or path searched under `/home/user/work`, `/home/user/peteromallet` or `/home/user/banodoco`. So vectors 1-11 cannot be compared with the originals.

What is on record: the closed escalation `viewing-20261020T0309Z-audio-projection-export.md` quotes four of Viewing's values. They match this file's vectors 1, 2, 7 and 8:

- gain 0.8 x 0.5: App 0.8, Agent 0.4 (vector 1);
- gain 1.5 x 2: App 1.5, Agent 3 (vector 2);
- source_offset 0.35 on trim 0.125..1.125: App applies the offset to the trim, Agent keeps the trim and the metadata (vector 7);
- occurrence speed 1.5 with the child speed absent: App uses 1.5, Agent keeps the child speed absent and the metadata (vector 8).

**Needs Viewing sign-off** (against the authored originals, not the escalation): vectors 1, 2, 7 and 8 for the exact inputs and expectations, and vectors 3, 4, 5, 6, 9, 10 and 11, none of which the escalation quotes. Vectors 12-14 are Agent-authored under the 04:24 curve decision and have no Viewing counterpart. Any disagreement goes to the orchestrator, not into a quiet edit of either set.

## ENVELOPE_UNRENDERED join plan

Problem: the public 0.0.10 `applyAudioEnvelope` path needs a trusted prepared source. Main's normal render route has no producer (`astrid/packs/rendering/actions/render/` has no `render_source`). So a non-Player audio fade currently refuses `ENVELOPE_UNRENDERED`, and that refusal must stay. Relaxing the check, removing the fade, or adding a new refusal test is not allowed.

Plan (Agent side; Viewing wires its inactive helper to it afterwards, per the 03:17 decision):

1. **Compile.** A fade-bearing audio clip gets an exact envelope identity from the public `compileAudioEnvelope(clip, fps)`, and the clock from the rules above. No App-side envelope selection.
2. **Prepare (trusted host, normal render route).** Decode the source once per exact tuple `(source URL, envelope identity, source_from, playback_rate)`, using `applyAudioEnvelope` with the bounded decode. Write the result with `audioEnvelopeWav` into an attempt-owned file. Record it as `clip.audio.render_source = {file, envelope_key, source_from, playback_rate}`. This field is compile output and is never authored; App must not create it.
3. **Consume.** The public `encodedEnvelopeSource` accepts only an exact match of that tuple and throws `AudioEnvelopeError` otherwise. A forged or mismatched `render_source` refuses; it never plays.
4. **Until then.** Vectors 10-11 stay xfail. Non-Player fades keep refusing `ENVELOPE_UNRENDERED`. Nothing falls back to the frame-step callback.
5. **Ordering.** The 03:17 decision pairs this with the slice/layer P1 fix. Do not wire Viewing's helper before the Agent join is reviewed.

## Ledger and owner items

- VW-AUDIO-STEP: App `AudioTrack.tsx` per-frame callback and the old frame-table comparator are retired only after Agent's compiled clock is published, App's PCM adapter is live, both consumers use it, and Viewing's Player-vs-export PCM goldens pass with no threshold widening. The frame-step RED baseline stays as a record.
- Owner review at the hard stop (per the PLAN): films with fades will sound about 0.7 dB different mid-fade. List them.

## Open items for the orchestrator (not decided here)

1. **`curve=` on audio fades: RESOLVED, honoured** (decision 5, orchestrator 04:24Z). Owner visibility: the films that use `curve=` are listed in `design/owner-film-differences.md`. That scan found no owner film in reach, so the list is open.
2. **Viewing's 11.** Reconcile these vectors with Viewing's authored set. Any disagreement goes to the orchestrator, not into a quiet edit of either set.

## Not verified

- No PCM was rendered and no Player or export was compared. The vectors test the compiler's output fields only.
- The pinned 0.0.8 artifact's `AudioTrack` was not read (see above).
- App's tests were not run from this worktree.
