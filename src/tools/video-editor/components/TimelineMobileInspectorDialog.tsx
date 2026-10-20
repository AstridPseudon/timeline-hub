import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/shared/components/ui/dialog.tsx';
import { MOBILE_SHEET_CLASS } from '@/tools/video-editor/lib/mobile-sheet.ts';
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
        className={MOBILE_SHEET_CLASS}
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
