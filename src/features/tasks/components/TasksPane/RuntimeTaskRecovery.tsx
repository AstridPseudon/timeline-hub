import React, { useEffect, useMemo, useRef, useState } from 'react';
import { AstridRuntimeClient } from '@/integrations/runtime/client';
import type { ManagedOutput, MediaSelection, Task } from '@/integrations/runtime/generated';
import { Button } from '@/shared/components/ui/button';
import { bridgeMediaUrl } from '@/shared/lib/media/bridgeMediaUrl';
import { listAllRuntimeManagedOutputs } from './hooks/useRuntimeTasks';
import { isRuntimeRecoveryOutput, readRuntimeRecoverySelection, runtimeTaskRecoveryPresentation } from './utils/runtimeTaskRecovery';

export type OpenRuntimeTaskOutput = (task: Task, output: ManagedOutput, selection: MediaSelection) => void;

interface RecoveryRead {
  task: Task;
  projectId: string;
  outputs: { output: ManagedOutput; selection: MediaSelection | null }[];
}

export function RuntimeTaskRecovery({ task, projectId, onOpenOutput }: {
  task: Task;
  projectId: string;
  onOpenOutput?: OpenRuntimeTaskOutput;
}) {
  const client = useMemo(() => new AstridRuntimeClient(), []);
  const [read, setRead] = useState<RecoveryRead | null>(null);
  const [opening, setOpening] = useState<string | null>(null);
  const [actionError, setActionError] = useState(false);
  const presentation = runtimeTaskRecoveryPresentation(task, projectId);
  const candidate = Boolean(presentation);

  useEffect(() => {
    let active = true;
    let fetching = false;
    setRead(null);
    setOpening(null);
    setActionError(false);
    if (!candidate) return;
    const refresh = async () => {
      if (fetching) return;
      fetching = true;
      try {
        const outputs = (await listAllRuntimeManagedOutputs(client, task.task_id))
          .filter((output) => isRuntimeRecoveryOutput(task, output));
        if (!active) return;
        const rows = await Promise.all(outputs.map(async (output) => ({
          output,
          selection: await readRuntimeRecoverySelection(client, projectId, output).catch(() => null),
        })));
        if (active) setRead({ task, projectId, outputs: rows });
      } catch {
        if (active) setRead(null);
      } finally {
        fetching = false;
      }
    };
    void refresh();
    const interval = window.setInterval(() => { void refresh(); }, 5_000);
    return () => { active = false; window.clearInterval(interval); };
  }, [client, task, projectId, candidate]);

  // An in-flight action belongs to this exact rendered task/project/read.
  const actionScope = useRef<object | null>(null);
  useEffect(() => {
    actionScope.current = {};
    setOpening(null);
    return () => { actionScope.current = null; };
  }, [task, projectId, read]);

  if (!presentation || read?.task !== task || read.projectId !== projectId || !read.outputs.length) return null;

  const open = async (output: ManagedOutput) => {
    const scope = actionScope.current;
    setOpening(output.association_id);
    setActionError(false);
    try {
      const [currentTask, currentOutput] = await Promise.all([
        client.getTask(task.task_id), client.getManagedOutput(output.association_id),
      ]);
      if (!scope || actionScope.current !== scope) return;
      if (currentTask.task_id !== task.task_id || !runtimeTaskRecoveryPresentation(currentTask, projectId)
        || !isRuntimeRecoveryOutput(currentTask, currentOutput)
        || currentOutput.association_id !== output.association_id
        || currentOutput.object_id !== output.object_id || currentOutput.version !== output.version) {
        throw new Error('Output changed');
      }
      const selection = await readRuntimeRecoverySelection(client, projectId, currentOutput);
      if (actionScope.current === scope) onOpenOutput?.(currentTask, currentOutput, selection);
    } catch {
      if (actionScope.current === scope) setActionError(true);
    } finally {
      if (actionScope.current === scope) setOpening(null);
    }
  };

  return <section className="mt-2 space-y-2 text-xs" aria-label="Manual placement recovery">
    <p className="text-muted-foreground">{presentation.label}</p>
    {read.outputs.map(({ output, selection }) => <div key={output.association_id} className="space-y-1">
      <a className="underline" href={bridgeMediaUrl(projectId, output.object_id)} target="_blank" rel="noreferrer">
        View {output.filename.split(/[\\/]/).at(-1) || 'output'}
      </a>
      {selection && onOpenOutput ? <Button variant="outline" size="sm" className="ml-2 h-7"
        disabled={opening !== null} onClick={() => { void open(output); }}>
        {opening === output.association_id ? 'Checking output…' : 'Open output'}
      </Button> : null}
      <p className="text-muted-foreground">Manual placement unavailable here. Recover this output from the project gallery.</p>
    </div>)}
    {actionError && <p role="status">Output changed or is unavailable. Reopen it from the project gallery.</p>}
  </section>;
}
