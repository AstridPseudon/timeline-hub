import { test } from 'bun:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { ProjectChatRegistry } from './astrid-project-chat.ts';
import { ApiError, type Project } from './runtime-client.ts';

function registryFor(project: Project) {
  const claimDirectory = mkdtempSync(join(tmpdir(), 'project-chat-test-'));
  const registry = new ProjectChatRegistry({
    getProject: async () => structuredClone(project),
    listProjects: async () => ({ items: [structuredClone(project)], next_cursor: null }),
    updateProject: async (_id, _key, version, _name, metadata) => {
      assert.equal(version, project.version);
      project = { ...project, version: version + 1, metadata: metadata! };
      return structuredClone(project);
    },
  }, 'test', Date.now, claimDirectory);
  return { registry, cleanup: () => rmSync(claimDirectory, { recursive: true, force: true }) };
}

test('New selects the created chat without changing the project Main chat', async () => {
  const project: Project = {
    project_id: 'p', realm_id: 'r', slug: 'p', name: 'p', version: 1,
    created_at: '', updated_at: '', metadata: {
      astrid_agent_chat_v1: { test: {
        revision: 4, selected_session_id: 'old', main_session_id: 'main',
        sessions: [{ id: 'main' }, { id: 'old' }], draft: { text: '', revision: 0, queued_messages: [] },
      } },
    },
  };
  const { registry, cleanup } = registryFor(project);
  try {
    const result = await registry.create('p', 'new', 'new-operation', async () => ({ sessionId: 'new-session' }));
    assert.equal(result.selected_session_id, 'new-session');
    assert.equal(result.main_session_id, 'main');
    assert.deepEqual(result.sessions.map(session => session.id), ['main', 'old', 'new-session']);
  } finally {
    cleanup();
  }
});

test('New does not assign Main when the project has no Main chat', async () => {
  const project: Project = { project_id: 'p', realm_id: 'r', slug: 'p', name: 'p', metadata: {}, version: 1, created_at: '', updated_at: '' };
  const { registry, cleanup } = registryFor(project);
  try {
    const result = await registry.create('p', 'new', 'new-operation', async () => ({ sessionId: 'new-session' }));
    assert.equal(result.selected_session_id, 'new-session');
    assert.equal(result.main_session_id, null);
  } finally {
    cleanup();
  }
});

test('ensure replaces an empty selected session in its existing chat entry when its transcript is missing', async () => {
  const project: Project = {
    project_id: 'p', realm_id: 'r', slug: 'p', name: 'p', version: 1,
    created_at: '', updated_at: '', metadata: {
      astrid_agent_chat_v1: { test: {
        revision: 4, selected_session_id: 'empty', main_session_id: 'empty',
        sessions: [{ id: 'older' }, { id: 'empty', title: 'Empty Claude chat', pending_first_message: true }, { id: 'newer' }],
        draft: { text: '', revision: 0, queued_messages: [] },
      } },
    },
  };
  const { registry, cleanup } = registryFor(project);
  try {
    let creates = 0;
    const result = await registry.create('p', 'ensure', 'reload-empty', async () => {
      creates++;
      return { sessionId: 'claude-code:fresh' };
    }, async () => false);
    assert.equal(creates, 1);
    assert.equal(result.operation_session_id, 'claude-code:fresh');
    assert.equal(result.selected_session_id, 'claude-code:fresh');
    assert.equal(result.main_session_id, 'claude-code:fresh');
    assert.deepEqual(result.sessions, [
      { id: 'older' },
      { id: 'claude-code:fresh', title: 'Empty Claude chat', pending_first_message: true },
      { id: 'newer' },
    ]);
  } finally {
    cleanup();
  }
});

test('targeted reload reuses an empty chat when its ACP session still resumes', async () => {
  const project: Project = {
    project_id: 'p', realm_id: 'r', slug: 'p', name: 'p', version: 1,
    created_at: '', updated_at: '', metadata: {
      astrid_agent_chat_v1: { test: {
        revision: 1, selected_session_id: 'codex:empty', main_session_id: 'other',
        sessions: [{ id: 'codex:empty', pending_first_message: true }, { id: 'other' }],
        draft: { text: '', revision: 0, queued_messages: [] },
      } },
    },
  };
  const { registry, cleanup } = registryFor(project);
  try {
    let creates = 0;
    const result = await registry.create('p', 'ensure', 'reload-still-live', async () => {
      creates++;
      return { sessionId: 'codex:unexpected' };
    }, async id => id === 'codex:empty', 'codex:empty');
    assert.equal(creates, 0);
    assert.equal(result.operation_session_id, 'codex:empty');
    assert.equal(result.selected_session_id, 'codex:empty');
    assert.equal(result.main_session_id, 'other');
    assert.deepEqual(result.sessions, [{ id: 'codex:empty', pending_first_message: true }, { id: 'other' }]);
  } finally {
    cleanup();
  }
});

