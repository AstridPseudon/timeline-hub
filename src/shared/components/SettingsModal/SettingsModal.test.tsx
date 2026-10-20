// @vitest-environment jsdom
import { fireEvent, render, screen, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { SCHEMA_DIGEST } from '@/integrations/runtime/generated-contract-metadata.ts';
import { RUNTIME_CONNECTION_COPY as COPY, withBrowser } from '@/shared/components/RuntimeConnection/copy.ts';

const { connectionMock } = vi.hoisted(() => ({ connectionMock: { value: null as unknown } }));

vi.mock('@/integrations/runtime/RuntimeConnectionProvider.tsx', () => ({
  useRuntimeConnection: () => connectionMock.value,
}));
vi.mock('@/shared/hooks/mobile', () => ({ useIsMobile: () => false }));
vi.mock('@/shared/hooks/useModal', () => ({
  useLargeModal: () => ({
    className: '', style: {}, isMobile: false, headerClass: '', scrollClass: '', footerClass: '',
  }),
}));
vi.mock('@/shared/hooks/useScrollFade', () => ({ useScrollFade: () => ({ showFade: false, scrollRef: { current: null } }) }));
vi.mock('@/shared/contexts/AIInputModeContext', () => ({ useAIInputMode: () => ({ mode: 'text', setMode: vi.fn() }) }));
vi.mock('@/integrations/supabase/client', () => ({ getSupabaseClient: () => ({ auth: { signOut: vi.fn() } }) }));
vi.mock('./sections/PreferencesSection', () => ({ PreferencesSection: () => <div>Preferences</div> }));

import { SettingsModal } from './SettingsModal';

type Status = 'connected' | 'connecting' | 'blocked' | 'not_running';

function connection(status: Status, overrides: Record<string, unknown> = {}) {
  const state = status === 'connected'
    ? { status, realm: { realm_id: 'realm-1', display_name: 'My Studio' } }
    : { status };
  return {
    gated: true,
    state,
    isConnected: status === 'connected',
    isBooting: false,
    isChecking: false,
    awaitingConnect: false,
    realmName: status === 'connected' ? 'My Studio' : null,
    schemaDigest: status === 'connected' ? SCHEMA_DIGEST : null,
    connect: vi.fn(),
    ...overrides,
  };
}

function renderSettings() {
  render(
    <SettingsModal
      isOpen
      onOpenChange={vi.fn()}
      preserveUserText={false}
      setPreserveUserText={vi.fn()}
    />,
  );
  return screen.getByRole('region', { name: 'Connection' });
}

beforeEach(() => {
  connectionMock.value = connection('connected');
});

describe('SettingsModal connection', () => {
  it('says it is connected, names the workspace and shows the Runtime and Workspace marks only', () => {
    const section = renderSettings();

    expect(within(section).getByRole('status')).toHaveTextContent(COPY.connected.sentence);
    expect(within(section).getByText('Workspace: My Studio')).toBeTruthy();
    expect(within(section).getByText('Runtime')).toHaveAttribute('data-state', 'pass');
    expect(within(section).getByText('Workspace')).toHaveAttribute('data-state', 'pass');
    expect(within(section).queryByText('Tools')).toBeNull();
    expect(within(section).queryByText(COPY.updateNeeded.title)).toBeNull();
  });

  it('leads with the update when Astrid on this computer speaks another schema', () => {
    connectionMock.value = connection('connected', { schemaDigest: 'sha256:older-runtime' });
    const section = renderSettings();

    expect(within(section).getByRole('status')).toHaveTextContent(COPY.updateNeeded.title);
    expect(within(section).getByText(COPY.updateNeeded.sentence)).toBeTruthy();
    expect(within(section).queryByText(COPY.connected.sentence)).toBeNull();
  });

  it('gives the not-running step while the marks keep looking', () => {
    connectionMock.value = connection('not_running');
    const section = renderSettings();

    expect(within(section).getByRole('status')).toHaveTextContent(COPY.notRunning.title);
    expect(within(section).getByText(COPY.notRunning.sentence)).toBeTruthy();
    for (const name of ['Runtime', 'Workspace']) {
      expect(within(section).getByText(name)).toHaveAttribute('data-state', 'checking');
    }
  });

  it('offers Connect while the browser has not been asked, and nothing else checks then', () => {
    const value = connection('connecting', { awaitingConnect: true });
    connectionMock.value = value;
    const section = renderSettings();

    expect(within(section).getByRole('status')).toHaveTextContent(withBrowser(COPY.permission.title));
    expect(within(section).queryByText('Runtime')).toBeNull();
    fireEvent.click(within(section).getByRole('button', { name: COPY.permission.connect }));
    expect(value.connect).toHaveBeenCalledTimes(1);
  });

  it('gives the browser steps when it blocks this page', () => {
    connectionMock.value = connection('blocked');
    const section = renderSettings();

    expect(within(section).getByRole('status')).toHaveTextContent(withBrowser(COPY.blocked.title));
    expect(within(section).getByText(COPY.blocked.steps.join(' '))).toBeTruthy();
    expect(within(section).queryByRole('button')).toBeNull();
  });
});
