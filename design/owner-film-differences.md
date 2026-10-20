# Owner film differences

Status: **NOT a clean result.** The owner-film scan was run over the roots reachable from this worktree, and it found no owner film data. The lists below are empty for that reason, not because no owner film uses these features. The scanner and canonical closure named in the 04:26Z escalation (`workers/vw-m3-owner-film-cliplook-scan/`) were not reachable, so the list is open until that scan runs.

Decisions this file serves: 04:24Z (fade `curve=` honoured), 03:59Z (element clips get the clip look), 03:20Z (continuous audio gain). Contracts: `design/audio-compile-contract.md`, `design/visual-compile-contract.md`.

## 1. `curve=` on audio fades (honoured from 04:24Z)

Scan, read-only, for `fadeInCurve`, `fadeOutCurve` and `curve=<name>` in `*.json`, `*.yaml`, `*.yml`, `*.md`, `*.txt`, `*.tl`:

| Root | Hits | What the hits are |
|---|---|---|
| `/home/user/work` (all worktrees) | the contract doc only, in `agt-compile-contracts` | no owner film carries a curve key |
| `/home/user/banodoco` (`reigh-app`, `banodoco-workspace-runtime`, `timeline-theme-2rp`) | none in those file types | one TypeScript test, `reigh-app/src/tools/video-editor/lib/timeline-data.audio-envelope.test.ts`, mentions a curve key. It is a unit test, not a film |

Fades without a curve exist in the repo fixtures (for example `tests/fixtures/reshape/hype_regression/hype.timeline.json`, `examples/hype.timeline*.json` in the `.test-*` tree, and `tests/editing_scenarios/look/look.fade-in*.yaml`). None sets a curve, so their audio is linear before and after the change. Those are test fixtures, not owner films.

Effect of the decision, for any owner film that does use `curve=`: its audible fade shape changes from linear to the named curve. Curve names are the registry in `astrid/core/timeline/audio_curves.json`: `linear`, `equal-power`, `exponential-fast`, `exponential-slow`, `s-curve`.

| Film | Clip | Fade | Curve (current) | Curve (after) | Owner visible? |
|---|---|---|---|---|---|
| _to fill from the owner scan_ | | | | | |

## 2. v0.0.7 clip-look differences (main pins 0.0.6)

Source: composition repo tags `v0.0.6` to `v0.0.7`, commits `1ec2e2d`..`6bd784d` (`git diff --stat v0.0.6 v0.0.7` lists `ClipLook.tsx`, `TimelineComposition.tsx`, `TransitionLayer.tsx`, `lib/clip-look.ts`, `lib/transition-spans.ts`, `lib/fade.ts`, `lib/transitions.tsx`; `AudioTrack.tsx` is not in the list, so audio playback is unchanged between the two tags).

Differences a film can see:

1. **Element clips get the clip look.** Opacity and crop apply to element clips (`ClipLook.tsx:40-48`). Independent fades on overlapping element clips now DIP, where 0.0.6 drew them opaque. This is the approved difference (03:59 decision; the 16-30 DIP golden).
2. **Entrance and exit on media clips.** `ClipLook` wraps media clips too (`TimelineComposition.tsx:99,104,119`), so media with `entrance` or `exit` animations now animate. Media opacity and crop are still handled by `VisualClip`, not by `ClipLook`.
3. **Element speed remaps time** (`42e1538`; README "Speed"). An element clip with `speed` other than 1 plays its animation at `speed` times the rate, over a clip length of hold / speed, through `<Freeze>` (`ClipLook.tsx`). Media clips still use `playbackRate` and are unchanged.
4. **Transitions are planned per boundary** (`2220e8f`, `8b9868e`; `lib/transition-spans.ts`):
   - a transition with any id other than `fade` is a dissolve; `fade` is a dip (README "Transitions");
   - `align` (`end` default, `start`, `center`) sets where the overlap window sits;
   - the outgoing clip is extended past its end and the incoming clip back before its start, drawn frozen on the boundary frame (extension frames);
   - chains are planned independently per boundary;
   - a boundary whose next clip does not start within one frame of the outgoing end is a cut, and a transition longer than either clip is ignored.
   The 0.0.6 transition path was not compared here, so the size of each change is unverified.

