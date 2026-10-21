import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {existsSync, lstatSync, readFileSync, readlinkSync, readdirSync, realpathSync} from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {gunzipSync} from 'node:zlib';
import {build} from '/home/user/work/app/node_modules/esbuild/lib/main.js';

const FROZEN_CONTROLLER = '/home/user/work/wt/app-pin-0d432391/tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs';
const {hashTree: controllerHashTree} = await import(pathToFileURL(FROZEN_CONTROLLER).href);

export const STAGE = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage';
export const STAGE_METADATA_ROOT = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054';
export const SOURCE = '/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b';
export const SOURCE_GRAPH = '4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c';
export const LOCK = 'c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24';
export const PUBLIC13 = '9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738';
export const SCRIPT = '24cc758029518075f671b06dffc75582b772f2fc52a5e4b57450b46c08a0c66c';
export const MANIFEST = 'b349c5344ec607bc32b0e4711adf317aacd984ce98d3e5a316ba726079bb37ac';
export const NODE_MANIFEST = '0d9da325991bfed2fda247284adb37885d118a08f5f4fc655128f6b7481c04de';
export const CUSTODY = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m3-staged-runtime-attachment-final-custody-1054-REPORT.md';

const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const digest = file => sha(readFileSync(file));
const contained = (root, target) => target === root || target.startsWith(`${root}${path.sep}`);

function tree(root) {
  return controllerHashTree(root);
}

function readlink(file) {
  return readlinkSync(file);
}

function assertRealRegular(file, label) {
  const stat = lstatSync(file);
  assert.equal(stat.isFile(), true, `${label} must be a regular file`);
  assert.equal(stat.isSymbolicLink(), false, `${label} must not be a symlink`);
  assert.equal(stat.nlink, 1, `${label} must have nlink=1`);
  return stat;
}

function assertContainedGraph(root) {
  const files = [];
  const walk = directory => {
    for (const name of readdirSync(directory)) {
      const absolute = path.join(directory, name);
      const stat = lstatSync(absolute);
      if (stat.isDirectory()) walk(absolute);
      else if (stat.isSymbolicLink()) {
        const target = realpathSync(absolute);
        assert.equal(contained(root, target), true, `graph link escapes project: ${absolute}`);
        assertRealRegular(target, `graph link target ${absolute}`);
      } else if (stat.isFile()) {
        assert.equal(stat.nlink, 1, `destination regular file is shared: ${absolute}`);
        files.push(absolute);
      } else throw new Error(`unsupported project member: ${absolute}`);
    }
  };
  walk(root);
  return files;
}

function assertGraphInodes(sourceRoot, destinationRoot) {
  const walk = (directory, relative = '') => {
    for (const name of readdirSync(directory)) {
      const source = path.join(directory, name);
      const destination = path.join(destinationRoot, relative, name);
      const stat = lstatSync(source);
      assert.equal(existsSync(destination), true, `missing staged graph member: ${relative}${name}`);
      const dstStat = lstatSync(destination);
      if (stat.isDirectory()) walk(source, path.join(relative, name));
      else if (stat.isFile()) {
        assert.equal(dstStat.isFile(), true, `staged graph kind changed: ${relative}${name}`);
        assert.notDeepEqual([stat.dev, stat.ino], [dstStat.dev, dstStat.ino], `source inode reused: ${relative}${name}`);
        assert.equal(digest(source), digest(destination), `staged graph content changed: ${relative}${name}`);
      } else if (stat.isSymbolicLink()) {
        assert.equal(dstStat.isSymbolicLink(), true, `staged graph link changed: ${relative}${name}`);
        assert.equal(readlink(destination), readlink(source), `staged graph link target changed: ${relative}${name}`);
      }
    }
  };
  walk(sourceRoot);
}

function tarRegularMembers(archive) {
  const bytes = gunzipSync(readFileSync(archive));
  const members = [];
  for (let offset = 0; offset + 512 <= bytes.length;) {
    const header = bytes.subarray(offset, offset + 512);
    if (header.every(byte => byte === 0)) break;
    const name = header.subarray(0, 100).toString('utf8').replace(/\0.*$/, '');
    const sizeText = header.subarray(124, 136).toString('ascii').replace(/\0.*$/, '').trim();
    const size = sizeText ? Number.parseInt(sizeText, 8) : 0;
    const type = header[156];
    if (type === 0 || type === 48) members.push(name);
    offset += 512 + Math.ceil(size / 512) * 512;
  }
  return members;
}

