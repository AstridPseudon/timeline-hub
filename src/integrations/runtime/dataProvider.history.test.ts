import { describe, expect, it } from 'vitest';
import type { HistoryPage, Transport } from './generated.ts';
import { historyEntry } from './__tests__/timelineCommitFixture.ts';
import { RuntimeDataProvider } from './dataProvider.ts';
import { PROJECT_ID, TIMELINE_ID, json, runtimeFixture } from '@/test/fakeWorkspaceRuntime.ts';

const request = { projectId: PROJECT_ID, parentDocumentId: TIMELINE_ID };
const scope = { projectId: PROJECT_ID, timelineId: TIMELINE_ID };
const head = { revision_id: 'parent-r1', publication_id: 'publication-current' };
const current = () => historyEntry(head, scope);
const page = (): HistoryPage => ({ items: [current()], head, next_cursor: null });
const timelinePath = `/v1/projects/${PROJECT_ID}/timelines/${TIMELINE_ID}`;

function setup(
  pages: unknown[],
  mutateParent?: (parent: Record<string, unknown>) => void,
) {
  const fixture = runtimeFixture();
  const calls: Array<{ method: string; path: string }> = [];
  let pageIndex = 0;
  const transport: Transport = async (...args) => {
    const [method, path] = args;
    calls.push({ method, path });
    if (method === 'GET' && path.startsWith(`${timelinePath}/commits?`)) {
      const value = pages[pageIndex++];
      if (value instanceof Error) throw value;
      return { status: 200, headers: {}, body: json(value) };
    }
    const response = await fixture.transport(...args);
    if (mutateParent && method === 'GET' && path.startsWith(`${timelinePath}/composition-revisions/`)) {
      const parent = JSON.parse(new TextDecoder().decode(response.body));
      mutateParent(parent);
      return { ...response, body: json(parent) };
    }
    return response;
  };
  const provider = new RuntimeDataProvider({ projectId: PROJECT_ID, transport });
  return { provider, calls, fixture, list: () => provider.shotComposition.listHistory!(request) };
}

