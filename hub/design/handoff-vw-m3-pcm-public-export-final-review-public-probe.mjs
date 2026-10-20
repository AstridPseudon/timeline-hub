import assert from 'node:assert/strict';
import {createRequire, register} from 'node:module';
import {readFileSync} from 'node:fs';
import {dirname, resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
const require = createRequire("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-public-export-final-review" + '/public-probe.mjs');
const entry = require.resolve('@banodoco/timeline-composition/evaluation');
const inspect = (path, seen = new Set()) => {
  if (seen.has(path)) return;
  seen.add(path);
  for (const match of readFileSync(path, 'utf8').matchAll(/(?:from\s*|import\s*\()(['"])([^'"]+)\1/g)) {
    const specifier = match[2];
    assert.ok(specifier.startsWith('.'), `Evaluation imports runtime peer ${specifier}`);
    inspect(resolve(dirname(path), specifier), seen);
  }
};
inspect(entry);
register('data:text/javascript,' + encodeURIComponent(`
 export async function resolve(specifier, context, nextResolve) {
  if (!specifier.startsWith('.') && !specifier.startsWith('file:')) throw new Error('Runtime peer: ' + specifier);
  return nextResolve(specifier, context);
 }
`), import.meta.url);
for (const name of ['window','document','fetch','AudioContext','setTimeout','setInterval']) {
 Object.defineProperty(globalThis,name,{get(){throw new Error('Browser side effect: '+name)}});
}
const api=await import(pathToFileURL(entry).href);
assert.equal(typeof api.encodedEnvelopeSource,'function');
assert.equal(api.useAudioEnvelopeSource,undefined);
assert.equal(api.envelopeKey,undefined);
const clip={id:'sound',at:7.5,track:'A1',from:.05,to:.55,speed:2,params:{fadeIn:.1,fadeOut:.1}};
const envelope=api.compileAudioEnvelope(clip,30);
const from=api.computeMediaTrim(clip,30).trimBefore/30;
const rate=api.getSanitizedPlaybackRate(clip.speed);
const prepared={file:'https://example.test/attempt-envelope.wav',envelope_key:JSON.stringify(envelope),source_from:from,playback_rate:rate};
assert.equal(api.encodedEnvelopeSource(prepared,envelope,from,rate),prepared.file);
for(const change of [{envelope_key:JSON.stringify({keyframes:[{at:0,value:1}]})},{source_from:.05},{playback_rate:.5},{file:'blob:forged'}]) {
 assert.throws(()=>api.encodedEnvelopeSource({...prepared,...change},envelope,from,rate),api.AudioEnvelopeError);
}
console.log('Built public evaluation: matching prepared positive + four strict refusals; transitive graph has no runtime peers; browser side-effect traps untouched.');
