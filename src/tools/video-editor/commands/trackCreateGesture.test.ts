import { describe, expect, it } from 'vitest';
import { buildTimelineCommandData } from './timelineData.ts';
import fixture from './fixtures/recipe_m2_app_track_create.json';
import {
  captureTrackCreateEdit,
  projectTrackCreatePreview,
  submitTrackCreateEdit,
  trackCreatePreview,
  type TrackCreateCapturePort,
} from './trackCreateGesture.ts';
import { captureTrackCreate, finishTrackCreate, type TrackCreateArgs } from './trackCreateCapture.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

const bundle = fixture.bundle as unknown as AuthoredBundle;
const row = fixture.input.row as TrackCreateArgs['row'];

function current() {
  const parent = bundle.parent;
  return buildTimelineCommandData({ ...(parent.config as never), clips: parent.clips } as never, { assets: {} });
}

describe('parent track.create gesture port', () => {
  it('keeps the reserved full row through capture, submit, and local projection', () => {
    const port: TrackCreateCapturePort = {
      capture: () => captureTrackCreate(bundle, { row }),
      finish: (basis, args) => {
        const result = finishTrackCreate(basis, args);
        return { command: result.command, preview: trackCreatePreview(args.row) };
      },
      submit: ({ command, preview }) => {
        expect(command.op).toBe('track.create');
        expect(preview).toEqual(trackCreatePreview(row));
      },
    };
    const captured = captureTrackCreateEdit(port, current(), row);

    submitTrackCreateEdit(captured);
    const projected = projectTrackCreatePreview(trackCreatePreview(row), current());

    expect(projected?.config.tracks.at(-1)).toEqual(row);
    expect(projected?.resolvedConfig.tracks.at(-1)).toEqual(row);
    expect(captured.row).toEqual(row);
  });

  it('refuses a duplicate displayed identity before local projection', () => {
    const duplicate = { ...row, id: 'picture' };
    expect(() => projectTrackCreatePreview(trackCreatePreview(duplicate), {
      ...current(), config: { ...current().config, tracks: [...current().config.tracks, duplicate as never] },
    })).toThrow('Invalid native track.create preview');
  });

  it('preserves root data and accepted/local projection facts through a whole-row birth', () => {
    const before = current();
    const lane = {
      laneId: 'opaque:custom', kindId: 'custom', label: 'Custom', schemaRef: 'custom/v1', shape: 'point' as const,
      domain: 'timeline_seconds' as const, items: [], hidden: false, height: 24, opaque: true,
    };
    const sourceItems = {
      'custom/v1': [{ id: 'source-1', shape: 'point' as const, domain: 'timeline_seconds' as const,
        extent: { start: 0 }, schemaRef: 'custom/v1', payload: { keep: [null, false] },
        sourceArtifactRef: { assetId: 'asset-1' }, provenance: { adapterId: 'test', adapterVersion: '1' } }],
    };
    const transcriptReferences = { schema: 'media.transcript.references/v1' as const,
      associations: [{ assetId: 'asset-1', documentId: 'transcript-1' }] };
    const opaqueConfig = { opaque: { preserve: [null, false, { nested: true }] } };
    const registry = { assets: { 'asset-1': { file: 'asset-1.mp4', type: 'video/mp4' } } };
    before.head = { projectId: 'project', timelineId: 'timeline', headRevisionId: 'r0', headPublicationId: 'p0' };
    before.editProjection = { kind: 'accepted', head: { revisionId: 'r0', publicationId: 'p0' } };
    before.dataLanes = [lane];
    before.sourceItemsBySchemaRef = sourceItems;
    before.transcriptReferences = transcriptReferences;
    before.config = { ...before.config, app: opaqueConfig };
    before.registry = registry;
    before.assetMap = { 'asset-1': 'asset-1.mp4' };

    const projected = projectTrackCreatePreview(trackCreatePreview(row), before)!;

    expect(projected.head).toBe(before.head);
    expect(projected.configVersion).toBe(before.configVersion);
    expect(projected.dataLanes).toBe(before.dataLanes);
    expect(projected.sourceItemsBySchemaRef).toBe(before.sourceItemsBySchemaRef);
    expect(projected.transcriptReferences).toBe(before.transcriptReferences);
    expect(projected.config.app).toEqual(opaqueConfig);
    expect(projected.registry).toBe(before.registry);
    expect(projected.registry.assets['asset-1']).toEqual(registry.assets['asset-1']);
    expect(projected.assetMap).toBe(before.assetMap);
    expect(projected.editProjection).toEqual({ kind: 'local', base: { revisionId: 'r0', publicationId: 'p0' }, generation: 0 });

    const localProjection = { kind: 'local' as const, base: { revisionId: 'prior-r', publicationId: 'prior-p' }, generation: 7 };
    const existingLocal = { ...before, editProjection: localProjection };
    const retained = projectTrackCreatePreview(trackCreatePreview({ ...row, id: 'second' }), existingLocal)!;
    expect(retained.editProjection).toBe(localProjection);
    expect(retained.dataLanes).toBe(before.dataLanes);
    expect(retained.sourceItemsBySchemaRef).toBe(before.sourceItemsBySchemaRef);
  });
});
