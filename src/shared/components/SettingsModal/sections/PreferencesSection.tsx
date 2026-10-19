import React from "react";
import { TimeOfDayControl } from "@/shared/components/TimeOfDay/TimeOfDayControl";
import type { PreferencesSectionProps } from "../types";

const PreferencesSection: React.FC<PreferencesSectionProps> = ({
  isMobile,
  preserveUserText,
  setPreserveUserText,
}) => {
  return (
    <div className="space-y-6">
      {/* Appearance Subsection */}
      <div>
        <h3 className="text-sm font-medium text-muted-foreground mb-3">Appearance</h3>
        <div className={`${isMobile ? 'p-3' : 'p-4'} bg-muted/30 rounded-lg space-y-2`}>
          <span className="font-medium">Brightness:</span>
          <TimeOfDayControl compact />
        </div>

        {/* User Text Case Toggle */}
        <div className={`${isMobile ? 'p-3' : 'p-4'} bg-muted/30 rounded-lg space-y-2 mt-3`}>
          <div className={`flex ${isMobile ? 'flex-col gap-2' : 'items-center justify-between'}`}>
            <span className="font-medium">User Text:</span>
            <div className="flex items-center gap-0">
              <button
                onClick={() => setPreserveUserText(false)}
                className={`${isMobile ? 'px-2 py-1 text-xs' : 'px-3 py-1.5 text-sm'} rounded-l-full transition-all ${
                  !preserveUserText
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted text-muted-foreground hover:bg-muted/80'
                }`}
              >
                all lowercase
              </button>
              <button
                onClick={() => setPreserveUserText(true)}
                className={`${isMobile ? 'px-2 py-1 text-xs' : 'px-3 py-1.5 text-sm'} rounded-r-full transition-all verbatim-case ${
                  preserveUserText
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted text-muted-foreground hover:bg-muted/80'
                }`}
              >
                Original case
              </button>
            </div>
          </div>
          <p className="text-xs text-muted-foreground">
            How project names, shot names, and prompts are displayed
          </p>
        </div>

      </div>

    </div>
  );
};

export { PreferencesSection };
