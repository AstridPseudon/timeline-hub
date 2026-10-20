# Long audio source compatibility — complete UNAPPLIED proposal

**2 ordinary positive/control tests pass. The identical long-source positive fails
on d2ad with ENOBUFS. File-backed decoding removes the arbitrary PCM stdout cap;
public11 still requires whole-source memory, so bounded-memory adoption is HELD
at the exact Composition/Agent seams below. No product activation.**

Only two new worktree files, both flat design artifacts:

- `design/long-audio-source-compat.md`: derivation, exact predecessor, measured
  resource use, source-owner seams and unchanged activation dependencies.
- `design/long-audio-source-compat.patch`: UNAPPLIED delta atop exact d2ad helpers,
  changing the inactive decoder and adding ordinary
  `remotion/tests/long-audio-source.test.mjs`. Tested source lives only in own
  disposable ORCH proposal directory. Public-clock adapter is byte-identical.

Base Agent `384918908aa8c75229c2b6ccdd8fda03b7ce24a1`. `git diff --exit-code HEAD`
is 0: all tracked product/tests/pins/source/core/provider files remain unchanged.
No integration or other worker write, commit/merge/checkout/rebase/push.

Read PLAN, audio compile contract, completed prep/public-clock/codec-origin
ORCHREPORTs and previous normal-source proposal. Exact sources retrieved with
`git show` from `fd9f50f490aaa47465eee947d9fb370a9387c1ac` and
`d2ad2ff8290c8b11d8f97ccc7d669bd7a451daf5`. Existing flat normal-source proposal
also contains the same inactive helper; this patch is its later delta, not a
second helper. Public11 archive SHA256
`dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601` and all 77
used extraction members matched the archive; only advertised exports imported.
No install, dependency mutation, package build or new package/pin adoption.

## Demonstrated behavior and resource bound

The proposed decoder sends FFmpeg stdout directly to an exclusive attempt-local
file descriptor (the existing normal render path also uses stdout-to-file).
Read frame-aligned small blocks into the existing full-source planar arrays;
call unchanged public apply/WAV once, without copying DSP or shifting clock
arithmetic. Remove decoded scratch; publish only a fresh float WAV. Cleanup on
nonfinite PCM/empty decode removes only the new directory, retaining unrelated
attempt files. Process/IO/allocation/public-envelope errors remain honest.

One independently written native float PCM source, 48 kHz, two unequal channels,
8,388,609 frames, 174.7626875 s: **67,108,872 decoded bytes = 64 MiB + 8**.
Rational fps 30000/1001; public source clock
`{source_from: 0.06673333333333334, playback_rate: 1.5}`. All full-source WAV
bytes match independent whole-source channels through public apply/WAV:
SHA256 `8592a32de5b2c4f46fd176ac2129edfcea2ab9489aa0b0e178c8049b2e4681a2`.
Final WAV size 67,108,916 bytes. Real FFmpeg output readback retains full count,
original rate/channels, unequal boosted tail impulses; clip volume 7 is not
baked. Metadata/source graph/input bytes remain unchanged. No resample,
normalization, alignment, trim, padding, time shift, truncation, mixing or final
codec is used. No layer/window/codec/size refusal is introduced or approved.

Peak Node process RSS **193,308 KiB (~188.8 MiB)** in the final run, including
its sequential reference computation. Whole-source arrays plus public WAV are
approximately 2D live data, rather than retaining another D-byte stdout buffer.
This is measured fixture use, NOT duration-independent bounded memory. One Node
test process; all FFprobe/FFmpeg children sequential, FFmpeg decode threads=1;
one large fixture at a time. Authorized dispatch metadata has heavy=1 and the
regression requires explicit TIMELINE_HEAVY=1. Generated WAV/PCM scratch removed
by finally blocks; no build output, caches or temporary files in the worktree.

## Exact final verification

Working directory `/home/user/work/wt/vw-m3-long-audio-source-compat`.
Here `P=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-long-audio-source-compat`.
Both absolute ORCH and Viewing QUIET markers were absent (the ORCH symlink was
dangling) at inspection. Local Node 22.22.0; real local FFmpeg/FFprobe.

```sh
env -u NODE_OPTIONS -u NODE_PATH TIMELINE_HEAVY=1 node --expose-gc "$P/base/remotion/tests/long-audio-source.test.mjs" > "$P/regression-red.log" 2>&1
```

