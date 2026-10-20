import agentTheme from '../../../../../agent-theme.json';
import type { Theme } from '@banodoco/timeline-composition/theme-api';
// @vitest-environment jsdom
import React, { createRef } from 'react';
import { act, cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { RemotionPreview, type PreviewHandle } from './RemotionPreview';
import type { PreviewRevision } from './previewRevision';
import type { ResolvedTimelineConfig } from '@/tools/video-editor/types';

vi.mock('@/tools/video-editor/compositions/TimelineRenderer', () => ({ TimelineRenderer: () => null }));

// External Player boundary from the preserved C2 current-owner counterexample.
// It records commands and public events; config scheduling remains in the real owner.
const boundary = vi.hoisted(() => ({
  player: null as any,
  props: null as any,
  applied: [] as ResolvedTimelineConfig[],
  events: [] as Array<{ frame: number; fps: number; config: string }>,
  listeners: new Map<string, Set<(event: any) => void>>(),
}));
vi.mock('@remotion/player', async () => {
  const React = await import('react');
  return {
    Player: React.forwardRef(function Player(props: any, ref: any) {
      boundary.props = props;
      boundary.applied.push(props.inputProps.config);
      const handle = React.useRef<any>(null);
      if (!handle.current) {
        let frame = props.initialFrame;
        let playing = false;
        const emit = (name: string) => {
          for (const listener of boundary.listeners.get(name) ?? []) listener({});
        };
        handle.current = {
          seekTo: vi.fn((next: number) => {
            frame = next;
            boundary.events.push({ frame, fps: boundary.props.fps, config: boundary.props.inputProps.config.output.file });
          }),
          getCurrentFrame: vi.fn(() => frame),
          isPlaying: vi.fn(() => playing),
          play: vi.fn(() => { playing = true; emit('play'); }),
          pause: vi.fn(() => { playing = false; emit('pause'); }),
          toggle: vi.fn(() => { playing = !playing; emit(playing ? 'play' : 'pause'); }),
          addEventListener: (name: string, listener: (event: any) => void) => {
            if (!boundary.listeners.has(name)) boundary.listeners.set(name, new Set());
            boundary.listeners.get(name)!.add(listener);
          },
          removeEventListener: (name: string, listener: (event: any) => void) => boundary.listeners.get(name)?.delete(listener),
        };
      }
      React.useImperativeHandle(ref, () => handle.current, []);
      boundary.player = handle.current;
      return <div data-testid="mailbox-player" />;
    }),
  };
});

function config(name: string, fps = 30): ResolvedTimelineConfig {
  return {
    output: { fps, resolution: '1280x720', file: name },
    tracks: [{ id: 'V1', kind: 'visual', label: 'V1' }],
    clips: [{ id: name, at: 0, track: 'V1', clipType: 'hold', hold: 3 }],
    registry: {},
  };
}
let raf = new Map<number, FrameRequestCallback>();
let nextRaf = 0;
function flushFrame() {
  act(() => {
    const callbacks = [...raf.values()];
    raf.clear();
    for (const callback of callbacks) callback(1000);
  });
}
function advance(ms: number) { act(() => { vi.advanceTimersByTime(ms); }); }
function settle() {
  for (let i = 0; i < 8; i++) {
    advance(150);
    if (!raf.size) return;
    flushFrame();
  }
  expect(raf.size, 'finite RAF work exhausted').toBe(0);
}
function preview(initial: ResolvedTimelineConfig, initialRevision?: PreviewRevision, initialTheme?: Theme) {
  const ref = createRef<PreviewHandle>();
  const container = createRef<HTMLDivElement>();
  const onTimeUpdate = vi.fn();
  const draw = (c: ResolvedTimelineConfig, revision = initialRevision, theme = initialTheme) => (
    <RemotionPreview
      ref={ref}
      config={c}
      previewRevision={revision}
      resolvedTheme={theme}
      onTimeUpdate={onTimeUpdate}
      playerContainerRef={container}
    />
  );
  const view = render(draw(initial));
  return {
    ref,
    view,
    replace: (c: ResolvedTimelineConfig, revision?: PreviewRevision, theme?: Theme) => view.rerender(draw(c, revision, theme)),
  };
}
beforeEach(() => {
  vi.useFakeTimers();
  boundary.player = null;
  boundary.props = null;
  boundary.applied = [];
  boundary.events = [];
  boundary.listeners.clear();
  raf = new Map();
  nextRaf = 0;
  vi.stubGlobal('requestAnimationFrame', (callback: FrameRequestCallback) => { raf.set(++nextRaf, callback); return nextRaf; });
  vi.stubGlobal('cancelAnimationFrame', (id: number) => raf.delete(id));
});
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); vi.useRealTimers(); });

