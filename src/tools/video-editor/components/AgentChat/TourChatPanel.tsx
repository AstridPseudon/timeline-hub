import { useEffect, useMemo, useRef, useState } from 'react';
import { Loader2 } from 'lucide-react';
import { cn } from '@/shared/components/ui/contracts/cn.ts';
import {
  getEditorTourState,
  markEditorTourReady,
  markEditorTourSent,
  useEditorTour,
} from '@/shared/state/editorTourStore.ts';
import { usePanesStore } from '@/shared/state/panesStore.ts';
import { EDITOR_TOUR_ANCHOR_ATTRIBUTE, EDITOR_TOUR_ANCHORS } from '@/tools/video-editor/tour/anchors.ts';
import { EDITOR_TOUR_SCRIPT } from '@/tools/video-editor/tour/tourScript.ts';
import { AgentChatComposer } from './AgentChatComposer';
import { AgentChatMenu } from './AgentChatMenu';
import { AgentChatModelLine } from './AgentChatModelLine';
import { AgentIcon, agentNames } from './agentIdentity';
import { AgentChatMessage, AgentChatToolGroup } from './AgentChatMessage.tsx';
import { buildRenderedTurns } from './buildRenderedTurns';
import { buildTourTurns, tourActStartMs, type TourChatProgress } from './tourChatTurns';
import { CHAT_VOICE_ENABLED } from '@/tools/video-editor/hooks/chatVoice.ts';
import { useChatScroll } from './useChatScroll';

const IDLE_PLACEHOLDER = CHAT_VOICE_ENABLED ? 'Type or press Cmd+Shift+R to talk...' : 'Type a message...';
const COARSE_PLACEHOLDER = CHAT_VOICE_ENABLED ? 'Type, or tap the mic to talk...' : 'Type a message...';
const BUSY_PLACEHOLDER = 'Type to queue next message...';
// The header of a fresh chat: untitled, on the default agent. Static, so nothing here reaches a session.
const NO_SESSIONS: never[] = [];
const NO_OP = () => undefined;
const NO_MODEL_CHANGE = () => Promise.resolve();
const NO_PROGRESS: TourChatProgress = { typed: 0, replyChars: 0, cards: 0 };
// The tour never records: its mic is shown disabled while chat voice is on, and absent while it is off.
const NO_VOICE = { isRecording: false, onToggle: () => undefined, onCancel: () => undefined, micDisabled: true };

const TYPING_START_MS = 500;
const THINKING_MS = 700;
const STREAM_STEP_MS = 24;
const STREAM_CHARS_PER_STEP = 3;
const CARD_STEP_MS = 520;

/** A natural typing rhythm: steady, with a small pulse per character and a pause after punctuation. */
function typingDelayMs(typed: number, previous: string): number {
  const pause = /[,.?!]/.test(previous) ? 140 : previous === ' ' ? 18 : 0;
  return 34 + ((typed * 37) % 19) + pause;
}

/**
 * The scripted chat shown in place of the real one while the first-run tour runs. It renders the real
 * composer, message and tool-group components from the tour script and never touches a session or the agent.
 */
