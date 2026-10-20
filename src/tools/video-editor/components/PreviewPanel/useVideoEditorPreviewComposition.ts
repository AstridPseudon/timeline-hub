import { useMemo } from 'react';
import { useOptionalVideoEditorRuntime } from '../../contexts/VideoEditorRuntimeContext.tsx';
import { resolveCanonicalComposition } from '../../data/canonicalCompositionState.ts';
import { projectOutputTimelineConfig } from '../../data/timelineOutputProjection.ts';
import type { TimelineData } from '../../lib/timeline-data.ts';
import type { ResolvedTimelineConfig } from '../../types/index.ts';

/** Both the stage and panel stills include in-progress edits inside placed shots. */
export function useVideoEditorPreviewComposition(
  resolvedConfig: ResolvedTimelineConfig | null | undefined,
  timelineData?: TimelineData | null,
) {
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
  const projectedConfig = timelineData?.editProjection ? timelineData.resolvedConfig : null;
  return useMemo(() => {
    if (!projectedConfig) return canonical;
    // Command acceptance already flattens the returned pinned closure. Shot
    // shells would load unrelated latest children; they cannot carry its fact.
    const output = projectOutputTimelineConfig(projectedConfig).config;
    const complete = output.clips.every((clip) => clip.clipType !== 'shot'
      && (!(clip.asset || clip.clipType === 'media') || Boolean(clip.assetEntry?.src)));
    // The command producer pairs this config with its canonical projection
    // fact, independently of whether an older shot graph has loaded.
    if (complete) return { source: 'canonical' as const, status: 'ready' as const, config: projectedConfig, error: null };
    const cached = canonical.source === 'canonical' ? canonical.config : null;
    return {
      ...canonical,
      status: cached ? 'ready' as const : 'error' as const,
      config: cached,
      error: new Error('The command projection has unresolved shot content or media.'),
    };
  }, [canonical, projectedConfig]);
}
