import {encodedEnvelopeSource, compileAudioEnvelope, computeMediaTrim,
  getSanitizedPlaybackRate, type EncodedEnvelopeSource} from '@banodoco/timeline-composition/evaluation';
const clip = {id: 'sound', track: 'A1', at: 7.5, from: .05, to: .55, speed: 2,
  params: {fadeIn: .1, fadeOut: .1}};
const envelope = compileAudioEnvelope(clip, 30)!;
const record: EncodedEnvelopeSource = {file: 'https://example.test/pcm.wav',
  envelope_key: JSON.stringify(envelope), source_from: computeMediaTrim(clip, 30).trimBefore / 30,
  playback_rate: getSanitizedPlaybackRate(clip.speed)};
const source: string = encodedEnvelopeSource(record, envelope, record.source_from, record.playback_rate);
void source;
// @ts-expect-error The existing source clock remains numeric.
const invalid: EncodedEnvelopeSource = {...record, playback_rate: '2'};
// @ts-expect-error Admission requires the existing source clock arguments.
encodedEnvelopeSource(record, envelope);
void invalid;
