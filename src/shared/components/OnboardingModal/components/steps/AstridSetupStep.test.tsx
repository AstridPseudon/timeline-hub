import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { AstridCapabilityCensus } from '@/integrations/astrid/capabilityCensus.ts';

const { inspectMock } = vi.hoisted(() => ({ inspectMock: vi.fn() }));
vi.mock('@/integrations/astrid/capabilityCensus.ts', () => ({ inspectAstridCapabilities: inspectMock }));

import userEvent from '@testing-library/user-event';
import { OnboardingModal } from '@/shared/components/modals/OnboardingModal';
import type { ReactElement } from 'react';
import { Dialog, DialogContent } from '@/shared/components/ui/dialog';
import { AstridSetupStep, resetSetupChecksForTests, setupChecksFrom } from './AstridSetupStep';
import { LOCAL_AGENT_SETTING_KEY, savedLocalAgent } from '@/integrations/astrid/localAgents.ts';

const renderInDialog = (ui: ReactElement) => render(<Dialog open><DialogContent>{ui}</DialogContent></Dialog>);
import { AGENT_SETUP_BRIEF, ASTRID_LAUNCH_COMMANDS, ASTRID_STUDIO_MESSAGE, MANUAL_SETUP_STEPS, RECONNECT_COMMANDS } from '@/shared/components/OnboardingModal/lib/astridSetupGuide';

const down: AstridCapabilityCensus = {
  health: 'unavailable', readiness: 'unavailable', projectSlug: null,
  capabilities: { tasks: 'unknown', generations: 'unknown', media: 'unknown' },
  reasons: { health: 'bridge health unavailable' },
};
const freshWorkspace: AstridCapabilityCensus = {
  health: 'available', readiness: 'degraded', projectSlug: null,
  capabilities: { tasks: 'unknown', generations: 'unknown', media: 'unknown' },
  reasons: { projects: 'No project exists yet; project-scoped capabilities were not probed.' },
};
const ready: AstridCapabilityCensus = {
  health: 'available', readiness: 'ready', projectSlug: 'demo',
  capabilities: { tasks: 'supported', generations: 'supported', media: 'supported' },
  reasons: {},
};

describe('setupChecksFrom', () => {
  it('is not ready while the Runtime is down', () => {
    expect(setupChecksFrom(down)).toMatchObject({ runtime: 'fail', workspace: 'fail', ready: false });
  });

  it('counts a brand-new workspace with no projects as set up, checking tools later', () => {
    expect(setupChecksFrom(freshWorkspace)).toMatchObject({ runtime: 'pass', workspace: 'pass', tools: 'later', ready: true });
  });

  it('does not count an unreadable workspace as set up', () => {
    const broken = { ...freshWorkspace, reasons: { projects: 'Astrid bridge request failed: 500' } };
    expect(setupChecksFrom(broken)).toMatchObject({ runtime: 'pass', workspace: 'fail', ready: false });
  });

  it('passes every check on a working install with a project', () => {
    expect(setupChecksFrom(ready)).toMatchObject({ runtime: 'pass', workspace: 'pass', tools: 'pass', ready: true });
  });
});

