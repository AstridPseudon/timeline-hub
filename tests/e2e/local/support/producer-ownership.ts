import { randomUUID } from 'node:crypto';
import type { Page } from '@playwright/test';
import {
  APP_ENTRY_ROUTE,
  currentHead,
  expectConnected,
  firstTrackName,
  revisionBody,
  type DirectHarness,
} from './app.ts';
import {
  compositionPublication,
} from './harness.ts';
import { SCENE_PHASE_EXTENSION_ID } from '../../../../src/tools/video-editor/dev/scene-phase-markers/extension.ts';
import {
  TRANSCRIPT_CAPTION_TRACK_ID,
  transcriptCaptionClipId,
} from '../../../../src/tools/video-editor/dev/transcript-lane/extension.ts';

export const PRODUCER_OWNERSHIP_TRANSCRIPT_SOURCE_IDS = [
  'transcript-source:producer-ownership-speech:segment:producer-ownership-foreign',
  'transcript-source:producer-ownership-speech:segment:producer-ownership-user',
  'transcript-source:producer-ownership-speech:segment:producer-ownership-missing',
] as const;

export const PRODUCER_OWNERSHIP_SCENE_MARKERS = [
  { id: 'producer-ownership-marker-a', time: 1 },
  { id: 'producer-ownership-marker-b', time: 6 },
] as const;

export const PRODUCER_OWNERSHIP_PROTECTED_IDS = {
  transcriptForeign: transcriptCaptionClipId(PRODUCER_OWNERSHIP_TRANSCRIPT_SOURCE_IDS[0]),
  transcriptUser: transcriptCaptionClipId(PRODUCER_OWNERSHIP_TRANSCRIPT_SOURCE_IDS[1]),
  sceneForeign: 'producer-ownership-scene-foreign',
  sceneUser: 'producer-ownership-scene-user',
} as const;

export interface ProducerOwnershipSeed {
  projectSlug: string;
  timelineId: string;
  headRevisionId: string;
  transcriptMissingClipId: string;
  sceneFreshClipIds: readonly string[];
  protectedClipIds: readonly string[];
}

export interface ProducerOwnershipRevision {
  head: string;
  body: Record<string, any>;
}

