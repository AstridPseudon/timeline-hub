import { readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const functionsRoot = path.join(repoRoot, 'supabase/functions');
const supabaseConfig = readFileSync(path.join(repoRoot, 'supabase/config.toml'), 'utf8');

const RETIRED_HANDLER_FILES = [
  'ai-timeline-agent/index.ts',
  'timeline-import/index.ts',
];

const RETIRED_CANONICAL_WRITER_MARKERS = [
  'config-replaced',
  'create-with-config',
  'astridAppendService',
  'appendTimelineConfigViaService',
  'saveTimelineConfigVersioned',
  'upsert_asset_registry_entry',
];

function listProductionTypeScriptFiles(directory: string): string[] {
  return readdirSync(directory).flatMap((entry) => {
    const entryPath = path.join(directory, entry);
    const stats = statSync(entryPath);
    if (stats.isDirectory()) {
      if (entry === '_tests' || entry === 'node_modules') return [];
      return listProductionTypeScriptFiles(entryPath);
    }
    if (!entry.endsWith('.ts') || entry.endsWith('.test.ts')) return [];
    return [entryPath];
  });
}

describe('canonical timeline writer retirement', () => {
  it('removes retired handlers and canonical writer calls from edge production code', () => {
    for (const relativePath of RETIRED_HANDLER_FILES) {
      expect(() => statSync(path.join(functionsRoot, relativePath))).toThrow();
    }

    const productionSource = listProductionTypeScriptFiles(functionsRoot)
      .map((filePath) => readFileSync(filePath, 'utf8'))
      .join('\n');

    for (const marker of RETIRED_CANONICAL_WRITER_MARKERS) {
      expect(productionSource).not.toContain(marker);
    }

    expect(supabaseConfig).not.toMatch(/^\[functions\.(?:ai-timeline-agent|timeline-import)\]$/m);
    expect(supabaseConfig).toMatch(/^\[functions\.complete_task\]$/m);
  });
});
