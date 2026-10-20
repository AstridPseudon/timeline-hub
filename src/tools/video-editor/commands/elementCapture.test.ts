import { describe, expect, it } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import {
  captureClipElement,
  captureClipElementParams,
  executeClipElement,
  finishClipElement,
} from './elementCapture.ts';
import { AuthoredState } from './clipMovePrimitives.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';

const pin = { document_id: 'document:pack', version: 3, content_digest: 'sha256:pack' } as const;

const bundle = (): AuthoredBundle => ({
  project_id: 'project',
  timeline_id: 'film',
  base_parent: { revision_id: 'parent', content_digest: 'sha256:parent' },
  parent: {
    clips: [{
      id: 'effect',
      clipType: 'effect',
      elementRef: { id: 'effect', kind: 'effect', revision: 'draft-1' },
      params: { keep: { nested: [null, false, 'opaque'] }, value: 1 },
      at: 0,
      hold: 2,
      track: 'picture',
    }],
    config: { clips: [], tracks: [{ id: 'picture', kind: 'visual' }] },
  },
  placements: [],
  shots: {},
  source_mapping: {
    _runtime_document: { dependency_manifest: { documents: [pin] } },
    pinned_documents: [{ pin, document: { document_id: pin.document_id } }],
  },
});

const selectedBundle = (): AuthoredBundle => {
  const value = bundle();
  const clip = value.parent.clips[0] as Record<string, unknown>;
  clip.elementRef = { id: 'effect', kind: 'effect', packId: 'pack', revision: 'sha256:old' };
  return value;
};

const clip = (value: AuthoredBundle, ref = 'parent/clip:effect') => new AuthoredState(value).entity(ref)!;

describe('bounded native existing-clip element capture', () => {
  it('captures a revision and literal params without replacing unknown clip fields', () => {
    const input = bundle();
    const basis = captureClipElement(input, 'parent/clip:effect', {
      elementRef: { id: 'effect', kind: 'effect', revision: 'draft-2' },
    });
    const revision = finishClipElement(basis, {
      elementRef: { id: 'effect', kind: 'effect', revision: 'draft-2' },
    });
    expect(revision.command).toMatchObject({
      op: 'clip.set-element',
      select: 'parent/clip:effect',
      args: { elementRef: { id: 'effect', kind: 'effect', revision: 'draft-2' } },
    });
    expect(clip(revision.bundle).elementRef).toEqual({ id: 'effect', kind: 'effect', revision: 'draft-2' });

    const paramsBasis = captureClipElementParams(revision.bundle, 'parent/clip:effect', {
      values: { value: 2, unknown: { keep: true } }, clear: ['missing'],
    });
    expect(paramsBasis.command.op).toBe('clip.set-params');
    expect((paramsBasis.command.args.values as Record<string, unknown>).unknown).toEqual({ keep: true });
    expect(clip(paramsBasis.bundle).params).toEqual({ keep: { nested: [null, false, 'opaque'] }, value: 1 });
  });

  it('refuses selected-pack capture without Agent authority and preserves the draft', () => {
    const input = selectedBundle();
    const snapshot = structuredClone(input);
    const args = {
      elementRef: { id: 'effect', kind: 'effect', packId: 'pack', revision: 'sha256:new' },
      schema_source: pin,
    } as const;
    expect(() => captureClipElement(input, 'parent/clip:effect', args))
      .toThrow(/authoritative Agent schema capture/);
    expect(input).toEqual(snapshot);
    expect(() => captureClipElementParams(input, 'parent/clip:effect', {
      values: { literal: { unknown: [null, false] } }, clear: ['value'], schema_source: pin,
    })).toThrow(/authoritative Agent schema capture/);
    expect(input).toEqual(snapshot);
  });

  it('refuses fabricated or missing retained pins and unsafe identity changes', () => {
    const input = selectedBundle();
    expect(() => captureClipElement(input, 'parent/clip:effect', {
      elementRef: { id: 'effect', kind: 'effect', packId: 'pack', revision: 'sha256:new' },
    })).toThrow(/authoritative Agent schema capture/);
    expect(() => captureClipElement(input, 'parent/clip:effect', {
      elementRef: { id: 'effect', kind: 'effect', packId: 'pack', revision: 'sha256:new' },
      schema_source: { document_id: 'fake', version: 1, content_digest: 'sha256:fake' },
    })).toThrow(/authoritative Agent schema capture/);
    expect(() => captureClipElement(input, 'parent/clip:effect', {
      elementRef: { id: 'other', kind: 'effect', packId: 'pack', revision: 'sha256:new' },
      schema_source: pin,
    })).toThrow(/keep the element id/);
    expect(() => executeClipElement(input, {
      schema_version: 1, op: 'timeline.apply_element', version: '1', select: 'parent/clip:effect', args: {},
    } as EditCommand)).toThrow(/unsupported clip.set-element/);
  });
});
