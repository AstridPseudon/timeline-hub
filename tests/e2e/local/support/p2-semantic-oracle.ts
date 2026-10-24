import { expect } from '@playwright/test';
import type { CanonicalDocument, CommitRequest, HeadPin } from '../../../../src/integrations/runtime/timeline-commit-types.ts';

type JsonObject = Record<string, unknown>;

export type SemanticAddMediaOracle = {
  op: 'clip.add-media' | 'occurrence.add-media';
  owner: string;
  select: string;
};

export type SemanticCommitPost = {
  key: string;
  body: CommitRequest;
};

function object(value: unknown, label: string): JsonObject {
  expect(value, label).toBeTruthy();
  expect(typeof value, label).toBe('object');
  expect(Array.isArray(value), label).toBe(false);
  return value as JsonObject;
}

function assetIds(container: unknown): Set<string> {
  if (container === undefined || container === null) return new Set();
  const registry = object(container, 'authored registry container').registry;
  if (registry === undefined) return new Set();
  const assets = object(registry, 'authored registry').assets;
  if (assets === undefined) return new Set();
  return new Set(Object.keys(object(assets, 'authored assets')));
}

function authoredAssetIds(before: CanonicalDocument, owner: string): Set<string> {
  const parent = before.parent_revision.payload as unknown as JsonObject;
  if (owner === 'parent') {
    const ids = assetIds(parent);
    const config = parent.config;
    for (const id of assetIds(config)) ids.add(id);
    return ids;
  }

  expect(owner).toMatch(/^occurrence:[^/]+$/);
  const occurrenceId = owner.slice('occurrence:'.length);
  const occurrences = parent.occurrences;
  expect(Array.isArray(occurrences), 'authored occurrences').toBe(true);
  const occurrence = (occurrences as Array<JsonObject>).find((row) => row.occurrence_id === occurrenceId);
  expect(occurrence, `authored occurrence ${occurrenceId}`).toBeTruthy();
  const shot = before.shot_revisions.find((candidate) => candidate.shot_id === occurrence!.shot_id
    && candidate.revision_id === occurrence!.shot_revision_id);
  expect(shot, `authored shot for ${owner}`).toBeTruthy();
  const internal = before.internal_timeline_revisions.find((candidate) => candidate.revision_id === shot!.internal_timeline_revision_id);
  expect(internal, `authored internal timeline for ${owner}`).toBeTruthy();
  return assetIds(internal!.payload);
}

/** Strict request oracle for the two semantic media-birth routes. */
export function assertSemanticAddMediaRequest(
  post: SemanticCommitPost,
  before: HeadPin,
  authored: CanonicalDocument,
  expected: SemanticAddMediaOracle,
): void {
  expect(post.key).toMatch(/\S/);
  const body = post.body;
  expect(body.api_version).toBe(1);
  expect(body.base_revision_id).toBe(before.revision_id);
  expect(body.base_publication_id).toBe(before.publication_id);
  expect(body.project_id).toEqual(expect.any(String));
  expect(body.timeline_id).toEqual(expect.any(String));
  expect(body.label).toEqual(expect.any(String));
  expect(body.dry_run).toBe(false);
  expect(body.source).toEqual({ via: 'app' });
  for (const key of ['rationale', 'group_id'] as const) {
    if (Object.hasOwn(body, key)) expect(body[key]).toEqual(expect.any(String));
  }
  expect(body.merge).toBe('fields');
  expect(Object.hasOwn(body, 'reads')).toBe(false);
  expect(body.commands).toHaveLength(1);
  expect(body.steps).toHaveLength(1);

  const command = body.commands[0]!;
  expect(Object.keys(command).filter((key) => ![
    'schema_version', 'op', 'version', 'select', 'args', 'intent', 'resolved', 'expect', 'authorship',
    'reads', 'selections', 'bindings', 'created', 'rationale', 'group_id',
  ].includes(key))).toEqual([]);
  expect(command.schema_version).toBe(1);
  expect(command.op).toBe(expected.op);
  expect(command.version).toBe('1');
  expect(command.select).toBe(expected.select);
  expect(command.intent).toEqual(expected.op === 'clip.add-media' ? {} : { ownership: 'occurrence' });
  const args = object(command.args, `${expected.op} args`);
  expect(Object.keys(args).sort()).toEqual(['media', 'row']);
  const row = object(args.row, `${expected.op} row`);
  expect(row.id).toEqual(expect.any(String));
  expect(row.asset).toEqual(expect.any(String));
  expect(args.media).toEqual(expect.any(Object));

  const created = authoredAssetIds(authored, expected.owner).has(row.asset as string)
    ? [`${expected.owner}/clip:${row.id}`]
    : [`${expected.owner}/asset:${row.asset}`, `${expected.owner}/clip:${row.id}`];
  expect(command.created).toEqual(created);

  const step = body.steps[0]!;
  expect(Object.keys(step).sort()).toEqual(['command_ordinals', 'id', 'intent', 'label', 'patch', 'tags']);
  expect(step.id).toEqual(expect.any(String));
  expect(step.label).toBe(body.label);
  expect(step.intent).toBe(body.label);
  expect(step.tags).toEqual([]);
  expect(step.command_ordinals).toEqual([0]);
  expect(step.patch).toEqual([]);
}
