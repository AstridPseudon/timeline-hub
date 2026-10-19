// @vitest-environment jsdom
import { render, screen } from '@testing-library/react';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import type { Project } from '@/integrations/runtime/generated.ts';
import { AstridTravelRoute } from './AstridTravelRoute.tsx';

const mocks = vi.hoisted(() => ({ discovery: null as any }));
vi.mock('@/tools/video-editor/hooks/useRuntimeEditorDiscovery.ts', () => ({
  useRuntimeEditorDiscovery: () => mocks.discovery,
  chooseRuntimeTimeline: (_project: Project, timelines: any[]) => timelines.find((t) => t.is_default),
}));
vi.mock('./LocalTimelineShotBrowser.tsx', () => ({
  LocalTimelineShotBrowser: (props: { projectSlug: string; projectId?: string; timelineRef: string }) => (
    <div data-testid="shot-browser" data-project={props.projectId} data-timeline={props.timelineRef} />
  ),
}));
function LocationProbe() {
  const location = useLocation();
  return <output data-testid="route-search">{location.search}</output>;
}

const project: Project = {
  project_id: 'project-id', realm_id: 'realm', slug: 'project-slug', name: 'Project',
  metadata: {}, version: 1, created_at: '', updated_at: '',
};

describe('AstridTravelRoute', () => {
  it('opens the canonical timeline without rewriting the URL', () => {
    mocks.discovery = {
      project,
      projectsQuery: { isLoading: false, error: null },
      timelinesQuery: { data: [{ timeline_id: 'timeline-id', timeline_ulid: 'timeline-alias', name: 'Main' }], isLoading: false, error: null },
    };
    render(<MemoryRouter initialEntries={['/tools/travel-between-images?project=project-id&timeline=timeline-id']}>
      <LocationProbe /><AstridTravelRoute />
    </MemoryRouter>);
    expect(screen.getByTestId('shot-browser')).toHaveAttribute('data-project', 'project-id');
    expect(screen.getByTestId('shot-browser')).toHaveAttribute('data-timeline', 'timeline-id');
    expect(screen.getByTestId('route-search')).toHaveTextContent('?project=project-id&timeline=timeline-id');
  });
  it('reports an explicitly missing timeline', () => {
    mocks.discovery = {
      project,
      projectsQuery: { isLoading: false, error: null },
      timelinesQuery: { data: [{ timeline_id: 'existing' }], isLoading: false, error: null },
    };
    render(<MemoryRouter initialEntries={['/tools/travel-between-images?project=project-id&timeline=missing']}>
      <AstridTravelRoute />
    </MemoryRouter>);
    expect(screen.getByText('Astrid timeline not found')).toBeInTheDocument();
  });
});
