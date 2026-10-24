// Pure controls for the mounted P2 parent-move request assertion; no browser or Runtime execution.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { compileFunction } from 'node:vm';
import { expect } from '@playwright/test';
import ts from 'typescript';

const source = readFileSync(new URL('../three-products.p2-tour.spec.ts', import.meta.url), 'utf8');
const helper = source.match(/^function assertParentMoveRequestV2\([^]*?^}/m)?.[0];
assert.ok(helper, 'exercise the actual mounted parent-move assertion helper');
const check = compileFunction(`${ts.transpileModule(helper, {}).outputText}\nreturn assertParentMoveRequestV2;`, ['expect'])(expect);

const original = {
  parent_revision: {
    payload: {
      config: {
        clips: [
          { id: 'f2-app-clip', at: 0, track: 'V1', clipType: 'media', from: 0, to: 3, speed: 1, asset: 'f2-app' },
          { id: 'f2-transition-clip', at: 15, track: 'V1', clipType: 'media', from: 0, to: 3, speed: 1, asset: 'f2-video' },
        ],
        tracks: [{ id: 'V1', kind: 'visual', label: 'V1' }],
        output: { fps: 30 },
      },
      registry: { assets: { 'f2-app': { object_id: 'sha256:image' }, 'f2-video': { object_id: 'sha256:video' } } },
    },
  },
};

const reads = [
  ['id', 'f2-app-clip', { state: 'present', value: 'f2-app-clip' }],
  ['track', 'f2-app-clip', { state: 'present', value: 'V1' }],
  ['at', 'f2-app-clip', { state: 'present', value: 0 }],
  ['clipType', 'f2-app-clip', { state: 'present', value: 'media' }],
  ['hold', 'f2-app-clip', { state: 'absent' }],
  ['from', 'f2-app-clip', { state: 'present', value: 0 }],
  ['to', 'f2-app-clip', { state: 'present', value: 3 }],
  ['speed', 'f2-app-clip', { state: 'present', value: 1 }],
  ['asset', 'f2-app-clip', { state: 'present', value: 'f2-app' }],
  ['fps', 'output', { state: 'present', value: 30 }],
  ['f2-app', 'assets', { state: 'present', value: original.parent_revision.payload.registry.assets['f2-app'] }],
  ['kind', 'V1', { state: 'present', value: 'visual' }],
  ['pinnedShotGroups', 'config', { state: 'absent' }],
  ['collection', 'clips', null],
  ['track', 'f2-transition-clip', { state: 'present', value: 'V1' }],
  ['id', 'f2-transition-clip', { state: 'present', value: 'f2-transition-clip' }],
  ['track', 'f2-transition-clip', { state: 'present', value: 'V1' }],
  ['at', 'f2-transition-clip', { state: 'present', value: 15 }],
  ['clipType', 'f2-transition-clip', { state: 'present', value: 'media' }],
  ['hold', 'f2-transition-clip', { state: 'absent' }],
  ['from', 'f2-transition-clip', { state: 'present', value: 0 }],
  ['to', 'f2-transition-clip', { state: 'present', value: 3 }],
  ['speed', 'f2-transition-clip', { state: 'present', value: 1 }],
  ['asset', 'f2-transition-clip', { state: 'present', value: 'f2-video' }],
  ['f2-video', 'assets', { state: 'present', value: original.parent_revision.payload.registry.assets['f2-video'] }],
];

function fieldRead(path, state) {
  return { kind: 'field', ref: 'parent', path, state };
}

function fixture() {
  const collection = { kind: 'collection', ref: 'parent', path: ['config', 'clips'], members: ['f2-app-clip', 'f2-transition-clip'], order: ['f2-app-clip', 'f2-transition-clip'] };
  const expectedReads = reads.map(([key, owner, state]) => {
    if (key === 'collection') return collection;
    if (key === 'fps') return fieldRead(['config', 'output', 'fps'], state);
    if (key === 'f2-app' || key === 'f2-video') return fieldRead(['config', 'registry', 'assets', key], state);
    if (key === 'kind') return fieldRead(['config', 'tracks', `id:${owner}`, 'kind'], state);
    if (key === 'pinnedShotGroups') return fieldRead(['config', key], state);
    return fieldRead(['config', 'clips', `id:${owner}`, key], state);
  });
  const changes = [{ op: 'set', ref: 'parent', path: ['clips', 'id:f2-app-clip', 'at'], before: { state: 'present', value: 0 }, value: 5 }];
  return {
    post: {
      key: 'receipt',
      body: {
        api_version: 1, project_id: 'project', timeline_id: 'timeline',
        base_revision_id: 'revision', base_publication_id: 'publication',
        commands: [{ schema_version: 1, op: 'doc.patch', version: '1', select: null, created: [], args: { changes } }],
        label: 'Edit timeline',
        steps: [{ id: 'step', label: 'Edit timeline', intent: 'Move f2-app-clip on V1', tags: [], command_ordinals: [0], patch: changes, reads: expectedReads }],
        merge: 'fields', reads: expectedReads, dry_run: false, source: { via: 'app' },
      },
    },
    expectedReads,
  };
}

test('actual helper accepts the exact parent move request shape', () => {
  const { post } = fixture();
  check(post, { revision_id: 'revision', publication_id: 'publication' }, original, 'f2-app-clip', 5);
});

test('actual helper refuses malformed, missing, and extra parent move variants', () => {
  const { post } = fixture();
  const variants = [
    (candidate) => { delete candidate.body.commands[0].created; },
    (candidate) => { candidate.body.commands[0].created = ['parent/clip:unexpected']; },
    (candidate) => { delete candidate.body.reads; },
    (candidate) => { candidate.body.reads = [...candidate.body.reads, { kind: 'scope', ref: 'timeline', path: [] }]; },
    (candidate) => { candidate.body.steps[0].reads = candidate.body.steps[0].reads.slice(0, -1); },
    (candidate) => { candidate.body.reads[0].path[3] = 'wrong'; },
    (candidate) => { candidate.body.steps[0].reads[0].path[3] = 'wrong'; },
    (candidate) => { candidate.body.reads[0].state.value = 'wrong'; },
    (candidate) => { candidate.body.steps[0].reads[0].state.value = 'wrong'; },
    (candidate) => { candidate.body.reads[0].state.state = 'absent'; },
    (candidate) => { candidate.body.steps[0].reads[0].state.state = 'absent'; },
    (candidate) => { candidate.body.extra = true; },
    (candidate) => { candidate.body.commands[0].extra = true; },
    (candidate) => { candidate.body.steps[0].extra = true; },
    (candidate) => { candidate.body.commands[0].select = { extra: true }; },
    (candidate) => { candidate.body.commands[0].args.extra = true; },
    (candidate) => { candidate.body.base_revision_id = 'other-revision'; },
    (candidate) => { candidate.body.base_publication_id = 'other-publication'; },
    (candidate) => { candidate.body.merge = 'atomic'; },
    (candidate) => { candidate.body.commands[0].op = 'clip.move'; },
    (candidate) => { candidate.body.commands[0].args.changes[0].value = 4; },
    (candidate) => { candidate.body.steps[0].intent = 'Save local editor changes'; },
    (candidate) => { candidate.body.rationale = 'extra'; },
  ];
  for (const mutate of variants) {
    const candidate = structuredClone(post);
    mutate(candidate);
    assert.throws(() => check(candidate, { revision_id: 'revision', publication_id: 'publication' }, original, 'f2-app-clip', 5));
  }
});
