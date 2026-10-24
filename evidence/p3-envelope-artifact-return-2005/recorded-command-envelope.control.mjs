import assert from 'node:assert/strict';

const clipId = 'clip-7';
const address = `parent/clip:${clipId}::at`;
const rawKeys = ['args', 'created', 'op', 'schema_version', 'select', 'version'];
const authorityKeys = [
  ...rawKeys.slice(0, 2),
  'expect',
  'intent',
  'op',
  'reads',
  'resolved',
  'schema_version',
  'select',
  'selections',
  'version',
  'authorship',
  'bindings',
].sort();

const submitted = {
  args: {
    changes: [
      {op: 'set', path: [address], previous: 5, value: 7},
      {op: 'set', path: [`parent/clip:${clipId}::label`], previous: 'A', value: 'B'},
    ],
  },
  created: [],
  op: 'doc.patch',
  schema_version: 1,
  select: null,
  version: '1',
};

const expected = {
  ...submitted,
  authorship: {[address]: 'direct'},
  bindings: {},
  expect: {[address]: {state: 'present', value: 5}},
  intent: {},
  reads: [{ref: `parent/clip:${clipId}`, path: ['at'], state: {state: 'present', value: 5}}],
  resolved: [],
  selections: [],
};

const clone = (value) => structuredClone(value);
const keys = (value) => Object.keys(value).sort();

function qualify(recorded, raw) {
  assert.deepStrictEqual(keys(raw), rawKeys);
  assert.deepStrictEqual(keys(recorded), authorityKeys);
  assert.deepStrictEqual(recorded, {
    ...raw,
    authorship: {[address]: 'direct'},
    bindings: {},
    expect: {[address]: {state: 'present', value: 5}},
    intent: {},
    reads: [{ref: `parent/clip:${clipId}`, path: ['at'], state: {state: 'present', value: 5}}],
    resolved: [],
    selections: [],
  });
}

qualify(expected, submitted);

const mutations = new Map();
for (const field of ['args', 'created', 'op', 'schema_version', 'select', 'version']) {
  const raw = clone(submitted);
  if (field === 'args') raw.args.changes[0].value = 8;
  else if (field === 'created') raw.created = ['parent/clip:new'];
  else if (field === 'schema_version') raw.schema_version = 2;
  else if (field === 'select') raw.select = ['parent/clip:new'];
  else raw[field] = field === 'op' ? 'native.move' : '2';
  mutations.set(`raw.${field}`, () => qualify(expected, raw));
}

for (const field of ['authorship', 'bindings', 'expect', 'intent', 'reads', 'resolved', 'selections']) {
  const recorded = clone(expected);
  if (field === 'authorship') recorded.authorship[address] = 'inferred';
  else if (field === 'bindings') recorded.bindings = {binding: 'unexpected'};
  else if (field === 'expect') recorded.expect[address].value = 4;
  else if (field === 'intent') recorded.intent = {kind: 'unexpected'};
  else if (field === 'reads') recorded.reads[0].state.value = 4;
  else if (field === 'resolved') recorded.resolved = ['unexpected'];
  else recorded.selections = ['unexpected'];
  mutations.set(`authority.${field}`, () => qualify(recorded, submitted));
}

const missingRaw = clone(submitted);
delete missingRaw.version;
mutations.set('missing.raw_key', () => qualify(expected, missingRaw));

const missingAuthority = clone(expected);
delete missingAuthority.reads;
mutations.set('missing.authority_key', () => qualify(missingAuthority, submitted));

const extraRaw = clone(submitted);
extraRaw.extra = true;
mutations.set('extra.raw_key', () => qualify(expected, extraRaw));

const extraAuthority = clone(expected);
extraAuthority.extra = true;
mutations.set('extra.authority_key', () => qualify(extraAuthority, submitted));

const wrongBefore = clone(expected);
wrongBefore.expect[address].value = 4;
wrongBefore.reads[0].state.value = 4;
mutations.set('wrong.before', () => qualify(wrongBefore, submitted));

const wrongValue = clone(submitted);
wrongValue.args.changes[0].value = 8;
mutations.set('wrong.value', () => qualify(expected, wrongValue));

const wrongIdentity = clone(expected);
wrongIdentity.authorship['parent/clip:other::at'] = wrongIdentity.authorship[address];
delete wrongIdentity.authorship[address];
wrongIdentity.reads[0].ref = 'parent/clip:other';
mutations.set('wrong.identity', () => qualify(wrongIdentity, submitted));

const wrongOrder = clone(submitted);
wrongOrder.args.changes.reverse();
mutations.set('wrong.order', () => qualify(expected, wrongOrder));

assert.equal(mutations.size, 21);
for (const [label, mutation] of mutations) {
  assert.throws(mutation, undefined, `${label} must be rejected`);
}

console.log(`PASS strict envelope controls: positive + ${mutations.size} independent mutations`);
