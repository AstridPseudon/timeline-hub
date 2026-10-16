import { useCallback, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Music2 } from 'lucide-react';

import { getBridgeTaskClient } from '@/integrations/astrid/bridgeTaskReads.ts';
import { createTask } from '@/shared/lib/taskCreation/createTask.ts';
import { Button } from '@/shared/components/ui/button.tsx';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/shared/components/ui/dialog.tsx';
import { DeclaredActionForm } from './DeclaredActionForm.tsx';
import {
  prepareDeclaredActionTaskRequest,
  CHIPTUNE_COMPOSE_ACTION_ID,
} from '@/tools/video-editor/data/declaredActionTask.ts';
import type { DeclaredActionCapability } from '@/tools/video-editor/data/bridgeContract.ts';
import type { TaskCreationResult } from '@/shared/lib/taskCreation/types.ts';

export function DeclaredActionLauncher({ projectSlug }: { projectSlug: string | null | undefined }) {
  const [open, setOpen] = useState(false);

  if (!projectSlug) return null;

  return (
    <>
      <Button
        type="button"
        variant="ghost"
        size="sm"
        onClick={() => setOpen(true)}
        title="Runtime Generator action"
        aria-label="Runtime Generator action"
        data-video-editor-runtime-action-launcher="true"
      >
        <Music2 className="mr-1.5 h-3.5 w-3.5" />
        Generator
      </Button>
      <Dialog open={open} onOpenChange={setOpen}>
        {open && (
          <DeclaredActionDialogContent
            projectSlug={projectSlug}
            onClose={() => setOpen(false)}
          />
        )}
      </Dialog>
    </>
  );
}

function DeclaredActionDialogContent({
  projectSlug,
  onClose,
}: {
  projectSlug: string;
  onClose: () => void;
}) {
  const capabilityQuery = useQuery({
    queryKey: ['astrid-runtime-capability', projectSlug, CHIPTUNE_COMPOSE_ACTION_ID],
    queryFn: async () => await getBridgeTaskClient(projectSlug).catalog.getV2(CHIPTUNE_COMPOSE_ACTION_ID),
    retry: false,
  });

  const onRunAction = useCallback(async (
    capability: DeclaredActionCapability,
    values: Record<string, unknown>,
  ): Promise<TaskCreationResult> => {
    const request = await prepareDeclaredActionTaskRequest(
      projectSlug,
      CHIPTUNE_COMPOSE_ACTION_ID,
      capability,
      values,
      getBridgeTaskClient(projectSlug).declaredActionPreparation,
    );
    return await createTask(request, { capabilityCatalogVersion: 2 });
  }, [projectSlug]);

  return (
    <DialogContent className="max-h-[85vh] overflow-y-auto sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>Runtime Generator action</DialogTitle>
        <DialogDescription>
          Run a ready action from this project’s authenticated Runtime capability catalog.
        </DialogDescription>
      </DialogHeader>
      {capabilityQuery.isPending ? (
        <p role="status" className="text-sm text-muted-foreground">Loading {CHIPTUNE_COMPOSE_ACTION_ID}…</p>
      ) : capabilityQuery.isError ? (
        <p role="status" className="text-sm text-destructive" data-video-editor-runtime-action-error="true">
          Runtime action unavailable: {capabilityQuery.error.message}
        </p>
      ) : (
        <DeclaredActionForm
          actionId={CHIPTUNE_COMPOSE_ACTION_ID}
          capability={capabilityQuery.data}
          onRunAction={onRunAction}
        />
      )}
      <Button type="button" variant="outline" size="sm" onClick={onClose}>
        Close
      </Button>
    </DialogContent>
  );
}
