import assert from 'node:assert/strict';
import test from 'node:test';
import { assertSemanticAddMediaRequest } from './p2-semantic-oracle.ts';

const before = {
  schema_version: 1,
  project_id: 'project',
  timeline_id: 'timeline',
  parent_revision: { revision_id: 'r0', content_digest: 'sha256:parent', payload: {
    config: { registry: { assets: {} } },
    registry: { assets: {} },
    occurrences: [],
  } },
  shot_revisions: [],
  internal_timeline_revisions: [],
  dependency_manifest: { shots: [], internal_timelines: [], media: [], documents: [] },
};

const base = { revision_id: 'r0', publication_id: 'p0' };
const row = { id: 'clip-new', asset: 'asset-new', track: 'V1', at: 5, hold: 2, clipType: 'media' };
const media = {
  asset: 'asset-new', generation_id: 'generation-new', variant_id: 'variant-new',
  object_id: 'sha256:0000000000000000000000000000000000000000000000000000000000000000',
  catalog_digest: 'sha256:1111111111111111111111111111111111111111111111111111111111111111',
};

function post(overrides = {}) {
  const body = {
    api_version: 1,
    project_id: 'project',
    timeline_id: 'timeline',
    base_revision_id: 'r0',
    base_publication_id: 'p0',
    commands: [{ schema_version: 1, op: 'clip.add-media', version: '1', select: 'parent', args: { row: structuredClone(row), media: structuredClone(media) }, intent: {}, created: ['parent/asset:asset-new', 'parent/clip:clip-new'] }],
    label: 'Edit timeline',
    steps: [{ id: 'place-media', label: 'Edit timeline', intent: 'Edit timeline', tags: [], command_ordinals: [0], patch: [] }],
    merge: 'fields',
    dry_run: false,
    source: { via: 'app' },
    ...overrides,
  };
  return { key: 'edit-1', body };
}

function accepts(value) {
  assert.doesNotThrow(() => assertSemanticAddMediaRequest(value, base, before, {
    op: 'clip.add-media', owner: 'parent', select: 'parent', label: 'Edit timeline',
  }));
}

test('semantic media oracle accepts the exact source shape and refuses the old shape', () => {
  accepts(post());
  assert.throws(() => assertSemanticAddMediaRequest(post({ merge: 'atomic' }), base, before, {
    op: 'clip.add-media', owner: 'parent', select: 'parent', label: 'Edit timeline',
  }));
  assert.throws(() => assertSemanticAddMediaRequest(post({ steps: [{ id: 'place-media', label: 'Place media', intent: 'Place media', tags: [], command_ordinals: [0], patch: [{}] }] }), base, before, {
    op: 'clip.add-media', owner: 'parent', select: 'parent', label: 'Edit timeline',
  }));
});

test('semantic media oracle refuses command, created, read, and submitted-patch drift', () => {
  const expected = { op: 'clip.add-media', owner: 'parent', select: 'parent', label: 'Edit timeline' };
  for (const mutate of [
    (value) => { value.body.commands = []; },
    (value) => { value.body.commands.push(structuredClone(value.body.commands[0])); },
    (value) => { value.body.commands[0].op = 'doc.patch'; },
    (value) => { value.body.commands[0].created = ['parent/clip:clip-new']; },
    (value) => { value.body.commands[0].created = ['parent/asset:asset-new', 'parent/clip:clip-new', 'parent/clip:extra']; },
    (value) => { delete value.body.commands[0].created; },
    (value) => { value.body.reads = []; },
    (value) => { value.body.unexpected = 'metadata'; },
    (value) => { value.body.commands[0].reads = []; },
    (value) => { value.body.commands[0].resolved = { extra: true }; },
    (value) => { value.body.commands[0].rationale = 123; },
    (value) => { value.body.commands[0].args.row.extra = true; },
    (value) => { value.body.commands[0].args.media.extra = true; },
    (value) => { value.body.label = 'Place media'; },
    (value) => { value.body.steps[0].reads = []; },
    (value) => { delete value.body.steps[0].patch; },
    (value) => { value.body.steps[0].patch = [{}]; },
  ]) {
    const value = post();
    mutate(value);
    assert.throws(() => assertSemanticAddMediaRequest(value, base, before, expected));
  }
});

test('semantic media oracle derives asset birth from the pregesture registry', () => {
  const authored = structuredClone(before);
  authored.parent_revision.payload.config.registry.assets['asset-new'] = { media_id: 'existing' };
  const value = post();
  value.body.commands[0].created = ['parent/clip:clip-new'];
  assert.doesNotThrow(() => assertSemanticAddMediaRequest(value, base, authored, {
    op: 'clip.add-media', owner: 'parent', select: 'parent', label: 'Edit timeline',
  }));
  value.body.commands[0].created = ['parent/asset:asset-new', 'parent/clip:clip-new'];
  assert.throws(() => assertSemanticAddMediaRequest(value, base, authored, {
    op: 'clip.add-media', owner: 'parent', select: 'parent', label: 'Edit timeline',
  }));
});
