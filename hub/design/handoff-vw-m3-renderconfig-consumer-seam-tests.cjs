// Artifact checks only: this does not execute or qualify the proposed behavior.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { createHash } = require('node:crypto');
const ts = require('/home/user/work/app/node_modules/typescript/lib/typescript.js');
const prefix = __filename.replace(/-tests\.cjs$/, '');
const identity = JSON.parse(readFileSync(prefix + '-source-identity.json', 'utf8'));
const sources = JSON.parse(readFileSync(0, 'utf8'));
const patch = readFileSync(prefix + '-consumer-UNAPPLIED.patch', 'utf8');
const files = [...patch.matchAll(/^--- a\/(.+)\n\+\+\+ b\/\1\n([\s\S]*?)(?=^--- a\/|$(?![\s\S]))/gm)];

test('patch changes only the five consumer/caller paths, with no producer or policy file', () => {
  assert.equal(files.length, 5);
  assert.deepEqual(files.map(m => m[1]).sort(), Object.keys(identity.sha256).sort());
});
for (const [, name, body] of files) {
  test('frozen source, exact unapplied hunks and TypeScript syntax: ' + name, () => {
    const source = sources[name];
    assert.equal(createHash('sha256').update(source).digest('hex'), identity.sha256[name]);
    const original = source.split('\n');
    const result = [];
    let cursor = 0;
    for (const hunk of body.split(/(?=^@@ )/m).filter(h => h.startsWith('@@ '))) {
      const lines = hunk.trimEnd().split('\n');
      const match = /^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@/.exec(lines.shift());
      assert.ok(match);
      const start = Number(match[1]) - 1;
      result.push(...original.slice(cursor, start));
      cursor = start;
      for (const line of lines) {
        const kind = line[0];
        if (kind === ' ' || kind === '-') assert.equal(original[cursor++], line.slice(1));
        if (kind === ' ' || kind === '+') result.push(line.slice(1));
      }
    }
    result.push(...original.slice(cursor));
    const candidate = result.join('\n');
    const parsed = ts.createSourceFile(name, candidate, ts.ScriptTarget.Latest, true,
      name.endsWith('.tsx') ? ts.ScriptKind.TSX : ts.ScriptKind.TS);
    assert.deepEqual(parsed.parseDiagnostics.map(d => ts.flattenDiagnosticMessageText(d.messageText, '\n')), []);
  });
}
