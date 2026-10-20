import { Layers, Sparkles } from 'lucide-react';
import { LABEL_WIDTH } from '@/tools/video-editor/lib/coordinate-utils.ts';
import type { TimelineCreateToolsHost } from '@/tools/video-editor/lib/mobile-interaction-model.ts';
import { VIDEO_EDITOR_THEME_VARS } from '@/tools/video-editor/lib/themeTokens.ts';

/** The prompts the effect and animation tools hand to the agent composer. One definition, shared by the
 *  canvas footer and the shell hosts, so the two placements cannot drift apart. */
export const CREATE_EFFECT_PROMPT = "I'd like to create a new effect.";
export const CREATE_ANIMATION_PROMPT = "I'd like to create an animation.";

const TOOL_BUTTON_BASE_CLASS = 'pointer-events-auto relative flex items-center justify-center rounded-full ring-1 transition-all duration-150 hover:-translate-y-0.5 hover:scale-105 active:translate-y-0 active:scale-100';
const POINTER_TOOL_BUTTON_SIZE_CLASS = 'h-6 w-6';
const TOUCH_TOOL_BUTTON_SIZE_CLASS = 'h-10 w-10';
const TEXT_TOOL_TONE_CLASS = 'bg-[var(--video-editor-accent-bg-strong)] text-foreground ring-[var(--video-editor-accent-ring)] hover:bg-[var(--video-editor-accent-bg-hover)] hover:shadow-[0_6px_18px_var(--video-editor-accent-shadow-soft)] hover:ring-[var(--video-editor-accent-border)]';
const EFFECT_TOOL_TONE_CLASS = 'bg-[var(--video-editor-effect-bg)] text-foreground ring-[var(--video-editor-effect-ring)] hover:bg-[var(--video-editor-effect-bg-hover)] hover:shadow-[0_6px_18px_var(--video-editor-effect-shadow-soft)] hover:ring-[var(--video-editor-effect-ring-strong)]';
const SEQUENCE_TOOL_TONE_CLASS = 'bg-[var(--video-editor-success-bg)] text-foreground ring-[var(--video-editor-success-ring)] hover:bg-[var(--video-editor-success-bg-hover)] hover:shadow-[0_6px_18px_var(--video-editor-success-shadow-soft)] hover:ring-[var(--video-editor-success-ring-strong)]';
const TOOL_TOOLTIP_CLASS = 'pointer-events-none absolute bottom-full left-1/2 mb-2 -translate-x-1/2 whitespace-nowrap rounded-md border border-border bg-popover px-2 py-1 text-[11px] font-medium text-popover-foreground opacity-0 shadow-md transition-opacity group-hover/tool:opacity-100';

function TextGlyph({ size }: { size: number }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/></svg>
  );
}

export interface TimelineCreateToolsProps {
  /** `pointer`: 24px HTML5 drag sources. `touch`: 40px tap buttons (drag and drop never fires on touch). */
  variant: 'pointer' | 'touch';
  /** Where the cluster is mounted; see `resolveTimelineCreateToolsHost`. */
  host: TimelineCreateToolsHost;
  /** Presence shows the text tool. Called on tap; the pointer variant is a drag source and never calls it. */
  onAddText?: () => void;
  /** Presence shows the effect tool. */
  onCreateEffect?: () => void;
  effectLabel: string;
  /** Presence shows the animation tool. */
  onCreateAnimation?: () => void;
  animationLabel: string;
  /** Pointer variant only: the effect tool is a drag source (an effect layer dropped on a track) instead of a prompt button. */
  effectDragSource?: boolean;
}

/**
 * The text / effect / animation create tools. One component, two presentations and three hosts: the
 * canvas footer (desktop and shell-less hosts), the phone's playback row and the tablet toolbar slot.
 */
