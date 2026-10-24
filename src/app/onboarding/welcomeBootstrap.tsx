import { createRoot } from 'react-dom/client';
import { AppErrorBoundary } from '@/app/components/error/AppErrorBoundary.tsx';
import { applyAppTheme, appThemeDarkness, readStoredAppThemeTime } from '@/shared/hooks/core/useAppTheme.ts';
import { WelcomeFlow } from './WelcomeFlow.tsx';
import '@/index.css';

export function renderWelcome(root: HTMLElement): void {
  // The boundary's screen uses theme tokens; paint the stored/time-of-day theme as the app does.
  applyAppTheme(appThemeDarkness(readStoredAppThemeTime()));
  createRoot(root).render(<AppErrorBoundary><WelcomeFlow /></AppErrorBoundary>);
}
