// Sandbox pipes return EPERM. Preserve captured bytes using private regular files.
import childProcess from 'node:child_process';
import {syncBuiltinESMExports} from 'node:module';
import {closeSync, mkdtempSync, openSync, readFileSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
const original = childProcess.spawnSync;
childProcess.spawnSync = (command, args, options = {}) => {
  if (options.stdio !== undefined) return original(command, args, options);
  const directory = mkdtempSync(join(tmpdir(), 'captured-child-'));
  const output = join(directory, 'stdout');
  const error = join(directory, 'stderr');
  const out = openSync(output, 'w');
  const err = openSync(error, 'w');
  let result;
  try {
    result = original(command, args, {...options, stdio: ['ignore', out, err]});
  } finally {
    closeSync(out);
    closeSync(err);
  }
  try {
    result.stdout = readFileSync(output, options.encoding ?? null);
    result.stderr = readFileSync(error, options.encoding ?? null);
    result.output = [null, result.stdout, result.stderr];
    return result;
  } finally {
    rmSync(directory, {recursive: true, force: true});
  }
};
syncBuiltinESMExports();
