import type { ReactNode } from 'react';
import './TourCard.css';
import { EDITOR_TOUR_SCRIPT as SCRIPT } from '../tourScript';
import { TOUR_FINALE_ENTRANCE_MS, TourStrip } from './TourStrip';
import { TourVisual } from './TourVisual';
import { TOUR_CARD_ENTRANCE_MS, useTourCardEntrance } from './useTourCardEntrance';
import { useEditorTour, type EditorTourAct, type EditorTourBeat } from '@/shared/state/editorTourStore';
import { ChevronLeft } from 'lucide-react';
import { DiscordMark } from '@/pages/Home/PublicAstridSocialLinks';
import { DISCORD_URL } from '@/pages/Home/publicAstridLinks';
import { Button } from '@/shared/components/ui/button.tsx';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import { detectInstallScenario } from '@/pages/Home/installScenario.ts';

export interface TourCardProps {
  /** The beat to show: the runner's settled beat, which trails the store's while the card is about to move. */
  act: EditorTourAct;
  beat: EditorTourBeat;
  /** Next, "I got it", or (while the reply plays) finish it: the runner decides, as for Enter. */
  onPrimary: () => void;
  /** Go back to the previous place the user acted. Without it the card shows no Back. */
  onBack?: () => void;
  /** Leave the tour, as Esc does. Without it the card only names the key. */
  onSkip?: () => void;
}

const ACT_COUNT = 3;

/**
 * The tour's card, for whatever beat the store is on. It opens with Astrid's welcome; while the chat has
 * the spotlight it is a quiet line (and the Next for the reply); on each `land` it explains the act with a
 * visual and the Three.js → frames → video strip; at the end it asks "Do you get it?". Presentational: the runner positions it and owns the
 * actions. It marks itself ready once its entrance has played (at once on reduced motion or a skip).
 */
export function TourCard({ act, beat, onPrimary, onBack, onSkip }: TourCardProps) {
  const runId = useEditorTour((state) => state.runId);
  const live = useEditorTour((state) => state.act === act && state.beat === beat);
  const key = `${runId}:${act}:${beat}`;
  const explains = beat === 'welcome' || beat === 'land' || beat === 'finale' || beat === 'feedback';
  const showKeyboardHints = detectInstallScenario() !== 'mobile'
    && !(typeof window !== 'undefined' && Boolean(window.matchMedia?.('(pointer: coarse)').matches));
  // A card still showing the previous beat never reports ready for the new one.
  // The finale's entrance runs on until its chain has lit.
  const { settled, reducedMotion } = useTourCardEntrance(key, explains && live, beat === 'finale' ? TOUR_FINALE_ENTRANCE_MS : TOUR_CARD_ENTRANCE_MS);

  return (
    <div
      key={key}
      data-editor-tour-card={beat}
      data-settled={settled || undefined}
      className={cn('editor-tour-card', reducedMotion ? 'editor-tour-card-reduced' : !settled && 'editor-tour-card-playing')}
    >
      <section
        aria-label={beat === 'welcome' ? SCRIPT.welcome.title : beat === 'finale' ? SCRIPT.finale.title : beat === 'feedback' ? SCRIPT.feedback.title : `Tour, step ${act} of ${ACT_COUNT}`}
        className={cn(
          'editor-tour-rise max-w-[calc(100vw-24px)] max-h-[calc(100dvh-24px)] overflow-y-auto rounded-xl border border-border bg-card text-card-foreground shadow-xl',
          beat === 'welcome' && 'w-[400px] p-6',
          beat === 'land' && 'w-[380px] p-5',
          beat === 'finale' && 'w-[480px] p-6',
          beat === 'feedback' && 'w-[440px] p-6',
          !explains && (beat === 'respond' || (beat === 'compose' && SCRIPT.acts[act].composeHeader) ? 'w-[360px]' : 'w-[300px]') + ' px-4 py-3',
        )}
      >
        {beat === 'welcome' && <Welcome onPrimary={onPrimary} onSkip={onSkip} showKeyboardHints={showKeyboardHints} />}
        {beat === 'land' && <Explainer act={act} playing={!reducedMotion} onPrimary={onPrimary} onBack={onBack} onSkip={onSkip} showKeyboardHints={showKeyboardHints} />}
        {beat === 'finale' && <Finale playing={!reducedMotion} onPrimary={onPrimary} onBack={onBack} showKeyboardHints={showKeyboardHints} />}
        {beat === 'feedback' && <Feedback onPrimary={onPrimary} onBack={onBack} showKeyboardHints={showKeyboardHints} />}
        {!explains && <Hint act={act} beat={beat} onPrimary={onPrimary} onBack={onBack} onSkip={onSkip} showKeyboardHints={showKeyboardHints} />}
      </section>
    </div>
  );
}