it('H3 newest C beats queued playing B on explicit pause and subsequent one-second seek', () => {
  const a = config('h3-a', 30), b = config('h3-b', 60), c = config('h3-c', 90);
  const h = preview(a);
  settle();
  act(() => h.ref.current!.play());
  flushFrame();
  h.replace(b);
  act(() => { h.ref.current!.pause(); h.replace(c); });
  // Pending live work flushes immediately, without a 150ms paused-edit wait.
  expect.soft(boundary.props.inputProps.config).toBe(c);
  settle();
  act(() => h.ref.current!.seek(1));
  settle();
  expect.soft(boundary.props.inputProps.config).toBe(c);
  expect.soft(boundary.player.seekTo).toHaveBeenLastCalledWith(90);
  expect.soft(boundary.player.isPlaying()).toBe(false);
  expect.soft(boundary.player.play).toHaveBeenCalledTimes(1);
  expect.soft(boundary.applied).not.toContain(b);
  expect.soft(raf.size).toBe(0);
  expect.soft(vi.getTimerCount()).toBe(0);
});

it('flushes pending B immediately when pausing without a newer config', () => {
  const a = config('pending-a'), b = config('pending-b', 60);
  const h = preview(a);
  settle();
  act(() => h.ref.current!.play());
  flushFrame();
  h.replace(b);
  expect(boundary.props.inputProps.config).toBe(a);
  act(() => h.ref.current!.pause());
  expect(boundary.props.inputProps.config).toBe(b);
  expect(raf.size).toBe(0);
  settle();
  act(() => h.ref.current!.seek(1));
  settle();
  expect(boundary.player.seekTo).toHaveBeenLastCalledWith(60);
  expect(boundary.player.isPlaying()).toBe(false);
  expect(boundary.player.play).toHaveBeenCalledTimes(1);
});

it('keeps ordinary paused edits debounced for 150ms and cancels the older timer', () => {
  const a = config('paused-a'), b = config('paused-b'), c = config('paused-c');
  const h = preview(a);
  settle();
  h.replace(b);
  advance(100);
  h.replace(c);
  advance(149);
  expect(boundary.props.inputProps.config).toBe(a);
  advance(1);
  expect(boundary.props.inputProps.config).toBe(c);
  settle();
  expect(boundary.applied).not.toContain(b);
  expect(boundary.player.play).not.toHaveBeenCalled();
});

it('coalesces playing edits to only the newest config on the next finite RAF', () => {
  const a = config('coalesce-a'), b = config('coalesce-b'), c = config('coalesce-c');
  const h = preview(a);
  settle();
  act(() => h.ref.current!.play());
  flushFrame();
  h.replace(b);
  h.replace(c);
  expect(boundary.props.inputProps.config).toBe(a);
  expect(raf.size).toBe(1);
  flushFrame();
  expect(boundary.props.inputProps.config).toBe(c);
  expect(boundary.applied).not.toContain(b);
  expect(boundary.player.play).toHaveBeenCalledTimes(1);
  expect(boundary.player.isPlaying()).toBe(true);
});

