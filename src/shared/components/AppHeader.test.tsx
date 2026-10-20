// @vitest-environment jsdom
import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import { AppHeader } from '@/shared/components/AppHeader.tsx';

const runtimeMock = vi.hoisted(() => ({
  discovery: null as any,
}));
vi.mock('@/tools/video-editor/hooks/useRuntimeEditorDiscovery.ts', () => ({
  useRuntimeEditorDiscovery: () => runtimeMock.discovery,
}));
vi.mock('@/shared/components/ProjectHeaderActions.tsx', () => ({
  ProjectHeaderActions: () => null,
}));
function RouteSearch() {
  const location = useLocation();
  return <output data-testid="route-search">{location.search}</output>;
}
beforeAll(() => {
  if (!Element.prototype.scrollIntoView) Element.prototype.scrollIntoView = vi.fn();
});

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

  it('sits in the content layer, above the fixed sky backdrop, in both header variants', () => {
    const { unmount } = render(<AppHeader />);
    expect(screen.getByTestId('video-editor-header')).toHaveClass('relative', 'z-10');
    unmount();

    vi.stubEnv('VITE_ASTRID_EDITOR_ONLY', '1');
    render(<AppHeader />);
    expect(screen.getByTestId('video-editor-header')).toHaveClass('relative', 'z-10');
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

  it('selects Runtime project IDs and writes canonical project navigation', async () => {
    const project = { project_id: 'canonical-project', slug: 'project-slug', name: 'Canonical Project', metadata: {} };
    runtimeMock.discovery = {
      project,
      projectsQuery: { data: [project], isLoading: false, error: null, refetch: vi.fn() },
      reconnect: vi.fn(),
    };
    render(
      <MemoryRouter initialEntries={['/tools/video-editor?project=old-project&timeline=old-timeline&intent=keep']}>
        <RouteSearch />
        <AppHeader showProjectControls />
      </MemoryRouter>,
    );
    const user = userEvent.setup();
    await user.click(screen.getByRole('combobox', { name: 'Select project' }));
    await user.click(await screen.findByRole('option', { name: /Canonical Project/ }));
    expect(screen.getByTestId('route-search')).toHaveTextContent('project=canonical-project');
    expect(screen.getByTestId('route-search')).not.toHaveTextContent('timeline=');
    expect(screen.getByTestId('route-search')).toHaveTextContent('intent=keep');
  });
});