Films affected, by feature: any film with element clips that overlap others and carry a fade, opacity, crop, entrance or exit; any film with transitions; any element clip with `speed` other than 1; any media clip with an entrance or exit. The owner-film scan should list films by these features. None are listed yet.

Proof still owed (not done here): a MAIN replay built from tag `v0.0.6` (`git archive` reproduces main's locked sha512) against the unified result, with real pixels. Only the differences above may appear.

## 3. Continuous audio gain (03:20 decision)

- The unified path evaluates gain continuously per PCM source sample (the public `applyAudioEnvelope`). Main steps gain once per video frame (`AudioTrack.tsx:48-70`).
- The step can be up to about 0.7 dB off mid-fade, per the PLAN. This was not measured here.
- Every film with an audio fade changes slightly, even with no `curve=`: the change is the step being removed.
- The fade length is rounded to the frame grid (`Math.round(raw * fps) / fps`, `compileAudioEnvelope`), so a fade is still frame-aligned in length.
- Films with a `curve=` change in shape as well as in step (section 1).
- Playback readiness, retry, mute and amplify behaviour are unchanged. The fade still refuses `ENVELOPE_UNRENDERED` on non-Player paths until the prepared-source join lands (`design/audio-compile-contract.md`).

Owner review (PLAN, hard stop): play the films listed in section 1 and section 2 with the new and old audio, and list them in the film-viewing steps.

## Not verified

- No owner film was found or read. The lists are empty for that reason.
- No frames or PCM were rendered or compared.
- The pinned 0.0.8 artifact was not read; the statements are about the composition repo tags and HEAD.

## 4. Compiler and source evidence for the popup closure (04:44 item 3)

Added by `agt-visual-contract-correct`. Contracts: `design/visual-compile-contract.md` (section 1) and `design/audio-compile-contract.md`. This section records what the compiler and the native source show. It does not change the owner list.

Visual closure (the native ADD fixture, not a reconstruction):

| Fact | Evidence |
|---|---|
| Source | App `309cb7a4`, `src/tools/video-editor/commands/fixtures/recipe_m2_occurrence_media.json` (blob `22be2059`), key `add.output`, copied verbatim into `visual_compile_contract.json` as `native_add_output` |
| Occurrence A at 8 s, B at 10 s, both 10 s | `add.output.parent_revision.payload.occurrences` (`placement.start_ms` 8000 and 10000, `duration_ms` 10000) |
| Source window child: at 1, hold 4, from 2, to 6, speed 2, so 2 s on the timeline | `add.output.internal_timeline_revisions` (`internal-1` and `authoring-timeline-revision-bfcf…`) |
| Native child `reserved-child` keeps `opaque` `[null, false, {}]` and `params` `null` | `add.output.internal_timeline_revisions[1].payload.clips` |
| No child overhangs its occurrence end, so the clamp does not change the rows | `_project_clip` at `shot_composition_projection.py:308-313`; largest child ends 15 s (A, end 18 s) and 17 s (B, end 20 s) |
| Occurrence spans overlap (A 8-18 s, B 10-20 s); main accepts it | `project_runtime_parent_composition` output (`occurrences` at 8.0 and 10.0, hold 10.0 each); no validation rejects it |
| Native fps is a `{numerator, denominator}` dict; `Fraction(30000, 1001)` works, the dict and the `[num, den]` list raise | `add.output.parent_revision.payload.config.output.fps`; `duration.py:45-49` (`_positive_fps`) |
| Rows: occ-a child 270 to 330 (60 frames); occ-b child 330 to 390 (60 frames) | Probe on this branch, `project_runtime_parent_composition` with `Fraction(30000, 1001)` |

Owner-film meaning: none found. The popup closure is App's native fixture, not an owner film, and the owner scan above found no owner film in reach.

Audio: 11 of Viewing's originals are not reachable from this tree. The reconciliation status and the list needing Viewing's sign-off are in `design/audio-compile-contract.md`, "Reconciliation with Viewing's 11".

Open for the orchestrator: whether overlapping occurrence spans on one lane are intended, and what decides the clamp when no child overhangs.
