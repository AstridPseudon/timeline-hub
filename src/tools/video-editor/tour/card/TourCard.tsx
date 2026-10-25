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
import type { TimelineDeviceClass } from '../../lib/mobile-interaction-model';

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
  /**
   * The editor's layout. A phone's card spans the screen and leaves the picture to the spotlit preview above it; a tablet's
   * is roomier with a larger strip in place of the picture; both size every control for a finger (44 px).
   */
  device?: TimelineDeviceClass;
}

/** What the card's parts need to know about the device: finger-sized controls, and which layout. */
interface Fit {
  touch: boolean;
  device: TimelineDeviceClass;
  showKeyboardHints: boolean;
}

const ACT_COUNT = 3;

/**
 * The tour's card, for whatever beat the store is on. It opens with Astrid's welcome; while the chat has
 * the spotlight it is a quiet line (and the Next for the reply); on each `land` it explains the act with a
 * visual and the Three.js → frames → video strip; at the end it asks "Do you get it?". Presentational: the runner positions it and owns the
 * actions. It marks itself ready once its entrance has played (at once on reduced motion or a skip).
 */
export function TourCard({ act, beat, onPrimary, onBack, onSkip, device = 'desktop' }: TourCardProps) {
  const runId = useEditorTour((state) => state.runId);
  const live = useEditorTour((state) => state.act === act && state.beat === beat);
  const key = `${runId}:${act}:${beat}`;
  const explains = beat === 'welcome' || beat === 'land' || beat === 'finale' || beat === 'feedback';
  const coarse = typeof window !== 'undefined' && Boolean(window.matchMedia?.('(pointer: coarse)').matches);
  const fit: Fit = { device, touch: device !== 'desktop' || coarse, showKeyboardHints: detectInstallScenario() !== 'mobile' && !coarse };
  const phone = device === 'phone';
  const tablet = device === 'tablet';
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
          'editor-tour-rise max-w-[calc(100vw-24px)] max-h-[calc(100dvh-24px)] overflow-y-auto overscroll-contain rounded-xl border border-border bg-card text-card-foreground shadow-xl',
          phone ? cn('w-[calc(100vw-24px)] rounded-2xl', explains ? 'p-5' : 'px-5 py-4') : tablet ? cn(
            beat === 'welcome' && 'w-[460px] p-7',
            beat === 'land' && 'w-[520px] p-6',
            beat === 'finale' && 'w-[540px] p-7',
            beat === 'feedback' && 'w-[500px] p-7',
            !explains && 'w-[400px] px-5 py-4',
          ) : cn(
            beat === 'welcome' && 'w-[400px] p-6',
            beat === 'land' && 'w-[380px] p-5',
            beat === 'finale' && 'w-[480px] p-6',
            beat === 'feedback' && 'w-[440px] p-6',
            !explains && (beat === 'respond' || (beat === 'compose' && SCRIPT.acts[act].composeHeader) ? 'w-[360px]' : 'w-[300px]') + ' px-4 py-3',
          ),
        )}
      >
        {beat === 'welcome' && <Welcome onPrimary={onPrimary} onSkip={onSkip} fit={fit} />}
        {beat === 'land' && <Explainer act={act} playing={!reducedMotion} onPrimary={onPrimary} onBack={onBack} onSkip={onSkip} fit={fit} />}
        {beat === 'finale' && <Finale playing={!reducedMotion} onPrimary={onPrimary} onBack={onBack} fit={fit} />}
        {beat === 'feedback' && <Feedback onPrimary={onPrimary} onBack={onBack} fit={fit} />}
        {!explains && <Hint act={act} beat={beat} onPrimary={onPrimary} onBack={onBack} onSkip={onSkip} fit={fit} />}
      </section>
    </div>
  );
}

