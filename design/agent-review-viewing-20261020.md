# Agent review of Viewing items, 2026-10-20

Worker: agt-viewing-reviews. Branch: tl/agt-viewing-reviews, on top of tl/agt-compile-contracts (fd82c36c). Integration tip read: tl/integration 4a75f68f. Read-only review, plus the compile-contract design and vectors.

Summary:

| Item | Result | Verdict |
|---|---|---|
| 1. Mouth proposal (preserve known) | Artifact not readable | **No verdict.** Neither APPROVE nor REJECT is supported by what is on disk. |
| 2. D09 minimal deletion unit | Artifact not readable; branches contain no D09 commit | **HOLD** (agrees with the escalation). Conditions below. |
| 3. Popup reference, 6 render-facing rows | Settled, fixture and test updated | Done. All 6 rows pass today; no xfail needed. |
| 4. Fade `curve=` honoured | Decided; contract, vectors and owner list updated | Done. Owner scan found no owner film, so the list is open. |

## 1. Mouth proposal (`vw-m3-mouth-proposal-preserve-known`)

What I was asked to read: `workers/vw-m3-mouth-proposal-preserve-known/{ORCHREPORT.md,proposal.patch}`.

What I found:

- That directory is not in `orch/workers/`. Neither file is in the orchestrator scratch tree, the worktree list, or any ref. The 04:26Z escalation names the same path.
- Branch `tl/vw-m3-mouth-proposal-preserve-known` (and its `timeline/agent/` mirror) has head `751dd75e` (03:14Z, "expose presenter mouth crop incompatibilities"). That is an earlier test commit on a rendering branch based on `f6fbe741`, not the corrected proposal. I did not review it as the proposal.
- The escalation asks for Agent approval "by 03:25", but it is dated 04:26Z. The deadline is already past. The orchestrator should confirm whether the approval window still applies.

So I cannot check any of the five points. Per point:

- shared actual erase geometry with legacy-sized padding: not checkable;
- default, partial and raw-invalid facts stay KNOWN, mosaic stays unknown: not checkable;
- no new public type: not checkable;
- no threshold widening: not checkable;
- pixel verification not replaced: not checkable.

**Verdict: no verdict.** The corrected proposal needs to be delivered as a readable file or branch. Then this review applies the five points above to its diff. The old narrowing and refusal proposal was already rejected in the escalation, and nothing here reopens that.

## 2. D09 minimal deletion unit

What I was asked to read: `vw-m3-d09-current-deletion-unit` (core/onscreen.py deletion plus SDK check.py migration).

What I found:

- `tl/vw-m3-d09-current-deletion-unit` points at `4a75f68f`, the integration tip. `git diff --stat 4a75f68f` is empty. There is no D09 commit.
- `tl/vw-m3-d09-known-caller-preservation`, the "next focused worker" in the escalation, also points at `4a75f68f`.
- No `broad09` branch exists in the refs I can see.
- `proposal.patch` and `FILELIST.md` are not readable (same as item 1).

So I cannot check the diff against integration. The "does not erase newer M1 changes" check is not done. The integration tip itself contains the M1 commits the check would protect: `a76c6537` (shared redo after exact occurrence undo), `a610cd30` (merge of shared redo compat), and `d9a849e8` / `4a75f68f` (exact numeric move revision images).

**Verdict: HOLD.** This agrees with the escalation.

Conditions to unhold, all required:

1. The `+80 netproduct` item is resolved and recorded with evidence.
2. Trusted source and label forwarding is qualified. Until then the unit cannot know a scene check's source, so unknown scene checks cannot be left advisory with confidence.
3. The legitimate component and caller positives are qualified, and the SDK hold and cut caller positives are preserved. This is the known-caller-preservation worker's job, and it is not on any branch yet.
4. The patch is a diff against `4a75f68f` that deletes only the D09 unit. It keeps `a76c6537`, `a610cd30` and `d9a849e8` and their tests. Targeted runs of those tests must be green on the patch. This is checked by the worker's own run, not by reading the patch.
5. Saving stays renderer-free. Unknown scene checks stay advisory. Both are shown by tests on the patch, not by assertion.
6. The orchestrator confirms the `broad09` branch named in the escalation is not merged. It is not in the refs I can see.

## 3. Popup reference: the 6 render-facing rows

