# Agent: does compile commute with the host slice? (PCM source-carry blocker)

Worker: agt-pcm-compile-idempotence. Measurement only; no product code changed, no repo file added. Base: tl/integration worktree `agt-pcm-compile-idempotence`.

Scripts (read-only, in the worker scratchpad; run from the worktree):
- `/tmp/claude-0/-home-user-work-wt-agt-pcm-compile-idempotence/8298440d-7723-4c38-b5a9-8482c97f5abf/scratchpad/measure.py` (corpus run)
- `.../scratchpad/extra.py` (corpus census, the §1 fixture, drift bound)

```
/home/user/work/venv-agent/bin/python -I <scratchpad>/measure.py   # from the worktree
/home/user/work/venv-agent/bin/python -I <scratchpad>/extra.py
```

`-I` ignores `PYTHONPATH`, so both scripts insert the worktree on `sys.path` themselves.

## Definitions

- `compile(x)` = `Timeline.from_json_data(x).for_render().to_json_data()` (what `_serialize_timeline` does after `load`).
- `P = compile(slice(raw))`: today. Host slices the raw JSON (`service.py:1052`/`_window_timeline`), the renderer compiles the sliced file (`run.py:1104-1107`).
- `Q = compile(slice(compile(raw)))`: option (a). Host slices the compiled document; the renderer still recompiles the sliced file.
- `Q0 = slice(compile(raw))`: option (a) before the renderer's own recompile (what the host would hold/write).
- Compared per windowed clip id over `at/from/to/hold`, plus the set of clip ids that survive the window.

## Corpus

Every JSON under `tests/` containing a `clips` list with `track` (incl. nested ones in `tests/editing_conformance/fixtures`): **236 candidates, 24 accepted by the compiler**, 212 rejected (not timelines, or schema-invalid). Accepted = 79 clips: 14 audio, 65 visual, 4 with speed != 1, 4 with `at` finer than 3 dp, **0 with fades**, 0 with `from` finer than 3 dp. Honest limitation: the repo corpus has no fade-bearing clip and almost no sub-ms authored `at`, so it barely stresses the rounding.

Windows: per fixture and per fps in {30, 24, 60, 30000/1001}, boundary frames at every clip's `at`/end frame ±1, all consecutive and ≤90-frame pairs, 60 sampled per (fixture, fps).

A seeded synthetic corpus (40 timelines, 2-4 clips each, `at` with 3/4/5 dp, `from`/`to` 3-4 dp, speeds {0.5, 0.8, 1, 1.5, 2}, audio and visual tracks, fades in ~60% of clips) covers the gap.

## Results

| | cases | P == Q0 | P != Q0 | P == Q | P != Q | max drift (s) | max drift (frames) | clip-id set differs |
|---|---|---|---|---|---|---|---|---|
| repo, 24 fixtures | 801 | 672 | 129 | **801** | **0** | Q0: 0.00037 (1/90 frame) / Q: 0 | Q0: 0.011 / Q: 0 | 0 |
| synthetic, 40 fixtures | 9023 | 1672 | 7351 | 2591 | **6432** | **0.0010** (30 fps: 0.030 frame) | 0.030 | 14 |

- `compile(compile(x)) == compile(x)` held for all 64 fixtures. Compile is idempotent; the problem is that it does not commute with the slice.
- Repo corpus: `P != Q0` only because the renderer's recompile rounds the slice's own `at` (0.0333 → 0.033). Once the sliced file is recompiled (`Q`), it is byte-identical to `P` in all 801 cases. The corpus is just too coarse to expose the other mechanism.
- Synthetic: `P != Q` in 71% of cases, from `from`/`to` (source drift) and in 14 cases a clip is kept or dropped at a window edge (id set differs).
- Worst case: `synthetic-31`, 30 fps, window 146..154, `from` 3.68033 (raw) vs 3.67933 (compiled) = 1.0 ms (speed 2).
- The drift is bounded exactly: max over all synthetic cases of `|Δfrom or Δto| / (speed × 0.5 ms)` = **1.000000000002**. So `|Δ source| ≤ 0.5 ms × speed`.

The §1 fixture of `agent-pcm-source-carry.md` reproduces: authored `at 0.1234, from 0.125, to 2.125, fadeIn 0.5`, window 15..45 @ 30:

| | at | from | to | `astrid_slice_origin.at` |
|---|---|---|---|---|
| P (today, after renderer compile) | 0.0 | 0.5016 | 1.5016 | 0.1234 |
| Q (slice the compiled doc) | 0.0 | 0.502 | 1.502 | 0.123 |

