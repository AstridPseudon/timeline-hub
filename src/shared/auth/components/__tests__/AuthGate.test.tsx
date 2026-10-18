// @vitest-environment jsdom
import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { connectionFor } from '@/shared/components/RuntimeConnection/connectionFixture';
import { AuthGate } from '../AuthGate';

const auth = vi.hoisted(() => ({ isLoading: false }));
const connectionRef = vi.hoisted(() => ({ value: undefined as unknown }));

vi.mock('@/shared/contexts/AuthContext', () => ({ useAuth: () => ({ userId: null, isAuthenticated: false, isLoading: auth.isLoading }) }));
vi.mock('@/integrations/runtime/RuntimeConnectionProvider', () => ({ useRuntimeConnection: () => connectionRef.value }));

afterEach(cleanup);

describe('AuthGate', () => {
  it('exports component', () => {
    expect(AuthGate).toBeDefined();
  });

  it('hosted build, still booting: shows the connecting state, not a blank page', () => {
    auth.isLoading = true;
    connectionRef.value = connectionFor({ status: 'connecting' }, { isBooting: true });
    render(<AuthGate><p>app</p></AuthGate>);

    expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'connecting');
    expect(screen.queryByText('app')).not.toBeInTheDocument();
  });

  it('same-origin build, still loading: renders nothing', () => {
    auth.isLoading = true;
    connectionRef.value = connectionFor({ status: 'connecting' }, { gated: false });
    const { container } = render(<AuthGate><p>app</p></AuthGate>);

    expect(container).toBeEmptyDOMElement();
  });

  it('renders its children once loaded', () => {
    auth.isLoading = false;
    connectionRef.value = connectionFor({ status: 'connecting' });
    render(<AuthGate><p>app</p></AuthGate>);

    expect(screen.getByText('app')).toBeInTheDocument();
  });
});
