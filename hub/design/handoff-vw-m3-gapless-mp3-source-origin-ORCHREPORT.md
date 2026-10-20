# Gapless MP3 source origin — complete UNAPPLIED proposal

**Four ordinary tests pass. The identical four tests on exact d2ad and on the
exact long-source proposal each give 2 PASS / 2 FAIL: both positive MP3 tests
fail at the old origin guard. No product activation; Agent worktree clean.**

## Deliverables and exact composition

All changes are offline under ORCH, with no Agent repository changes:

- design/handoff-vw-m3-gapless-mp3-source-origin-proposal.patch — delta after
  d2ad plus the retained long-source proposal; changes the inactive helper's
  metadata admission and adds the ordinary regression.
- design/handoff-vw-m3-gapless-mp3-source-origin-regression.test.mjs — flat copy
  of the tested regression (install beside the existing tests when reviewing).
- design/handoff-vw-m3-gapless-mp3-source-origin-required-decoder-data.md — exact
  source-backed fields/equation, measured native references, unresolved debt.
- This report also appears at
  design/handoff-vw-m3-gapless-mp3-source-origin-ORCHREPORT.md.

Frozen base: d2ad2ff8290c8b11d8f97ccc7d669bd7a451daf5. Apply the existing
handoff-vw-m3-long-audio-source-compat-proposal.patch first (SHA256
7618abad18d6f6e7096dba7a6e265a514d8986ad29bf013a7d2f86c26c26e5bb), then this
delta (SHA256 9bff9ae6c48df0340f7ebf297f03bc2fecdc7fe7c2a304628d710511a6061798).
The packaging check applied both in a disposable own ORCH directory and compared
the resulting helper, clock and new test against the tested proposal; the
retained long-source regression is unchanged. No other worker outputs touched.
Do not apply this delta directly to integration or create a second helper when
composing the earlier normal-source proposal.

The public-clock adapter equals frozen d2ad byte-for-byte. The local public11
archive SHA256 is dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601;
all 77 extraction members were compared to it. Only advertised evaluation
exports are imported. No install, dependency change, new package/pin, provider,
core, compiler, DTO, source grant, normal producer or runtime path change.

## Change and proof

Read PLAN, the audio compile contract, completed 27-case codec characterization,
long-source proposal/report, and frozen d2ad attempt/public-clock kernels.
The old guard reads stream.start_time, not format.start_time. Both are 0.023021
for this MP3. The proposal preserves the old guard and adds one narrow way
through it: actual MP3 codec AND MP3 demuxer, first packet PTS/DTS zero,
positive padding skip, normal skip/discard reasons, and exact rational
presentation start ticks equal to that skip at the native sample rate. No
hardcoded delay, floating tolerance or filename exception. Packet metadata is
read for only one packet. Raw decode, file-backed reads, cleanup and public
apply/WAV calls are unchanged from the long-source predecessor.

The independent 1.8-second native PCM16 stereo source has 86400 frames, onset
9606/14405. Native gapless MP3 decode retains 86400 frames, onset 9606/14406;
first skip=1105, tail discard=47, packet accounting gives 87552-1105-47=86400.
Unity public envelope output retains **every float byte of the complete native
MP3 decode**, both unequal channels and all leading/trailing samples. The WAV
header is native 48 kHz stereo float32, and real FFmpeg readback equals the
payload byte-for-byte. This proves no extra decode/presentation-origin shift;
it does not assert lossy samples equal the original PCM16 waveform.

A second positive runs the actual proposed decode -> public compile/apply ->
full-source WAV with fps 30000/1001, authored from=.051 rounded by the unchanged
public adapter to 2/fps=.06673333333333334 and child speed=1.5. The entire WAV
matches an independent unchanged public apply/WAV over native MP3 arrays.
Clip volume 7 stays downstream and is not baked. Source/graph identity,
returned clock/envelope metadata and attempt scratch removal are checked.
A deliberately wrong +1105/48000 origin produces a different whole-source WAV;
no alignment, origin fitting, normalization, resampling, trimming, padding,
shift, time stretch, gain baking or final encoding makes a test pass.

WAV SHA256s:

- unity: d8a6de77461ad1040ae64f4d411beb12319a7a5c61f48bde8ed81e96de2d7ddf
- rational trim/speed: 2dce02df933ad094b75790971a9acb0d798549cf20e707df148af4960dd49696
- deliberately wrong origin: 54b053925236e364d499bc4f601d5675f83e56bb59e2199c9734bf3ed6924f84

