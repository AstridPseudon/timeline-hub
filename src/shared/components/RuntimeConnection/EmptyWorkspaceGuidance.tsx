import { useEffect, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { AstridRuntimeClient } from '@/integrations/runtime/client.ts';
import { runtimeApiBase } from '@/integrations/runtime/connection.ts';
import { Button } from '@/shared/components/ui/button.tsx';
import { writeClipboardTextSafe } from '@/shared/lib/browser/clipboard.ts';
import { RUNTIME_CONNECTION_COPY } from './copy.ts';

type WorkspaceIdentity = { name: string; realmId: string };

/** The details are for an agent to diagnose a misplaced workspace, not for the person to inspect. */
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
  const [didCopy, setDidCopy] = useState(false);
  const copiedTimer = useRef<number | null>(null);
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
  const copy = RUNTIME_CONNECTION_COPY.agent;

  useEffect(() => () => {
    if (copiedTimer.current !== null) window.clearTimeout(copiedTimer.current);
  }, []);

  const handleCopy = async () => {
    const copied = await writeClipboardTextSafe(diagnostic);
    if (copiedTimer.current !== null) window.clearTimeout(copiedTimer.current);
    setCopyState(copied ? 'copied' : 'failed');
    if (copied) {
      setDidCopy(true);
      copiedTimer.current = window.setTimeout(() => {
        copiedTimer.current = null;
        setCopyState('idle');
      }, 2000);
    }
  };

  const handleCheckAgain = () => {
    if (identity.error) void identity.refetch();
    onRefresh();
  };

  return <div className="space-y-3 text-sm text-muted-foreground">
    <p>Astrid is connected, but there are no projects here yet.</p>
    <p>Expected to see your work? It may be in another Astrid folder on this computer.</p>
    <details onToggle={event => setShowDetails(event.currentTarget.open)}>
      <summary className="cursor-pointer text-foreground">Find my work</summary>
      <div className="mt-3 space-y-3">
        {identity.isPending ? <p role="status">Reading details…</p>
          : identity.error ? <p role="status">Astrid's details aren't available right now.</p>
            : identity.data ? <>
              <Button variant="outline" onClick={() => void handleCopy()}>
                {copyState === 'copied' ? copy.copied : copy.copy}
              </Button>
              {didCopy && <p role="status">{copy.pasteNext}</p>}
              {copyState === 'failed' && <div className="space-y-2">
                <p role="status">{copy.copyFailed}</p>
                <textarea aria-label={copy.copyFailed} readOnly value={diagnostic} rows={6} onFocus={event => event.currentTarget.select()} className="w-full rounded-md border border-border bg-background p-2 text-xs text-foreground" />
              </div>}
            </> : null}
        <Button variant="outline" onClick={handleCheckAgain}>Check again</Button>
      </div>
    </details>
  </div>;
}
