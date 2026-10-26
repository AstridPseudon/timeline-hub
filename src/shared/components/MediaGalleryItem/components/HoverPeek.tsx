import React, { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { Eye } from 'lucide-react';
import { cn } from '@/shared/components/ui/contracts/cn';
import { UI_Z_LAYERS } from '@/shared/lib/uiLayers';
import { mediaCrossOrigin } from '@/shared/lib/media/mediaCrossOrigin';
import type { GeneratedImageWithMetadata } from '../../MediaGallery/types';
import { isPeekImageLoaded, markPeekImageLoaded, useHoverPeek } from './useHoverPeek';

const DEFAULT_ASPECT_RATIO = 16 / 9;

interface HoverPeekButtonProps {
  image: GeneratedImageWithMetadata;
  /** Thumbnail shown at once in the peek, and the video poster. */
  thumbSrc: string | null;
  /** Full-size image URL. Null for video, which plays `videoSrc` instead. */
  fullSrc: string | null;
  videoSrc: string | null;
  isVideo: boolean;
  /** Aspect ratio from the item's metadata resolution, if it has one. */
  metadataAspectRatio: number | null;
  /** Aspect ratio of the project, used until the media's own size is known. */
  projectAspectRatio: number | null;
  onOpenLightbox: (image: GeneratedImageWithMetadata) => void;
}

/**
 * Desktop-only eye on a gallery tile. Hovering it opens the item's full-size media in a large
 * peek over the page; the peek stays open while the pointer is on it, and clicking it opens the
 * lightbox. Hidden on coarse pointers, where touch uses the "+" instead.
 */
export const HoverPeekButton: React.FC<HoverPeekButtonProps> = ({
  image,
  thumbSrc,
  fullSrc,
  videoSrc,
  isVideo,
  metadataAspectRatio,
  projectAspectRatio,
  onOpenLightbox,
}) => {
  const { open, close, eyeHandlers, peekHandlers } = useHoverPeek(isVideo ? null : fullSrc);

  const openLightbox = () => {
    close();
    onOpenLightbox(image);
  };

  return (
    <>
      <button
        type="button"
        aria-label="Preview"
        onPointerEnter={eyeHandlers.onPointerEnter}
        onPointerLeave={eyeHandlers.onPointerLeave}
        onClick={(event) => {
          event.stopPropagation();
          openLightbox();
        }}
        className={cn(
          'h-7 w-7 p-0 rounded-full bg-black/50 hover:bg-black/70 text-white flex items-center justify-center transition-opacity',
          'opacity-0 group-hover:opacity-100 group-focus-within:opacity-100',
          '[@media(pointer:coarse)]:hidden',
        )}
        data-testid="gallery-tile-preview"
      >
        <Eye className="h-3.5 w-3.5" />
      </button>
      {open && createPortal(
        <HoverPeekLayer
          image={image}
          thumbSrc={thumbSrc}
          fullSrc={fullSrc}
          videoSrc={videoSrc}
          isVideo={isVideo}
          metadataAspectRatio={metadataAspectRatio}
          projectAspectRatio={projectAspectRatio}
          handlers={peekHandlers}
          onActivate={openLightbox}
        />,
        document.body,
      )}
    </>
  );
};

interface HoverPeekLayerProps extends Omit<HoverPeekButtonProps, 'onOpenLightbox'> {
  handlers: { onPointerEnter: () => void; onPointerLeave: () => void };
  onActivate: () => void;
}

const HoverPeekLayer: React.FC<HoverPeekLayerProps> = ({
  image,
  thumbSrc,
  fullSrc,
  videoSrc,
  isVideo,
  metadataAspectRatio,
  projectAspectRatio,
  handlers,
  onActivate,
}) => {
  const [fullLoaded, setFullLoaded] = useState(() => Boolean(fullSrc && isPeekImageLoaded(fullSrc)));
  const [measuredAspectRatio, setMeasuredAspectRatio] = useState<number | null>(null);
  const [entered, setEntered] = useState(false);

  // Mounted with the start styles, then flipped on the next frame so the fade and scale run.
  useEffect(() => {
    const frame = requestAnimationFrame(() => setEntered(true));
    return () => cancelAnimationFrame(frame);
  }, []);

  const aspectRatio = metadataAspectRatio ?? measuredAspectRatio ?? projectAspectRatio ?? DEFAULT_ASPECT_RATIO;
  const stop = (event: React.SyntheticEvent) => event.stopPropagation();
  const measure = (width: number, height: number) => {
    if (width > 0 && height > 0) setMeasuredAspectRatio(width / height);
  };

  return (
    <div
      className="fixed inset-0 flex items-center justify-center pointer-events-none"
      style={{ zIndex: UI_Z_LAYERS.GALLERY_PEEK }}
    >
      <div
        className={cn(
          'absolute inset-0 bg-black/50 pointer-events-none transition-opacity duration-[120ms]',
          entered ? 'opacity-100' : 'opacity-0',
        )}
      />
      <div
        role="button"
        tabIndex={-1}
        aria-label="Open in lightbox"
        data-testid="gallery-tile-peek"
        draggable={false}
        onPointerEnter={handlers.onPointerEnter}
        onPointerLeave={handlers.onPointerLeave}
        onPointerDown={stop}
        onPointerUp={stop}
        onDoubleClick={stop}
        onClick={(event) => {
          event.stopPropagation();
          onActivate();
        }}
        style={{
          width: `min(90vw, calc(90vh * ${aspectRatio}))`,
          aspectRatio: String(aspectRatio),
        }}
        className={cn(
          'pointer-events-auto relative cursor-pointer overflow-hidden rounded-lg bg-black shadow-2xl ring-1 ring-white/10',
          'transition-[opacity,transform] duration-[120ms] ease-out motion-reduce:transform-none',
          entered ? 'opacity-100 scale-100' : 'opacity-0 scale-[0.97]',
        )}
      >
        {isVideo ? (
          <video
            src={videoSrc ?? undefined}
            poster={thumbSrc ?? undefined}
            muted
            loop
            autoPlay
            playsInline
            draggable={false}
            onLoadedMetadata={(event) => measure(event.currentTarget.videoWidth, event.currentTarget.videoHeight)}
            className="absolute inset-0 h-full w-full object-contain"
          />
        ) : (
          <>
            {thumbSrc && (
              <img
                src={thumbSrc}
                alt=""
                draggable={false}
                crossOrigin={mediaCrossOrigin(thumbSrc)}
                onLoad={(event) => measure(event.currentTarget.naturalWidth, event.currentTarget.naturalHeight)}
                className="absolute inset-0 h-full w-full object-contain"
              />
            )}
            {fullSrc && (
              <img
                src={fullSrc}
                alt={image.prompt ?? ''}
                draggable={false}
                crossOrigin={mediaCrossOrigin(fullSrc)}
                onLoad={() => {
                  markPeekImageLoaded(fullSrc);
                  setFullLoaded(true);
                }}
                className={cn(
                  'absolute inset-0 h-full w-full object-contain transition-opacity duration-150',
                  fullLoaded ? 'opacity-100' : 'opacity-0',
                )}
              />
            )}
          </>
        )}
      </div>
    </div>
  );
};
