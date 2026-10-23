import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TooltipProvider } from '@/shared/components/ui/tooltip';
import { PaneControlTab } from './PaneControlTab';

vi.mock('@/shared/hooks/mobile', () => ({ useIsMobile: () => false, useIsTablet: () => false }));

const renderTab = (side: 'right' | 'left', isOpen = false) =>
  render(
    <TooltipProvider>
      <PaneControlTab
        position={{ side, paneDimension: 300 }}
        state={{ isLocked: true, isOpen }}
        handlers={{ toggleLock: vi.fn(), openPane: vi.fn(), handlePaneEnter: vi.fn(), handlePaneLeave: vi.fn() }}
        actions={{ thirdButton: { onClick: vi.fn(), ariaLabel: 'third', content: <span>0</span> } }}
      />
    </TooltipProvider>,
  );

describe('PaneControlTab grip', () => {
  it('rests as a slim grip on the right and expands on hover and focus', () => {
    const { container } = renderTab('right');
    const tab = container.querySelector('[data-pane-control]') as HTMLElement;
    expect(tab.dataset.paneControlGrip).toBe('true');
    expect(tab.className).toContain('w-[10px]');
    fireEvent.mouseEnter(tab);
    expect(tab.dataset.paneControlGrip).toBeUndefined();
    fireEvent.mouseLeave(tab);
    expect(tab.dataset.paneControlGrip).toBe('true');
    fireEvent.focus(screen.getByLabelText('third'));
    expect(tab.dataset.paneControlGrip).toBeUndefined();
    fireEvent.blur(screen.getByLabelText('third'));
    expect(tab.dataset.paneControlGrip).toBe('true');
  });

  it('keeps the full tab on other sides', () => {
    const { container } = renderTab('left');
    expect((container.querySelector('[data-pane-control]') as HTMLElement).dataset.paneControlGrip).toBeUndefined();
  });
});
