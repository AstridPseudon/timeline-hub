import React from "react";
import { Plus } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/shared/components/ui/tooltip";
import { cn } from '@/shared/components/ui/contracts/cn';
import { COARSE_TOUCH_TARGET } from '@/shared/components/ui/contracts/touchTarget';

interface AddToTimelineButtonProps {
  generationId: string;
  onAddToTimeline: (generationId: string) => void;
  /** When set, adding is refused: the button is disabled and this explains why. */
  disabledReason?: string;
  /** On a coarse pointer (touch) the control is only shown on the selected tile. */
  isSelected: boolean;
}

/**
 * Round "+" control on a gallery tile. Desktop: shown on tile hover or keyboard focus.
 * Touch: shown on the selected tile only. A tap here is an add, not a tile tap, so it does
 * not reach the tile's touch or click handlers.
 */
export const AddToTimelineButton: React.FC<AddToTimelineButtonProps> = ({
  generationId,
  onAddToTimeline,
  disabledReason,
  isSelected,
}) => {
  const disabled = Boolean(disabledReason);
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span className="inline-flex">
          <button
            type="button"
            aria-label="Add to timeline"
            disabled={disabled}
            onClick={(event) => {
              event.stopPropagation();
              if (disabled) return;
              onAddToTimeline(generationId);
            }}
            onTouchStart={(event) => event.stopPropagation()}
            onTouchEnd={(event) => event.stopPropagation()}
            className={cn(
              "h-7 w-7 p-0 rounded-full bg-black/50 hover:bg-black/70 text-white flex items-center justify-center transition-opacity",
              "opacity-0 group-hover:opacity-100 group-focus-within:opacity-100",
              isSelected && "[@media(pointer:coarse)]:opacity-100",
              "disabled:cursor-not-allowed disabled:opacity-40",
              COARSE_TOUCH_TARGET,
            )}
            data-testid="gallery-tile-add-to-timeline"
          >
            <Plus className="h-3.5 w-3.5" />
          </button>
        </span>
      </TooltipTrigger>
      <TooltipContent side="bottom" align="end">
        {disabled ? disabledReason : "Add to timeline"}
      </TooltipContent>
    </Tooltip>
  );
};
