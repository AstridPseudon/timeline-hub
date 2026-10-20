from pathlib import Path
import json
import os
import subprocess
import tempfile
from astrid.core.element.registry import ElementRegistry
from astrid.core.element.schema import ElementDefinition
from astrid.core.rendering import remotion_runtime
from astrid.core.theme._schema import BUILTIN_DEFAULT_THEME
from scripts import gen_effect_registry

REPO = Path('/home/user/work/wt/vw-m3-pcm-kernel-current-land-unit')
PREFIX = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-kernel-current-land-unit-'
PROJECT = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-kernel-current-land-unit/checks/remotion')
NODE = '/tmp/vw-m3-agent-gate-node20.19.4/bin/node'
assert remotion_runtime._COMPOSITION_PACKAGE_VERSION == '0.0.12'
assert remotion_runtime._composition_package_problem(PROJECT) is None
print('PASS: unchanged real admission code accepts the private public12 package')
exports = ['.', './evaluation', './theme-api', './registries', './effects.generated', './animations.generated', './transitions.generated', './registry.generated']
probe = PROJECT / 'public-runtime.mjs'
probe.write_text('''import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createRequire} from 'node:module';
import path from 'node:path';
import {DEFAULT_THEME, TimelineComposition} from '@banodoco/timeline-composition';
const require = createRequire(import.meta.url);
const installed = path.resolve('node_modules/@banodoco/timeline-composition/package.json');
const packageRequire = createRequire(installed);
assert.equal(JSON.parse(fs.readFileSync(installed)).version, '0.0.12');
for (const name of ['react', 'react-dom', 'remotion', '@remotion/media', '@remotion/layout-utils']) {
  assert.equal(fs.realpathSync(require.resolve(name + '/package.json')), fs.realpathSync(packageRequire.resolve(name + '/package.json')), name);
}
for (const subpath of ''' + json.dumps(exports) + ''') {
  const name = '@banodoco/timeline-composition' + (subpath === '.' ? '' : subpath.slice(1));
  assert.ok(Object.keys(await import(name)).length, name);
}
assert.equal(typeof TimelineComposition, 'function');
assert.deepEqual(DEFAULT_THEME, ''' + json.dumps(BUILTIN_DEFAULT_THEME) + ''');
console.log('PASS: eight public runtime exports; React/Remotion peer identity; full DEFAULT_THEME deep equality');
''')
subprocess.run([NODE, str(probe)], cwd=PROJECT, check=True, env=os.environ)
# Exercise the unchanged direct consumer/SSR/registry test from this source tree.
with tempfile.TemporaryDirectory(dir=PROJECT, prefix='host-fixture-') as scratch:
    fixture=Path(scratch)
    elements=[]
    for kind, element_id in [('effects','custom'),('animations','fade-up'),('transitions','fade')]:
        root=fixture / kind / element_id
        root.mkdir(parents=True)
        (root/'component.tsx').write_bytes((REPO/'remotion/tests'/f'custom-{kind}.tsx').read_bytes())
        elements.append(ElementDefinition(id=element_id,kind=kind,root=root,source='pack:probe',editable=True,
            priority=0,component=root/'component.tsx',schema={},defaults={'durationFrames':8},
            metadata={'pack_id':'probe','kind':'wrapper','phase':['entrance','exit'],
                **({'clipTypeAliases':['custom-alias']} if kind=='effects' else {})}))
    registry=ElementRegistry(elements)
    gen_effect_registry._element_registry=lambda:registry
    for kind in ['effects','animations','transitions']:
        (fixture/f'{kind}.generated.ts').write_text(gen_effect_registry.generate_element_registry(kind))
    (fixture/'host-registries.ts').write_bytes((REPO/'remotion/src/host-registries.ts').read_bytes())
    subprocess.run([NODE,str(PROJECT/'tests/composition-package.mjs'),str(fixture)],cwd=PROJECT,check=True,env=os.environ)
print('PASS: exact current host registry generator and unmodified package consumer/SSR probe')
