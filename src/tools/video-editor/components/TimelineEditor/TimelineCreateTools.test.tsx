// @vitest-environment jsdom
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import {
  CREATE_ANIMATION_PROMPT,
  CREATE_EFFECT_PROMPT,
  TimelineCreateTools,
} from '@/tools/video-editor/components/TimelineEditor/TimelineCreateTools.tsx';

const noop = () => {};

describe('TimelineCreateTools', () => {
  it('touch: three 40px tap buttons that call their handlers, and are not drag sources', () => {
    const onAddText = vi.fn();
    const onCreateEffect = vi.fn();
    const onCreateAnimation = vi.fn();
    render(
      <TimelineCreateTools
        variant="touch"
        host="playback-row"
        onAddText={onAddText}
        onCreateEffect={onCreateEffect}
        effectLabel="Create new effect"
        onCreateAnimation={onCreateAnimation}
        animationLabel="Create animation"
      />,
    );

    const buttons = ['New text at playhead', 'Create new effect', 'Create animation'].map(
      (name) => screen.getByRole('button', { name }),
    );
    buttons.forEach((button) => {
      expect(button.tagName).toBe('BUTTON');
      expect(button.className).toContain('h-10 w-10');
      expect(button.getAttribute('draggable')).not.toBe('true');
      fireEvent.click(button);
    });
    expect(onAddText).toHaveBeenCalledTimes(1);
    expect(onCreateEffect).toHaveBeenCalledTimes(1);
    expect(onCreateAnimation).toHaveBeenCalledTimes(1);
  });

  it('pointer: keeps the text-tool and effect-layer HTML5 drag sources', () => {
    render(
      <TimelineCreateTools
        variant="pointer"
        host="timeline-footer"
        onAddText={noop}
        onCreateEffect={noop}
        effectLabel="New effect layer at playhead"
        effectDragSource
        onCreateAnimation={noop}
        animationLabel="Create animation sequence"
      />,
    );

    const text = screen.getByTitle('Drag onto timeline to add text');
    const effect = screen.getByTitle('Drag onto timeline to add an effect layer');
    expect(text.getAttribute('draggable')).toBe('true');
    expect(effect.getAttribute('draggable')).toBe('true');

    const textTransfer = { setData: vi.fn(), effectAllowed: '' };
    fireEvent.dragStart(text, { dataTransfer: textTransfer });
    expect(textTransfer.setData).toHaveBeenCalledWith('text-tool', 'true');
    const effectTransfer = { setData: vi.fn(), effectAllowed: '' };
    fireEvent.dragStart(effect, { dataTransfer: effectTransfer });
    expect(effectTransfer.setData).toHaveBeenCalledWith('effect-layer', 'true');
    expect(screen.getByRole('button', { name: 'Create animation sequence' }).className).toContain('h-6 w-6');
  });

  it('marks the root with its host, and as shell chrome only when the shell hosts it', () => {
    const { rerender } = render(
      <TimelineCreateTools variant="pointer" host="timeline-footer" onAddText={noop} effectLabel="x" animationLabel="y" />,
    );
    const root = () => screen.getByTestId('timeline-tool-buttons');
    expect(root().getAttribute('data-create-tools-host')).toBe('timeline-footer');
    expect(root().hasAttribute('data-shell-interaction')).toBe(false);

    rerender(<TimelineCreateTools variant="touch" host="toolbar" onAddText={noop} effectLabel="x" animationLabel="y" />);
    expect(root().getAttribute('data-create-tools-host')).toBe('toolbar');
    expect(root().getAttribute('data-shell-interaction')).toBe('true');
  });

  it.each(['playback-row', 'toolbar'] as const)('carries its own theme variables when the shell hosts it (%s), outside any canvas', (host) => {
    render(<TimelineCreateTools variant="touch" host={host} onAddText={noop} onCreateEffect={noop} onCreateAnimation={noop} effectLabel="x" animationLabel="y" />);
    const root = screen.getByTestId('timeline-tool-buttons');
    ['--video-editor-accent-bg-strong', '--video-editor-effect-bg', '--video-editor-success-bg'].forEach((name) => {
      expect(root.style.getPropertyValue(name), name).not.toBe('');
    });
    expect(root.style.left).toBe('');
  });

  it('keeps pointer-down from reaching the timeline behind it', () => {
    const onParentPointerDown = vi.fn();
    render(
      <div onPointerDown={onParentPointerDown}>
        <TimelineCreateTools variant="touch" host="toolbar" onAddText={noop} effectLabel="x" animationLabel="y" />
      </div>,
    );
    fireEvent.pointerDown(screen.getByRole('button', { name: 'New text at playhead' }));
    expect(onParentPointerDown).not.toHaveBeenCalled();
  });

  it('defines each agent prompt exactly once in the source', () => {
    const dir = join(import.meta.dirname, '..');
    const sources = [
      'TimelineEditor/TimelineCanvas.tsx',
      'TimelineEditor/TimelineCreateTools.tsx',
      'TimelineEditorShellCore.tsx',
    ].map((file) => readFileSync(join(dir, file), 'utf8'));
    const occurrences = (needle: string) => sources.reduce((count, source) => count + source.split(needle).length - 1, 0);

    expect(CREATE_EFFECT_PROMPT).toBe("I'd like to create a new effect.");
    expect(CREATE_ANIMATION_PROMPT).toBe("I'd like to create an animation.");
    expect(occurrences(CREATE_EFFECT_PROMPT)).toBe(1);
    expect(occurrences(CREATE_ANIMATION_PROMPT)).toBe(1);
  });
});
