import { describe, expect, it } from 'vitest';
import { editorTourTargets, phoneSpotlight } from './EditorTourRunner';

describe('editorTourTargets', () => {
  it('spotlights the act’s new row with the preview on land', () => {
    expect(editorTourTargets(2, 'land')).toEqual(['[data-editor-tour-track="tour-stills"]', '[data-editor-tour="preview"]']);
    expect(editorTourTargets(1, 'compose')).toEqual(['[data-editor-tour="chat-composer"]']);
  });
});

describe('phoneSpotlight', () => {
  const track = { x: 0, y: 440, width: 393, height: 44 };
  const preview = { x: 6, y: 150, width: 381, height: 216 };

  it('keeps the new row lit when the sheet fits under it', () => {
    expect(phoneSpotlight([track, preview], 300, 852)).toEqual([track, preview]);
  });

  it('lets the row give way on a short phone, keeping the preview lit', () => {
    expect(phoneSpotlight([track, preview], 300, 667)).toEqual([preview]);
  });
});