export function TimelineCreateTools({
  variant,
  host,
  onAddText,
  onCreateEffect,
  effectLabel,
  onCreateAnimation,
  animationLabel,
  effectDragSource = false,
}: TimelineCreateToolsProps) {
  const touch = variant === 'touch';
  const inFooter = host === 'timeline-footer';
  const sizeClass = touch ? TOUCH_TOOL_BUTTON_SIZE_CLASS : POINTER_TOOL_BUTTON_SIZE_CLASS;

  return (
    <div
      data-testid="timeline-tool-buttons"
      data-create-tools-host={host}
      data-shell-interaction={inFooter ? undefined : 'true'}
      className={inFooter
        ? 'pointer-events-none sticky z-30 ml-2 flex shrink-0 gap-1.5 self-center'
        : 'flex shrink-0 items-center gap-1.5'}
      // The shell hosts sit outside the canvas subtree that defines the editor's theme variables, so the
      // cluster carries its own: the tones below resolve wherever it is mounted.
      style={{ ...VIDEO_EDITOR_THEME_VARS, ...(inFooter ? { left: LABEL_WIDTH + 8 } : {}) }}
      onPointerDown={(event) => event.stopPropagation()}
    >
      {onAddText && (touch ? (
        <button
          type="button"
          className={`${TOOL_BUTTON_BASE_CLASS} ${sizeClass} ${TEXT_TOOL_TONE_CLASS}`}
          title="New text"
          aria-label="New text at playhead"
          onClick={onAddText}
        >
          <TextGlyph size={16} />
        </button>
      ) : (
        <div
          draggable
          onDragStart={(event) => {
            event.dataTransfer.setData('text-tool', 'true');
            event.dataTransfer.effectAllowed = 'copy';
          }}
          className={`group/tool ${TOOL_BUTTON_BASE_CLASS} ${sizeClass} cursor-grab active:cursor-grabbing ${TEXT_TOOL_TONE_CLASS}`}
          title="Drag onto timeline to add text"
        >
          <TextGlyph size={12} />
          <span aria-hidden="true" className={TOOL_TOOLTIP_CLASS}>
            New text
          </span>
        </div>
      ))}
      {onCreateEffect && (touch ? (
        <button
          type="button"
          className={`${TOOL_BUTTON_BASE_CLASS} ${sizeClass} ${EFFECT_TOOL_TONE_CLASS}`}
          title="New effect"
          aria-label={effectLabel}
          onClick={onCreateEffect}
        >
          <Layers className="h-4 w-4" />
        </button>
      ) : effectDragSource ? (
        <div
          draggable
          onDragStart={(event) => {
            event.dataTransfer.setData('effect-layer', 'true');
            event.dataTransfer.effectAllowed = 'copy';
          }}
          className={`group/tool ${TOOL_BUTTON_BASE_CLASS} ${sizeClass} cursor-grab active:cursor-grabbing ${EFFECT_TOOL_TONE_CLASS}`}
          title="Drag onto timeline to add an effect layer"
        >
          <Layers className="h-3 w-3" />
          <span aria-hidden="true" className={TOOL_TOOLTIP_CLASS}>
            New effect
          </span>
        </div>
      ) : (
        <button
          type="button"
          className={`group/tool ${TOOL_BUTTON_BASE_CLASS} ${sizeClass} ${EFFECT_TOOL_TONE_CLASS} focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--video-editor-effect-ring-strong)]`}
          title="New effect"
          aria-label={effectLabel}
          onClick={onCreateEffect}
        >
          <Layers className="h-3 w-3" />
          <span aria-hidden="true" className={`${TOOL_TOOLTIP_CLASS} group-focus-visible/tool:opacity-100`}>
            New effect
          </span>
        </button>
      ))}
      {onCreateAnimation && (
        <button
          type="button"
          className={`${TOOL_BUTTON_BASE_CLASS} ${sizeClass} ${SEQUENCE_TOOL_TONE_CLASS} focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--video-editor-success-focus-ring)]`}
          title={animationLabel}
          aria-label={animationLabel}
          onClick={onCreateAnimation}
        >
          <Sparkles className={touch ? 'h-4 w-4' : 'h-3 w-3'} />
          {!touch && (
            <span aria-hidden="true" className={`${TOOL_TOOLTIP_CLASS} group-focus-visible/tool:opacity-100`}>
              {animationLabel}
            </span>
          )}
        </button>
      )}
    </div>
  );
}
