import { Layers, Sparkles } from 'lucide-react';

/** The prompts the effect and animation tools hand to the agent composer. One definition, shared by the
 *  canvas handlers and the shell's sequence-creator entry, so the two cannot drift apart. */
export const CREATE_EFFECT_PROMPT = "I'd like to create a new effect.";
export const CREATE_ANIMATION_PROMPT = "I'd like to create an animation.";

const TOOL_BUTTON_BASE_CLASS = 'pointer-events-auto relative flex items-center justify-center rounded-full ring-1 transition-all duration-150 hover:-translate-y-0.5 hover:scale-105 active:translate-y-0 active:scale-100';
const TOOL_BUTTON_SIZE_CLASS = 'h-6 w-6';
const TEXT_TOOL_TONE_CLASS = 'bg-[var(--video-editor-accent-bg-strong)] text-foreground ring-[var(--video-editor-accent-ring)] hover:bg-[var(--video-editor-accent-bg-hover)] hover:shadow-[0_6px_18px_var(--video-editor-accent-shadow-soft)] hover:ring-[var(--video-editor-accent-border)]';
const EFFECT_TOOL_TONE_CLASS = 'bg-[var(--video-editor-effect-bg)] text-foreground ring-[var(--video-editor-effect-ring)] hover:bg-[var(--video-editor-effect-bg-hover)] hover:shadow-[0_6px_18px_var(--video-editor-effect-shadow-soft)] hover:ring-[var(--video-editor-effect-ring-strong)]';
const SEQUENCE_TOOL_TONE_CLASS = 'bg-[var(--video-editor-success-bg)] text-foreground ring-[var(--video-editor-success-ring)] hover:bg-[var(--video-editor-success-bg-hover)] hover:shadow-[0_6px_18px_var(--video-editor-success-shadow-soft)] hover:ring-[var(--video-editor-success-ring-strong)]';
const TOOL_TOOLTIP_CLASS = 'pointer-events-none absolute bottom-full left-1/2 mb-2 -translate-x-1/2 whitespace-nowrap rounded-md border border-border bg-popover px-2 py-1 text-[11px] font-medium text-popover-foreground opacity-0 shadow-md transition-opacity group-hover/tool:opacity-100';

export interface TimelineCreateToolsProps {
  /** Width of the sticky track-name column (the timeline's `startLeft`): the cluster sits just right of it. */
  labelWidth: number;
  /** Shows the text tool: an HTML5 drag source dropped on a track. */
  showTextTool?: boolean;
  /** Presence shows the effect tool. */
  onCreateEffect?: () => void;
  effectLabel: string;
  /** Presence shows the animation tool. */
  onCreateAnimation?: () => void;
  animationLabel: string;
  /** The effect tool is a drag source (an effect layer dropped on a track) instead of a prompt button. */
  effectDragSource?: boolean;
}

/**
 * The text / effect / animation create tools in the canvas footer: 24px pointer tools, desktop only. They are
 * in the layout flow under the last track, so no track is ever under a button. Touch has no create tools
 * (adding elements is the agent's job there).
 */
export function TimelineCreateTools({
  labelWidth,
  showTextTool = false,
  onCreateEffect,
  effectLabel,
  onCreateAnimation,
  animationLabel,
  effectDragSource = false,
}: TimelineCreateToolsProps) {
  return (
    <div
      data-testid="timeline-tool-buttons"
      className="pointer-events-none sticky z-30 ml-2 flex shrink-0 gap-1.5 self-center"
      style={{ left: labelWidth + 8 }}
      onPointerDown={(event) => event.stopPropagation()}
    >
      {showTextTool && (
        <div
          draggable
          onDragStart={(event) => {
            event.dataTransfer.setData('text-tool', 'true');
            event.dataTransfer.effectAllowed = 'copy';
          }}
          className={`group/tool ${TOOL_BUTTON_BASE_CLASS} ${TOOL_BUTTON_SIZE_CLASS} cursor-grab active:cursor-grabbing ${TEXT_TOOL_TONE_CLASS}`}
          title="Drag onto timeline to add text"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/></svg>
          <span aria-hidden="true" className={TOOL_TOOLTIP_CLASS}>
            New text
          </span>
        </div>
      )}
      {onCreateEffect && (effectDragSource ? (
        <div
          draggable
          onDragStart={(event) => {
            event.dataTransfer.setData('effect-layer', 'true');
            event.dataTransfer.effectAllowed = 'copy';
          }}
          className={`group/tool ${TOOL_BUTTON_BASE_CLASS} ${TOOL_BUTTON_SIZE_CLASS} cursor-grab active:cursor-grabbing ${EFFECT_TOOL_TONE_CLASS}`}
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
          className={`group/tool ${TOOL_BUTTON_BASE_CLASS} ${TOOL_BUTTON_SIZE_CLASS} ${EFFECT_TOOL_TONE_CLASS} focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--video-editor-effect-ring-strong)]`}
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
          className={`${TOOL_BUTTON_BASE_CLASS} ${TOOL_BUTTON_SIZE_CLASS} ${SEQUENCE_TOOL_TONE_CLASS} focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--video-editor-success-focus-ring)]`}
          title={animationLabel}
          aria-label={animationLabel}
          onClick={onCreateAnimation}
        >
          <Sparkles className="h-3 w-3" />
          <span aria-hidden="true" className={`${TOOL_TOOLTIP_CLASS} group-focus-visible/tool:opacity-100`}>
            {animationLabel}
          </span>
        </button>
      )}
    </div>
  );
}
