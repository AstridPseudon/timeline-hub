// @vitest-environment node
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import type { OutboxJson } from './commitOutbox.ts';
import { documentPatchIntent } from './documentPatchIntent.ts';
import trimFixture from './fixtures/recipe_m2_clip_trim.json';
import corpus from '../../../../tests/fixtures/p1-feasibility/cases.json';

type Intent = Parameters<typeof documentPatchIntent>[0];
type JsonObject = { [key: string]: OutboxJson };
type Fixture = { input: CanonicalDocument; output: CanonicalDocument };

const appRoot = resolve(import.meta.dirname, '../../../../');
const agentRoot = resolve('/home/user/work/agent');
const copy = <T>(value: T): T => structuredClone(value);
const present = (value: OutboxJson) => ({ state: 'present', value });

function parentPayload(document: CanonicalDocument): JsonObject {
  return document.parent_revision.payload as JsonObject;
}

function clip(document: CanonicalDocument, id: string): JsonObject {
  const clips = parentPayload(document).clips as JsonObject[];
  const result = clips.find((candidate) => candidate.id === id);
  if (!result) throw new Error(`Missing clip ${id}`);
  return result;
}

function parentRoot(document: CanonicalDocument) {
  return {
    ref: 'parent' as const,
    revisionId: document.parent_revision.revision_id,
    contentDigest: document.parent_revision.content_digest,
  };
}

function intent(before: CanonicalDocument, after: CanonicalDocument, label: string): Intent {
  return {
    before,
    after,
    roots: [parentRoot(before)],
    basis: { head: { revisionId: before.parent_revision.revision_id, publicationId: 'fixture-publication' } },
    label,
    step: { id: 'fixture-edit', label, intent: 'P1 real corpus edit', tags: ['p1', 'corpus'] },
  };
}

/**
 * The fixture output is an authored payload after execution. Its generated
 * revision/digest wrappers are not an App-authored edit target, so retain the
 * input wrappers while using the exact fixture payload as the after document.
 */
function authoredPayloadAfter(before: CanonicalDocument, authoredOutput: CanonicalDocument): CanonicalDocument {
  const after = copy(before);
  after.parent_revision.payload = copy(authoredOutput.parent_revision.payload);
  return after;
}

function readAgentSplit(): Fixture {
  const path = resolve(agentRoot, 'tests/editing_conformance/fixtures/recipe_m2_clip_split.json');
  const bytes = readFileSync(path);
  const source = corpus.cases.find((entry) => entry.id === 'agent-split-created-id')!.source;
  expect(createHash('sha256').update(bytes).digest('hex')).toBe(source.sha256);
  return JSON.parse(bytes.toString()) as Fixture;
}

describe('P1 real corpus document patch encoder', () => {
  it('encodes the real App trim output with complete guards, roots, mirrors, and clears', () => {
    const before = trimFixture.input as CanonicalDocument;
    const after = authoredPayloadAfter(before, trimFixture.output as CanonicalDocument);
    const proposal = documentPatchIntent(intent(before, after, 'Real App trim')) as JsonObject;
    const beforeClip = clip(before, 'clip-a');

    expect(proposal).toMatchObject({
      kind: 'document-patch-intent',
      basis: { head: { revisionId: 'parent-1', publicationId: 'fixture-publication' } },
      roots: [parentRoot(before)],
      created: [],
    });
    expect(proposal.changes).toEqual([
      { op: 'set', ref: 'parent', path: ['clips', 'id:clip-a', 'hold'], before: present(beforeClip.hold), value: 4 },
      { op: 'remove', ref: 'parent', path: ['clips', 'id:clip-a', 'app', 'astrid', 'for'], before: present(19) },
      { op: 'remove', ref: 'parent', path: ['clips', 'id:clip-a', 'app', 'astrid', 'until'], before: present(null) },
      { op: 'set', ref: 'parent', path: ['clips', 'id:clip-a', 'from'], before: present(2), value: 1 },
      { op: 'set', ref: 'parent', path: ['clips', 'id:clip-a', 'to'], before: present(6), value: 5 },
    ]);
    expect((parentPayload(after).config as JsonObject).clips).toEqual(parentPayload(after).clips);
    expect(parentPayload(after).registry).toEqual(parentPayload(before).registry);
    expect(parentPayload(after).clips).toEqual(parentPayload(after).config!.clips);
    expect((proposal.after as JsonObject).parent_revision).toEqual(after.parent_revision);
  });

  it('encodes the authored split allocation and reports the missing App dependent trim seam', () => {
    const split = readAgentSplit();
    const before = split.input;
    const after = authoredPayloadAfter(before, split.output);
    const proposal = documentPatchIntent(intent(before, after, 'Real Agent split')) as JsonObject;
    const inserted = (proposal.changes as JsonObject[]).find((change) => change.op === 'list.insert');

    expect(inserted).toMatchObject({
      op: 'list.insert', ref: 'parent', path: ['clips'], id: 'right', before: { state: 'absent' },
      order_before: ['clip-a', 'clip-b'], after_id: 'clip-a',
    });
    expect(proposal.created).toEqual(['parent/clip:right']);
    expect((inserted!.value as JsonObject).id).toBe('right');
    expect((proposal.changes as JsonObject[]).some((change) => change.path?.join('.') === 'id:right.from')).toBe(false);
    expect(corpus.h3_chain.status).toBe('authored-not-go');
    expect(corpus.h3_chain.required_seams).toContain('App split capture/submit port for clip.split and created-id binding');
    expect(corpus.h3_chain.required_seams).toContain('App mixed-command queue acceptance of clip.trim against a newly created id');
  });
});
