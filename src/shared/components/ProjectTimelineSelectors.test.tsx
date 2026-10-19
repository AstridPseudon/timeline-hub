// @vitest-environment jsdom
import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeAll, describe, expect, it, vi } from 'vitest';
import { ProjectTimelinePicker } from '@/shared/components/ProjectTimelineSelectors.tsx';

beforeAll(() => {
  if (!Element.prototype.scrollIntoView) Element.prototype.scrollIntoView = vi.fn();
});

describe('ProjectTimelinePicker', () => {
  it('shows project and timeline names with the primary indicator', async () => {
    render(
      <ProjectTimelinePicker
        projects={[{ id: 'project-id', name: 'Project Name', detail: 'project-slug' }]}
        timelines={[
          { id: 'timeline-id', name: 'Main Cut', detail: 'edited 5 minutes ago', isPrimary: true },
          { id: 'shot-id', name: 'Shot 1', detail: 'shot-001' },
        ]}
        projectId="project-id"
        timelineId="timeline-id"
        onSelectProject={vi.fn()}
        onSelectTimeline={vi.fn()}
      />,
    );
    expect(screen.getByRole('combobox', { name: 'Select project' })).toHaveTextContent('Project Name');
    const user = userEvent.setup();
    await user.click(screen.getByRole('combobox', { name: 'Select timeline' }));
    expect(await screen.findByRole('option', { name: /Main Cut/ })).toHaveTextContent('Primary');
    expect(screen.getByRole('option', { name: /Shot 1/ })).toBeInTheDocument();
  });

  it('creates the first timeline from an empty list and disables while creating', async () => {
    const onCreateTimeline = vi.fn();
    const view = render(
      <ProjectTimelinePicker
        projects={[]}
        timelines={[]}
        projectId="project-id"
        timelineId={null}
        onSelectProject={vi.fn()}
        onSelectTimeline={vi.fn()}
        onCreateTimeline={onCreateTimeline}
      />,
    );
    const user = userEvent.setup();
    await user.click(screen.getByRole('combobox', { name: 'Select timeline' }));
    await user.click(await screen.findByRole('button', { name: 'Create first timeline' }));
    expect(onCreateTimeline).toHaveBeenCalledTimes(1);
    view.rerender(
      <ProjectTimelinePicker
        projects={[]}
        timelines={[]}
        projectId="project-id"
        timelineId={null}
        onSelectProject={vi.fn()}
        onSelectTimeline={vi.fn()}
        onCreateTimeline={onCreateTimeline}
        creatingTimeline
      />,
    );
    await user.click(screen.getByRole('combobox', { name: 'Select timeline' }));
    expect(await screen.findByRole('button', { name: 'Creating timeline…' })).toBeDisabled();
  });

  it('retries discovery and selects canonical primary timeline IDs', async () => {
    const onRetry = vi.fn();
    const onSetPrimaryTimeline = vi.fn();
    render(
      <ProjectTimelinePicker
        projects={[]}
        timelines={[{ id: 'canonical-id', name: 'Alt Cut' }]}
        projectId={null}
        timelineId={null}
        projectsError="Runtime offline"
        onRetry={onRetry}
        onSelectProject={vi.fn()}
        onSelectTimeline={vi.fn()}
        onSetPrimaryTimeline={onSetPrimaryTimeline}
      />,
    );
    const user = userEvent.setup();
    await user.click(screen.getByRole('combobox', { name: 'Select project' }));
    await user.click(await screen.findByRole('button', { name: 'Retry connection' }));
    expect(onRetry).toHaveBeenCalledTimes(1);
    await user.click(screen.getByRole('combobox', { name: 'Select timeline' }));
    await user.click(await screen.findByRole('button', { name: 'Make Alt Cut primary' }));
    expect(onSetPrimaryTimeline).toHaveBeenCalledWith('canonical-id');
  });

  it('renames the selected timeline without selecting it', async () => {
    const onSelectTimeline = vi.fn();
    const onRenameTimeline = vi.fn(async () => undefined);
    render(
      <ProjectTimelinePicker
        projects={[]}
        timelines={[{ id: 'timeline-1', name: 'Intro Cut' }]}
        projectId={null}
        timelineId="timeline-1"
        onSelectProject={vi.fn()}
        onSelectTimeline={onSelectTimeline}
        onRenameTimeline={onRenameTimeline}
      />,
    );
    const user = userEvent.setup();
    await user.click(screen.getByRole('combobox', { name: 'Select timeline' }));
    await user.click(await screen.findByRole('button', { name: 'Rename timeline' }));
    const input = await screen.findByRole('textbox', { name: 'Timeline name' });
    fireEvent.change(input, { target: { value: '  Opening Cut  ' } });
    fireEvent.submit(input.closest('form')!);
    expect(onRenameTimeline).toHaveBeenCalledWith('timeline-1', 'Opening Cut');
    expect(onSelectTimeline).not.toHaveBeenCalled();
  });
});
