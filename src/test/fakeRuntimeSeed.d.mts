// The fake Runtime's UI-facing seed (see fakeRuntimeSeed.mjs).

export interface BridgeTimelineFixtures {
  readonly timelineSummary: Record<string, unknown> & { timeline_id: string };
  readonly registry: { assets: Record<string, Record<string, unknown> & { file: string; type: string }> };
  readonly config: Record<string, unknown> & { clips: Array<Record<string, unknown>> };
}

export function fixtureUlid(suffix: string): string;

export const FIXTURE_PROJECT: { readonly slug: string; readonly name: string };
export const FIXTURE_TIMELINE_ID: string;
export const AUDIO_REACTIVE_FIXTURE_TIMELINE_ID: string;
export const AUDIO_REACTIVE_OFFSET_FIXTURE_TIMELINE_ID: string;
export const AUDIO_REACTIVE_OFFSET_START_FRAME: number;
export const AUDIO_REACTIVE_OFFSET_INITIAL_COLOR: string;

export function createTimelineFixtures(options?: { assetSrcBaseUrl?: string }): BridgeTimelineFixtures;
export function createAudioReactiveColourFixtures(options?: { assetSrcBaseUrl?: string }): BridgeTimelineFixtures;
export function createOffsetAudioReactiveColourFixtures(options?: { assetSrcBaseUrl?: string }): BridgeTimelineFixtures;
export function createGalleryFixtures(): {
  readonly media: Array<{ media_id: string; mime: string; bytes: Uint8Array }>;
  readonly details: Array<Record<string, unknown>>;
  readonly pageRows: Array<Record<string, unknown>>;
};
