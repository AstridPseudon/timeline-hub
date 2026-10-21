import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import {
  TIMELINE_POSTPROCESS_SHADER_APP_KEY,
} from '@/tools/video-editor/lib/timeline-domain.ts';
import type {
  TimelineClipShaderMetadata,
  TimelinePostprocessShaderMetadata,
} from '@/tools/video-editor/types/index.ts';

type ShaderInspectorTarget =
  | { scope: 'clip'; clipId: string }
  | { scope: 'postprocess' };

type ShaderInspectorMetadata = TimelineClipShaderMetadata | TimelinePostprocessShaderMetadata;

export class ShaderInspectorCaptureRefusal extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ShaderInspectorCaptureRefusal';
  }
}

/**
 * Build the existing patch shape without activating it in ShaderInspector.
 * Native Agent has no command for either shader metadata root yet.
 */
export function buildShaderInspectorPatch(
  target: ShaderInspectorTarget,
  shader: ShaderInspectorMetadata,
  version = 1,
): TimelinePatch {
  if (!Number.isSafeInteger(version) || version < 0) {
    throw new ShaderInspectorCaptureRefusal('Shader metadata requires a valid patch version');
  }

  if (target.scope !== shader.scope) {
    throw new ShaderInspectorCaptureRefusal(
      `Shader metadata scope ${shader.scope} does not match ${target.scope} target`,
    );
  }

  if (target.scope === 'clip') {
    if (!target.clipId.trim()) {
      throw new ShaderInspectorCaptureRefusal('Clip shader metadata requires a stable clip identity');
    }

    return {
      version,
      source: 'shader-inspector',
      operations: [{
        op: 'clip.update',
        target: target.clipId,
        payload: { app: { shader } },
      }],
    };
  }

  return {
    version,
    source: 'shader-inspector',
    operations: [{
      op: 'app.update',
      target: TIMELINE_POSTPROCESS_SHADER_APP_KEY,
      payload: shader,
    }],
  };
}
