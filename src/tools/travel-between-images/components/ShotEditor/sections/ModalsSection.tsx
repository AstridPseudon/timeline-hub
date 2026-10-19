/**
 * ModalsSection - Renders all modals used by ShotSettingsEditor
 *
 * Keeps modal rendering separate from main component logic.
 */

import React from 'react';
import { SettingsModal } from '@/shared/components/SettingsModal/SettingsModal';
import { useTextCase } from '@/shared/hooks/useTextCase';

interface ModalsSectionProps {
  // Settings modal
  isSettingsModalOpen: boolean;
  onSettingsModalOpenChange: (open: boolean) => void;
}

export const ModalsSection: React.FC<ModalsSectionProps> = ({
  isSettingsModalOpen,
  onSettingsModalOpenChange,
}) => {
  const { preserveUserText, setPreserveUserText } = useTextCase();

  return (
    <SettingsModal
      isOpen={isSettingsModalOpen}
      onOpenChange={onSettingsModalOpenChange}
      preserveUserText={preserveUserText}
      setPreserveUserText={setPreserveUserText}
    />
  );
};
