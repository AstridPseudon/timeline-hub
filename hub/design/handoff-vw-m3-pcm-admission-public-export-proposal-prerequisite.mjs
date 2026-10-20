import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project" + '/package.json');
const api=await import(require.resolve('@banodoco/timeline-composition/evaluation'));
const root=await import(require.resolve('@banodoco/timeline-composition'));
assert.equal(require('@banodoco/timeline-composition/package.json').version,'0.0.12');
assert.equal(api.encodedEnvelopeSource,undefined);
assert.equal(root.encodedEnvelopeSource,undefined);
for (const name of ['compileAudioEnvelope','computeMediaTrim','getSanitizedPlaybackRate','applyAudioEnvelope','audioEnvelopeWav','validateAudioEnvelope']) assert.equal(typeof api[name],'function');
for (const suffix of ['dist/lib/audio-envelope.js','dist/lib/use-audio-envelope.js']) {
 assert.throws(()=>require.resolve('@banodoco/timeline-composition/'+suffix),{code:'ERR_PACKAGE_PATH_NOT_EXPORTED'});
}
const clip={id:'sound',at:7.5,track:'A1',from:.05,to:.55,speed:2,volume:.8,params:{fadeIn:.1,fadeOut:.1}};
const envelope=api.compileAudioEnvelope(clip,30);
const from=api.computeMediaTrim(clip,30).trimBefore/30;
const rate=api.getSanitizedPlaybackRate(clip.speed);
assert.equal(from,2/30);
const prepared={file:'https://example.test/attempt-envelope.wav',envelope_key:JSON.stringify(envelope),source_from:from,playback_rate:rate};
const fresh=()=>{
 const channel=Float32Array.from({length:48000},(_,i)=>i%2?-2:3);
 api.applyAudioEnvelope([channel],48000,envelope,from,rate);
 return Buffer.from(api.audioEnvelopeWav([channel],48000));
};
const expected=fresh();
for (const [name,change] of [['matching',{}],['wrong envelope',{envelope_key:JSON.stringify({keyframes:[{at:0,value:1}]})}],['raw origin',{source_from:.05}],['wrong rate',{playback_rate:.5}],['blob',{file:'blob:forged'}]]) {
 const render_source={...prepared,...change};
 assert.deepEqual(api.compileAudioEnvelope({...clip,audio:{render_source}},30),envelope);
 api.validateAudioEnvelope(envelope);
 assert.deepEqual(fresh(),expected);
 console.log(name+': fresh public PCM preparation identical; prepared claim not inspected');
}
console.log('Immutable public12 public surface: preparation available, exact prepared-source admission unavailable; deep imports refused.');
