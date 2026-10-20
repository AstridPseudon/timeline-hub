import { describe, expect, it } from 'vitest';
import type { DocumentPin, HistoryEntry, HistoryPage } from '@/integrations/runtime/timeline-commit-types.ts';
import { resolveSelectedParamAuthority, SelectedParamAuthorityError } from './selectedParamAuthority.ts';

const select = 'parent/clip:effect';
const element = { packId: 'project-pack', id: 'reveal', kind: 'effect', revision: 'element-r1' };
const p1: DocumentPin = { document_id: 'project-document', version: 1, content_digest: 'sha256:document-v1' };
const p2: DocumentPin = { document_id: 'project-document', version: 2, content_digest: 'sha256:document-v2' };
const object = { object_id: 'sha256:object', digest: 'sha256:object', size: 12, media_type: 'application/json' as const };

function record(pin: DocumentPin, op: 'clip.set-element' | 'clip.set-params' = 'clip.set-element', values: Record<string, unknown> = {}) {
  return {
    ordinal: 0,
    command: { schema_version: 1, op, version: '1', select,
      args: op === 'clip.set-element' ? { elementRef: element, schema_source: pin }
        : { values, clear: [], schema_source: pin } },
    writes: [{ ref: select, path: op === 'clip.set-element' ? ['elementRef'] : ['params', 'seed'] }],
    reads: op === 'clip.set-params' ? [{ ref: select, path: ['elementRef'], state: { state: 'present', value: element } }] : [],
    selections: [],
    bindings: [
      { key: 'scalar.target', ref: select, policy: 'fixed', dependencies: ['scalar.images'] },
      { key: 'params.element', ref: select, policy: 'fixed', dependencies: ['params.schema', 'params.snapshot'] },
    ],
    created: [], derived_writes: [],
    dependencies: [
      { key: 'params.schema', kind: 'source', pin, policy: 'exact' },
      { key: 'params.snapshot', kind: 'entity', policy: 'exact', pin: { source: pin, element, object } },
    ],
  };
}

function entry(publication_id: string, revision_id: string, previous: { publication_id: string; revision_id: string } | null,
  commands: unknown[] = [], intent: HistoryEntry['intent'] = 'recorded'): HistoryEntry {
  return { publication_id, revision_id, previous, receipt: {} as HistoryEntry['receipt'], intent,
    records: intent === 'recorded' ? { schema_version: 1, commands, undo_of: [], restored_from: null } : null,
    provider_version: null, compiler_version: null, publisher: 'agent-1' } as HistoryEntry;
}

function page(items: HistoryEntry[], next_cursor: string | null = null): HistoryPage {
  const last = items.at(-1)!;
  return { items, next_cursor, head: { publication_id: last.publication_id, revision_id: last.revision_id } };
}

function selectedHistory(...entries: HistoryEntry[]) {
  const rawClip = { id: 'effect', elementRef: structuredClone(element), params: { seed: 4 } };
  return { history: page(entries), select, rawClip };
}

describe('resolveSelectedParamAuthority', () => {
  it('returns the exact direct-triple pin while ignoring newer unrelated accepted records', () => {
    const root = entry('p0', 'r0', null, [], 'bootstrap');
    const selected = entry('p1', 'r1', { publication_id: 'p0', revision_id: 'r0' }, [record(p1)]);
    const unrelated = entry('p2', 'r2', { publication_id: 'p1', revision_id: 'r1' }, [{
      ordinal: 0, command: { schema_version: 1, op: 'track.set', version: '1', select: 'parent/track:picture', args: {} },
      writes: [{ ref: 'parent/track:picture', path: ['label'] }], bindings: [], dependencies: [], reads: [], selections: [], created: [], derived_writes: [],
    }]);
    expect(resolveSelectedParamAuthority(selectedHistory(root, selected, unrelated))).toEqual(p1);
  });

  it('takes the latest accepted direct selection for the same raw element', () => {
    const root = entry('p0', 'r0', null, [], 'bootstrap');
    const first = entry('p1', 'r1', { publication_id: 'p0', revision_id: 'r0' }, [record(p1)]);
    const second = entry('p2', 'r2', { publication_id: 'p1', revision_id: 'r1' }, [record(p2, 'clip.set-params', { seed: 16 })]);
    expect(resolveSelectedParamAuthority(selectedHistory(root, first, second))).toEqual(p2);
  });

  it.each([
    ['an incomplete page', () => {
      const root = entry('p0', 'r0', null, [], 'bootstrap');
      const selected = entry('p1', 'r1', { publication_id: 'p0', revision_id: 'r0' }, [record(p1)]);
      return { ...selectedHistory(root, selected), history: page([root, selected], 'next-page') };
    }],
    ['a missing predecessor', () => {
      const selected = entry('p1', 'r1', { publication_id: 'missing', revision_id: 'r-missing' }, [record(p1)]);
      return selectedHistory(selected);
    }],
    ['an ambiguous direct triple', () => {
      const root = entry('p0', 'r0', null, [], 'bootstrap');
      const selected = entry('p1', 'r1', { publication_id: 'p0', revision_id: 'r0' }, [{
        ...record(p1), dependencies: [...record(p1).dependencies, { ...record(p1).dependencies[0] }],
      }]);
      return selectedHistory(root, selected);
    }],
    ['a later unknown legacy row effect', () => {
      const root = entry('p0', 'r0', null, [], 'bootstrap');
      const selected = entry('p1', 'r1', { publication_id: 'p0', revision_id: 'r0' }, [record(p1)]);
      const legacy = entry('p2', 'r2', { publication_id: 'p1', revision_id: 'r1' }, [], 'legacy_unknown');
      return selectedHistory(root, selected, legacy);
    }],
    ['an inverse that needs accepted target lineage', () => {
      const root = entry('p0', 'r0', null, [], 'bootstrap');
      const selected = entry('p1', 'r1', { publication_id: 'p0', revision_id: 'r0' }, [record(p1)]);
      const inverse = entry('p2', 'r2', { publication_id: 'p1', revision_id: 'r1' }, [{
        ordinal: 0, command: { schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: ['p1'] } },
        writes: [], bindings: [], dependencies: [], reads: [], selections: [], created: [], derived_writes: [],
      }]);
      return selectedHistory(root, selected, inverse);
    }],
  ])('%s refuses visibly', (_label, build) => {
    expect(() => resolveSelectedParamAuthority(build())).toThrow(SelectedParamAuthorityError);
  });

  it('does not infer authority from a changed raw element or a display-only source', () => {
    const root = entry('p0', 'r0', null, [], 'bootstrap');
    const selected = entry('p1', 'r1', { publication_id: 'p0', revision_id: 'r0' }, [record(p1)]);
    const input = selectedHistory(root, selected);
    input.rawClip = { id: 'effect', elementRef: { ...element, revision: 'display-relabel' } };
    expect(() => resolveSelectedParamAuthority(input)).toThrow('authority is unavailable');
  });
});

