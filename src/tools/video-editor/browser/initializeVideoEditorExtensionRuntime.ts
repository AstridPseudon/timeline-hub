import {
  installExtensionOperationalAnalyticsSink,
} from '../runtime/extensionOperationalAnalytics.ts';

export interface InitializeVideoEditorExtensionRuntimeOptions {
  readonly development: boolean;
}

/**
 * Initialize the browser-owned extension runtime before the host renders.
 *
 * Operational analytics remains best-effort. There is no release config to wait
 * for: the extension host ships on. Keeping this composition behind the browser contract prevents
 * app shells from depending on video-editor runtime internals.
 */
export function initializeVideoEditorExtensionRuntime(
  _options?: InitializeVideoEditorExtensionRuntimeOptions,
): void {
  installExtensionOperationalAnalyticsSink();
}
