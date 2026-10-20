**Answer:** compile does not commute with the slice. Slicing the compiled timeline on the host (option a) removes the drift. The report is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-pcm-compile-idempotence.md`. No product code or repo files changed, so there is no commit-msg. I created the `DONE` file.

**Corpus:**
- 236 JSON files under `tests/` have a `clips` list with tracks, and the compiler accepted 24.
- Those 24 hold 79 clips: 14 audio, 4 with speed other than 1, and none with a fade.
- A seeded synthetic corpus of 40 timelines fills that gap, with fades, 3 to 5 decimal places on `at`, and speeds from 0.5 to 2.
- Windows were taken at every clip boundary ±1 frame, at 30, 24, 60 and 30000/1001 fps.

**Results.** P is what happens today (host slices the raw JSON, renderer compiles the slice). Q is option (a) (host slices the compiled JSON, renderer still recompiles).

| Corpus | Cases | P differs from Q | Max drift |
|---|---|---|---|
| Repo fixtures | 801 | 0 | 0 |
| Synthetic | 9023 | 6432 (71%) | 1.0 ms (0.03 frame at 30 fps) |

- The repo fixtures are identical because their `at` values are almost all at most 3 decimals, so the rounding never bites.
- In the synthetic run, 14 cases also keep or drop a clip at a window edge differently.
- The drift in source seconds is at most 0.5 ms × clip speed. The worst case measured was 1.0 ms at speed 2.
- `compile(compile(x)) == compile(x)` held for all 64 fixtures.
- Your fade fixture reproduces exactly: `from` is 0.5016 today and 0.502 with option (a). The unwindowed render gives 0.125 + (0.5 − 0.123) = 0.502, so 0.502 is the faithful value.

**Rounding rule:** `astrid/core/timeline/banodoco_composer.py:48-51` (`_round_at_for_dump`) rounds a float `at` to 3 decimals on every compile (applied at `:268`). The raw slice shifts `from` by `(start − at) × speed` using the unrounded `at`, and the compiled slice uses the rounded one.

**Recommendation: (a), slice in the compiled domain on the host.**
- It is the only option where the original and the transformed clip come from the same domain.
- It also covers track exclusion and the theme default, which (b) does not.
- Option (b), rounding `at` in the slicer, duplicates a compiler rule.
- Option (c) cannot meet the sample-exact PCM tests, which need 1e-7 s. The tolerance would be 0.5 ms × speed, about 24 samples at 48 kHz and 48 at speed 2.
- The source-carry re-derivation check must compare against the recompiled slice. The host's own slice still has the unrounded `at`, so a plain comparison fails.
- The service should call the timeline compiler in `astrid.core.timeline` directly, not import `_serialize_timeline` from the rendering pack.

**Caveats:**
- The repo corpus has no fades and few sub-millisecond `at` values, so the synthetic corpus carries most of the evidence.
- I compared timing fields only, not the audio signal.
- Layered slicing with a track allowlist was not measured separately. It filters clips before the slice, so the timing result should be the same.
- `python -I` ignores `PYTHONPATH`, so the scripts add the worktree to `sys.path` themselves.

The scripts are in my scratchpad (`/tmp/claude-0/-home-user-work-wt-agt-pcm-compile-idempotence/8298440d-7723-4c38-b5a9-8482c97f5abf/scratchpad/`): `measure.py` runs the corpus and `extra.py` gives the census, the fade fixture and the drift bound.
