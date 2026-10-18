/**
 * The SOLE fixture authority for every fake/stub bridge surface.
 *
 * Consumers:
 * - `src/test/fakeBridgeRouter.ts` (vitest fetch-level router)
 * - `tests/e2e/timeline/astrid-bridge-stub.mjs` (node http stand-in)
 *
 * This module is plain ESM JavaScript (no TypeScript) because the node stub
 * imports it directly without a loader. Wire shapes here are frozen against
 * the phase-b `astrid serve` implementation (doc-27 §4.1): polling summaries
 * key identity as `task_id`, admission responses as `id`, gallery rows carry
 * `primary`/`variant_count`, detail carries `variants`.
 */

/** 26-char lowercase Crockford-style ULIDs, deterministic per suffix. */
export function fixtureUlid(suffix) {
  const stem = '01j8zcex4q7m4sjdy6g6';
  const pad = (suffix + 'aaaaaaaaaaaaaaaaaaaa').slice(0, 26 - stem.length);
  return `${stem}${pad}`;
}

export const FIXTURE_PROJECT = {
  slug: 'demo-project',
  name: 'Demo Project',
};

export const FIXTURE_TIMELINE_ID = 'demo-timeline';
export const AUDIO_REACTIVE_FIXTURE_TIMELINE_ID = 'audio-reactive-colour-timeline';
export const AUDIO_REACTIVE_OFFSET_FIXTURE_TIMELINE_ID = 'audio-reactive-colour-offset-timeline';
export const AUDIO_REACTIVE_OFFSET_START_FRAME = 6;
export const AUDIO_REACTIVE_OFFSET_INITIAL_COLOR = '#102030';

function createAudioReactiveColourShotComposition({
  timelineId = AUDIO_REACTIVE_FIXTURE_TIMELINE_ID,
  atSeconds = 0,
  initialColor = '#000000',
} = {}) {
  const projectId = FIXTURE_PROJECT.slug;
  const parentDocumentId = `${timelineId}-document`;
  const shotId = 'audio-reactive-colour-shot';
  const revisionId = 'audio-reactive-colour-shot-rev-1';
  const occurrenceId = 'audio-reactive-colour-occurrence-1';
  const outputIdentity = `project/${projectId}/document/${parentDocumentId}/occurrence/${occurrenceId}/output/final-video`;
  const stableDeepLink = `project/${projectId}/document/${parentDocumentId}/shot/${shotId}/revision/${revisionId}/occurrence/${occurrenceId}`;
  const audioDigest = 'sha256:fa17b6d0dc1e6ca7aed9833b0ceded944644f12b22964f081d7a982427f8ac29';
  const durationMs = 600;
  return {
    schema_version: 1,
    project: { project_id: projectId, document_id: parentDocumentId, role: 'project' },
    primary_timeline: {
      document_id: parentDocumentId,
      role: 'primary_timeline',
      head: { revision_id: `${timelineId}-head-1`, content_digest: `sha256:${'b'.repeat(64)}` },
    },
    shot_revisions: [{
      shot_id: shotId,
      revision_id: revisionId,
      document_role: 'shot_revision',
      content_digest: `sha256:${'c'.repeat(64)}`,
      internal_timeline_revision: {
        revision_id: `${revisionId}-timeline`,
        content_digest: `sha256:${'d'.repeat(64)}`,
        timeline: {
          tracks: [{ id: 'colour', kind: 'visual' }, { id: 'audio', kind: 'audio' }],
          clips: [
            { id: 'colour_map', clip_type: 'audio-reactive-colour', track: 'colour', at_ms: 0, duration_ms: durationMs, params: { schemaVersion: 1, initialColor, events: [{ id: 'first', frame: 2, color: '#203040' }, { id: 'second', frame: 4, color: '#405060' }] } },
            { id: 'audio_source', clip_type: 'media', track: 'audio', at_ms: 0, duration_ms: durationMs, asset_id: 'source_audio' },
          ],
        },
      },
      dependencies: [],
      assets: [{ asset_id: 'source_audio', object_id: 'fixture-media-audio', media_type: 'audio/wav', digest: audioDigest, scope: { project_id: projectId, shot_id: shotId }, role: 'source' }],
      generation_inputs: [],
      timing: { duration_ms: durationMs },
      audio: { track_id: 'audio', object_id: 'fixture-media-audio', digest: audioDigest, scope: { project_id: projectId } },
      provenance: { source: 'audio-reactive-colour-export-fixture', created_by: 'test' },
    }],
    occurrences: [{ occurrence_id: occurrenceId, parent_document_id: parentDocumentId, shot_id: shotId, revision_id: revisionId, ordinal: 0, at_ms: Math.round(atSeconds * 1000), duration_ms: durationMs, stable_deep_link: stableDeepLink, output_identity: outputIdentity }],
    cases: {
      missing_dependency: { shot_id: 'missing-shot', revision_id: 'missing-revision', expected: 'missing_dependency' },
      stale_write_rejection: { expected_head_revision_id: `${timelineId}-head-1`, submitted_head_revision_id: `${timelineId}-head-0`, expected_status: 409 },
    },
  };
}

