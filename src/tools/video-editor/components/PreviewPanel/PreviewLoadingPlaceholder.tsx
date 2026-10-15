/** Shared by Remotion's suspense fallback and scoped pack preparation. */
export function PreviewLoadingPlaceholder() {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-label="Loading preview"
      className="absolute inset-0 flex items-center justify-center bg-background text-sm text-muted-foreground"
      data-testid="preview-loading-placeholder"
    />
  );
}