export function TourChatPanel({ isExpanded = false }: { isExpanded?: boolean }) {
  const runId = useEditorTour((state) => state.runId);
  const act = useEditorTour((state) => state.act);
  const beat = useEditorTour((state) => state.beat);
  const sent = useEditorTour((state) => state.sent);
  const chatReady = useEditorTour((state) => state.ready.chat);
  const reducedMotion = useEditorTour((state) => state.reducedMotion);
  const skipAnimation = useEditorTour((state) => state.skipAnimation);
  const setIsTasksPaneOpen = usePanesStore((state) => state.setIsTasksPaneOpen);
  const script = EDITOR_TOUR_SCRIPT.acts[act];
  const [coarsePointer] = useState(() => window.matchMedia?.('(pointer: coarse)').matches === true);

  useEffect(() => { setIsTasksPaneOpen(true); }, [setIsTasksPaneOpen]);

  // Each run (and replay) starts from an empty transcript with its own clock for the message times.
  const [clock, setClock] = useState(() => ({ runId, ms: Date.now() }));
  if (clock.runId !== runId) setClock({ runId, ms: Date.now() });
  const baseMs = clock.ms;

  const beatKey = `${runId}:${act}:${beat}`;
  const [animation, setAnimation] = useState<{ key: string } & TourChatProgress>({ key: '', ...NO_PROGRESS });
  const progress = animation.key === beatKey ? animation : NO_PROGRESS;
  const finishRef = useRef<(() => void) | null>(null);

  useEffect(() => {
    const timers = new Set<number>();
    const later = (fn: () => void, ms: number) => { timers.add(window.setTimeout(fn, ms)); };
    const update = (patch: Partial<TourChatProgress>) => setAnimation((prev) => ({
      ...(prev.key === beatKey ? prev : { key: beatKey, ...NO_PROGRESS }),
      ...patch,
    }));
    const finish = (patch: Partial<TourChatProgress>) => {
      timers.forEach((timer) => window.clearTimeout(timer));
      timers.clear();
      update(patch);
      markEditorTourReady('chat');
    };
    finishRef.current = null;

    if (beat === 'compose') {
      const { prompt } = script;
      const complete = () => finish({ typed: prompt.length });
      finishRef.current = complete;
      if (reducedMotion) { complete(); } else {
        const type = (typed: number) => {
          update({ typed });
          if (typed >= prompt.length) { markEditorTourReady('chat'); return; }
          later(() => type(typed + 1), typingDelayMs(typed, prompt[typed - 1] ?? ''));
        };
        later(() => type(1), TYPING_START_MS);
      }
    } else if (beat === 'respond') {
      const { reply, toolCards } = script;
      const complete = () => finish({ replyChars: reply.length, cards: toolCards.length });
      finishRef.current = complete;
      if (reducedMotion) { complete(); } else {
        const showCard = (cards: number) => {
          update({ cards });
          if (cards >= toolCards.length) { markEditorTourReady('chat'); return; }
          later(() => showCard(cards + 1), CARD_STEP_MS);
        };
        const stream = (replyChars: number) => {
          update({ replyChars });
          if (replyChars >= reply.length) { later(() => showCard(1), CARD_STEP_MS); return; }
          later(() => stream(Math.min(reply.length, replyChars + STREAM_CHARS_PER_STEP)), STREAM_STEP_MS);
        };
        later(() => stream(STREAM_CHARS_PER_STEP), THINKING_MS);
      }
    } else {
      markEditorTourReady('chat');
    }

    return () => {
      timers.forEach((timer) => window.clearTimeout(timer));
      finishRef.current = null;
    };
  }, [beat, beatKey, reducedMotion, script]);

  // The first Enter mid-animation (the runner bumps `skipAnimation`) jumps to the end of the current one.
  const lastSkip = useRef({ runId, skipAnimation });
  useEffect(() => {
    const last = lastSkip.current;
    lastSkip.current = { runId, skipAnimation };
    if (last.runId === runId && last.skipAnimation !== skipAnimation) finishRef.current?.();
  }, [runId, skipAnimation]);

  const turns = useMemo(
    () => buildTourTurns(EDITOR_TOUR_SCRIPT, baseMs, act, beat, sent, progress),
    [baseMs, act, beat, sent, progress],
  );
  const renderedTurns = useMemo(() => buildRenderedTurns(turns), [turns]);
  const currentActStart = new Date(tourActStartMs(baseMs, act)).toISOString();
  const { scrollContainerRef, scrollContentRef, onScroll } = useChatScroll(`tour:${runId}`, true, renderedTurns.length);

  const composerText = beat === 'compose' && !sent ? script.prompt.slice(0, progress.typed) : '';
  // As in the real chat, the indicator gives way once the reply text starts.
  const busy = beat === 'respond' && !chatReady;
  const thinking = busy && progress.replyChars === 0;

  return (
    <div className="flex h-full w-full flex-col overflow-hidden">
      {/* The real chat's header (same pieces, static props): the chat menu names the chat, the agent sits under it. */}
      <div className="relative flex min-w-0 items-center justify-between gap-2 border-b border-border/70 px-3 py-1.5">
        <div className="-ml-1.5 flex min-w-0 flex-col items-start">
          <AgentChatMenu
            sessions={NO_SESSIONS}
            activeSessionId={null}
            defaultAgent="astrid"
            onSelectSession={NO_OP}
            onNewChat={NO_OP}
          />
          <AgentChatModelLine
            agent="astrid"
            hasChat={false}
            modelName={null}
            onChangeThinkingLevel={NO_MODEL_CHANGE}
            onChooseAnotherModel={NO_OP}
          />
        </div>
        <div className="flex shrink-0 items-center gap-1" />
      </div>

      <div
        ref={scrollContainerRef}
        onScroll={onScroll}
        {...{ [EDITOR_TOUR_ANCHOR_ATTRIBUTE]: EDITOR_TOUR_ANCHORS.chatTranscript }}
        className="flex-1 overflow-y-auto overscroll-contain px-4 py-3"
      >
        {renderedTurns.length === 0 && (
          <div className="flex min-h-full flex-col items-center justify-center py-8 text-center text-sm text-muted-foreground">
            <p>✨ I can do almost anything</p>
            {CHAT_VOICE_ENABLED && (coarsePointer
              ? <p className="mt-1 text-xs">Tap the mic to talk</p>
              : <p className="mt-1 text-xs">Press <kbd className="rounded border border-border px-1 py-0.5 text-[10px]">Cmd+Shift+R</kbd> to talk</p>)}
            <p className="mt-4 flex items-center gap-1.5 rounded-md border border-border/70 px-2 py-1 text-[11px]">
              <AgentIcon agent="astrid" className="h-3 w-3 shrink-0" />
              {agentNames.astrid} · default model
            </p>
          </div>
        )}

        <div ref={scrollContentRef} className="flex flex-col gap-2.5">
          {renderedTurns.map((item) => {
            const at = item.kind === 'message' ? item.turn.timestamp : item.pairs[0].call.timestamp;
            return (
              <div
                key={item.key}
                className={cn(item.kind === 'message' ? 'flex flex-col gap-2.5' : 'space-y-2', reducedMotion && at >= currentActStart && 'animate-in fade-in duration-300')}
              >
                {item.kind === 'message'
                  ? <AgentChatMessage turn={item.turn} />
                  : <AgentChatToolGroup pairs={item.pairs} defaultOpen />}
              </div>
            );
          })}
          {thinking && (
            <div className="flex items-center gap-2 py-1 text-xs text-muted-foreground">
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              Thinking...
            </div>
          )}
        </div>
      </div>

      <div className="border-t border-border/70 px-3 py-3">
        <AgentChatComposer
          value={composerText}
          readOnly
          rows={isExpanded ? 8 : 4}
          placeholder={busy ? BUSY_PLACEHOLDER : coarsePointer ? COARSE_PLACEHOLDER : IDLE_PLACEHOLDER}
          voice={CHAT_VOICE_ENABLED ? NO_VOICE : undefined}
          onSend={() => {
            if (!getEditorTourState().sent) markEditorTourSent();
          }}
          sendDisabled={sent || beat !== 'compose' || progress.typed < script.prompt.length}
        />
      </div>
    </div>
  );
}
