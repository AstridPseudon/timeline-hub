import { describe, expect, it, vi } from 'vitest';
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';

import { DeclaredActionForm } from '@/tools/video-editor/components/AgentToolsPanel/DeclaredActionForm';
import {
  createDeclaredActionInitialValues,
  parseDeclaredActionDeclaration,
  validateDeclaredActionValues,
} from '@/tools/video-editor/data/declaredActionForm';
import type { RuntimeCapability } from '@/tools/video-editor/data/bridgeContract';

function chiptuneDeclaration() {
  return {
    kind: 'generator' as const,
    name: 'Chiptune Compose',
    short_description: 'Compose a short chiptune track.',
    description: 'Compose a tempo-locked NES-style cue.',
    keywords: ['music', 'chiptune'],
    invocation: {
      kind: 'command',
      command: { argv: ['{python_exec}', '-m', 'compose', '--out', '{out}'] },
    },
    inputs: [
      { name: 'duration_s', type: 'number', required: true, description: 'Exact cue length in seconds.' },
      { name: 'bpm', type: 'integer', required: false, default: 132, description: 'Tempo locked to the beat grid.' },
      { name: 'key', type: 'string', required: false, default: 'A minor', description: 'Tonic and mode.' },
      { name: 'seed', type: 'integer', required: false, default: 1, description: 'Seed for deterministic motifs.' },
      { name: 'sections', type: 'json', required: true, description: 'Array of cue sections.' },
      { name: 'hits', type: 'json', required: false, description: 'Accent times or hit objects.' },
      { name: 'duck', type: 'json', required: false, description: 'Explicit gain dips.' },
      { name: 'vo_mask', type: 'json', required: false, description: 'Speech spans to duck.' },
      { name: 'mutes', type: 'json', required: false, description: 'Hard-mute windows.' },
      { name: 'duck_db', type: 'number', required: false, default: -10, description: 'Gain applied under voice spans.' },
      { name: 'master_db', type: 'number', required: false, default: -16, description: 'RMS target in dBFS.' },
      { name: 'style', type: 'string', required: false, default: 'nes', description: 'Synthesis style.' },
    ],
    outputs: [
      {
        name: 'music', type: 'file', artifact_type: 'audio',
        description: '48 kHz stereo 16-bit WAV.', path_template: '$PATH/music.wav',
      },
      {
        name: 'beats', type: 'file', artifact_type: 'application/json',
        description: 'JSON beat, downbeat, bar and section data.', path_template: '$PATH/beats.json',
      },
    ],
  };
}

function runtimeProjection() {
  const source = chiptuneDeclaration();
  return {
    kind: source.kind,
    name: source.name,
    short_description: source.short_description,
    description: source.description,
    keywords: source.keywords,
    inputs: source.inputs,
    outputs: source.outputs.map(({ name, type, artifact_type, description }) => ({
      name, type, artifact_type, description,
    })),
  };
}

function capability(overrides: Partial<RuntimeCapability> = {}): RuntimeCapability {
  return {
    capability_id: 'chiptune.compose',
    definition_digest: `sha256:${'a'.repeat(64)}`,
    status: 'ready',
    required_resource_keys: [],
    estimated_scratch_bytes: 0,
    estimated_output_bytes: 0,
    ...overrides,
  };
}

