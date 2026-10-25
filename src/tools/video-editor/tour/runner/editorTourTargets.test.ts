import { describe, expect, it } from 'vitest';
import { editorTourTargets } from './EditorTourRunner';

describe('editorTourTargets', () => {
  it('spotlights the act’s new row with the preview on a tablet or desktop', () => {
    expect(editorTourTargets(2, 'land', 'tablet')).toEqual(['[data-editor-tour-track="tour-stills"]', '[data-editor-tour="preview"]']);
    expect(editorTourTargets(2, 'land')).toEqual(editorTourTargets(2, 'land', 'desktop'));
  });

  it('leaves a phone’s land beat to the preview alone, its timeline being under the card', () => {
    expect(editorTourTargets(3, 'land', 'phone')).toEqual(['[data-editor-tour="preview"]']);
    expect(editorTourTargets(1, 'compose', 'phone')).toEqual(['[data-editor-tour="chat-composer"]']);
  });
});
