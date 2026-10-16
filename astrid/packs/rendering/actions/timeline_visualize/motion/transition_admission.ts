/** Authoring admission after the timing compiler has resolved own frame spans.
 * The host supplies its admitted Composition evaluation API. No local planner,
 * package fallback, timing resolution, legacy rewrite or render is performed.
 */
type Span = {id: string; track: string; start: number; duration: number};
type AuthoredTransition = {
  trackId: string;
  clipId: string;
  transition: {type: string; duration: number; params?: Record<string, unknown>};
};

// Structural port for the two existing shared calls, avoiding an import from
// an unavailable pinned package. This does not claim that package is installed.
type Evaluation<Declaration, Prepared> = {
  declareAppTransition(trackId: string, clipId: string, transition: AuthoredTransition['transition'],
    fps: number, host: string): Declaration;
  prepareDeclaredTrack(trackId: string, clips: readonly Span[], declarations: readonly Declaration[],
    host: string): Prepared;
};

export function prepareAuthoredTransitions<Declaration, Prepared>(
  evaluation: Evaluation<Declaration, Prepared>,
  trackIds: readonly string[],
  resolvedClips: readonly Span[],
  authored: readonly AuthoredTransition[],
  fps: number,
  host: string,
): Array<{trackId: string; prepared: Prepared}> {
  const tracks = new Set(trackIds);
  if (trackIds.length === 0 || tracks.size !== trackIds.length || trackIds.some(id => !id)
      || resolvedClips.some(clip => !tracks.has(clip.track))
      || authored.some(input => !tracks.has(input.trackId))) {
    throw new Error('Transition inputs must name unique declared visual tracks. Next step: supply each owning track once.');
  }
  // Declare every input before returning any plan. Errors from the shared
  // converter/planner retain their exact code and actionable nextStep.
  const declarations = authored.map(input => ({trackId: input.trackId,
    value: evaluation.declareAppTransition(input.trackId, input.clipId, input.transition, fps, host)}));
  return trackIds.map(trackId => ({trackId, prepared: evaluation.prepareDeclaredTrack(
    trackId,
    resolvedClips.filter(clip => clip.track === trackId),
    declarations.filter(declaration => declaration.trackId === trackId).map(declaration => declaration.value),
    host,
  )}));
}
