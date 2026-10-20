import { useCallback, useEffect, useRef, useState, type ChangeEvent, type KeyboardEvent } from 'react';
import { Check, Trash2 } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { FieldLabel, TrackSettingsFields } from '../TimelineEditor/TrackLabel.tsx';
import type { TrackDefinition } from '@/tools/video-editor/types/index.ts';
import type { TrackLabelDraft, TrackLabelEditStart } from '@/tools/video-editor/commands/trackLabelGesture.ts';

/** Touch track editing shares the Inspector with clip actions and properties. */
export function TrackInspector({ track, hasClips, readOnly = false, onChange, onLabelEditStart, onAddTrack, onRemove }: {
  track: TrackDefinition;
  hasClips: boolean;
  readOnly?: boolean;
  onChange: (trackId: string, patch: Partial<TrackDefinition>) => void;
  onLabelEditStart?: TrackLabelEditStart;
  onAddTrack: (kind: 'visual' | 'audio') => void;
  onRemove: (trackId: string) => void;
}) {
  const [confirmingDelete, setConfirmingDelete] = useState(false);
  useEffect(() => {
    if (!confirmingDelete) return;
    const timer = setTimeout(() => setConfirmingDelete(false), 2000);
    return () => clearTimeout(timer);
  }, [confirmingDelete]);

  const localNameDrafts = useRef(new Map<string, TrackLabelDraft>());
  const nameDrafts = onLabelEditStart?.drafts ?? localNameDrafts.current;
  const [, updateNameDraft] = useState(0);
  const refreshNameDraft = () => updateNameDraft((version) => version + 1);
  const nameEdit = nameDrafts.get(track.id);
  const nameError = nameEdit?.error ?? null;
  const [submittedName, setSubmittedName] = useState<{
    owner: typeof nameDrafts; trackId: string; value: string;
  } | null>(null);
  useEffect(() => setSubmittedName(null), [track.label, track.id, nameDrafts]);
  const nameValue = nameEdit?.value ?? (submittedName?.owner === nameDrafts && submittedName.trackId === track.id
    ? submittedName.value : track.label);

  const beginNameEdit = () => {
    if (nameDrafts.has(track.id)) return;
    const edit: TrackLabelDraft = { value: nameValue, dirty: false };
    nameDrafts.set(track.id, edit);
    try {
      if (!onLabelEditStart) throw new Error('Track label command capture is unavailable.');
      edit.finish = onLabelEditStart(track.id);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Track rename is unavailable.';
      edit.captureError = message;
      edit.error = message;
    }
    refreshNameDraft();
  };

  const finishNameEdit = () => {
    const edit = nameDrafts.get(track.id);
    if (!edit) return;
    if (edit.captureError) return;
    if (edit.dirty) {
      try {
        edit.finish?.(edit.value);
      } catch (error) {
        edit.error = error instanceof Error ? error.message : 'Track rename was refused.';
        refreshNameDraft();
        return;
      }
      setSubmittedName({ owner: nameDrafts, trackId: track.id, value: edit.value });
    } else {
      setSubmittedName(null);
    }
    nameDrafts.delete(track.id);
    refreshNameDraft();
  };

  const nameInputFocusedRef = useRef<(() => void) | null>(null);
  const nameInputRef = useCallback((node: HTMLInputElement | null) => {
    if (!node && nameInputFocusedRef.current) {
      const finish = nameInputFocusedRef.current;
      nameInputFocusedRef.current = null;
      finish();
    }
  }, []);
  const nameInputProps = {
    ref: nameInputRef,
    value: nameValue,
    'aria-label': 'Track name',
    'aria-invalid': nameError ? true : undefined,
    onFocus: () => {
      nameInputFocusedRef.current = finishNameEdit;
      beginNameEdit();
    },
    onChange: (event: ChangeEvent<HTMLInputElement>) => {
      if (!onLabelEditStart) {
        onChange(track.id, { label: event.target.value });
        return;
      }
      beginNameEdit();
      const edit = nameDrafts.get(track.id);
      if (edit) {
        edit.dirty = true;
        edit.value = event.target.value;
      }
      refreshNameDraft();
    },
    onBlur: () => {
      nameInputFocusedRef.current = null;
      finishNameEdit();
    },
    onKeyDown: (event: KeyboardEvent<HTMLInputElement>) => {
      if (event.key === 'Enter' && !event.nativeEvent.isComposing) {
        event.preventDefault();
        event.stopPropagation();
        finishNameEdit();
      }
    },
  };

  // Where the Inspector is wide (iPad) the fields and actions take two columns, so the whole
  // track fits without scrolling; a phone stacks them.
  return <div className="@container">
    <fieldset disabled={readOnly} className="min-w-0 space-y-4 [&_[role=combobox]]:h-11" aria-label="Track settings">
      <div className="space-y-1.5">
        <FieldLabel>Name</FieldLabel>
        <input
          className="h-11 w-full rounded-md border border-border bg-background px-3 text-base outline-none focus-visible:ring-2 focus-visible:ring-ring"
          {...nameInputProps}
        />
      </div>
      {nameError && <p role="alert" className="text-xs text-destructive">{nameError}</p>}
      <TrackSettingsFields
        track={track}
        onChange={onChange}
        disabled={readOnly}
        className="@[34rem]:grid @[34rem]:grid-cols-2 @[34rem]:items-start @[34rem]:gap-4 @[34rem]:space-y-0"
      />
      <div className="grid grid-cols-2 gap-2 @[34rem]:grid-cols-3">
        <Button type="button" variant="secondary" className="h-11 min-w-0 px-2" onClick={() => onAddTrack('visual')}>Add video track</Button>
        <Button type="button" variant="secondary" className="h-11 min-w-0 px-2" onClick={() => onAddTrack('audio')}>Add audio track</Button>
        <Button
          type="button"
          variant="outline"
          className={`col-span-2 h-11 min-w-0 gap-1.5 @[34rem]:col-span-1 ${confirmingDelete ? 'border-destructive text-destructive' : ''}`}
          onClick={() => {
            if (hasClips && !confirmingDelete) setConfirmingDelete(true);
            else {
              setConfirmingDelete(false);
              onRemove(track.id);
            }
          }}
        >
          {confirmingDelete ? <Check className="h-4 w-4" /> : <Trash2 className="h-4 w-4" />}
          {confirmingDelete ? 'Tap again to confirm deletion' : 'Delete track'}
        </Button>
      </div>
    </fieldset>
  </div>;
}