**Exit 1; 1 PASS / 1 FAIL / 0 skipped, 1.337 s.** Same ordinary positive test,
byte-identical test file against the exact untouched d2ad helper: long source
fails `spawnSync ffmpeg ENOBUFS`; cleanup control passes. This RED is retained
as evidence and not rewritten into a refusal expectation/xfail.

```sh
env -u NODE_OPTIONS -u NODE_PATH TIMELINE_HEAVY=1 node --expose-gc "$P/proposal/remotion/tests/long-audio-source.test.mjs" > "$P/regression-green.log" 2>&1
```

**Exit 0; 2 PASS / 0 FAIL / 0 skipped / 0 todo, 3.416 s.** Public whole-source
byte identity, actual decode/readback, clocks/full source/native header,
immutability/tail boost, success/error cleanup and unrelated-file preservation.

```sh
python3 -B "$P/package-proposal.py"
python3 -B "$P/check-patch.py"
node --check "$P/proposal/remotion/attempt-envelope-pcm.mjs"
node --check "$P/proposal/remotion/tests/long-audio-source.test.mjs"
git diff --exit-code HEAD
git diff --check
git diff --no-index --check /dev/null design/long-audio-source-compat.md
```

Packaging/identity/syntax/tracked-tree/whitespace checks **PASS**. No-index
returns its normal 1 for a new-file difference, with no diagnostics.
`check-patch.py` runs `git apply --check --whitespace=error-all` and `git apply`
in own disposable d2ad copy, then compares both resulting files with the tested
proposal. It does not apply the patch to the worktree or integration.

Initial instrumentation attempt `/usr/bin/time -v node ...` exited 127 because
/usr/bin/time is absent; no tests ran. Switched to native process.resourceUsage.
Initial `node --test --test-concurrency=1` harness invocations each reported one
file-wrapper pass, without individual cases; those are not cited as two-test
evidence. Direct native Node invocation executes/reports the ordinary node:test
cases in one process. An earlier direct two-case prototype also passed but used
the old helper with an explicit fixture allowance as oracle; the final regression
above instead uses independent full-source public apply/WAV arrays. Final code
and actual evidence are exactly those packaged in the delta.

Prior 22/27-case results belong to predecessor reports and were not rerun or
claimed here. No existing test rewritten/deleted/disabled; no new xfail/skip.
No full/central/named suite, network, browser, socket, renderer/export, actual
normal-route trusted source, physical Player/export parity or owner film run.

## Decisions, remaining seams and next steps

Chose file-backed synchronous stdout and small reads: reuse existing OS
subprocess/file handling, preserve exact public calls and byte identity, avoid
new framework or speculative gain policy. Removing an arbitrary stdout limit
is not sufficient to promise arbitrary-length memory safety with current API.

**Exact bounded-memory seam returned to Composition owner:** existing
`typescript/src/lib/audio-envelope.ts:applyAudioEnvelope` needs an optional
absolute source sample offset, default zero, with the existing sample-time
expression using `sample + sourceSampleOffset` before division. Existing
`audioEnvelopeWav` needs bounded file/sink serialization preserving RIFF float
bytes and native layout. Its current uint32 RIFF sizes wrap on sufficiently long
files; support an appropriate long WAV representation through the actual
consumer instead of installing another size refusal. No such API/format change
is made here. Adjusting sourceFrom per chunk rearranges floating operations and
is not a byte-exact public-clock substitute.

**Agent owner:** compose those existing public operations with descriptor-backed
decode at the already identified attempt/asset-stage seam in
`astrid/packs/rendering/rendering/renderers/remotion/run.py:_execute_remotion_locked`,
after admitted materialization/canonical compilation and before props write.
Keep source binding, stream origin/priming and original envelope phase correct;
use existing served disposable root/lifetime. The inherited 30-second deadline
is not arbitrary-length qualification either; resource lifecycle belongs there.

Recommendation: retain this as an offline 64 MiB compatibility proposal and
positive regression. Do not adopt it as a bounded-memory/all-size solution or
activate producer/provider/core/pins. Resolve the exact public block/long-WAV
seams plus prior trusted transformed-source binding, full/window/layer fade
phase, compatible codec origin and coordinated public11 adoption, then qualify
the original normal-path positive requirements. Valid long music beds remain
a requirement; no compatibility cut is requested. Worker scope is complete;
these named downstream holds are not a missing worker action.
