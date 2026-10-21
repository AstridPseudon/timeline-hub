import { describe, expect, it } from 'vitest';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import {
  assignTimelinePostprocessShader,
  TIMELINE_POSTPROCESS_SHADER_APP_KEY,
} from '../lib/timeline-domain.ts';
import type { TimelinePostprocessShaderMetadata } from '../types/index.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { captureProjectDataMember, executeProjectDataMember } from './projectDataMember.ts';
import { environment } from './__tests__/commitSessionEnvironment.ts';

const originalShader: TimelinePostprocessShaderMetadata = {
  scope: 'postprocess',
  extensionId: 'com.example.shader',
  contributionId: 'post-grade',
  shaderId: 'shader.postGrade',
  uniforms: { exposure: 0.1 },
  opaque: { retained: [null, false, { order: 1 }] },
};

async function authoredBundle() {
  const env = await environment();
  const bundle = await authoringBundleFromDocument(env.initial.canonicalDocument);
  bundle.parent.config = {
    app: {
      [TIMELINE_POSTPROCESS_SHADER_APP_KEY]: structuredClone(originalShader),
    },
  };
  return bundle;
}

function replaceShaderId(value: string): TimelinePatch {
  return {
    version: 1,
    operations: [{
      op: 'project-data.write',
      target: TIMELINE_POSTPROCESS_SHADER_APP_KEY,
      payload: { key: 'shaderId', value, mode: 'replace' },
    }],
  };
}

describe('postprocess shader project-data carrier boundary', () => {
  it('preserves the raw root shape, opaque siblings, order, and absence while replacing one key', async () => {
    const bundle = await authoredBundle();
    const patch = replaceShaderId(originalShader.shaderId);

    const captured = captureProjectDataMember(bundle, patch);
    const root = (captured.bundle.parent.config as Record<string, any>).app[
      TIMELINE_POSTPROCESS_SHADER_APP_KEY
    ];

    expect(root).toEqual(originalShader);
    expect(Object.keys(root)).toEqual(Object.keys(originalShader));
    expect(root.opaque).toEqual(originalShader.opaque);
    expect(root).not.toHaveProperty('enabled');
    expect(captured.commands[0].args).toEqual({
      target: TIMELINE_POSTPROCESS_SHADER_APP_KEY,
      key: 'shaderId',
      value: originalShader.shaderId,
      mode: 'replace',
    });

    const replayed = executeProjectDataMember(bundle, captured.commands);
    expect(replayed.bundle).toEqual(captured.bundle);
  });

  it('accepts a leaf identity change that the postprocess source authority must refuse', async () => {
    const bundle = await authoredBundle();
    const replacement: TimelinePostprocessShaderMetadata = {
      ...originalShader,
      shaderId: 'shader.postVignette',
    };
    const authority = assignTimelinePostprocessShader(
      { app: { [TIMELINE_POSTPROCESS_SHADER_APP_KEY]: originalShader } },
      replacement,
    );

    expect(authority).toMatchObject({ ok: false, code: 'shader_scope_occupied' });

    const captured = captureProjectDataMember(bundle, replaceShaderId(replacement.shaderId));
    expect((captured.bundle.parent.config as Record<string, any>).app[
      TIMELINE_POSTPROCESS_SHADER_APP_KEY
    ]).toMatchObject({
      ...originalShader,
      shaderId: replacement.shaderId,
    });
  });
});
