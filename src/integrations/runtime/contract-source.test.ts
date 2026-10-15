// @vitest-environment node
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { SCHEMA_DIGEST } from './generated-contract-metadata.ts';
import { RUNTIME_SCHEMA_DIGEST } from './contract-metadata.ts';

// Source admission is supplied by the caller. Never discover a live Runtime or
// sibling checkout implicitly. No generation, writes, service or data access.
const runtimeSource = process.env.RUNTIME_CONTRACT_SOURCE;
const opcallSchema = process.env.ASTRID_OPCALL_SCHEMA;
describe.skipIf(!runtimeSource || !opcallSchema)('admitted Runtime source contract binding', () => {
  it('binds the App digest to the exact producer generator and server/client metadata', () => {
    const typescript = readFileSync(path.join(runtimeSource!, 'packages/typescript/src/contract-metadata.ts'), 'utf8');
    const server = readFileSync(path.join(runtimeSource!, 'runtime_protocol/contract_metadata.py'), 'utf8');
    const producerDigest = typescript.match(/SCHEMA_DIGEST = "([^"]+)"/)?.[1];
    expect(server.match(/SCHEMA_DIGEST = '([^']+)'/)?.[1]).toBe(producerDigest);
    expect(RUNTIME_SCHEMA_DIGEST).toBe(SCHEMA_DIGEST);
    // Keep both exact mismatches visible; neither justifies guessing a new pin.
    expect.soft(SCHEMA_DIGEST).toBe(producerDigest);
    const generation = spawnSync('python3', ['-c',
      "import runpy,sys; print(runpy.run_path(sys.argv[1])['contract_digest']())",
      path.join(runtimeSource!, 'generators/generate.py')], {
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1', ASTRID_OPCALL_SCHEMA: opcallSchema! },
      encoding: 'utf8',
    });
    expect.soft(generation.status, generation.stderr).toBe(0);
    if (generation.status === 0) expect(generation.stdout.trim()).toBe(producerDigest);
  });
});
