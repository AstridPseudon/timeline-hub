import { afterEach, describe, expect, it, vi } from 'vitest';
import { emitTimelineSaveDiagnostic } from './timeline-diagnostics';

describe('timeline save diagnostic projection', () => {
  afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

  it('does not evaluate observations unless the browser flag is exactly true', () => {
    const read = vi.fn(() => ({}));
    for (const flag of [undefined, false, 1, 'true']) {
      vi.stubGlobal('__timelineSaveDiagnosticsEnabled', flag);
      emitTimelineSaveDiagnostic('schedule', read);
    }
    expect(read).not.toHaveBeenCalled();
    Object.defineProperty(window, '__timelineSaveDiagnosticsEnabled', { configurable: true, get() { throw new Error('flag'); } });
    expect(() => emitTimelineSaveDiagnostic('schedule', read)).not.toThrow();
    expect(read).not.toHaveBeenCalled();
  });

  it('emits detached bounded scalar records with stable non-auth aliases', () => {
    vi.stubGlobal('__timelineSaveDiagnosticsEnabled', true);
    const records: Record<string, unknown>[] = [];
    const listener = (event: Event) => records.push((event as CustomEvent).detail);
    window.addEventListener('timeline:save-diagnostic', listener);
    try {
      const owner = {};
      const clip = { id: 'clip-1', from: 3, to: null, hold: Infinity, speed: 1, metadata: 'secret' };
      const source = { config: { clips: [clip] }, head: { projectId: 'project-1', headRevisionId: 'r0', headPublicationId: 'p0' }, bundle: 'secret' };
      const read = () => ({ owner, timelineId: 'timeline-1', clipId: 'clip-1', mounted: source,
        source, basis: { source }, basisStatus: 'ready', gesture: { kind: 'trim', patch: { from: 3 } },
        state: { status: 'dirty', ownerId: 'secret', recoverableOwners: ['secret'] } });
      emitTimelineSaveDiagnostic('capture-called', read);
      emitTimelineSaveDiagnostic('capture-resolved', read);
      expect(records).toHaveLength(2);
      expect(records[0]).toMatchObject({ version: 1, projectId: 'project-1', timelineId: 'timeline-1', clipId: 'clip-1',
        mountedHead: { revisionId: 'r0', publicationId: 'p0' }, originalHead: { revisionId: 'r0', publicationId: 'p0' },
        patch: { from: 3, fromState: 'present', toState: 'absent' },
        mountedClip: { from: 3, to: null, toState: 'null', hold: 'UNKNOWN', holdState: 'UNKNOWN' },
        recoverableOwnerCount: 1, intentsPendingCount: 'UNKNOWN' });
      expect(records[1].ownerAlias).toBe(records[0].ownerAlias);
      expect(Number(records[1].sequence)).toBeGreaterThan(Number(records[0].sequence));
      expect(Number(records[1].time)).toBeGreaterThanOrEqual(Number(records[0].time));
      clip.from = 9;
      expect(records[0].mountedClip).toMatchObject({ from: 3 });
      expect(Object.isFrozen(records[0])).toBe(true);
      expect(Object.isFrozen(records[0].mountedClip)).toBe(true);
      expect(JSON.stringify(records)).not.toContain('secret');
      expect(JSON.stringify(records).length).toBeLessThan(8000);
    } finally { window.removeEventListener('timeline:save-diagnostic', listener); }
  });

  it('does not invoke nested getters, deep walk arbitrary data, or propagate projection/dispatch errors', () => {
    vi.stubGlobal('__timelineSaveDiagnosticsEnabled', true);
    const getter = vi.fn(() => { throw new Error('private'); });
    const source = Object.defineProperty({}, 'config', { get: getter });
    const dispatch = vi.spyOn(window, 'dispatchEvent').mockReturnValue(true);
    emitTimelineSaveDiagnostic('capture-rejected', () => ({ mounted: source, state: { error: new Error('secret') } }));
    expect(getter).not.toHaveBeenCalled();
    const detail = (dispatch.mock.calls[0][0] as CustomEvent).detail;
    expect(detail).toMatchObject({ errorStage: 'capture', errorCode: 'operation-rejected',
      mountedClip: { fromState: 'UNKNOWN' } });
    expect(JSON.stringify(detail)).not.toContain('secret');
    expect(() => emitTimelineSaveDiagnostic('schedule', () => { throw new Error('projection'); })).not.toThrow();
    dispatch.mockImplementation(() => { throw new Error('listener'); });
    expect(() => emitTimelineSaveDiagnostic('schedule', () => ({}))).not.toThrow();
  });

  it('limits selected clip inspection and never emits URL-shaped identifiers or unknown state strings', () => {
    vi.stubGlobal('__timelineSaveDiagnosticsEnabled', true);
    const clips = Array.from({ length: 257 }, (_, i) => ({ id: `clip-${i}`, from: i }));
    const dispatch = vi.spyOn(window, 'dispatchEvent').mockReturnValue(true);
    emitTimelineSaveDiagnostic('schedule', () => ({ clipId: 'clip-256', timelineId: 'https://secret',
      mounted: { config: { clips } }, state: { status: 'secret' } }));
    expect((dispatch.mock.calls[0][0] as CustomEvent).detail).toMatchObject({ timelineId: 'UNKNOWN', status: 'UNKNOWN',
      mountedClip: { from: 'UNKNOWN', fromState: 'UNKNOWN' } });
  });
});