export async function assertCompleteStage(stage = STAGE) {
  assert.equal(realpathSync(stage), stage, 'complete stage must be canonical');
  assert.equal(realpathSync(STAGE_METADATA_ROOT), STAGE_METADATA_ROOT, 'stage metadata root must be canonical');
  assert.equal(path.dirname(stage), STAGE_METADATA_ROOT, 'stage must use the reviewed metadata root');
  const project = path.join(stage, 'remotion');
  const closure = path.join(stage, 'astrid/packs/rendering/editor/live-scenes');
  assert.equal(realpathSync(project), project, 'staged project must be canonical');
  assert.equal(realpathSync(closure), closure, 'staged source closure must be canonical');
  assert.equal(digest(path.join(STAGE_METADATA_ROOT, 'stage-complete-runtime.sh')), SCRIPT);
  assert.equal(digest(path.join(STAGE_METADATA_ROOT, 'stage-manifest.tsv')), MANIFEST);
  assert.equal(digest(path.join(STAGE_METADATA_ROOT, 'node-graph-manifest.tsv')), NODE_MANIFEST);
  assert.equal(digest(path.join(project, 'package-lock.json')), LOCK);
  assert.equal(digest(path.join(project, 'artifacts/banodoco-timeline-composition-0.0.13.tgz')), PUBLIC13);
  assert.equal(tarRegularMembers(path.join(project, 'artifacts/banodoco-timeline-composition-0.0.13.tgz')).length, 77);
  const graph = tree(path.join(project, 'node_modules'));
  assert.equal(graph.sha256, SOURCE_GRAPH);
  assert.equal(graph.fileCount, 21455);
  assertGraphInodes(path.join(SOURCE, 'node_modules'), path.join(project, 'node_modules'));
  assertContainedGraph(project);
  for (const file of ['node_modules/@remotion/cli/remotion-cli.js', 'src/astrid-frame-worker.mjs']) {
    assertContainedGraph(path.dirname(path.join(project, file)));
    assertRealRegular(path.join(project, file), file);
  }
  const closureHashes = {
    'SceneSurface.tsx': '830b7966ed736431ef688242c0917273d563e9716f3f58a633b5402879e7c2f9',
    'authoring.ts': '0a555b38ad93727e87f0dc08ed958a90412511be94a8bb632830c234f233d276',
    'diagnostics.ts': '012c8d739dfddf33742e0479a19a59d0a1f1b7e618e1e3948a049b962080a022',
    'extension.tsx': '4a77f276c6f1ac2725441bb93ade19bf51032c38cc8f95a76642eeeacb7c9f83',
    'identity.ts': 'ab1fa9c6972518d85dd39f5f1fdeee983a2754b6ad04a738d3e4dff13ed2b3b9',
    'runtime.ts': '3bdfa73290d935699d3937798df950376cfd25209a442fc9b294fc12c98a14f2',
  };
  for (const [file, expected] of Object.entries(closureHashes)) {
    assert.equal(digest(path.join(closure, file)), expected, `closure changed: ${file}`);
    assertRealRegular(path.join(closure, file), file);
  }
  assert.match(readFileSync(CUSTODY, 'utf8'), /APPROVED for the single subsequent central preflight only/);
  const bundle = await build({
    entryPoints: [path.join(project, 'src/index.ts')], bundle: true, write: false,
    format: 'esm', platform: 'neutral', target: 'es2022', jsx: 'automatic',
    plugins: [{name: 'externalize-bare-package-imports', setup(api) {
      api.onResolve({filter: /^[^./]/}, args => ({path: args.path, external: true}));
    }}],
  });
  assert.ok(bundle.outputFiles[0].contents.byteLength > 0, 'final-root closure bundle is empty');
  return {stage, project, graph, closureFiles: Object.keys(closureHashes).length, bundleBytes: bundle.outputFiles[0].contents.byteLength};
}

if (import.meta.url === `file://${process.argv[1]}`) {
  console.log(JSON.stringify(await assertCompleteStage(process.argv[2] || STAGE), null, 2));
}
