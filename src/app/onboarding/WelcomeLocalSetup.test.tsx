import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { ASTRID_COMMANDS, localSetupInstructions, localSetupSteps, LOCAL_SETUP } from '@/shared/components/RuntimeConnection/copy.ts';
import { WelcomeLocalSetup } from './WelcomeLocalSetup.tsx';

beforeEach(() => {
  cleanup();
  Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText: vi.fn().mockResolvedValue(undefined) } });
});
afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe('local setup card', () => {
  it('copies instructions and shows copied feedback', async () => {
    render(<WelcomeLocalSetup onBack={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Copy agent instructions' }));
    expect(await screen.findByRole('button', { name: 'Copied. Paste them into your agent.' })).toBeInTheDocument();
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith(localSetupInstructions());
  });

  it('keeps the instructions disclosure closed until opened', () => {
    render(<WelcomeLocalSetup onBack={vi.fn()} />);
    const instructionBlock = () => Array.from(document.querySelectorAll('pre')).find(pre => pre.textContent === localSetupInstructions());
    expect(instructionBlock()).toBeUndefined();
    expect(screen.getByText('Or do it yourself')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Show the instructions' }));
    expect(instructionBlock()?.textContent).toBe(localSetupInstructions());
    expect(screen.getByRole('button', { name: 'Hide the instructions' })).toBeInTheDocument();
  });

  it('shows five ordered macOS/Linux steps using commands from the shared setup source', () => {
    vi.spyOn(navigator, 'platform', 'get').mockReturnValue('MacIntel');
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Macintosh');
    render(<WelcomeLocalSetup onBack={vi.fn()} />);

    const list = screen.getByRole('list');
    expect(list.tagName).toBe('OL');
    expect(within(list).getAllByRole('listitem')).toHaveLength(5);
    expect(within(list).getAllByRole('listitem')[0]).toHaveTextContent('Install Astrid: in Terminal run');
    expect(localSetupSteps().map(step => step.command).filter(Boolean)).toEqual([
      ASTRID_COMMANDS.macLinux,
      [LOCAL_SETUP.cloneCommand, LOCAL_SETUP.changeDirectoryCommand, LOCAL_SETUP.installDependenciesCommand].join('\n'),
      LOCAL_SETUP.startCommand,
      LOCAL_SETUP.openUrl,
    ]);
    expect(list.querySelectorAll('pre code')).toHaveLength(4);
    expect(within(list).getAllByRole('listitem')[4]).toHaveTextContent('Open this address in your browser. The editor opens with your project.');
    expect(within(list).getAllByRole('listitem')[4].querySelectorAll('pre code')).toHaveLength(1);
    expect(within(list).getAllByRole('listitem')[4].querySelector('pre code')?.textContent).toBe(LOCAL_SETUP.openUrl);
    expect(screen.queryByRole('link', { name: LOCAL_SETUP.openUrl })).not.toBeInTheDocument();
    expect(screen.queryByText(/step 4 command/i)).not.toBeInTheDocument();
    expect(localSetupInstructions()).not.toMatch(/confirm it shows Connected|says Connected/i);
    expect(screen.queryByText('If pasting gives nothing, select the command and press Ctrl+C.')).not.toBeInTheDocument();
  });

  it('copies each command row exactly, including the three-line editor setup block', async () => {
    vi.spyOn(navigator, 'platform', 'get').mockReturnValue('MacIntel');
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Macintosh');
    render(<WelcomeLocalSetup onBack={vi.fn()} />);

    const labels = [
      'Copy the install command',
      'Copy the editor setup commands',
      'Copy the start command',
      'Copy the address',
    ];
    const commands = [
      ASTRID_COMMANDS.macLinux,
      [LOCAL_SETUP.cloneCommand, LOCAL_SETUP.changeDirectoryCommand, LOCAL_SETUP.installDependenciesCommand].join('\n'),
      LOCAL_SETUP.startCommand,
      LOCAL_SETUP.openUrl,
    ];

    for (let index = 0; index < labels.length; index += 1) {
      await act(async () => {
        fireEvent.click(screen.getByRole('button', { name: labels[index] }));
        await vi.waitFor(() => expect(navigator.clipboard.writeText).toHaveBeenCalledTimes(index + 1));
      });
      expect(navigator.clipboard.writeText).toHaveBeenNthCalledWith(index + 1, commands[index]);
    }
  });

  it('shows the PowerShell installer command and paste hint only on Windows', () => {
    vi.spyOn(navigator, 'platform', 'get').mockReturnValue('Win32');
    vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Windows');
    render(<WelcomeLocalSetup onBack={vi.fn()} />);

    const firstStep = within(screen.getByRole('list')).getAllByRole('listitem')[0];
    expect(firstStep).toHaveTextContent('Install Astrid: in PowerShell run');
    expect(firstStep.querySelector('pre code')?.textContent).toBe(ASTRID_COMMANDS.windows);
    expect(within(firstStep).getByText('If pasting gives nothing, select the command and press Ctrl+C.')).toBeInTheDocument();
  });

  it('calls onBack', () => {
    const onBack = vi.fn();
    render(<WelcomeLocalSetup onBack={onBack} />);
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(onBack).toHaveBeenCalledOnce();
  });
});
