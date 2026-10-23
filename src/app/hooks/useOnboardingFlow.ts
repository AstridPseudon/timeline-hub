import { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { normalizeAndPresentError } from '@/shared/lib/errorHandling/runtimeError';
import { useOnboarding } from '@/shared/hooks/useOnboarding';
import {
  checkAstridDoctorAvailability,
  type AstridDoctorAvailability,
} from '@/integrations/astrid/doctorAvailability.ts';
import { getBridgeRecoveryGuidance } from '@/integrations/astrid/bridgeRecovery.ts';
import { hasRuntimeDocumentIdentity } from '@/app/runtime/runtimeDocument';
import { APP_ENTRY_PATH } from '@/app/entryClassification';

export function useOnboardingFlow() {
  const { showOnboardingModal, onboardingMode, closeOnboardingModal } = useOnboarding();
  const navigate = useNavigate();
  const availabilityRequestRef = useRef(0);
  const [doctorAvailability, setDoctorAvailability] = useState<AstridDoctorAvailability>({
    status: 'checking',
  });

  const refreshDoctorAvailability = useCallback(async () => {
    const requestVersion = ++availabilityRequestRef.current;
    setDoctorAvailability({ status: 'checking' });
    const result = await checkAstridDoctorAvailability();
    if (availabilityRequestRef.current === requestVersion) {
      setDoctorAvailability(result);
    }
    return result;
  }, []);

  // The shots pack has no v1 route, so a "Getting Started" shot cannot
  // be chosen in local mode. Check the doctor-owned
  // runtime instead, then enter the tool without fabricating a shot identity.
  const handleOnboardingClose = useCallback(async () => {
    // Coming back to a Runtime that had stopped: the person was mid-work, so just return them to it.
    if (onboardingMode === 'reconnect' || hasRuntimeDocumentIdentity(window.location.search)) {
      closeOnboardingModal();
      return;
    }
    const availability = await refreshDoctorAvailability();
    if (availability.status === 'unavailable') {
      const recovery = getBridgeRecoveryGuidance('capability_unavailable');
      normalizeAndPresentError(
        new Error(`${availability.reason}. ${recovery.nextAction}`),
        {
          context: 'useOnboardingFlow.doctorUnavailable',
          showToast: true,
        },
      );
      return;
    }

    closeOnboardingModal();
    navigate(APP_ENTRY_PATH);
  }, [closeOnboardingModal, navigate, onboardingMode, refreshDoctorAvailability]);

  useEffect(() => {
    if (showOnboardingModal) {
      void refreshDoctorAvailability();
    }
  }, [refreshDoctorAvailability, showOnboardingModal]);

  useEffect(() => () => {
    availabilityRequestRef.current += 1;
  }, []);

  return {
    showOnboardingModal,
    onboardingMode,
    handleOnboardingClose,
    doctorAvailability,
  };
}
