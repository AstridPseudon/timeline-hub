import * as evaluation from '@banodoco/timeline-composition/evaluation';
import * as composition from '@banodoco/timeline-composition';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const pkg = require('@banodoco/timeline-composition/package.json');
const result = { version: pkg.version, evaluation: {}, root: {}, deepImport: {} };
for (const name of ['compileAudioEnvelope', 'computeMediaTrim', 'getSanitizedPlaybackRate', 'applyAudioEnvelope', 'audioEnvelopeWav', 'encodedEnvelopeSource', 'useAudioEnvelopeSource']) {
  result.evaluation[name] = typeof evaluation[name];
  result.root[name] = typeof composition[name];
}
for (const path of ['dist/lib/audio-envelope.js', 'dist/lib/use-audio-envelope.js']) {
  try { await import('@banodoco/timeline-composition/' + path); result.deepImport[path] = 'unexpected success'; }
  catch (error) { result.deepImport[path] = error.code; }
}
console.log(JSON.stringify(result, null, 2));
