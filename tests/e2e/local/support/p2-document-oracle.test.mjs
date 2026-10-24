import assert from 'node:assert/strict';
import test from 'node:test';
import { assertCatalogDocumentPatch, assertInverseRequestV2, assertParamsDocumentPatch } from './p2-document-oracle.ts';

const clips = [
  { id: 'f2-app-clip', clipType: 'media', hold: 2, from: 0, to: 2, speed: 1, track: 'V1', at: 0, asset: 'f2-app' },
  { id: 'f2-transition-clip', clipType: 'transition', hold: 1, from: 0, to: 1, speed: 1, track: 'V1', at: 2, asset: 'f2-video' },
];
const original = { schema_version: 1, project_id: 'p', timeline_id: 't', parent_revision: { payload: { config: { clips, tracks: [{ id: 'V1', kind: 'visual' }] } } } };
const base = { revision_id: 'r0', publication_id: 'p0' };

function post(branch, changes, reads, created = [], intent = branch === 'catalog' ? 'timeline.apply_element' : 'timeline.update_element') {
  return { key: 'k1', body: {
    api_version: 1, project_id: 'p', timeline_id: 't', base_revision_id: 'r0', base_publication_id: 'p0',
    commands: [{ schema_version: 1, op: 'doc.patch', version: '1', select: null, created, args: { changes } }],
    label: 'Edit timeline', steps: [{ id: 's1', label: 'Edit timeline', intent, tags: [], command_ordinals: [0], patch: changes, reads }],
    merge: 'atomic', reads, dry_run: false, source: { via: 'app' },
  } };
}

const catalogReads = [
  { kind: 'collection', ref: 'parent', path: ['config', 'clips'], members: ['f2-app-clip', 'f2-transition-clip'].sort(), order: ['f2-app-clip', 'f2-transition-clip'] },
  ...['id', 'clipType', 'hold', 'from', 'to', 'speed', 'track', 'at'].map((key) => ({ kind: 'field', ref: 'parent', path: ['config', 'clips', 'id:f2-app-clip', key], state: { state: 'present', value: clips[0][key] } })),
  { kind: 'field', ref: 'parent', path: ['config', 'clips', 'id:f2-transition-clip', 'id'], state: { state: 'present', value: 'f2-transition-clip' } },
  { kind: 'field', ref: 'parent', path: ['config', 'tracks'], state: { state: 'present', value: [{ id: 'V1', kind: 'visual' }] } },
];

test('document oracle accepts exact catalog and params shapes', () => {
  const catalog = post('catalog', [{ op: 'list.insert', ref: 'parent', path: ['clips'], id: 'new', before: { state: 'absent' }, value: { id: 'new', elementRef: { id: 'am-burst', kind: 'effect', packId: 'astrid_motion' } }, order_before: ['f2-app-clip', 'f2-transition-clip'], after_id: 'f2-transition-clip' }], catalogReads, ['parent/clip:new']);
  assert.doesNotThrow(() => assertCatalogDocumentPatch(catalog, base, original, 'f2-app-clip'));

  const paramsBase = { schema_version: 1, project_id: 'p', timeline_id: 't', parent_revision: { payload: { config: { clips: [...clips, { id: 'new', elementRef: { id: 'am-burst', kind: 'effect', packId: 'astrid_motion' } }], tracks: [{ id: 'V1', kind: 'visual' }] } } } };
  const paramsReads = [
    { kind: 'collection', ref: 'parent', path: ['config', 'clips'], members: ['f2-app-clip', 'f2-transition-clip', 'new'].sort(), order: ['f2-app-clip', 'f2-transition-clip', 'new'] },
    ...['id'].map((key) => ({ kind: 'field', ref: 'parent', path: ['config', 'clips', 'id:f2-app-clip', key], state: { state: 'present', value: 'f2-app-clip' } })),
    ...['id'].map((key) => ({ kind: 'field', ref: 'parent', path: ['config', 'clips', 'id:f2-transition-clip', key], state: { state: 'present', value: 'f2-transition-clip' } })),
    { kind: 'field', ref: 'parent', path: ['config', 'clips', 'id:new', 'id'], state: { state: 'present', value: 'new' } },
    { kind: 'field', ref: 'parent', path: ['config', 'clips', 'id:new', 'elementRef'], state: { state: 'present', value: paramsBase.parent_revision.payload.config.clips[2].elementRef } },
    { kind: 'field', ref: 'parent', path: ['config', 'clips', 'id:new', 'params'], state: { state: 'absent' } },
  ];
  const params = post('params', [{ op: 'set', ref: 'parent', path: ['clips', 'id:new', 'params', 'bob'], before: { state: 'absent' }, value: 12 }], paramsReads);
  assert.doesNotThrow(() => assertParamsDocumentPatch(params, base, paramsBase, 'new'));
});

test('document oracle refuses missing, extra, reordered, and forged branch claims', () => {
  const change = { op: 'list.insert', ref: 'parent', path: ['clips'], id: 'new', before: { state: 'absent' }, value: { id: 'new', elementRef: { id: 'am-burst', kind: 'effect', packId: 'astrid_motion' } }, order_before: ['f2-app-clip', 'f2-transition-clip'], after_id: 'f2-transition-clip' };
  for (const mutate of [
    (value) => { value.body.reads = value.body.reads.slice(1); value.body.steps[0].reads = value.body.reads; },
    (value) => { value.body.reads.push({ kind: 'scope', ref: 'parent', path: [] }); value.body.steps[0].reads = value.body.reads; },
    (value) => { value.body.commands[0].created = []; },
    (value) => { value.body.commands[0].args.changes[0].order_before = ['f2-transition-clip', 'f2-app-clip']; },
    (value) => { value.body.steps[0].intent = 'wrong'; },
  ]) {
    const value = post('catalog', [structuredClone(change)], catalogReads, ['parent/clip:new']);
    mutate(value);
    assert.throws(() => assertCatalogDocumentPatch(value, base, original, 'f2-app-clip'));
  }
});

test('inverse oracle requires full v2 fields metadata and no reads', () => {
  const value = { key: 'undo-1', body: {
    api_version: 1, project_id: 'p', timeline_id: 't', base_revision_id: 'r1', base_publication_id: 'p1',
    commands: [{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: ['target'] } }],
    label: 'Undo timeline', steps: [{ id: 's1', label: 'Undo timeline', intent: 'Undo timeline', tags: [], command_ordinals: [0], patch: [] }],
    merge: 'fields', dry_run: false, source: { via: 'app' },
  } };
  assert.doesNotThrow(() => assertInverseRequestV2(value, { revision_id: 'r1', publication_id: 'p1' }, 'target'));
  for (const mutate of [
    (item) => { item.body.merge = 'atomic'; },
    (item) => { item.body.reads = []; },
    (item) => { item.body.steps[0].patch = [{}]; },
    (item) => { item.body.commands[0].args.publications = ['other']; },
  ]) {
    const copy = structuredClone(value);
    mutate(copy);
    assert.throws(() => assertInverseRequestV2(copy, { revision_id: 'r1', publication_id: 'p1' }, 'target'));
  }
});
