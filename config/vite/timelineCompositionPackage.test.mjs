import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';
import { resolveConfig } from 'vite';

const appRoot = fileURLToPath(new URL('../..', import.meta.url));
const packageName = '@banodoco/timeline-composition';
const packageRoot = path.join(appRoot, 'node_modules', packageName);
const manifest = JSON.parse(fs.readFileSync(path.join(packageRoot, 'package.json'), 'utf8'));
const configs = [
  'config/vite/vite.config.ts',
  'config/testing/vitest.config.ts',
  'config/testing/vitest.boundary.config.ts',
  'config/testing/vitest.astrid-renderer.config.ts',
  'config/testing/vitest.edge.config.ts',
  'scripts/astrid-landing/public-host-browser/vite.config.ts',
];

test('root and lock use the approved immutable public10 artifact', () => {
  const artifact = 'vendor/artifacts/banodoco-timeline-composition-0.0.10.tgz';
  const bytes = fs.readFileSync(path.join(appRoot, artifact));
  const root = JSON.parse(fs.readFileSync(path.join(appRoot, 'package.json'), 'utf8'));
  const lock = JSON.parse(fs.readFileSync(path.join(appRoot, 'package-lock.json'), 'utf8'));
  const installed = lock.packages[`node_modules/${packageName}`];
  assert.equal(bytes.length, 58008);
  assert.equal(createHash('sha256').update(bytes).digest('hex'), 'cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7');
  assert.equal(root.dependencies[packageName], `file:${artifact}`);
  assert.equal(lock.packages[''].dependencies[packageName], root.dependencies[packageName]);
  assert.equal(installed.version, '0.0.10');
  assert.equal(installed.resolved, `file:${artifact}`);
  assert.equal(installed.integrity, `sha512-${createHash('sha512').update(bytes).digest('base64')}`);
  assert.equal(root.dependencies['@remotion/layout-utils'], '4.0.509');
});

for (const configFile of configs) {
  test(`${configFile} resolves Composition public exports and shared peers`, async () => {
    const previousCheckout = process.env.ASTRID_CHECKOUT;
    const previousPublicCheckout = process.env.ASTRID_PUBLIC_CHECKOUT;
    const checkout = previousCheckout || path.join(appRoot, 'vendor/astrid-browser');
    process.env.ASTRID_CHECKOUT = checkout;
    process.env.ASTRID_PUBLIC_CHECKOUT = previousPublicCheckout || checkout;
    try {
      const config = await resolveConfig({ configFile: path.join(appRoot, configFile) }, 'build');
      const resolve = config.createResolver();
      const importers = [
        path.join(appRoot, 'src/tools/video-editor/compositions/TimelineRenderer.tsx'),
        path.join(checkout, 'remotion/src/ThreeTimelineComposition.tsx'),
      ];
      assert.equal(manifest.version, '0.0.10');
      for (const [subpath, entry] of Object.entries(manifest.exports)) {
        if (subpath === './package.json') continue;
        const specifier = packageName + subpath.slice(1);
        for (const importer of importers) {
          const resolved = await resolve(specifier, importer);
          assert.ok(resolved, `${specifier} from ${importer}`);
          assert.equal(fs.realpathSync(resolved), fs.realpathSync(path.join(packageRoot, entry.import)));
        }
      }
      for (const [peer, version] of Object.entries({ ...manifest.peerDependencies, three: '0.185.1', '@remotion/three': '4.0.509' })) {
        const peerRoot = path.join(appRoot, 'node_modules', peer);
        assert.equal(JSON.parse(fs.readFileSync(path.join(peerRoot, 'package.json'), 'utf8')).version, version);
        const appPeer = await resolve(peer, importers[0]);
        const linkedPeer = await resolve(peer, importers[1]);
        const compositionPeer = await resolve(peer, path.join(packageRoot, manifest.main));
        assert.ok(appPeer, peer);
        assert.equal(linkedPeer, appPeer, `${peer} must share one runtime`);
        assert.equal(compositionPeer, appPeer, `${peer} inside Composition must share the App runtime`);
      }
    } finally {
      if (previousCheckout === undefined) delete process.env.ASTRID_CHECKOUT;
      else process.env.ASTRID_CHECKOUT = previousCheckout;
      if (previousPublicCheckout === undefined) delete process.env.ASTRID_PUBLIC_CHECKOUT;
      else process.env.ASTRID_PUBLIC_CHECKOUT = previousPublicCheckout;
    }
  });
}
