import {cpSync, rmSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {join} from 'node:path';
import {buildRemotionPrimitives, primitivesPath} from './build-remotion-primitives.mjs';

const test = process.argv.includes('--test');
const output = test ? 'typescript/test-dist' : 'dist';
rmSync(output, {recursive: true, force: true});
await buildRemotionPrimitives();
execFileSync(process.execPath, ['node_modules/typescript/bin/tsc', '-p',
  `typescript/tsconfig${test ? '.test' : ''}.json`], {stdio: 'inherit'});
const lib = join(output, test ? 'src/lib' : 'lib');
cpSync(primitivesPath.replace(/\.js$/, '.d.ts'), join(lib, 'remotion-primitives.generated.d.ts'));
if (test) cpSync(primitivesPath, join(lib, 'remotion-primitives.generated.js'));
