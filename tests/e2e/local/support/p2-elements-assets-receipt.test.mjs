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
const requestHelper = extract('assertRequestV2');
const helperSource = [
  extract('object'),
  extract('exactKeys'),
  extract('assertAgentState'),
  extract('assertCommitRead'),
  extract('assertPatchChange'),
  extract('assertNativeCommandShape'),
  extract('assertNativeBinding'),
  extract('assertNativeStepShape'),
  extract('assertNativeRecorder'),
  requestHelper,
  extract('acceptedMutation'),
  extract('publicationId'),
  extract('assertNativeAcceptedReply'),
  extract('assertNativeHistoryEntry'),
  extract('assertAcceptedReply'),
  extract('assertHistoryEntry'),
  extract('assertUndoHistoryEntry'),
].join('\n');
const helpers = compileFunction(`${ts.transpileModule(helperSource, {}).outputText}\nreturn { assertAcceptedReply, assertHistoryEntry, assertUndoHistoryEntry };`, ['expect'])(expect);
const checkRequest = compileFunction(`${ts.transpileModule([extract('object'), requestHelper].join('\n'), {}).outputText}\nreturn assertRequestV2;`, ['expect'])(expect);

const command = {
  schema_version: 1,
  op: 'doc.patch',
  version: '1',
  select: null,
  args: { changes: [{ op: 'set', ref: 'parent', path: ['clips', 'id:clip-1', 'at'], before: { state: 'present', value: 0 }, value: 5 }] },
};
const step = { id: 'step-1', label: 'Edit timeline', intent: 'Edit timeline', tags: [], command_ordinals: [0], patch: command.args.changes };
const requestId1 = '6d8f4e2a-7c41-4b9e-8d03-5a6f1c2e7b90';
const requestId2 = 'b1c2d3e4-f567-4890-ab12-cd34ef567890';
const receiptId1 = 'txn-9a7b6c5d4e3f2a10b9c8d7e6f5a40321';
const receiptId2 = 'txn-1234567890abcdef1234567890abcdef';
const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const receiptPattern = /^txn-[0-9a-f]{32}$/i;

function acceptedPost({ requestKey = requestId1, publication = receiptId1, revision = 'revision-1', baseRevision = 'revision-0', basePublication = 'publication-0', inverse = false } = {}) {
  const inverseState = { state: 'present', value: [] };
  const acceptedCommand = inverse ? {
    schema_version: 1, op: 'timeline.inverse', version: '1', select: null,
    args: { publications: [basePublication] }, intent: {}, resolved: [],
    expect: { 'parent::config.clips': inverseState },
    authorship: { 'parent::config.clips': 'direct' },
    reads: [{ kind: 'field', ref: 'parent', path: ['config', 'clips'], state: inverseState }], selections: [], bindings: {}, created: [],
  } : command;
  const acceptedStep = inverse ? {
    ...step,
    patch: [{ op: 'set', ref: 'parent', path: ['config', 'clips'], before: inverseState, value: [] }],
    dependencies: [{ kind: 'field', ref: 'parent', path: ['config', 'clips'], state: inverseState }],
  } : step;
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
    merge_mode: inverse ? 'fields' : 'atomic',
    steps: [acceptedStep],
    publisher: 'publisher',
    source: { via: 'app' },
    label: inverse ? 'Undo timeline' : 'Edit timeline',
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
    commands: [acceptedCommand], label: inverse ? 'Undo timeline' : 'Edit timeline', steps: [acceptedStep],
    merge: inverse ? 'fields' : 'atomic', ...(inverse ? { reads: [] } : {}), dry_run: false, source: { via: 'app' },
  };
  return { request: {}, response: { status: () => 200 }, body, json: { data, receipt }, key: requestKey };
}

