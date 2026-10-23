// @vitest-environment node
import { describe, expect, it, vi } from 'vitest';
import fixture from '@/tools/video-editor/data/shotComposition.fixture.json';
import { createShotCompositionAdapter } from '@/tools/video-editor/data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '@/tools/video-editor/data/shotCompositionProjection.ts';
import type { DataProvider, TimelineCommandBasis } from '@/tools/video-editor/data/DataProvider.ts';
import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import { createShotTimelineDataProvider } from './shotTimelineDataProvider.ts';

const sessionMock = vi.hoisted(() => ({
  appendDocument: vi.fn(),
  flush: vi.fn(),
  getDocument: vi.fn(),
  dispose: vi.fn(async () => undefined),
}));

vi.mock('@/tools/video-editor/commands/localSaveSession.ts', () => ({
  createLocalSaveSession: vi.fn(async () => sessionMock),
}));

function canonicalDocument(): CanonicalDocument {
  const occurrence = fixture.occurrences.find((value) => value.occurrence_id === 'occ-3')!;
  const shot = fixture.shot_revisions.find((value) => value.shot_id === 'shot-alpha' && value.revision_id === 'rev-b')!;
  const internal = shot.internal_timeline_revision;
  return {
    schema_version: 1,
    project_id: 'project-001',
    timeline_id: 'document-primary',
    parent_revision: {
      revision_id: fixture.primary_timeline.head.revision_id,
      content_digest: 'sha256:parent',
      payload: {
        config: { clips: [], tracks: [] },
        occurrences: [{
          occurrence_id: occurrence.occurrence_id,
          shot_id: occurrence.shot_id,
          shot_revision_id: occurrence.revision_id,
        }],
      },
    },
    shot_revisions: [{
      shot_id: shot.shot_id,
      revision_id: shot.revision_id,
      internal_timeline_revision_id: internal.revision_id,
      content_digest: 'sha256:shot',
      payload: { name: 'raw-shot', internal_timeline_revision_id: internal.revision_id },
    }],
    internal_timeline_revisions: [{
      timeline_id: 'timeline-alpha',
      revision_id: internal.revision_id,
      content_digest: internal.content_digest,
      payload: structuredClone(internal.timeline),
    }],
    dependency_manifest: {
      shots: [{ shot_id: shot.shot_id, revision_id: shot.revision_id,
        internal_timeline_revision_id: internal.revision_id, content_digest: 'sha256:shot' }],
      internal_timelines: [{ timeline_id: 'timeline-alpha', revision_id: internal.revision_id, content_digest: internal.content_digest }],
      media: [], documents: [],
    },
  } as CanonicalDocument;
}

describe('shot popup A3 save ingress', () => {
  it('uses the A2 session for a uniquely owned child root and publishes its accepted closure', async () => {
    const adapter = createShotCompositionAdapter({ load: vi.fn(), publish: vi.fn() });
    const composition = adapter.prepare(fixture);
    const occurrence = composition.occurrences.find((value) => value.occurrenceId === 'occ-3')!;
    const config = projectCanonicalComposition({ ...composition, occurrences: [occurrence] }).config;
    const before = canonicalDocument();
    const basis: TimelineCommandBasis = {
      head: { revisionId: fixture.primary_timeline.head.revision_id, publicationId: 'pub-0' },
      canonicalDocument: before,
      graph: fixture,
    };
    sessionMock.getDocument.mockReturnValue(before);
    sessionMock.flush.mockResolvedValue({
      ...basis,
      head: { revisionId: 'rev-accepted', publicationId: 'pub-accepted' },
      graph: { ...fixture, primary_timeline: { ...fixture.primary_timeline,
        head: { ...fixture.primary_timeline.head, revision_id: 'rev-accepted' } } },
    });
    const timelineDataProvider = {
      loadTimelineCommandBasis: vi.fn(async () => basis),
      getRecoverableIdentity: vi.fn(async () => ({ actorId: 'actor-1', realmId: 'realm-1' })),
      commitTimeline: vi.fn(),
    } as unknown as DataProvider;
    const published = vi.fn();
    const provider = createShotTimelineDataProvider(
      config,
      composition,
      occurrence.occurrenceId,
      adapter,
      published,
      undefined,
      0,
      undefined,
      timelineDataProvider,
    );
    const nextConfig = {
      ...config,
      clips: config.clips.map((clip, index) => index === 0 ? { ...clip, hold: (clip.hold ?? 0) + 0.25 } : clip),
    };

    await expect(provider.saveTimeline('popup-timeline', nextConfig, 1)).resolves.toBe(2);
    expect(sessionMock.appendDocument).toHaveBeenCalledWith(expect.objectContaining({
      label: 'Edit shot timeline',
      roots: [{ ref: 'internal-revision:timeline-alpha-b', revisionId: 'timeline-alpha-b', contentDigest: 'sha256:5555555555555555555555555555555555555555555555555555555555555555' }],
      before,
      after: expect.objectContaining({
        internal_timeline_revisions: [expect.objectContaining({
          revision_id: 'timeline-alpha-b',
          payload: expect.objectContaining({
            clips: [expect.objectContaining({
              id: 'alpha-video-b',
              app: expect.objectContaining({ visualBoundary: { intentionalPause: true } }),
            })],
          }),
        })],
      }),
    }));
    expect(published).toHaveBeenCalledWith(expect.objectContaining({ headRevisionId: 'rev-accepted' }), 0, fixture.primary_timeline.head.revision_id);
    expect(timelineDataProvider.commitTimeline).not.toHaveBeenCalled();
  });
});
