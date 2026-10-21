import { forwardRef, useCallback, useEffect, useLayoutEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { Minimize2 } from 'lucide-react';

export interface PanelFullscreenFrameProps {
  title: string;
  onExit: () => void;
}

const FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

function focusInitial(body: HTMLElement): boolean {
  const target = body.querySelector<HTMLElement>('[data-autofocus]') ?? body.querySelector<HTMLElement>(FOCUSABLE);
  if (!target) return false;
  target.focus({ preventScroll: true });
  return true;
}

/**
 * A panel at the full size of the browser window, above the editor, chat and panes (not the
 * Fullscreen API). The host moves the panel's DOM node into the ref'd body. Modal: Esc exits and
 * Tab stays inside. Whoever opened it returns focus to its own button on exit.
 */
export const PanelFullscreenFrame = forwardRef<HTMLDivElement, PanelFullscreenFrameProps>(function PanelFullscreenFrame(
  { title, onExit },
  bodyRef,
) {
  const frameRef = useRef<HTMLDivElement | null>(null);
  const innerBodyRef = useRef<HTMLDivElement | null>(null);
  const onExitRef = useRef(onExit);
  onExitRef.current = onExit;

  const setBodyRef = useCallback((node: HTMLDivElement | null) => {
    innerBodyRef.current = node;
    if (typeof bodyRef === 'function') bodyRef(node);
    else if (bodyRef) bodyRef.current = node;
  }, [bodyRef]);

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
  }, []);

  // Esc exits unless a panel consumed it; Tab wraps inside the frame.
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const frame = frameRef.current;
      if (!frame) return;
      if (event.key === 'Escape' && !event.defaultPrevented) {
        event.preventDefault();
        onExitRef.current();
        return;
      }
      if (event.key !== 'Tab' || event.defaultPrevented) return;
      const items = Array.from(frame.querySelectorAll<HTMLElement>(FOCUSABLE)).filter((el) => el.offsetParent !== null || el === document.activeElement);
      if (items.length === 0) return;
      const first = items[0];
      const last = items[items.length - 1];
      const active = document.activeElement;
      if (!(active instanceof Node) || !frame.contains(active)) {
        event.preventDefault();
        first.focus();
      } else if (event.shiftKey && active === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && active === last) {
        event.preventDefault();
        first.focus();
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, []);

  // The page behind stays put while the frame is up.
  useLayoutEffect(() => {
    const previous = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = previous; };
  }, []);

  // The app's pane handles are fixed at z-[100016] (see shared/config/panes.ts); the frame stacks above them.
  const frame = (
    <div
      ref={frameRef}
      role="dialog"
      aria-modal="true"
      aria-label={title}
      data-panel-fullscreen-frame
      className="fixed inset-0 z-[100017] flex min-h-0 flex-col bg-background text-foreground"
    >
      <div data-panel-fullscreen-titlebar className="flex h-9 shrink-0 select-none items-center gap-2 border-b border-border bg-muted/40 px-3">
        <span className="min-w-0 flex-1 truncate text-sm font-medium">{title}</span>
        <button
          type="button"
          aria-label="Back to sidebar"
          title="Back to sidebar (Esc)"
          onClick={onExit}
          className="inline-flex h-6 w-6 items-center justify-center rounded-sm opacity-70 hover:bg-accent hover:opacity-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <Minimize2 className="h-4 w-4" />
        </button>
      </div>
      <div ref={setBodyRef} data-panel-fullscreen-body className="relative flex min-h-0 flex-1 flex-col overflow-hidden" />
    </div>
  );

  return createPortal(frame, document.body);
});
