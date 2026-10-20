import { describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { createCommitOutbox } from '../../src/tools/video-editor/commands/commitOutbox.ts';

describe('audit of current pre-H0 persistence port', () => {
  it('can persist an owner and reserved ID, but has no legal pre-create request reservation', async () => {
    const scope = { realmId: 'realm', actorId: 'actor', projectId: 'project', timelineId: 'reserved-before-create' };
    const factory = createFakeIndexedDB();
    const open = () => createCommitOutbox({ indexedDB: factory, exclusiveLock: async (_name, work) => work() });
    const transmit = vi.fn();
    let owner = '';
    await open().create(scope, async (box, id) => {
      owner = id;
      expect(box).not.toHaveProperty('reserveCreate');
      await expect(box.append({ createBody: { timeline_id: scope.timelineId }, createKey: 'original' }, { after: 'missing' }))
        .rejects.toThrow('Dependent intent must follow');
      await expect(box.dispatch(() => ({ method: 'POST', path: '/v1/projects/project/timelines', body: { timeline_id: scope.timelineId } }), transmit))
        .rejects.toThrow('Outbox is empty');
    });
    await open().recover(scope, owner, async (box) => {
      const record = await box.read();
      expect(record.scope.timelineId).toBe(scope.timelineId);
      expect(record.intents).toEqual([]);
      expect(record.pending).toBeUndefined();
    });
    expect(transmit).not.toHaveBeenCalled();
  });
});
