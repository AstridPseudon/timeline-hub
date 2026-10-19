// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { PublicAstridHeroCta } from './PublicAstridHeroCta';

describe('PublicAstridHeroCta', () => {
  beforeEach(() => {
    window.matchMedia = vi.fn().mockImplementation((media: string) => ({ media, matches: false, addEventListener: vi.fn(), removeEventListener: vi.fn(), addListener: vi.fn(), removeListener: vi.fn() }));
    Object.defineProperty(HTMLDialogElement.prototype, 'showModal', { configurable: true, value: vi.fn(function (this: HTMLDialogElement) { this.open = true; }) });
    Object.defineProperty(HTMLDialogElement.prototype, 'close', { configurable: true, value: vi.fn(function (this: HTMLDialogElement) { this.open = false; }) });
  });

  afterEach(() => {
    cleanup();
  });

  it.each(['app', 'agent'] as const)('%s audience opens the shared OS installer line', (audience) => {
    render(<PublicAstridHeroCta audience={audience} active />);
    fireEvent.click(screen.getByRole('button', { name: 'Set up Astrid' }));
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Copy' })).toBeInTheDocument();
    expect(screen.getByText(/curl -fsSL https:\/\/astrid\.haus\/install \| sh/)).toBeInTheDocument();
    expect(screen.getByText('Add a browser shortcut')).toBeInTheDocument();
  });
});
