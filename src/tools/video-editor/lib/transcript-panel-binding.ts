import type { PanelVideoAdapter } from '@/sdk/ui.ts';
import type { TimelineStoreApi } from '../hooks/timelineStore.ts';
import { createTranscriptPanelAdapter } from './transcript-panel-adapter.ts';

/** Called once per existing host/store/video identity at the app panel boundary. */
export function bindTranscriptPanelVideo(store: TimelineStoreApi, video: PanelVideoAdapter): PanelVideoAdapter {
  const transcript = createTranscriptPanelAdapter({
    getData: () => store.getState().data.dataRef.current,
    subscribe: (listener) => {
      const unsubscribe = store.subscribe((next, previous) => {
        if (next.data.data !== previous.data.data) listener();
      });
      return { dispose: unsubscribe };
    },
    video,
    editText: (edit) => store.getState().ops.transcriptHost?.editText(edit)
      ?? { ok: false, code: 'timeline_unavailable', message: 'Wait for the timeline to finish loading before correcting text.' },
    importTranscript: (input) => {
      const host = store.getState().ops.transcriptHost;
      if (!host) throw Object.assign(new Error('Wait for the timeline to finish loading before importing a transcript.'), { code: 'timeline_not_loaded' });
      return host.importTranscript(input);
    },
  });
  return { ...video, transcript };
}
