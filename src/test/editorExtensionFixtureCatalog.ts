/**
 * Fixed extension inventory for browser capability-matrix tests.
 *
 * This file is selected only by the `serve`-only Vite alias gated with
 * ASTRID_APP_E2E_EXTENSION_FIXTURES=1. Production builds and ordinary development
 * sessions continue to use Astrid's generated editor catalog. Keep this list
 * explicit: it is a test fixture, not an extension discovery mechanism.
 */
import type { AstridExtension } from '@astrid/editor-sdk';
import { scenePhaseMarkersExtension } from '@/tools/video-editor/dev/scene-phase-markers/extension';
import { transcriptLaneExtension } from '@/tools/video-editor/dev/transcript-lane/extension';
import { runawayTimelineExtension } from '@/tools/video-editor/dev/runaway-timeline/extension';
import { creativeLabExtensions } from '@/tools/video-editor/examples/extensions/creative-lab';

export const devLocalExtensions: AstridExtension[] = [
  scenePhaseMarkersExtension,
  transcriptLaneExtension,
  runawayTimelineExtension,
  ...creativeLabExtensions,
];
