import { act, renderHook } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { useProjectCRUD } from '../useProjectCRUD';

const mocks = vi.hoisted(() => ({
  workspaceV1: false,
  clientOptions: [] as unknown[],
  createProject: vi.fn(),
}));

vi.mock('@/integrations/astrid/workspaceV1', () => ({
  get isAstridWorkspaceV1() { return mocks.workspaceV1; },
}));

vi.mock('@/integrations/astrid/client', () => ({
  AstridLocalClient: class MockAstridLocalClient {
    projects = { create: mocks.createProject };

    constructor(options: unknown) {
      mocks.clientOptions.push(options);
    }
  },
}));

describe('useProjectCRUD local workspace project creation', () => {
  beforeEach(() => {
    mocks.workspaceV1 = true;
    mocks.clientOptions = [];
    mocks.createProject.mockReset().mockResolvedValue({
      data: {
        slug: 'reigh-local-launch-smoke-2026-10-14',
        name: 'Reigh local launch smoke 2026-10-14',
        metadata: { aspect_ratio: '16:9' },
        created_at: '2026-10-14T00:00:00.000Z',
      },
    });
    window.history.replaceState({}, '', '/tools/video-editor');
  });

  it('creates through workspace.v1 before a project is selected or present in the URL', async () => {
    const onProjectsLoaded = vi.fn();
    const onProjectCreated = vi.fn();
    const { result } = renderHook(() => useProjectCRUD({
      userId: 'local-user',
      selectedProjectId: null,
      onProjectsLoaded,
      onProjectCreated,
      onProjectDeleted: vi.fn(),
      updateUserSettings: vi.fn(async () => undefined),
    }));

    let createdProject;
    await act(async () => {
      createdProject = await result.current.addNewProject({
        name: 'Reigh local launch smoke 2026-10-14',
        aspectRatio: '16:9',
      });
    });

    expect(mocks.clientOptions).toEqual([{ projectSlug: '__discovery__' }]);
    expect(mocks.createProject).toHaveBeenCalledWith({
      name: 'Reigh local launch smoke 2026-10-14',
      slug: 'reigh-local-launch-smoke-2026-10-14',
      metadata: { aspect_ratio: '16:9' },
    });
    expect(createdProject).toMatchObject({
      id: 'reigh-local-launch-smoke-2026-10-14',
      name: 'Reigh local launch smoke 2026-10-14',
      user_id: 'local-user',
      aspectRatio: '16:9',
    });
    expect(onProjectCreated).toHaveBeenCalledWith(createdProject);
    expect(onProjectsLoaded).not.toHaveBeenCalled();
  });
});