function historyFor(post, { publication = post.json.receipt.receipt_id, receipt = post.json.receipt, revision = post.json.data.accepted_revision_id, undoOf = undefined, undoSteps = [] } = {}) {
  const native = post.body.commands[0].op === 'timeline.inverse';
  const nativeRecord = native ? {
    ordinal: 0,
    command: post.json.data.commands[0],
    writes: [{ ref: 'parent', path: ['config', 'clips'], before: { state: 'present', value: [] }, after: { state: 'present', value: [] } }],
    reads: post.json.data.commands[0].reads,
    selections: post.json.data.commands[0].selections,
    bindings: [{ key: 'inverse.stage', ref: 'parent', policy: 'fixed', dependencies: [], boundary: {
      publication_id: post.body.base_publication_id, step_id: post.json.data.steps[0].id,
      command_ordinals: [0], native_write_range: [0, 1], effect_range: [0, 1],
    } }],
    created: [], dependencies: [],
    derived_writes: [{ ref: 'parent', path: ['config', 'clips'], before: { state: 'present', value: [] }, after: { state: 'present', value: [] }, cause: 0 }],
  } : null;
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
        commands: [nativeRecord ?? { ordinal: 0, command: post.json.data.commands[0], writes: ['parent'], reads: ['parent'], bindings: ['parent'], dependencies: [], derived_writes: [] }],
        steps: post.body.commands[0].op === 'timeline.inverse'
          ? post.json.data.steps
          : [{ patch: [{ op: 'set' }], dependencies: ['parent'] }],
        ...(post.body.commands[0].op === 'timeline.inverse' ? { label: post.json.data.label, merge_mode: post.json.data.merge_mode } : {}),
        undo_steps: undoSteps,
        undo_of: undoOf ?? [],
      },
      previous: { revision_id: post.json.data.previous_revision_id, publication_id: post.json.data.previous_publication_id },
      provider_version: 'provider', compiler_version: 'compiler', merge: post.json.data.merge_mode, merge_mode: post.json.data.merge_mode,
      steps: post.json.data.steps, publisher: 'publisher', source: { via: 'app' }, label: post.json.data.label,
      ...(post.body.reads ? { reads: post.body.reads } : {}),
    }],
  };
}

test('actual accepted helper preserves distinct publication and idempotency identities', () => {
  const post = acceptedPost();
  assert.match(post.key, uuidPattern);
  assert.match(post.json.receipt.receipt_id, receiptPattern);
  assert.notEqual(post.key, post.json.receipt.receipt_id);
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
  const targetPublication = target.json.receipt.receipt_id;
  const undo = acceptedPost({ requestKey: requestId2, publication: receiptId2, revision: 'revision-2', baseRevision: 'revision-1', basePublication: targetPublication, inverse: true });
  const page = historyFor(undo, { undoOf: [targetPublication], undoSteps: null });
  assert.doesNotThrow(() => helpers.assertUndoHistoryEntry(page, undo, target));
  assert.throws(() => helpers.assertUndoHistoryEntry(historyFor(undo, { publication: undo.key, undoOf: [targetPublication], undoSteps: null }), undo, target));
  assert.throws(() => helpers.assertUndoHistoryEntry(historyFor(undo, { undoOf: [target.key], undoSteps: null }), undo, target));
  assert.throws(() => helpers.assertUndoHistoryEntry(historyFor(undo, { undoOf: [targetPublication] }), undo, target));
});

