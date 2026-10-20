// @vitest-environment jsdom

import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import type { TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { ClipParamsCapturePort } from '@/tools/video-editor/commands/clipParamsGesture.ts';
import type { ClipParamsArgs } from '@/tools/video-editor/commands/clipParamsCapture.ts';
import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { AvailableSequenceMetadata } from '@/tools/video-editor/sequences/registry.ts';
import type { ResolvedTimelineConfig } from '@/tools/video-editor/types/index.ts';
import { SequenceParamEditor } from './SequenceParamEditor.tsx';

const metadata = (params: AvailableSequenceMetadata['params']): AvailableSequenceMetadata => ({
  clipType: 'legacy-sequence',
  themeId: 'test-theme',
  label: 'Legacy Sequence',
  description: 'Legacy sequence fields.',
  whenToUse: 'Legacy test fixture.',
  hold: { defaultSeconds: 2, minSeconds: 1, maxSeconds: 4, stepSeconds: 1 },
  params,
});

const props = {
  clipType: 'unregistered-test-sequence',
  params: {},
  registry: {} as ResolvedTimelineConfig['registry'],
  onChange: () => undefined,
};

describe('SequenceParamEditor empty state', () => {
  it('keeps the warning when no Astrid form owns the empty state', () => {
    render(<SequenceParamEditor {...props} metadata={metadata([])} />);
    expect(screen.getByText('This clip type does not expose editable sequence params in the current registry view.')).toBeTruthy();
  });

  it('hides only the empty warning when an active Astrid form owns it', () => {
    const { container } = render(<SequenceParamEditor {...props} metadata={metadata([])} hideEmptyState />);
    expect(container.textContent).toBe('');
  });

  it('keeps nonempty legacy controls when the Astrid form is also active', () => {
    render(
      <SequenceParamEditor
        {...props}
        metadata={metadata([{
          key: 'legacyTitle',
          label: 'Legacy title',
          kind: 'string',
          description: 'A legacy parameter.',
          defaultValue: 'Keep me',
        }])}
        hideEmptyState
      />,
    );
    expect(screen.getByText('Legacy Sequence')).toBeTruthy();
    expect(screen.getByText('Legacy title')).toBeTruthy();
    expect(screen.queryByText('This clip type does not expose editable sequence params in the current registry view.')).toBeNull();
  });
});

const nativeCurrent = {
  resolvedConfig: { clips: [{ id: 'clip-1' }] },
} as unknown as TimelineData;

function nativePort() {
  return {
    capture: vi.fn(() => ({ select: 'parent/clip:clip-1' })),
    finish: vi.fn((_basis: unknown, args: ClipParamsArgs) => ({
      command: {
        schema_version: 1,
        op: 'clip.set-params',
        version: '1',
        select: 'parent/clip:clip-1',
        args,
      } as unknown as EditCommand,
      previewParams: args.clear.length ? {} : args.values,
    })),
    submit: vi.fn(),
  } as unknown as ClipParamsCapturePort;
}

describe('SequenceParamEditor discrete native params controls', () => {
  it('submits an asset-array leaf through the native port without whole-params onChange', () => {
    const port = nativePort();
    const onChange = vi.fn();
    render(
      <SequenceParamEditor
        clipType="unregistered-test-sequence"
        metadata={metadata([{ key: 'assets', label: 'Assets', kind: 'asset-list', description: 'Assets.' }])}
        params={{ assets: [] }}
        registry={{ 'asset-a': {} } as ResolvedTimelineConfig['registry']}
        current={nativeCurrent}
        clipId="clip-1"
        clipParamsPort={port}
        onChange={onChange}
      />,
    );

    fireEvent.change(screen.getByPlaceholderText('asset-key-a, asset-key-b'), { target: { value: 'asset-a' } });

    expect(port.capture).toHaveBeenCalledWith({ clipId: 'clip-1', current: nativeCurrent });
    expect(port.finish).toHaveBeenCalledWith({ select: 'parent/clip:clip-1' }, {
      values: { assets: ['asset-a'] },
      clear: [],
    });
    expect(port.submit).toHaveBeenCalledTimes(1);
    expect(onChange).not.toHaveBeenCalled();
  });

  it('submits an optional JSON clear through the native port', () => {
    const port = nativePort();
    const onChange = vi.fn();
    render(
      <SequenceParamEditor
        clipType="unregistered-test-sequence"
        metadata={metadata([{ key: 'keyframes', label: 'Keyframes', kind: 'json', description: 'Frames.' }])}
        params={{ keyframes: [{ at: 0 }] }}
        registry={{}}
        current={nativeCurrent}
        clipId="clip-1"
        clipParamsPort={port}
        onChange={onChange}
      />,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Clear' }));

    expect(port.finish).toHaveBeenCalledWith({ select: 'parent/clip:clip-1' }, { values: {}, clear: ['keyframes'] });
    expect(port.submit).toHaveBeenCalledTimes(1);
    expect(onChange).not.toHaveBeenCalled();
  });

  it('keeps the detached presentation callback when no native editor context is supplied', () => {
    const onChange = vi.fn();
    render(
      <SequenceParamEditor
        clipType="unregistered-test-sequence"
        metadata={metadata([{ key: 'assets', label: 'Assets', kind: 'asset-list', description: 'Assets.' }])}
        params={{ assets: [] }}
        registry={{ 'asset-a': {} } as ResolvedTimelineConfig['registry']}
        onChange={onChange}
      />,
    );

    fireEvent.change(screen.getByPlaceholderText('asset-key-a, asset-key-b'), { target: { value: 'asset-a' } });
    expect(onChange).toHaveBeenCalledWith({ assets: ['asset-a'] });
  });

  it('disables discrete controls when mounted context has no native port', () => {
    render(
      <SequenceParamEditor
        clipType="unregistered-test-sequence"
        metadata={metadata([
          { key: 'assets', label: 'Assets', kind: 'asset-list', description: 'Assets.' },
          { key: 'keyframes', label: 'Keyframes', kind: 'json', description: 'Frames.' },
        ])}
        params={{ assets: [], keyframes: [{ at: 0 }] }}
        registry={{ 'asset-a': {} } as ResolvedTimelineConfig['registry']}
        current={nativeCurrent}
        clipId="clip-1"
        onChange={vi.fn()}
      />,
    );

    expect(screen.getByPlaceholderText('asset-key-a, asset-key-b')).toBeDisabled();
    expect(screen.getByRole('button', { name: 'Clear' })).toBeDisabled();
    expect(screen.getByText(/Native clip parameter editing is unavailable/)).toBeInTheDocument();
  });
});
