/**
 * Pack-authored editor extensions admitted by Astrid's generated catalog.
 *
 * `VideoEditorPage` admits only reviewed extensions before activating
 * these entries in production. Both builds honor the Extension Manager's
 * built-in disabled-ID store. Host-only smoke checks remain separate from this catalog.
 */
import type { AstridExtension } from '@astrid/editor-sdk';
import { ASTRID_EDITOR_EXTENSIONS } from '@astrid/packs/rendering/editor/catalog';
import { scenePhaseMarkersExtension } from './scene-phase-markers/extension';

// Scene Phase Markers is an App-owned reviewed extension admitted alongside
// the generated pack catalog so its ordinary producer runs through the host.
export const devLocalExtensions: AstridExtension[] = [
  ...ASTRID_EDITOR_EXTENSIONS,
  scenePhaseMarkersExtension,
];
