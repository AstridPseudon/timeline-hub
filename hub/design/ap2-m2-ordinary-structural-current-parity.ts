import { readFileSync, writeFileSync } from 'node:fs';
import { authoringBundleFromDocument } from './src/tools/video-editor/commands/authoringBundle.ts';
import {
  captureOrdinaryStructuralBatch,
  executeOrdinaryStructuralBatch,
} from './src/tools/video-editor/commands/ordinaryStructuralMember.ts';

const fixture = JSON.parse(readFileSync(
  './src/tools/video-editor/commands/fixtures/authoringBundle.json', 'utf8',
));
const document = fixture.cases.find((item: { name: string }) => item.name === 'parent-only').document;
const bundle = await authoringBundleFromDocument(document);
const patch = {
  version: 1,
  operations: [
    { op: 'track.add' as const, target: 'ordinary-track', payload: {
      kind: 'visual', role: 'output', opaque: { keep: [null, false] },
    }, order: 0 },
    { op: 'clip.add' as const, target: 'ordinary-clip', payload: {
      clipType: 'text', track: 'ordinary-track', at: 1.25, hold: 2.5,
      params: { text: 'Ordinary' }, app: { opaque: { keep: [null, false] } }, nullable: null,
    }, order: 1 },
  ],
};
const added = captureOrdinaryStructuralBatch(bundle, patch);
const deletion = captureOrdinaryStructuralBatch(added.bundle, {
  version: 2,
  operations: [{ op: 'clip.remove', target: 'ordinary-clip', order: 0 }],
});
const replay = executeOrdinaryStructuralBatch(bundle, added.commands);
const deleteReplay = executeOrdinaryStructuralBatch(added.bundle, deletion.commands);
writeFileSync(process.argv[2], JSON.stringify({
  add: { commands: added.commands, records: added.records, bundle: added.bundle },
  delete: { commands: deletion.commands, records: deletion.records, bundle: deletion.bundle },
  replay: { records: replay.records, bundle: replay.bundle },
  deleteReplay: { records: deleteReplay.records, bundle: deleteReplay.bundle },
}));
