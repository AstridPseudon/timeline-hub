import { useCallback, useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
import { Thumbnail } from '@remotion/player';
import type { PanelFrameAnchor, PanelPreviewService } from '@/sdk/ui.ts';
import { TimelineRenderer } from '../../compositions/TimelineRenderer.tsx';
import { useOptionalVideoEditorRuntime } from '../../contexts/VideoEditorRuntimeContext.tsx';
import { projectOutputTimelineConfig } from '../../data/timelineOutputProjection.ts';
import { getClipDurationInFrames, parseResolution, secondsToFrames } from '../../lib/config-utils.ts';
import { cloneFrame, FramePreviewCache, timelineSecondsToFrame } from '../../lib/frame-preview-cache.ts';
import { areShotsSettling } from '../../lib/shots-settling.ts';
import { getAdmittedElementReadiness, getAdmittedElementSelection, subscribeAdmittedElementReadiness, subscribeAdmittedElements } from '../../runtime/admitted-elements.ts';
import type { ResolvedTimelineConfig } from '../../types/index.ts';

interface FrameRequest { seconds: number; anchor: PanelFrameAnchor }

/** A per-panel service; handles from an earlier word cannot dismiss a newer one. */
export function usePanelFramePreview() {
  const [request, setRequest] = useState<FrameRequest | null>(null);
  const preview = useMemo<PanelPreviewService>(() => ({
    showFrame: (input) => {
      const next = { ...input };
      setRequest(next);
      return { dispose: () => setRequest((current) => current === next ? null : current) };
    },
  }), []);
  const dismiss = useCallback(() => setRequest(null), []);
  useEffect(() => {
    window.addEventListener('scroll', dismiss, true);
    window.addEventListener('resize', dismiss);
    return () => {
      window.removeEventListener('scroll', dismiss, true);
      window.removeEventListener('resize', dismiss);
    };
  }, [dismiss]);
  return { preview, request };
}

/** Fixed viewport placement keeps the card out of scroll clipping and off the word. */
export function framePreviewPlacement(anchor: PanelFrameAnchor, aspect: number, viewportWidth: number, viewportHeight: number) {
  const gap = 8;
  const above = Math.max(0, anchor.top - gap * 2);
  const below = Math.max(0, viewportHeight - anchor.top - anchor.height - gap * 2);
  const preferredHeight = Math.min(160, 240 / aspect, (viewportWidth - gap * 2) / aspect);
  const flip = above < preferredHeight && below > above;
  const height = Math.min(preferredHeight, flip ? below : above);
  const width = height * aspect;
  return {
    width, height,
    left: Math.max(gap, Math.min(anchor.left + anchor.width / 2 - width / 2, viewportWidth - gap - width)),
    top: flip ? anchor.top + anchor.height + gap : anchor.top - gap - height,
  };
}

/** One reusable Remotion still, with bounded frozen DOM frames for return visits. */
export function TimelineFramePreview({ config, request }: { config: ResolvedTimelineConfig | null; request: FrameRequest | null }) {
  const runtime = useOptionalVideoEditorRuntime();
  const admission = useSyncExternalStore(subscribeAdmittedElements, getAdmittedElementSelection, getAdmittedElementSelection);
  const readiness = useSyncExternalStore(subscribeAdmittedElementReadiness, getAdmittedElementReadiness, getAdmittedElementReadiness);
  const output = useMemo(() => config ? projectOutputTimelineConfig(config).config : null, [config]);
  const revision = useMemo(() => ({ output, admission, readiness, host: runtime?.astridElementHost }), [output, admission, readiness, runtime?.astridElementHost]);
  const [cache] = useState(() => new FramePreviewCache<HTMLElement>());
  const [delivery, setDelivery] = useState<{ revision: object; frame: number } | null>(null);
  const [, refresh] = useState(0);
  const live = useRef<HTMLDivElement>(null);
  const frozen = useRef<HTMLDivElement>(null);
  const metadata = useMemo(() => {
    if (!output) return null;
    const fps = output.output.fps;
    const { width, height } = parseResolution(output.output.resolution);
    return {
      fps, compositionWidth: width, compositionHeight: height,
      durationInFrames: Math.max(1, ...output.clips.map((clip) => secondsToFrames(clip.at, fps) + getClipDurationInFrames(clip, fps))),
    };
  }, [output]);
  const frame = request && metadata ? timelineSecondsToFrame(request.seconds, metadata.fps, metadata.durationInFrames) : null;
  const cached = frame === null ? undefined : cache.get(revision, frame);
  const preparing = Boolean(output && runtime?.project?.projectId && runtime.astridElementHost?.isPreviewPreparing?.(runtime.project.projectId, output.clips));
  const settling = areShotsSettling(runtime?.shots);
  const inputProps = useMemo(() => ({ config: output!, ...(runtime?.astridElementHost ? { astridElementHost: runtime.astridElementHost } : {}) }), [output, runtime?.astridElementHost]);

  useEffect(() => {
    if (frame !== null && !cached) setDelivery({ revision, frame });
  }, [revision, frame, cached]);

  // Decode and paint first. Late child-shot loads, video seeks and image loads
  // restart capture; a loading placeholder is never retained as a film frame.
  useEffect(() => {
    const root = live.current;
    if (!root || !delivery || delivery.revision !== revision || preparing || settling) return;
    let raf = 0;
    let stopped = false;
    const schedule = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        raf = requestAnimationFrame(() => {
          if (stopped || root.querySelector('[data-testid="shot-preview-loading"], [data-frame-loading]')) return;
          const composition = root.firstElementChild;
          const snapshot = composition instanceof HTMLElement ? cloneFrame(composition) : null;
          if (snapshot) {
            cache.set(revision, delivery.frame, snapshot);
            refresh((value) => value + 1);
          }
        });
      });
    };
    const observer = new MutationObserver(schedule);
    observer.observe(root, { subtree: true, childList: true, attributes: true });
    for (const event of ['load', 'loadeddata', 'seeked']) root.addEventListener(event, schedule, true);
    schedule();
    return () => {
      stopped = true;
      cancelAnimationFrame(raf);
      observer.disconnect();
      for (const event of ['load', 'loadeddata', 'seeked']) root.removeEventListener(event, schedule, true);
    };
  }, [cache, revision, delivery, preparing, settling]);

  useEffect(() => {
    frozen.current?.replaceChildren(...(cached ? [cached] : []));
  }, [cached]);

  if (!output || !metadata || !delivery) return null;
  const placement = framePreviewPlacement(request?.anchor ?? { left: 0, top: 0, width: 0, height: 0 }, metadata.compositionWidth / metadata.compositionHeight, window.innerWidth, window.innerHeight);
  const visible = frame !== null && placement.height > 0;
  return createPortal(
    <div className="transcript-frame-preview rounded-md border border-border bg-popover shadow-lg" role={visible ? 'tooltip' : undefined} aria-label="Film frame preview" aria-hidden={!visible}
      style={{ position: 'fixed', zIndex: 100, pointerEvents: 'none', overflow: 'hidden', ...placement, visibility: visible ? 'visible' : 'hidden' }}>
      <div ref={frozen} style={{ position: 'absolute', width: 240, height: 240 * metadata.compositionHeight / metadata.compositionWidth, transform: `scale(${placement.width / 240})`, transformOrigin: 'top left', visibility: cached ? 'visible' : 'hidden' }} />
      <div ref={live} style={{ width: 240, height: 240 * metadata.compositionHeight / metadata.compositionWidth, transform: `scale(${placement.width / 240})`, transformOrigin: 'top left', visibility: cached || preparing || settling || delivery.revision !== revision || delivery.frame !== frame ? 'hidden' : 'inherit' }}>
        <Thumbnail component={TimelineRenderer} inputProps={inputProps} {...metadata} frameToDisplay={Math.min(delivery.frame, metadata.durationInFrames - 1)} style={{ width: '100%', height: '100%' }}
          renderLoading={() => <div data-frame-loading="" />} />
      </div>
    </div>, document.body,
  );
}
