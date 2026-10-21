import { randomUUID } from 'node:crypto';
import type { Page } from '@playwright/test';
import {
  APP_ENTRY_ROUTE,
  expectConnected,
  firstTrackName,
  type DirectHarness,
} from './app.ts';
import { compositionPublication } from './harness.ts';
import {
  SCENE_PHASE_EXTENSION_ID,
  scenePhaseShotId,
} from '../../../../src/tools/video-editor/dev/scene-phase-markers/extension.ts';
import {
  TRANSCRIPT_CAPTION_CONTRIBUTION_ID,
  TRANSCRIPT_CAPTION_TRACK_ID,
  TRANSCRIPT_EXTENSION_VERSION,
  TRANSCRIPT_LANE_EXTENSION_ID,
  TRANSCRIPT_SCHEMA_REF,
  transcriptCaptionClipId,
} from '../../../../src/tools/video-editor/dev/transcript-lane/extension.ts';
import { createHostGeneratedObjectMeta } from '../../../../src/sdk/video/timeline/sourceMap.ts';

export const CURRENT_PIN_TRANSCRIPT_SOURCE_IDS = [
  'transcript-source:current-pin-speech:segment:foreign',
  'transcript-source:current-pin-speech:segment:user',
  'transcript-source:current-pin-speech:segment:stale',
] as const;

export const CURRENT_PIN_TRANSCRIPT_CARRIER_ID = 'current-pin-speech-carrier';

export const CURRENT_PIN_SCENE_MARKERS = [
  { id: 'current-pin-marker-a', time: 1 },
  { id: 'current-pin-marker-b', time: 6 },
] as const;

export const CURRENT_PIN_PROTECTED_IDS = {
  transcriptForeign: transcriptCaptionClipId(`${CURRENT_PIN_TRANSCRIPT_SOURCE_IDS[0]}@${CURRENT_PIN_TRANSCRIPT_CARRIER_ID}`),
  transcriptUser: transcriptCaptionClipId(`${CURRENT_PIN_TRANSCRIPT_SOURCE_IDS[1]}@${CURRENT_PIN_TRANSCRIPT_CARRIER_ID}`),
  sceneForeign: 'current-pin-scene-foreign',
  sceneUser: 'current-pin-scene-user',
} as const;

export interface CurrentPinProducerSeed {
  projectSlug: string;
  timelineId: string;
  headRevisionId: string;
  transcriptStaleClipId: string;
  sceneOwnedClipId: string;
  protectedClipIds: readonly string[];
}

export interface ProducerRevision {
  head: string;
  body: Record<string, any>;
}

function staleGeneratedMeta() {
  const sourceItemId = CURRENT_PIN_TRANSCRIPT_SOURCE_IDS[2];
  return createHostGeneratedObjectMeta({
    extensionId: TRANSCRIPT_LANE_EXTENSION_ID,
    contributionId: TRANSCRIPT_CAPTION_CONTRIBUTION_ID,
    extensionVersion: TRANSCRIPT_EXTENSION_VERSION,
    sourceSchemaRef: TRANSCRIPT_SCHEMA_REF,
    sourceItemId,
    sourceValue: {
      schemaRef: TRANSCRIPT_SCHEMA_REF,
      sourceItemId,
      payload: { text: 'Stale caption outside the carrier window' },
      timelineStart: 14,
      timelineEnd: 16,
    },
    outputValue: {
      track: TRANSCRIPT_CAPTION_TRACK_ID,
      at: 14,
      duration: 2,
      clipType: 'text',
      label: 'Stale caption outside the carrier window',
      text: { content: 'Stale caption outside the carrier window' },
    },
    sourceRevision: 1,
    conflictPolicy: 'regenerate-output',
  });
}

