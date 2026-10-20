import { useEffect, useId, useRef, useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { Input } from '@/shared/components/ui/input.tsx';
import type { ClipSetParamsArgs, DocumentPin } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelineOps } from '@/sdk/video/timeline/timelineOps.ts';
import type { CommandSessionState } from '../../commands/commitSession.ts';
import { equal } from '../../commands/clipMovePrimitives.ts';
import type { ResolvedTimelineClip } from '../../types/index.ts';
import type { AstridElementParamDescriptor } from './astrid-element-param-descriptor.ts';

export interface SelectedElementParamFieldsProps {
  clip: ResolvedTimelineClip;
  descriptor: AstridElementParamDescriptor;
  retainedDocumentPin: DocumentPin;
  timelineOps?: Pick<TimelineOps, 'setClipParams'>;
  commandState?: CommandSessionState;
}

/** Raw JSON drafts: schema properties describe controls, never authorize values. */
export function SelectedElementParamFields({ clip, descriptor, retainedDocumentPin, timelineOps, commandState }: SelectedElementParamFieldsProps) {
  const id = useId();
  const originalPin = useRef(structuredClone(retainedDocumentPin));
  const request = useRef<AbortController>();
  useEffect(() => () => { request.current?.abort(); }, []);
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState<Record<string, string> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [reading, setReading] = useState(false);
  useEffect(() => {
    if (!submitted || commandState?.status !== 'saved') return;
    setDrafts((current) => Object.fromEntries(Object.entries(current).filter(([name, value]) =>
      !Object.hasOwn(submitted, name) || submitted[name] !== value)));
    setSubmitted(null);
  }, [commandState?.status, submitted]);
  const properties = (descriptor.schema as { properties: Record<string, { title?: string; description?: string }> }).properties;
  const apply = async () => {
    setError(null);
    try {
      if (!equal(originalPin.current, retainedDocumentPin)) throw new Error('Retained schema pin changed; draft preserved.');
      if (!timelineOps?.setClipParams || !commandState) throw new Error('Selected parameter commands are unavailable; draft preserved.');
      const args: ClipSetParamsArgs = { values: {}, clear: [], schema_source: structuredClone(originalPin.current) };
      for (const [name, draft] of Object.entries(drafts)) {
        if (draft.trim() === '') args.clear.push(name);
        else Object.defineProperty(args.values, name, { value: JSON.parse(draft), enumerable: true });
      }
      setReading(true);
      const controller = new AbortController();
      request.current = controller;
      await timelineOps.setClipParams(clip.id, args, controller.signal);
      setSubmitted(drafts);
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : String(failure));
    } finally {
      setReading(false);
    }
  };

  return <div className="space-y-3">
    <p className="text-xs text-muted-foreground">Enter JSON values; leave blank to clear. Schema details are hints. Accepted values remain in the timeline until provider acceptance.</p>
    {Object.entries(properties).map(([name, hints]) => {
      const label = hints?.title ?? name;
      const accepted = JSON.stringify(clip.params?.[name]) ?? '';
      return <div key={name} className="space-y-1">
        <label htmlFor={`${id}-${name}`}>{label}</label>
        <Input id={`${id}-${name}`} value={Object.hasOwn(drafts, name) ? drafts[name] : accepted}
          onChange={(event) => { setDrafts((current) => ({ ...current, [name]: event.target.value })); setError(null); }} />
        <output aria-label={`${label} accepted value`}>{accepted || 'absent'}</output>
        {hints?.description && <p className="text-xs text-muted-foreground">{hints.description}</p>}
      </div>;
    })}
    <Button type="button" disabled={reading || commandState?.status === 'pending' || !Object.keys(drafts).length}
      onClick={() => { void apply(); }}>Apply parameters</Button>
    <p aria-label="Parameter command status" role={error || commandState?.status === 'error' || commandState?.status === 'conflict' ? 'alert' : 'status'}>
      {error ?? (reading ? 'PENDING retained parameter inputs; draft preserved' : commandState?.error
        ?? (commandState?.status === 'saved' && Object.keys(drafts).length ? 'Draft parameters; not submitted' : commandState?.status ?? 'Draft'))}
    </p>
  </div>;
}
