import { useEffect, useMemo, useState, useSyncExternalStore } from 'react';
import { getAdmittedElementSelection, subscribeAdmittedElements } from '../../runtime/admitted-elements';
import { CodePathParamEditor } from '@/tools/video-editor/components/SequenceCreator/CodePathParamEditor.tsx';
import { useVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { useTimelineEditorDataSafe, useTimelineEditorOpsSafe } from '@/tools/video-editor/hooks/timelineStore.ts';
import { captureClipElementEdit, submitClipElementEdit } from '@/tools/video-editor/commands/elementGesture.ts';
import { captureClipParamsEdit, submitClipParamsEdit } from '@/tools/video-editor/commands/clipParamsGesture.ts';
import type { JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import type { ClipPanelProps } from './ClipPanelBody.tsx';
import { resolveAstridElementParamDescriptor } from './astrid-element-param-descriptor.ts';

/** Editable host-provided parameters for the exact pinned Astrid element revision. */
export function AstridElementParams({
  clip,
  readOnly,
  registry,
  onChange: _onChange,
  selectedParam: selectedParamProp,
}: Pick<ClipPanelProps, 'clip' | 'readOnly' | 'registry' | 'onChange' | 'selectedParam'>) {
  useSyncExternalStore(subscribeAdmittedElements, getAdmittedElementSelection, getAdmittedElementSelection);
  const runtime = useVideoEditorRuntime();
  const editorData = useTimelineEditorDataSafe();
  const editorOps = useTimelineEditorOpsSafe();
  const descriptors = runtime.astridElementHost?.descriptors ?? [];
  const descriptor = resolveAstridElementParamDescriptor(
    clip,
    descriptors,
    readOnly,
    runtime.timelineEditability,
  );
  const params = useMemo(() => ({ ...(clip?.params ?? {}) }), [clip?.params]);
  const [draftParams, setDraftParams] = useState(params);
  const [paramError, setParamError] = useState<string | null>(null);
  useEffect(() => { setDraftParams(params); }, [clip?.id, descriptor?.id, descriptor?.revision, params]);
  if (!clip || !descriptor) return null;
  const reference = clip.elementRef;
  const saveParams = (nextParams: Record<string, unknown>) => {
    if (readOnly) return;
    const currentDescriptor = resolveAstridElementParamDescriptor(
      clip,
      runtime.astridElementHost?.descriptors ?? [],
      readOnly,
      runtime.timelineEditability,
    );
    const next = { params: { ...draftParams, ...nextParams } };
    if (!currentDescriptor
      || currentDescriptor.id !== descriptor.id
      || currentDescriptor.kind !== descriptor.kind
      || currentDescriptor.packId !== descriptor.packId
      || currentDescriptor.revision !== descriptor.revision) {
      setDraftParams(next.params);
      setParamError('The element schema changed; this draft was not saved.');
      return;
    }
    if (reference?.packId) {
      setDraftParams(next.params);
      setParamError(null);
      const port = selectedParamProp ?? editorOps?.selectedParam;
      const current = editorData?.data;
      if (!port || !current || !port.resolveAuthority) {
        setParamError('Selected PARAM schema carrier is unavailable; Agent retained-read support is required');
        return;
      }
      void (async () => {
        const identity = (clip as unknown as { app?: { canonical?: { clipRef?: string } } }).app?.canonical;
        const select = identity?.clipRef ?? `parent/clip:${clip.id}`;
        const pin = port.resolveAuthority!({ select, rawClip: clip as unknown as Record<string, unknown> });
        const captured = captureClipParamsEdit(port, current, clip.id);
        await captured.port.prefetch?.(captured.basis, pin);
        submitClipParamsEdit(captured, {
          values: next.params as Record<string, JSON>,
          clear: [],
          schema_source: pin,
        });
      })().catch((error) => {
        setParamError(error instanceof Error ? error.message : String(error));
        console.error('[AstridElementParams] Selected PARAM edit was refused; draft preserved', error);
      });
      return;
    }
    if (!reference?.packId) {
      setDraftParams(next.params);
      setParamError(null);
      if (!editorData?.data || !editorOps?.element) {
        setParamError('Literal PARAM native capture is unavailable; draft preserved.');
        return;
      }
      const edit = { params: { values: next.params as Record<string, JSON>, clear: [] } };
      try {
        const captured = captureClipElementEdit(editorOps.element, editorData.data, clip.id, edit);
        submitClipElementEdit(captured, edit);
      } catch (error) {
        setParamError(error instanceof Error ? error.message : String(error));
        console.error('[AstridElementParams] Literal PARAM edit was refused; draft preserved', error);
      }
      return;
    }
  };

  const schemaTitle = (descriptor.schema as { title?: unknown }).title;
  const label = typeof schemaTitle === 'string' && schemaTitle.length > 0
    ? schemaTitle
    : descriptor.id;

  return (
    <section
      className="mt-3 space-y-2 rounded-xl border border-border bg-card/70 p-3"
      data-testid="astrid-element-params"
    >
      <div>
        <h3 className="text-sm font-medium text-foreground">{label} parameters</h3>
        <p className="text-xs text-muted-foreground">Values save with this pinned element revision.</p>
        {paramError && (
          <p
            role="alert"
            data-testid={reference?.packId ? 'astrid-selected-param-error' : 'astrid-element-param-error'}
            className="text-xs text-destructive"
          >{paramError}</p>
        )}
      </div>
      <CodePathParamEditor
        schemaJson={descriptor.schema}
        values={draftParams}
        allowedAssetKeys={Object.keys(registry)}
        onChange={saveParams}
      />
    </section>
  );
}

export type { AstridElementParamDescriptor } from './astrid-element-param-descriptor.ts';
