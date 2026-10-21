import { useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { ImageGenerationModal } from '@/shared/components/modals/ImageGenerationModal.tsx';
import type { ImageGenerationPlacement } from '@/shared/lib/taskCreation/imageGeneration.ts';

export function EditorImageGeneration({ placement }: { placement: ImageGenerationPlacement }) {
  const [draftPlacement, setDraftPlacement] = useState<ImageGenerationPlacement | null>(null);
  const [open, setOpen] = useState(false);
  return <>
    <Button type="button" variant="outline" size="sm" onClick={() => { setDraftPlacement((original) => original ?? placement); setOpen(true); }}>Generate image</Button>
    <ImageGenerationModal isOpen={open} onClose={() => setOpen(false)} timelinePlacement={draftPlacement ?? placement} />
  </>;
}

