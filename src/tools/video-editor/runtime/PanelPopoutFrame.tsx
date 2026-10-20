import { forwardRef, useCallback, useEffect, useLayoutEffect, useRef, useState, type PointerEvent as ReactPointerEvent } from 'react';
import { createPortal } from 'react-dom';
import { Maximize2, Minimize2, X } from 'lucide-react';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import { useEditorSettings } from '@/tools/video-editor/settings/useEditorSettings.ts';

export interface PanelRect {
  x: number;
  y: number;
  width: number;
  height: number;
}

/** The size of the area the frame lives in. The shell root element, or any object with its size. */
export type PanelPopoutBounds = HTMLElement | { readonly width: number; readonly height: number };

export interface PanelPopoutFrameProps {
  title: string;
  /** Shell root (measured at each interaction) or its size. Rects are clamped to it. */
  bounds: PanelPopoutBounds;
  /** Opening rect, relative to the bounds' top-left. Clamped on open. */
  defaultRect: PanelRect;
  /** Touch layout: fills the bounds, no move or resize, a Done button in place of [x]. */
  touch: boolean;
  onClose: () => void;
  /** Element the frame is portalled into. Defaults to the bounds element, else document.body. */
  container?: HTMLElement | null;
  /** Key for size memory. Defaults to title. */
  panelKey?: string;
}

export interface PanelPopoutSize {
  width: number;
  height: number;
}

export const MIN_POPOUT_WIDTH = 640;
export const MIN_POPOUT_HEIGHT = 420;
export const POPOUT_SIZES_STORAGE_KEY = 'video-editor:popout-sizes';

const NO_SIZES: Readonly<Record<string, PanelPopoutSize>> = {};

function measureBounds(bounds: PanelPopoutBounds): PanelPopoutSize {
  return bounds instanceof HTMLElement
    ? { width: bounds.clientWidth, height: bounds.clientHeight }
    : { width: bounds.width, height: bounds.height };
}

/** Fit a rect inside the bounds: at least the minimum size (or the whole bounds if smaller), at most the bounds. */
export function clampRect(rect: PanelRect, bounds: PanelPopoutSize): PanelRect {
  const width = Math.min(Math.max(rect.width, Math.min(MIN_POPOUT_WIDTH, bounds.width)), bounds.width);
  const height = Math.min(Math.max(rect.height, Math.min(MIN_POPOUT_HEIGHT, bounds.height)), bounds.height);
  return {
    x: Math.min(Math.max(rect.x, 0), bounds.width - width),
    y: Math.min(Math.max(rect.y, 0), bounds.height - height),
    width,
    height,
  };
}

type Edge = 'n' | 's' | 'e' | 'w';
const HANDLES: readonly { readonly name: string; readonly edges: readonly Edge[]; readonly className: string }[] = [
  { name: 'n', edges: ['n'], className: 'left-2 right-2 top-0 h-1.5 cursor-ns-resize' },
  { name: 's', edges: ['s'], className: 'bottom-0 left-2 right-2 h-1.5 cursor-ns-resize' },
  { name: 'e', edges: ['e'], className: 'bottom-2 right-0 top-2 w-1.5 cursor-ew-resize' },
  { name: 'w', edges: ['w'], className: 'bottom-2 left-0 top-2 w-1.5 cursor-ew-resize' },
  { name: 'nw', edges: ['n', 'w'], className: 'left-0 top-0 h-3 w-3 cursor-nwse-resize' },
  { name: 'ne', edges: ['n', 'e'], className: 'right-0 top-0 h-3 w-3 cursor-nesw-resize' },
  { name: 'se', edges: ['s', 'e'], className: 'bottom-0 right-0 h-3 w-3 cursor-nwse-resize' },
  { name: 'sw', edges: ['s', 'w'], className: 'bottom-0 left-0 h-3 w-3 cursor-nesw-resize' },
];

const FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

function focusInitial(body: HTMLElement): boolean {
  const target = body.querySelector<HTMLElement>('[data-autofocus]') ?? body.querySelector<HTMLElement>(FOCUSABLE);
  if (!target) return false;
  target.focus({ preventScroll: true });
  return true;
}

interface Gesture {
  startX: number;
  startY: number;
  startRect: PanelRect;
  bounds: PanelPopoutSize;
  /** Null for a move. */
  edges: readonly Edge[] | null;
}

/**
 * Non-modal floating frame for a panel. The host moves the panel's DOM node into the ref'd body.
 * Lives inside the editor shell root, which must be `relative`.
 */