/** The top row of the Hint and the Explainer: "N of 3", Back right beside it, Skip on the right. */
function CounterRow({ act, onBack, onSkip, showKeyboardHint }: { act: EditorTourAct; showKeyboardHint: boolean } & Pick<TourCardProps, 'onBack' | 'onSkip'>) {
  return (
    <div className="flex items-center justify-between leading-none text-muted-foreground">
      <div className="flex items-center gap-3">
        <span className="text-xs tabular-nums">{act} of {ACT_COUNT}</span>
        <BackControl onBack={onBack} />
      </div>
      <SkipControl onSkip={onSkip} showKeyboardHint={showKeyboardHint} />
    </div>
  );
}

function Explainer({ act, playing, onPrimary, onBack, onSkip, showKeyboardHints }: { act: EditorTourAct; playing: boolean; showKeyboardHints: boolean } & Omit<TourCardProps, 'act' | 'beat'>) {
  const { title, body, visual, labels } = SCRIPT.acts[act].card;
  return (
    <>
      <CounterRow act={act} onBack={onBack} onSkip={onSkip} showKeyboardHint={showKeyboardHints} />
      <div className="mt-3">
        <TourVisual visual={visual} labels={labels} playing={playing} />
      </div>
      <h2 className="mt-4 text-pretty font-serif font-theme-heading text-lg leading-tight text-foreground">{title}</h2>
      <p className="mt-1.5 text-pretty text-sm leading-6 text-muted-foreground">{body}</p>
      <div className="mt-4">
        <TourStrip filled={act} labels={SCRIPT.strip} />
      </div>
      <div className="mt-5 flex justify-end">
        <PrimaryButton label={SCRIPT.controls.next} onPrimary={onPrimary} showKeyboardHint={showKeyboardHints} />
      </div>
    </>
  );
}

/** Astrid speaks at the start and the end: the pixel mink, at a whole multiple of its 16px grid, beside the title. */
function MinkTitle({ children }: { children: ReactNode }) {
  return (
    <div className="flex items-center gap-3">
      <img src="/astrid-favicon.svg" alt="" className="h-8 w-8 [image-rendering:pixelated]" draggable={false} />
      <h2 className="font-serif font-theme-heading text-2xl leading-tight text-foreground">{children}</h2>
    </div>
  );
}

function Welcome({ onPrimary, onSkip, showKeyboardHints }: Omit<TourCardProps, 'act' | 'beat'> & { showKeyboardHints: boolean }) {
  return (
    <>
      <MinkTitle>{SCRIPT.welcome.title}</MinkTitle>
      <p className="mt-3 text-pretty text-[15px] leading-6 text-muted-foreground">{SCRIPT.welcome.body}</p>
      <div className="mt-6 flex items-center justify-between gap-3">
        <SkipControl onSkip={onSkip} showKeyboardHint={showKeyboardHints} />
        <PrimaryButton label={SCRIPT.welcome.action} onPrimary={onPrimary} size="default" showKeyboardHint={showKeyboardHints} />
      </div>
    </>
  );
}

function Finale({ playing, onPrimary, onBack, showKeyboardHints }: { playing: boolean; onPrimary: () => void; onBack?: () => void; showKeyboardHints: boolean }) {
  return (
    <>
      <MinkTitle>{SCRIPT.finale.title}</MinkTitle>
      <div className="mt-6">
        <TourStrip filled={3} labels={SCRIPT.finale.recap} size="large" playing={playing} />
      </div>
      <div className="mt-7 flex items-center justify-between gap-3">
        <BackControl onBack={onBack} />
        <PrimaryButton label={SCRIPT.finale.action} onPrimary={onPrimary} size="default" showKeyboardHint={showKeyboardHints} />
      </div>
    </>
  );
}

