import { vi } from 'vitest';
import { createTimelineStore } from '../hooks/timelineStore.ts';
import { buildTimelineData, type TimelineData } from './timeline-data.ts';
import { createTimelineViewStore } from './timeline-view-store.ts';
import { createTranscriptPanelHost } from './transcript-panel-host.ts';
import { bindTranscriptPanelVideo } from './transcript-panel-binding.ts';
import type { TimelineConfig } from '../types/index.ts';

export async function setupTranscriptHost() {
  const config: TimelineConfig = {
    output: { resolution: '1920x1080', fps: 30, file: 'out.mp4' },
    tracks: [{ id: 'v', kind: 'video', label: 'Video', muted: false }],
    clips: [{ id: 'clip', asset: 'media', at: 0, from: 0, to: 10, track: 'v' },
      { id: 'repeat', asset: 'media', at: 20, from: 0, to: 10, track: 'v' },
      { id: 'sound', asset: 'audio', at: 0, from: 0, to: 10, track: 'v' },
      { id: 'picture', asset: 'image', at: 0, from: 0, to: 10, track: 'v' }],
  };
  const data = await buildTimelineData(config, { assets: {
    media: { file: 'Interview.mp4', type: 'video/mp4', duration: 10 },
    audio: { file: 'Audio.wav', type: 'audio/wav', duration: 10 },
    image: { file: 'Photo.png', type: 'image/png' },
    unused: { file: 'Other.mp4', type: 'video/mp4', duration: 10 },
  } }, (file) => file, 1);
  const store = createTimelineStore();
  const dataRef: { current: TimelineData | null } = { current: data };
  const commitData = vi.fn((next: TimelineData) => {
    dataRef.current = next;
    const current = store.getState().data;
    store.getState().syncDataSlice({ ...current, data: next, dataRef });
  });
  let allowed = true;
  const host = createTranscriptPanelHost({ dataRef, commitData, editability: { check: () => ({ allowed }), checkTimeline: () => ({ allowed }) } });
  store.getState().syncDataSlice({ ...store.getState().data, data, dataRef });
  store.getState().syncOpsSlice({ ...store.getState().ops, transcriptHost: host });
  const view = createTimelineViewStore();
  const seek = vi.fn();
  const video = bindTranscriptPanelVideo(store, { view, seek });
  return { store, view, seek, video, host, commitData, dataRef, lock: () => { allowed = false; } };
}