Settled, in `design/visual-compile-contract.md` and `tests/editing_conformance/fixtures/visual_compile_contract.json`.

The six rows are start, end and duration frames for each occurrence:

| Row | Clip | Field | Frames |
|---|---|---|---|
| 1 | A (occ-1, shot-alpha rev-a, 8 s) | start_frame | 0 |
| 2 | A | end_frame | 240 |
| 3 | A | duration_frames | 240 |
| 4 | B (occ-3, shot-alpha rev-b, 10 s) | start_frame | 240 |
| 5 | B | end_frame | 540 |
| 6 | B | duration_frames | 300 |

Interpretation: the brief said "the intended render-facing 6 rows" without defining them. I read them as three values per occurrence. If the orchestrator meant something else, the table is easy to change.

Clock: `fps_rational: [30, 1]`. Main's rational is the two-element `fps_rational` list, read as `Fraction(*pair)` at `astrid/packs/rendering/actions/timeline_visualize/filmstrip_cards.py:466` on `origin/main` e51595c6. Main has no `{num, den}` object.

Half-open frames, `Math.round` semantics: `astrid/core/timeline/duration.py:145-156` on `e51595c6`. The clamp is `shot_composition_projection.py:309-313` on `e51595c6`.

The premise did not reproduce. The brief said main's helpers return NaN on the rational object. Measured on this branch:

- `clip_start_frame` / `clip_end_frame` with a `Fraction(30, 1)` return 240 and 540 for the B clip (correct);
- with `{"num": 30, "den": 1}` or `[30, 1]` they raise `ValueError: fps must be a number` at `_positive_fps` (`duration.py:45-49`).

So the test passes a `Fraction` built from the pair. Nothing returns NaN.

Test run, targeted, on this branch:

```
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_compile_contracts.py -rxX
20 passed, 2 xfailed
```

The two xfails are the audio vectors 10 and 11 (strict, unchanged in status). No visual row needed an xfail, because the compiler produces all six rows. Adding one would encode a gap that does not exist.

## 4. Fade `curve=` honoured (04:24Z)

Applied in `design/audio-compile-contract.md`, `tests/editing_conformance/fixtures/audio_compile_contract.json` and `test_compile_contracts.py`.

What I verified:

- Main writes the curve at `params.fadeInCurve` / `params.fadeOutCurve` (`clip_fields.py:513-518`, `cli.py:3069-3070`). `_audio_fade_parts` drops it only from the duration value (`clip_fields.py:358`). Playback never reads it. The earlier wording "main parses then discards" was imprecise, and the doc now says so.
- The public package's `compileAudioEnvelope` reads `params[`${name}Curve`] ?? 'linear'` (composition repo HEAD `typescript/src/lib/audio-envelope.ts`). The curve names and formulas match `astrid/core/timeline/audio_curves.py` and `audio_curves.json`. The pinned 0.0.10 copy was not read.
- A test-harness bug: the old `elif want is None: assert key not in clip` only looked at top-level keys, so a dotted check like `params.fadeInCurve` could never fail. It is now `_lookup(clip, key) is None`. This does not change any existing top-level check.

New vectors 12-14 pass: a kept `equal-power` fade-in curve, a kept `exponential-slow` fade-out curve, and no curve key for a linear fade. Vectors 10-11 stay strict xfail; their reasons now say the join's envelope must apply the curve.

Test run, targeted:

```
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_compile_contracts.py -rxX
20 passed, 2 xfailed
```

Owner visibility is in `design/owner-film-differences.md`. The scan found no owner film; see that file. The v0.0.7 section corrects an earlier wording: media clips do get entrance and exit animations from `ClipLook` (`TimelineComposition.tsx:99,104,119`), and the visual doc now says so. The 0.0.7 list also covers transitions and element speed remap, which the visual doc did not mention before.

## Not verified

- Items 1 and 2: neither proposal file was readable, so no diff was checked.
- No frames, PCM or pixels were rendered or compared. The vectors test compiler output fields only.
- The App-side clamp and curve work (`ShotTimelinePreview.tsx`, `shotTimelineDataProvider.ts`) was not touched or run.
- The pinned 0.0.8 composition artifact was not read.
- The orchestrator's full-suite rule was respected: no full or browser suite was requested. The targeted runs above are the only test runs.