/** The top row of the Hint and the Explainer: "N of 3", Back right beside it, Skip on the right. */
function CounterRow({ act, onBack, onSkip, fit }: { act: EditorTourAct; fit: Fit } & Pick<TourCardProps, 'onBack' | 'onSkip'>) {
  return (
    <div className="flex items-center justify-between leading-none text-muted-foreground">
      <div className={cn('flex items-center', fit.touch ? 'gap-4' : 'gap-3')}>
        <span className="text-xs tabular-nums">{act} of {ACT_COUNT}</span>
        <BackControl onBack={onBack} touch={fit.touch} />
      </div>
      <SkipControl onSkip={onSkip} fit={fit} />
    </div>
  );
}

function Explainer({ act, playing, onPrimary, onBack, onSkip, fit }: { act: EditorTourAct; playing: boolean; fit: Fit } & Omit<TourCardProps, 'act' | 'beat'>) {
  const { title, body, visual, labels } = SCRIPT.acts[act].card;
  // The spotlit preview above a touch card already shows this act's picture, full size.
  const pictured = !fit.touch;
  return (
    <>
      <CounterRow act={act} onBack={onBack} onSkip={onSkip} fit={fit} />
      {pictured && (
        <div className="mt-3">
          <TourVisual visual={visual} labels={labels} playing={playing} />
        </div>
      )}
      <h2 className={cn('text-pretty font-serif font-theme-heading leading-tight text-foreground', pictured ? 'mt-4 text-lg' : 'mt-3 text-xl')}>{title}</h2>
      <p className={cn('mt-1.5 text-pretty leading-6 text-muted-foreground', fit.device === 'tablet' ? 'text-[15px]' : 'text-sm')}>{body}</p>
      {fit.device === 'tablet' ? (
        // A tablet has the width for the larger strip and Next side by side, which keeps the card short enough to sit beside its targets.
        <div className="mt-5 flex items-end gap-6">
          <div className="min-w-0 flex-1"><TourStrip filled={act} labels={SCRIPT.strip} size="medium" /></div>
          <PrimaryButton label={SCRIPT.controls.next} onPrimary={onPrimary} fit={fit} />
        </div>
      ) : (
        <>
          <div className="mt-4">
            <TourStrip filled={act} labels={SCRIPT.strip} />
          </div>
          <div className={cn('flex justify-end', fit.touch ? 'mt-4' : 'mt-5')}>
            <PrimaryButton label={SCRIPT.controls.next} onPrimary={onPrimary} fit={fit} />
          </div>
        </>
      )}
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

function Welcome({ onPrimary, onSkip, fit }: Omit<TourCardProps, 'act' | 'beat'> & { fit: Fit }) {
  return (
    <>
      <MinkTitle>{SCRIPT.welcome.title}</MinkTitle>
      <p className="mt-3 text-pretty text-[15px] leading-6 text-muted-foreground">{SCRIPT.welcome.body}</p>
      <div className="mt-6 flex items-center justify-between gap-3">
        <SkipControl onSkip={onSkip} fit={fit} />
        <PrimaryButton label={SCRIPT.welcome.action} onPrimary={onPrimary} size="default" fit={fit} />
      </div>
    </>
  );
}

function Finale({ playing, onPrimary, onBack, fit }: { playing: boolean; onPrimary: () => void; onBack?: () => void; fit: Fit }) {
  return (
    <>
      <MinkTitle>{SCRIPT.finale.title}</MinkTitle>
      <div className="mt-6">
        <TourStrip filled={3} labels={SCRIPT.finale.recap} size="large" playing={playing} />
      </div>
      <div className="mt-7 flex items-center justify-between gap-3">
        <BackControl onBack={onBack} touch={fit.touch} />
        <PrimaryButton label={SCRIPT.finale.action} onPrimary={onPrimary} size="default" fit={fit} />
      </div>
    </>
  );
}

function Feedback({ onPrimary, onBack, fit }: { onPrimary: () => void; onBack?: () => void; fit: Fit }) {
  // On a phone or tablet the tour ends by sending Astrid to a computer, so "Start creating" would promise the wrong next screen.
  const action = detectInstallScenario() === 'mobile' ? SCRIPT.feedback.mobileAction : SCRIPT.feedback.action;
  return (
    <>
      <MinkTitle>{SCRIPT.feedback.title}</MinkTitle>
      <p className="mt-3 text-pretty text-[15px] leading-6 text-muted-foreground">{SCRIPT.feedback.body}</p>
      <Button asChild variant="outline" className={cn('mt-4 gap-2', fit.touch && 'h-11')}>
        <a href={DISCORD_URL} target="_blank" rel="noopener noreferrer">
          <DiscordMark />
          {SCRIPT.feedback.discord}
        </a>
      </Button>
      <div className="mt-6 flex items-center justify-between gap-3">
        <BackControl onBack={onBack} touch={fit.touch} />
        <PrimaryButton label={action} onPrimary={onPrimary} size="default" fit={fit} />
      </div>
    </>
  );
}

/** Compose: send the prompt (the chat's Send, or Enter). Respond (act 1 only): the reply's Next. */
function Hint({ act, beat, onPrimary, onBack, onSkip, fit }: TourCardProps & { fit: Fit }) {
  const compose = beat === 'compose';
  const header = compose ? SCRIPT.acts[act].composeHeader : undefined;
  return (
    <>
      <CounterRow act={act} onBack={onBack} onSkip={onSkip} fit={fit} />
      {header && (
        <h2 className="mt-3 text-pretty font-serif font-theme-heading text-lg leading-tight text-foreground">{header}</h2>
      )}
      <div className={cn('mt-2 flex items-center justify-between gap-3', fit.touch ? 'min-h-11' : 'min-h-9')}>
        <p className="text-sm text-foreground">{compose ? (fit.touch ? SCRIPT.hints.composeTouch : SCRIPT.hints.compose) : SCRIPT.hints.respond}</p>
        {compose ? fit.showKeyboardHints && <Kbd>↵</Kbd> : <PrimaryButton label={SCRIPT.controls.next} onPrimary={onPrimary} fit={fit} />}
      </div>
    </>
  );
}

function PrimaryButton({ label, onPrimary, size = 'sm', fit }: { label: string; onPrimary: () => void; size?: 'sm' | 'default'; fit: Fit }) {
  return (
    <Button type="button" size={fit.touch ? 'lg' : size} className={cn('gap-2', fit.touch ? 'min-w-24 px-6 text-[15px]' : 'pr-2.5')} onClick={onPrimary}>
      {label}
      {fit.showKeyboardHints && <Kbd onPrimary>↵</Kbd>}
    </Button>
  );
}

/** Quiet text controls; on touch their hit area grows to 44 px around the same visual size. */
const QUIET_TOUCH = 'min-h-11 min-w-11 -my-3.5 justify-center text-sm';

function BackControl({ onBack, touch }: { onBack?: () => void; touch: boolean }) {
  if (!onBack) return null;
  return (
    <button
      type="button"
      className={cn(
        'inline-flex items-center gap-0.5 rounded-sm leading-none text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
        touch ? cn(QUIET_TOUCH, '-mx-2 px-2') : '-mx-1 -my-1.5 px-1 py-1.5 text-xs',
      )}
      onClick={onBack}
    >
      <ChevronLeft className={touch ? 'h-4 w-4' : 'h-3 w-3'} aria-hidden />
      {SCRIPT.controls.back}
    </button>
  );
}

function SkipControl({ onSkip, fit }: { onSkip?: () => void; fit: Fit }) {
  const content = (
    <>
      {SCRIPT.controls.skip}
      {fit.showKeyboardHints && <Kbd>Esc</Kbd>}
    </>
  );
  const className = cn('inline-flex items-center gap-1.5 leading-none text-muted-foreground', fit.touch ? cn(QUIET_TOUCH, '-mx-2 px-2') : 'text-xs');
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
