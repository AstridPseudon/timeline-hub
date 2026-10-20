import { useRef, useSyncExternalStore } from 'react';
import { getAdmittedElementSelection, subscribeAdmittedElements } from '../../runtime/admitted-elements';
import { CodePathParamEditor } from '@/tools/video-editor/components/SequenceCreator/CodePathParamEditor.tsx';
import { useVideoEditorRuntime } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import type { ClipPanelProps } from './ClipPanelBody.tsx';
import { resolveAstridElementParamDescriptor, type AstridElementParamDescriptor } from './astrid-element-param-descriptor.ts';
import { SelectedElementParamFields } from './SelectedElementParamFields.tsx';

/** Editable host-provided parameters for the exact pinned Astrid element revision. */
export function AstridElementParams({
  clip,
  readOnly,
  registry,
  onChange,
  retainedDocumentPin,
  timelineOps,
  commandState,
}: Pick<ClipPanelProps, 'clip' | 'readOnly' | 'registry' | 'onChange' | 'retainedDocumentPin' | 'timelineOps' | 'commandState'>) {
  useSyncExternalStore(subscribeAdmittedElements, getAdmittedElementSelection, getAdmittedElementSelection);
  const runtime = useVideoEditorRuntime();
  const descriptors = runtime.astridElementHost?.descriptors ?? [];
  const retained = useRef<{ clipId: string; descriptor: AstridElementParamDescriptor }>();
  if (retained.current?.clipId !== clip?.id || !retainedDocumentPin) retained.current = undefined;
  const descriptor = resolveAstridElementParamDescriptor(
    clip,
    retainedDocumentPin && retained.current ? [retained.current.descriptor] : descriptors,
    readOnly,
    runtime.timelineEditability,
  );
  // Keep display hints through live pack replacement/removal, never schema authority.
  if (clip && descriptor && retainedDocumentPin && !retained.current) {
    retained.current = { clipId: clip.id, descriptor: structuredClone(descriptor) };
  }
  if (!clip || !descriptor) return null;

  const params = { ...(clip.params ?? {}) };
  const saveParams = (nextParams: Record<string, unknown>) => {
    if (readOnly) return;
    const currentDescriptor = resolveAstridElementParamDescriptor(
      clip,
      runtime.astridElementHost?.descriptors ?? [],
      readOnly,
      runtime.timelineEditability,
    );
    if (!currentDescriptor
      || currentDescriptor.id !== descriptor.id
      || currentDescriptor.kind !== descriptor.kind
      || currentDescriptor.packId !== descriptor.packId
      || currentDescriptor.revision !== descriptor.revision) return;
    onChange({ params: { ...params, ...nextParams } });
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
      </div>
      {retainedDocumentPin ? <SelectedElementParamFields
        key={clip.id}
        clip={clip}
        descriptor={descriptor}
        retainedDocumentPin={retainedDocumentPin}
        timelineOps={timelineOps}
        commandState={commandState}
      /> : <CodePathParamEditor
        schemaJson={descriptor.schema}
        values={params}
        allowedAssetKeys={Object.keys(registry)}
        onChange={saveParams}
      />}
    </section>
  );
}

export type { AstridElementParamDescriptor } from './astrid-element-param-descriptor.ts';
