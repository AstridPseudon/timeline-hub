import { useMemo } from 'react';
import { compilePlayerTransitions } from '../../compositions/playerEvaluation.ts';
import type { CompiledCanonicalTransitions } from '@banodoco/timeline-composition';
import { useOptionalVideoEditorRuntime } from '../../contexts/VideoEditorRuntimeContext.tsx';
import { resolveCanonicalComposition } from '../../data/canonicalCompositionState.ts';
import { projectOutputTimelineConfig } from '../../data/timelineOutputProjection.ts';
import { boundCanonicalConfigClips } from '../../lib/canonicalRenderBounds.ts';
import type { TimelineData } from '../../lib/timeline-data.ts';
import type { ResolvedTimelineConfig } from '../../types/index.ts';

type PreviewCompositionResolution = ReturnType<typeof resolveCanonicalComposition> & {
  /** The exact config/fact pair selected for delivery, including its private copy. */
  pairedConfig: ResolvedTimelineConfig | null;
  /** One compiled vector shared by Player, client render, and panel stills. */
  compiledTransitions?: CompiledCanonicalTransitions;
};

function hasStoredOccurrenceCap(config: ResolvedTimelineConfig): boolean {
  return config.clips.some((clip) => {
    const timing = clip.app?.canonicalTiming;
    const stored = timing && typeof timing === 'object' && !Array.isArray(timing)
      ? (timing as Record<string, unknown>).storedOccurrenceDurationMs
      : undefined;
    const effective = timing && typeof timing === 'object' && !Array.isArray(timing)
      ? (timing as Record<string, unknown>).occurrenceDurationMs
      : undefined;
    return typeof stored === 'number' && Number.isFinite(stored) && stored >= 0
      && typeof effective === 'number' && Number.isFinite(effective) && stored < effective;
  });
}

/** Both the stage and panel stills include in-progress edits inside placed shots. */
export function useVideoEditorPreviewComposition(
  resolvedConfig: ResolvedTimelineConfig | null | undefined,
  timelineData?: TimelineData | null,
): PreviewCompositionResolution {
  const runtime = useOptionalVideoEditorRuntime();
  const hasShotClips = Boolean(resolvedConfig?.clips.some((clip) => clip.clipType === 'shot'));
  const composition = runtime?.userId === null
    ? runtime.shots?.canonicalDraft?.composition ?? runtime.shots?.canonicalComposition
    : null;
  const compositionError = runtime?.userId === null ? runtime.shots?.canonicalCompositionError : null;
  const compositionErrorDependency = composition ? null : compositionError;
  const canonical = useMemo(() => resolveCanonicalComposition({
    userId: runtime?.userId,
    hasShotClips,
    hasShotComposition: Boolean(runtime?.shots?.shotComposition),
    composition,
    compositionError: compositionErrorDependency,
    baseConfig: resolvedConfig,
  }), [hasShotClips, composition, compositionErrorDependency, resolvedConfig,
    runtime?.shots?.shotComposition, runtime?.userId]);
  const projectionFact = timelineData?.editProjection;
  const projectedConfig = projectionFact ? timelineData.resolvedConfig : null;
  const resolution = useMemo(() => {
    if (!projectionFact || !projectedConfig) return { ...canonical, pairedConfig: null };
    // Command acceptance already flattens the returned pinned closure. Shot
    // shells would load unrelated latest children; they cannot carry its fact.
    const output = projectOutputTimelineConfig(projectedConfig).config;
    const complete = output.clips.every((clip) => clip.clipType !== 'shot'
      && (!(clip.asset || clip.clipType === 'media') || Boolean(clip.assetEntry?.src)));
    // The command producer pairs this config with its canonical projection
    // fact, independently of whether an older shot graph has loaded.
    if (complete) {
      const config = hasStoredOccurrenceCap(projectedConfig)
        ? { ...projectedConfig, clips: boundCanonicalConfigClips(projectedConfig.clips, 'stored') }
        : projectedConfig;
      return {
        source: 'canonical' as const,
        status: 'ready' as const,
        config,
        pairedConfig: config,
        error: null,
      };
    }
    const cached = canonical.source === 'canonical' ? canonical.config : null;
    return {
      ...canonical,
      status: cached ? 'ready' as const : 'error' as const,
      config: cached,
      pairedConfig: null,
      error: new Error('The command projection has unresolved shot content or media.'),
    };
  }, [canonical, projectionFact, projectedConfig]);
  const compiledTransitions = useMemo(() => resolution.source === 'canonical' && resolution.config
    ? compilePlayerTransitions(resolution.config) : undefined, [resolution.config, resolution.source]);
  return useMemo(() => ({ ...resolution, compiledTransitions }), [compiledTransitions, resolution]);
}
