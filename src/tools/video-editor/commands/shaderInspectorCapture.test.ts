import { describe, expect, it } from 'vitest';
import {
  buildShaderInspectorPatch,
  ShaderInspectorCaptureRefusal,
} from '@/tools/video-editor/commands/shaderInspectorCapture.ts';
import type {
  TimelineClipShaderMetadata,
  TimelinePostprocessShaderMetadata,
} from '@/tools/video-editor/types/index.ts';

const clipShader: TimelineClipShaderMetadata = {
  scope: 'clip',
  extensionId: 'com.example.shader',
  contributionId: 'wash',
  shaderId: 'wash',
  uniforms: { intensity: 0.75 },
  metadata: {
    retained: null,
    opaque: [false, 0],
  },
};

const postprocessShader: TimelinePostprocessShaderMetadata = {
  scope: 'postprocess',
  extensionId: 'com.example.shader',
  contributionId: 'post-wash',
  shaderId: 'post-wash',
  enabled: false,
  uniforms: { intensity: 0.25 },
};

describe('ShaderInspector dormant patch builder', () => {
  it('builds a clip metadata patch without narrowing or dropping opaque shader roots', () => {
    expect(buildShaderInspectorPatch({ scope: 'clip', clipId: 'clip-1' }, clipShader, 7)).toEqual({
      version: 7,
      source: 'shader-inspector',
      operations: [{
        op: 'clip.update',
        target: 'clip-1',
        payload: { app: { shader: clipShader } },
      }],
    });
  });

  it('builds a postprocess metadata patch at the existing timeline app root', () => {
    expect(buildShaderInspectorPatch({ scope: 'postprocess' }, postprocessShader)).toEqual({
      version: 1,
      source: 'shader-inspector',
      operations: [{
        op: 'app.update',
        target: 'shaderPostprocess',
        payload: postprocessShader,
      }],
    });
  });

  it('refuses a scope mismatch before producing a patch', () => {
    expect(() => buildShaderInspectorPatch(
      { scope: 'clip', clipId: 'clip-1' },
      postprocessShader,
    )).toThrow(ShaderInspectorCaptureRefusal);
  });

  it('refuses a missing clip identity without converting the draft to an arbitrary target', () => {
    expect(() => buildShaderInspectorPatch(
      { scope: 'clip', clipId: '  ' },
      clipShader,
    )).toThrow('stable clip identity');
  });
});
