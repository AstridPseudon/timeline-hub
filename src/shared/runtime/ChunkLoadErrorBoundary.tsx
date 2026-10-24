import React from 'react';
import { Button } from '@/shared/components/ui/button';
import { reportErrorBoundaryCatch } from '@/shared/lib/errorHandling/recoverableError';

/** True for the failures a stale hashed chunk produces after a redeploy. */
export function isChunkLoadError(error: unknown): boolean {
  const message = error instanceof Error ? error.message : String(error ?? '');
  return (
    message.includes('Failed to fetch dynamically imported module') ||
    message.includes('Loading chunk') ||
    message.includes('ChunkLoadError') ||
    message.includes('MIME type')
  );
}

interface ChunkLoadErrorBoundaryState {
  hasError: boolean;
}

/**
 * Error boundary that gives users a way out when a lazy chunk fails to load.
 *
 * This handles the common scenario where:
 * 1. User has cached old JS that references old chunk hashes
 * 2. New deployment changes chunk hashes
 * 3. Dynamic import fails because old chunk no longer exists
 *
 * Usage:
 * <ChunkLoadErrorBoundary>
 *   <React.Suspense fallback={null}>
 *     <LazyComponent />
 *   </React.Suspense>
 * </ChunkLoadErrorBoundary>
 */
export class ChunkLoadErrorBoundary extends React.Component<
  { children: React.ReactNode },
  ChunkLoadErrorBoundaryState
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ChunkLoadErrorBoundaryState {
    // Check if it's a chunk load error
    if (isChunkLoadError(error)) {
      return { hasError: true };
    }

    // Re-throw other errors
    throw error;
  }

  componentDidCatch(error: Error) {
    reportErrorBoundaryCatch({
      context: 'ChunkLoadErrorBoundary.componentDidCatch',
      error,
      recoveryAction: 'fallback',
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <main className="grid min-h-screen place-content-center gap-3 p-6 text-foreground">
          <h1 className="text-xl font-semibold">Astrid was updated</h1>
          <p className="max-w-prose text-muted-foreground">Reload to continue.</p>
          <Button
            className="w-fit"
            onClick={() => window.location.reload()}
            type="button"
          >
            Reload
          </Button>
        </main>
      );
    }

    return this.props.children;
  }
}