describe('DeclaredActionForm', () => {
  it('derives supported controls, defaults and output descriptions from the V3 declaration', () => {
    const parsed = parseDeclaredActionDeclaration(chiptuneDeclaration());
    expect(parsed.ok).toBe(true);
    if (!parsed.ok) return;

    const defaults = createDeclaredActionInitialValues(parsed.declaration);
    expect(defaults).toMatchObject({
      duration_s: '',
      bpm: '132',
      key: 'A minor',
      seed: '1',
      sections: '',
      duck_db: '-10',
      master_db: '-16',
      style: 'nes',
    });

    render(
      <DeclaredActionForm
        actionId="chiptune.compose"
        capability={capability({ action_declaration: runtimeProjection() })}
      />,
    );

    expect(screen.getByLabelText(/duration_s/).getAttribute('required')).not.toBeNull();
    expect((screen.getByTestId('declared-action-input-bpm') as HTMLInputElement).value).toBe('132');
    expect(screen.getByText('Exact cue length in seconds.')).toBeTruthy();
    expect(screen.getByText('Tempo locked to the beat grid.')).toBeTruthy();
    expect(screen.getByText('generator')).toBeTruthy();
    expect(screen.getByText('Compose a short chiptune track.')).toBeTruthy();
    expect(screen.getByText('music')).toBeTruthy();
    expect(screen.getByText('beats')).toBeTruthy();
    expect(screen.getByText('48 kHz stereo 16-bit WAV.')).toBeTruthy();
    expect(screen.getByText('JSON beat, downbeat, bar and section data.')).toBeTruthy();
    expect(document.querySelector('[data-video-editor-declared-action-output="music"]')?.textContent)
      .toContain('audio');
    expect(document.querySelector('[data-video-editor-declared-action-output="beats"]')?.textContent)
      .toContain('application/json');
    expect(document.querySelector('input[name="out"]')).toBeNull();
    expect(document.body.textContent).not.toContain('$PATH');
    expect(document.body.textContent).not.toContain('path_template');
    expect(document.body.textContent).not.toContain('music.wav');
  });

  it('validates required and typed inputs, then refuses before task admission on this unsupported host', () => {
    const parsed = parseDeclaredActionDeclaration(chiptuneDeclaration());
    expect(parsed.ok).toBe(true);
    if (!parsed.ok) return;

    const invalid = validateDeclaredActionValues(parsed.declaration, {
      duration_s: '',
      sections: '{bad json',
    });
    expect(invalid).toEqual({
      ok: false,
      errors: {
        duration_s: 'duration_s is required.',
        sections: 'sections must be valid JSON.',
      },
    });
    expect(validateDeclaredActionValues(parsed.declaration, {
      duration_s: '4.5',
      bpm: '132.5',
      sections: '[]',
    })).toMatchObject({ ok: false, errors: { bpm: 'bpm must be a whole number.' } });

    render(
      <DeclaredActionForm
        actionId="chiptune.compose"
        capability={capability({ action_declaration: runtimeProjection() })}
      />,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Run action' }));
    expect(screen.getByText('duration_s is required.')).toBeTruthy();
    expect(screen.getByText('sections is required.')).toBeTruthy();

    fireEvent.change(screen.getByTestId('declared-action-input-duration_s'), { target: { value: '4.5' } });
    fireEvent.change(screen.getByTestId('declared-action-input-sections'), { target: { value: '[]' } });
    fireEvent.click(screen.getByRole('button', { name: 'Run action' }));

    expect(screen.getByText(/no source-backed mapping .* task admission spec and managed project-media result path/i))
      .toBeTruthy();
    expect(document.querySelector('[data-video-editor-declared-action-code="action-host-unsupported"]'))
      .toBeTruthy();
  });

  it('passes the selected ready capability and typed action values to the host exactly once', async () => {
    const selectedCapability = capability({ action_declaration: runtimeProjection() });
    let resolveTask: ((result: { task_id: string; status: string }) => void) | undefined;
    const onRunAction = vi.fn(() => new Promise<{ task_id: string; status: string }>((resolve) => {
      resolveTask = resolve;
    }));
    render(
      <DeclaredActionForm
        actionId="chiptune.compose"
        capability={selectedCapability}
        onRunAction={onRunAction}
      />,
    );

    fireEvent.change(screen.getByTestId('declared-action-input-duration_s'), { target: { value: '4.5' } });
    fireEvent.change(screen.getByTestId('declared-action-input-sections'), {
      target: { value: '[{"start_s":0,"end_s":4.5,"energy":0.4,"mood":"bright"}]' },
    });
    const form = screen.getByRole('button', { name: 'Run action' }).closest('form');
    if (!form) throw new Error('Declared action form was not rendered.');
    fireEvent.submit(form);
    fireEvent.submit(form);

    expect(onRunAction).toHaveBeenCalledTimes(1);
    resolveTask?.({ task_id: 'host-task-17', status: 'queued' });
    await screen.findByText('Task host-task-17 submitted (queued).');
    expect(onRunAction).toHaveBeenCalledTimes(1);
    expect(onRunAction.mock.calls[0]?.[0]).toBe(selectedCapability);
    expect(onRunAction.mock.calls[0]?.[1]).toEqual({
      duration_s: 4.5,
      bpm: 132,
      key: 'A minor',
      seed: 1,
      sections: [{ start_s: 0, end_s: 4.5, energy: 0.4, mood: 'bright' }],
      duck_db: -10,
      master_db: -16,
      style: 'nes',
    });
  });

  it('refuses missing and invalid values before invoking an available callback', () => {
    const onRunAction = vi.fn(async () => ({ task_id: 'must-not-exist', status: 'queued' }));
    render(
      <DeclaredActionForm
        actionId="chiptune.compose"
        capability={capability({ action_declaration: runtimeProjection() })}
        onRunAction={onRunAction}
      />,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Run action' }));
    expect(screen.getByText('duration_s is required.')).toBeTruthy();
    expect(screen.getByText('sections is required.')).toBeTruthy();
    expect(onRunAction).not.toHaveBeenCalled();

    fireEvent.change(screen.getByTestId('declared-action-input-duration_s'), { target: { value: '4.5' } });
    fireEvent.change(screen.getByTestId('declared-action-input-sections'), { target: { value: '{bad json' } });
    fireEvent.click(screen.getByRole('button', { name: 'Run action' }));
    expect(screen.getByText('sections must be valid JSON.')).toBeTruthy();
    expect(onRunAction).not.toHaveBeenCalled();
  });

  it('reports host callback errors without inventing a task handle', async () => {
    const onRunAction = vi.fn(async () => { throw new Error('Runtime bridge refused admission.'); });
    render(
      <DeclaredActionForm
        actionId="chiptune.compose"
        capability={capability({ action_declaration: runtimeProjection() })}
        onRunAction={onRunAction}
      />,
    );
    fireEvent.change(screen.getByTestId('declared-action-input-duration_s'), { target: { value: '4.5' } });
    fireEvent.change(screen.getByTestId('declared-action-input-sections'), { target: { value: '[]' } });
    fireEvent.click(screen.getByRole('button', { name: 'Run action' }));

    await waitFor(() => expect(screen.getByRole('alert').textContent).toBe('Runtime bridge refused admission.'));
    expect(onRunAction).toHaveBeenCalledTimes(1);
    expect(document.querySelector('[data-video-editor-declared-action-task-id]')).toBeNull();
  });

  it('does not display a late host response after the selected capability identity changes', async () => {
    let resolveTask: ((result: { task_id: string; status: string }) => void) | undefined;
    const onRunAction = vi.fn(() => new Promise<{ task_id: string; status: string }>((resolve) => {
      resolveTask = resolve;
    }));
    const { rerender } = render(
      <DeclaredActionForm
        actionId="chiptune.compose"
        capability={capability({ action_declaration: runtimeProjection() })}
        onRunAction={onRunAction}
      />,
    );
    fireEvent.change(screen.getByTestId('declared-action-input-duration_s'), { target: { value: '4.5' } });
    fireEvent.change(screen.getByTestId('declared-action-input-sections'), { target: { value: '[]' } });
    fireEvent.click(screen.getByRole('button', { name: 'Run action' }));
    expect(onRunAction).toHaveBeenCalledTimes(1);

    rerender(
      <DeclaredActionForm
        actionId="chiptune.compose"
        capability={capability({ capability_id: 'another.action', action_declaration: runtimeProjection() })}
        onRunAction={onRunAction}
      />,
    );
    await act(async () => {
      resolveTask?.({ task_id: 'stale-host-task', status: 'queued' });
      await Promise.resolve();
    });

    expect(document.querySelector('[data-video-editor-declared-action-task-id]')).toBeNull();
    expect(screen.getByText(/Runtime returned another.action for action chiptune.compose/i)).toBeTruthy();
  });

  it('shows a typed unavailable result for the current metadata-only catalog item', () => {
    render(
      <DeclaredActionForm
        actionId="chiptune.compose"
        capability={capability()}
      />,
    );

    expect(document.querySelector('[data-video-editor-declared-action-code="action-declaration-unavailable"]'))
      .toBeTruthy();
    expect(screen.getByText(/catalog entry contains summary metadata only/i)).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Run action' })).toBeNull();
  });

  it('refuses a declaration projected from a different capability identity', () => {
    const onRunAction = vi.fn(async () => ({ task_id: 'must-not-exist', status: 'queued' }));
    render(<DeclaredActionForm
      actionId="chiptune.compose"
      capability={capability({
        capability_id: 'another.action',
        action_declaration: runtimeProjection(),
      })}
      onRunAction={onRunAction}
    />);

    expect(document.querySelector('[data-video-editor-declared-action-code="capability-mismatch"]'))
      .toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Run action' })).toBeNull();
    expect(onRunAction).not.toHaveBeenCalled();
  });

  it('rejects declarations containing unsupported input types instead of guessing a control', () => {
    const result = parseDeclaredActionDeclaration({
      inputs: [{ name: 'file', type: 'file', required: true }],
      outputs: [],
    });
    expect(result).toMatchObject({ ok: false, code: 'unsupported-input-type' });

    const outputRouting = parseDeclaredActionDeclaration({
      inputs: [{ name: 'out', type: 'string', required: false }],
      outputs: [],
    });
    expect(outputRouting).toMatchObject({ ok: false, code: 'host-owned-output-input' });
  });
});
