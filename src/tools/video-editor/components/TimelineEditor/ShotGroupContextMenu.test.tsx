// @vitest-environment jsdom
import { createRef } from 'react';
import { fireEvent, render } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { ShotGroupContextMenu } from './ShotGroupContextMenu.tsx';

describe('canonical shot media prerequisites', () => {
  it('explains an unavailable authored group and enables the same action after adoption', () => {
    const onSwitchToFinalVideo = vi.fn();
    const menu = { x: 0, y: 0, shotId: 'A', shotName: 'Shot', clipIds: ['a'], rowId: 'V1', trackId: 'V1', hasFinalVideo: true, hasStaleVideo: false, mode: 'images' as const,
      mediaSwitchUnavailableReason: 'Pin contiguous image clips and reload the accepted head.' };
    const props = { menu, menuRef: createRef<HTMLDivElement>(), closeMenu: vi.fn(), onSwitchToFinalVideo };
    const view = render(<ShotGroupContextMenu {...props} />);
    const action = view.getByRole('button', { name: 'Switch to Final Video' });
    expect(action).toBeDisabled();
    expect(view.getByText(menu.mediaSwitchUnavailableReason)).toBeVisible();
    fireEvent.click(action);
    expect(onSwitchToFinalVideo).not.toHaveBeenCalled();
    view.rerender(<ShotGroupContextMenu {...props} menu={{ ...menu, mediaSwitchUnavailableReason: undefined }} />);
    fireEvent.click(view.getByRole('button', { name: 'Switch to Final Video' }));
    expect(onSwitchToFinalVideo).toHaveBeenCalledOnce();
  });
});
