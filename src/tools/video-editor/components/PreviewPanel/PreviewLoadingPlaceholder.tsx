import { Video } from 'lucide-react';

/** Shared by Remotion's suspense fallback and scoped pack preparation. */
export function PreviewLoadingPlaceholder() {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-label="Loading preview"
      className="absolute inset-0 flex items-center justify-center border border-border/40 bg-muted/40 text-muted-foreground"
      data-testid="preview-loading-placeholder"
    >
      <Video aria-hidden="true" className="h-[6%] w-auto opacity-25" strokeWidth={1.25} />
    </div>
  );
}
