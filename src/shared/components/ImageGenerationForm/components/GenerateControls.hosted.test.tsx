import { describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { RUNTIME_CONNECTION_COPY } from '@/shared/components/RuntimeConnection/copy.ts';

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

describe('GenerateControls on the hosted build', () => {
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
