// @vitest-environment jsdom
import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';
import { PublicAstridHeroCta } from './PublicAstridHeroCta';

describe('PublicAstridHeroCta', () => {
  afterEach(cleanup);

  it('offers a single Get Started link to the welcome', () => {
    render(<PublicAstridHeroCta active />);
    expect(screen.getByRole('link', { name: 'Get Started' })).toHaveAttribute('href', '/tools/video-editor');
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