describe('RuntimeDataProvider accepted history', () => {
  it('keeps Runtime page order and repeated revisions, with real metadata and exact head pairs', async () => {
    const bootstrap = historyEntry({ revision_id: 'parent-old', publication_id: 'publication-bootstrap' }, scope, {
      intent: 'bootstrap', records: null, publisher: null, provider_version: null, compiler_version: null,
    });
    const legacy = historyEntry({ revision_id: head.revision_id, publication_id: 'publication-legacy' }, scope, {
      intent: 'legacy_unknown', records: null, publisher: null, provider_version: null, compiler_version: null,
    });
    const recorded = { ...current(), label: 'Restore opening', rationale: 'Keep the original framing' };
    for (const entry of [bootstrap, legacy]) {
      entry.receipt.command_kind = 'parent_composition.publish';
      entry.receipt.result = {
        project_id: PROJECT_ID, timeline_id: TIMELINE_ID,
        parent_revision_id: entry.revision_id,
      };
    }
    recorded.receipt.created_at = '2026-10-20T10:00:00Z';
    const { list, calls } = setup([
      { items: [bootstrap, legacy], next_cursor: 'next/+==', head },
      { items: [recorded], next_cursor: null, head },
    ]);

    const entries = await list();

    expect(entries.map((entry) => [entry.publicationId, entry.revisionId, entry.isCurrentHead])).toEqual([
      ['publication-bootstrap', 'parent-old', false],
      ['publication-legacy', 'parent-r1', false],
      ['publication-current', 'parent-r1', true],
    ]);
    expect(entries[1]).toMatchObject({ intent: 'legacy_unknown', publisher: null });
    expect(entries[1]).not.toHaveProperty('records');
    expect(entries[1]).not.toHaveProperty('undoable');
    expect(entries[2]).toMatchObject({
      projectId: PROJECT_ID, parentDocumentId: TIMELINE_ID,
      publisher: 'actor-1', label: recorded.label, rationale: recorded.rationale,
      createdAt: recorded.receipt.created_at, contentDigest: `sha256:${'1'.repeat(64)}`,
    });
    expect(calls.filter((call) => call.path.includes('/commits?')).map((call) => call.path)).toEqual([
      `${timelinePath}/commits?limit=50`,
      `${timelinePath}/commits?limit=50&cursor=next%2F%2B%3D%3D`,
    ]);
    expect(calls.some((call) => call.path === `${timelinePath}/composition-revisions`
      || call.path.startsWith(`${timelinePath}/composition-revisions?`))).toBe(false);
    expect(calls.every((call) => call.method === 'GET' || call.path === '/v1/handshake')).toBe(true);
  });

  it('shares concurrent history and normal immutable reads, then refreshes history without a persistent cache', async () => {
    const { list, calls, provider } = setup([page(), page()]);
    const [first, second] = await Promise.all([
      list(), list(), provider.shotComposition.loadAtHead!({ ...request, headRevisionId: head.revision_id }),
    ]);
    expect(first).toEqual(second);
    expect(calls.filter((call) => call.path.includes('/commits?'))).toHaveLength(1);
    expect(calls.filter((call) => call.path.endsWith('/composition-revisions/parent-r1'))).toHaveLength(1);
    await list();
    expect(calls.filter((call) => call.path.includes('/commits?'))).toHaveLength(2);
  });

  it('retries a failed history read and never falls back to revision listings', async () => {
    const { list, calls } = setup([new Error('Runtime history unavailable'), page()]);
    await expect(list()).rejects.toThrow('Runtime history unavailable');
    await expect(list()).resolves.toHaveLength(1);
    expect(calls.filter((call) => call.path.includes('/commits?'))).toHaveLength(2);
    expect(calls.filter((call) => call.path.includes('/composition-revisions'))).toEqual([
      { method: 'GET', path: `${timelinePath}/composition-revisions/parent-r1` },
    ]);
  });

  it('rejects a request outside the provider project before reading', async () => {
    const { provider, calls } = setup([]);
    await expect(provider.shotComposition.listHistory!({ ...request, projectId: 'other-project' }))
      .rejects.toThrow('provider project');
    expect(calls).toEqual([]);
  });

  it('preserves optional empty labels and rationale from the official history DTO', async () => {
    const { list } = setup([{ ...page(), items: [{ ...current(), label: '', rationale: '' }] }]);
    await expect(list()).resolves.toEqual([expect.objectContaining({ label: '', rationale: '' })]);
  });

  it.each([
    ['missing head', { ...page(), head: undefined }],
    ['missing head publication', { ...page(), head: { revision_id: head.revision_id } }],
    ['missing head revision', { ...page(), head: { publication_id: head.publication_id } }],
    ['missing items', { ...page(), items: undefined }],
    ['missing cursor', { ...page(), next_cursor: undefined }],
    ['malformed cursor', { ...page(), next_cursor: 12 }],
    ['empty cursor', { ...page(), next_cursor: '' }],
    ['missing publication', { ...page(), items: [{ ...current(), publication_id: undefined }] }],
    ['missing revision', { ...page(), items: [{ ...current(), revision_id: undefined }] }],
    ['foreign receipt project', { ...page(), items: [{ ...current(), receipt: { ...current().receipt, project_id: 'other-project' } }] }],
    ['mismatched receipt publication', { ...page(), items: [{ ...current(), receipt: { ...current().receipt, receipt_id: 'other-publication' } }] }],
    ['invalid timestamp', { ...page(), items: [{ ...current(), receipt: { ...current().receipt, created_at: 'not-a-date' } }] }],
    ['missing timestamp', { ...page(), items: [{ ...current(), receipt: { ...current().receipt, created_at: undefined } }] }],
    ['unknown intent', { ...page(), items: [{ ...current(), intent: 'unverified' }] }],
    ['missing attribution', { ...page(), items: [{ ...current(), publisher: undefined }] }],
    ['malformed rationale', { ...page(), items: [{ ...current(), rationale: { text: 'reason' } }] }],
    ['duplicate publications', { ...page(), items: [current(), current()] }],
    ['missing current head pair', { ...page(), head: { ...head, publication_id: 'absent-publication' } }],
    ['mismatched current head revision', { ...page(), head: { ...head, revision_id: 'absent-revision' } }],
  ])('visibly refuses %s', async (_label, value) => {
    const { list, calls } = setup([value]);
    await expect(list()).rejects.toThrow();
    expect(calls.some((call) => call.path.startsWith(`${timelinePath}/composition-revisions?`))).toBe(false);
  });

  it.each(['project_id', 'timeline_id', 'revision_id', 'content_digest'])(
    'refuses an immutable read with a mismatched %s instead of inferring history facts', async (field) => {
      const { list } = setup([page()], (parent) => { parent[field] = 'wrong'; });
      await expect(list()).rejects.toThrow();
    },
  );

  it('refuses cursor loops even when intermediate pages are empty', async () => {
    const { list, calls } = setup([
      { ...page(), next_cursor: 'a' },
      { items: [], head, next_cursor: 'b' },
      { items: [], head, next_cursor: 'a' },
    ]);
    await expect(list()).rejects.toThrow('repeated history cursor');
    expect(calls.filter((call) => call.path.includes('/commits?'))).toHaveLength(3);
  });

  it.each(['revision_id', 'publication_id'])('refuses pagination when head %s changes', async (field) => {
    const { list } = setup([
      { ...page(), next_cursor: 'next' },
      { items: [], head: { ...head, [field]: 'changed-head' }, next_cursor: null },
    ]);
    await expect(list()).rejects.toThrow('head changed during pagination');
  });
});
