import { createHash } from 'node:crypto';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const closureRoot = path.join(projectRoot, 'vendor/astrid-build-inputs');
const manifestPath = path.join(closureRoot, 'manifest.json');
const manifest = JSON.parse(await readFile(manifestPath, 'utf8'));

if (manifest.schema !== 'astrid-container-source-closure/v1') {
  throw new Error(`Unsupported Astrid source closure schema: ${manifest.schema}`);
}

let checked = 0;
for (const [name, source] of Object.entries(manifest.sources ?? {})) {
  const sourceDirectory = path.join(closureRoot, source.directory);
  const expectedRoot = path.resolve(sourceDirectory, source.source_root);
  const rootStat = await stat(expectedRoot).catch(() => null);
  if (!rootStat?.isDirectory()) {
    throw new Error(`Missing ${name} Astrid source root: ${expectedRoot}`);
  }

  for (const entry of source.files ?? []) {
    if (path.isAbsolute(entry.path) || entry.path.split(/[\\/]/).includes('..')) {
      throw new Error(`Unsafe ${name} source path in manifest: ${entry.path}`);
    }
    const sourcePath = path.resolve(sourceDirectory, entry.path);
    const relative = path.relative(sourceDirectory, sourcePath);
    if (relative.startsWith(`..${path.sep}`) || relative === '..') {
      throw new Error(`Astrid source path escapes its pinned root: ${entry.path}`);
    }

    const bytes = await readFile(sourcePath);
    const actual = createHash('sha256').update(bytes).digest('hex');
    if (actual !== entry.sha256) {
      throw new Error(`Astrid ${name} source hash mismatch for ${entry.path}: ${actual}`);
    }
    if (bytes.length !== entry.size_bytes) {
      throw new Error(`Astrid ${name} source size mismatch for ${entry.path}`);
    }
    checked += 1;
  }
}

if (checked === 0) throw new Error('Astrid source closure manifest contains no files');
process.stdout.write(`Verified ${checked} pinned Astrid source files.\n`);