describe('AstridSetupStep', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    resetSetupChecksForTests();
    localStorage.removeItem(LOCAL_AGENT_SETTING_KEY);
  });

  it('guides the agent through choosing and saving Astrid’s model', () => {
    expect(AGENT_SETUP_BRIEF).toContain(`FINALLY: CHOOSE YOUR MODEL AND HAND OVER TO ASTRID
Astrid has its own agent (the astrid command, running on oh-my-pi). Make sure the command is installed; install any missing requirements.

1. Run astrid agent models --json. Show me the saved current default, signed-in model choices, and providers that need sign-in. Ask which exact PROVIDER/MODEL I want to use.
2. If my chosen provider needs sign-in, have me run astrid --onboard locally and choose the provider by its exact displayed name. If onboarding is unavailable, have me run omp, then /login, and pick that same name. Use OMP's own sign-in; never read, copy, or forward credential files or tokens from another agent, including ~/.codex/auth.json.
3. Run astrid agent use PROVIDER/MODEL with my choice, then astrid agent models to verify the saved default. This persists OMP's modelRoles.default for new App and terminal chats using this OMP profile. Existing chats and explicit project defaults can retain their own model.

Tell me I can later ask Astrid "Which models can you use?" or "Switch to PROVIDER/MODEL." After a billing, authentication, or quota error, Astrid should list signed-in alternatives and offer to switch.

Don't set up generation (GPU, models, API keys, workflows) yourself: Astrid does that with me.`);
    expect(AGENT_SETUP_BRIEF).toContain('1. Inside an agent I already use, like you: through the Astrid skill you installed, I can just ask for Astrid there.');
    expect(AGENT_SETUP_BRIEF).toContain("2. In Astrid's own dedicated agent: run astrid in a terminal.");
  });

  it('opens the modal on its content and lets Tab reach the selected setup option', async () => {
    inspectMock.mockResolvedValue(down);
    const user = userEvent.setup();
    render(<OnboardingModal isOpen onClose={vi.fn()} />);
    const agentOption = await screen.findByRole('radio', { name: 'Claude Code' });
    await waitFor(() => {
      expect(document.activeElement).toContainElement(screen.getByRole('heading', { name: 'Set up Astrid' }));
      expect(agentOption).not.toHaveFocus();
    });
    await user.tab();
    expect(agentOption).toHaveFocus();
  });

  it('keeps the shared Runtime, Workspace and Tools rows in onboarding', async () => {
    inspectMock.mockResolvedValue(ready);
    render(<OnboardingModal isOpen onClose={vi.fn()} />);
    const runtime = await screen.findByText('Runtime');
    expect(runtime).toHaveAttribute('data-state', 'pass');
    expect(screen.getByText('Workspace')).toHaveAttribute('data-state', 'pass');
    expect(screen.getByText('Tools')).toHaveAttribute('data-state', 'pass');
  });

  it('offers the agent brief verbatim and copies it whole', async () => {
    inspectMock.mockResolvedValue(down);
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    renderInDialog(<AstridSetupStep onNext={vi.fn()} onClose={vi.fn()} />);
    await act(async () => {});

    expect(screen.getByRole('note').textContent).toMatch(/requires a GPU/i);
    expect(screen.getByRole('note').textContent).toMatch(/technically use APIs/i);
    fireEvent.click(screen.getByRole('button', { name: /copy brief/i }));
    await act(async () => {});
    expect(writeText).toHaveBeenCalledWith(AGENT_SETUP_BRIEF);
  });

  it.each([
    ['Claude Code', 'claude-code'],
    ['Codex', 'codex'],
    ['Hermes', 'hermes'],
  ] as const)('saves %s and offers a brief addressed to it', async (name, id) => {
    inspectMock.mockResolvedValue(down);
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    renderInDialog(<AstridSetupStep onNext={vi.fn()} onClose={vi.fn()} />);
    await act(async () => {});

    expect(screen.getByText('Already use an agent?')).toBeTruthy();
    expect(screen.getByRole('radiogroup', { name: 'Already use an agent?' })).toBeTruthy();
    fireEvent.click(screen.getByRole('radio', { name }));
    expect(savedLocalAgent()).toBe(id);
    expect(screen.getByText(`Paste this into ${name}`)).toBeTruthy();
    const tailoredLine = `I'll use Astrid from ${name}, so sync Astrid's skills into ${name}.`;
    expect(screen.getByText((_, element) => element?.tagName === 'PRE' && element.textContent?.includes(tailoredLine))).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: /copy brief/i }));
    await act(async () => {});
    expect(writeText).toHaveBeenCalledWith(expect.stringContaining(tailoredLine));
  });

  it('maps None yet to Astrid and selects the manual setup route', async () => {
    inspectMock.mockResolvedValue(down);
    renderInDialog(<AstridSetupStep onNext={vi.fn()} onClose={vi.fn()} />);
    await act(async () => {});
    fireEvent.click(screen.getByRole('radio', { name: 'None yet' }));
    expect(savedLocalAgent()).toBe('astrid');
    expect(screen.getByRole('radio', { name: 'I’ll set it up myself' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByText(/check what you already have/i)).toBeTruthy();
  });

  it('leaves the existing default untouched when no agent is selected', async () => {
    inspectMock.mockResolvedValue(down);
    localStorage.setItem(LOCAL_AGENT_SETTING_KEY, 'codex');
    renderInDialog(<AstridSetupStep onNext={vi.fn()} onClose={vi.fn()} />);
    await act(async () => {});

    expect(savedLocalAgent()).toBe('codex');
    expect(screen.getByText('Brief for your agent to set everything up')).toBeTruthy();
  });

  it('lists the manual steps when the person sets it up themselves', async () => {
    inspectMock.mockResolvedValue(down);
    renderInDialog(<AstridSetupStep onNext={vi.fn()} onClose={vi.fn()} />);
    await act(async () => {});

    fireEvent.click(screen.getByText(/set it up myself/i));
    for (const step of MANUAL_SETUP_STEPS.unix) expect(screen.getByText(step.title)).toBeTruthy();
    expect(screen.getByText(/check what you already have/i)).toBeTruthy();

    fireEvent.click(screen.getByText('Windows'));
    expect(screen.getByText(/open powershell/i)).toBeTruthy();
    expect(screen.getByText(/not yet validated on windows/i)).toBeTruthy();
  });

  it('says you are set up once the Runtime responds, and continues', async () => {
    inspectMock.mockResolvedValue(freshWorkspace);
    const onNext = vi.fn();
    renderInDialog(<AstridSetupStep onNext={onNext} onClose={vi.fn()} />);
    await act(async () => {});

    fireEvent.click(screen.getByRole('radio', { name: 'Hermes' }));
    expect(savedLocalAgent()).toBe('hermes');
    fireEvent.click(screen.getByRole('button', { name: /continue/i }));
    expect(onNext).toHaveBeenCalled();
  });

  it('once set up, hands over to Astrid with a message to paste in', async () => {
    inspectMock.mockResolvedValue(freshWorkspace);
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    renderInDialog(<AstridSetupStep onNext={vi.fn()} onClose={vi.fn()} />);
    await act(async () => {});

    expect(screen.getByText(/set up your studio with astrid/i)).toBeTruthy();
    expect(screen.getByText((_, element) => element?.tagName === 'PRE' && element.textContent === ASTRID_LAUNCH_COMMANDS.unix)).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: /copy message/i }));
    await act(async () => {});
    expect(writeText).toHaveBeenCalledWith(ASTRID_STUDIO_MESSAGE);
  });

  it('shows a set-up install how to start its Runtime again', async () => {
    inspectMock.mockResolvedValue(down);
    renderInDialog(<AstridSetupStep reconnect onNext={vi.fn()} onClose={vi.fn()} />);
    await act(async () => {});

    expect(screen.getByText(RECONNECT_COMMANDS.unix)).toBeTruthy();
  });

  it('returns directly to Astrid when a reconnecting Runtime becomes ready', async () => {
    inspectMock.mockResolvedValue(ready);
    const onNext = vi.fn();
    renderInDialog(<AstridSetupStep reconnect onNext={onNext} onClose={vi.fn()} />);

    await waitFor(() => expect(onNext).toHaveBeenCalledTimes(1));
  });
});
