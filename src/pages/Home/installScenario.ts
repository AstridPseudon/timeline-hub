import {
  detectBrowser,
  detectDeviceType,
  detectPlatform,
  detectSafariPwaSupport,
  isDesktopPlatform,
} from '@/shared/hooks/platformInstall/platformDetection';

/** Which explainer to show: each browser installs from a different spot, and phones can't yet. */
export type InstallScenario = 'chromium' | 'safari' | 'unsupported' | 'mobile';

export function detectInstallScenario(): InstallScenario {
  const platform = detectPlatform();
  const browser = detectBrowser();
  if (detectDeviceType(platform) !== 'desktop' || !isDesktopPlatform(platform)) return 'mobile';
  if (browser === 'chrome' || browser === 'edge') return 'chromium';
  if (detectSafariPwaSupport(browser, platform)) return 'safari';
  return 'unsupported';
}

/**
 * Whether this device can't run Astrid (a phone or tablet): the landing page's install dialog and the hosted build's
 * connection gate both ask, so the two always agree on who gets "Desktop only, for now".
 */
export function isMobileDevice(): boolean {
  return detectInstallScenario() === 'mobile';
}

/**
 * The name the connection cards give the person's browser ("Choose Allow in Edge"). The local-network prompt is a
 * Chromium one, so Edge is named as Edge and every other browser as Chrome.
 */
export function installBrowserName(): 'Chrome' | 'Edge' {
  return detectBrowser() === 'edge' ? 'Edge' : 'Chrome';
}
