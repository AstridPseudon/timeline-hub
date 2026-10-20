import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import ts from '../../node_modules/typescript/lib/typescript.js';

const inputs = JSON.parse(fs.readFileSync(path.join(process.env.AUDIT_NOTES, 'source-inputs.json'), 'utf8'));
const git = (repo, sha, file) => Buffer.from(inputs.blobs[JSON.stringify([repo, sha, file])]);
const app = '/home/user/work/app';
const agent = '/home/user/work/agent';
const runtime = '/home/user/work/runtime';
const base = '7bb885b638838588a0dff81b64b7c34960ac07f3';
const stage = 'f0112b846c1084b0902cdba091442cc840d8e88d';
const fixed = '3a1d9c8524f37a2960d37d1b892d041b4c19ed0b';
const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');
assert.equal(inputs.head, base);
const helper = 'src/integrations/runtime/createDefaultTimeline.ts';
const tests = 'src/integrations/runtime/createDefaultTimeline.test.ts';
assert.deepEqual(git(app, base, helper), git(app, '44f0b9ca9d0247d909f86f56955a04ef6c18a2aa', helper));
assert.deepEqual(fs.readFileSync(helper), git(app, base, helper));
assert.deepEqual(fs.readFileSync(tests), git(app, base, tests));
function bodies(source) {
  const parsed = ts.createSourceFile('tests.ts', source.toString(), ts.ScriptTarget.Latest, true);
  const found = new Map();
  function visit(node) {
    if (ts.isCallExpression(node) && node.expression.getText(parsed) === 'it'
        && ts.isStringLiteral(node.arguments[0]) && node.arguments[1]) {
      found.set(node.arguments[0].text, node.arguments[1].getText(parsed));
    }
    ts.forEachChild(node, visit);
  }
  visit(parsed);
  return found;
}
const old = bodies(git(app, stage, tests));
const now = bodies(git(app, base, tests));
const originalSeven = [...old.keys()].filter((name) => !name.startsWith('never reapplies'));
assert.equal(originalSeven.length, 7);
for (const name of originalSeven) assert.equal(now.get(name), old.get(name), name);
for (const file of [helper, tests]) assert.deepEqual(git(app, fixed, file), git(app, stage, file));
function schemaInfo(repo, commit, file) {
  const raw = git(repo, commit, file);
  const schema = JSON.parse(raw);
  const ops = new Set();
  function walk(value) {
    if (!value || typeof value !== 'object') return;
    if (value.if?.properties?.op?.const) ops.add(value.if.properties.op.const);
    Object.values(value).forEach(walk);
  }
  walk(schema);
  return { commit, file, sha256: sha256(raw), definitions: Object.keys(schema.$defs).length, operations: [...ops].sort() };
}
const schemas = {
  agent31d: schemaInfo(agent, '31d02d45ad21f452724091b94b285478d00c9c21', 'astrid/core/timeline/schema/edit-command.schema.json'),
  agentCurrent: schemaInfo(agent, 'a2ba1bca3cb68a15abb62a1260162c4cb73903af', 'astrid/core/timeline/schema/edit-command.schema.json'),
  agentS2: schemaInfo(agent, '26ef2bbb31b4892fdd7c15ee5b20700bd40cb933', 'astrid/core/timeline/schema/edit-command.schema.json'),
  agentPristine: schemaInfo(agent, '487ca1e0d74edf4aecdd2b4e045294ab089fc273', 'astrid/core/timeline/schema/edit-command.schema.json'),
  runtimeS2: schemaInfo(runtime, 'f7081c14efd9a5b834987e7a1e2abf597b66313b', 'contract/schemas/edit-command.json'),
};
assert.equal(schemas.runtimeS2.sha256, schemas.agentS2.sha256);
assert.equal(schemas.runtimeS2.operations.length, 22);
assert(!schemas.runtimeS2.operations.includes('timeline.init'));
assert(schemas.agentPristine.operations.includes('timeline.init'));
assert.equal(schemas.agentPristine.operations.length, 23);
const result = {
  appBase: base, main: '44f0b9ca9d0247d909f86f56955a04ef6c18a2aa',
  helperEqualToMain: true, productFilesUnchanged: true,
  currentTestCount: now.size, unchangedOriginalSeven: originalSeven,
  unchangedAllEightStageCallbacks: [...old].every(([name, body]) => now.get(name) === body),
  fixedStageOriginalHelperAndTestsUnchanged: true, schemas,
  retainedNativeGolden: sha256(git(app, stage, 'src/tools/video-editor/commands/fixtures/recipe_m2_app_bootstrap.json')),
};
fs.writeFileSync(path.join(process.env.AUDIT_NOTES, 'source-audit.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({ ...result, schemas: Object.fromEntries(Object.entries(schemas).map(([k, v]) => [k, { ...v, operations: v.operations.length }])) }, null, 2));
