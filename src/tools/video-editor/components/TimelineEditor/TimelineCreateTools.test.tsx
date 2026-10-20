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
  it('keeps the text-tool and effect-layer HTML5 drag sources, 24px, and a prompt-free animation button', () => {
    const onCreateAnimation = vi.fn();
    render(
      <TimelineCreateTools
        labelWidth={144}
        showTextTool
        onCreateEffect={noop}
        effectLabel="New effect layer at playhead"
        effectDragSource
        onCreateAnimation={onCreateAnimation}
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
    expect(textTransfer.effectAllowed).toBe('copy');
    const effectTransfer = { setData: vi.fn(), effectAllowed: '' };
    fireEvent.dragStart(effect, { dataTransfer: effectTransfer });
    expect(effectTransfer.setData).toHaveBeenCalledWith('effect-layer', 'true');

    const animation = screen.getByRole('button', { name: 'Create animation sequence' });
    expect(animation.className).toContain('h-6 w-6');
    fireEvent.click(animation);
    expect(onCreateAnimation).toHaveBeenCalledTimes(1);
  });

  it('turns the effect tool into a prompt button when the host takes prompts', () => {
    const onCreateEffect = vi.fn();
    render(
      <TimelineCreateTools labelWidth={144} onCreateEffect={onCreateEffect} effectLabel="Create new effect" animationLabel="Create animation" />,
    );

    expect(screen.queryByTitle('Drag onto timeline to add an effect layer')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Create new effect' }));
    expect(onCreateEffect).toHaveBeenCalledTimes(1);
  });

  it('shows only the tools it is given, just right of the track-name column', () => {
    render(<TimelineCreateTools labelWidth={144} showTextTool effectLabel="x" animationLabel="y" />);

    expect(screen.getByTitle('Drag onto timeline to add text')).toBeInTheDocument();
    expect(screen.queryByTitle('New effect')).toBeNull();
    expect(screen.queryByRole('button')).toBeNull();
    expect(screen.getByTestId('timeline-tool-buttons').style.left).toBe('152px');
  });

  it('keeps pointer-down from reaching the timeline behind it', () => {
    const onParentPointerDown = vi.fn();
    render(
      <div onPointerDown={onParentPointerDown}>
        <TimelineCreateTools labelWidth={144} onCreateAnimation={noop} effectLabel="x" animationLabel="Create animation" />
      </div>,
    );
    fireEvent.pointerDown(screen.getByRole('button', { name: 'Create animation' }));
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