/**
 * Timeline document + registry exactly as the editor's Local mode expects
 * them. `assetSrcBaseUrl` lets the node stub point display `src` fields at
 * its dev-server origin; vitest leaves it empty.
 */
export function createTimelineFixtures({ assetSrcBaseUrl = '' } = {}) {
  const src = (file) => `${assetSrcBaseUrl}/${file}`;
  return {
    timelineSummary: {
      timeline_id: FIXTURE_TIMELINE_ID,
      timeline_ulid: '01j0000000000000000000demo',
      slug: FIXTURE_TIMELINE_ID,
      name: 'Demo Timeline',
      is_default: true,
    },
    registry: {
      assets: {
        'demo-hero': {
          file: 'example-image1.jpg',
          src: src('example-image1.jpg'),
          type: 'image/jpeg',
          duration: 4,
          generationId: 'gen-demo-hero',
        },
        'demo-detail': {
          file: 'example-image2.jpg',
          src: src('example-image2.jpg'),
          type: 'image/jpeg',
          duration: 4,
          generationId: 'gen-demo-detail',
        },
        'demo-clip': {
          file: 'example-video.mp4',
          src: src('example-video.mp4'),
          type: 'video/mp4',
          duration: 5,
          generationId: 'gen-demo-clip',
        },
      },
    },
    config: {
      output: {
        resolution: '1280x720',
        fps: 30,
        file: 'demo.mp4',
        background: null,
        background_scale: null,
      },
      tracks: [
        { id: 'V1', kind: 'visual', label: 'V1', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
        { id: 'V2', kind: 'visual', label: 'V2', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
        { id: 'A1', kind: 'audio', label: 'A1', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
      ],
      clips: [
        { id: 'clip-hero', track: 'V1', at: 0, clipType: 'media', hold: 4, asset: 'demo-hero' },
        { id: 'clip-title', track: 'V1', at: 4, clipType: 'text', hold: 2.5, text: { content: 'Hello timeline' } },
        { id: 'clip-detail', track: 'V1', at: 6.5, clipType: 'media', hold: 4, asset: 'demo-detail' },
        { id: 'clip-video', track: 'V2', at: 1.5, clipType: 'media', hold: 5, asset: 'demo-clip' },
      ],
    },
  };
}

/**
 * The isolated browser/export fixture for Astrid's pinned
 * `audio-reactive-colour` semantic contract.  Keep this separate from the
 * general four-clip demo: the effect fast path is deliberately one visual
 * effect plus one audio clip, and must not be accidentally coupled to the
 * caption/Runaway paired-release fixture.
 *
 * The marker values and frame positions are copied from Astrid's pinned
 * renderer-parity fixture (`audio-reactive-colour.timeline.json`).  At 30fps
 * the 0.6s hold is exactly 18 frames, making the decoded MP4 boundary
 * assertions deterministic.
 */
export function createAudioReactiveColourFixtures({ assetSrcBaseUrl = '' } = {}) {
  const src = (file) => `${assetSrcBaseUrl}/${file}`;
  return {
    timelineSummary: {
      timeline_id: AUDIO_REACTIVE_FIXTURE_TIMELINE_ID,
      timeline_ulid: '01j0000000000000000000colour',
      slug: AUDIO_REACTIVE_FIXTURE_TIMELINE_ID,
      name: 'Audio Reactive Colour Fixture',
      is_default: false,
    },
    registry: {
      assets: {
        source_audio: {
          file: 'audio-reactive-colour-tone.wav',
          // Managed-media identity is canonical; file remains as a
          // compatibility/source locator for the isolated bridge fixture.
          media_id: 'fixture-media-audio',
          src: src('audio-reactive-colour-tone.wav'),
          type: 'audio/wav',
          duration: 0.6,
        },
      },
    },
    shotComposition: createAudioReactiveColourShotComposition(),
    config: {
      output: {
        resolution: '640x360',
        fps: 30,
        file: 'audio-reactive-colour.mp4',
        background: null,
        background_scale: null,
      },
      tracks: [
        { id: 'colour', kind: 'visual', label: 'Colour', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
        { id: 'audio', kind: 'audio', label: 'Audio', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
      ],
      clips: [
        {
          id: 'colour_map',
          at: 0,
          track: 'colour',
          clipType: 'audio-reactive-colour',
          hold: 0.6,
          params: {
            schemaVersion: 1,
            initialColor: '#000000',
            events: [
              { id: 'first', frame: 2, color: '#203040' },
              { id: 'second', frame: 4, color: '#405060' },
            ],
          },
        },
        {
          id: 'audio_source',
          at: 0,
          track: 'audio',
          clipType: 'media',
          asset: 'source_audio',
          from: 0,
          to: 0.6,
          speed: 1,
          volume: 1,
        },
      ],
    },
  };
}

/**
 * The same pinned colour contract with both clips starting after a deliberate
 * global gap. This catches renderers that apply marker frames in composition
 * coordinates instead of clip-relative coordinates.
 */
export function createOffsetAudioReactiveColourFixtures({ assetSrcBaseUrl = '' } = {}) {
  const base = createAudioReactiveColourFixtures({ assetSrcBaseUrl });
  const offsetSeconds = AUDIO_REACTIVE_OFFSET_START_FRAME / base.config.output.fps;
  return {
    ...base,
    timelineSummary: {
      ...base.timelineSummary,
      timeline_id: AUDIO_REACTIVE_OFFSET_FIXTURE_TIMELINE_ID,
      timeline_ulid: '01j0000000000000000000offset',
      slug: AUDIO_REACTIVE_OFFSET_FIXTURE_TIMELINE_ID,
      name: 'Audio Reactive Colour Offset Fixture',
    },
    config: {
      ...base.config,
      output: { ...base.config.output, file: 'audio-reactive-colour-offset.mp4' },
      clips: base.config.clips.map((clip) => ({
        ...clip,
        at: clip.at + offsetSeconds,
        ...(clip.clipType === 'audio-reactive-colour'
          ? { params: { ...clip.params, initialColor: AUDIO_REACTIVE_OFFSET_INITIAL_COLOR } }
          : {}),
      })),
    },
    shotComposition: createAudioReactiveColourShotComposition({
      timelineId: AUDIO_REACTIVE_OFFSET_FIXTURE_TIMELINE_ID,
      atSeconds: offsetSeconds,
      initialColor: AUDIO_REACTIVE_OFFSET_INITIAL_COLOR,
    }),
  };
}

/** One 1×1 red PNG — deterministic managed-media bytes. */
const PNG_1PX_BASE64 =
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
/** Minimal deterministic mp4-flavoured bytes (not a playable movie; size/range fixture only). */
const MP4_STUB_BYTES = new Uint8Array(2048).fill(0x2f);

/**
 * Seeded gallery journey: two generations with variants whose primary
 * variants point at managed media served through R9.
 */
export function createGalleryFixtures() {
  const mediaPng = {
    media_id: fixtureUlid('mediapng'),
    mime: 'image/png',
    bytes: Uint8Array.from(atob(PNG_1PX_BASE64), (c) => c.charCodeAt(0)),
  };
  const mediaMp4 = {
    media_id: fixtureUlid('mediamp4'),
    mime: 'video/mp4',
    bytes: MP4_STUB_BYTES,
  };

  const primaryVariantA = {
    id: fixtureUlid('varaatla'),
    generation_id: fixtureUlid('genaaaaaa'),
    media_id: mediaPng.media_id,
    variant_type: 'original',
    name: 'Original',
    params: {},
    is_primary: true,
    starred: false,
    viewed_at: null,
    created_at: '2026-08-20T10:00:00Z',
  };
  const secondaryVariantA = {
    ...primaryVariantA,
    id: fixtureUlid('varaaltb'),
    media_id: mediaMp4.media_id,
    is_primary: false,
    name: 'Alternate',
    created_at: '2026-08-20T10:05:00Z',
  };
  const primaryVariantB = {
    id: fixtureUlid('varbpric'),
    generation_id: fixtureUlid('genbbbbbb'),
    media_id: mediaMp4.media_id,
    variant_type: 'original',
    name: 'Original',
    params: {},
    is_primary: true,
    starred: true,
    viewed_at: null,
    created_at: '2026-08-21T09:00:00Z',
  };

  const detailA = {
    generation_id: fixtureUlid('genaaaaaa'),
    project_id: fixtureUlid('projsect'),
    task_id: null,
    type: 'image',
    name: null,
    based_on_generation_id: null,
    parent_generation_id: null,
    child_order: null,
    params: {},
    starred: false,
    deleted_at: null,
    created_at: '2026-08-20T10:00:00Z',
    updated_at: '2026-08-20T10:05:00Z',
    variants: [primaryVariantA, secondaryVariantA],
    items: [],
  };
  const detailB = {
    ...detailA,
    generation_id: fixtureUlid('genbbbbbb'),
    starred: true,
    created_at: '2026-08-21T09:00:00Z',
    updated_at: '2026-08-21T09:00:00Z',
    variants: [primaryVariantB],
  };

  // Gallery page rows: recency-first (created_at DESC), primary summary only.
  const pageRows = [detailB, detailA].map((detail) => ({
    generation_id: detail.generation_id,
    name: detail.name,
    type: detail.type,
    starred: detail.starred,
    created_at: detail.created_at,
    updated_at: detail.updated_at,
    primary: (() => {
      const primary = detail.variants.find((variant) => variant.is_primary);
      return primary ? { media_id: primary.media_id, variant_type: primary.variant_type } : null;
    })(),
    variant_count: detail.variants.length,
  }));

  return { media: [mediaPng, mediaMp4], details: [detailA, detailB], pageRows };
}

/** Families this fake admits; everything else maps to capability_unavailable. */
export const AVAILABLE_FAMILIES = ['image_generation', 'render_export', 'rendering.render'];

export function makeAdmittedTaskReadModel({ taskId, family = 'image_generation', capability = 'astrid.qwen_image' }) {
  const now = '2026-08-22T12:00:00Z';
  return {
    id: taskId,
    project_id: fixtureUlid('projsect'),
    capability,
    spec: {
      schema_version: 1,
      family,
      source_task_type: 'qwen_image',
      params: {},
      output_policy: { create_generation: true },
    },
    spec_hash: 'f'.repeat(64),
    input_manifest: [],
    status: 'queued',
    priority: 0,
    available_at: now,
    max_attempts: 3,
    run_id: null,
    run_ordinal: null,
    winning_attempt_id: null,
    cancel_request_id: null,
    cancel_requested_at: null,
    event_head_seq: 1,
    created_at: now,
    updated_at: now,
    finished_at: null,
    dependencies: [],
  };
}

/** Polling-summary projection of one task (the `_task_summary` wire shape). */
export function taskSummaryFromReadModel(readModel) {
  return {
    task_id: readModel.id,
    project_id: readModel.project_id,
    capability: readModel.capability,
    status: readModel.status,
    spec: readModel.spec,
    priority: readModel.priority,
    max_attempts: readModel.max_attempts,
    created_at: readModel.created_at,
    updated_at: readModel.updated_at,
    finished_at: readModel.finished_at ?? null,
    winning_attempt_id: readModel.winning_attempt_id ?? null,
  };
}

/** Bounded current-attempt extra (fence 409s and running-task reads). */
export function makeAttemptWireShape({ attemptNo = 1, status = 'running', statusVersion = 2 }) {
  return {
    attempt_id: fixtureUlid('attemptid'),
    attempt_no: attemptNo,
    status,
    status_version: statusVersion,
    lease_id: fixtureUlid('leaseiden'),
    lease_expires_at: '2026-08-22T12:05:00Z',
    heartbeat_counter: 0,
    last_heartbeat_at: null,
  };
}

/**
 * Mutable journey state shared by the vitest router and (via delegation) the
 * node stub. Tests mutate it directly to drive poll/cancel scenarios.
 */
export function createJourneyState({ assetSrcBaseUrl } = {}) {
  const timeline = createTimelineFixtures({ assetSrcBaseUrl });
  const gallery = createGalleryFixtures();
  return {
    project: FIXTURE_PROJECT,
    timelineSummary: timeline.timelineSummary,
    registry: structuredClone(timeline.registry),
    config: structuredClone(timeline.config),
    configVersion: 1,
    /** task_id → polling summary. */
    tasks: new Map(),
    /** IdempotencyKey → serialized admit body (receipt replay/mismatch). */
    receipts: new Map(),
    /** Admission sequence for deterministic task ULIDs. */
    admissions: 0,
    galleryPageRows: gallery.pageRows,
    galleryDetails: gallery.details,
    /** media_id → {mime, bytes}. */
    media: new Map(gallery.media.map((entry) => [entry.media_id, { mime: entry.mime, bytes: entry.bytes }])),
  };
}