it('preserves finite H2 A to B to the exact same A pending seek delivery', () => {
  const a = config('h2-a'), b = config('h2-b', 60);
  const h = preview(a);
  settle();
  act(() => h.ref.current!.seek(0.5));
  h.replace(b);
  h.replace(a);
  act(() => h.ref.current!.seek(1));
  settle();
  expect(boundary.props.inputProps.config).toBe(a);
  expect(boundary.player.seekTo).toHaveBeenNthCalledWith(1, 15);
  expect(boundary.player.seekTo).toHaveBeenLastCalledWith(30);
  expect(boundary.player.seekTo).toHaveBeenCalledTimes(2);
  expect(boundary.player.play).not.toHaveBeenCalled();
});

it('cancels pending mailbox and paused timer work on unmount', () => {
  const a = config('unmount-a'), b = config('unmount-b');
  const h = preview(a);
  settle();
  h.replace(b);
  expect(vi.getTimerCount()).toBe(1);
  h.view.unmount();
  expect(vi.getTimerCount()).toBe(0);
  const live = preview(a);
  settle();
  act(() => live.ref.current!.play());
  flushFrame();
  live.replace(b);
  expect(raf.size).toBe(1);
  live.view.unmount();
  expect(raf.size).toBe(0);
  settle();
  expect(boundary.applied).not.toContain(b);
});

it('labels a delivered historical committed revision', () => {
  preview(config('historical'), { kind: 'committed', revisionId: 'R1' });

  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Committed R1');
});

it('labels a delivered local draft with its committed base', () => {
  preview(config('draft'), { kind: 'local', baseRevisionId: 'R1' });

  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Unsaved local · based on R1');
});

it('keeps the old label until the throttled config and its metadata arrive together', () => {
  const first = config('label-first');
  const draft = config('label-draft');
  const h = preview(first, { kind: 'committed', revisionId: 'R1' });

  h.replace(draft, { kind: 'local', baseRevisionId: 'R1' });
  expect(boundary.props.inputProps.config).toBe(first);
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Committed R1');

  advance(149);
  expect(boundary.props.inputProps.config).toBe(first);
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Committed R1');

  advance(1);
  expect(boundary.props.inputProps.config).toBe(draft);
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Unsaved local · based on R1');
});

it('does not let a late acknowledgement relabel a delivered local suffix', () => {
  const local = config('local-prefix');
  const suffix = config('local-suffix');
  const h = preview(local, { kind: 'local', baseRevisionId: 'R1' });
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Unsaved local · based on R1');

  // The acknowledgement changes host metadata but not the Player input.
  h.replace(local, { kind: 'committed', revisionId: 'R2' });
  expect(boundary.props.inputProps.config).toBe(local);
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Unsaved local · based on R1');

  h.replace(suffix, { kind: 'local', baseRevisionId: 'R2' });
  advance(150);
  expect(boundary.props.inputProps.config).toBe(suffix);
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Unsaved local · based on R2');
});

it('ignores stale paused generation completion and its stale label', () => {
  const first = config('stale-first');
  const stale = config('stale-generation');
  const newest = config('newest-generation');
  const h = preview(first, { kind: 'committed', revisionId: 'R1' });

  h.replace(stale, { kind: 'committed', revisionId: 'R2' });
  advance(100);
  h.replace(newest, { kind: 'local', baseRevisionId: 'R2' });
  advance(150);

  expect(boundary.props.inputProps.config).toBe(newest);
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Unsaved local · based on R2');
});

it('keeps cached committed pixels labelled while a target is unavailable', () => {
  const h = preview(config('cached-r1'), {
    kind: 'committed',
    revisionId: 'R1',
    unavailableTarget: { targetRevisionId: 'R2', reason: 'Runtime read failed' },
  });

  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Committed R1');
  expect(screen.getByTestId('preview-revision-unavailable')).toHaveTextContent('Preview of R2 unavailable');
  expect(boundary.props.inputProps.previewRevision).toMatchObject({ kind: 'committed', revisionId: 'R1' });
});

it('shows an unavailable target without inventing a committed revision when there is no cache', () => {
  preview(config('no-cache'), {
    kind: 'unavailable',
    unavailableTarget: { targetRevisionId: 'R2', reason: 'Runtime read failed' },
  });

  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Preview of R2 unavailable');
  expect(screen.queryByText('Committed R2')).toBeNull();
});

