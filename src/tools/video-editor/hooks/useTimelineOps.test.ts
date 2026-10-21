// @vitest-environment jsdom
/**
 * useTimelineOps — host adapter tests.
 *
 * These tests cover the native commitData/history path for operations awaiting
 * command migration. Track-label command routing has its own adjacent suite.
 */
import { act, renderHook } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { useTimelineOps } from './useTimelineOps';
import { configToRows, type TimelineData } from '../lib/timeline-data';
import { createTimelineReader } from '../lib/timeline-reader';
import { createProposalRuntime } from '../lib/proposal-runtime';
import { getConfigSignature, getStableConfigSignature } from '../lib/config-utils';
import type { TimelineConfig } from '../types';
import type { Checkpoint } from '../types/history';
import type {
  TimelineDiff,
  TimelinePatch,
  TimelinePatchValidationResult,
  TimelinePreviewResult,
} from '@/sdk/video/timeline/patch.ts';
import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { GenericPatchCapturePort, GenericPatchBasis } from '../commands/genericPatchCapture.ts';

// ---------------------------------------------------------------------------
// Fixture helpers
// ---------------------------------------------------------------------------

function makeBaseTimelineData(overrides: Partial<TimelineConfig> = {}): TimelineData {
  const config: TimelineConfig = {
    output: { resolution: '1920x1080', fps: 30, file: 'out.mp4' },
    tracks: [
      { id: 'V1', kind: 'visual', label: 'V1' },
      { id: 'A1', kind: 'audio', label: 'A1', muted: false },
    ],
    clips: [
      {
        id: 'clip-1',
        at: 0,
        track: 'V1',
        clipType: 'hold',
        hold: 3,
      },
    ],
    ...overrides,
  };

  const rowData = configToRows(config);
  const resolvedConfig = {
    output: { ...config.output },
    tracks: (config.tracks ?? []).map((t) => ({ ...t })),
    clips: config.clips.map((clip) => ({ ...clip, assetEntry: undefined })),
    registry: {},
    theme: config.theme,
    theme_overrides: config.theme_overrides,
    generation_defaults: config.generation_defaults,
  };

  return {
    config,
    configVersion: 1,
    registry: { assets: {} },
    resolvedConfig,
    rows: rowData.rows,
    meta: rowData.meta,
    effects: rowData.effects,
    assetMap: {},
    output: { ...config.output },
    tracks: (config.tracks ?? []).map((t) => ({ ...t })),
    clipOrder: rowData.clipOrder,
    signature: getConfigSignature(resolvedConfig),
    stableSignature: getStableConfigSignature(config, { assets: {} }),
  };
}

// ---------------------------------------------------------------------------
// Test suite
// ---------------------------------------------------------------------------

