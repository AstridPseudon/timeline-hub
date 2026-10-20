import { useEffect, useId, useRef, useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { Input } from '@/shared/components/ui/input.tsx';
import type { ClipSetParamsArgs, DocumentPin } from '@/integrations/runtime/timeline-commit-types.ts';
import type { SubmittedClipParamsInput, TimelineOps } from '@/sdk/video/timeline/timelineOps.ts';
import type { CommandSessionState } from '../../commands/commitSession.ts';
import { equal } from '../../commands/clipMovePrimitives.ts';
import type { ResolvedTimelineClip } from '../../types/index.ts';
import type { AstridElementParamDescriptor } from './astrid-element-param-descriptor.ts';

export interface SelectedElementParamFieldsProps {
  clip: ResolvedTimelineClip;
  descriptor: AstridElementParamDescriptor;
  retainedDocumentPin: DocumentPin;
  timelineOps?: Pick<TimelineOps, 'setClipParams' | 'getSubmittedClipParams'>;
  commandState?: CommandSessionState;
}

function inputDrafts(args: ClipSetParamsArgs): Record<string, string> {
  return Object.fromEntries([
    ...Object.entries(args.values).map(([name, value]) => [name, JSON.stringify(value)]),
    ...args.clear.map((name) => [name, '']),
  ]);
}

/** Raw JSON drafts: schema properties describe controls, never authorize values. */
export function SelectedElementParamFields({ clip, descriptor, retainedDocumentPin, timelineOps, commandState }: SelectedElementParamFieldsProps) {
  const id = useId();
  const input = timelineOps?.getSubmittedClipParams?.(clip.id);
  const pending = input && !input.accepted ? input : undefined;
  const originalPin = useRef(structuredClone(pending?.args.schema_source ?? retainedDocumentPin));
  const request = useRef<AbortController>();
  const edits = useRef(new Map<string, number>());
  useEffect(() => () => { request.current?.abort(); }, []);
  const [drafts, setDrafts] = useState<Record<string, string>>(() => pending ? inputDrafts(pending.args) : {});
  const [submitted, setSubmitted] = useState<{ input: SubmittedClipParamsInput; drafts: Record<string, string>; edits: Map<string, number> } | null>(() =>
    pending ? { input: pending, drafts: inputDrafts(pending.args), edits: new Map() } : null);
  const [error, setError] = useState<string | null>(null);
  const [reading, setReading] = useState(false);
  const accepted = submitted?.input.accepted;
  useEffect(() => {
    if (!submitted || !accepted) return;
    setDrafts((current) => Object.fromEntries(Object.entries(current).filter(([name, value]) =>
      !Object.hasOwn(submitted.drafts, name) || submitted.drafts[name] !== value || submitted.edits.get(name) !== edits.current.get(name))));
    setSubmitted(null);
  }, [accepted, submitted]);
  useEffect(() => {
    if (!pending || pending.id === submitted?.input.id) return;
    const restored = inputDrafts(pending.args);
    originalPin.current = structuredClone(pending.args.schema_source!);
    setDrafts((current) => ({ ...restored, ...current }));
    setSubmitted({ input: pending, drafts: restored, edits: new Map() });
  }, [pending, submitted?.input.id]);
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
      const submittedEdits = new Map(edits.current);
      setReading(true);
      const controller = new AbortController();
      request.current = controller;
      await timelineOps.setClipParams(clip.id, args, controller.signal);
      const queued = timelineOps.getSubmittedClipParams?.(clip.id);
      if (queued) setSubmitted({ input: queued, drafts, edits: submittedEdits });
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
      const accepted = clip.params && Object.hasOwn(clip.params, name) ? JSON.stringify(clip.params[name]) ?? '' : '';
      return <div key={name} className="space-y-1">
        <label htmlFor={`${id}-${name}`}>{label}</label>
        <Input id={`${id}-${name}`} value={Object.hasOwn(drafts, name) ? drafts[name] : accepted}
          onChange={(event) => { edits.current.set(name, (edits.current.get(name) ?? 0) + 1); setDrafts((current) => ({ ...current, [name]: event.target.value })); setError(null); }} />
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