export async function seedProducerOwnershipFixture(harness: DirectHarness): Promise<ProducerOwnershipSeed> {
  const project = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}`);
  if (project.status !== 200) throw new Error(`read producer ownership project: ${project.status} ${JSON.stringify(project.body)}`);

  const transcriptTexts = ['Foreign caption survives', 'User caption survives', 'Fresh caption is owned'];
  const assetKey = 'producer-ownership-speech';
  const bundle = {
    schema_version: 1,
    itemsBySchemaRef: {
      'astrid.transcript_segment/v1': transcriptTexts.map((text, index) => ({
        id: PRODUCER_OWNERSHIP_TRANSCRIPT_SOURCE_IDS[index],
        shape: 'interval',
        domain: 'source_seconds',
        extent: { start: index * 2, end: index * 2 + 2 },
        schemaRef: 'astrid.transcript_segment/v1',
        payload: { text },
        sourceArtifactRef: { assetId: assetKey },
        provenance: { adapterId: 'astrid.adaptTranscript', adapterVersion: '2' },
      })),
    },
  };
  const timelineId = randomUUID();
  const transcriptForeign = {
    id: PRODUCER_OWNERSHIP_PROTECTED_IDS.transcriptForeign,
    track: TRANSCRIPT_CAPTION_TRACK_ID,
    at: 0,
    hold: 2,
    clipType: 'text',
    label: 'foreign caption',
    text: { content: 'Foreign caption survives', fontSize: 22, color: '#f00', future: { keep: true } },
    app: { managedBy: 'com.other.transcript-extension', foreign: { nested: [1, null, false] } },
  };
  const transcriptUser = {
    id: PRODUCER_OWNERSHIP_PROTECTED_IDS.transcriptUser,
    track: TRANSCRIPT_CAPTION_TRACK_ID,
    at: 2,
    hold: 2,
    clipType: 'text',
    label: 'user caption',
    text: { content: 'User caption survives', fontSize: 31, color: '#0f0', userField: 'keep-me' },
    app: { userAuthored: true, opaque: { order: ['a', 'b'] } },
  };
  const sceneForeign = {
    id: PRODUCER_OWNERSHIP_PROTECTED_IDS.sceneForeign,
    track: 'V1',
    at: 20,
    hold: 2,
    clipType: 'hold',
    label: 'foreign scene clip',
    app: { managedBy: 'com.other.scene-extension', foreign: { nested: { keep: true } } },
  };
  const sceneUser = {
    id: PRODUCER_OWNERSHIP_PROTECTED_IDS.sceneUser,
    track: 'V1',
    at: 24,
    hold: 2,
    clipType: 'hold',
    label: 'user scene clip',
    app: { userAuthored: true, opaque: { nullable: null, ordered: [false, 0, ''] } },
  };
  const speechClip = {
    id: 'producer-ownership-speech-carrier',
    at: 8,
    track: 'V1',
    clipType: 'media',
    asset: assetKey,
    from: 0,
    to: 6,
    speed: 1,
  };
  const clips = [speechClip, transcriptForeign, transcriptUser, sceneForeign, sceneUser];
  const publication = compositionPublication({ projectId: harness.seed.projectId, timelineId }, null, 'Producer ownership', 30);
  publication.parent_composition.config = {
    ...publication.parent_composition.config,
    tracks: [
      { id: 'V1', kind: 'visual', label: 'V1' },
      { id: TRANSCRIPT_CAPTION_TRACK_ID, kind: 'visual', label: 'Transcript Captions' },
    ],
    clips,
    bundle,
    app: { [SCENE_PHASE_EXTENSION_ID]: { sceneMarkers: [...PRODUCER_OWNERSHIP_SCENE_MARKERS] } },
  } as unknown as typeof publication.parent_composition.config;
  publication.parent_composition.clips = clips as unknown as typeof publication.parent_composition.clips;
  publication.parent_composition.registry = {
    assets: {
      [assetKey]: {
        file: 'producer-ownership-speech.webm',
        type: 'video',
        duration: 12,
        media_id: harness.seed.video.objectId,
        content_sha256: harness.seed.video.digest,
      },
    },
  } as unknown as typeof publication.parent_composition.registry;
  const published = await harness.runtimeJson(
    'POST',
    `/v1/projects/${harness.seed.projectId}/timelines/${timelineId}/composition-revisions`,
    publication,
  );
  if (published.status !== 200) throw new Error(`seed producer ownership timeline: ${published.status} ${JSON.stringify(published.body)}`);
  const projectData = project.body.data ?? project.body;
  return {
    projectSlug: projectData.slug,
    timelineId,
    headRevisionId: published.body.data.new_head,
    transcriptMissingClipId: transcriptCaptionClipId(PRODUCER_OWNERSHIP_TRANSCRIPT_SOURCE_IDS[2]),
    sceneFreshClipIds: PRODUCER_OWNERSHIP_SCENE_MARKERS.map((marker) => `scene-phase-shot-${marker.id}`),
    protectedClipIds: Object.values(PRODUCER_OWNERSHIP_PROTECTED_IDS),
  };
}

export async function openProducerOwnershipTimeline(page: Page, harness: DirectHarness, seed: ProducerOwnershipSeed) {
  await page.goto(`${harness.origin}${APP_ENTRY_ROUTE}?project=${encodeURIComponent(harness.seed.projectId)}&timeline=${encodeURIComponent(seed.timelineId)}`);
  await expectConnected(page);
  await expect(firstTrackName(page)).toBeVisible();
}

export async function producerOwnershipRevision(harness: DirectHarness, seed: ProducerOwnershipSeed): Promise<ProducerOwnershipRevision> {
  const head = await currentHead(harness);
  return { head, body: await revisionBody(harness, head) };
}

function parentConfig(body: Record<string, any>): Record<string, any> {
  return body.payload?.config ?? body.data?.payload?.config ?? {};
}

export function protectedClipState(body: Record<string, any>, seed: ProducerOwnershipSeed) {
  const clips = Array.isArray(parentConfig(body).clips) ? parentConfig(body).clips as Array<Record<string, any>> : [];
  return seed.protectedClipIds.map((id) => ({
    order: clips.findIndex((clip) => clip.id === id),
    clip: clips.find((clip) => clip.id === id),
  }));
}

export function clipFromRevision(body: Record<string, any>, id: string): Record<string, any> | undefined {
  const clips = parentConfig(body).clips;
  return Array.isArray(clips) ? clips.find((clip: Record<string, any>) => clip.id === id) : undefined;
}

export function submittedTargets(value: unknown): string[] {
  const targets: string[] = [];
  const visit = (node: unknown) => {
    if (!node || typeof node !== 'object') return;
    if (Array.isArray(node)) {
      node.forEach(visit);
      return;
    }
    for (const [key, child] of Object.entries(node)) {
      if ((key === 'target' || key === 'select') && typeof child === 'string') targets.push(child);
      visit(child);
    }
  };
  visit(value);
  return targets;
}

export interface CommitObservation {
  body: Record<string, any>;
  rawBody: string;
}

export function observeProducerCommits(page: Page) {
  const requests: CommitObservation[] = [];
  const listener = (request: import('@playwright/test').Request) => {
    if (request.method() !== 'POST' || !new URL(request.url()).pathname.endsWith('/commit')) return;
    const rawBody = request.postData() ?? '{}';
    requests.push({ body: JSON.parse(rawBody) as Record<string, any>, rawBody });
  };
  page.on('request', listener);
  return {
    requests,
    dispose: () => page.off('request', listener),
  };
}

export function transcriptRegenerate(page: Page) {
  return page.locator('[data-lane-kind="astrid.transcript"]')
    .getByRole('button', { name: 'Transcript actions' })
    .click()
    .then(() => page.getByRole('menuitem', { name: 'Regenerate transcript captions and replace edits' }).click());
}

export function sceneCreateShots(page: Page) {
  return page.getByTestId('scene-markers-create-shots').click();
}

export function sceneMoveShots(page: Page) {
  return page.getByTestId('scene-markers-move-shots').click();
}