it('clears a recovered unavailable request without relabelling the delivered pixels', () => {
  const current = config('recovered-r1');
  const h = preview(current, {
    kind: 'committed',
    revisionId: 'R1',
    unavailableTarget: { targetRevisionId: 'R2', reason: 'Runtime read failed' },
  });

  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Committed R1');
  expect(screen.getByTestId('preview-revision-unavailable')).toHaveTextContent('Preview of R2 unavailable');

  h.replace(current, { kind: 'committed', revisionId: 'R1' });

  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Committed R1');
  expect(screen.queryByTestId('preview-revision-unavailable')).toBeNull();
  expect(boundary.props.inputProps.previewRevision).toEqual({ kind: 'committed', revisionId: 'R1' });
});

// PLAN 2026-10-20 06:07: actual Agent result, never copied default literals.
it('defers config, actual theme and factual revision as one paused delivery', () => {
  const first = config('theme-first'), second = config('theme-second');
  const h = preview(first, {kind: 'committed', revisionId: 'R1'}, agentTheme.implicit);
  h.replace(second, {kind: 'local', baseRevisionId: 'R1'}, agentTheme.explicit);
  advance(149);
  expect(boundary.props.inputProps.config).toBe(first);
  expect(boundary.props.inputProps.resolvedTheme).toBe(agentTheme.implicit);
  expect(boundary.props.inputProps.previewRevision).toEqual({kind: 'committed', revisionId: 'R1'});
  advance(1);
  expect(boundary.props.inputProps.config).toBe(second);
  expect(boundary.props.inputProps.resolvedTheme).toBe(agentTheme.explicit);
  expect(boundary.props.inputProps.previewRevision).toEqual({kind: 'local', baseRevisionId: 'R1'});
});

it('changes theme on the same config identity only through the delivery mailbox', () => {
  const current = config('theme-arrival');
  const h = preview(current, {kind: 'committed', revisionId: 'R1'}, agentTheme.implicit);
  h.replace(current, {kind: 'committed', revisionId: 'R1'}, agentTheme.explicit);
  expect(boundary.props.inputProps.resolvedTheme).toBe(agentTheme.implicit);
  advance(150);
  expect(boundary.props.inputProps.resolvedTheme).toBe(agentTheme.explicit);
});

it('keeps theme while an M1 metadata-only failed-target notice arrives and recovers', () => {
  const current = config('theme-metadata');
  const h = preview(current, {kind: 'committed', revisionId: 'R1'}, agentTheme.explicit);
  h.replace(current, {kind: 'committed', revisionId: 'R1', unavailableTarget: {targetRevisionId: 'R2', reason: 'read failed'}}, agentTheme.explicit);
  expect(boundary.props.inputProps.resolvedTheme).toBe(agentTheme.explicit);
  expect(boundary.props.inputProps.previewRevision.unavailableTarget.targetRevisionId).toBe('R2');
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Committed R1');
  h.replace(current, {kind: 'committed', revisionId: 'R1'}, agentTheme.explicit);
  expect(boundary.props.inputProps.resolvedTheme).toBe(agentTheme.explicit);
  expect(boundary.props.inputProps.previewRevision.unavailableTarget).toBeUndefined();
});

it('keeps only the newest playing config and resolved theme pair', () => {
  const first = config('theme-play-first'), stale = config('theme-play-stale'), newest = config('theme-play-newest');
  const h = preview(first, {kind: 'committed', revisionId: 'R1'}, agentTheme.implicit);
  settle();
  act(() => h.ref.current!.play());
  h.replace(stale, {kind: 'committed', revisionId: 'R2'}, agentTheme.explicit);
  h.replace(newest, {kind: 'local', baseRevisionId: 'R2'}, agentTheme.implicit);
  flushFrame();
  expect(boundary.props.inputProps.config).toBe(newest);
  expect(boundary.props.inputProps.resolvedTheme).toBe(agentTheme.implicit);
  expect(boundary.props.inputProps.previewRevision).toEqual({kind: 'local', baseRevisionId: 'R2'});
});
