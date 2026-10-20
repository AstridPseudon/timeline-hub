import { useEffect, useLayoutEffect, useRef, useSyncExternalStore } from 'react';
import {
  PUBLIC_ASTRID_SKY_PIXEL,
} from './publicAstridSkyRender';
import {
  PARALLAX_DEPTH,
  PARALLAX_MARGIN,
  SCROLL_DEPTH,
  type PublicAstridSkySession,
} from './publicAstridSkySession';
import './PublicAstridSky.css';
import { PUBLIC_ASTRID_SKY_LAYERS as SKY_LAYERS, type PublicAstridSkyLayer as SkyLayer } from './publicAstridSkyRenderer';

/** Parallax: each layer is drawn this much larger on every side, so shifting it never shows an edge. */

export type { PublicAstridSkySettings } from './publicAstridSkySession';
export {
  DEFAULT_PUBLIC_ASTRID_SKY_SETTINGS,
  PUBLIC_ASTRID_SKY_REPLAY_MS,
  PUBLIC_ASTRID_SKY_REPLAY_SETTLE_MS,
  PUBLIC_ASTRID_SKY_REPLAY_TURN_MS,
  replayOffsetHours,
  skyDate,
  skyLocation,
} from './publicAstridSkySession';
export { quietField } from './publicAstridSkyGeometry';

interface PublicAstridSkyProps {
  session: PublicAstridSkySession;
  reducedMotion?: boolean;
  active?: boolean;
  geometryRoot?: { readonly current: HTMLElement | null };
  geometryOwner?: string;
  /** The page's reading text (a CSS selector). The sky quiets behind it so it stays crisp: the moon's
   *  craters and seas smooth out, its rim softens a little, and the stars and clouds thin. */
  quietBehind?: string;
}

/** A huge pixel sun or moon far behind the page, following the visitor's clock. Decorative only. Drawn as
 *  three layers (sun, moon and stars; far clouds; near clouds) that drift apart a little with the
 *  pointer, for depth. */
function useSkyControls(session: PublicAstridSkySession, active: boolean) {
  return useSyncExternalStore(
    active ? session.subscribeControls : () => () => {},
    session.getControlsSnapshot,
    session.getControlsSnapshot,
  );
}

function useSkyGeometry(
  session: PublicAstridSkySession,
  active: boolean,
  rootRef: { readonly current: HTMLElement | null } | undefined,
  selector: string | undefined,
  owner: string,
) {
  useLayoutEffect(() => {
    if (!active || !rootRef?.current || !selector) return undefined;
    return session.registerGeometryRoot(rootRef.current, selector, owner);
  }, [active, owner, rootRef, selector, session]);
}

export function PublicAstridSky({ session, active = true, geometryRoot, geometryOwner = 'sky', quietBehind }: PublicAstridSkyProps) {
  const canvasRefs = useRef<Record<SkyLayer, HTMLCanvasElement | null>>({ sky: null, stars: null, far: null, near: null });
  const { settings } = useSkyControls(session, active);
  useSkyGeometry(session, settings.enabled && active, geometryRoot, quietBehind, geometryOwner);

  // A single active-view pass consumes the latest values from the independent channels. Parallax
  // wakes only compositor writes; raster/geometry/resize signals coalesce without React frame renders.
  useEffect(() => {
    if (!active || !settings.enabled) return undefined;
    let alive = true;
    let frame = 0;
    let rasterDirty = true;
    let idleHandle: number | null = null;
    let moonKey = '';
    const idle = window.requestIdleCallback ?? ((callback: () => void) => window.setTimeout(callback, 400));
    const cancelIdle = window.cancelIdleCallback ?? window.clearTimeout;
    session.renderer.invalidate();
    const schedule = () => {
      if (alive && !frame) frame = window.requestAnimationFrame(paint);
    };
    const invalidate = () => { rasterDirty = true; schedule(); };
    function paint() {
      if (!alive) return;
      frame = 0;
      // Read: no DOM writes until all scene, viewport and geometry inputs have been captured.
      const snapshot = session.getSnapshot();
      if (!snapshot.visible || !snapshot.settings.enabled) return;
      const settings = snapshot.settings;
      const columns = Math.ceil((window.innerWidth + 2 * PARALLAX_MARGIN) / PUBLIC_ASTRID_SKY_PIXEL);
      const rows = Math.ceil((window.innerHeight + 2 * PARALLAX_MARGIN) / PUBLIC_ASTRID_SKY_PIXEL);
      session.setGeometryViewport(columns, rows);
      const geometry = session.getGeometrySnapshot();
      const quiet = geometry.columns === columns && geometry.rows === rows ? geometry.quiet : null;
      if (rasterDirty) session.renderer.paint({
        columns,
        rows,
        state: { ...snapshot.state, hours: snapshot.cloudHours },
        phase: snapshot.phase,
        // Strength is set for day and night; through twilight it moves between the two.
        intensity: settings.intensity.light + (settings.intensity.dark - settings.intensity.light) * snapshot.darkness,
        reveal: snapshot.reveal,
        tick: snapshot.tick,
        path: settings.path,
        size: settings.size[settings.path],
        lift: settings.lift[settings.path],
        moonScale: settings.moonScale,
        quiet: quiet ?? undefined,
      }, canvasRefs.current);
      rasterDirty = false;
      for (const layer of SKY_LAYERS) {
        const canvas = canvasRefs.current[layer];
        if (!canvas) continue;
        const width = `${columns * PUBLIC_ASTRID_SKY_PIXEL}px`;
        const height = `${rows * PUBLIC_ASTRID_SKY_PIXEL}px`;
        const transform = `translate3d(${snapshot.parallaxX * PARALLAX_DEPTH[layer]}px, ${snapshot.parallaxY * SCROLL_DEPTH[layer]}px, 0)`;
        if (canvas.style.width !== width) canvas.style.width = width;
        if (canvas.style.height !== height) canvas.style.height = height;
        if (canvas.style.transform !== transform) canvas.style.transform = transform;
      }
      const nextMoonKey = [rows, snapshot.phase, settings.size[settings.path], settings.moonScale].join('|');
      if (nextMoonKey !== moonKey) {
        moonKey = nextMoonKey;
        if (idleHandle !== null) cancelIdle(idleHandle);
        idleHandle = idle(() => {
          idleHandle = null;
          if (alive && session.getSnapshot().visible) session.renderer.prepareMoon(rows, snapshot.phase, settings.size[settings.path], settings.moonScale);
        });
      }
    }
    const cleanups = [session.subscribeRaster(invalidate), session.subscribeGeometry(invalidate), session.subscribeParallax(schedule)];
    window.addEventListener('resize', invalidate);
    schedule();
    return () => {
      alive = false;
      window.cancelAnimationFrame(frame);
      if (idleHandle !== null) cancelIdle(idleHandle);
      cleanups.forEach((cleanup) => cleanup());
      window.removeEventListener('resize', invalidate);
      session.renderer.invalidate();
    };
  }, [active, session, settings.enabled]);

  if (!settings.enabled) return null;
  const renderLayer = (layer: SkyLayer) => (
    <canvas
      key={layer}
      ref={(node) => { canvasRefs.current[layer] = node; }}
      data-layer={layer}
      style={{
        left: -PARALLAX_MARGIN,
        top: -PARALLAX_MARGIN,
      }}
    />
  );
  return (
    <div className="astrid-sky" aria-hidden="true">
      {SKY_LAYERS.map(renderLayer)}
    </div>
  );
}

export function usePublicAstridSkyControls(session: PublicAstridSkySession, active = true) {
  return useSkyControls(session, active);
}
