/**
 * Test-only extension for browser specs. It contributes:
 * - `OVERLAY_LAYER_FIXTURE_COUNT` independent `timelineOverlay` layers, each with one coincident
 *   ruler marker. The host pages marker layers (3 below 640 px, 6 above), so a spec needs more layers
 *   than one page holds; this supplies them without depending on a product extension. Layers are keyed
 *   `<extension id>:<contribution id>`.
 * - one empty `panel`. The right dock's Extensions tab (and its Manage button) is only reachable while
 *   some enabled extension contributes a panel, and the other fixture extensions contribute none.
 */
import { createElement } from 'react';
import { defineExtension } from '@astrid/editor-sdk';
import type {
  AstridExtension,
  ContributionId,
  DisposeHandle,
  ExtensionId,
  PanelRenderProps,
  TimelineOverlayRenderProps,
} from '@astrid/editor-sdk';
import type { ReactNode } from 'react';

export const OVERLAY_LAYERS_FIXTURE_EXTENSION_ID = 'haus.astrid.e2e-overlay-layers' as ExtensionId;
/** More than one desktop page (6) so the pager has a second page next to the scene-phase layer. */
export const OVERLAY_LAYER_FIXTURE_COUNT = 7;

const PANEL_RENDER_ID = 'panel/render';
const layerIds = Array.from({ length: OVERLAY_LAYER_FIXTURE_COUNT }, (_, index) => `layer-${index + 1}`);

export const overlayLayersFixtureExtension: AstridExtension = defineExtension({
  manifest: {
    id: OVERLAY_LAYERS_FIXTURE_EXTENSION_ID,
    version: '1.0.0',
    label: 'E2E overlay layers',
    description: 'Test fixture: several marker layers whose markers coincide on the ruler, and an empty panel.',
    apiVersion: 1,
    license: 'MIT',
    contributions: [
      ...layerIds.map((layerId, index) => ({
        id: layerId as ContributionId,
        kind: 'timelineOverlay' as const,
        render: `${layerId}/render`,
        order: 20 + index,
        label: `Overlay layer ${index + 1}`,
      })),
      {
        id: 'panel' as ContributionId,
        kind: 'panel' as const,
        render: PANEL_RENDER_ID,
        label: 'E2E fixture panel',
      },
    ],
  },
  activate(ctx) {
    const handles: DisposeHandle[] = layerIds.map((layerId, index) => ctx.ui.registerRenderer<TimelineOverlayRenderProps>(
      `${layerId}/render`,
      (props) => props.primitives.markerLayer({
        markers: [{ id: `${layerId}-marker`, time: 2, label: String(index + 1) }],
        placement: 'ruler',
        interactive: false,
        snap: false,
      }) as ReactNode,
    ));
    handles.push(ctx.ui.registerRenderer<PanelRenderProps>(
      PANEL_RENDER_ID,
      () => createElement('div', { 'data-testid': 'e2e-fixture-panel' }) as ReactNode,
    ));
    return {
      dispose() {
        for (const handle of handles) handle.dispose();
      },
    };
  },
});
