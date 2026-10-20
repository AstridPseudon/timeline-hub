import { describe, expect, it } from 'vitest';
import {
  assertContractMetadataEqual,
  assertLockMatchesManifest,
  assertSourceIdentity,
  readCommittedAppAuthority,
  requireCurrentQualificationEnvironment,
  type ContractMetadata,
} from '../../../tests/e2e/local/support/currentQualification.ts';

const committed = readCommittedAppAuthority();

describe('current browser qualification source guards', () => {
  it('uses the committed App metadata and Runtime artifact lock as the positive fixture', () => {
    expect(committed.metadata.contractVersion).toBe('0.2.3');
    expect(committed.metadata.schemaDigest).toMatch(/^sha256:[0-9a-f]{64}$/);
    expect(committed.metadata.componentManifestSha256).toMatch(/^sha256:[0-9a-f]{64}$/);
    const manifest = {
      producer: committed.runtimeLock.producer,
      version: committed.runtimeLock.producer_version,
      artifacts: Object.fromEntries(Object.values(committed.runtimeLock.files).map((entry) => [entry.from, entry.sha256])),
    };
    expect(() => assertLockMatchesManifest(committed.runtimeLock, manifest, 'fixture')).not.toThrow();
  });

  it('requires every source pin and rejects an abbreviated head', () => {
    const env = { ...Object.fromEntries(['ASTRID_CHECKOUT', 'ASTRID_RUNTIME_CHECKOUT'].map((name) => [name, '/read-only/source'])) };
    expect(() => requireCurrentQualificationEnvironment(env)).toThrow(/TIMELINE_BUNDLE_AGENT_HEAD/);
    expect(() => requireCurrentQualificationEnvironment({
      ...env,
      TIMELINE_BUNDLE_AGENT_HEAD: 'abc123',
      TIMELINE_BUNDLE_RUNTIME_HEAD: '0'.repeat(40),
    })).toThrow(/full 40-character SHA/);
  });

  it('rejects an Agent or Runtime source that moved after pinning', () => {
    const identity = { head: 'a'.repeat(40), tree: 'b'.repeat(40), status: '' };
    expect(() => assertSourceIdentity(identity, 'c'.repeat(40), 'Agent source')).toThrow(/moved/);
    expect(() => assertSourceIdentity({ ...identity, status: ' M generated.py' }, identity.head, 'Runtime source')).toThrow(/dirty/);
  });

  it('rejects client, schema, and artifact mismatches', () => {
    const wrong = (key: keyof ContractMetadata): ContractMetadata => ({ ...committed.metadata, [key]: 'mismatch' });
    expect(() => assertContractMetadataEqual(committed.metadata, wrong('contractVersion'), 'Agent')).toThrow(/client/);
    expect(() => assertContractMetadataEqual(committed.metadata, wrong('schemaDigest'), 'Runtime')).toThrow(/schema/);
    expect(() => assertContractMetadataEqual(committed.metadata, wrong('componentManifestSha256'), 'Runtime')).toThrow(/artifact/);

    const manifest = {
      producer: committed.runtimeLock.producer,
      version: committed.runtimeLock.producer_version,
      artifacts: Object.fromEntries(Object.values(committed.runtimeLock.files).map((entry) => [entry.from, entry.sha256])),
    };
    const [firstPath] = Object.keys(manifest.artifacts);
    manifest.artifacts[firstPath!] = 'sha256:' + '0'.repeat(64);
    expect(() => assertLockMatchesManifest(committed.runtimeLock, manifest, 'Runtime')).toThrow(/official artifact/);
  });
});
