import type { CanonicalDocument, CommandRecord, EditCommand, JSON as JsonValue } from '@/integrations/runtime/timeline-commit-types.ts';

/**
 * Projection of Agent donor `recipe_m2_clip_split.json`.
 * Donor SHA-256: a0e24c1f78d8580f908973745950ed0196c17257831197ec2f75a55abc638f63.
 * The expected command and record are assembled from the authored rows here,
 * independently of the native capture implementation under test.
 */

type JsonRecord = Record<string, JsonValue>;
type State = { state: 'absent' } | { state: 'present'; value: JsonValue };

const copy = <T,>(value: T): T => structuredClone(value);
const present = (value: JsonValue): State => ({ state: 'present', value: copy(value) });
const absent = (): State => ({ state: 'absent' });

const clipA = (): JsonRecord => ({
  id: 'clip-a', track: 'picture', asset: 'picture', clipType: 'media', at: 1, hold: 8,
  app: {
    'org.example': { literal: 'clip-a', clear: null },
    astrid: { for: 4, opaque: { for: 'literal' } },
  },
  from: 2, to: 10, speed: 2,
  opaque: { nested: [null, false, 0, {}, []], literal: 'clip-a' },
  params: { volume: 0.7, unknown: [null, false] },
});

const clipB = (): JsonRecord => ({
  id: 'clip-b', track: 'picture', asset: 'picture', clipType: 'media', at: 5, hold: 2,
  app: { 'org.example': { literal: 'clip-a', clear: null } },
});

const parentPayload = (): JsonRecord => ({
  config: {
    tracks: [{ id: 'picture', kind: 'visual' }],
    clips: [clipA(), clipB()],
    output: { fps: { numerator: 30000, denominator: 1001 } },
    opaque: { timestamp: 'authored timestamp', v: [null, false, 0] },
  },
  clips: [clipA(), clipB()],
  registry: {
    assets: {
      picture: {
        media_id: 'sha256:1111111111111111111111111111111111111111111111111111111111111111',
        type: 'video', duration: 20,
      },
    },
  },
  occurrences: [], name: 'Renamed Film', unknown: { opaque: ['parent-1', null] },
});

const input = {
  schema_version: 1,
  project_id: 'project-1',
  timeline_id: 'film',
  parent_revision: {
    revision_id: 'parent-1',
    payload: parentPayload(),
    content_digest: 'sha256:66e4590cbf1c2d8e06bd3c7e0dbd094dd9e0a1c18ec4b842b8c4839133895953',
  },
  shot_revisions: [],
  internal_timeline_revisions: [],
  dependency_manifest: {
    shots: [], internal_timelines: [],
    media: [{
      media_id: 'sha256:1111111111111111111111111111111111111111111111111111111111111111',
      content_digest: 'sha256:1111111111111111111111111111111111111111111111111111111111111111',
    }],
    documents: [],
  },
} as unknown as CanonicalDocument;

const inputJson = input as unknown as JsonRecord;
const payload = inputJson.parent_revision as JsonRecord;
const authored = payload.payload as JsonRecord;
const originalRows = authored.clips as JsonValue[];
const target = copy(originalRows[0]) as JsonRecord;
const neighbor = copy(originalRows[1]) as JsonRecord;
const left = { ...copy(target), hold: 4, to: 6 } as JsonRecord;
const right = { ...copy(target), id: 'right', at: 3, hold: 4, from: 6 } as JsonRecord;
((left.app as JsonRecord).astrid as JsonRecord).for = 2;
((right.app as JsonRecord).astrid as JsonRecord).for = 2;
const beforeRows = [copy(target), copy(neighbor)] as JsonValue[];
const afterRows = [copy(left), copy(right), copy(neighbor)] as JsonValue[];

