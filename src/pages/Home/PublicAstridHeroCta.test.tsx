// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { PublicAstridHeroCta } from './PublicAstridHeroCta';

describe('PublicAstridHeroCta', () => {
  beforeEach(() => {
    Object.defineProperty(navigator, 'userAgent', { value: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36', configurable: true });
    Object.defineProperty(navigator, 'platform', { value: 'MacIntel', configurable: true });
    window.matchMedia = vi.fn().mockImplementation((media: string) => ({ media, matches: false, addEventListener: vi.fn(), removeEventListener: vi.fn(), addListener: vi.fn(), removeListener: vi.fn() }));
    Object.defineProperty(HTMLDialogElement.prototype, 'showModal', { configurable: true, value: vi.fn(function (this: HTMLDialogElement) { this.open = true; }) });
    Object.defineProperty(HTMLDialogElement.prototype, 'close', { configurable: true, value: vi.fn(function (this: HTMLDialogElement) { this.open = false; }) });
  });

  afterEach(() => {
    cleanup();
  });

  it('opens on the app step, then shows the shared OS installer line in step 2', () => {
    render(<PublicAstridHeroCta active />);
    fireEvent.click(screen.getByRole('button', { name: 'Set up Astrid' }));
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Get the Astrid app' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Use it in the browser' }));
    expect(screen.getByRole('button', { name: 'Copy agent instructions' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Copy command' })).toBeInTheDocument();
    expect(screen.getByText(/curl -fsSL https:\/\/astrid\.haus\/install \| sh/)).toBeInTheDocument();
    expect(screen.queryByText('Add a browser shortcut')).not.toBeInTheDocument();
  });
});
