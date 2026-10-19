import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { AstridRuntimeClient } from '@/integrations/runtime/client.ts';
import { runtimeApiBase } from '@/integrations/runtime/connection.ts';
import { Button } from '@/shared/components/ui/button.tsx';
import { writeClipboardTextSafe } from '@/shared/lib/browser/clipboard.ts';

type WorkspaceIdentity = { name: string; realmId: string };

/** Only public identity fields are copied; Runtime sessions and credentials stay in the client. */
function emptyWorkspaceDiagnostic(identity: WorkspaceIdentity, pageOrigin: string, endpoint: string): string {
  return [
    `Astrid at ${pageOrigin} is connected, but its workspace returned no projects.`,
    `Connected workspace: ${identity.name}`,
    `Workspace ID: ${identity.realmId}`,
    `Connection: ${endpoint}`,
    'Please check which existing workspace the local Astrid launcher is using, including its configured data root and Runtime discovery files. Compare it with the workspace that contains my existing work.',
    'Keep my existing installation, profile, data, credentials and agent instructions. Do not create a new workspace or project to work around missing data.',
    'If the launcher points to the wrong workspace, reconnect it to the existing intended workspace, then reload this page and check the project list.',
  ].join('\n\n');
}

/** An empty, healthy workspace can be the wrong one; help people check before creating new work. */
export function EmptyWorkspaceGuidance({ onRefresh }: { onRefresh: () => void }) {
  const [showDetails, setShowDetails] = useState(false);
  const [copyState, setCopyState] = useState<'idle' | 'copied' | 'failed'>('idle');
  const identity = useQuery({
    queryKey: ['runtime', 'empty-workspace-identity'],
    enabled: showDetails,
    retry: false,
    queryFn: async (): Promise<WorkspaceIdentity> => {
      const session = await new AstridRuntimeClient().ensureSession();
      return {
        name: session.realm.display_name,
        realmId: session.realm.realm_id,
      };
    },
  });
  const diagnostic = identity.data
    ? emptyWorkspaceDiagnostic(identity.data, window.location.origin, runtimeApiBase())
    : '';

  return <div className="space-y-3 text-sm text-muted-foreground">
    <p>Astrid is connected, but this workspace has no projects.</p>
    <p>If you expected existing work, check which workspace is connected before creating a project.</p>
    <details onToggle={event => setShowDetails(event.currentTarget.open)}>
      <summary className="cursor-pointer text-foreground">Check connected workspace</summary>
      <div className="mt-3 space-y-3">
        <p>Check the workspace selected by Astrid on this computer. After reconnecting to the workspace with your work, reload this page.</p>
        {identity.isPending ? <p role="status">Reading workspace details…</p>
          : identity.error ? <div className="space-y-2"><p>Workspace details are unavailable.</p><Button variant="outline" onClick={() => void identity.refetch()}>Retry workspace details</Button></div>
            : identity.data ? <>
              <dl className="space-y-1 break-all text-xs">
                <div><dt className="inline font-medium text-foreground">Workspace: </dt><dd className="inline">{identity.data.name}</dd></div>
                <div><dt className="inline font-medium text-foreground">Workspace ID: </dt><dd className="inline">{identity.data.realmId}</dd></div>
                <div><dt className="inline font-medium text-foreground">Connection: </dt><dd className="inline">{runtimeApiBase()}</dd></div>
              </dl>
              <Button variant="outline" onClick={() => void writeClipboardTextSafe(diagnostic).then(copied => setCopyState(copied ? 'copied' : 'failed'))}>
                {copyState === 'copied' ? 'Copied' : 'Copy workspace check for your agent'}
              </Button>
              {copyState === 'copied' && <p role="status">Paste this into your coding agent to check the existing workspace.</p>}
              {copyState === 'failed' && <textarea aria-label="Workspace check for your agent" readOnly value={diagnostic} rows={6} onFocus={event => event.currentTarget.select()} className="w-full rounded-md border border-border bg-background p-2 text-xs text-foreground" />}
            </> : null}
        <Button variant="outline" onClick={onRefresh}>Check projects again</Button>
      </div>
    </details>
  </div>;
}
