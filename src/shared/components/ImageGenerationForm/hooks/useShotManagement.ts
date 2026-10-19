import { useEffect, useRef, useCallback } from 'react';
import { useAutoSaveSettings } from '@/shared/settings/hooks/useAutoSaveSettings';
import { useListShots } from '@/shared/hooks/shots';
import { useShotCreation } from '@/shared/hooks/shotCreation/useShotCreation';
import { useShotNavigation } from '@/shared/hooks/shots/useShotNavigation';
import { useQueryClient } from '@tanstack/react-query';
import { shotQueryKeys } from '@/shared/lib/queryKeys/shots';
import { SETTINGS_IDS } from '@/shared/lib/settingsIds';

import type { FormUIActions } from '../state/useFormUIState';
import type { ImageGenShotSettings } from '../types';

// Per-shot prompt settings start empty and are not inherited between shots.
// IMPORTANT: Do NOT default selectedReferenceId to null: null is treated as an explicit
// override and would suppress the project-level per-shot selection mapping
// (selectedReferenceIdByShot), leading to "no selection" and jitter/jumps when the user clicks.
const SHOT_PROMPT_DEFAULTS: ImageGenShotSettings = { prompts: [] };

interface UseShotManagementProps {
  selectedProjectId: string | null;
  associatedShotId: string | null;
  setAssociatedShotId: (id: string | null) => void;
  ready: boolean;
  markAsInteracted: () => void;
  onShotChange?: (shotId: string | null) => void;
  initialShotId?: string | null;
  uiActions: FormUIActions;
}

export function useShotManagement({
  selectedProjectId,
  associatedShotId,
  setAssociatedShotId,
  ready,
  markAsInteracted,
  onShotChange,
  initialShotId,
  uiActions,
}: UseShotManagementProps) {
  const queryClient = useQueryClient();

  const { data: shots } = useListShots(selectedProjectId);
  const { createShot, isCreating: isCreatingShot } = useShotCreation();
  const { navigateToShot } = useShotNavigation();

  // Shot-specific prompts using per-shot storage
  const shotPromptSettings = useAutoSaveSettings<ImageGenShotSettings>({
    toolId: SETTINGS_IDS.IMAGE_GEN_PROMPTS,
    shotId: associatedShotId,
    projectId: selectedProjectId,
    scope: 'shot',
    defaults: SHOT_PROMPT_DEFAULTS,
    enabled: !!associatedShotId,
  });

  // Apply initialShotId once after hydration (takes precedence over persisted value)
  // If initialShotId is explicitly null, reset to None (opened from outside shot context)
  // IMPORTANT: Do NOT call markAsInteracted() here - initialShotId is a temporary context
  // override (e.g., from modal opened in shot context), not a user preference to persist.
  // The tool page's persisted shot selection should only change when explicitly changed by user.
  const hasAppliedInitialShotId = useRef(false);
  useEffect(() => {
    // Only apply once, after hydration is complete
    // Only override when initialShotId is a specific shot ID (truthy string)
    // null or undefined = keep the persisted value from project settings
    if (ready && !hasAppliedInitialShotId.current && shots) {
      if (initialShotId) {
        // initialShotId was provided as a specific shot - set to that shot if it exists
        const shotExists = shots.some(shot => shot.id === initialShotId);
        if (shotExists && associatedShotId !== initialShotId) {
          setAssociatedShotId(initialShotId);
          // Don't persist - this is a temporary context override
        }
      }
      // If initialShotId is null/undefined, keep the persisted value from project settings
      hasAppliedInitialShotId.current = true;
    }
  }, [ready, initialShotId, shots, associatedShotId, setAssociatedShotId]);

  // Reset associatedShotId if the selected shot no longer exists (e.g., was deleted)
  useEffect(() => {
    if (associatedShotId && shots) {
      const shotExists = shots.some(shot => shot.id === associatedShotId);
      if (!shotExists) {
        setAssociatedShotId(null);
        markAsInteracted();
      }
    }
  }, [associatedShotId, shots, markAsInteracted, setAssociatedShotId]);

  // Handle shot change with proper prompt initialization
  const handleShotChange = useCallback((value: string) => {
    markAsInteracted();
    const newShotId = value === "none" ? null : value;

    // usePersistentToolState auto-syncs associatedShotId to DB
    setAssociatedShotId(newShotId);

    // Call the parent callback if provided
    if (onShotChange) {
      onShotChange(newShotId);
    }

    // Note: Prompts for the new shot will be loaded automatically via useAutoSaveSettings
    // and initialized if empty via the initialization effect
  }, [markAsInteracted, onShotChange, setAssociatedShotId]);

  // Handle creating a new shot
  const handleCreateShot = useCallback(async (shotName: string, files: File[]) => {
    // Use unified shot creation - handles inheritance, events, lastAffected automatically
    const result = await createShot({
      name: shotName,
      files: files.length > 0 ? files : undefined,
      dispatchSkeletonEvents: false, // No skeleton needed in form context
      onSuccess: () => {
        // Invalidate and refetch shots to update the list
        const projectShotKey = [...shotQueryKeys.all, selectedProjectId!];
        queryClient.invalidateQueries({ queryKey: projectShotKey });
        queryClient.refetchQueries({ queryKey: projectShotKey });
      },
    });

    if (!result) {
      // Error already shown by useShotCreation
      return;
    }

    // Note: Settings inheritance is handled automatically by useShotCreation

    // Switch to the newly created shot
    markAsInteracted();
    setAssociatedShotId(result.shotId);
    uiActions.setCreateShotModalOpen(false);
  }, [createShot, markAsInteracted, queryClient, selectedProjectId, uiActions, setAssociatedShotId]);

  return {
    shots,
    shotPromptSettings,
    isCreatingShot,
    navigateToShot,
    handleShotChange,
    handleCreateShot,
  };
}
