// @vitest-environment jsdom
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';

let origin = '';
vi.mock('@/integrations/runtime/connection.ts', () => ({ runtimeOrigin: () => origin }));

import { TimelineLoadErrorCard } from './TimelineLoadErrorCard.tsx';

const ENGINEER_WORDS = /Reigh|Runtime|workspace|realm|gateway|127\.0\.0\.1|npm run/i;
const ENGINEER_MESSAGE = 'Workspace Runtime is unavailable at http://127.0.0.1:17340/api/runtime: http_error: HTTP 503. Start the supported Runtime and configure its authenticated connector, then retry.';

afterEach(() => {
  origin = '';
  cleanup();
});

describe('TimelineLoadErrorCard on the hosted build', () => {
  it('never prints the error message: one friendly line and Try again', () => {
    origin = 'http://127.0.0.1:17340';
    const onRetry = vi.fn();
    render(<TimelineLoadErrorCard message={ENGINEER_MESSAGE} onRetry={onRetry} />);

    const alert = screen.getByRole('alert');
    expect(alert).toHaveTextContent("Couldn't load this timeline");
    expect(alert).toHaveTextContent("Astrid on this computer didn't answer. Start it and try again.");
    expect(document.body.textContent).not.toMatch(ENGINEER_WORDS);
    expect(document.body.textContent).not.toMatch(/toolbar/);

    fireEvent.click(screen.getByRole('button', { name: 'Try again' }));
    expect(onRetry).toHaveBeenCalledTimes(1);
  });

  it('is unchanged same-origin', () => {
    origin = '';
    render(<TimelineLoadErrorCard message="bridge unreachable" onRetry={vi.fn()} />);
    expect(screen.getByRole('alert')).toHaveTextContent('Unable to load this timeline');
    expect(screen.getByRole('alert')).toHaveTextContent('bridge unreachable');
  });
});
