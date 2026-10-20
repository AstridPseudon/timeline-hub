/**
 * Pack-authored editor extensions admitted by Astrid's generated catalog.
 *
 * `VideoEditorPage` admits only reviewed extensions before activating
 * these entries in production. DEV honors the Extension Manager's local
 * disabled-ID store. Host-only smoke checks remain separate from this catalog.
 */
import type { AstridExtension } from '@astrid/editor-sdk';
import { ASTRID_EDITOR_EXTENSIONS } from '@astrid/packs/rendering/editor/catalog';
import { scenePhaseMarkersExtension } from './scene-phase-markers/extension';

// Scene Phase Markers remains an App-owned reviewed extension. Keep the
// generated Astrid pack catalog intact while admitting this existing editor
// surface to the normal host in which its project-data producer is exercised.
export const devLocalExtensions: AstridExtension[] = [
  ...ASTRID_EDITOR_EXTENSIONS,
  scenePhaseMarkersExtension,
];
