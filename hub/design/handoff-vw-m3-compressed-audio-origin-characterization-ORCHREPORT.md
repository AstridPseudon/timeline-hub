# Inactive compressed-audio decoder-origin characterization

Result: **5 new direct characterization tests pass; original 15 PCM tests and 7 public-clock tests remain byte-identical and pass (27/27 combined). No helper or product activation.** The existing nonzero-start refusal is too broad for one origin-preserving MP3 case, but removing it generally would be unsafe: timestamped AAC cases without skip metadata shift the decoded onset by one AAC frame, and an ADTS AAC stream with no reported `start_time` also shifts by one frame.

## Change

Added only `remotion/tests/attempt-envelope-pcm.codec-origin.test.mjs` (203 lines). It generates and tears down bounded temporary fixtures under the system temporary directory using local ffmpeg 6.1.1:

- 48 kHz, stereo PCM reference with unequal delayed left/right tones;
- raw ADTS AAC;
- MP3;
- AAC in M4A;
- the same AAC remuxed into Matroska with a positive container timestamp;
- video MP4 with AAC;
- video MP4 with its AAC input offset.

Each case is probed with ffprobe, including stream time base/start and first-packet `Skip Samples` side data, then fully decoded as interleaved float PCM with ffmpeg at the original sample rate/channel count. The test compares full frame count and independent left/right onset against the PCM reference. It does not trim, pad, resample, normalize, fit, shift, or align decoded output. No fixture is retained in the worktree.

The existing files `remotion/attempt-envelope-pcm.mjs`, `remotion/compiled-audio-source-clock.mjs`, `remotion/tests/attempt-envelope-pcm.test.mjs`, and `remotion/tests/compiled-audio-source-clock.test.mjs` were compared byte-for-byte with `HEAD` and are unchanged.

## Measured mapping

Reference: 86,400 stereo frames; left onset 9,606; right onset 14,405; 48 kHz, `1/48000`.

| Fixture | Audio stream start | Time base | First packet skip | Full decoded frames | Onset L/R | Delta from reference |
| --- | ---: | --- | ---: | ---: | --- | --- |
| ADTS AAC | stream field absent; format start 0 | `1/28224000` | 0 | 88,064 | 10,630 / 15,429 | +1,024 / +1,024 |
| MP3 | `0.023021` s | `1/14112000` | 1,105 | 86,400 | 9,606 / 14,406 | 0 / +1 |
| M4A AAC | `0` s | `1/48000` | 1,024 | 87,040 | 9,606 / 14,405 | 0 / 0 |
| AAC in timestamped MKA | `0.104000` s | `1/1000` | 0 | 88,064 | 10,630 / 15,429 | +1,024 / +1,024 |
| Video MP4 + AAC | `0` s | `1/48000` | 1,024 | 87,040 | 9,606 / 14,405 | 0 / 0 |
| Offset video MP4 + AAC | `0.103000` s | `1/48000` | 0 | 80,896 | 10,630 / 15,429 | +1,024 / +1,024 |

The first packet PTS also distinguishes the cases: MP3 is `0` with a 1,105-sample skip; M4A/normal video are `-0.021333` with a 1,024-sample skip; timestamped MKA is `0.104000` with no skip. The rational timeline fixture uses 29.97002997002997 fps (`30000/1001`), `source_from = 7*1001/30000`, and playback rate `3/2`; this is only clock arithmetic coverage, not a source-offset/speed policy.

## What the current helper assumes

`prepareAttemptEnvelopePcm` probes only `sample_rate`, `channels`, and `start_time`. It rejects an explicitly nonzero stream `start_time`, but treats an absent start field as acceptable. It does not inspect packet skip/discard side data or codec/container priming. Therefore:

- MP3 is a concrete false refusal for this fixture: its positive start is exactly the reported 1,105-sample skip (within ffprobe decimal rendering), and full decoded stereo onset/count preserve the PCM reference.
- Timestamped MKA AAC and offset-video AAC are correctly unsafe for the current full-decode join: their positive starts have no skip metadata and the decoded content is one AAC frame late.
- ADTS AAC is an important zero/absent-start counterexample: the current start check would admit it, but no skip metadata is reported and its full decode is one AAC frame late.
- M4A/normal-video AAC has zero stream start, a negative first packet PTS, and 1,024 skip samples; ffmpeg’s full decode preserves onset while retaining 640 trailing frames. This is not interchangeable with ADTS AAC.

Thus the current refusal cannot be settled by deleting the nonzero check. Stream start alone is not decoder origin, and an absent/zero stream start is not proof of origin preservation.

## Unapplied Agent attempt-stage proposal

No code patch is applied. For Agent review, the smallest bounded seam is an origin-admission probe beside the existing ffprobe call:

1. Preserve the exact rational first packet PTS/time base and first-packet `Skip Samples`/`discard_padding`; do not coerce absent `start_time` to zero.
2. Admit a compressed source only when its decoder/container metadata describes the priming relationship used by the ffmpeg decode path. The MP3 evidence is the narrow positive example: `start_time * sample_rate` matches `skip_samples`, and decoded count/onset retain the source origin. M4A/normal-video AAC is the zero-start/negative-PTS + 1,024-skip example.
3. Keep timestamped AAC with no skip metadata and ADTS AAC with no origin metadata out of any newly activated origin-preserving producer until an owner-approved decoder join proves their mapping. Do not hide the mismatch with trim/pad/shift.
4. Preserve the current explicit `sourceClock` contract and downstream trim/rate/gain/mix behavior. Do not infer canonical `source_offset`, occurrence inheritance, speed policy, or the eleven-vector compiler contract from these codec observations.

This is a proposal only. It does not change the helper, public exports, package pins, source/provider/custody paths, or normal export. The original positive behavior remains untouched; no refusal test was added to the existing helper suite and no new codec refusal was presented as compatibility.

## Verification

Working tree: `/home/user/work/wt/vw-m3-compressed-audio-origin-characterization`, base `d2ad2ff82`.

Before each CPU/test command, both absolute Viewing QUIET markers were checked; neither was active. Local toolchain: ffmpeg/ffprobe `6.1.1-3ubuntu5`, Vitest `4.1.5`, shared `/home/user/work/app/node_modules`.

```sh
/home/user/work/app/node_modules/.bin/vitest run --config /tmp/timeline-origin-all-vitest.config.mjs --reporter=verbose
```

**Exit 0 — 27 PASS / 3 files / 5.23s.** This includes the new 5-case fixture characterization, unchanged 15-case PCM suite, and unchanged 7-case public clock suite.

```sh
node --check remotion/tests/attempt-envelope-pcm.codec-origin.test.mjs
git diff --check
git diff --no-index --check /dev/null remotion/tests/attempt-envelope-pcm.codec-origin.test.mjs
```

Syntax and tracked-tree whitespace checks passed. The no-index check returns its normal exit 1 because the file is new, with no whitespace diagnostics. Four `cmp` checks against `git show HEAD:<path>` passed for the predecessor helper/tests and clock adapter/tests.

No full suite, browser, live socket, renderer/export, physical audio, network, install, package build, source certification, normal-route activation, or parity claim was run.

