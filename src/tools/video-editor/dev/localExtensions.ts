/**
 * Editor extensions admitted by Astrid's generated catalog plus the App-owned
 * read-only transcript consumer. Deployment release flags still gate production.
 *
 * `VideoEditorPage` applies deployment-owned release flags before activating
 * these entries in production. DEV honors the Extension Manager's local
 * disabled-ID store. Host-only smoke checks remain separate from this catalog.
 */
import type { ReighExtension } from '@reigh/editor-sdk';
import { ASTRID_EDITOR_EXTENSIONS } from '@astrid/packs/rendering/editor/catalog';
import { transcriptCaptionFoundryExtension } from '@/tools/video-editor/extensions/transcript-caption-foundry/extension';

export const devLocalExtensions: ReighExtension[] = [
  ...ASTRID_EDITOR_EXTENSIONS,
  transcriptCaptionFoundryExtension,
];
