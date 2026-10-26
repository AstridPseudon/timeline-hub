import React from 'react';
import { fireEvent, render, screen, within } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { GenerationsPaneControls } from './GenerationsPaneControls';
import { SHOT_FILTER } from '@/shared/constants/filterConstants';

const SHOTS = [
  { id: 'shot-1', name: 'Opening' },
  { id: 'shot-2', name: 'Finale' },
] as React.ComponentProps<typeof GenerationsPaneControls>['filters']['shots'];

describe('GenerationsPaneControls', () => {
  function buildProps(overrides: Partial<React.ComponentProps<typeof GenerationsPaneControls>> = {}) {
    return {
      filters: {
        shots: [],
        selectedShotFilter: SHOT_FILTER.ALL,
        onSelectedShotFilterChange: vi.fn(),
        excludePositioned: false,
        onExcludePositionedChange: vi.fn(),
        isMobile: false,
        shotFilterContentRef: { current: null },
        mediaTypeFilterContentRef: { current: null },
        shotFilterOpen: false,
        onShotFilterOpenChange: vi.fn(),
        mediaTypeFilter: 'all',
        onMediaTypeFilterChange: vi.fn(),
        mediaTypeFilterOpen: false,
        onMediaTypeFilterOpenChange: vi.fn(),
        searchTerm: '',
        onSearchTermChange: vi.fn(),
        isSearchOpen: false,
        onSearchOpenChange: vi.fn(),
        searchInputRef: { current: null },
        starredOnly: false,
        onStarredOnlyChange: vi.fn(),
        currentShotId: null,
        isSpecialFilterSelected: false,
      },
      pagination: {
        totalCount: 3,
        perPage: 18,
        page: 1,
        onPageChange: vi.fn(),
      },
      interaction: {
        isInteractionDisabled: false,
      },
      ...overrides,
    } as React.ComponentProps<typeof GenerationsPaneControls>;
  }

  it('offers All, Images, Videos and Audio with All selected by default', () => {
    render(<GenerationsPaneControls {...buildProps()} />);
    const group = screen.getByRole('radiogroup', { name: 'Media type' });
    const radios = within(group).getAllByRole('radio');
    expect(radios.map((r) => r.textContent)).toEqual(['All', 'Images', 'Videos', 'Audio']);
    expect(within(group).getByRole('radio', { name: 'All' })).toHaveAttribute('aria-checked', 'true');
  });

  it('passes video through the media type handler', () => {
    const props = buildProps();
    render(<GenerationsPaneControls {...props} />);
    const group = screen.getByRole('radiogroup', { name: 'Media type' });
    fireEvent.click(within(group).getByRole('radio', { name: 'Videos' }));
    expect(props.filters.onMediaTypeFilterChange).toHaveBeenCalledWith('video');
  });

  it('hides the scope menu when there are no shots and no current shot', () => {
    render(<GenerationsPaneControls {...buildProps()} />);
    expect(screen.queryByRole('combobox')).not.toBeInTheDocument();
    expect(screen.queryByText('All shots')).not.toBeInTheDocument();
  });

  it('shows the scope menu with labels, not raw values', () => {
    render(
      <GenerationsPaneControls
        {...buildProps({
          filters: { ...buildProps().filters, shots: SHOTS, selectedShotFilter: SHOT_FILTER.NO_SHOT },
        })}
      />,
    );
    expect(screen.getByText('Not in a shot')).toBeInTheDocument();
    expect(screen.queryByText('no-shot')).not.toBeInTheDocument();
  });

  it('shows the page range for page 2 of 19 at 18 per page', () => {
    render(
      <GenerationsPaneControls
        {...buildProps({
          pagination: { totalCount: 19, perPage: 18, page: 2, onPageChange: vi.fn() },
        })}
      />,
    );
    expect(screen.getByText('19–19 of 19')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Next page' })).toBeDisabled();
    expect(screen.getByRole('button', { name: 'Previous page' })).toBeEnabled();
  });

  it('opens the page menu and jumps to the chosen page', () => {
    const onPageChange = vi.fn();
    render(
      <GenerationsPaneControls
        {...buildProps({
          pagination: { totalCount: 19, perPage: 18, page: 2, onPageChange },
        })}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /19–19 of 19/ }));
    fireEvent.click(screen.getByRole('menuitemradio', { name: 'Page 1' }));
    expect(onPageChange).toHaveBeenCalledWith(1);
  });

  it('shows a plain item count on a single page', () => {
    render(
      <GenerationsPaneControls
        {...buildProps({ pagination: { totalCount: 19, perPage: 25, page: 1, onPageChange: vi.fn() } })}
      />,
    );
    expect(screen.getByText('19 items')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Next page' })).not.toBeInTheDocument();
  });

  it('reports the star as pressed when starred only is on', () => {
    render(
      <GenerationsPaneControls
        {...buildProps({ filters: { ...buildProps().filters, starredOnly: true } })}
      />,
    );
    expect(screen.getByRole('button', { name: 'Starred only' })).toHaveAttribute('aria-pressed', 'true');
  });

  it('toggles search and starred filters via callbacks', () => {
    const onSearchOpenChange = vi.fn();
    const onStarredOnlyChange = vi.fn();
    render(
      <GenerationsPaneControls
        {...buildProps({
          filters: { ...buildProps().filters, onSearchOpenChange, onStarredOnlyChange },
        })}
      />,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Search prompts' }));
    fireEvent.click(screen.getByRole('button', { name: 'Starred only' }));

    expect(onSearchOpenChange).toHaveBeenCalledWith(true);
    expect(onStarredOnlyChange).toHaveBeenCalledWith(true);
  });
});
