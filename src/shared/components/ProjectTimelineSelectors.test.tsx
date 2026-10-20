// @vitest-environment jsdom
import { fireEvent, render, screen, within } from '@testing-library/react';
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
    expect(await screen.findByText('No timelines for this project yet.')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'New timeline' }));
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

  it('offers New timeline only as the last row of the timeline list', async () => {
    const onCreateTimeline = vi.fn();
    render(
      <ProjectTimelinePicker
        projects={[]}
        timelines={[
          { id: 'timeline-1', name: 'Intro Cut' },
          { id: 'timeline-2', name: 'Alt Cut' },
        ]}
        projectId="project-id"
        timelineId="timeline-1"
        onSelectProject={vi.fn()}
        onSelectTimeline={vi.fn()}
        onCreateTimeline={onCreateTimeline}
      />,
    );
    // No caption and no second button beside the picker: the combobox names itself.
    expect(screen.queryByRole('button', { name: 'New timeline' })).toBeNull();
    expect(screen.queryByText('Timeline')).toBeNull();
    const user = userEvent.setup();
    await user.click(screen.getByRole('combobox', { name: 'Select timeline' }));
    // Still offered while a search hides every row.
    await user.type(await screen.findByPlaceholderText('Search timelines...'), 'zzz');
    await user.click(screen.getByRole('button', { name: 'New timeline' }));
    expect(onCreateTimeline).toHaveBeenCalledTimes(1);
    expect(screen.queryByRole('button', { name: 'New timeline' })).toBeNull();
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

  it('marks only the primary timeline row with a labelled star in the left column', async () => {
    render(
      <ProjectTimelinePicker
        projects={[]}
        timelines={[
          { id: 'main', name: 'Main Cut', isPrimary: true },
          { id: 'alt', name: 'Alt Cut' },
        ]}
        projectId={null}
        timelineId="alt"
        onSelectProject={vi.fn()}
        onSelectTimeline={vi.fn()}
      />,
    );
    const user = userEvent.setup();
    await user.click(screen.getByRole('combobox', { name: 'Select timeline' }));
    const primaryRow = await screen.findByRole('option', { name: /Main Cut/ });
    const mark = within(primaryRow).getByRole('img', { name: 'Primary timeline' });
    expect(mark.closest('.absolute')).not.toBeNull();
    expect(primaryRow.querySelector('svg.lucide-check')).toBeNull();

    const otherRow = screen.getByRole('option', { name: /Alt Cut/ });
    expect(within(otherRow).queryByRole('img', { name: 'Primary timeline' })).toBeNull();
    expect(otherRow.querySelector('svg.lucide-star')).toBeNull();
  });

  it('shows the selected tick and the primary star together when the selected timeline is primary', async () => {
    const { rerender } = render(
      <ProjectTimelinePicker
        projects={[]}
        timelines={[{ id: 'main', name: 'Main Cut', isPrimary: true }, { id: 'alt', name: 'Alt Cut' }]}
        projectId={null}
        timelineId="main"
        onSelectProject={vi.fn()}
        onSelectTimeline={vi.fn()}
      />,
    );
    // The closed trigger carries the same star for the current primary timeline.
    expect(within(screen.getByRole('combobox', { name: 'Select timeline' })).getByRole('img', { name: 'Primary timeline' })).toBeInTheDocument();

    const user = userEvent.setup();
    await user.click(screen.getByRole('combobox', { name: 'Select timeline' }));
    const row = await screen.findByRole('option', { name: /Main Cut/ });
    expect(row).toHaveAttribute('aria-current', 'true');
    expect(row.querySelector('svg.lucide-check')).not.toBeNull();
    expect(within(row).getByRole('img', { name: 'Primary timeline' })).toBeInTheDocument();
    await user.keyboard('{Escape}');

    rerender(
      <ProjectTimelinePicker
        projects={[]}
        timelines={[{ id: 'main', name: 'Main Cut', isPrimary: true }, { id: 'alt', name: 'Alt Cut' }]}
        projectId={null}
        timelineId="alt"
        onSelectProject={vi.fn()}
        onSelectTimeline={vi.fn()}
      />,
    );
    // A non-primary selection shows no star on the trigger.
    expect(within(screen.getByRole('combobox', { name: 'Select timeline' })).queryByRole('img', { name: 'Primary timeline' })).toBeNull();
  });
});
