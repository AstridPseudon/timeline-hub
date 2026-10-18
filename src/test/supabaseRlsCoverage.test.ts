import { readdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

const migrationsDir = path.resolve(process.cwd(), 'supabase', 'migrations');

const explicitUserOwnedTables = new Map([
  ['projects', 'core project container owned by users'],
  ['shots', 'project-owned child records'],
  ['shot_generations', 'project-owned join records'],
]);

function normalizeSql(sql: string): string {
  return sql
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/--.*$/gm, '');
}

function scanMigrations() {
  const createTablePattern =
    /create table\s+(?:if not exists\s+)?(?:"?public"?\.)?"?([a-z0-9_]+)"?\s*\(([\s\S]*?)\);/gim;
  const enableRlsPattern =
    /alter table\s+(?:if exists\s+)?(?:"?public"?\.)?"?([a-z0-9_]+)"?\s+enable row level security\b/gim;
  const createPolicyPattern =
    /create policy\s+.+?\s+on\s+(?:"?public"?\.)?"?([a-z0-9_]+)"?\b/gim;

  const userOwned = new Map<string, { file: string; reason: string }>();
  const rlsEnabled = new Set<string>();
  const policied = new Set<string>();

  const migrationFiles = readdirSync(migrationsDir)
    .filter((entry) => entry.endsWith('.sql'))
    .sort();

  for (const file of migrationFiles) {
    const sql = normalizeSql(readFileSync(path.join(migrationsDir, file), 'utf8'));

    for (const match of sql.matchAll(createTablePattern)) {
      const tableName = match[1].toLowerCase();
      const createBody = match[2].toLowerCase();
      const isDirectUserOwned =
        explicitUserOwnedTables.has(tableName)
        || /\buser_id\b/.test(createBody)
        || /references\s+(?:"?public"?\.)?"?users"?\s*\(/.test(createBody);

      if (isDirectUserOwned && !userOwned.has(tableName)) {
        userOwned.set(tableName, {
          file,
          reason: explicitUserOwnedTables.get(tableName) ?? 'table stores direct user ownership',
        });
      }
    }

    for (const match of sql.matchAll(enableRlsPattern)) {
      rlsEnabled.add(match[1].toLowerCase());
    }

    for (const match of sql.matchAll(createPolicyPattern)) {
      policied.add(match[1].toLowerCase());
    }
  }

  return { userOwned, rlsEnabled, policied };
}

describe('user-owned Supabase tables', () => {
  const { userOwned, rlsEnabled, policied } = scanMigrations();

  it('finds the user-owned tables the migrations create', () => {
    expect(userOwned.size).toBeGreaterThan(0);
  });

  it('enables row level security and at least one policy for each', () => {
    const errors: string[] = [];
    for (const [tableName, origin] of userOwned) {
      if (!rlsEnabled.has(tableName)) {
        errors.push(
          `${tableName} (${origin.reason}) was introduced in ${origin.file} without any ENABLE ROW LEVEL SECURITY coverage in migrations.`,
        );
      }
      if (!policied.has(tableName)) {
        errors.push(
          `${tableName} (${origin.reason}) was introduced in ${origin.file} without any CREATE POLICY coverage in migrations.`,
        );
      }
    }
    expect(errors).toEqual([]);
  });
});
