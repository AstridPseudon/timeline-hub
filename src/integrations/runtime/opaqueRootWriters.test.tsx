import { act, renderHook } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { RuntimeDataProvider } from './dataProvider.ts';
import { PROJECT_ID, TIMELINE_ID, runtimeFixture } from '@/test/fakeWorkspaceRuntime.ts';
import { useTimelineCommit } from '@/tools/video-editor/hooks/useTimelineCommit.ts';
import { TimelineEventBus } from '@/tools/video-editor/hooks/useTimelineEventBus.ts';
import { buildTimelineData, type TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { buildDataFromSnapshot } from '@/tools/video-editor/lib/timeline-save-utils.ts';
import { splitClipAtPlayhead } from '@/tools/video-editor/lib/editor-utils.ts';
import { previewTimelineMutation } from '@/tools/video-editor/lib/timeline-mutation-engine.ts';
import { compileTimelinePatch } from '@/tools/video-editor/lib/timeline-patch.ts';
import { applyTimelineCommandEffect } from '@/tools/video-editor/commands/runner.ts';
import { serializeForDisk, validateSerializedConfig } from '@/tools/video-editor/lib/serialize.ts';
import { AstridElementOperationAdapter, createElementTimelineRoutes } from '@/tools/video-editor/runtime/element-adapter.ts';
import { buildAstridAgentElementContext } from '@/tools/video-editor/runtime/element-contract.ts';

const roots = () => JSON.parse(`{
  "opaque":{"values":[null,false,0,"",[],{"nested":true}]},
  "nullable":null,"ordered":["third","first","second"],
  "__proto__":{"literal":true},"constructor":{"prototype":[null]},"prototype":false
}`);

async function editor() {
  const raw = roots();
  const fixture = runtimeFixture({ initialConfig: raw, initialClips: [
    { id: 'a', track: 'V1', at: 0, hold: 4, clipType: 'hold' },
  ] });
  const provider = new RuntimeDataProvider({ projectId: PROJECT_ID, transport: fixture.transport });
  const loaded = await provider.loadTimeline(TIMELINE_ID);
  const registry = await provider.loadAssetRegistry(TIMELINE_ID);
  const initial = await buildTimelineData(loaded.config, registry, undefined, loaded.configVersion, undefined, loaded.head);
  const saves: TimelineData[] = [];
  const eventBus = new TimelineEventBus();
  eventBus.on('scheduleSave', (data) => saves.push(data));
  const hook = renderHook(() => useTimelineCommit({ eventBus, lastSavedSignatureRef: { current: '' }, initialData: initial }));
  return { raw, fixture, provider, loaded, registry, initial, saves, hook };
}

describe('opaque roots at live writer serialization boundaries', () => {
  it.each(['rows', 'split', 'patch', 'resolved-preview', 'command-effect'] as const)('%s preserves authored roots in the scheduled save, recovery rebuild, wire payload and reload', async (path) => {
    const { raw, fixture, provider, loaded, registry, initial, saves, hook } = await editor();
    const before = JSON.stringify(initial.config);
    const resolved = { ...initial.resolvedConfig, clips: initial.resolvedConfig.clips.map((clip) => ({ ...clip, opacity: 0.4 })) };
    act(() => {
      if (path === 'rows') {
        hook.result.current.applyEdit({ type: 'rows', rows: initial.rows, metaUpdates: { a: { opacity: 0.4 } } });
      } else if (path === 'split') {
        const split = splitClipAtPlayhead(initial.resolvedConfig, 'a', 2);
        expect(split.nextSelectedClipId).toBeTruthy();
        hook.result.current.applyEdit({ type: 'config', resolvedConfig: split.config });
      } else if (path === 'resolved-preview') {
        const preview = previewTimelineMutation(initial, { type: 'config', resolvedConfig: resolved });
        expect(preview.ok).toBe(true);
        if (!preview.ok) throw new Error(preview.error.message);
        hook.result.current.commitData(preview.nextData);
      } else if (path === 'patch') {
        const compiled = compileTimelinePatch({ version: initial.configVersion, operations: [
          { op: 'clip.update', target: 'a', payload: { opacity: 0.4 } },
        ] }, initial);
        expect(compiled.valid).toBe(true);
        if (!compiled.nextData) throw new Error('Patch produced no draft');
        hook.result.current.commitData(compiled.nextData);
      } else {
        hook.result.current.commitData(applyTimelineCommandEffect(initial, {
          mutation: { type: 'resolved-config', resolvedConfig: resolved },
        }));
      }
    });
    expect(saves).toHaveLength(1);
    const saved = saves[0];
    const recovered = buildDataFromSnapshot(saved.config, saved.registry, initial);
    for (const data of [saved, recovered]) {
      for (const [key, value] of Object.entries(raw)) {
        expect(Object.hasOwn(data.config, key), key).toBe(true);
        expect(Reflect.get(data.config, key), key).toEqual(value);
        expect(Reflect.get(data.resolvedConfig, key), key).toEqual(value);
      }
      expect(Object.hasOwn(data.config, 'absent')).toBe(false);
      expect(Object.hasOwn(data.config, 'registry')).toBe(false);
    }
    if (path === 'split') expect(saved.config.clips).toHaveLength(2);
    else expect(saved.config.clips[0].opacity).toBe(0.4);
    await provider.saveTimelineAtHead(TIMELINE_ID, saved.config, loaded.head!, registry);
    const publications = fixture.requests.filter(({ method, path }) => method === 'POST' && path.endsWith('/composition-revisions'));
    expect(publications).toHaveLength(1);
    const outgoing = publications[0].body as { parent_composition: { config: Record<string, unknown> } };
    const { output: _output, ...authored } = saved.config;
    expect(outgoing.parent_composition.config).toEqual(authored);
    const reopened = new RuntimeDataProvider({ projectId: PROJECT_ID, transport: fixture.transport });
    const reloaded = await reopened.loadTimeline(TIMELINE_ID);
    const { output: _reloadedOutput, ...reloadedAuthored } = reloaded.config;
    expect(reloadedAuthored).toEqual(authored);
    expect(JSON.stringify(initial.config)).toBe(before);
    hook.unmount();
  });

  it('merges the immutable raw basis even when the compatibility caller supplies a strict disk projection', async () => {
    const { raw, fixture, provider, loaded, initial, hook } = await editor();
    const projected = serializeForDisk({ ...initial.resolvedConfig, tracks: initial.tracks.map((track) => ({ ...track, label: 'Edited' })) });
    expect(Object.hasOwn(projected, 'opaque')).toBe(false);
    expect(() => validateSerializedConfig({ ...projected, ...raw })).toThrow();
    await provider.saveTimelineAtHead(TIMELINE_ID, projected, loaded.head!);
    const body = fixture.requests.find(({ method, path }) => method === 'POST' && path.endsWith('/composition-revisions'))!.body as { parent_composition: { config: unknown } };
    const { output: _output, ...basis } = loaded.config;
    expect(body.parent_composition.config).toEqual({ ...basis, ...projected });
    hook.unmount();
  });

  it('element adapter sends the complete raw config with only the requested fade changed', async () => {
    const { fixture, provider, loaded, hook } = await editor();
    const adapter = new AstridElementOperationAdapter(
      buildAstridAgentElementContext({}), createElementTimelineRoutes(provider), PROJECT_ID,
      { timelineId: TIMELINE_ID, assertAuthority: vi.fn(), capturedHead: loaded.head },
    );
    await adapter.execute({ name: 'timeline.set_clip_fade', project: PROJECT_ID, timeline: TIMELINE_ID,
      expected_version: loaded.configVersion, clip_id: 'a', fade_in: 0.2 });
    const body = fixture.requests.find(({ method, path }) => method === 'POST' && path.endsWith('/composition-revisions'))!.body as { parent_composition: { config: unknown } };
    const { output: _output, ...basis } = loaded.config;
    expect(body.parent_composition.config).toEqual({ ...basis, clips: basis.clips.map((clip) => ({
      ...clip, effects: { fade_in: 0.2 }, entrance: { type: 'fade', duration: 0.2 },
    })) });
    hook.unmount();
  });
});
