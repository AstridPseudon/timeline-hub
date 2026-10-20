// Pure in-memory evaluation of the frozen renderer's grant block. No renderer import.
import fs from 'node:fs';
import crypto from 'node:crypto';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath, pathToFileURL} from 'node:url';

const orch = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch';
const prefix = `${orch}/design/handoff-vw-m3-main-cap-controller-repair-`;
const own = `${orch}/workers/vw-m3-main-cap-controller-repair`;
const render = `${prefix}render.mjs`;
const controller = `${prefix}controller.py`;
const suiteLine = `agent e2e-viewing-main6-image-cap-three-stills /home/user/work/venv-agent/bin/python ${controller} capture`;
const source = fs.readFileSync(render, 'utf8');
const start = source.indexOf('const controller =');
const end = source.indexOf("check(fs.readFileSync(`${orch}/tests/suites.conf`");
assert(start > 0 && end > start);
const block = source.slice(start, end).replace('import.meta.url', JSON.stringify(pathToFileURL(render).href));
const original = new Map([
  [controller, fs.readFileSync(controller)],
  [render, fs.readFileSync(render)],
]);
const sha = (value) => crypto.createHash('sha256').update(value).digest('hex');
const grant = `${suiteLine}\ncontroller_sha256=${sha(original.get(controller))}\nrender_sha256=${sha(original.get(render))}\n`;

function run(kind) {
  const data = new Map(original);
  data.set(`${own}/CAPTURE-GRANT.txt`, Buffer.from(grant));
  if (kind === 'controller-tamper') data.set(controller, Buffer.concat([data.get(controller), Buffer.from('\n#tamper\n')]));
  if (kind === 'renderer-tamper') data.set(render, Buffer.concat([data.get(render), Buffer.from('\n//tamper\n')]));
  if (kind === 'path-only') data.set(`${own}/CAPTURE-GRANT.txt`, Buffer.from(suiteLine));
  const context = {
    prefix, own, suiteLine, fileURLToPath,
    check: (ok, message) => { if (!ok) throw new Error(message); },
    // Parent traversal is covered by source review; this probe isolates byte binding.
    realParents: () => {},
    digest: (file) => { assert(data.has(file)); return sha(data.get(file)); },
    fs: {readFileSync: (file, encoding) => {
      assert(data.has(file));
      return encoding ? data.get(file).toString(encoding) : data.get(file);
    }},
  };
  const evaluate = () => vm.runInNewContext(block, context, {timeout: 1000});
  if (kind === 'exact') evaluate();
  else assert.throws(evaluate, /controller\/render SHA256/);
  console.log(`PASS: renderer grant block ${kind}`);
}

for (const kind of ['exact', 'controller-tamper', 'renderer-tamper', 'path-only']) run(kind);
console.log('No module execution, renderer import, service read/write, source extraction, browser, or socket');
