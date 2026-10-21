/** Temporary, sanitized Gate6 popup diagnostics; keep private to the candidate. */
type PopupPostSelectionDiagnosticDetails = {
  ownerRef?: string;
  trackRef?: string;
  commandOp?: string;
  hasPort?: boolean;
  hasSelection?: boolean;
  hasTarget?: boolean;
  hasSession?: boolean;
};

function diagnosticError(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  return message
    .replace(/https?:\/\/\S+/gi, '[url]')
    .replace(/(?:authorization|cookie|password|secret|token|body)\s*[:=]\s*\S+/gi, '[redacted]')
    .slice(0, 180);
}

export function logPopupPostSelectionDiagnostic(
  boundary: string,
  outcome: 'enter' | 'return' | 'refused' | 'throw',
  details: PopupPostSelectionDiagnosticDetails = {},
  error?: unknown,
): void {
  console.log('[popup-post-selection-diagnostic]', {
    boundary,
    outcome,
    ...details,
    ...(error === undefined ? {} : { error: diagnosticError(error) }),
  });
}
