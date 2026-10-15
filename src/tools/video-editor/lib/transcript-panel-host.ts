import type { TranscriptPanelAdapter } from '@/sdk/video/transcript.ts';
import { createTranscriptImportCallback } from '../data/typed/importTranscriptHandoff.ts';
import { commitTranscriptTextEdit } from './transcript-text-edit.ts';

/** App-only capability: neither canonical refs nor commit functions cross the SDK boundary. */
export type TranscriptPanelHost = Required<Pick<TranscriptPanelAdapter, 'editText' | 'importTranscript'>>;
export function createTranscriptPanelHost(
  input: Parameters<typeof commitTranscriptTextEdit>[0],
): TranscriptPanelHost {
  const importTranscript = createTranscriptImportCallback(input);
  return {
    editText: (edit) => {
      const result = commitTranscriptTextEdit(input, edit);
      // The mutation helper's replacement source map is private to the host.
      return result.ok ? { ok: true, changed: result.changed } : result;
    },
    importTranscript: (document) => {
      if (input.editability?.checkTimeline && !input.editability.checkTimeline().allowed) {
        throw Object.assign(new Error('This timeline is currently read-only. Reopen it with editing access before importing a transcript.'), { code: 'timeline_read_only' });
      }
      return importTranscript(document);
    },
  };
}
