import type { EditorTourAct } from '@/shared/state/editorTourStore';

export interface EditorTourToolCard {
  readonly name: string;
  readonly detail: string;
}

export type EditorTourVisual = 'extension' | 'frame-to-still' | 'still-to-video';

export interface EditorTourActScript {
  /** Typed into the chat composer; the user sends it. */
  readonly prompt: string;
  /** Streamed as Astrid's reply. */
  readonly reply: string;
  readonly toolCards: readonly EditorTourToolCard[];
  /** The explainer on the act's `land` beat; the card's counter numbers it. */
  readonly card: {
    readonly title: string;
    readonly body: string;
    readonly visual: EditorTourVisual;
    /** The visual's two small labels: what it starts from, and what made the result. */
    readonly labels: readonly [string, string];
  };
}

export interface EditorTourScript {
  readonly acts: Readonly<Record<EditorTourAct, EditorTourActScript>>;
  /** The centred card before act 1: Astrid says hello. */
  readonly welcome: { readonly title: string; readonly body: string; readonly action: string };
  /** The card's quiet line while the chat has the spotlight: before Send, and (act 1 only) while the reply plays. */
  readonly hints: { readonly compose: string; readonly respond: string };
  readonly controls: { readonly next: string; readonly back: string; readonly skip: string };
  /** Three.js frame → still → video: the card's strip, one step per act. */
  readonly strip: readonly [string, string, string];
  readonly finale: { readonly title: string; readonly action: string; readonly recap: readonly [string, string, string] };
}

/**
 * Prompts keep the owner's wording. Each act's card title says what the agent just did (it creates and uses
 * extensions, generates with local models, brings it all together); the body carries the bigger picture.
 * Captions keep the tour's three claims and read in about two seconds.
 */
export const EDITOR_TOUR_SCRIPT = Object.freeze<EditorTourScript>({
  acts: {
    1: {
      prompt: 'Make me a Three.js journey through a valley with lanterns in it as the moon rises.',
      reply: 'Lantern Valley is on your timeline: 10 seconds of a live Three.js scene, with the moon up and the lanterns lifting off the water.',
      toolCards: [
        { name: 'Built Lantern Valley', detail: 'Three.js live scene' },
        { name: 'Placed it on the timeline', detail: 'Moon overlook · 10 s' },
      ],
      card: {
        title: 'Your agent creates with extendable tools',
        body: 'Lantern Valley is a live Three.js scene, on your timeline to play, test and give feedback on. You and your agent can create with any extension, or build your own.',
        visual: 'extension',
        labels: ['Three.js', 'extension'],
      },
    },
    2: {
      prompt: 'Can you make me realistic frames for that using Qwen Image 2.1?',
      reply: 'I made realistic start and end frames with Qwen Image 2.1 in ComfyUI. Both stills are on a new row above the scene.',
      toolCards: [
        { name: 'Captured 2 frames', detail: 'Lantern Valley · start and end' },
        { name: 'Qwen Image 2.1 × 2', detail: 'ComfyUI · frame → realistic still' },
      ],
      card: {
        title: 'Your agent generates with local models',
        body: 'Qwen Image 2.1 made these realistic frames in ComfyUI, on your own machine. Your agent can run ComfyUI, Wan2GP or any inference framework, and handles the tricky setup.',
        visual: 'frame-to-still',
        labels: ['Frame', 'Qwen Image 2.1'],
      },
    },
    3: {
      prompt: 'Now use MiniMax H3 to turn that into a 10-second video, following the motion in the Three.js scene.',
      reply: 'MiniMax H3 turned your start and end frames into one 10-second shot that follows the scene’s motion. It’s on the top row, ready to play.',
      toolCards: [{ name: 'MiniMax H3', detail: 'start + end frames · 10 s' }],
      card: {
        title: 'Your agent brings it all together',
        body: 'MiniMax H3 turned your frames into a 10-second shot that follows the Three.js motion. Every input you and your agent create gives you production‑level creative control.',
        visual: 'still-to-video',
        labels: ['MiniMax H3', '10 s'],
      },
    },
  },
  welcome: { title: 'Welcome to Astrid', body: 'I’m just going to show you a very quick tour of what Astrid can do.', action: 'OK' },
  hints: { compose: 'Press Send to ask Astrid', respond: 'Your agent uses creative and AI tools to deliver your request' },
  controls: { next: 'Next', back: 'Back', skip: 'Skip tour' },
  strip: ['Three.js', 'Frames', 'Video'],
  finale: { title: 'Do you get it?', action: 'I got it', recap: ['Agent + extensions', 'Local models', 'Production'] },
});
