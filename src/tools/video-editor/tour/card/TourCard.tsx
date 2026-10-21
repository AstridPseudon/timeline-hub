import type { ReactNode } from 'react';
import './TourCard.css';
import { EDITOR_TOUR_SCRIPT as SCRIPT } from '../tourScript';
import { TourStrip } from './TourStrip';
import { TourVisual } from './TourVisual';
import { useTourCardEntrance } from './useTourCardEntrance';
import { useEditorTour, type EditorTourAct, type EditorTourBeat } from '@/shared/state/editorTourStore';
import { Button } from '@/shared/components/ui/button.tsx';
import { cn } from '@/shared/components/ui/contracts/cn.ts';

export interface TourCardProps {
  /** Next, "I got it", or (while the reply plays) finish it: the runner decides, as for Enter. */
  onPrimary: () => void;
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
export function TourCard({ onPrimary, onSkip }: TourCardProps) {
  const act = useEditorTour((state) => state.act);
  const beat = useEditorTour((state) => state.beat);
  const runId = useEditorTour((state) => state.runId);
  const key = `${runId}:${act}:${beat}`;
  const explains = beat === 'welcome' || beat === 'land' || beat === 'finale';
  const { settled, reducedMotion } = useTourCardEntrance(key, explains);

  return (
    <div
      key={key}
      data-editor-tour-card={beat}
      data-settled={settled || undefined}
      className={cn('editor-tour-card', reducedMotion ? 'editor-tour-card-reduced' : !settled && 'editor-tour-card-playing')}
    >
      <section
        aria-label={beat === 'welcome' ? SCRIPT.welcome.title : beat === 'finale' ? SCRIPT.finale.title : `Tour, step ${act} of ${ACT_COUNT}`}
        className={cn(
          'editor-tour-rise rounded-xl border border-border bg-card text-card-foreground shadow-xl',
          beat === 'welcome' && 'w-[400px] p-6',
          beat === 'land' && 'w-[380px] p-5',
          beat === 'finale' && 'w-[480px] p-6',
          !explains && 'w-[300px] px-4 py-3',
        )}
      >
        {beat === 'welcome' && <Welcome onPrimary={onPrimary} onSkip={onSkip} />}
        {beat === 'land' && <Explainer act={act} playing={!reducedMotion} onPrimary={onPrimary} onSkip={onSkip} />}
        {beat === 'finale' && <Finale playing={!reducedMotion} onPrimary={onPrimary} />}
        {!explains && <Hint act={act} beat={beat} onPrimary={onPrimary} onSkip={onSkip} />}
      </section>
    </div>
  );
}

function Explainer({ act, playing, onPrimary, onSkip }: { act: EditorTourAct; playing: boolean } & TourCardProps) {
  const { title, body, visual, labels } = SCRIPT.acts[act].card;
  return (
    <>
      <TourVisual visual={visual} labels={labels} playing={playing} />
      <h2 className="mt-4 text-balance font-serif font-theme-heading text-xl leading-tight text-foreground">
        <span className="tabular-nums text-muted-foreground">{act} · </span>
        {title}
      </h2>
      <p className="mt-1.5 text-pretty text-sm leading-6 text-muted-foreground">{body}</p>
      <div className="mt-4">
        <TourStrip filled={act} labels={SCRIPT.strip} />
      </div>
      <div className="mt-5 flex items-center justify-between gap-3">
        <SkipControl onSkip={onSkip} />
        <PrimaryButton label={SCRIPT.controls.next} onPrimary={onPrimary} />
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

function Welcome({ onPrimary, onSkip }: TourCardProps) {
  return (
    <>
      <MinkTitle>{SCRIPT.welcome.title}</MinkTitle>
      <p className="mt-3 text-pretty text-[15px] leading-6 text-muted-foreground">{SCRIPT.welcome.body}</p>
      <div className="mt-6 flex items-center justify-between gap-3">
        <SkipControl onSkip={onSkip} />
        <PrimaryButton label={SCRIPT.welcome.action} onPrimary={onPrimary} size="default" />
      </div>
    </>
  );
}

function Finale({ playing, onPrimary }: { playing: boolean; onPrimary: () => void }) {
  return (
    <>
      <MinkTitle>{SCRIPT.finale.title}</MinkTitle>
      <div className="mt-6">
        <TourStrip filled={3} labels={SCRIPT.finale.recap} size="large" playing={playing} />
      </div>
      <div className="mt-7 flex justify-end">
        <PrimaryButton label={SCRIPT.finale.action} onPrimary={onPrimary} size="default" />
      </div>
    </>
  );
}

/** Compose: send the prompt (the chat's Send, or Enter). Respond: the reply's Next. */
function Hint({ act, beat, onPrimary, onSkip }: { act: EditorTourAct; beat: EditorTourBeat } & TourCardProps) {
  const compose = beat === 'compose';
  return (
    <>
      <div className="flex items-center justify-between text-[11px] leading-none text-muted-foreground">
        <span className="tabular-nums">{act} of {ACT_COUNT}</span>
        <SkipControl onSkip={onSkip} />
      </div>
      <div className="mt-2 flex min-h-9 items-center justify-between gap-3">
        <p className="text-sm text-foreground">{compose ? SCRIPT.hints.compose : SCRIPT.hints.respond}</p>
        {compose ? <Kbd>↵</Kbd> : <PrimaryButton label={SCRIPT.controls.next} onPrimary={onPrimary} />}
      </div>
    </>
  );
}

function PrimaryButton({ label, onPrimary, size = 'sm' }: { label: string; onPrimary: () => void; size?: 'sm' | 'default' }) {
  return (
    <Button type="button" size={size} className="gap-2 pr-2.5" onClick={onPrimary}>
      {label}
      <Kbd onPrimary>↵</Kbd>
    </Button>
  );
}

function SkipControl({ onSkip }: { onSkip?: () => void }) {
  const content = (
    <>
      {SCRIPT.controls.skip}
      <Kbd>Esc</Kbd>
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
