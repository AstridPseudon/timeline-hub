// @vitest-environment jsdom

import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import type { TimelineEditability } from '@/tools/video-editor/lib/timeline-editability.ts';
import type { AstridElementDescriptor } from '@/tools/video-editor/runtime/astrid-element-host.ts';
import type { ResolvedTimelineClip, ResolvedTimelineConfig } from '@/tools/video-editor/types/index.ts';
import type { ElementCapturePort } from '@/tools/video-editor/commands/elementGesture.ts';
import { AstridElementParams } from './AstridElementParams.tsx';
import type { ClipPanelProps } from './ClipPanelBody.tsx';
import { resolveAstridElementParamDescriptor } from './astrid-element-param-descriptor.ts';

const runtimeState = vi.hoisted(() => ({
  descriptors: [] as AstridElementDescriptor[],
  timelineEditability: undefined as TimelineEditability | undefined,
}));
const editorState = vi.hoisted(() => ({
  data: null as unknown,
  element: undefined as ElementCapturePort | undefined,
  selectedParam: undefined as any,
}));

vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', () => ({
  useVideoEditorRuntime: () => ({
    astridElementHost: { descriptors: runtimeState.descriptors },
    timelineEditability: runtimeState.timelineEditability,
  }),
}));

vi.mock('@/tools/video-editor/hooks/timelineStore.ts', () => ({
  useTimelineEditorDataSafe: () => editorState.data,
  useTimelineEditorOpsSafe: () => editorState.element || editorState.selectedParam
    ? { element: editorState.element, selectedParam: editorState.selectedParam } : null,
}));

const descriptor: AstridElementDescriptor = {
  id: 'v3-glow',
  kind: 'effect',
  packId: 'astrid-v3',
  revision: 'rev-7',
  componentPath: 'packs/v3/glow',
  schema: {
    title: 'Glow',
    properties: {
      selectedSegmentIndex: { type: 'number', title: 'Selected Segment Index' },
    },
  },
};

function clipFor(
  reference: Pick<AstridElementDescriptor, 'id' | 'kind' | 'packId' | 'revision'>,
  params: Record<string, unknown> = {},
): ResolvedTimelineClip {
  return {
    id: 'clip-v3-glow',
    at: 0,
    track: 'V1',
    hold: 2,
    clipType: 'effect-layer',
    elementRef: reference,
    params,
  } as unknown as ResolvedTimelineClip;
}

function renderForm({
  reference = descriptor,
  params = {},
  readOnly = false,
  onChange = vi.fn(),
}: {
  reference?: Pick<AstridElementDescriptor, 'id' | 'kind' | 'packId' | 'revision'>;
  params?: Record<string, unknown>;
  readOnly?: boolean;
  onChange?: ClipPanelProps['onChange'];
} = {}) {
  runtimeState.descriptors = [reference.packId === undefined ? { ...descriptor, packId: undefined } : descriptor];
  return {
    ...render(
      <AstridElementParams
        clip={clipFor(reference, params)}
        readOnly={readOnly}
        registry={{} as ResolvedTimelineConfig['registry']}
        onChange={onChange}
      />,
    ),
    onChange,
  };
}