function Feedback({ onPrimary, onBack, showKeyboardHints }: { onPrimary: () => void; onBack?: () => void; showKeyboardHints: boolean }) {
  return (
    <>
      <MinkTitle>{SCRIPT.feedback.title}</MinkTitle>
      <p className="mt-3 text-pretty text-[15px] leading-6 text-muted-foreground">{SCRIPT.feedback.body}</p>
      <Button asChild variant="outline" className="mt-4 gap-2">
        <a href={DISCORD_URL} target="_blank" rel="noopener noreferrer">
          <DiscordMark />
          {SCRIPT.feedback.discord}
        </a>
      </Button>
      <div className="mt-6 flex items-center justify-between gap-3">
        <BackControl onBack={onBack} />
        <PrimaryButton label={SCRIPT.feedback.action} onPrimary={onPrimary} size="default" showKeyboardHint={showKeyboardHints} />
      </div>
    </>
  );
}

/** Compose: send the prompt (the chat's Send, or Enter). Respond (act 1 only): the reply's Next. */
function Hint({ act, beat, onPrimary, onBack, onSkip, showKeyboardHints }: TourCardProps & { showKeyboardHints: boolean }) {
  const compose = beat === 'compose';
  const header = compose ? SCRIPT.acts[act].composeHeader : undefined;
  return (
    <>
      <CounterRow act={act} onBack={onBack} onSkip={onSkip} showKeyboardHint={showKeyboardHints} />
      {header && (
        <h2 className="mt-3 text-pretty font-serif font-theme-heading text-lg leading-tight text-foreground">{header}</h2>
      )}
      <div className="mt-2 flex min-h-9 items-center justify-between gap-3">
        <p className="text-sm text-foreground">{compose ? SCRIPT.hints.compose : SCRIPT.hints.respond}</p>
        {compose ? showKeyboardHints && <Kbd>↵</Kbd> : <PrimaryButton label={SCRIPT.controls.next} onPrimary={onPrimary} showKeyboardHint={showKeyboardHints} />}
      </div>
    </>
  );
}

function PrimaryButton({ label, onPrimary, size = 'sm', showKeyboardHint }: { label: string; onPrimary: () => void; size?: 'sm' | 'default'; showKeyboardHint: boolean }) {
  return (
    <Button type="button" size={size} className="gap-2 pr-2.5" onClick={onPrimary}>
      {label}
      {showKeyboardHint && <Kbd onPrimary>↵</Kbd>}
    </Button>
  );
}

function BackControl({ onBack }: { onBack?: () => void }) {
  if (!onBack) return null;
  return (
    <button
      type="button"
      className="-mx-1 -my-1.5 inline-flex items-center gap-0.5 rounded-sm px-1 py-1.5 text-xs leading-none text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      onClick={onBack}
    >
      <ChevronLeft className="h-3 w-3" aria-hidden />
      {SCRIPT.controls.back}
    </button>
  );
}

function SkipControl({ onSkip, showKeyboardHint }: { onSkip?: () => void; showKeyboardHint: boolean }) {
  const content = (
    <>
      {SCRIPT.controls.skip}
      {showKeyboardHint && <Kbd>Esc</Kbd>}
    </>
  );
  const className = 'inline-flex items-center gap-1.5 text-xs leading-none text-muted-foreground';
  if (!onSkip) return <span className={className}>{content}</span>;
  return (
    <button type="button" className={cn(className, 'rounded-sm transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring')} onClick={onSkip}>
      {content}
    </button>
  );
}

function Kbd({ children, onPrimary = false }: { children: ReactNode; onPrimary?: boolean }) {
  return (
    <kbd
      className={cn(
        'inline-flex h-5 min-w-5 items-center justify-center rounded border px-1 font-sans text-[10px] leading-none',
        onPrimary ? 'border-primary-foreground/30 text-primary-foreground/80' : 'border-border text-muted-foreground',
      )}
    >
      {children}
    </kbd>
  );
}
