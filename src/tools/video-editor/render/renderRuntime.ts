import type { RenderExportDestination } from '@/tools/video-editor/lib/renderRouter.ts';

export interface RenderRuntime {
  projectId: string;
  destination?: RenderExportDestination;
}
