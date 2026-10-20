import { useState } from 'react';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { PanelRenderProps } from '@astrid/editor-sdk';
import { ExtensionPanelHost, placePanelNode } from './ExtensionPanelHost';
import type { VideoEditorPanelDescriptor } from './extensionSurface';

vi.mock('@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx', () => ({
  useOptionalVideoEditorRuntime: () => null,
}));

const EXT = 'com.test.popout';
const transcriptKey = `${EXT}:transcript`;
const beatKey = `${EXT}:beat`;

/** Latest props each panel rendered with, keyed by panel id. */
const seen = new Map<string, PanelRenderProps>();
const attached: Node[] = [];

beforeEach(() => {
  seen.clear();
});

afterEach(() => {
  cleanup();
  for (const node of attached.splice(0)) node.parentNode?.removeChild(node);
});

function CounterPanel({ id, label, instanceId }: { id: string; label: string; instanceId: string }) {
  const [count, setCount] = useState(0);
  return (
    <div>
      <button type="button" aria-label={`${label} counter`} onClick={() => setCount((value) => value + 1)}>{count}</button>
      <span data-testid={`instance-${id}`}>{instanceId}</span>
    </div>
  );
}

function makePanel(id: string, label: string): VideoEditorPanelDescriptor {
  return {
    id,
    extensionId: EXT,
    label,
    placement: 'asset-panel',
    render: (props) => {
      seen.set(id, props);
      return <CounterPanel id={id} label={label} instanceId={props.instanceId} />;
    },
  };
}

/** Owns the popped key the way the dock does, so pop-out and bring-back run through real state. */
function Host({ panels, visible }: { panels: readonly VideoEditorPanelDescriptor[]; visible: ReadonlySet<string> }) {
  const [popped, setPopped] = useState<string | null>(null);
  return (
    <ExtensionPanelHost
      panels={panels}
      visiblePanelKeys={visible}
      poppedPanelKey={popped}
      onPoppedPanelKeyChange={setPopped}
    />
  );
}

const transcript = () => makePanel('transcript', 'Transcript');
const beat = () => makePanel('beat', 'Beat Cue');

function nodeOf(buttonName: string): HTMLElement {
  const node = screen.getByRole('button', { name: buttonName }).closest<HTMLElement>('[data-panel-node]');
  if (!node) throw new Error(`no panel node around ${buttonName}`);
  return node;
}

function popOut(id: string) {
  act(() => seen.get(id)!.popout!.onOpenChange(true));
}

describe('ExtensionPanelHost pop-out', () => {
  it('keeps state, instanceId and the DOM node identical across pop-out and bring-back', () => {
    render(<Host panels={[transcript()]} visible={new Set([transcriptKey])} />);
    const button = screen.getByRole('button', { name: 'Transcript counter' });
    fireEvent.click(button);
    fireEvent.click(button);
    expect(button).toHaveTextContent('2');
    const instanceId = seen.get('transcript')!.instanceId;
    const node = nodeOf('Transcript counter');
    expect(node.closest('[role="dialog"]')).toBeNull();

    popOut('transcript');
    const dialog = screen.getByRole('dialog');
    expect(dialog).toContainElement(node);
    expect(nodeOf('Transcript counter')).toBe(node);
    expect(screen.getByRole('button', { name: 'Transcript counter' })).toBe(button);
    expect(button).toHaveTextContent('2');
    expect(screen.getByTestId('instance-transcript')).toHaveTextContent(instanceId);
    expect(seen.get('transcript')!.instanceId).toBe(instanceId);

    fireEvent.click(screen.getByRole('button', { name: 'Bring back' }));
    expect(screen.queryByRole('dialog')).toBeNull();
    expect(nodeOf('Transcript counter')).toBe(node);
    expect(node.closest('[data-panel-key]')).toHaveAttribute('data-panel-key', transcriptKey);
    expect(screen.getByRole('button', { name: 'Transcript counter' })).toBe(button);
    expect(button).toHaveTextContent('2');
    expect(screen.getByTestId('instance-transcript')).toHaveTextContent(instanceId);
  });

  it('shows a docked placeholder while popped and reports visible even when not docked', () => {
    render(<Host panels={[transcript()]} visible={new Set()} />);
    expect(seen.get('transcript')!.visible).toBe(false);

    popOut('transcript');
    expect(screen.getByTestId('panel-popped-placeholder')).toHaveTextContent('Transcript is open in a window');
    expect(seen.get('transcript')!.visible).toBe(true);

    fireEvent.click(screen.getByRole('button', { name: 'Bring back', hidden: true }));
    expect(screen.queryByTestId('panel-popped-placeholder')).toBeNull();
    expect(screen.queryByRole('dialog')).toBeNull();
    expect(seen.get('transcript')!.visible).toBe(false);
  });

  it('docks the first panel when a second panel is popped, leaving one dialog', () => {
    render(<Host panels={[transcript(), beat()]} visible={new Set([transcriptKey, beatKey])} />);
    const transcriptNode = nodeOf('Transcript counter');

    popOut('transcript');
    expect(screen.getByRole('dialog')).toContainElement(transcriptNode);

    popOut('beat');
    expect(screen.getAllByRole('dialog')).toHaveLength(1);
    const dialog = screen.getByRole('dialog');
    const beatNode = nodeOf('Beat Cue counter');
    expect(dialog).toContainElement(beatNode);
    expect(dialog).not.toContainElement(transcriptNode);
    expect(transcriptNode.closest('[data-panel-key]')).toHaveAttribute('data-panel-key', transcriptKey);
    expect(transcriptNode.closest('[data-popped]')).toBeNull();
    expect(screen.getByTestId('panel-popped-placeholder')).toHaveTextContent('Beat Cue is open in a window');
  });

  it('offers no popout to panels when onPoppedPanelKeyChange is not supplied', () => {
    render(<ExtensionPanelHost panels={[transcript()]} visiblePanelKeys={new Set([transcriptKey])} />);
    expect(seen.get('transcript')!.popout).toBeUndefined();
    expect(screen.queryByRole('dialog')).toBeNull();
  });
});

describe('placePanelNode', () => {
  function connectedNodeAndParent() {
    const source = document.createElement('div');
    const node = document.createElement('div');
    source.appendChild(node);
    const parent = document.createElement('div');
    document.body.append(source, parent);
    attached.push(source, parent);
    return { node, parent };
  }

  it('uses moveBefore on a connected parent when the browser provides it', () => {
    const { node, parent } = connectedNodeAndParent();
    const moveBefore = vi.fn();
    Object.assign(parent, { moveBefore });
    const appendChild = vi.spyOn(parent, 'appendChild');
    placePanelNode(node, parent);
    expect(moveBefore).toHaveBeenCalledWith(node, null);
    expect(appendChild).not.toHaveBeenCalled();
  });

  it('falls back to appendChild when moveBefore is unavailable', () => {
    const { node, parent } = connectedNodeAndParent();
    const appendChild = vi.spyOn(parent, 'appendChild');
    placePanelNode(node, parent);
    expect(appendChild).toHaveBeenCalledWith(node);
    expect(parent.lastChild).toBe(node);
  });
});
