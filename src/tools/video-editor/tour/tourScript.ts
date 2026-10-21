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
  /** The explainer on the act's `land` beat; the card numbers the title itself. */
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
  /** The card's quiet line while the chat has the spotlight: before Send, and while the reply plays. */
  readonly hints: { readonly compose: string; readonly respond: string };
  readonly controls: { readonly next: string; readonly skip: string };
  /** Three.js frame → still → video: the card's strip, one step per act. */
  readonly strip: readonly [string, string, string];
  readonly finale: { readonly title: string; readonly action: string; readonly recap: readonly [string, string, string] };
}

/** Prompts keep the owner's wording. Captions keep the tour's three claims and read in about two seconds. */
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
        title: 'Create with your agent + extensions',
        body: 'Astrid is built so you and your agent can create in all kinds of flexible ways. This is an example of using Three.js, right in your timeline.',
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
        title: 'Generate with local models',
        body: 'You can use ComfyUI, Wan2GP or any other inference framework to run models on your own machine, with your agent taking care of all the tricky work.',
        visual: 'frame-to-still',
        labels: ['Frame', 'Qwen Image 2.1'],
      },
    },
    3: {
      prompt: 'Now use MiniMax H3 to turn that into a 10-second video, following the motion in the Three.js scene.',
      reply: 'MiniMax H3 turned your start and end frames into one 10-second shot that follows the scene’s motion. It’s on the top row, ready to play.',
      toolCards: [{ name: 'MiniMax H3', detail: 'start + end frames · 10 s' }],
      card: {
        title: 'Production-level creative control',
        body: 'MiniMax H3 turns your start and end frames into a finished 10-second shot that follows the scene’s motion: ultimate control over your tools and your output.',
        visual: 'still-to-video',
        labels: ['MiniMax H3', '10 s'],
      },
    },
  },
  welcome: { title: 'Welcome to Astrid', body: 'I’m just going to show you a very quick tour of what Astrid can do.', action: 'OK' },
  hints: { compose: 'Press Send to ask Astrid', respond: 'See where it lands' },
  controls: { next: 'Next', skip: 'Skip tour' },
  strip: ['Three.js', 'Frames', 'Video'],
  finale: { title: 'Do you get it?', action: 'I got it', recap: ['Agent + extensions', 'Local models', 'Production'] },
});
