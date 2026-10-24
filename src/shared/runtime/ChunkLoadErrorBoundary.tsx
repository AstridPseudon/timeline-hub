import React from 'react';
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
 * Error boundary that catches chunk load failures (from lazy imports after deployment)
 * and auto-reloads the page to get fresh assets.
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
      recoveryAction: 'reload',
    });
    // Small delay to ensure the error boundary renders before reload
    setTimeout(() => {
      window.location.reload();
    }, 100);
  }

  render() {
    if (this.state.hasError) {
      // Brief message shown before auto-reload
      return (
        <div className="flex items-center justify-center p-4 text-sm text-muted-foreground">
          Updating...
        </div>
      );
    }

    return this.props.children;
  }
}
