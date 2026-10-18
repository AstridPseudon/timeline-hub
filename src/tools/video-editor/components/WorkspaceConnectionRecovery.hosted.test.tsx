// @vitest-environment jsdom
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';

let origin = '';
vi.mock('@/integrations/runtime/connection.ts', () => ({ runtimeOrigin: () => origin }));

import { WorkspaceConnectionRecovery } from './WorkspaceConnectionRecovery';

afterEach(() => {
  origin = '';
  cleanup();
});

const recovery = () => render(
  <WorkspaceConnectionRecovery retrying={false} error="Connection refused." connectionUrl="https://astrid.haus" onRetry={vi.fn()} />,
);

describe('WorkspaceConnectionRecovery on the hosted build', () => {
  it('never renders: the connection panel and the Astrid cards cover every case, so two recovery paths never compete', () => {
    origin = 'http://127.0.0.1:17340';
    const { container } = recovery();

    expect(container).toBeEmptyDOMElement();
    expect(screen.queryByText('Workspace connection unavailable')).toBeNull();
    expect(screen.queryByText('Show full connection error')).toBeNull();
    expect(screen.queryByText(/Configured editor origin/)).toBeNull();
    expect(screen.queryByRole('button', { name: 'Give restart instructions to my agent' })).toBeNull();
    expect(screen.queryByRole('button', { name: /restart it myself/i })).toBeNull();
  });

  it('is unchanged same-origin', () => {
    origin = '';
    recovery();
    expect(screen.getByRole('heading', { name: 'Workspace connection unavailable' })).toBeInTheDocument();
  });
});
