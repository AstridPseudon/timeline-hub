// @vitest-environment jsdom

import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { ElementsLibraryPanel } from './ElementsLibraryPanel.tsx';

const harness = vi.hoisted(() => ({
  editorContext: null as unknown,
  selectedClipIds: ['source-clip'],
  execute: vi.fn(),
  invalidateQueries: vi.fn(),
  current: null as unknown,
  elementOverlay: null as unknown,
  clipScalar: null as unknown,
}));

vi.mock('@tanstack/react-query', () => ({
  useQueryClient: () => ({ invalidateQueries: harness.invalidateQueries }),
}));

vi.mock('@/shared/contexts/AgentChatContext', () => ({
  useAgentChatBridge: () => ({ editorContext: harness.editorContext }),
}));

vi.mock('@/tools/video-editor/hooks/timelineStore', () => ({
  useTimelineEditorData: () => ({ selectedClipIds: harness.selectedClipIds }),
  useTimelineEditorDataSafe: () => ({ data: harness.current }),
  useTimelineEditorOpsSafe: () => ({ clipScalar: harness.clipScalar }),
  useTimelineChromeContextSafe: () => ({ commandSession: { elementOverlay: harness.elementOverlay } }),
}));

const elementEntry = {
  id: 'end-spanning-layer',
  packId: 'local',
  label: 'Ending Spanning Layer',
  kind: 'effect' as const,
  placement: 'overlay' as const,
  revision: 'sha256:a91d9377',
  capabilities: {
    browserPreview: 'supported' as const,
    astridExport: 'supported' as const,
    workerExport: 'supported' as const,
  },
  publication: 'published' as const,
};

const transitionEntry = {
  ...elementEntry,
  id: 'crossfade',
  packId: 'rendering',
  label: 'Crossfade',
  kind: 'transition' as const,
  placement: 'between-clips' as const,
};

function renderPanel(catalog: readonly unknown[], selectedClipIds = ['source-clip']) {
  harness.selectedClipIds = selectedClipIds;
  harness.editorContext = {
    projectSlug: 'pack-coherence-browser-proof',
    timelineId: 'main',
    timelineSummary: { configVersion: 7, trackCount: 2, clipCount: 1, assetCount: 1, duration: 2 },
    elementContext: { catalog },
    elementOperationAdapter: { execute: harness.execute },
  };
  render(
    <ElementsLibraryPanel
      open
      onOpenChange={vi.fn()}
      onOpenCreationPrompt={vi.fn()}
    />,
  );
}

describe('ElementsLibraryPanel owner-pinned operations', () => {
  beforeEach(() => {
    harness.execute.mockReset().mockResolvedValue({ config_version: 8 });
    harness.invalidateQueries.mockReset();
    harness.current = null;
    harness.elementOverlay = null;
    harness.clipScalar = null;
  });

  it('persists the owning pack on an applied element reference', async () => {
    renderPanel([elementEntry]);

    fireEvent.click(screen.getByRole('button', { name: 'Apply' }));

    await waitFor(() => expect(harness.execute).toHaveBeenCalledWith(expect.objectContaining({
      name: 'timeline.apply_element',
      element: {
        id: 'end-spanning-layer',
        kind: 'effect',
        revision: 'sha256:a91d9377',
        packId: 'local',
      },
    })));
  });

  it('captures an applied transition as one native clip.set with its exact selected ref', async () => {
    harness.current = {
      resolvedConfig: {
        output: { fps: 30 },
        clips: [
          { id: 'source-clip', at: 0, hold: 2, track: 'V1' },
          { id: 'next-clip', at: 2, hold: 2, track: 'V1' },
        ],
      },
    };
    const basis = { select: 'parent/clip:next-clip' };
    const finish = vi.fn((_captured: unknown, args: unknown) => ({ command: {
      schema_version: 1, op: 'clip.set', version: '1', select: basis.select, args, intent: {},
    } }));
    harness.clipScalar = {
      capture: vi.fn().mockReturnValue(basis), finish, submit: vi.fn(),
    };
    renderPanel([transitionEntry], ['source-clip', 'next-clip']);

    fireEvent.click(screen.getByRole('button', { name: 'Apply' }));

    await waitFor(() => expect(harness.clipScalar.capture).toHaveBeenCalledWith(expect.objectContaining({
      clipId: 'next-clip', current: harness.current,
    })));
    expect(finish).toHaveBeenCalledWith(basis, {
      values: {
        transition: { type: 'crossfade', duration: 8 / 30, revision: 'sha256:a91d9377' },
        elementRef: { id: 'crossfade', kind: 'transition', revision: 'sha256:a91d9377', packId: 'rendering' },
      },
      clear: [],
    });
    expect(harness.clipScalar.submit).toHaveBeenCalled();
    expect(harness.execute).not.toHaveBeenCalled();
  });

  it('refuses hosted project-pack transitions while their retained binding is absent', async () => {
    renderPanel([{ ...transitionEntry, packId: 'local' }], ['source-clip', 'next-clip']);

    fireEvent.click(screen.getByRole('button', { name: 'Apply' }));

    await waitFor(() => expect(screen.getByText('Hosted transition binding is unavailable for this project pack; the draft was not changed.')).toBeInTheDocument());
    expect(harness.clipScalar).toBeNull();
    expect(harness.execute).not.toHaveBeenCalled();
  });

  it('sends an admitted literal effect through the native overlay port without the legacy adapter', async () => {
    const literal = { ...elementEntry, packId: undefined, admitted: true };
    harness.current = {
      configVersion: 7,
      head: { projectId: 'project', timelineId: 'main', headRevisionId: 'r1', headPublicationId: 'p1' },
      resolvedConfig: {
        clips: [{ id: 'source-clip', at: 0, hold: 2, track: 'V1', clipType: 'hold' }],
        tracks: [{ id: 'V1', kind: 'visual' }],
      },
    };
    const captured = { operation: { kind: 'create' as const, row: {} }, bundle: {}, commands: [], head: {}, localGeneration: 0, localBasis: {}, previewVersion: 7 };
    harness.elementOverlay = {
      capture: vi.fn().mockReturnValue(captured),
      finish: vi.fn().mockReturnValue({ commands: [], preview: { version: 7, operations: [] } }),
      submit: vi.fn(),
    };
    renderPanel([literal]);

    fireEvent.click(screen.getByRole('button', { name: 'Apply' }));

    await waitFor(() => expect(harness.elementOverlay.capture).toHaveBeenCalledWith(expect.objectContaining({
      operation: expect.objectContaining({
        kind: 'create',
        row: expect.objectContaining({ id: 'element-end-spanning-layer-0', clipType: 'end-spanning-layer', track: 'V1', hold: 2 }),
      }),
    })));
    expect(harness.execute).not.toHaveBeenCalled();
  });
});
