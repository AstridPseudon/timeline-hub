import { useId, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import type { PanelRenderProps, PanelVideoAdapter } from '@astrid/editor-sdk';
import type { VideoEditorPanelDescriptor } from './extensionSurface';
import {
  HostContributionErrorBoundary,
  type ContributionErrorInfo,
} from './ContributionErrorBoundary';
import { PanelPopoutFrame, type PanelPopoutBounds, type PanelRect } from './PanelPopoutFrame';
import { PanelFullscreenFrame } from './PanelFullscreenFrame';
import { useOptionalVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';

/** Stable contribution identity for selection/preferences within a host. */
export function getPanelKey(panel: Pick<VideoEditorPanelDescriptor, 'extensionId' | 'id'>): string {
  return `${panel.extensionId ?? 'host'}:${panel.id}`;
}

type MoveBeforeParent = Node & { moveBefore?: (node: Node, child: Node | null) => void };

/**
 * Put a panel's node last in `parent` without recreating it. `Element.moveBefore`
 * (Chromium) keeps iframes, focus and scroll running; elsewhere `appendChild`
 * detaches and reattaches, so an iframe reloads once. React state is unaffected
 * either way because the node is only a portal container.
 */
export function placePanelNode(node: Node, parent: Node): void {
  if (node.parentNode === parent && node === parent.lastChild) return;
  const target = parent as MoveBeforeParent;
  if (typeof target.moveBefore === 'function' && node.isConnected && parent.isConnected) {
    try {
      target.moveBefore(node, null);
      return;
    } catch {
      // Cross-document or disconnected moves throw; fall through to a plain move.
    }
  }
  parent.appendChild(node);
}

export interface ExtensionPanelHostProps {
  /** Include registered panels even while hidden. Removal ends their lifetime. */
  readonly panels: readonly VideoEditorPanelDescriptor[];
  /** Panels shown in their docked slot. A popped-out or full-screen panel is visible regardless. */
  readonly visiblePanelKeys: ReadonlySet<string>;
  readonly video?: PanelVideoAdapter;
  readonly settingsByPanelKey?: Readonly<Record<string, PanelRenderProps['settings']>>;
  readonly onError?: (info: ContributionErrorInfo) => void;
  /** Controlled: the one panel shown in the floating frame, if any. */
  readonly poppedPanelKey?: string | null;
  /** Supplying this is what offers `popout` to panels. Null docks the panel. */
  readonly onPoppedPanelKeyChange?: (key: string | null) => void;
  /** Touch chrome for the retained pop-out contract. */
  readonly touch?: boolean;
  /** Controlled: the one panel shown full screen, if any. */
  readonly fullscreenPanelKey?: string | null;
  /** Supplying this is what offers `fullscreen` to panels. Null returns the panel to its slot. */
  readonly onFullscreenPanelKeyChange?: (key: string | null) => void;
}

function PanelContent({ panel, ...props }: PanelRenderProps & { panel: VideoEditorPanelDescriptor }) {
  return panel.render(props);
}

interface PanelSlotProps {
  readonly panel: VideoEditorPanelDescriptor;
  readonly panelKey: string;
  readonly instanceId: string;
  readonly dockedVisible: boolean;
  readonly popped: boolean;
  readonly fullscreenActive: boolean;
  readonly popoutBody: () => HTMLElement | null;
  readonly fullscreenBody: () => HTMLElement | null;
  readonly video?: PanelVideoAdapter;
  readonly settings?: PanelRenderProps['settings'];
  readonly popout?: PanelRenderProps['popout'];
  readonly fullscreen?: PanelRenderProps['fullscreen'];
  readonly onDock: () => void;
  readonly onError?: (info: ContributionErrorInfo) => void;
}

function PanelSlot({ panel, panelKey, instanceId, dockedVisible, popped, fullscreenActive, popoutBody, fullscreenBody, video, settings, popout, fullscreen, onDock, onError }: PanelSlotProps) {
  // One DOM node per panel for its whole life; it is only ever moved, never recreated.
  const [node] = useState(() => {
    const el = document.createElement('div');
    el.className = 'flex h-full min-h-0 w-full flex-col @container/panel';
    el.dataset.panelNode = '';
    return el;
  });
  const mountRef = useRef<HTMLDivElement>(null);
  const wasPoppedRef = useRef(false);
  const openerRef = useRef<Element | null>(null);
  useLayoutEffect(() => {
    if (popped && !wasPoppedRef.current) openerRef.current = document.activeElement;
    const parent = fullscreenActive ? fullscreenBody() : popped ? popoutBody() : mountRef.current;
    if (parent) placePanelNode(node, parent);
    if (!popped && wasPoppedRef.current) {
      const opener = openerRef.current;
      if (!(opener instanceof HTMLElement && opener.isConnected)) node.querySelector<HTMLElement>('[data-autofocus]')?.focus({ preventScroll: true });
      openerRef.current = null;
    }
    wasPoppedRef.current = popped;
  });
  useLayoutEffect(() => () => { node.remove(); }, [node]);
  const visible = dockedVisible || popped || fullscreenActive;
  return (
    <div className="h-full min-h-0 flex-col" style={{ display: dockedVisible ? 'flex' : 'none' }} hidden={!dockedVisible} data-video-editor-panel-id={panel.id} data-panel-key={panelKey} data-popped={popped ? 'true' : undefined} data-fullscreen={fullscreenActive ? 'true' : undefined}>
      {popped && <div data-testid="panel-popped-placeholder" className="flex flex-1 flex-col items-center justify-center gap-2 p-4 text-center text-sm text-muted-foreground"><p>{panel.label || panel.id} is open in a window</p><button type="button" className="rounded-md border border-border/70 px-2 py-1 text-xs text-foreground hover:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring" onClick={onDock}>Bring back</button></div>}
      <div ref={mountRef} className="min-h-0 flex-1" hidden={popped || fullscreenActive} />
      {createPortal(
        <HostContributionErrorBoundary
          contributionId={panel.id}
          extensionId={panel.extensionId}
          kind="panel"
          label={panel.label}
          onError={onError}
        >
          <PanelContent panel={panel} instanceId={instanceId} visible={visible} video={video} settings={settings} popout={popout} fullscreen={fullscreen} />
        </HostContributionErrorBoundary>,
        node,
      )}
    </div>
  );
}

/** One React instance per qualified contribution in each mounted host. */
export function ExtensionPanelHost({ panels, visiblePanelKeys, video, onError, settingsByPanelKey, poppedPanelKey = null, onPoppedPanelKeyChange, touch = false, fullscreenPanelKey = null, onFullscreenPanelKeyChange }: ExtensionPanelHostProps) {
  const hostId = useId();
  const runtime = useOptionalVideoEditorRuntime();
  const popoutFrameRef = useRef<HTMLDivElement>(null);
  const fullscreenFrameRef = useRef<HTMLDivElement>(null);
  const poppedPanel = poppedPanelKey === null ? undefined : panels.find((panel) => getPanelKey(panel) === poppedPanelKey);
  const fullscreenPanel = fullscreenPanelKey === null ? undefined : panels.find((panel) => getPanelKey(panel) === fullscreenPanelKey);
  const shellRoot = runtime?.shellRootRef?.current ?? null;
  // The frame outlives full screen by one commit: the panel node must move back to its
  // slot (a state-preserving moveBefore) before React removes the frame's DOM.
  const poppedKey = poppedPanel ? getPanelKey(poppedPanel) : null;
  const activeKey = fullscreenPanel ? getPanelKey(fullscreenPanel) : null;
  const [shownPoppedKey, setShownPoppedKey] = useState(poppedKey);
  const [shownFullscreenKey, setShownFullscreenKey] = useState(activeKey);
  if (poppedKey && shownPoppedKey !== poppedKey) setShownPoppedKey(poppedKey);
  if (activeKey && shownFullscreenKey !== activeKey) setShownFullscreenKey(activeKey);
  useLayoutEffect(() => {
    if (!poppedKey && shownPoppedKey) setShownPoppedKey(null);
  }, [poppedKey, shownPoppedKey]);
  useLayoutEffect(() => {
    if (!activeKey && shownFullscreenKey) setShownFullscreenKey(null);
  }, [activeKey, shownFullscreenKey]);
  const shownPopped = shownPoppedKey === null ? undefined : panels.find((panel) => getPanelKey(panel) === shownPoppedKey);
  const shownFullscreen = shownFullscreenKey === null ? undefined : panels.find((panel) => getPanelKey(panel) === shownFullscreenKey);
  return (
    <>
      {shownPopped && onPoppedPanelKeyChange && (
        <PanelPopoutFrame
          key={getPanelKey(shownPopped)}
          ref={popoutFrameRef}
          title={shownPopped.label || shownPopped.id}
          panelKey={getPanelKey(shownPopped)}
          bounds={shellRoot ?? WINDOW_BOUNDS()}
          defaultRect={previewRect(shellRoot)}
          touch={touch}
          onClose={() => onPoppedPanelKeyChange(null)}
        />
      )}
      {shownFullscreen && onFullscreenPanelKeyChange && (
        <PanelFullscreenFrame
          key={getPanelKey(shownFullscreen)}
          ref={fullscreenFrameRef}
          title={shownFullscreen.label || shownFullscreen.id}
          onExit={() => onFullscreenPanelKeyChange(null)}
        />
      )}
      {panels.map((panel) => {
        const key = getPanelKey(panel);
        const popped = key === poppedKey;
        const active = key === activeKey;
        return (
          <PanelSlot
            key={key}
            panel={panel}
            panelKey={key}
            instanceId={`${hostId}:${key}`}
            dockedVisible={visiblePanelKeys.has(key)}
            popped={popped}
            fullscreenActive={active}
            popoutBody={() => popoutFrameRef.current}
            fullscreenBody={() => fullscreenFrameRef.current}
            video={video}
            settings={settingsByPanelKey?.[key]}
            popout={onPoppedPanelKeyChange ? {
              open: popped,
              onOpenChange: (open) => {
                if (open) onPoppedPanelKeyChange(key);
                else if (popped) onPoppedPanelKeyChange(null);
              },
            } : undefined}
            fullscreen={onFullscreenPanelKeyChange ? {
              active,
              enter: () => onFullscreenPanelKeyChange(key),
              exit: () => { if (active) onFullscreenPanelKeyChange(null); },
            } : undefined}
            onDock={() => onPoppedPanelKeyChange?.(null)}
            onError={onError}
          />
        );
      })}
    </>
  );
}

const WINDOW_BOUNDS = (): PanelPopoutBounds => ({ width: window.innerWidth, height: window.innerHeight });

function previewRect(shellRoot: HTMLElement | null): PanelRect {
  const stage = shellRoot?.querySelector<HTMLElement>('[data-video-editor-shell-region="preview"]');
  if (!shellRoot || !stage) return { x: 48, y: 48, width: 960, height: 600 };
  const root = shellRoot.getBoundingClientRect();
  const rect = stage.getBoundingClientRect();
  return { x: rect.left - root.left, y: rect.top - root.top, width: rect.width, height: rect.height };
}
