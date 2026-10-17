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
  assert.equal(source.source_commit, '80f801061be732b658a7216f379a9e328e58f8bc');
  assert.equal(source.source_tree, 'feb2d58551605a733af0443ad0d079a96dc5f052');
  assert.equal(source.source_parent, 'e34470948ddce060e0bb1417497b2a2d0e1161e6');
  assert.equal(source.source_branch, 'codex/timeline-r4-A-A110-SCENE-CAPABILITY-141-CONTINUATION-001-T');
  assert.equal(source.archive, 'projects/A-integration/out/A-A110-SCENE-CAPABILITY-141-JOINED-PACKAGE-001/banodoco-timeline-composition-0.0.7.tgz');
  assert.equal(source.archive_sha256, '6011abee2026fb38c432999c4600b1cda06a336c0594c0792f3dc802294a2f01');
  assert.equal(source.archive_sha512, 'bd19355f63daf13cf865e862b5c8b944b01cf9eb9bd2dec5f085aa9c60726440fe8a367663b3da083945e05725acab017308076d1240c155188fc580cd8aca7b');
  assert.equal(source.archive_bytes, 78072);
  assert.equal(source.archive_member_count, 90);
  assert.equal(source.unpacked_bytes, 278106);
  assert.equal(source.npm_shasum, '9116ff2902353a78dc456a420d76a2f1b25ce7c1');
  assert.equal(source.npm_integrity, 'sha512-vRk1X2Pa8Tz4Zehitci5RLAc+eub0t7F8IWqnGByZED+ijZ2Y7PaCDlF4FclrKsBcwgHbRJAwVUYj8WAzYrKew==');
  assert.equal(source.source_baseline.kind, 'admitted-T-git-source');
  assert.equal(source.source_baseline.commit, source.source_commit);
  assert.equal(source.source_baseline.tree, source.source_tree);
  assert.equal(source.source_baseline.parent, source.source_parent);
  assert.equal(source.build_commit, source.source_commit);
  assert.equal(source.build_exit_code, 2);
  assert.equal(source.build_diagnostic_count, 13);
  assert.equal(source.build_diagnostics_match_inherited_baseline, true);
  assert.equal(source.build_stdout_byte_identical_to_retained_producer, true);
  assert.equal(source.producer_handback, 'projects/A-integration/receipts/A-A110-SCENE-CAPABILITY-141-CONTINUATION-001-XHARD-handback.md');
  assert.equal(source.producer_handback_sha256, '7c86e675fb6d64511ea7555e19c1bfe26a04fe67681e467696e219b958f23cc1');
  assert.equal(source.integrated_astrid_merge_commit, '13c1a2598b355acdb8f211f92392886b45787daf');
  assert.equal(source.integrated_astrid_merge_tree, 'da1ab1ff6c3c4fc945726b03a6c63fdf8e058f87');
  assert.deepEqual(source.integrated_astrid_merge_parents, [
    '8e56b10cc14f74b2920ebda42eee4dc111322037',
    'de3c8ec36f9c8fe6849d2707440eff93ddbc8b8c',
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