The full unwindowed render sees `at = 0.123`, so source time at timeline 0.5 s is `0.125 + (0.5 - 0.123) = 0.502`. **Q is the one consistent with the unwindowed render; P is off by 1.6 ms.**

## Rounding rule responsible

`astrid/core/timeline/banodoco_composer.py:48-51` `_round_at_for_dump`: `at = round(at, 3)` for float `at` only (ints and `from`/`to`/`hold`/`speed` are untouched). It runs on every `Timeline.to_json_data()` (`:268`). The slicer (`service.py:_window_clip`, `at` read at ~`:1180`, `from` shifted by `(visible_start - clip_start) × speed` at ~`:1217`) works in exact `Fraction`s of whatever `at` it is given. Two consequences:

1. **Input rounding (the blocker).** Slicing raw uses the unrounded `at`; slicing compiled uses the rounded one. The shift `(start - at) × speed` therefore differs by up to 0.5 ms × speed. This also moves clip membership at window edges and the `astrid_slice_origin` stamp.
2. **Output rounding.** The renderer's recompile of the sliced file rounds the slice's own `at` (a frame fraction like 0.0333) to 3 dp, without adjusting `from`/`to`. Same in P and Q, so it is not a P-vs-Q difference, but it is why `Q0 != Q` (≤ 0.5 ms in `at`).

Other compile steps (`_exclude_source_tracks` `:174`, `theme` default) do not change the clip timing here but do change which tracks/clips the slice sees (not exercised by the corpus: no `role: source` track in the 24).

## Recommendation

**(a) Slice in the compiled domain on the host.** Reasons:
- It is the only option where the pair (original, transformed) provably comes from one domain, which the PCM requirement needs (and the source-carry design already needs the compiled unsliced document for the sidecar).
- It removes the mismatch by construction, including `_exclude_source_tracks`/`theme`, which (b) would not cover; and it makes windowed output match the unwindowed render (above).
- Renderer-side behaviour is unchanged: the renderer recompiles the sliced file anyway, and `compile(compile(x)) == compile(x)`.

Notes for the implementer:
- The re-derivation check (`_window_clip(original, ...) == transformed`, source-carry §5) must compare against **`compile(Q0)`** or restrict to `from/to` (`Q0` still has the unrounded slice `at`; the renderer's transformed clip has the 3 dp one). Compared that way, `Q == compile(Q0)` is exact in all 9824 cases.
- Only rounded-`at` clips change output vs today: by ≤ 0.5 ms × speed in `from`/`to`, i.e. a sub-frame move in source (≤ 0.03 frame at 30 fps). Check `tests/core/rendering/test_service.py` slice expectations that use an `at` finer than 3 dp (the 3 dp ones are unaffected: repo `P == Q` in all 801 cases).
- Layering: `_serialize_timeline` lives in `astrid/packs/rendering/shared/rendering_backend/__init__.py`; the service should call `Timeline.from_json_data(...).for_render().to_json_data()` from `astrid.core.timeline` directly rather than import from a pack.

**(b) Round with the compiler's rule** (apply `round(at, 3)` to a float `at` inside `_window_clip`): a one-line change that would make `slice(raw)` match `slice(compile(raw))` on `at`-driven drift. Rejected: duplicates a compiler rule in the slicer (two places to keep in sync), does not cover track exclusion/theme, and still leaves the host without a compiled unsliced original.

**(c) Accept with tolerance:** not compatible with the PCM sample-exact tests (1e-7 s at source 0.5 s). If it were taken, the tolerance would be `0.5 ms × speed` in source seconds = 24 samples at 48 kHz (48 at speed 2, 22 at 44.1 kHz speed 1) plus the id-set edge cases; that is audible as a click-level offset between original and transformed and cannot be asserted at sample level.

## Unverified / caveats

- Corpus has no fades and few sub-ms `at` values; the synthetic corpus supplies those, and the drift bound (0.5 ms × speed) is analytical (half a ULP of the 3 dp rounding), confirmed to 1e-12 by measurement.
- Only timing fields are compared, not the audio signal or `params` (the slice leaves `params` untouched; the `astrid_slice_origin` stamp differs in `at` as shown).
- Layered (`tracks=` allowlist) slicing not measured separately; it filters clips before `_window_clip`, so the timing result is identical.
- No permanent test added; a characterization test would be easy to add in `tests/core/rendering/` with the §1 fixture if wanted.
