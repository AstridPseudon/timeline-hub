import { afterEach, describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { RUNTIME_CONNECTION_COPY } from '@/shared/components/RuntimeConnection/copy.ts';
import { setRuntimeAppUrl } from '@/integrations/runtime/runtimeAppUrl.ts';

let origin = '';
vi.mock('@/integrations/runtime/connection.ts', () => ({ runtimeOrigin: () => origin }));

import { GenerateControls } from './GenerateControls';

function renderControls() {
  return render(
    <GenerateControls
      imagesPerPrompt={2}
      onChangeImagesPerPrompt={vi.fn()}
      actionablePromptsCount={1}
      isGenerating={false}
      justQueued={false}
      promptMode="managed"
    />,
  );
}

afterEach(() => setRuntimeAppUrl(null));

describe('GenerateControls on the hosted build', () => {
  it('follows the compose line with an "Open it" link to the local app, without showing its address', () => {
    origin = 'http://127.0.0.1:17340';
    setRuntimeAppUrl('http://127.0.0.1:2222');
    renderControls();

    expect(screen.getByText('Making new images works in Astrid on your computer for now.')).toBeInTheDocument();
    const link = screen.getByRole('link', { name: 'Open it' });
    expect(link).toHaveAttribute('href', 'http://127.0.0.1:2222');
    expect(screen.getByRole('note').textContent).not.toContain('127.0.0.1');
  });

  it('renders no link when the gateway did not report the app address', () => {
    origin = 'http://127.0.0.1:17340';
    renderControls();

    expect(screen.getByText(RUNTIME_CONNECTION_COPY.composeDisabled)).toBeInTheDocument();
    expect(screen.queryByRole('link')).toBeNull();
  });

  it('with the gateway origin, disables the submit button and shows the compose line', () => {
    origin = 'http://127.0.0.1:17340';
    renderControls();

    expect(screen.getByRole('button', { name: /Generate/ })).toBeDisabled();
    expect(screen.getByText(RUNTIME_CONNECTION_COPY.composeDisabled)).toBeInTheDocument();
  });

  it('same-origin is unchanged: the button is enabled and no line shows', () => {
    origin = '';
    renderControls();

    expect(screen.getByRole('button', { name: /Generate/ })).toBeEnabled();
    expect(screen.queryByText(RUNTIME_CONNECTION_COPY.composeDisabled)).toBeNull();
  });
});
