import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

const WORK = '/home/user/work';
const CLI_RELATIVE = 'node_modules/@remotion/cli/remotion-cli.js';
const root = await fs.mkdtemp(path.join(os.tmpdir(), 'vw-m4-runtime-child-existing-env-carrier-1156-'));
console.log(`fixture root: ${root}`);

function refusal(message) {
  throw new Error(`REFUSED: ${message}`);
}

async function existingProject(envFile, runtime) {
  let text;
  try {
    text = await fs.readFile(envFile, 'utf8');
  } catch {
    refusal(`missing authoritative env ${envFile}`);
  }
  const lines = text.split('\n').filter((line) => line.startsWith('ASTRID_REMOTION_PROJECT_DIR='));
  if (lines.length !== 1) refusal(`${envFile} must contain exactly one ASTRID_REMOTION_PROJECT_DIR`);
  const value = lines[0].slice('ASTRID_REMOTION_PROJECT_DIR='.length);
  if (!value.startsWith('/')) refusal(`broken non-absolute project in ${envFile}`);
  const flat = `${WORK}/runtimes/${runtime}`;
  const nested = `${flat}/remotion`;
  if (value !== flat && value !== nested) refusal(`foreign project in ${envFile}`);
  return value;
}

async function carrySuite(envFile, runtime, suiteLine, childName) {
  const project = await existingProject(envFile, runtime);
  const tokens = suiteLine.trim().split(/\s+/);
  const projectIndexes = tokens.flatMap((token, index) =>
    token.startsWith('ASTRID_REMOTION_PROJECT_DIR=') ? [index] : []);
  if (projectIndexes.length !== 1) refusal('base suite does not carry one project selection');
  const childIndex = tokens.indexOf('venv-agent-child-s2');
  if (childIndex < 0) refusal('base suite does not carry the child environment selector');
  tokens[1] = `${childName}-full`;
  tokens[projectIndexes[0]] = `ASTRID_REMOTION_PROJECT_DIR=${project}`;
  tokens[childIndex] = childName;
  const carried = tokens.join(' ');
  const selectedProject = carried.match(/(?:^| )ASTRID_REMOTION_PROJECT_DIR=([^ ]+)/)?.[1];
  assert.equal(selectedProject, project);
  const cli = path.resolve(selectedProject, CLI_RELATIVE);
  assert.equal(cli, path.join(project, CLI_RELATIVE));
  assert.equal(path.relative(project, cli), CLI_RELATIVE);
  return { carried, project, cli };
}

try {
  const oldRuntime = 'agent-remotion-0012';
  const newRuntime = 'agent-remotion-child-carrier-1156';
  const oldEnv = path.join(root, 'old.env');
  const newEnv = path.join(root, 'nested.env');
  await fs.writeFile(oldEnv, `ASTRID_REMOTION_PROJECT_DIR=${WORK}/runtimes/${oldRuntime}\n`);
  await fs.writeFile(newEnv, `ASTRID_REMOTION_PROJECT_DIR=${WORK}/runtimes/${newRuntime}/remotion\n`);
  const base = `agent remotion-0012-nodes env ASTRID_REMOTION_PROJECT_DIR=${WORK}/runtimes/${oldRuntime} venv-agent-child-s2 ${WORK}/venv-agent-child-s2/bin/python`;

  const old = await carrySuite(oldEnv, oldRuntime, base, 'venv-agent-child-flat-1156');
  assert.equal(old.project, `${WORK}/runtimes/${oldRuntime}`);
  assert.match(old.cli, /agent-remotion-0012\/node_modules\/\@remotion\/cli\/remotion-cli\.js$/);
  assert.match(old.carried, /ASTRID_REMOTION_PROJECT_DIR=\/home\/user\/work\/runtimes\/agent-remotion-0012 /);
  console.log('PASS old flat env value selects old project and in-project CLI');

  const nested = await carrySuite(newEnv, newRuntime, base, 'venv-agent-child-nested-1156');
  assert.equal(nested.project, `${WORK}/runtimes/${newRuntime}/remotion`);
  assert.match(nested.cli, /agent-remotion-child-carrier-1156\/remotion\/node_modules\/\@remotion\/cli\/remotion-cli\.js$/);
  assert.match(nested.carried, /ASTRID_REMOTION_PROJECT_DIR=\/home\/user\/work\/runtimes\/agent-remotion-child-carrier-1156\/remotion /);
  console.log('PASS new nested env value selects nested project and in-project CLI');

  const missing = path.join(root, 'missing.env');
  await assert.rejects(() => existingProject(missing, oldRuntime), /missing authoritative env/);
  await fs.writeFile(path.join(root, 'foreign.env'), 'ASTRID_REMOTION_PROJECT_DIR=/tmp/foreign-runtime\n');
  await assert.rejects(() => existingProject(path.join(root, 'foreign.env'), oldRuntime), /foreign project/);
  await fs.writeFile(path.join(root, 'broken.env'), 'ASTRID_REMOTION_PROJECT_DIR=relative/runtime\n');
  await assert.rejects(() => existingProject(path.join(root, 'broken.env'), oldRuntime), /broken non-absolute/);
  await assert.rejects(() => carrySuite(oldEnv, oldRuntime, 'agent remotion-0012-nodes venv-agent-child-s2', 'child'), /base suite does not carry one project/);
  console.log('PASS missing, foreign, broken env, and missing suite carrier refuse');
} finally {
  await fs.rm(root, { recursive: true, force: true });
}
