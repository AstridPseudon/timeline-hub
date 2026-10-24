import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {readFileSync} from 'node:fs';

const baseCommit = 'f6a21c285267d6475816adbda74233907ac93911';
const sourcePath = 'tests/e2e/local/three-products.spec.ts';
const patchPath = new URL('./proposal.patch', import.meta.url);
const base = execFileSync('git', ['show', `${baseCommit}:${sourcePath}`], {encoding: 'utf8'});
const patch = readFileSync(patchPath, 'utf8').split('\n');
const helperStart = patch.findIndex((line) => line.startsWith('+function expectRecordedDocumentPatchCommand'));
const helperEnd = patch.findIndex((line, index) => index > helperStart && line === '+}');
assert(helperStart >= 0 && helperEnd >= 0, 'helper not found in exact patch');
const helper = patch.slice(helperStart, helperEnd + 1).map((line) => line.slice(1)).join('\n') + '\n\n';
const marker = 'async function expectV2History';
const oldPredicate = '  expect(recordedB?.commands[0].command).toEqual(requestB.commands[0]);';
const newPredicate = '  expectRecordedDocumentPatchCommand(recordedB?.commands[0].command, requestB.commands[0], seed3.appClipId);';
const insertAt = base.indexOf(marker);
const lastPredicate = base.lastIndexOf(oldPredicate);
assert.notEqual(insertAt, -1, 'helper insertion marker not found');
assert.notEqual(lastPredicate, -1, 'merged B predicate not found');
const withHelper = base.slice(0, insertAt) + helper + base.slice(insertAt);
const predicateAt = withHelper.lastIndexOf(oldPredicate);
const virtual = withHelper.slice(0, predicateAt) + newPredicate + withHelper.slice(predicateAt + oldPredicate.length);
const sha256 = (value) => createHash('sha256').update(value).digest('hex');
const lines = (value) => value.split('\n');
const sliceHash = (value, start, end, terminalNewline) => {
  const region = lines(value).slice(start - 1, end).join('\n');
  return sha256(region + (terminalNewline ? '\n' : ''));
};

const actual = {
  base: sha256(base),
  patch: sha256(readFileSync(patchPath)),
  virtual: sha256(virtual),
  helper: sliceHash(virtual, 957, 977, true),
  mergedBBefore: sliceHash(base, 1819, 1822, false),
  mergedBAfter: sliceHash(virtual, 1840, 1843, false),
  mapping: {helper: [957, 977], mergedBBefore: 1820, mergedBAfter: 1841},
};

const expected = {
  base: '736fd38108283b9c8b5faac47adff4a9c1abd087cb326184a6bfec480e491e05',
  patch: '80127a0bc4174b8a5b25d9bc34a52d01c712f76a32a1076245ad9547c0846733',
  virtual: '93c2bf4c72ac3c91442a1a52174e36311113751ab9d8b7e0f52e4a958559a64b',
  helper: '312ded75179f64711c83ee2b9e2e764283eab7905ec5602437733cefe18390c2',
  mergedBBefore: '67e2292e268a86cfc51c045cfdddfdf8951846821d20c32bf0604eec892434b6',
  mergedBAfter: 'f0c857e32eeca8fcdc8362c3adf6382dc9d2bf7e9d4be8c7504921a73a1e54f5',
};
assert.deepStrictEqual(actual, {...expected, mapping: actual.mapping});
console.log(JSON.stringify(actual, null, 2));