describe('useTimelineOps', () => {
  it('keeps an extension-retained adapter on the current command port after startup', () => {
    const dataRef = { current: makeBaseTimelineData() };
    const commitData = vi.fn();
    const patch: TimelinePatch = { version: 1, operations: [
      { op: 'clip.move', target: 'clip-1', payload: { at: 1 } },
      { op: 'clip.update', target: 'clip-1', payload: { hold: 5 } },
    ] };
    const preview: TimelinePatch = { ...patch, source: 'timeline.native-ordinary' };
    const port = {
      capture: vi.fn(() => ({})),
      finish: vi.fn(() => ({ commands: [], preview })),
      submit: vi.fn(),
    } as unknown as GenericPatchCapturePort;
    const checkpoint = vi.fn();
    const rollback = vi.fn();
    const { result, rerender } = renderHook(({ genericPatchPort }) => useTimelineOps({
      dataRef, commitData, genericPatchPort,
      createManualCheckpoint: checkpoint, jumpToCheckpoint: rollback, checkpoints: [],
    }), { initialProps: { genericPatchPort: undefined as GenericPatchCapturePort | undefined } });
    // Extension activation retains this object while command-session startup is asynchronous.
    const retained = result.current;
    rerender({ genericPatchPort: port });
    act(() => { retained.apply(patch); });

    expect(port.capture).toHaveBeenCalledWith({ patch, current: dataRef.current });
    expect(port.finish).toHaveBeenCalledOnce();
    expect(port.submit).toHaveBeenCalledWith({ commands: [], preview });
    expect(commitData).not.toHaveBeenCalled();
    expect(result.current).toBe(retained);
  });

  it('uses current authority and preserves capture refusal through a retained adapter', () => {
    const dataRef = { current: makeBaseTimelineData() };
    const commitData = vi.fn();
    const patch: TimelinePatch = { version: 1, operations: [
      { op: 'clip.move', target: 'clip-1', payload: { at: 1 } },
    ] };
    const port = {
      capture: vi.fn(() => { throw new Error('Displayed timeline does not match the raw authoring basis'); }),
      finish: vi.fn(), submit: vi.fn(),
    } as unknown as GenericPatchCapturePort;
    const { result, rerender } = renderHook(({ allowed }) => useTimelineOps({
      dataRef, commitData, genericPatchPort: port,
      editability: { checkTimeline: () => ({ allowed, reason: 'read_only' }) } as any,
      createManualCheckpoint: vi.fn(), jumpToCheckpoint: vi.fn(), checkpoints: [],
    }), { initialProps: { allowed: true } });
    const retained = result.current;
    expect(() => retained.apply(patch)).toThrow('Displayed timeline does not match the raw authoring basis');
    expect(port.finish).not.toHaveBeenCalled();
    expect(port.submit).not.toHaveBeenCalled();
    expect(commitData).not.toHaveBeenCalled();

    vi.mocked(port.capture).mockClear();
    rerender({ allowed: false });
    expect(() => retained.apply(patch)).toThrow('timeline edit denied');
    expect(port.capture).not.toHaveBeenCalled();
    expect(commitData).not.toHaveBeenCalled();
  });

  it('routes a complete native patch through one command-session port', () => {
    const dataRef = { current: makeBaseTimelineData() };
    const commitData = vi.fn();
    const preview: TimelinePatch = {
      version: 1,
      source: 'timeline.native-label-hold',
      operations: [{ op: 'track.update', target: 'V1', payload: { label: 'Native label' } }],
    };
    const genericPatchPort = {
      capture: vi.fn(() => ({})),
      finish: vi.fn(() => ({ commands: [], preview })),
      submit: vi.fn(),
    } as unknown as GenericPatchCapturePort;
    const { result } = renderHook(() => useTimelineOps({
      dataRef,
      commitData,
      genericPatchPort,
      createManualCheckpoint: vi.fn(),
      jumpToCheckpoint: vi.fn(),
      checkpoints: [],
    }));

    const diff = result.current.apply({
      version: 1,
      operations: [{ op: 'track.update', target: 'V1', payload: { label: 'Native label' } }],
    });

    expect(genericPatchPort.capture).toHaveBeenCalledOnce();
    expect(genericPatchPort.finish).toHaveBeenCalledOnce();
    expect(genericPatchPort.submit).toHaveBeenCalledWith({ commands: [], preview });
    expect(commitData).not.toHaveBeenCalled();
    expect(diff.entries).toEqual(expect.arrayContaining([
      expect.objectContaining({ target: 'V1' }),
    ]));
  });

  it('accepts a supported proposal through one native batch without snapshot traffic', () => {
    const dataRef = { current: makeBaseTimelineData() };
    const commitData = vi.fn();
    const patch: TimelinePatch = {
      version: 1,
      source: 'agent.proposal',
      meta: { group_id: 'proposal-group', intent: 'preserve-order' },
      operations: [
        { op: 'clip.update', target: 'clip-1', payload: { hold: 4 }, order: 0 },
        { op: 'track.update', target: 'V1', payload: { label: 'Picture' }, order: 1 },
      ],
    };
    const command = {
      schema_version: 1,
      op: 'clip.set',
      version: '1',
      select: 'parent/clip:clip-1',
      args: { values: { hold: 4 }, clear: [] },
    } as EditCommand;
    const preview: TimelinePatch = {
      version: 1,
      source: 'timeline.native-ordinary',
      operations: patch.operations,
    };
    const genericPatchPort = {
      capture: vi.fn((input: { patch: TimelinePatch; current: TimelineData }) => ({
        current: input.current,
        capture: {},
      } as unknown as GenericPatchBasis)),
      finish: vi.fn(() => ({ commands: [command], preview })),
      submit: vi.fn(),
    } as unknown as GenericPatchCapturePort;
    const { result } = renderHook(() => useTimelineOps({
      dataRef,
      commitData,
      genericPatchPort,
      createManualCheckpoint: vi.fn(),
      jumpToCheckpoint: vi.fn(),
      checkpoints: [],
    }));
    const proposalRuntime = createProposalRuntime({
      timelineOps: result.current,
      reader: createTimelineReader({ data: dataRef.current! }),
    });
    const proposal = proposalRuntime.create({
      source: 'agent.proposal',
      patch,
      baseVersion: 1,
    });

    expect(proposalRuntime.accept(proposal.id).entries).toEqual(expect.arrayContaining([
      expect.objectContaining({ target: 'clip-1' }),
      expect.objectContaining({ target: 'V1' }),
    ]));
    expect(genericPatchPort.capture).toHaveBeenCalledWith({ patch, current: dataRef.current });
    expect(genericPatchPort.finish).toHaveBeenCalledOnce();
    expect(genericPatchPort.submit).toHaveBeenCalledWith({ commands: [command], preview });
    expect(proposalRuntime.get(proposal.id)?.state).toBe('accepted');
    expect(commitData).not.toHaveBeenCalled();
  });

  it('refuses a mixed proposal atomically and preserves its draft without snapshot traffic', () => {
    const dataRef = { current: makeBaseTimelineData() };
    const commitData = vi.fn();
    const patch: TimelinePatch = {
      version: 1,
      source: 'agent.proposal',
      operations: [
        { op: 'clip.update', target: 'clip-1', payload: { hold: 4 }, order: 0 },
        { op: 'project-data.write', target: 'com.example.producer', payload: { key: 'source', value: 'draft' }, order: 1 },
      ],
    };
    const genericPatchPort = {
      capture: vi.fn(() => { throw new Error('mixed native batch refused'); }),
      finish: vi.fn(),
      submit: vi.fn(),
    } as unknown as GenericPatchCapturePort;
    const { result } = renderHook(() => useTimelineOps({
      dataRef,
      commitData,
      genericPatchPort,
      createManualCheckpoint: vi.fn(),
      jumpToCheckpoint: vi.fn(),
      checkpoints: [],
    }));
    const proposalRuntime = createProposalRuntime({
      timelineOps: result.current,
      reader: createTimelineReader({ data: dataRef.current! }),
    });
    const proposal = proposalRuntime.create({ source: 'agent.proposal', patch, baseVersion: 1 });

    expect(() => proposalRuntime.accept(proposal.id)).toThrow('mixed native batch refused');
    expect(proposalRuntime.get(proposal.id)?.state).toBe('pending');
    expect(genericPatchPort.capture).toHaveBeenCalledOnce();
    expect(genericPatchPort.finish).not.toHaveBeenCalled();
    expect(genericPatchPort.submit).not.toHaveBeenCalled();
    expect(commitData).not.toHaveBeenCalled();
  });

  it('keeps standalone compiler data on the guarded snapshot path', () => {
    const dataRef = { current: makeBaseTimelineData() };
    const commitData = vi.fn();
    const genericPatchPort = {
      capture: vi.fn(),
      finish: vi.fn(),
      submit: vi.fn(),
    } as unknown as GenericPatchCapturePort;
    const { result } = renderHook(() => useTimelineOps({
      dataRef,
      commitData,
      genericPatchPort,
      createManualCheckpoint: vi.fn(),
      jumpToCheckpoint: vi.fn(),
      checkpoints: [],
    }));

    act(() => result.current.apply({
      version: 1,
      operations: [{
        op: 'project-data.write',
        target: 'com.example.compiler-canary',
        payload: { key: 'source', value: { dsl: 'clip x' } },
      }],
    }));

    expect(genericPatchPort.capture).not.toHaveBeenCalled();
    expect(genericPatchPort.finish).not.toHaveBeenCalled();
    expect(genericPatchPort.submit).not.toHaveBeenCalled();
    expect(commitData).toHaveBeenCalledWith(expect.anything(), { save: true, semantic: true });
  });

  it('keeps a standalone legacy cross-track move on the guarded snapshot path', () => {
    const dataRef = { current: makeBaseTimelineData() };
    const commitData = vi.fn();
    const genericPatchPort = {
      capture: vi.fn(),
      finish: vi.fn(),
      submit: vi.fn(),
    } as unknown as GenericPatchCapturePort;
    const { result } = renderHook(() => useTimelineOps({
      dataRef,
      commitData,
      genericPatchPort,
      createManualCheckpoint: vi.fn(),
      jumpToCheckpoint: vi.fn(),
      checkpoints: [],
    }));

    act(() => result.current.apply({
      version: 1,
      operations: [{ op: 'clip.move', target: 'clip-1', payload: { track: 'A1', at: 2 } }],
    }));

    expect(genericPatchPort.capture).not.toHaveBeenCalled();
    expect(genericPatchPort.finish).not.toHaveBeenCalled();
    expect(genericPatchPort.submit).not.toHaveBeenCalled();
    expect(commitData).toHaveBeenCalledWith(expect.anything(), { save: true, semantic: true });
  });

  it('keeps a legacy cross-track move-and-hold batch on the guarded snapshot path', () => {
    const dataRef = { current: makeBaseTimelineData() };
    const commitData = vi.fn();
    const genericPatchPort = {
      capture: vi.fn(),
      finish: vi.fn(),
      submit: vi.fn(),
    } as unknown as GenericPatchCapturePort;
    const { result } = renderHook(() => useTimelineOps({
      dataRef,
      commitData,
      genericPatchPort,
      createManualCheckpoint: vi.fn(),
      jumpToCheckpoint: vi.fn(),
      checkpoints: [],
    }));

    act(() => result.current.apply({
      version: 1,
      operations: [
        { op: 'clip.move', target: 'clip-1', payload: { track: 'A1', at: 2 } },
        { op: 'clip.update', target: 'clip-1', payload: { hold: 2, mode: 'merge' } },
      ],
    }));

    expect(genericPatchPort.capture).not.toHaveBeenCalled();
    expect(genericPatchPort.finish).not.toHaveBeenCalled();
    expect(genericPatchPort.submit).not.toHaveBeenCalled();
    expect(commitData).toHaveBeenCalledTimes(1);
    expect(commitData).toHaveBeenCalledWith(expect.anything(), { save: true, semantic: true });
  });

  describe('flush — durable host acknowledgement', () => {
    it('keeps apply synchronous and awaits exactly the host barrier receipt', async () => {
      let acknowledge!: (version: number) => void;
      const receipt = new Promise<number>((resolve) => { acknowledge = resolve; });
      const flushPendingSave = vi.fn(() => receipt);
      const commitData = vi.fn();
      const { result } = renderHook(() => useTimelineOps({
        dataRef: { current: makeBaseTimelineData() },
        commitData,
        flushPendingSave,
        createManualCheckpoint: vi.fn(),
        jumpToCheckpoint: vi.fn(),
        checkpoints: [],
      }));

      const diff = result.current.apply({
        version: 1,
        operations: [{ op: 'track.update', target: 'A1', payload: { muted: true } }],
      });
      expect(diff).not.toBeInstanceOf(Promise);
      expect(commitData).toHaveBeenCalledWith(expect.anything(), { save: true, semantic: true });
      expect(flushPendingSave).not.toHaveBeenCalled();

      let settled = false;
      const flushed = result.current.flush().then((ack) => { settled = true; return ack; });
      expect(flushPendingSave).toHaveBeenCalledTimes(1);
      await Promise.resolve();
      expect(settled).toBe(false);
      acknowledge(7);
      const ack = await flushed;
      expect(ack).toEqual({ version: 7 });
      expect(Object.isFrozen(ack)).toBe(true);
      expect(commitData).toHaveBeenCalledTimes(1);
    });

    it('rejects unloaded data, absent persistence, and the host failure without inventing a receipt', async () => {
      const dataRef: { current: TimelineData | null } = { current: makeBaseTimelineData() };
      const args = { dataRef, commitData: vi.fn(), createManualCheckpoint: vi.fn(), jumpToCheckpoint: vi.fn(), checkpoints: [] };
      const { result, rerender } = renderHook(
        ({ barrier }: { barrier?: () => Promise<number> }) => useTimelineOps({ ...args, flushPendingSave: barrier }),
        { initialProps: { barrier: undefined as (() => Promise<number>) | undefined } },
      );
      const adapter = result.current;
      await expect(adapter.flush()).rejects.toThrow('durable persistence is unavailable');
      const failure = new Error('write acknowledgement unavailable; remote outcome unknown');
      const barrier = vi.fn(() => Promise.reject(failure));
      rerender({ barrier });
      expect(result.current).toBe(adapter);
      await expect(adapter.flush()).rejects.toBe(failure);
      dataRef.current = null;
      await expect(adapter.flush()).rejects.toThrow('timeline data is not yet loaded');
      expect(barrier).toHaveBeenCalledTimes(1);
    });
  });

  // -----------------------------------------------------------------------
  // Atomic apply through native commitData
  // -----------------------------------------------------------------------
  describe('apply — atomic commit through native commitData', () => {
    it('commits exactly once with semantic:true and save:true', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let diff: TimelineDiff | undefined;
      act(() => {
        diff = result.current.apply({
          version: 1,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-new',
              payload: { track: 'V1', at: 3, clipType: 'hold', hold: 2 },
            },
          ],
        });
      });

      // Assert: commitData called exactly once
      expect(commitData).toHaveBeenCalledTimes(1);

      // Assert: called with semantic:true and save:true
      const callArgs = commitData.mock.calls[0];
      expect(callArgs[0]).toBeDefined(); // nextData
      expect(callArgs[1]).toMatchObject({ save: true, semantic: true });

      // Assert: diff is returned with entries
      expect(diff).toBeDefined();
      expect(diff!.entries.length).toBeGreaterThan(0);
    });

    it('throws and does NOT call commitData when validation fails', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      expect(() =>
        act(() =>
          result.current.apply({
            version: 1,
            operations: [
              // Invalid: track.add requires kind
              { op: 'track.add' as any, target: 'T1', payload: {} },
            ],
          }),
        ),
      ).toThrow();

      // commitData must NOT have been called
      expect(commitData).not.toHaveBeenCalled();
    });

    it('throws and does NOT call commitData when data is not yet loaded', () => {
      const commitData = vi.fn();
      const dataRef = { current: null as TimelineData | null };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      expect(() =>
        act(() =>
          result.current.apply({
            version: 1,
            operations: [
              {
                op: 'clip.add',
                target: 'clip-x',
                payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
              },
            ],
          }),
        ),
      ).toThrow('TimelineOps.apply: timeline data is not yet loaded.');

      expect(commitData).not.toHaveBeenCalled();
    });

    it('the native commitData receives the compiled nextData (not a clone of the original)', () => {
      const commitData = vi.fn();
      const original = makeBaseTimelineData();
      const dataRef = { current: original };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      act(() =>
        result.current.apply({
          version: 1,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-new',
              payload: { track: 'V1', at: 0, clipType: 'hold', hold: 5 },
            },
          ],
        }),
      );

      const committedData = commitData.mock.calls[0][0] as TimelineData;
      // The committed data must have the new clip
      expect(committedData.config.clips.some((c) => c.id === 'clip-new')).toBe(
        true,
      );
      // The original dataRef must not have been mutated by apply (commitData
      // is what updates dataRef in the real pipeline — the test mock doesn't
      // do that, so original stays unchanged)
      expect(original.config.clips.some((c) => c.id === 'clip-new')).toBe(
        false,
      );
      // Verify the committed data is distinct from the original
      expect(committedData).not.toBe(original);
    });
  });

  // -----------------------------------------------------------------------
  // Failed-batch no-op (validation rejects entire batch atomically)
  // -----------------------------------------------------------------------
  describe('apply — failed batch is a full no-op', () => {
    it('rejects the entire batch when any operation is invalid', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      // Batch with one valid and one invalid op
      expect(() =>
        act(() =>
          result.current.apply({
            version: 1,
            operations: [
              {
                op: 'clip.add',
                target: 'clip-ok',
                payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
              },
              { op: 'track.add' as any, target: 'T1', payload: {} }, // invalid
            ],
          }),
        ),
      ).toThrow();

      // Entire batch rejected — commitData never called
      expect(commitData).not.toHaveBeenCalled();
      // Original data unchanged
      expect(dataRef.current!.config.clips).toHaveLength(1);
    });

    it('rejects a batch with an unknown operation family', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      expect(() =>
        act(() =>
          result.current.apply({
            version: 1,
            operations: [
              { op: 'nonexistent.op' as any, target: 'x', payload: {} },
            ],
          }),
        ),
      ).toThrow();

      expect(commitData).not.toHaveBeenCalled();
    });
  });

  // -----------------------------------------------------------------------
  // Undo/redo through native history
  // -----------------------------------------------------------------------
  describe('undo/redo — native history integration', () => {
    it('a single apply call produces one undo stack entry via native onBeforeCommit', () => {
      // Real pipeline: useTimelineCommit wires onBeforeCommit via
      // TimelineEventBus.  We test that apply() calls commitData with
      // semantic:true AND skipHistory is NOT set, which means the native
      // history layer will record an undo entry.

      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      act(() =>
        result.current.apply({
          version: 1,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-x',
              payload: { track: 'V1', at: 3, clipType: 'hold', hold: 2 },
            },
          ],
        }),
      );

      // skipHistory must NOT be true — the native history layer needs to
      // record the undo entry.
      const options = commitData.mock.calls[0][1];
      expect(options.skipHistory).not.toBe(true);
    });

    it('consecutive apply calls each go through the native commit path', () => {
      const appliedData: TimelineData[] = [];
      const commitData = vi.fn((nextData: TimelineData) => {
        appliedData.push(nextData);
        // Simulate the real commitData: update dataRef
        dataRef.current = nextData;
      });
      const dataRef = { current: makeBaseTimelineData() as TimelineData | null };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      // First apply: add clip-a
      act(() =>
        result.current.apply({
          version: 1,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-a',
              payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
            },
          ],
        }),
      );

      // Second apply: add clip-b
      act(() =>
        result.current.apply({
          version: 1,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-b',
              payload: { track: 'V1', at: 5, clipType: 'hold', hold: 2 },
            },
          ],
        }),
      );

      expect(commitData).toHaveBeenCalledTimes(2);

      // Both calls carry semantic:true
      for (const call of commitData.mock.calls) {
        expect(call[1]).toMatchObject({ save: true, semantic: true });
      }

      // dataRef should now have three clips (original + clip-a + clip-b)
      expect(dataRef.current!.config.clips).toHaveLength(3);
    });
  });

  // -----------------------------------------------------------------------
  // Checkpoint
  // -----------------------------------------------------------------------
  describe('checkpoint', () => {
    it('delegates to native createManualCheckpoint with the label', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let checkpointId: string;
      act(() => {
        checkpointId = result.current.checkpoint('my-label');
      });

      // Returns a non-empty ID
      expect(checkpointId!).toBeTruthy();
      expect(typeof checkpointId!).toBe('string');

      // Delegates to native createManualCheckpoint
      expect(createManualCheckpoint).toHaveBeenCalledWith('my-label');
    });

    it('generates a default label when none is provided', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      act(() => {
        result.current.checkpoint();
      });

      expect(createManualCheckpoint).toHaveBeenCalledTimes(1);
      const labelArg = createManualCheckpoint.mock.calls[0][0];
      expect(labelArg).toContain('Patch checkpoint');
    });

    it('returns a stable ID that can be used for rollback', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let id1: string, id2: string;
      act(() => {
        id1 = result.current.checkpoint('alpha');
        id2 = result.current.checkpoint('beta');
      });

      // IDs must be distinct
      expect(id1!).not.toBe(id2!);
      // Both non-empty
      expect(id1!.length).toBeGreaterThan(0);
      expect(id2!.length).toBeGreaterThan(0);
    });
  });

  // -----------------------------------------------------------------------
  // Rollback
  // -----------------------------------------------------------------------
  describe('rollback', () => {
    it('delegates to native jumpToCheckpoint when an exact ID match exists', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [
        {
          id: 'ckpt-1',
          timelineId: 'tl-1',
          config: dataRef.current!.config,
          createdAt: new Date().toISOString(),
          triggerType: 'manual',
          label: 'Manual checkpoint',
          editsSinceLastCheckpoint: 0,
        },
      ];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let diff;
      act(() => {
        diff = result.current.rollback('ckpt-1');
      });

      // Delegates to native jumpToCheckpoint
      expect(jumpToCheckpoint).toHaveBeenCalledWith('ckpt-1');
      // Returns a diff
      expect(diff).not.toBeNull();
      expect(diff!.entries.length).toBeGreaterThanOrEqual(0);
    });

    it('resolves a client-generated checkpoint ID via label-based fallback', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [
        {
          id: 'backend-ckpt-1',
          timelineId: 'tl-1',
          config: dataRef.current!.config,
          createdAt: new Date().toISOString(),
          triggerType: 'manual',
          label: 'My saved checkpoint',
          editsSinceLastCheckpoint: 0,
        },
      ];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      // First, create a checkpoint to register the label mapping
      let clientId: string;
      act(() => {
        clientId = result.current.checkpoint('My saved checkpoint');
      });

      // Now the pendingLabels map has clientId → 'My saved checkpoint'.
      // When we rollback with clientId, it should resolve to 'backend-ckpt-1'.
      act(() => {
        result.current.rollback(clientId!);
      });

      expect(jumpToCheckpoint).toHaveBeenCalledWith('backend-ckpt-1');
    });

    it('returns null when the checkpoint ID cannot be resolved', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let diff;
      act(() => {
        diff = result.current.rollback('nonexistent-ckpt');
      });

      expect(diff).toBeNull();
      expect(jumpToCheckpoint).not.toHaveBeenCalled();
    });
  });

  // -----------------------------------------------------------------------
  // setAllTracksMuted
  // -----------------------------------------------------------------------
  describe('setAllTracksMuted', () => {
    it('delegates to apply(), which commits through native commitData', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      act(() => {
        result.current.setAllTracksMuted(true);
      });

      // Must call commitData through apply()
      expect(commitData).toHaveBeenCalledTimes(1);
      expect(commitData.mock.calls[0][1]).toMatchObject({
        save: true,
        semantic: true,
      });
    });

    it('returns an empty diff when there are no audio tracks', () => {
      const commitData = vi.fn();
      // Timeline with only visual tracks (no audio)
      const data = makeBaseTimelineData({
        tracks: [{ id: 'V1', kind: 'visual', label: 'V1' }],
      });
      const dataRef = { current: data };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let diff;
      act(() => {
        diff = result.current.setAllTracksMuted(true);
      });

      expect(diff!.entries).toHaveLength(0);
      expect(diff!.affectedObjectIds).toHaveLength(0);
      // No commitData because apply was never called
      expect(commitData).not.toHaveBeenCalled();
    });

    it('throws when data is not yet loaded', () => {
      const commitData = vi.fn();
      const dataRef = { current: null as TimelineData | null };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      expect(() =>
        act(() => {
          result.current.setAllTracksMuted(true);
        }),
      ).toThrow('TimelineOps.setAllTracksMuted: timeline data is not yet loaded.');
    });
  });

  describe('whole-timeline editability guard', () => {
    const deniedEditability = {
      check: () => ({ allowed: false as const, reason: 'timeline_read_only' as const }),
      checkTimeline: () => ({ allowed: false as const, reason: 'timeline_read_only' as const }),
    };

    it('rejects apply before commit and leaves the input snapshot unchanged', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const before = structuredClone(dataRef.current);
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const { result } = renderHook(() => useTimelineOps({
        commitData,
        dataRef,
        createManualCheckpoint,
        jumpToCheckpoint,
        checkpoints: [],
        editability: deniedEditability,
      }));

      expect(() => result.current.apply({
        version: 1,
        operations: [{
          op: 'clip.add',
          target: 'blocked-clip',
          payload: { track: 'V1', at: 3, clipType: 'hold', hold: 1 },
        }],
      })).toThrow('TimelineOps.apply: timeline edit denied (timeline_read_only).');
      expect(commitData).not.toHaveBeenCalled();
      expect(createManualCheckpoint).not.toHaveBeenCalled();
      expect(jumpToCheckpoint).not.toHaveBeenCalled();
      expect(dataRef.current).toEqual(before);
    });

    it('rejects checkpoint before registering or persisting it', () => {
      const dataRef = { current: makeBaseTimelineData() };
      const before = structuredClone(dataRef.current);
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const { result } = renderHook(() => useTimelineOps({
        commitData: vi.fn(),
        dataRef,
        createManualCheckpoint,
        jumpToCheckpoint,
        checkpoints: [],
        editability: deniedEditability,
      }));

      expect(() => result.current.checkpoint('blocked')).toThrow(
        'TimelineOps.checkpoint: timeline edit denied (timeline_read_only).',
      );
      expect(createManualCheckpoint).not.toHaveBeenCalled();
      expect(jumpToCheckpoint).not.toHaveBeenCalled();
      expect(dataRef.current).toEqual(before);
    });

    it('rejects rollback before resolving or jumping to a checkpoint', () => {
      const dataRef = { current: makeBaseTimelineData() };
      const before = structuredClone(dataRef.current);
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [{
        id: 'blocked-checkpoint',
        timelineId: 'tl-1',
        config: dataRef.current.config,
        createdAt: new Date().toISOString(),
        triggerType: 'manual',
        label: 'Blocked',
        editsSinceLastCheckpoint: 0,
      }];
      const { result } = renderHook(() => useTimelineOps({
        commitData: vi.fn(),
        dataRef,
        createManualCheckpoint,
        jumpToCheckpoint,
        checkpoints,
        editability: deniedEditability,
      }));

      expect(() => result.current.rollback('blocked-checkpoint')).toThrow(
        'TimelineOps.rollback: timeline edit denied (timeline_read_only).',
      );
      expect(createManualCheckpoint).not.toHaveBeenCalled();
      expect(jumpToCheckpoint).not.toHaveBeenCalled();
      expect(dataRef.current).toEqual(before);
    });

    it('rejects setAllTracksMuted through guarded apply without committing', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const before = structuredClone(dataRef.current);
      const { result } = renderHook(() => useTimelineOps({
        commitData,
        dataRef,
        createManualCheckpoint: vi.fn(),
        jumpToCheckpoint: vi.fn(),
        checkpoints: [],
        editability: deniedEditability,
      }));

      expect(() => result.current.setAllTracksMuted(true)).toThrow(
        'TimelineOps.apply: timeline edit denied (timeline_read_only).',
      );
      expect(commitData).not.toHaveBeenCalled();
      expect(dataRef.current).toEqual(before);
    });

    it('keeps validate and preview available while edits are denied', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const before = structuredClone(dataRef.current);
      const patch = {
        version: 1,
        operations: [{
          op: 'clip.add' as const,
          target: 'preview-only',
          payload: { track: 'V1', at: 3, clipType: 'hold', hold: 1 },
        }],
      };
      const { result } = renderHook(() => useTimelineOps({
        commitData,
        dataRef,
        createManualCheckpoint: vi.fn(),
        jumpToCheckpoint: vi.fn(),
        checkpoints: [],
        editability: deniedEditability,
      }));

      expect(result.current.validate(patch).valid).toBe(true);
      expect(result.current.preview(patch).fullyPreviewable).toBe(true);
      expect(commitData).not.toHaveBeenCalled();
      expect(dataRef.current).toEqual(before);
    });
  });

  // -----------------------------------------------------------------------
  // Preview (read-only, no commit)
  // -----------------------------------------------------------------------
  describe('preview', () => {
    it('returns a preview result without calling commitData', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let previewResult;
      act(() => {
        previewResult = result.current.preview({
          version: 1,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-p',
              payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
            },
          ],
        });
      });

      expect(previewResult).toBeDefined();
      expect(previewResult!.diff).toBeDefined();
      // preview is read-only — no commit
      expect(commitData).not.toHaveBeenCalled();
      // Original data unchanged
      expect(dataRef.current!.config.clips).toHaveLength(1);
    });

    it('returns an error diagnostic when data is not yet loaded', () => {
      const commitData = vi.fn();
      const dataRef = { current: null as TimelineData | null };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let previewResult;
      act(() => {
        previewResult = result.current.preview({
          version: 1,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-x',
              payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
            },
          ],
        });
      });

      expect(previewResult!.fullyPreviewable).toBe(false);
      expect(previewResult!.diagnostics).toHaveLength(1);
      expect(previewResult!.diagnostics[0].code).toBe('timeline-patch/no-data');
    });
  });

  // -----------------------------------------------------------------------
  // Validate (pure, no side effects)
  // -----------------------------------------------------------------------
  describe('validate', () => {
    it('returns validation result without touching dataRef or commitData', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let validationResult;
      act(() => {
        validationResult = result.current.validate({
          version: 1,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-v',
              payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
            },
          ],
        });
      });

      expect(validationResult!.valid).toBe(true);
      expect(commitData).not.toHaveBeenCalled();
      expect(dataRef.current!.config.clips).toHaveLength(1);
    });
  });

  // -----------------------------------------------------------------------
  // Adapter stability
  // -----------------------------------------------------------------------
  describe('adapter stability', () => {
    it('returns the same object reference across re-renders with stable deps', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result, rerender } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      const first = result.current;

      // Re-render with same deps
      rerender();

      expect(result.current).toBe(first);
    });

    it('reads the latest dataRef.current on every call without adapter recreation', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      const adapter = result.current;

      // Mutate dataRef behind the scenes (simulating a provider update)
      // Add an external clip, then add a new track
      const newData = makeBaseTimelineData({
        tracks: [
          { id: 'V1', kind: 'visual', label: 'V1' },
          { id: 'A1', kind: 'audio', label: 'A1' },
          { id: 'V2', kind: 'visual', label: 'V2' },
        ],
        clips: [
          ...dataRef.current!.config.clips,
          {
            id: 'clip-external',
            at: 10,
            track: 'V2',
            clipType: 'hold',
            hold: 2,
          },
        ],
      });
      dataRef.current = newData;

      // Preview a clip.add operation against the updated dataRef
      let previewResult: TimelinePreviewResult | undefined;
      act(() => {
        previewResult = adapter.preview({
          version: 1,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-preview',
              payload: { track: 'V2', at: 12, clipType: 'hold', hold: 1 },
            },
          ],
        });
      });

      // Preview should reflect the new data — the diff should include
      // the new clip and the track it's on.
      expect(previewResult!.diff.affectedObjectIds).toContain('clip-preview');
      expect(previewResult!.diff.affectedObjectIds).toContain('V2');
      // The pre-existing clip-external on V2 should not be in affectedIds
      // (only the newly added clip and its track are affected).
    });
  });

  // -----------------------------------------------------------------------
  // Base-version staleness (T13)
  // -----------------------------------------------------------------------
  describe('apply — base-version staleness rejection', () => {
    it('rejects a stale patch when patch.version !== dataRef.current.configVersion', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      expect(() =>
        act(() =>
          result.current.apply({
            version: 5,
            operations: [
              {
                op: 'clip.add',
                target: 'clip-stale',
                payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
              },
            ],
          }),
        ),
      ).toThrow();

      expect(commitData).not.toHaveBeenCalled();
    });

    it('rejects a stale patch when patch.version is behind configVersion', () => {
      const commitData = vi.fn();
      const data = makeBaseTimelineData();
      (data as any).configVersion = 5;
      const dataRef = { current: data };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      expect(() =>
        act(() =>
          result.current.apply({
            version: 1,
            operations: [
              {
                op: 'clip.add',
                target: 'clip-stale',
                payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
              },
            ],
          }),
        ),
      ).toThrow();

      expect(commitData).not.toHaveBeenCalled();
    });

    it('throws TimelineVersionConflictError with a descriptive message', () => {
      const commitData = vi.fn();
      const data = makeBaseTimelineData();
      (data as any).configVersion = 3;
      const dataRef = { current: data };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let caught: unknown;
      try {
        act(() =>
          result.current.apply({
            version: 7,
            operations: [
              {
                op: 'clip.add',
                target: 'clip-x',
                payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
              },
            ],
          }),
        );
      } catch (e) {
        caught = e;
      }

      expect(caught).toBeDefined();
      expect((caught as any)?.name).toBe('TimelineVersionConflictError');
      expect((caught as any)?.message).toContain('stale baseVersion');
      expect((caught as any)?.message).toContain('version 7');
      expect((caught as any)?.message).toContain('version 3');
    });

    it('does NOT reject when patch.version is 0 (no-version-expectation bypass)', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let diff: TimelineDiff | undefined;
      act(() => {
        diff = result.current.apply({
          version: 0,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-v0',
              payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
            },
          ],
        });
      });

      expect(diff).toBeDefined();
      expect(commitData).toHaveBeenCalledTimes(1);
    });

    it('accepts patch when version matches current configVersion', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let diff: TimelineDiff | undefined;
      act(() => {
        diff = result.current.apply({
          version: 1,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-ok',
              payload: { track: 'V1', at: 5, clipType: 'hold', hold: 2 },
            },
          ],
        });
      });

      expect(diff).toBeDefined();
      expect(commitData).toHaveBeenCalledTimes(1);
    });

    it('leaves the canonical timeline unchanged on stale rejection', () => {
      const commitData = vi.fn();
      const original = makeBaseTimelineData();
      const dataRef = { current: original };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      const clipCountBefore = original.config.clips.length;

      expect(() =>
        act(() =>
          result.current.apply({
            version: 999,
            operations: [
              {
                op: 'clip.add',
                target: 'clip-should-not-exist',
                payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
              },
            ],
          }),
        ),
      ).toThrow();

      expect(original.config.clips).toHaveLength(clipCountBefore);
      expect(commitData).not.toHaveBeenCalled();
    });

    it('rejects stale batch even when some operations are valid', () => {
      const commitData = vi.fn();
      const data = makeBaseTimelineData();
      (data as any).configVersion = 10;
      const dataRef = { current: data };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      expect(() =>
        act(() =>
          result.current.apply({
            version: 1,
            operations: [
              {
                op: 'clip.add',
                target: 'clip-a',
                payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
              },
              {
                op: 'clip.add',
                target: 'clip-b',
                payload: { track: 'V1', at: 5, clipType: 'hold', hold: 2 },
              },
            ],
          }),
        ),
      ).toThrow();

      expect(commitData).not.toHaveBeenCalled();
    });
  });

  // -----------------------------------------------------------------------
  // Preview — stale base-version warning (T13)
  // -----------------------------------------------------------------------
  describe('preview — stale base-version warning', () => {
    it('attaches a warning diagnostic when baseVersion does not match configVersion', () => {
      const commitData = vi.fn();
      const data = makeBaseTimelineData();
      (data as any).configVersion = 5;
      const dataRef = { current: data };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let previewResult: TimelinePreviewResult | undefined;
      act(() => {
        previewResult = result.current.preview({
          version: 3,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-p',
              payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
            },
          ],
        });
      });

      expect(previewResult).toBeDefined();
      expect(previewResult!.fullyPreviewable).toBe(true);
      const staleDiag = previewResult!.diagnostics.find(
        (d) => d.code === 'timeline-patch/stale-base-version',
      );
      expect(staleDiag).toBeDefined();
      expect(staleDiag!.severity).toBe('warning');
      expect(staleDiag!.message).toContain('baseVersion (3)');
      expect(staleDiag!.message).toContain('version (5)');
    });

    it('does NOT warn when baseVersion matches configVersion', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let previewResult: TimelinePreviewResult | undefined;
      act(() => {
        previewResult = result.current.preview({
          version: 1,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-p',
              payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
            },
          ],
        });
      });

      const staleDiag = previewResult!.diagnostics.find(
        (d) => d.code === 'timeline-patch/stale-base-version',
      );
      expect(staleDiag).toBeUndefined();
    });

    it('does NOT warn when patch.version is 0 (no-version-expectation bypass)', () => {
      const commitData = vi.fn();
      const dataRef = { current: makeBaseTimelineData() };
      const createManualCheckpoint = vi.fn();
      const jumpToCheckpoint = vi.fn();
      const checkpoints: Checkpoint[] = [];

      const { result } = renderHook(() =>
        useTimelineOps({
          commitData,
          dataRef,
          createManualCheckpoint,
          jumpToCheckpoint,
          checkpoints,
        }),
      );

      let previewResult: TimelinePreviewResult | undefined;
      act(() => {
        previewResult = result.current.preview({
          version: 0,
          operations: [
            {
              op: 'clip.add',
              target: 'clip-p',
              payload: { track: 'V1', at: 0, clipType: 'hold', hold: 1 },
            },
          ],
        });
      });

      const staleDiag = previewResult!.diagnostics.find(
        (d) => d.code === 'timeline-patch/stale-base-version',
      );
      expect(staleDiag).toBeUndefined();
    });
  });
});