A real offset MP3-in-MKA is the source-backed negative control: no first skip,
87505 frames, onset debt 1105/1106, nonzero timestamp. It still fails the old
guard and leaves attempt contents/unrelated files intact. Direct characterization
also retains no-Xing MP3 (zero start, +1105/1106 debt), ADTS (absent start,
+1024/1024 debt), M4A (correct onset but 640 extra trailing frames) and offset
AAC (+1024/1024). The required-data file contains exact fields and counts.
No new blanket codec refusal, xfail or skip; no passing behavior test weakened.

## Exact verification

Worktree /home/user/work/wt/vw-m3-gapless-mp3-source-origin, HEAD 470e4001d.
Local Node 22.22.0, ffmpeg/ffprobe 6.1.1-3ubuntu5. CPU-only, sequential native
subprocesses, FFmpeg threads=1, one 1.8-second independent source, no video.
No extra 64 MiB fixture run. Here:

    P=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gapless-mp3-source-origin

    env -u NODE_OPTIONS -u NODE_PATH node "$P/d2ad/remotion/tests/gapless-mp3-source-origin.test.mjs" > "$P/regression-d2ad-red.log" 2>&1

Exit 1, **2 PASS / 2 FAIL / 0 skipped / 0 todo**, 1.455 seconds. Both positives
fail at the original source PCM clock guard; both controls pass.

    env -u NODE_OPTIONS -u NODE_PATH node "$P/base/remotion/tests/gapless-mp3-source-origin.test.mjs" > "$P/regression-red.log" 2>&1

Exit 1, **2 PASS / 2 FAIL / 0 skipped / 0 todo**, 1.411 seconds. Exact untouched
long-source proposed helper, same ordinary test bytes and positive failures.

    env -u NODE_OPTIONS -u NODE_PATH node "$P/proposal/remotion/tests/gapless-mp3-source-origin.test.mjs" > "$P/regression-green.log" 2>&1

Exit 0, **4 PASS / 0 FAIL / 0 skipped / 0 todo**, 1.758 seconds. This is the
final native test execution; its complete log contains direct source metadata.

    python3 -B "$P/package-proposal.py"
    node --check "$P/proposal/remotion/attempt-envelope-pcm.mjs"
    node --check "$P/proposal/remotion/tests/gapless-mp3-source-origin.test.mjs"
    git diff --exit-code HEAD
    git diff --check

All PASS: composition/apply/whitespace, exact predecessor/helper/clock/test
identity, package archive/extraction integrity, syntax, tracked-tree identity.
Final git status --short is empty. No repository temp/build output remains.

Exploratory runs are not cited as evidence: an initial probe omitted ignored
stdin and hit sandbox EPERM; explicit stdio ['ignore','pipe','pipe'] fixed it
without changing helper behavior. One initial characterization expected a
format start=0 where this metadata probe reports absence; corrected to the
actual fact. A prototype negative control asked Node assert to format a huge
Buffer difference and its run was killed; replaced only that diagnostic with
exact Buffer.equals/SHA256 mismatch checks. Its own temporary fixture directory
was removed. The finalized identical positive tests remain ordinary red-before
and green-after; no old test was changed, skipped or marked expected-to-fail.

Prior 27-case suites and the heavy long-source regression were read, not rerun
or claimed. No full/central/named suite, browser, live socket, network, install,
render/export, actual source binding/certification, physical audio or owner film
run. No Player/export parity claim.

## Decisions, limits and next steps

Use source demuxer priming/presentation facts at the existing ffprobe seam and
let unchanged native FFmpeg honor them; no second decoder/envelope policy.
Exact integer ticks avoid mistaking rounded stream-start decimals for a source
offset. Native known-MP3 origin/count can be proved with this independent PCM
reference and full-source readback; no browser is needed for that bounded claim.

Zero/absent-start admission is inherited and remains unqualified, explicitly
including metadata-free MP3 and ADTS debt. This proposal repairs only the proven
nonzero-start false refusal. It neither removes existing accepted behavior nor
claims unknown origins safe. Other MP3 rates/encoders, AAC presentation/count,
other containers, browser decoder equivalence and damaged source metadata are
not qualified by this fixture. Real transformed-source binding, original fade
phase across full/window/layer, coordinated public11 adoption and the long-source
memory/long-WAV/time-budget seams remain the predecessor's separate holds.

Recommendation: review this delta with the long-source proposal at the existing
attempt/asset-stage seam; keep both inactive. Preserve the ordinary MP3 positive
when activating the actual producer, and resolve the named unknown-origin/count
and trusted-source joins through existing owners before claiming normal-path
compatibility. No worker blocker; no product commit required.