const read = (ref: string, path: string[], state: State): JsonRecord => ({ ref, path, state });
const absentRelations = [
  'on', 'fixed_start', 'until', 'until_film_end', 'for', 'cut', 'sequence', 'sequence_index',
  'sequence_fit', 'orphan', 'formulas', 'anchor', 'standin', 'standin_intent',
];
const absentReads = ['', 'app', 'app.astrid'].flatMap((prefix) => absentRelations.map((key) => read(
  'parent/clip:clip-b', prefix ? prefix.split('.').concat(key) : [key], absent(),
)));
const reads = [
  read('parent/collection:clip', [], present({
    members: present([]), config: present({}), payload_members: present([]),
  })),
  read('parent/clip:clip-a', [], present(target)),
  read('parent/registry', ['assets', 'picture'], present({
    media_id: 'sha256:1111111111111111111111111111111111111111111111111111111111111111',
    type: 'video', duration: 20,
  })),
  ...absentReads,
  read('parent/clip:clip-b', ['transition'], absent()),
  read('parent', ['config', 'output', 'fps'], present({ numerator: 30000, denominator: 1001 })),
  read('parent/clip:right', [], absent()),
];

const selections = [
  {
    key: 'collection.clips', query_version: 1, owner: 'parent',
    members: ['parent/clip:clip-a', 'parent/clip:clip-b'],
    order: ['parent/clip:clip-a', 'parent/clip:clip-b'],
    boundaries: ['parent/clip:clip-a', 'parent/clip:clip-b'], policy: 'guard-membership',
  },
  {
    key: 'collection.clips.after', query_version: 1, owner: 'parent',
    members: ['parent/clip:clip-a'],
    order: ['parent/clip:clip-a', 'parent/clip:clip-b'],
    boundaries: ['parent/clip:clip-a', 'parent/clip:clip-b'], policy: 'guard-membership',
  },
];
const bindings = [{ key: 'split.target', ref: 'parent/clip:clip-a', policy: 'fixed', dependencies: [] }];
const created = [{ ref: 'parent/clip:right', kind: 'clip', owner: 'parent' }];
const expect = {
  'parent/clip:right::': absent(),
  'parent/clip:clip-a::hold': present(8),
  'parent/clip:clip-a::to': present(10),
  'parent/clip:clip-a::app.astrid.for': present(4),
};
const authorship = {
  'parent/clip:right::': 'direct',
  'parent/clip:clip-a::hold': 'direct',
  'parent/clip:clip-a::to': 'direct',
  'parent/clip:clip-a::app.astrid.for': 'direct',
};

const command = {
  schema_version: 1, op: 'clip.split', version: '1', select: 'parent/clip:clip-a',
  args: { on: 3, right_id: 'right' }, intent: {}, resolved: ['parent/clip:clip-a'], reads,
  selections, bindings: { 'split.target': 'parent/clip:clip-a' }, created: ['parent/clip:right'],
  expect, authorship,
} as unknown as EditCommand;
const writes = [
  { ref: 'parent/clip:right', path: [], before: absent(), after: present(right) },
  { ref: 'parent/clip:clip-a', path: ['hold'], before: present(8), after: present(4) },
  { ref: 'parent/clip:clip-a', path: ['to'], before: present(10), after: present(6) },
  { ref: 'parent/clip:clip-a', path: ['app', 'astrid', 'for'], before: present(4), after: present(2) },
];
const record = {
  ordinal: 0, command: copy(command), writes, reads, selections,
  bindings, created, dependencies: [],
  derived_writes: [{ ref: 'parent', path: ['config', 'clips'], before: present(beforeRows), after: present(afterRows), cause: 0 }],
} as unknown as CommandRecord;

const output = copy(input);
const outputJson = output as unknown as JsonRecord;
const outputPayload = (outputJson.parent_revision as JsonRecord).payload as JsonRecord;
(outputPayload.config as JsonRecord).clips = copy(afterRows);
outputPayload.clips = copy(afterRows);
(outputJson.parent_revision as JsonRecord).revision_id =
  'authoring-parent-revision-c806c2a6991bf0ba1fc2b0b35bc16f91c443a8c5eaf22cbbe9a4ecfba9999527';
(outputJson.parent_revision as JsonRecord).content_digest =
  'sha256:76192229a72046cec36b533a3d4643ca922dc52da44f57c2090efc663da34167';

export default { input, commands: [command], records: [record], output };
