import { expect } from '@playwright/test';
import type { CanonicalDocument, CommitRead, HeadPin } from '../../../../src/integrations/runtime/timeline-commit-types.ts';

type JsonObject = Record<string, unknown>;
type DocumentPatchPost = { key: string; body: Record<string, any> };
type DocumentPatchBranch = 'catalog' | 'params';

function object(value: unknown, label: string): JsonObject {
  expect(value, label).toBeTruthy();
  expect(typeof value, label).toBe('object');
  expect(Array.isArray(value), label).toBe(false);
  return value as JsonObject;
}

function state(row: JsonObject, key: string): CommitRead['state'] {
  return Object.hasOwn(row, key)
    ? { state: 'present', value: row[key] as never }
    : { state: 'absent' };
}

function sourceClips(document: CanonicalDocument): { parent: JsonObject; config: JsonObject; path: string[]; rows: JsonObject[] } {
  const parent = object(document.parent_revision.payload, 'parent payload');
  const config = object(parent.config, 'parent config');
  const topLevelClips = !Object.hasOwn(config, 'clips') && Array.isArray(parent.clips);
  const rows = (topLevelClips ? parent.clips : config.clips) as Array<JsonObject>;
  expect(Array.isArray(rows), 'authored parent clips').toBe(true);
  return { parent, config, path: topLevelClips ? ['clips'] : ['config', 'clips'], rows };
}

function readField(row: JsonObject, path: string[], key: string): CommitRead {
  return { kind: 'field', ref: 'parent', path: [...path, `id:${String(row.id)}`, key], state: state(row, key) };
}

export function documentReads(document: CanonicalDocument, branch: DocumentPatchBranch, selectedId: string): CommitRead[] {
  const { config, path, rows } = sourceClips(document);
  const order = rows.map((row) => String(row.id));
  expect(order.every(Boolean), 'authored clip identities').toBe(true);
  const reads: CommitRead[] = [{ kind: 'collection', ref: 'parent', path, members: [...order].sort(), order }];
  for (const row of rows) {
    reads.push(readField(row, path, 'id'));
    if (String(row.id) !== selectedId) continue;
    const keys = branch === 'catalog'
      ? ['clipType', 'hold', 'from', 'to', 'speed', 'track', 'at']
      : ['elementRef', 'params'];
    for (const key of keys) reads.push(readField(row, path, key));
  }
  if (branch === 'catalog') {
    reads.push({ kind: 'field', ref: 'parent', path: ['config', 'tracks'], state: state(config, 'tracks') });
  }
  return reads;
}

function assertRequestEnvelope(post: DocumentPatchPost, before: HeadPin, reads: CommitRead[], label: string, intent: string): JsonObject {
  expect(post.key).toMatch(/\S/);
  const body = post.body;
  expect(Object.keys(body).sort()).toEqual(['api_version', 'base_publication_id', 'base_revision_id', 'commands', 'dry_run', 'label', 'merge', 'project_id', 'reads', 'source', 'steps', 'timeline_id'].sort());
  expect(body).toMatchObject({
    api_version: 1,
    project_id: expect.any(String),
    timeline_id: expect.any(String),
    base_revision_id: before.revision_id,
    base_publication_id: before.publication_id,
    label,
    merge: 'atomic',
    reads,
    dry_run: false,
    source: { via: 'app' },
  });
  expect(body.commands).toHaveLength(1);
  expect(body.steps).toHaveLength(1);
  const command = object(body.commands[0], 'document patch command');
  expect(Object.keys(command).sort()).toEqual(['args', 'created', 'op', 'schema_version', 'select', 'version']);
  expect(command).toMatchObject({ schema_version: 1, op: 'doc.patch', version: '1', select: null });
  expect(Object.keys(object(command.args, 'document patch args')).sort()).toEqual(['changes']);
  expect(body.steps[0]).toMatchObject({ label, intent, tags: [], command_ordinals: [0], reads, patch: command.args.changes });
  expect(Object.keys(body.steps[0]).sort()).toEqual(['command_ordinals', 'id', 'intent', 'label', 'patch', 'reads', 'tags']);
  return command;
}

export function assertCatalogDocumentPatch(post: DocumentPatchPost, before: HeadPin, original: CanonicalDocument, selectedId: string): void {
  expect(post.body.project_id).toBe(original.project_id);
  expect(post.body.timeline_id).toBe(original.timeline_id);
  const reads = documentReads(original, 'catalog', selectedId);
  const command = assertRequestEnvelope(post, before, reads, 'Edit timeline', 'timeline.apply_element');
  expect(command.created).toEqual(expect.arrayContaining([expect.stringMatching(/^parent\/clip:.+$/)]));
  expect(command.created).toHaveLength(1);
  const changes = command.args.changes;
  expect(changes).toHaveLength(1);
  const insert = object(changes[0], 'catalog list insert');
  const { path, rows } = sourceClips(original);
  const order = rows.map((row) => String(row.id));
  expect(insert).toMatchObject({ op: 'list.insert', ref: 'parent', path: ['clips'], before: { state: 'absent' }, order_before: order, after_id: order.at(-1) });
  expect(insert.id).toEqual(expect.any(String));
  expect(insert.value).toEqual(expect.objectContaining({ id: insert.id, elementRef: { id: 'am-burst', kind: 'effect', packId: 'astrid_motion' } }));
  expect(command.created).toEqual([`parent/clip:${String(insert.id)}`]);
  expect((bodyStep(post).patch as unknown[])).toEqual(changes);
}

export function assertParamsDocumentPatch(post: DocumentPatchPost, before: HeadPin, original: CanonicalDocument, selectedId: string): void {
  expect(post.body.project_id).toBe(original.project_id);
  expect(post.body.timeline_id).toBe(original.timeline_id);
  const reads = documentReads(original, 'params', selectedId);
  const command = assertRequestEnvelope(post, before, reads, 'Edit timeline', 'timeline.update_element');
  expect(command.created).toEqual([]);
  const changes = command.args.changes;
  expect(changes).toHaveLength(1);
  expect(changes[0]).toEqual({ op: 'set', ref: 'parent', path: ['clips', `id:${selectedId}`, 'params', 'bob'], before: { state: 'absent' }, value: 12 });
  expect(bodyStep(post).patch).toEqual(changes);
}

function bodyStep(post: DocumentPatchPost): JsonObject {
  return object(post.body.steps[0], 'document patch step');
}

export function assertInverseRequestV2(post: DocumentPatchPost, before: HeadPin, targetPublication: string): void {
  expect(post.key).toMatch(/\S/);
  const body = post.body;
  expect(Object.keys(body).sort()).toEqual(['api_version', 'base_publication_id', 'base_revision_id', 'commands', 'dry_run', 'label', 'merge', 'project_id', 'source', 'steps', 'timeline_id'].sort());
  expect(body).toMatchObject({
    api_version: 1,
    project_id: expect.any(String),
    timeline_id: expect.any(String),
    base_revision_id: before.revision_id,
    base_publication_id: before.publication_id,
    label: 'Undo timeline',
    merge: 'fields',
    dry_run: false,
    source: { via: 'app' },
  });
  expect(Object.hasOwn(body, 'reads')).toBe(false);
  expect(body.commands).toEqual([{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: [targetPublication] } }]);
  expect(body.steps).toHaveLength(1);
  expect(body.steps[0]).toMatchObject({ label: 'Undo timeline', intent: 'Undo timeline', tags: [], command_ordinals: [0], patch: [] });
  expect(Object.hasOwn(body.steps[0], 'reads')).toBe(false);
}
