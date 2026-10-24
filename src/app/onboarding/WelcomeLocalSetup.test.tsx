import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { localSetupInstructions } from '@/shared/components/RuntimeConnection/copy.ts';
import { WelcomeLocalSetup } from './WelcomeLocalSetup.tsx';

beforeEach(() => {
  cleanup();
  Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText: vi.fn().mockResolvedValue(undefined) } });
});
afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe('local setup card', () => {
  it('copies instructions and shows copied feedback', async () => {
    render(<WelcomeLocalSetup onBack={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Copy instructions' }));
    expect(await screen.findByRole('button', { name: 'Copied. Paste them into your agent.' })).toBeInTheDocument();
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith(localSetupInstructions());
  });

  it('keeps the instructions disclosure closed until opened', () => {
    render(<WelcomeLocalSetup onBack={vi.fn()} />);
    expect(document.querySelector('pre')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Show the instructions' }));
    expect(document.querySelector('pre')?.textContent).toBe(localSetupInstructions());
    expect(screen.getByRole('button', { name: 'Hide the instructions' })).toBeInTheDocument();
  });

  it('calls onBack', () => {
    const onBack = vi.fn();
    render(<WelcomeLocalSetup onBack={onBack} />);
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(onBack).toHaveBeenCalledOnce();
  });
});