test('empty marker and model metadata writes preserve the chat selection revision', async () => {
  const project: Project = {
    project_id: 'p', realm_id: 'r', slug: 'p', name: 'p', version: 1,
    created_at: '', updated_at: '', metadata: {
      astrid_agent_chat_v1: { test: {
        revision: 7, selected_session_id: 'codex:empty', main_session_id: null,
        sessions: [{ id: 'codex:empty', pending_first_message: true, model_id: 'alpha' }],
        draft: { text: '', revision: 0, queued_messages: [] },
      } },
    },
  };
  const { registry, cleanup } = registryFor(project);
  try {
    await registry.markSessionStarted('p', 'codex:empty');
    await registry.setSessionModel('p', 'codex:empty', 'beta');
    const result = await registry.get('p');
    assert.equal(result.revision, 7);
    assert.deepEqual(result.sessions, [{ id: 'codex:empty', pending_first_message: false, model_id: 'beta' }]);
  } finally {
    cleanup();
  }
});

test('identical draft retries acknowledge without writes while divergent stale payloads retain CAS protection', async () => {
  let project: Project = { project_id: 'p', realm_id: 'r', slug: 'p', name: 'p', metadata: {}, version: 1, created_at: '', updated_at: '' };
  let writes = 0;
  const registry = new ProjectChatRegistry({
    getProject: async () => structuredClone(project),
    listProjects: async () => ({ items: [structuredClone(project)], next_cursor: null }),
    updateProject: async (_id, _key, version, _name, metadata) => {
      assert.equal(version, project.version);
      writes++;
      project = { ...project, version: version + 1, metadata: metadata! };
      return structuredClone(project);
    },
  }, 'test');
  const queue = [{ id: 'q', text: 'queued', session_id: 's', attachments: [{ object_id: 'asset-a', variant: { id: 'v1' } }] }];
  assert.equal((await registry.draft('p', 0, '', [])).draft.revision, 0);
  assert.equal(writes, 0);
  const first = await registry.draft('p', 0, 'local', queue);
  assert.equal(first.draft.revision, 1);
  const duplicate = await registry.draft('p', 0, 'local', structuredClone(queue));
  assert.deepEqual(duplicate, first);
  assert.equal(writes, 1);
  for (const changed of [
    { text: 'other', queue },
    { text: 'local', queue: [] },
    { text: 'local', queue: [{ ...queue[0], session_id: 'other-session' }] },
    { text: 'local', queue: [{ ...queue[0], attachments: [{ object_id: 'asset-b', variant: { id: 'v1' } }] }] },
  ]) {
    await assert.rejects(registry.draft('p', 0, changed.text, changed.queue), (error: unknown) => Boolean(error && typeof error === 'object' && 'code' in error && error.code === 'draft_conflict'));
    assert.deepEqual(await registry.get('p'), first);
  }
  assert.equal(writes, 1);
});

test('parallel identical drafts survive project version retries without advancing twice', async () => {
  let project: Project = { project_id: 'p', realm_id: 'r', slug: 'p', name: 'p', metadata: {}, version: 1, created_at: '', updated_at: '' };
  let writes = 0;
  const registry = new ProjectChatRegistry({
    getProject: async () => structuredClone(project),
    listProjects: async () => ({ items: [structuredClone(project)], next_cursor: null }),
    updateProject: async (_id, _key, version, _name, metadata) => {
      if (version !== project.version) throw new ApiError(409, 'version_conflict', 'changed');
      writes++;
      project = { ...project, version: version + 1, metadata: metadata! };
      return structuredClone(project);
    },
  }, 'test');
  const [first, second] = await Promise.all([registry.draft('p', 0, 'same', []), registry.draft('p', 0, 'same', [])]);
  assert.deepEqual(first, second);
  assert.equal(writes, 1);
});
