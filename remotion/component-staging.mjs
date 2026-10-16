import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

// Only Python's invocation-private stage projection enters this seam. Neither
// timeline JSON nor a browser request supplies a module path.
export const componentAliases = (configuration, remotionRoot, env = process.env) => {
  const raw = env.ASTRID_REMOTION_COMPONENT_STAGE;
  if (!raw) return configuration;
  if (typeof remotionRoot !== 'string' || !path.isAbsolute(remotionRoot)) {
    throw new Error('Component staging requires its explicit absolute Remotion root');
  }
  const stage = JSON.parse(raw);
  const root = fs.realpathSync(stage.root);
  const files = stage.files;
  if (!path.isAbsolute(stage.root) || !files || !Object.hasOwn(files, stage.module)) {
    throw new Error('Invalid component stage projection');
  }
  for (const [filename, digest] of Object.entries(files)) {
    const relative = path.relative(root, fs.realpathSync(filename));
    if (!relative || relative === '..' || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)
      || createHash('sha256').update(fs.readFileSync(filename)).digest('hex') !== digest) {
      throw new Error(`Changed or escaped staged component: ${filename}`);
    }
  }
  return {
    ...configuration,
    resolve: {...configuration.resolve, alias: {...configuration.resolve?.alias,
      '@astrid-component-bindings$': stage.module}},
    module: {...configuration.module, rules: [...(configuration.module?.rules ?? []), {
      enforce: 'pre', include: Object.keys(files),
      loader: path.join(remotionRoot, 'component-source-loader.cjs'), options: {root, files},
    }]},
  };
};
