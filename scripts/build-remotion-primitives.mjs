import {mkdirSync, rmSync, readFileSync, writeFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import {dirname, join, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {build} from 'esbuild';

export const projectRoot = fileURLToPath(new URL('..', import.meta.url));
export const primitivesPath = 'typescript/src/lib/remotion-primitives.generated.js';

// Compile the installed calculation authority, never an authored copy of it.
export async function buildRemotionPrimitives(root = projectRoot) {
  const outfile = join(root, primitivesPath);
  rmSync(outfile, {force: true});
  const require = createRequire(join(root, 'package.json'));
  const packagePath = require.resolve('remotion/package.json');
  const {version} = JSON.parse(readFileSync(packagePath, 'utf8'));
  if (version !== '4.0.509') throw new Error(`Expected Remotion 4.0.509, got ${version}`);
  const cjs = join(dirname(packagePath), 'dist/cjs');
  const result = await build({
    stdin: {
      contents: "export {spring} from './spring/index.js'; export {interpolate} from './interpolate.js';",
      resolveDir: cjs,
      sourcefile: 'remotion-primitives',
    },
    outfile,
    bundle: true,
    format: 'esm',
    platform: 'neutral',
    target: 'es2022',
    metafile: true,
    write: false,
  });
  for (const input of Object.keys(result.metafile.inputs)) {
    if (!resolve(input).startsWith(cjs + '/')) {
      throw new Error(`Unexpected Remotion calculation dependency: ${input}`);
    }
  }
  if (Object.values(result.metafile.outputs).some(output => output.imports.length)) {
    throw new Error('Remotion calculation bundle must be self-contained');
  }
  // Do not leave a previous bundle available if resolution or compilation fails.
  mkdirSync(dirname(outfile), {recursive: true});
  writeFileSync(outfile, result.outputFiles[0].contents);
  return result.metafile;
}
