import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { describe, it } from 'node:test';
import {
  MAIN95_AGENT,
  MAIN95_PRIVATE13,
  MAIN95_VENDOR,
  checkPrivateGraph,
  compareInstalledComposition,
  resolverTestCount,
  validateMain95Vendor,
  validatePrivate13Lease,
  validatePrivate13ReadyRecord,
} from './main95-prompt-settings-integration.mjs';

const provenance = JSON.parse(readFileSync('vendor/astrid-browser/provenance.json', 'utf8'));
const moduleBytes = readFileSync(`vendor/astrid-browser/${MAIN95_VENDOR.module}`);

describe('Main95 prompt/settings source roles', () => {
  it('accepts the independently qualified current vendor role', () => {
    assert.notDeepEqual(MAIN95_VENDOR, MAIN95_AGENT);
    assert.deepEqual(validateMain95Vendor(provenance, moduleBytes), {
      commit: MAIN95_VENDOR.commit,
      tree: MAIN95_VENDOR.tree,
      fileCount: MAIN95_VENDOR.fileCount,
      module: MAIN95_VENDOR.module,
      moduleSha256: MAIN95_VENDOR.moduleSha256,
    });
  });

  it('rejects the frozen execution Agent as the vendor role', () => {
    const wrongRole = structuredClone(provenance);
    wrongRole.astrid_commit = MAIN95_AGENT.commit;
    wrongRole.astrid_tree = MAIN95_AGENT.tree;
    assert.throws(() => validateMain95Vendor(wrongRole, moduleBytes), /independently qualified/);
  });

  it('rejects a vendor module provenance or byte hash change', () => {
    const wrongProvenanceHash = structuredClone(provenance);
    wrongProvenanceHash.files[MAIN95_VENDOR.module] = '0'.repeat(64);
    assert.throws(() => validateMain95Vendor(wrongProvenanceHash, moduleBytes), /module provenance hash/);
    assert.throws(() => validateMain95Vendor(provenance, Buffer.concat([moduleBytes, Buffer.from('\n')])), /module bytes changed/);
  });
});

describe('Main95 prompt/settings private13 custody', () => {
  it('accepts protected package and lock bytes through the production digest boundary', () => {
    checkPrivateGraph(
      {
        app: process.cwd(),
        privateGraph: MAIN95_PRIVATE13.graph,
        privateReady: MAIN95_PRIVATE13.ready,
        privateLease: MAIN95_PRIVATE13.lease,
      },
      'vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz',
    );
  });

  it('accepts the protected r6 lease and byte-identical installed Composition', () => {
    assert.equal(validatePrivate13ReadyRecord(readFileSync(MAIN95_PRIVATE13.ready, 'utf8')), readFileSync(MAIN95_PRIVATE13.ready, 'utf8'));
    const lease = readFileSync(MAIN95_PRIVATE13.lease, 'utf8');
    assert.equal(validatePrivate13Lease(lease).status, 'READY');
    assert.deepEqual(
      compareInstalledComposition(
        'vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz',
        `${MAIN95_PRIVATE13.graph}/@banodoco/timeline-composition`,
      ),
      { sha256: 'sha256:9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738', fileCount: 77 },
    );
  });

  it('rejects planted READY, lease, and zero-resolver-test claims', () => {
    assert.throws(() => validatePrivate13ReadyRecord('NOT READY: 77/77 regular archive members'), /READY record bytes changed/);
    const lease = readFileSync(MAIN95_PRIVATE13.lease, 'utf8').replace(
      'composition_regular_files=77',
      'composition_regular_files=0',
    );
    assert.throws(() => validatePrivate13Lease(lease), /composition_regular_files/);
    assert.equal(resolverTestCount('# tests 2\n'), 2);
    assert.throws(() => resolverTestCount('# tests 0\n'), /zero tests/);
  });
});