test('actual mounted asset helper accepts the exact native inverse envelope and rejects policy drift', () => {
  const post = {
    key: requestId2,
    body: {
      api_version: 1, project_id: 'project', timeline_id: 'timeline',
      base_revision_id: 'revision-1', base_publication_id: receiptId1,
      commands: [{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: [receiptId1] } }],
      label: 'Undo timeline',
      steps: [{ id: '6d8f4e2a-7c41-4b9e-8d03-5a6f1c2e7b90', label: 'Undo timeline', intent: 'Undo timeline', tags: [], command_ordinals: [0], patch: [] }],
      merge: 'fields', reads: [], dry_run: false, source: { via: 'app' },
    },
  };
  assert.doesNotThrow(() => checkRequest(post, { revision_id: 'revision-1', publication_id: receiptId1 }, { project_id: 'project', timeline_id: 'timeline' }));
  const variants = [
    (candidate) => { candidate.body.project_id = 'wrong-project'; },
    (candidate) => { candidate.body.timeline_id = 'wrong-timeline'; },
    (candidate) => { candidate.body.merge = 'atomic'; },
    (candidate) => { delete candidate.body.reads; },
    (candidate) => { candidate.body.reads = [{ kind: 'scope', ref: 'timeline', path: [] }]; },
    (candidate) => { candidate.body.commands[0].args.publications[0] = 'wrong-publication'; },
    (candidate) => { candidate.body.commands[0].extra = true; },
    (candidate) => { candidate.body.commands[0].select = {}; },
    (candidate) => { candidate.body.steps[0].patch = [{ op: 'set' }]; },
    (candidate) => { candidate.body.steps[0].reads = []; },
    (candidate) => { candidate.body.steps[0].label = 'Edit timeline'; },
    (candidate) => { candidate.body.base_revision_id = 'wrong-revision'; },
    (candidate) => { candidate.body.base_publication_id = 'wrong-publication'; },
    (candidate) => { candidate.body.extra = true; },
  ];
  for (const mutate of variants) {
    const candidate = structuredClone(post);
    mutate(candidate);
    assert.throws(() => checkRequest(candidate, { revision_id: 'revision-1', publication_id: receiptId1 }, { project_id: 'project', timeline_id: 'timeline' }));
  }
});

test('actual native authoritative reply and recorder reject metadata drift', () => {
  const post = acceptedPost({ inverse: true, requestKey: requestId2, publication: receiptId2, baseRevision: 'revision-1', basePublication: receiptId1 });
  assert.doesNotThrow(() => helpers.assertAcceptedReply(post, { revision_id: 'revision-1', publication_id: receiptId1 }));
  const replyVariants = [
    (candidate) => { delete candidate.json.data.commands[0].reads[0].ref; },
    (candidate) => { delete candidate.json.data.commands[0].expect['parent::config.clips']; },
    (candidate) => { candidate.json.data.commands[0].authorship.extra = 'direct'; },
    (candidate) => { candidate.json.data.commands[0].bindings.extra = 'parent'; },
    (candidate) => { candidate.json.data.commands[0].resolved = ['parent']; },
    (candidate) => { candidate.json.data.commands[0].created = ['parent/clip:new']; },
    (candidate) => { delete candidate.json.data.steps[0].patch[0].ref; },
    (candidate) => { candidate.json.data.steps[0].dependencies = []; },
    (candidate) => { delete candidate.json.data.commands[0].authorship; },
    (candidate) => { delete candidate.json.data.steps[0].dependencies; },
  ];
  for (const [index, mutate] of replyVariants.entries()) {
    const candidate = { ...post, body: structuredClone(post.body), json: structuredClone(post.json) };
    mutate(candidate);
    assert.throws(() => helpers.assertAcceptedReply(candidate, { revision_id: 'revision-1', publication_id: receiptId1 }), undefined, `reply variant ${index}`);
  }

  const page = historyFor(post, { undoSteps: null });
  assert.doesNotThrow(() => helpers.assertHistoryEntry(page, post, post.json));
  const historyVariants = [
    (candidate) => { candidate.items[0].records.commands[0].reads[0].path = ['wrong']; },
    (candidate) => { candidate.items[0].records.commands[0].writes = []; },
    (candidate) => { candidate.items[0].records.commands[0].bindings = []; },
    (candidate) => { candidate.items[0].records.commands[0].dependencies = [{ kind: 'scope', ref: 'parent', path: [] }]; },
    (candidate) => { candidate.items[0].records.commands[0].derived_writes = []; },
    (candidate) => { candidate.items[0].records.commands[0].bindings = null; },
    (candidate) => { candidate.items[0].records.steps[0].dependencies = []; },
  ];
  for (const [index, mutate] of historyVariants.entries()) {
    const candidate = structuredClone(page);
    mutate(candidate);
    assert.throws(() => helpers.assertHistoryEntry(candidate, post, post.json), undefined, `history variant ${index}`);
  }
});
