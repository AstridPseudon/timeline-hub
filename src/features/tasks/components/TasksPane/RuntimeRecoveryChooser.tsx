import React, { useEffect, useMemo, useRef, useState } from 'react';
import { AstridRuntimeClient } from '@/integrations/runtime/client';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider';
import { ShotSelector } from '@/shared/components/selectors/ShotSelector';
import { Button } from '@/shared/components/ui/button';
import { Input } from '@/shared/components/ui/input';
import {
  assertRuntimeRecoveryHead, assertRuntimeRecoverySource, freezeRecoveryValue, loadRuntimeRecoveryDestinations,
  type RuntimeRecoveryDestinations, type RuntimeRecoveryPlacementDraft, type RuntimeRecoverySource,
} from './utils/runtimeRecoveryDestinations';

export interface RuntimeRecoveryChooserProps {
  projectId: string | null;
  timelineId: string | null;
  source: RuntimeRecoverySource;
  // No current App service exposes a qualified native ADD callback. TasksPane
  // leaves this absent; the typed local seam carries no commit authority.
  onRequestPlacement?: (draft: RuntimeRecoveryPlacementDraft, signal?: AbortSignal) => Promise<void>;
}

export function RuntimeRecoveryChooser(props: RuntimeRecoveryChooserProps) {
  // Remount local state when any explicit scope/source changes, including a
  // replacement output for the same task. Pending reads cannot populate it.
  const { projectId, timelineId, source } = props;
  const key = JSON.stringify([projectId, timelineId, source]);
  return <RecoverySelection key={key} {...props} />;
}

function RecoverySelection({ projectId, timelineId, source, onRequestPlacement }: RuntimeRecoveryChooserProps) {
  const client = useMemo(() => new AstridRuntimeClient(), []);
  const provider = useMemo(() => projectId ? new RuntimeDataProvider({ projectId }) : null, [projectId]);
  const [read, setRead] = useState<RuntimeRecoveryDestinations | null>(null);
  const [destinationId, setDestinationId] = useState('');
  const [on, setOn] = useState('');
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [status, setStatus] = useState('Checking selected timeline and output…');
  const [valid, setValid] = useState(false);
  const [pending, setPending] = useState(false);
  const active = useRef<object | null>(null);
  const placementRequest = useRef<AbortController | null>(null);
  const editVersion = useRef(0);
  const changed = () => { editVersion.current++; placementRequest.current?.abort(); };

  useEffect(() => {
    const scope = {};
    active.current = scope;
    let checking = false;
    let initialRead: RuntimeRecoveryDestinations | null = null;
    if (!projectId || !timelineId || !provider) {
      setStatus('Select a Runtime project and timeline in the editor to choose a destination.');
      return () => { active.current = null; };
    }
    const check = async () => {
      if (checking) return;
      checking = true;
      try {
        await assertRuntimeRecoverySource(client, projectId, source);
        const destinations = await loadRuntimeRecoveryDestinations(provider, client, projectId, timelineId);
        if (active.current !== scope) return;
        if (initialRead && (initialRead.basis.head.revisionId !== destinations.basis.head.revisionId
          || initialRead.basis.head.publicationId !== destinations.basis.head.publicationId)) {
          setValid(false);
          setStatus('Timeline changed. Selection draft kept; reopen the output to refresh destinations.');
          return;
        }
        initialRead ??= destinations;
        setRead(initialRead);
        setValid(true);
        setStatus(destinations.bindings.length ? 'Choose a destination and explicit timing.' : 'No explicit visual destination is available on this timeline.');
      } catch {
        if (active.current === scope) {
          setValid(false);
          setStatus('Selected timeline or output is unavailable or changed. Selection draft kept.');
        }
      } finally { checking = false; }
    };
    void check();
    const interval = window.setInterval(() => { void check(); }, 5_000);
    return () => { active.current = null; placementRequest.current?.abort(); window.clearInterval(interval); };
  }, [client, provider, projectId, timelineId, source]);

  const destination = read?.bindings.find((row) => row.id === destinationId);
  const numbers = [on, from, to].map(Number);
  const complete = destination && [on, from, to].every((value) => value.trim())
    && numbers.every((value) => Number.isFinite(value) && value >= 0) && numbers[2] > numbers[1];
  const request = async () => {
    if (!complete || !valid || !read || !destination || !projectId || !timelineId || !onRequestPlacement || pending) return;
    const version = editVersion.current;
    const scope = active.current;
    const controller = new AbortController();
    placementRequest.current = controller;
    setPending(true);
    try {
      await Promise.all([
        assertRuntimeRecoverySource(client, projectId, source),
        assertRuntimeRecoveryHead(client, projectId, timelineId, read.basis),
      ]);
      if (!scope || active.current !== scope || editVersion.current !== version) return;
      await onRequestPlacement(freezeRecoveryValue(structuredClone({ projectId, timelineId, basis: read.basis, source,
        destination, on: numbers[0], sourceWindow: { from: numbers[1], to: numbers[2] } })), controller.signal);
      // Acceptance/placement presentation belongs to the qualified service.
    } catch {
      if (active.current === scope && editVersion.current === version) {
        setValid(false);
        setStatus('Placement unavailable or source changed. Selection draft kept.');
      }
    } finally { if (active.current === scope) setPending(false); }
  };

  return <section aria-label="Runtime manual destination" className="absolute bottom-4 left-4 z-[70] max-w-sm space-y-2 rounded bg-background p-3 text-foreground"
    onClick={(event) => event.stopPropagation()} onPointerDown={(event) => event.stopPropagation()}>
    <p role="status" className="text-xs">{status}</p>
    {read && <>
      <ShotSelector shots={read.bindings} value={destinationId} placeholder="Select destination"
        onValueChange={(value) => { changed(); setDestinationId(value); }} />
      <div className="flex gap-2">
        {([
          ['Timeline start (seconds)', on, setOn], ['Source from (seconds)', from, setFrom], ['Source to (seconds)', to, setTo],
        ] as const).map(([label, value, setValue]) => <label key={label} className="text-xs">{label}
          <Input type="number" min="0" step="any" value={value} onChange={(event) => { changed(); setValue(event.target.value); }} />
        </label>)}
      </div>
      <p className="text-xs">Selection draft uses the output opened from this task.</p>
    </>}
    {!onRequestPlacement && <p className="text-xs">Manual placement unavailable: native command service is not connected. Selection stays a draft.</p>}
    {onRequestPlacement && <Button disabled={!complete || !valid || pending} onClick={() => { void request(); }}>Request placement</Button>}
  </section>;
}
