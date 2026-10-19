// @vitest-environment jsdom
import { fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { AppHeader } from '@/shared/components/AppHeader.tsx';

describe('AppHeader', () => {
  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it('uses Home navigation when the editor is not the home tool', () => {
    const onNavigate = vi.fn();

    render(
      <AppHeader
        onNavigate={onNavigate}
        navigationControls={<div data-testid="selectors">Project One</div>}
        timelineName="Main timeline"
      />,
    );

    expect(screen.getByRole('button', { name: 'Go home' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Open tools' })).toBeNull();
    expect(screen.getByTestId('selectors')).toBeInTheDocument();
    expect(screen.getByText('Main timeline')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Go home' }));
    expect(onNavigate).toHaveBeenCalledTimes(1);
  });

  it('uses Tools navigation when the editor is the home tool', () => {
    render(
      <AppHeader
        navigationMode="tools"
        onNavigate={vi.fn()}
      />,
    );

    expect(screen.getByRole('button', { name: 'Open tools' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Go home' })).toBeNull();
  });

  it('keeps editor selectors and app settings while removing app navigation in local Astrid mode', () => {
    vi.stubEnv('VITE_ASTRID_EDITOR_ONLY', '1');
    const settingsEvent = vi.fn();
    window.addEventListener('openSettings', settingsEvent, { once: true });

    render(
      <AppHeader
        onNavigate={vi.fn()}
        navigationControls={<div data-testid="selectors">Project One</div>}
        timelineName="Main timeline"
      />,
    );

    expect(screen.getByTestId('selectors')).toBeInTheDocument();
    expect(screen.getByText('Main timeline')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Go home' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Open tools' })).toBeNull();
    expect(screen.getByRole('button', { name: 'App settings' })).toBeInTheDocument();
    expect(screen.getByTestId('video-editor-header')).not.toHaveClass('border-b');

    fireEvent.click(screen.getByRole('button', { name: 'App settings' }));
    expect(settingsEvent).toHaveBeenCalledTimes(1);
  });

  it('renders the page-owned project selector without app-wide Tools or built-in project controls', () => {
    vi.stubEnv('VITE_ASTRID_EDITOR_ONLY', '1');
    render(
      <AppHeader
        navigationMode="tools"
        navigationControls={<button type="button">Editor project selector</button>}
        showProjectControls={false}
      />,
    );

    expect(screen.getByRole('button', { name: 'Editor project selector' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Open tools' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Go home' })).toBeNull();
    expect(screen.getByRole('button', { name: 'App settings' })).toBeInTheDocument();
  });
});
