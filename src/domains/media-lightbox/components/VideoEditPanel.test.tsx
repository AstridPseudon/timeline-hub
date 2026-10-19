// @vitest-environment jsdom

import { render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  videoEdit: { videoEditSubMode: null as string | null },
  portionEditor: vi.fn((_props: unknown) => <div data-testid="portion-editor" />),
}));

vi.mock('../contexts/LightboxStateContext', () => ({
  useLightboxCoreSafe: () => ({ onClose: vi.fn() }),
  useLightboxVariantsSafe: () => ({
    variants: [],
    activeVariant: null,
    handleVariantSelect: vi.fn(),
    handleMakePrimary: vi.fn(),
    isLoadingVariants: false,
    onLoadVariantSettings: vi.fn(),
    handleDeleteVariant: vi.fn(),
  }),
}));

vi.mock('../contexts/VideoEditContext', () => ({
  useVideoEditSafe: () => ({
    videoEditSubMode: mocks.videoEdit.videoEditSubMode,
    handleEnterVideoReplaceMode: vi.fn(),
    handleEnterVideoRegenerateMode: vi.fn(),
    handleEnterVideoEnhanceMode: vi.fn(),
    handleExitVideoEditMode: vi.fn(),
  }),
}));

vi.mock('./EditPanelLayout', () => ({
  EditPanelLayout: ({ modeSelector, children }: { modeSelector: React.ReactNode; children: React.ReactNode }) => (
    <div>
      {modeSelector}
      {children}
    </div>
  ),
}));

vi.mock('./ModeSelector', () => ({
  ModeSelector: ({ items, activeId }: { items: Array<{ id: string; label: string }>; activeId: string }) => (
    <div data-testid="mode-selector" data-active={activeId}>
      {items.map((item) => <button key={item.id} type="button">{item.label}</button>)}
    </div>
  ),
}));

vi.mock('@/shared/components/VideoPortionEditor', () => ({
  VideoPortionEditor: (props: unknown) => mocks.portionEditor(props),
}));

vi.mock('./SegmentRegenerateForm', () => ({ SegmentRegenerateForm: () => null }));
vi.mock('./VideoEnhanceForm', () => ({ VideoEnhanceForm: () => <div data-testid="enhance-form" /> }));

import { VideoEditPanel } from './VideoEditPanel';

const videoEditing = {
  editSettings: {
    settings: {
      gapFrameCount: 12,
      contextFrameCount: 8,
      negativePrompt: '',
      enhancePrompt: false,
      motionMode: 'basic',
    },
    updateField: vi.fn(),
    updateFields: vi.fn(),
  },
  maxContextFrames: 20,
  selections: [],
  handleUpdateSelectionSettings: vi.fn(),
  handleAddSelection: vi.fn(),
  handleRemoveSelection: vi.fn(),
  loraManager: {},
  handleGenerate: vi.fn(),
  isGenerating: false,
  generateSuccess: false,
  isValid: true,
  validationErrors: [],
};

function renderPanel(props: { isCloudMode?: boolean; regenerate?: boolean } = {}) {
  return render(
    <VideoEditPanel
      variant="desktop"
      isCloudMode={props.isCloudMode ?? true}
      videoUrl="https://cdn.example/video.mp4"
      replace={{ videoEditing: videoEditing as never, projectId: 'project-1' }}
      regenerateFormProps={props.regenerate ? ({} as never) : null}
      enhance={{
        settings: {} as never,
        onUpdateSetting: vi.fn(),
        onGenerate: vi.fn(),
      }}
    />,
  );
}

describe('VideoEditPanel', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.videoEdit.videoEditSubMode = null;
  });

  it('offers Replace and Enhance (and Regenerate when available) but no Trim', () => {
    renderPanel({ regenerate: true });

    const labels = screen.getAllByRole('button').map((button) => button.textContent);
    expect(labels).toEqual(['Replace', 'Regenerate', 'Enhance']);
    expect(screen.queryByText('Trim')).toBeNull();
    expect(screen.getByTestId('mode-selector').dataset.active).toBe('replace');
  });

  it('shows the replace editor for the replace sub-mode with the source video url', () => {
    mocks.videoEdit.videoEditSubMode = 'replace';

    renderPanel();

    expect(screen.getByTestId('portion-editor')).toBeTruthy();
    expect(mocks.portionEditor).toHaveBeenCalledWith(expect.objectContaining({
      selections: expect.objectContaining({ videoUrl: 'https://cdn.example/video.mp4' }),
    }));
  });

  it('shows the enhance form for the enhance sub-mode', () => {
    mocks.videoEdit.videoEditSubMode = 'enhance';

    renderPanel();

    expect(screen.getByTestId('enhance-form')).toBeTruthy();
    expect(screen.queryByTestId('portion-editor')).toBeNull();
  });
});
