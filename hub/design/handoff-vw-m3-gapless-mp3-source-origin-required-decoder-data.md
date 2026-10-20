# Required decoder data — inactive gapless MP3 proposal

UNAPPLIED. This is a narrow native-FFmpeg origin admission, not general codec or
Player/export qualification. The existing guard actually reads **stream**
start_time; the characterized MP3's format start_time has the same value.

At the existing local source ffprobe seam, retain:

| Source-backed field | Required for this nonzero-start relaxation |
| --- | --- |
| format.format_name | Exactly mp3, from FFmpeg's demuxer; extension is irrelevant |
| stream.codec_name | Exactly mp3 |
| stream.sample_rate / channels | Existing positive safe integers; retain unchanged |
| stream.start_time | Existing nonzero-start branch trigger; never use this rounded decimal to calculate an offset |
| stream.start_pts / time_base | Positive safe-integer ticks and positive rational numerator/denominator |
| First audio packet pts / dts | Both exactly zero |
| First packet Skip Samples skip_samples | Positive safe integer, from source demuxer side data |
| skip_reason / discard_reason | Both zero (padding), rather than an uncharacterized skip reason |
| First packet discard_padding | Zero for the characterized first packet |

Read only the first packet with ffprobe -read_intervals '%+#1'; do not collect
all packets in the proposed helper. Accept only the exact integer equation:

    start_pts * time_base.numerator * sample_rate
      == skip_samples * time_base.denominator

The proposal uses BigInt. For this source:

    324870 * 1 * 48000 == 1105 * 14112000

No fixed 0.023021/1105 exception, epsilon-based clock admission, start-time
subtraction, sample deletion, silence insertion or envelope-origin change.
FFmpeg consumes its own skip/discard metadata during the unchanged full decode.
No new DTO/source grant, caller-supplied origin token or separate decoder kernel.
The first packet probe runs only for the existing nonzero stream start branch,
and only after both codec and demuxer match. The decoder command and public
apply/WAV calls remain byte-identical to the long-source predecessor.

## Measured independent reference and packet accounting

Local ffmpeg/ffprobe 6.1.1-3ubuntu5; independent 48 kHz PCM16 stereo, 1.8 seconds,
86,400 frames. Left onset 9,606; right onset 14,405, measured at |sample| > .03.
The tones and threshold are fixed before encoding; no offset search or alignment.

| Actual full native decode | First packet PTS / skip | Stream start | Frames | L/R onset delta from original PCM |
| --- | --- | --- | ---: | --- |
| Gapless MP3 | 0 / 1105 | 0.023021 | 86400 | 0 / 1 |
| MP3 without Xing metadata | 0 / absent | 0 | 87552 | 1105 / 1106 |
| ADTS AAC | 0 / absent | absent | 88064 | 1024 / 1024 |
| M4A AAC | -1024 / 1024 | 0 | 87040 | 0 / 0 |
| Offset AAC in MKA | 104 ms / absent | 0.104 | 88064 | 1024 / 1024 |
| Offset MP3 in MKA | 102 ms / absent | 0.102 | 87505 | 1105 / 1106 |

For the gapless MP3 only, the test additionally reads all packet metadata from
its bounded 1.8-second fixture: 76 packets * 1152 frames = 87552;
87552 - first skip 1105 - last discard 47 = **86400**. Last PTS 25401600,
packet duration 338688 at time base 1/14112000. The prepared unity-envelope WAV
has exactly the complete native MP3 decoded float payload, unchanged on both
channels, and decodes back to identical float bytes. Lossy MP3 samples are not
claimed equal to the original PCM16 waveform; the 0/1 onset difference is
measured codec waveform behavior. Full frame count and logical source onset
are compared against that independent original, never against a shifted source.

The current small metadata-only ADTS probe omits both stream and format start;
the previous 27-case report obtained format start 0 with its probe. Both cases
carry no priming proof. This does not change the observed +1024-frame debt.

## Deliberately unresolved

Zero/absent stream start remains the predecessor's existing path. The proposal
does NOT certify that path: metadata-free MP3 and ADTS are concrete unsafe
examples. M4A preserves onset here but has 640 trailing native frames. Timestamped
AAC remains a refusal at the old nonzero-start guard. No existing accepted
behavior is cut and no entire codec is newly refused to make the tests green.

Before an origin-preserving normal producer may claim those cases, the existing
source-stage owner must establish the authored/native-decoder presentation
origin and complete logical sample count for each such source class, including
AAC priming and trailing padding. Preserve that relationship in existing source
admission; do not infer it from start_time=0 or absence. Future browser/Player
parity qualification must compare the original compressed source and prepared
full-source WAV at native rate/channels with no per-clip fitting, and expose
unknown metadata cases explicitly. This worker proves the bounded known MP3
native decoder path only; it makes no browser decoding or audio-device claim.
