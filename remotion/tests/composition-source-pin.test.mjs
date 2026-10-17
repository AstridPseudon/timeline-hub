import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync, readdirSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import test from 'node:test';

const root = fileURLToPath(new URL('../', import.meta.url));
const vendor = path.join(root, 'vendor/timeline-composition');
const json = (file) => JSON.parse(readFileSync(file, 'utf8'));
const source = json(path.join(root, 'vendor/timeline-composition.source.json'));
const manifest = json(path.join(root, 'package.json'));
const lock = json(path.join(root, 'package-lock.json'));
const packed = json(path.join(vendor, 'package.json'));

test('vendored payload matches the recorded package and retains source Git blob identities', () => {
  const files = (dir) => readdirSync(dir, {withFileTypes: true}).flatMap((entry) => {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) return files(file);
    assert.ok(entry.isFile(), `unexpected non-regular payload: ${file}`);
    return [path.relative(vendor, file).split(path.sep).join('/')];
  });
  assert.deepEqual(files(vendor).sort(), source.files.map((file) => file.path).sort());
  assert.equal(source.files.length, source.archive_member_count);
  assert.equal(source.files.reduce((sum, file) => sum + file.bytes, 0), source.unpacked_bytes);
  for (const file of source.files) {
    assert.ok(!path.isAbsolute(file.path) && !file.path.split('/').includes('..'));
    const bytes = readFileSync(path.join(vendor, file.path));
    assert.equal(bytes.length, file.bytes, file.path);
    assert.equal(createHash('sha256').update(bytes).digest('hex'), file.sha256, file.path);
    if (file.source_git_blob) {
      assert.equal(createHash('sha1').update(`blob ${bytes.length}\0`).update(bytes).digest('hex'), file.source_git_blob, file.path);
      assert.equal(file.emitted_from, null, file.path);
    } else {
      assert.ok(file.path.startsWith('typescript/dist/src/') && file.path.endsWith('.js'), file.path);
      assert.ok(source.files.some((sourceFile) => sourceFile.path === file.emitted_from && sourceFile.source_git_blob), file.path);
    }
  }
  assert.equal(source.files.find((file) => file.path === 'package.json').sha256,
    '20b0f15eba3fce002314fb24bba9017c22fd6ab2b72f4931167412e7cec00a7e');
});

test('provenance identifies this run-local development archive without authenticating the tag', () => {
  assert.equal(source.source_commit, '67245fb4f734e2c4d9138e8ab3df87921f51b492');
  assert.equal(source.source_tree, '23854d166c8692bb8c21f1da1f5ae0203215fb98');
  assert.equal(source.source_parent, 'f2cf610726410c4bb5d8933f17a85baa23ee252e');
  assert.equal(source.source_branch, 'codex/timeline-r4-A-COMPOSITION-EASING-005');
  assert.equal(source.archive, 'projects/A-integration/out/A-COMPOSITION-EASING-RESTORE-005/banodoco-timeline-composition-0.0.7.tgz');
  assert.equal(source.archive_sha256, '724b8818d5787687abfc72be9e9cffc185bcbffa9a122dd0a43750be337f62b6');
  assert.equal(source.archive_sha512, '841d8af8a121cd3c658a36d9d0d6532511da114b5c790d2e31d181bc90b34fafa7f4cbbad96f3610f73c07a532ac36607e5a389bb075f8ec71770d8cf53a7aa5');
  assert.equal(source.archive_bytes, 74885);
  assert.equal(source.archive_member_count, 88);
  assert.equal(source.unpacked_bytes, 267424);
  assert.equal(source.npm_shasum, '40a19a0bc4975baf73ea530ea11d244711fa620d');
  assert.equal(source.npm_integrity, 'sha512-hB2K+KEhzTxlijbZ0NZTJRHaEUtceQ0uMdGBvJCzT6+n9Mu62W82EPc8B6UyrDZgflo4m7B1+Oxxdw2M9Tp6pQ==');
  assert.equal(source.source_baseline.kind, 'authenticated-npm-package-payload-import');
  assert.equal(source.source_baseline.authenticated_archive_sha256, '02500c55dcdc1883e027d89ab42e2426191fad3ab1fdcd08d3fce1ca51f11032');
  assert.equal(source.source_baseline.initial_commit, 'f9da6c0477feb73a7d0f13f37bed3e4861254cd2');
  assert.equal(source.source_baseline.initial_tree, '1d92ed9b6a1a77ee382c84205419e878cf49ef4d');
  assert.equal(source.source_baseline.initial_parent, null);
  assert.equal(source.source_baseline.single_exact_remote_fetch.exit_code, 128);
  assert.equal(source.easing_patch_sha256, '11ea52a2fdcdebf75cf51b492191f5fc7b1f49d021e9bd8cdb7dc793b7c04800');
  assert.equal(source.easing_patch_commit, 'f2cf610726410c4bb5d8933f17a85baa23ee252e');
  assert.equal(source.build_commit, source.source_commit);
  assert.equal(source.build_exit_code, 2);
  assert.equal(source.build_diagnostic_count, 13);
  assert.equal(source.build_diagnostics_match_inherited_baseline, true);
  assert.equal(source.producer_handback, 'projects/I-story-motion-audio/receipts/I-EXT-COMPONENT-UNKNOWN-BOUNDS-006-handback.md');
  assert.equal(source.producer_handback_sha256, 'ae569f046c193dc87f7b55684239e413e823a527e62877f5695f9a9b822013bd');
  assert.equal(source.required_ref, 'v0.0.7/e2ab21a7');
  assert.equal(source.required_ref_authenticated, false);
  assert.match(source.scope, /Run-local development package/);
  assert.match(source.scope, /original T source repository\/history and tests were not recovered/);
  assert.equal(packed.name, source.package);
  assert.equal(packed.version, source.package_version);
});

test('manifest and lock consume the local package with matching linked metadata', () => {
  const name = '@banodoco/timeline-composition';
  assert.equal(lock.lockfileVersion, 3);
  assert.equal(manifest.dependencies[name], 'file:vendor/timeline-composition');
  assert.deepEqual(lock.packages[''].dependencies, manifest.dependencies);
  assert.deepEqual(lock.packages[''].devDependencies, manifest.devDependencies);
  assert.deepEqual(lock.packages[`node_modules/${name}`], {
    resolved: 'vendor/timeline-composition', link: true,
  });
  const metadata = Object.fromEntries(
    ['name', 'version', 'dependencies', 'devDependencies', 'peerDependencies']
      .filter((key) => key in packed).map((key) => [key, packed[key]]),
  );
  assert.deepEqual(lock.packages['vendor/timeline-composition'], metadata);
  // The admitted package's own historical devDependencies remain byte-exact;
  // this assertion covers the host dependency closure, not that dev subtree.
  for (const group of ['dependencies', 'devDependencies']) {
    for (const [name, version] of Object.entries(manifest[group])) {
      if (name === 'remotion' || name.startsWith('@remotion/')) {
        assert.equal(version, '4.0.509', name);
        assert.equal(lock.packages[`node_modules/${name}`].version, version, name);
      }
    }
  }
});

test('public evaluation export resolves to an inventoried pure source file', () => {
  for (const target of Object.values(packed.exports['./evaluation'])) {
    assert.equal(target, './typescript/src/evaluation.ts');
    assert.ok(source.files.some((file) => `./${file.path}` === target));
  }
});
