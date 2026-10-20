import { describe, expect, it, vi } from 'vitest';
import type { ResolvedTimelineConfig, TimelineConfig } from '@/tools/video-editor/types/index.ts';
import { prepareVisualSeamSnapshotConfig } from './useTimelineState.ts';

const authoredContract = {
  version: 1,
  mode: 'enforced',
  pictureTracks: ['picture'],
  continuityTracks: ['picture'],
  gaps: [{ kind: 'pause', track: 'picture', startFrame: 30, endFrame: 60 }],
  intents: { '90': 'synchronized' },
  customDisclosure: { owner: 'app', retained: true },
};

const baseConfig: TimelineConfig = {
  output: { resolution: '1280x720', fps: 30, file: 'timeline.mp4' },
  tracks: [{ id: 'picture', kind: 'visual', label: 'Picture' }],
  clips: [],
  app: {
    opaqueAppData: { keep: ['this'] },
    visualSeamContract: authoredContract,
  },
};

function acknowledgedConfig(contract: Record<string, unknown>): ResolvedTimelineConfig {
  return {
    ...baseConfig,
    tracks: baseConfig.tracks ?? [],
    registry: {},
    app: {
      ...baseConfig.app,
      visualSeamContract: contract,
    },
  };
}

describe('ordinary visual seam acknowledgement persistence', () => {
  it('does not issue a snapshot save when only the derived report changes', () => {
    const current: TimelineConfig = {
      ...baseConfig,
      app: {
        ...baseConfig.app,
        visualSeamContract: {
          ...authoredContract,
          report: { version: 1, warningCount: 1, blocked: true },
        },
      },
    };
    const acknowledged = acknowledgedConfig({
      ...authoredContract,
      report: { version: 1, warningCount: 0, blocked: false },
    });
    const saveSnapshot = vi.fn();
    const prepared = prepareVisualSeamSnapshotConfig(current, acknowledged);
    if (prepared) saveSnapshot(prepared);

    expect(prepared).toBeNull();
    expect(saveSnapshot).not.toHaveBeenCalled();
    expect(current.app?.visualSeamContract).toMatchObject({
      report: { warningCount: 1, blocked: true },
    });
    expect(acknowledged.app?.visualSeamContract).toMatchObject({
      report: { warningCount: 0, blocked: false },
    });
  });

  it('saves authored seam changes while preserving opaque app data and omitting the report', () => {
    const acknowledged = acknowledgedConfig({
      ...authoredContract,
      intents: { ...authoredContract.intents, '120': 'hard-cut' },
      report: { version: 1, warningCount: 0, blocked: false },
    });

    const prepared = prepareVisualSeamSnapshotConfig(baseConfig, acknowledged);

    expect(prepared).not.toBeNull();
    expect(prepared?.app?.opaqueAppData).toEqual({ keep: ['this'] });
    expect(prepared?.app?.visualSeamContract).toEqual({
      ...authoredContract,
      intents: { ...authoredContract.intents, '120': 'hard-cut' },
    });
    expect(prepared?.app?.visualSeamContract).not.toHaveProperty('report');
  });

  it('preserves an existing opaque legacy report when authored seam data changes', () => {
    const legacyReport = {
      version: 1,
      warningCount: 1,
      blocked: true,
      opaqueDiagnostic: { source: 'legacy', code: 'SEAM-001' },
    };
    const current: TimelineConfig = {
      ...baseConfig,
      app: {
        ...baseConfig.app,
        visualSeamContract: { ...authoredContract, report: legacyReport },
      },
    };
    const acknowledged = acknowledgedConfig({
      ...authoredContract,
      intents: { ...authoredContract.intents, '120': 'hard-cut' },
      report: { version: 1, warningCount: 0, blocked: false },
    });

    const prepared = prepareVisualSeamSnapshotConfig(current, acknowledged);

    expect(prepared?.app?.visualSeamContract).toMatchObject({
      ...authoredContract,
      intents: { ...authoredContract.intents, '120': 'hard-cut' },
      report: legacyReport,
    });
    expect(prepared?.app?.visualSeamContract?.report).toEqual(legacyReport);
    expect(prepared?.app?.visualSeamContract?.report).not.toEqual(acknowledged.app?.visualSeamContract?.report);
  });
});
