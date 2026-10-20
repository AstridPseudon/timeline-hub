import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/shared/components/ui/dialog.tsx';
import { PropertiesPanel } from '@/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx';

/**
 * The touch clip sheet, on phones and tablets. Tapping a clip opens it (the
 * shell owns that); there is no button for it. The inspector's own clip header
 * names the clip and carries delete and close, so the sheet adds no visible
 * title or second close button: closing the clip, deleting it or tapping
 * outside closes the sheet. Past phone width it keeps a reading width (36rem)
 * at the bottom centre instead of spanning the screen.
 */
export function TimelineMobileInspectorDialog({
  open,
  onOpenChange,
  title,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
}) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        data-testid="timeline-clip-sheet"
        className="top-auto bottom-0 flex max-h-[78dvh] flex-col w-full max-w-none translate-x-[-50%] translate-y-0 gap-0 overflow-hidden rounded-t-2xl border-x-0 border-b-0 border-border bg-background p-0 pb-[env(safe-area-inset-bottom)] sm:max-w-xl sm:border-x data-[ending-style]:slide-out-to-bottom-[100%] data-[open]:slide-in-from-bottom-[100%] motion-reduce:animate-none motion-reduce:transition-none [&>[data-dialog-close]]:hidden"
      >
        <DialogHeader className="sr-only">
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>Clip actions and properties.</DialogDescription>
        </DialogHeader>
        <div aria-hidden="true" className="mx-auto mt-2 h-1 w-10 shrink-0 rounded-full bg-border" />
        <div className="min-h-0 flex-1 overflow-y-auto p-3">
          <PropertiesPanel />
        </div>
      </DialogContent>
    </Dialog>
  );
}
