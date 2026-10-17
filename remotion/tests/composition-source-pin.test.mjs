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
      assert.ok(source.files.some((sourceFile) => sourceFile.path === file.emitted_from
        && sourceFile.source_git_blob === file.emitted_from_git_blob), file.path);
    }
  }
  assert.equal(source.files.find((file) => file.path === 'package.json').sha256,
    '20b0f15eba3fce002314fb24bba9017c22fd6ab2b72f4931167412e7cec00a7e');
});

test('provenance identifies this run-local development archive without authenticating the tag', () => {
  assert.equal(source.source_commit, '5947abc0f5d6c0f5ca20bb478521e010e76be039');
  assert.equal(source.source_tree, '50a4598a79b671688e4eb9e6b341e9e1e7eacbd1');
  assert.equal(source.source_parent, '80f801061be732b658a7216f379a9e328e58f8bc');
  assert.equal(source.source_branch, 'codex/timeline-r4-A-I144-ROLLING-PACKAGE-002-T');
  assert.equal(source.archive, 'projects/A-integration/out/A-I144-ROLLING-PACKAGE-002/banodoco-timeline-composition-0.0.7.tgz');
  assert.equal(source.archive_sha256, '632698e68a2d3b0b7307ed2b706b77235197ac7abcedf5f4009a9b89aee8cda8');
  assert.equal(source.archive_sha512, 'c3aeb8211d7f6310fe56cd597502297e7924f4778ad61961d1fae94d4e55cf8450c4c05db50acb14dec473f43089a59540b3c11a62569c677f1da6d46b9615f4');
  assert.equal(source.archive_bytes, 81826);
  assert.equal(source.archive_member_count, 92);
  assert.equal(source.unpacked_bytes, 291693);
  assert.equal(source.npm_shasum, 'e10a9f48d369dfc704d8dd120989eda9b49d9c16');
  assert.equal(source.npm_integrity, 'sha512-w664IR1/YxD+Vs1ZdQIpfnkk9HeK1hlh0frpTU5Vz4RQxMBdtQrLFN7Ec/QwiaWVQLPBGmJWnGd/HabUa5YV9A==');
  assert.equal(source.source_baseline.kind, 'admitted-T-git-source');
  assert.equal(source.source_baseline.commit, source.source_commit);
  assert.equal(source.source_baseline.tree, source.source_tree);
  assert.equal(source.source_baseline.parent, source.source_parent);
  assert.equal(source.build_commit, source.source_commit);
  assert.equal(source.build_exit_code, 2);
  assert.equal(source.build_diagnostic_count, 13);
  assert.equal(source.build_diagnostics_match_inherited_baseline, true);
  assert.equal(source.build_stdout_byte_identical_to_retained_producer, true);
  assert.equal(source.producer_handback, 'projects/A-integration/receipts/A-I144-COMPATIBLE-SOURCE-JOIN-001-handback.md');
  assert.equal(source.producer_handback_sha256, '2c5753ab793564aa597c94d7d9932bc4d24e981366c4622f2dbdd347b3e3b601');
  assert.equal(source.integrated_astrid_merge_commit, '8b4289dda77175e229d94b3a987dacd01cf976b4');
  assert.equal(source.integrated_astrid_merge_tree, '4bd0ec6e8a667697da19a37e1b77073f5a994a6d');
  assert.deepEqual(source.integrated_astrid_merge_parents, [
    '21e60f73a532c7b45d654423631b825418144a51',
    '94daf237fa64f6faaa0868889e8e0bb85cd16a86',
  ]);
  assert.equal(source.required_ref, 'v0.0.7/e2ab21a7');
  assert.equal(source.required_ref_authenticated, false);
  assert.match(source.scope, /Run-local development package/);
  assert.match(source.scope, /same 13 inherited TS2307 diagnostics/);
  assert.match(source.scope, /does not authenticate the published tag/);
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
