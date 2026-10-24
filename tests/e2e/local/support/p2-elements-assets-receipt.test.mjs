// Pure controls for the actual mounted elements/assets receipt helpers; no browser or Runtime execution.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { compileFunction } from 'node:vm';
import { expect } from '@playwright/test';
import ts from 'typescript';

const source = readFileSync(new URL('../three-products.p2-elements-assets.spec.ts', import.meta.url), 'utf8');
const extract = (name) => {
  const match = source.match(new RegExp(`^function ${name}\\([^]*?^}`, 'm'));
  assert.ok(match, `exercise the actual ${name} helper`);
  return match[0];
};
const helperSource = [
  extract('object'),
  extract('acceptedMutation'),
  extract('publicationId'),
  extract('assertAcceptedReply'),
  extract('assertHistoryEntry'),
  extract('assertUndoHistoryEntry'),
].join('\n');
const helpers = compileFunction(`${ts.transpileModule(helperSource, {}).outputText}\nreturn { assertAcceptedReply, assertHistoryEntry, assertUndoHistoryEntry };`, ['expect'])(expect);

const command = {
  schema_version: 1,
  op: 'doc.patch',
  version: '1',
  select: null,
  args: { changes: [{ op: 'set', ref: 'parent', path: ['clips', 'id:clip-1', 'at'], before: { state: 'present', value: 0 }, value: 5 }] },
};
const step = { id: 'step-1', label: 'Edit timeline', intent: 'Edit timeline', tags: [], command_ordinals: [0], patch: command.args.changes };

function acceptedPost({ requestKey = 'request-1', publication = 'publication-1', revision = 'revision-1', baseRevision = 'revision-0', basePublication = 'publication-0', inverse = false } = {}) {
  const acceptedCommand = inverse ? { schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: ['publication-1'] } } : command;
  const acceptedStep = inverse ? { ...step, patch: [] } : step;
  const data = {
    status: 'accepted',
    base_revision_id: baseRevision,
    base_publication_id: basePublication,
    previous_revision_id: baseRevision,
    previous_publication_id: basePublication,
    accepted_revision_id: revision,
    rebased_onto: null,
    canonical_document: {},
    document_digest: 'digest',
    commands: [acceptedCommand],
    id_map: {},
    provider_version: 'provider',
    compiler_version: 'compiler',
    merge_mode: 'atomic',
    steps: [acceptedStep],
    publisher: 'publisher',
    source: { via: 'app' },
    label: 'Edit timeline',
  };
  const receipt = {
    receipt_id: publication,
    command_kind: 'commit',
    idempotency_key: requestKey,
    request_hash: 'hash',
    project_id: 'project',
    project_seq: [1, 1],
    event_ids: ['event'],
    result: data,
    created_at: '2026-10-24T00:00:00Z',
  };
  const body = {
    api_version: 1, project_id: 'project', timeline_id: 'timeline',
    base_revision_id: baseRevision, base_publication_id: basePublication,
    commands: [acceptedCommand], label: 'Edit timeline', steps: [acceptedStep],
    merge: 'atomic', dry_run: false, source: { via: 'app' },
  };
  return { request: {}, response: { status: () => 200 }, body, json: { data, receipt }, key: requestKey };
}

function historyFor(post, { publication = post.json.receipt.receipt_id, receipt = post.json.receipt, revision = post.json.data.accepted_revision_id, undoOf = undefined, undoSteps = [] } = {}) {
  return {
    head: { revision_id: revision, publication_id: publication },
    next_cursor: null,
    items: [{
      publication_id: publication,
      revision_id: revision,
      previous: null,
      receipt,
      intent: 'recorded',
      records: {
        commands: [{ command: post.json.data.commands[0], writes: ['parent'], reads: ['parent'], bindings: ['parent'], dependencies: ['parent'], derived_writes: [] }],
        steps: [{ patch: [{ op: 'set' }], dependencies: ['parent'] }],
        undo_steps: undoSteps,
        ...(undoOf ? { undo_of: undoOf } : {}),
      },
      provider_version: 'provider', compiler_version: 'compiler', merge_mode: 'atomic',
      steps: post.json.data.steps, publisher: 'publisher', source: { via: 'app' }, label: 'Edit timeline',
    }],
  };
}

test('actual accepted helper preserves distinct publication and idempotency identities', () => {
  const post = acceptedPost();
  assert.doesNotThrow(() => helpers.assertAcceptedReply(post, { revision_id: 'revision-0', publication_id: 'publication-0' }));
  assert.throws(() => helpers.assertAcceptedReply({ ...post, json: { ...post.json, receipt: { ...post.json.receipt, receipt_id: post.key } } }, { revision_id: 'revision-0', publication_id: 'publication-0' }));
  assert.throws(() => helpers.assertAcceptedReply({ ...post, json: { ...post.json, receipt: { ...post.json.receipt, idempotency_key: 'wrong-request' } } }, { revision_id: 'revision-0', publication_id: 'publication-0' }));
});

test('actual history helper joins by authoritative publication and guards the head', () => {
  const post = acceptedPost();
  const result = post.json;
  assert.doesNotThrow(() => helpers.assertHistoryEntry(historyFor(post), post, result));
  assert.throws(() => helpers.assertHistoryEntry(historyFor(post, { publication: post.key }), post, result));
  assert.throws(() => helpers.assertHistoryEntry({ ...historyFor(post), head: { revision_id: 'revision-1', publication_id: post.key } }, post, result));
  assert.throws(() => helpers.assertHistoryEntry(historyFor(post, { receipt: { ...post.json.receipt, receipt_id: 'wrong-receipt' } }), post, result));
});

test('actual undo history helper joins both inverse and target by receipt publication', () => {
  const target = acceptedPost();
  const undo = acceptedPost({ requestKey: 'request-2', publication: 'publication-2', revision: 'revision-2', baseRevision: 'revision-1', basePublication: 'publication-1', inverse: true });
  const page = historyFor(undo, { undoOf: ['publication-1'], undoSteps: null });
  assert.doesNotThrow(() => helpers.assertUndoHistoryEntry(page, undo, target));
  assert.throws(() => helpers.assertUndoHistoryEntry(historyFor(undo, { publication: undo.key, undoOf: ['publication-1'], undoSteps: null }), undo, target));
  assert.throws(() => helpers.assertUndoHistoryEntry(historyFor(undo, { undoOf: [target.key], undoSteps: null }), undo, target));
  assert.throws(() => helpers.assertUndoHistoryEntry(historyFor(undo, { undoOf: ['publication-1'] }), undo, target));
});