describe('AstridElementParams', () => {
  it('matches the exact host owner and pinned revision', () => {
    const clip = clipFor(descriptor);
    expect(resolveAstridElementParamDescriptor(clip, [descriptor], false, undefined)).toBe(descriptor);
    expect(resolveAstridElementParamDescriptor(
      clipFor({ ...descriptor, packId: 'other-owner' }),
      [descriptor],
      false,
      undefined,
    )).toBeUndefined();
    expect(resolveAstridElementParamDescriptor(
      clipFor({ ...descriptor, revision: 'stale-revision' }),
      [descriptor],
      false,
      undefined,
    )).toBeUndefined();

    renderForm();
    expect(screen.getByTestId('astrid-element-params')).toBeTruthy();
  });

  it('preserves existing params and writes through the selected native producer', async () => {
    const command = {
      schema_version: 1, op: 'clip.set-params', version: '1', select: 'parent/clip:clip-v3-glow',
      args: { values: { selectedSegmentIndex: 1, futureParam: 'keep-me' }, clear: [],
        schema_source: { document_id: 'pack', version: 1, content_digest: `sha256:${'a'.repeat(64)}` } },
    };
    const port = {
      resolveAuthority: vi.fn(() => command.args.schema_source),
      capture: vi.fn(() => ({ select: command.select, localGeneration: 0 })),
      prefetch: vi.fn(async () => undefined),
      finish: vi.fn(() => ({ command, previewParams: null })),
      submit: vi.fn(),
    };
    editorState.data = { data: { resolvedConfig: { clips: [clipFor(descriptor)] } } };
    editorState.selectedParam = port;
    const { onChange } = renderForm({ params: { selectedSegmentIndex: 2, futureParam: 'keep-me' } });
    fireEvent.change(screen.getByLabelText('Selected Segment Index'), { target: { value: '1' } });
    await waitFor(() => expect(port.submit).toHaveBeenCalledTimes(1));
    expect(onChange).not.toHaveBeenCalled();
  });

  it('refuses selected-pack edits when the native carrier is unavailable', () => {
    const capture = vi.fn(() => { throw new Error('selected-pack native capture must not run'); });
    editorState.data = { data: {} };
    editorState.selectedParam = undefined;
    editorState.element = { capture, finish: vi.fn(), submit: vi.fn() } as unknown as ElementCapturePort;
    const { onChange } = renderForm({ params: { selectedSegmentIndex: 2 } });

    fireEvent.change(screen.getByLabelText('Selected Segment Index'), { target: { value: '1' } });

    expect(capture).not.toHaveBeenCalled();
    expect(onChange).not.toHaveBeenCalled();
    expect(screen.getByTestId('astrid-selected-param-error')).toHaveTextContent(
      'Selected PARAM schema carrier is unavailable; Agent retained-read support is required',
    );
  });

  it('routes a literal existing-clip edit through the mounted native port without legacy onChange', () => {
    const literal = { ...descriptor, packId: undefined };
    const edit = { params: { values: { selectedSegmentIndex: 1 }, clear: [] } };
    const command = {
      schema_version: 1, op: 'clip.set-params', version: '1', select: 'parent/clip:clip-v3-glow',
      args: edit.params,
    };
    const preview = {
      version: 1, source: 'timeline.native-existing-element',
      operations: [{ op: 'clip.update', target: 'clip-v3-glow', payload: { params: { selectedSegmentIndex: 1 } } }],
    };
    const capture = vi.fn(() => ({
      clipId: 'clip-v3-glow', select: command.select, edit, capture: {}, before: {},
      localGeneration: 0, localBasis: {}, previewVersion: 1,
    }));
    const finish = vi.fn(() => ({ command, preview }));
    const submit = vi.fn();
    editorState.data = { data: {} };
    editorState.element = { capture, finish, submit } as unknown as ElementCapturePort;
    const onChange = vi.fn();
    renderForm({ reference: literal, onChange });

    fireEvent.change(screen.getByLabelText('Selected Segment Index'), { target: { value: '1' } });

    expect(capture).toHaveBeenCalledTimes(1);
    expect(submit).toHaveBeenCalledTimes(1);
    expect(onChange).not.toHaveBeenCalled();
  });

  it('does not expose the form for read-only timelines or stale host registrations', () => {
    const readOnly = renderForm({ readOnly: true });
    expect(screen.queryByTestId('astrid-element-params')).toBeNull();
    readOnly.unmount();

    const stale = renderForm({ reference: { ...descriptor, revision: 'stale-revision' } });
    expect(screen.queryByTestId('astrid-element-params')).toBeNull();
    stale.unmount();
  });

  it('uses distinct field ids for two form instances', () => {
    runtimeState.descriptors = [descriptor];
    render(
      <>
        <AstridElementParams
          clip={clipFor(descriptor)}
          registry={{} as ResolvedTimelineConfig['registry']}
          onChange={() => undefined}
        />
        <AstridElementParams
          clip={clipFor(descriptor)}
          registry={{} as ResolvedTimelineConfig['registry']}
          onChange={() => undefined}
        />
      </>,
    );
    const fields = screen.getAllByLabelText('Selected Segment Index');
    expect(fields).toHaveLength(2);
    expect(fields[0].id).not.toBe(fields[1].id);
  });
});