export const PanelPopoutFrame = forwardRef<HTMLDivElement, PanelPopoutFrameProps>(function PanelPopoutFrame(
  { title, bounds, defaultRect, touch, onClose, container, panelKey },
  bodyRef,
) {
  const memoryKey = panelKey ?? title;
  const [sizes, setSizes] = useEditorSettings<Record<string, PanelPopoutSize>>(POPOUT_SIZES_STORAGE_KEY, NO_SIZES, 200);

  const [rect, setRectState] = useState<PanelRect>(() => {
    const measured = measureBounds(bounds);
    const remembered = sizes[memoryKey];
    const requested = remembered ? { ...defaultRect, width: remembered.width, height: remembered.height } : defaultRect;
    return clampRect(requested, measured);
  });
  const rectRef = useRef(rect);
  const setRect = useCallback((next: PanelRect) => {
    rectRef.current = next;
    setRectState(next);
  }, []);

  const [filled, setFilled] = useState(false);
  const restoreRectRef = useRef<PanelRect | null>(null);
  const [dragging, setDragging] = useState(false);
  const gestureRef = useRef<Gesture | null>(null);

  const frameRef = useRef<HTMLDivElement | null>(null);
  const innerBodyRef = useRef<HTMLDivElement | null>(null);
  const onCloseRef = useRef(onClose);
  onCloseRef.current = onClose;
  const boundsRef = useRef(bounds);
  boundsRef.current = bounds;

  const setBodyRef = useCallback((node: HTMLDivElement | null) => {
    innerBodyRef.current = node;
    if (typeof bodyRef === 'function') bodyRef(node);
    else if (bodyRef) bodyRef.current = node;
  }, [bodyRef]);

  // Keep the frame inside the bounds when the window changes size, and keep fill matched to the bounds.
  useEffect(() => {
    const onResize = () => {
      const measured = measureBounds(boundsRef.current);
      if (filled) setRect({ x: 0, y: 0, width: measured.width, height: measured.height });
      else setRect(clampRect(rectRef.current, measured));
    };
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, [filled, setRect]);

  // Focus: opener is remembered on open and restored on close.
  useLayoutEffect(() => {
    const opener = document.activeElement;
    return () => {
      if (opener instanceof HTMLElement && opener.isConnected) opener.focus({ preventScroll: true });
    };
  }, []);

  // Initial focus: the body is filled by the host, so keep watching until something focusable arrives.
  useEffect(() => {
    const body = innerBodyRef.current;
    if (!body) return undefined;
    if (focusInitial(body)) return undefined;
    const observer = new MutationObserver(() => {
      if (focusInitial(body)) observer.disconnect();
    });
    observer.observe(body, { childList: true, subtree: true });
    return () => observer.disconnect();
  }, [touch]);

  // Esc docks the panel only when focus is inside the frame and nothing earlier consumed the key.
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== 'Escape' || event.defaultPrevented) return;
      const frame = frameRef.current;
      if (!frame || !frame.contains(document.activeElement)) return;
      onCloseRef.current();
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, []);

  // The drag shield: iframes inside the body must not swallow pointer moves.
  useEffect(() => {
    const body = innerBodyRef.current;
    if (!body) return;
    body.style.pointerEvents = dragging ? 'none' : '';
  }, [dragging]);

  const endGesture = useCallback((commit: boolean) => {
    const gesture = gestureRef.current;
    gestureRef.current = null;
    setDragging(false);
    if (commit && gesture?.edges) {
      const { width, height } = rectRef.current;
      setSizes((current) => ({ ...current, [memoryKey]: { width, height } }));
    }
  }, [memoryKey, setSizes]);

  const onPointerMove = useCallback((event: PointerEvent) => {
    const gesture = gestureRef.current;
    if (!gesture) return;
    const dx = event.clientX - gesture.startX;
    const dy = event.clientY - gesture.startY;
    const start = gesture.startRect;
    const { bounds: measured } = gesture;

    if (!gesture.edges) {
      setRect(clampRect({ ...start, x: start.x + dx, y: start.y + dy }, measured));
      return;
    }

    // Resize: move the dragged edges, keep the others, and stop each edge at the bounds and the minimum size.
    let left = start.x;
    let right = start.x + start.width;
    let top = start.y;
    let bottom = start.y + start.height;
    if (gesture.edges.includes('w')) left = Math.min(Math.max(left + dx, 0), right - Math.min(MIN_POPOUT_WIDTH, measured.width));
    if (gesture.edges.includes('e')) right = Math.max(Math.min(right + dx, measured.width), left + Math.min(MIN_POPOUT_WIDTH, measured.width));
    if (gesture.edges.includes('n')) top = Math.min(Math.max(top + dy, 0), bottom - Math.min(MIN_POPOUT_HEIGHT, measured.height));
    if (gesture.edges.includes('s')) bottom = Math.max(Math.min(bottom + dy, measured.height), top + Math.min(MIN_POPOUT_HEIGHT, measured.height));
    setRect({ x: left, y: top, width: right - left, height: bottom - top });
  }, [setRect]);

  useEffect(() => {
    if (!dragging) return undefined;
    const onUp = () => {
      window.removeEventListener('pointermove', onPointerMove);
      window.removeEventListener('pointerup', onUp);
      window.removeEventListener('pointercancel', onUp);
      endGesture(true);
    };
    window.addEventListener('pointermove', onPointerMove);
    window.addEventListener('pointerup', onUp);
    window.addEventListener('pointercancel', onUp);
    return () => {
      window.removeEventListener('pointermove', onPointerMove);
      window.removeEventListener('pointerup', onUp);
      window.removeEventListener('pointercancel', onUp);
    };
  }, [dragging, endGesture, onPointerMove]);

  const startGesture = (event: ReactPointerEvent<HTMLElement>, edges: readonly Edge[] | null) => {
    if (touch || event.button !== 0) return;
    event.preventDefault();
    if (filled) setFilled(false);
    gestureRef.current = {
      startX: event.clientX,
      startY: event.clientY,
      startRect: rectRef.current,
      bounds: measureBounds(boundsRef.current),
      edges,
    };
    setDragging(true);
  };

  const toggleFill = () => {
    if (filled) {
      const restore = restoreRectRef.current ?? rectRef.current;
      setRect(clampRect(restore, measureBounds(bounds)));
      setFilled(false);
      return;
    }
    restoreRectRef.current = rectRef.current;
    const measured = measureBounds(bounds);
    setRect({ x: 0, y: 0, width: measured.width, height: measured.height });
    setFilled(true);
  };

  const frame = (
    <div
      ref={frameRef}
      role="dialog"
      aria-modal="false"
      aria-label={title}
      data-panel-popout-frame
      className={cn(
        'absolute z-40 flex min-h-0 flex-col overflow-hidden border border-border bg-background text-foreground shadow-lg',
        touch
          ? 'inset-0 pb-[env(safe-area-inset-bottom)] pl-[env(safe-area-inset-left)] pr-[env(safe-area-inset-right)] pt-[env(safe-area-inset-top)]'
          : 'rounded-lg',
      )}
      style={touch ? undefined : { left: rect.x, top: rect.y, width: rect.width, height: rect.height }}
    >
      <div
        data-panel-popout-titlebar
        onPointerDown={touch ? undefined : (event) => startGesture(event, null)}
        className={cn(
          'flex h-9 shrink-0 select-none items-center gap-2 border-b border-border bg-muted/40 px-3',
          !touch && 'cursor-move',
        )}
      >
        <span className="min-w-0 flex-1 truncate text-sm font-medium">{title}</span>
        {touch ? (
          <button type="button" onClick={onClose} className="rounded-sm px-2 py-1 text-sm font-medium hover:bg-accent focus:outline-none focus-visible:ring-2 focus-visible:ring-ring">
            Done
          </button>
        ) : (
          <>
            <button
              type="button"
              aria-pressed={filled}
              aria-label={filled ? 'Restore size' : 'Fill editor'}
              title={filled ? 'Restore size' : 'Fill editor'}
              onPointerDown={(event) => event.stopPropagation()}
              onClick={toggleFill}
              className="inline-flex h-6 w-6 items-center justify-center rounded-sm opacity-70 hover:bg-accent hover:opacity-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {filled ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
            </button>
            <button
              type="button"
              aria-label="Return to panel"
              title="Return to panel"
              onPointerDown={(event) => event.stopPropagation()}
              onClick={onClose}
              className="inline-flex h-6 w-6 items-center justify-center rounded-sm opacity-70 hover:bg-accent hover:opacity-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <X className="h-4 w-4" />
            </button>
          </>
        )}
      </div>

      <div ref={setBodyRef} data-panel-popout-body className="relative flex min-h-0 flex-1 flex-col overflow-hidden" />

      {!touch && HANDLES.map((handle) => (
        <div
          key={handle.name}
          data-panel-popout-handle={handle.name}
          aria-hidden="true"
          onPointerDown={(event) => startGesture(event, handle.edges)}
          className={cn('absolute z-10', handle.className)}
        />
      ))}
    </div>
  );

  const target = container ?? (bounds instanceof HTMLElement ? bounds : document.body);
  return createPortal(frame, target);
});
