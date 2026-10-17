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
  assert.equal(source.source_commit, 'c82eb7c459d0a41263954bf007071a6a0e8e0a6a');
  assert.equal(source.source_tree, '49975e7a54fd594e1b7fc807681fe28611d57864');
  assert.equal(source.source_parent, '5947abc0f5d6c0f5ca20bb478521e010e76be039');
  assert.deepEqual(source.source_parents, ['5947abc0f5d6c0f5ca20bb478521e010e76be039', 'dfc14e43451979198e5821175edf2b4fdb8d9375']);
  assert.equal(source.source_branch, 'codex/timeline-r4-A-STABLE145-I144-G-BG-003-T');
  assert.equal(source.archive, 'projects/A-integration/evidence/A-STABLE145-I144-G-BG-003-XHARD/banodoco-timeline-composition-0.0.7.tgz');
  assert.equal(source.archive_sha256, '9973b30819f60ed68a67e6ff8836585f72fa2550789dcb2445d5044f51fa2fe6');
  assert.equal(source.archive_sha512, '9dd7ac41432e67233f7646150112ff1ffdfa3caeba4facd9930ab8da61befc3ba5d558c3d6676369654844192ca39d5a4dda2280ed04bd14cbfd43742f11550e');
  assert.equal(source.archive_bytes, 81951);
  assert.equal(source.archive_member_count, 92);
  assert.equal(source.unpacked_bytes, 292039);
  assert.equal(source.npm_shasum, '94ab0cd290c121623798adeb205a70ec2d1c8e2b');
  assert.equal(source.npm_integrity, 'sha512-ndesQUMuZyM/dkYVARL/H/36PK66T6zZkwq42mG+/Dul1VjD1mdjaWVIRBkso51aTdoigO0EvRTL/UN0LxFVDg==');
  assert.equal(source.source_baseline.kind, 'admitted-T-git-source');
  assert.equal(source.source_baseline.commit, source.source_commit);
  assert.equal(source.source_baseline.tree, source.source_tree);
  assert.equal(source.source_baseline.parent, source.source_parent);
  assert.equal(source.build_commit, source.source_commit);
  assert.equal(source.build_exit_code, 2);
  assert.equal(source.build_diagnostic_count, 13);
  assert.equal(source.build_diagnostics_match_inherited_baseline, true);
  assert.equal(source.build_stdout_byte_identical_to_retained_producer, true);
  assert.equal(source.producer_handback, 'projects/A-integration/receipts/A-ASTRA110-NATIVE-HOLD-SCENE-003-source-handback.md');
  assert.equal(source.producer_handback_sha256, 'b42a61d0057de9ce00908ba1c5a265cc7caccfe0107f9509ff4bea25cb6dfdb6');
  assert.equal(source.integrated_astrid_merge_commit, '2b60097e3df642ff0985c3f6646c41672b2321ce');
  assert.equal(source.integrated_astrid_merge_tree, 'fa5d077f0546e185d16e49e86b20bf039adcb857');
  assert.deepEqual(source.integrated_astrid_merge_parents, ['8b4289dda77175e229d94b3a987dacd01cf976b4']);
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
