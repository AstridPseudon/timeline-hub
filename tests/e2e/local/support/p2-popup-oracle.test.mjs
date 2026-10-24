// Pure controls for the mounted P2 popup receipt/publication assertions.
// Compile the helpers from the production proof so these controls cannot drift
// into a parallel, weaker oracle.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { compileFunction } from 'node:vm';
import { expect } from '@playwright/test';
import ts from 'typescript';

const source = readFileSync(new URL('../three-products.p2-popup.spec.ts', import.meta.url), 'utf8');
const publicationHelper = source.match(/^function authoritativePublicationId\([^]*?^}/m)?.[0];
const historyHelper = source.match(/^function assertAuthoritativeHistoryPublication\([^]*?^}/m)?.[0];
const headHelper = source.match(/^function assertAuthoritativeHead\([^]*?^}/m)?.[0];
const inverseHelper = source.match(/^function assertInverseTargetsPublication\([^]*?^}/m)?.[0];
const undoHelper = source.match(/^function assertUndoHistoryPublication\([^]*?^}/m)?.[0];
assert.ok(publicationHelper, 'exercise the actual popup reply helper');
assert.ok(historyHelper && headHelper && inverseHelper && undoHelper, 'exercise actual popup publication helpers');
const compile = (body, returnName, names, values) => compileFunction(
  `${ts.transpileModule(body, {}).outputText}\nreturn ${returnName};`, names,
)(...values);
const publicationId = compile(publicationHelper, 'authoritativePublicationId', ['expect'], [expect]);
const checkBindings = compile(
  [historyHelper, headHelper, inverseHelper, undoHelper]
    .map((helper) => ts.transpileModule(helper, {}).outputText).join('\n'),
  '{ assertAuthoritativeHistoryPublication, assertAuthoritativeHead, assertInverseTargetsPublication, assertUndoHistoryPublication }',
  ['expect'], [expect],
);

function replyFixture() {
  const key = '0f3c4b3a-2e1d-4c5b-8a79-0123456789ab';
  const receiptId = 'txn-0123456789abcdef0123456789abcdef';
  const data = { accepted_revision_id: 'revision-next' };
  const receipt = { receipt_id: receiptId, idempotency_key: key };
  const post = {
    key,
    body: { project_id: 'project', timeline_id: 'timeline', commands: [{
      schema_version: 1, op: 'timeline.inverse', version: '1', select: null,
      args: { publications: [receiptId] },
    }] },
  };
  const result = { data, receipt };
  return {
    post, result,
    entry: { publication_id: receiptId, records: { undo_of: [receiptId] } },
    head: { revision_id: data.accepted_revision_id, publication_id: receiptId },
  };
}

test('actual popup helpers accept distinct UUID request and txn receipt identities', () => {
  const { post, result, entry, head } = replyFixture();
  assert.equal(publicationId(post, result), result.receipt.receipt_id);
  checkBindings.assertAuthoritativeHistoryPublication(entry, result);
  checkBindings.assertAuthoritativeHead(head, result);
  checkBindings.assertInverseTargetsPublication(post, result.receipt.receipt_id);
  checkBindings.assertUndoHistoryPublication(entry, result.receipt.receipt_id);
});

test('actual popup helpers refuse wrong receipt, key, head, history, inverse, and undo identities', () => {
  const { post, result, entry, head } = replyFixture();
  const wrong = [
    () => publicationId(post, { ...result, receipt: { ...result.receipt, receipt_id: post.key } }),
    () => publicationId(post, { ...result, receipt: { ...result.receipt, idempotency_key: 'other-request-key' } }),
    () => checkBindings.assertAuthoritativeHead({ ...head, publication_id: 'wrong-publication' }, result),
    () => checkBindings.assertAuthoritativeHistoryPublication({ ...entry, publication_id: 'wrong-publication' }, result),
    () => checkBindings.assertInverseTargetsPublication({ ...post, body: { ...post.body, commands: [{
      ...post.body.commands[0], args: { publications: ['wrong-publication'] },
    }] } }, result.receipt.receipt_id),
    () => checkBindings.assertUndoHistoryPublication({ records: { undo_of: ['wrong-publication'] } }, result.receipt.receipt_id),
  ];
  for (const checkWrong of wrong) assert.throws(checkWrong);
});