/** Seed a dedicated timeline through the worker's isolated Runtime realm. */
export async function seedCurrentPinProducerFixture(harness: DirectHarness): Promise<CurrentPinProducerSeed> {
  const project = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}`);
  if (project.status !== 200) throw new Error(`read current-pin project: ${project.status} ${JSON.stringify(project.body)}`);

  const assetKey = 'current-pin-speech';
  const sourceItems = [
    { id: CURRENT_PIN_TRANSCRIPT_SOURCE_IDS[0], extent: { start: 0, end: 2 }, text: 'Foreign caption survives' },
    { id: CURRENT_PIN_TRANSCRIPT_SOURCE_IDS[1], extent: { start: 2, end: 4 }, text: 'User caption survives' },
    // The carrier ends at source second 4. This valid source item is therefore
    // absent from the mounted projection while its generated output is stale.
    { id: CURRENT_PIN_TRANSCRIPT_SOURCE_IDS[2], extent: { start: 6, end: 8 }, text: 'Stale caption outside the carrier window' },
  ];
  const bundle = {
    schema_version: 1,
    itemsBySchemaRef: {
      [TRANSCRIPT_SCHEMA_REF]: sourceItems.map((item) => ({
        id: item.id,
        shape: 'interval',
        domain: 'source_seconds',
        extent: item.extent,
        schemaRef: TRANSCRIPT_SCHEMA_REF,
        payload: { text: item.text },
        sourceArtifactRef: { assetId: assetKey },
        provenance: { adapterId: 'astrid.adaptTranscript', adapterVersion: '2' },
      })),
    },
  };

  const transcriptForeign = {
    id: CURRENT_PIN_PROTECTED_IDS.transcriptForeign,
    track: TRANSCRIPT_CAPTION_TRACK_ID,
    at: 8,
    hold: 2,
    clipType: 'text',
    label: 'foreign caption',
    text: { content: 'Foreign caption survives', fontSize: 22, color: '#f00', future: { keep: true } },
    app: { managedBy: 'com.other.transcript-extension', foreign: { nested: [1, null, false] } },
  };
  const transcriptUser = {
    id: CURRENT_PIN_PROTECTED_IDS.transcriptUser,
    track: TRANSCRIPT_CAPTION_TRACK_ID,
    at: 10,
    hold: 2,
    clipType: 'text',
    label: 'user caption',
    text: { content: 'User caption survives', fontSize: 31, color: '#0f0', userField: 'keep-me' },
    app: { userAuthored: true, opaque: { order: ['a', 'b'] } },
  };
  const transcriptStale = {
    id: transcriptCaptionClipId(`${CURRENT_PIN_TRANSCRIPT_SOURCE_IDS[2]}@${CURRENT_PIN_TRANSCRIPT_CARRIER_ID}`),
    track: TRANSCRIPT_CAPTION_TRACK_ID,
    at: 14,
    hold: 2,
    clipType: 'text',
    label: 'Stale caption outside the carrier window',
    text: { content: 'Stale caption outside the carrier window' },
    app: { managedBy: TRANSCRIPT_LANE_EXTENSION_ID, __generated__: staleGeneratedMeta() },
  };
  const sceneForeign = {
    id: CURRENT_PIN_PROTECTED_IDS.sceneForeign,
    track: 'V1',
    at: 20,
    hold: 2,
    clipType: 'hold',
    label: 'foreign scene clip',
    app: { managedBy: 'com.other.scene-extension', foreign: { nested: { keep: true } } },
  };
  const sceneUser = {
    id: CURRENT_PIN_PROTECTED_IDS.sceneUser,
    track: 'V1',
    at: 24,
    hold: 2,
    clipType: 'hold',
    label: 'user scene clip',
    app: { userAuthored: true, opaque: { nullable: null, ordered: [false, 0, ''] } },
  };
  const sceneOwned = {
    id: scenePhaseShotId(CURRENT_PIN_SCENE_MARKERS[0].id),
    track: 'V1',
    at: 30,
    hold: 2,
    clipType: 'hold',
    label: 'Existing owned scene output',
    app: { managedBy: SCENE_PHASE_EXTENSION_ID, generated: { source: 'existing-output' } },
  };
  const carrier = {
    id: CURRENT_PIN_TRANSCRIPT_CARRIER_ID,
    at: 8,
    track: 'V1',
    clipType: 'media',
    asset: assetKey,
    from: 0,
    to: 4,
    speed: 1,
  };
  // Keep the removable stale row after every protected row so deleting it
  // cannot alter the protected rows' raw order positions.
  const clips = [carrier, transcriptForeign, transcriptUser, sceneForeign, sceneUser, sceneOwned, transcriptStale];
  const timelineId = randomUUID();
  const publication = compositionPublication({ projectId: harness.seed.projectId, timelineId }, null, 'Current producer ownership', 40);
  publication.parent_composition.config = {
    ...publication.parent_composition.config,
    tracks: [
      { id: 'V1', kind: 'visual', label: 'V1' },
      { id: TRANSCRIPT_CAPTION_TRACK_ID, kind: 'visual', label: 'Transcript Captions' },
    ],
    clips,
    bundle,
    app: { [SCENE_PHASE_EXTENSION_ID]: { sceneMarkers: [...CURRENT_PIN_SCENE_MARKERS] } },
  } as unknown as typeof publication.parent_composition.config;
  publication.parent_composition.clips = clips as unknown as typeof publication.parent_composition.clips;
  publication.parent_composition.registry = {
    assets: {
      [assetKey]: {
        file: 'current-pin-speech.webm',
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
  if (published.status !== 200) throw new Error(`seed current-pin timeline: ${published.status} ${JSON.stringify(published.body)}`);
  const projectData = project.body.data ?? project.body;
  return {
    projectSlug: projectData.slug,
    timelineId,
    headRevisionId: published.body.data.new_head,
    transcriptStaleClipId: transcriptStale.id,
    sceneOwnedClipId: sceneOwned.id,
    protectedClipIds: Object.values(CURRENT_PIN_PROTECTED_IDS),
  };
}

export async function openCurrentPinTimeline(page: Page, harness: DirectHarness, seed: CurrentPinProducerSeed) {
  await page.goto(`${harness.origin}${APP_ENTRY_ROUTE}?project=${encodeURIComponent(harness.seed.projectId)}&timeline=${encodeURIComponent(seed.timelineId)}`);
  await expectConnected(page);
  await expect(firstTrackName(page)).toBeVisible();
}

export async function currentPinRevision(harness: DirectHarness, seed: CurrentPinProducerSeed): Promise<ProducerRevision> {
  const path = `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions`;
  const revisions = await harness.runtimeJson('GET', `${path}?limit=1`);
  if (revisions.status !== 200) throw new Error(`read current-pin head: ${revisions.status} ${JSON.stringify(revisions.body)}`);
  const head = revisions.body.items.find((item: any) => item.is_current_head)?.revision_id;
  if (typeof head !== 'string') throw new Error(`current-pin timeline has no current head: ${JSON.stringify(revisions.body)}`);
  const revision = await harness.runtimeJson('GET', `${path}/${head}`);
  if (revision.status !== 200) throw new Error(`read current-pin revision: ${revision.status} ${JSON.stringify(revision.body)}`);
  return { head, body: revision.body };
}

function parentConfig(body: Record<string, any>): Record<string, any> {
  return body.payload?.config ?? body.data?.payload?.config ?? {};
}

export function clipFromRevision(body: Record<string, any>, id: string): Record<string, any> | undefined {
  const clips = parentConfig(body).clips;
  return Array.isArray(clips) ? clips.find((clip: Record<string, any>) => clip.id === id) : undefined;
}

export function protectedClipState(body: Record<string, any>, seed: CurrentPinProducerSeed) {
  const clips = Array.isArray(parentConfig(body).clips) ? parentConfig(body).clips as Array<Record<string, any>> : [];
  return seed.protectedClipIds.map((id) => ({ order: clips.findIndex((clip) => clip.id === id), clip: clips.find((clip) => clip.id === id) }));
}

export interface CommitObservation {
  body: Record<string, any>;
  rawBody: string;
  key: string | undefined;
  status: number | null;
  response: Record<string, any> | null;
}

export function observeProducerCommits(page: Page) {
  const requests: CommitObservation[] = [];
  const listener = (request: import('@playwright/test').Request) => {
    if (request.method() !== 'POST' || !new URL(request.url()).pathname.endsWith('/commit')) return;
    const rawBody = request.postData() ?? '{}';
    requests.push({ body: JSON.parse(rawBody) as Record<string, any>, rawBody, key: request.headers()['idempotency-key'], status: null, response: null });
  };
  page.on('request', listener);
  return { requests, dispose: () => page.off('request', listener) };
}

/** Let Runtime accept a commit, then drop only the browser acknowledgement. */
export async function discardFirstAcceptedCommitAcknowledgement(page: Page, requests: CommitObservation[]) {
  const commits = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
  let first = true;
  let resolveAccepted!: () => void;
  let rejectAccepted!: (error: unknown) => void;
  const accepted = new Promise<void>((resolve, reject) => { resolveAccepted = resolve; rejectAccepted = reject; });
  const intercept = async (route: import('@playwright/test').Route) => {
    if (route.request().method() !== 'POST' || !first) return route.fallback();
    first = false;
    try {
      const response = await route.fetch({ maxRetries: 0 });
      const body = await response.json() as Record<string, any>;
      const observation = requests.at(-1);
      if (!observation) throw new Error('lost-ack interceptor did not observe its commit request');
      observation.status = response.status();
      observation.response = body;
      if (response.status() !== 200 || !['accepted', 'rebased'].includes(String(body.data?.status))) {
        throw new Error(`lost-ack route received non-accepted Runtime response: ${response.status()} ${JSON.stringify(body)}`);
      }
      await route.abort('connectionreset');
      resolveAccepted();
    } catch (error) {
      rejectAccepted(error);
    }
  };
  await page.route(commits, intercept);
  return { accepted, dispose: () => page.unroute(commits, intercept) };
}

export function transcriptRegenerate(page: Page) {
  return page.locator('[data-lane-kind="astrid.transcript"]')
    .getByRole('button', { name: 'Transcript actions' })
    .click()
    .then(() => page.getByRole('menuitem', { name: 'Regenerate transcript captions and replace edits' }).click());
}

export const sceneMoveShots = (page: Page) => page.getByTestId('scene-markers-move-shots').click();
