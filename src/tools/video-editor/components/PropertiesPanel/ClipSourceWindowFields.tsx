import { useId, useRef, useState } from 'react';
import { NumberInput } from '@/shared/components/ui/number-input.tsx';
import {
  captureClipTrimEdit,
  submitClipTrimEdit,
  type CapturedClipTrim,
  type ClipTrimCapturePort,
} from '@/tools/video-editor/commands/clipTrimGesture.ts';
import type { TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { ResolvedTimelineClip } from '@/tools/video-editor/types/index.ts';
import { FieldLabel } from './clip-panel-primitives.tsx';

type Endpoint = 'from' | 'to';

/** Local source drafts keep the focus-time guards until one discrete commit. */
export function ClipSourceWindowFields({ clip, current, port, readOnly }: {
  clip: ResolvedTimelineClip;
  current?: TimelineData;
  port?: ClipTrimCapturePort;
  readOnly: boolean;
}) {
  const id = useId();
  const [draft, setDraft] = useState<Partial<Record<Endpoint, number | null>>>({});
  const [error, setError] = useState<string | null>(null);
  const edits = useRef<Partial<Record<Endpoint, {
    captured?: CapturedClipTrim;
    error?: string;
    changed: boolean;
    initial: number;
  }>>>({});
  const displayed = (field: Endpoint) => field === 'from' ? clip.from ?? 0 : clip.to ?? clip.assetEntry?.duration ?? 5;
  const begin = (field: Endpoint) => {
    if (readOnly || edits.current[field]) return;
    const edit: NonNullable<typeof edits.current[Endpoint]> = { changed: false, initial: displayed(field) };
    edits.current[field] = edit;
    try {
      if (!current) throw new Error('Source trim requires the displayed timeline.');
      if (current.config.pinnedShotGroups?.some((group) => group.clipIds.includes(clip.id))) {
        throw new Error('Source trim requires one ungrouped parent clip.');
      }
      edit.captured = captureClipTrimEdit(port, current, clip.id);
      setError(null);
    } catch (cause) {
      edit.error = cause instanceof Error ? cause.message : 'Source trim capture failed.';
      setError(edit.error);
    }
  };
  const commit = (field: Endpoint, value: number | null) => {
    const edit = edits.current[field];
    delete edits.current[field];
    if (readOnly || !edit?.changed) return;
    try {
      if (!edit.captured) throw new Error(edit.error ?? 'Source trim capture is unavailable.');
      if (value === null || !Number.isFinite(value)) throw new Error('Source trim requires a finite source time.');
      if (value !== edit.initial) {
        submitClipTrimEdit(edit.captured, field === 'from' ? { in_s: value } : { out_s: value });
      }
      setDraft((previous) => { const next = { ...previous }; delete next[field]; return next; });
      setError(null);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Source trim failed.');
    }
  };

  return <>
    {(['from', 'to'] as const).map((field) => (
      <div key={field} className="space-y-2"
        onFocusCapture={() => begin(field)} onPointerDownCapture={() => begin(field)}
        onKeyDownCapture={(event) => { if (event.key !== 'Tab') begin(field); }}
        onPasteCapture={() => begin(field)}
        onClickCapture={(event) => { if (event.detail === 0) begin(field); }}
        onBlur={(event) => {
          if (!event.currentTarget.contains(event.relatedTarget as Node | null)) delete edits.current[field];
        }}>
        <div id={`${id}-${field}`}><FieldLabel>{field === 'from' ? 'Source In' : 'Source Out'}</FieldLabel></div>
        <NumberInput
          value={Object.prototype.hasOwnProperty.call(draft, field) ? draft[field]! : displayed(field)}
          min={0}
          step={0.1}
          aria-labelledby={`${id}-${field}`}
          aria-describedby={error ? `${id}-error` : undefined}
          aria-invalid={Boolean(error)}
          onChange={(value) => {
            if (readOnly) return;
            const edit = edits.current[field] ?? { initial: displayed(field), changed: false,
              error: 'Begin a source trim by focusing the source control.' };
            edits.current[field] = edit;
            edit.changed = true;
            setDraft((previous) => ({ ...previous, [field]: value }));
          }}
          onValueCommitted={(value) => commit(field, value)}
        />
      </div>
    ))}
    {error && <div id={`${id}-error`} role="alert" className="text-sm text-destructive">{error}</div>}
  </>;
}
