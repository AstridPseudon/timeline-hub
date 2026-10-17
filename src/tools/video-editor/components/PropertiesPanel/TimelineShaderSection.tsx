import { useState } from 'react';
import type { ResolvedTimelineConfig } from '../../types/index.ts';
import type { TimelineApplyEdit } from '../../hooks/timeline-state-types.ts';
import { useShaderEffectRegistrySnapshot } from '../../shaders/registry/ShaderEffectRegistryContext.tsx';
import { createTimelinePostprocessShaderMetadata, getShaderPassKind, NO_SHADER } from '../../lib/shader-catalog.ts';
import { selectedShaderRecord, shaderSlotCommand } from '../../commands/shaderSlots.ts';

/** Timeline ownership is explicit: this surface mounts only with no clip/track selection. */
export function TimelineShaderSection({ config, applyEdit }: { config: ResolvedTimelineConfig; applyEdit: TimelineApplyEdit }) {
  const snapshot = useShaderEffectRegistrySnapshot();
  const [message, setMessage] = useState('');
  const shader = config.app?.shaderPostprocess;
  const key = (owner: string, contribution: string, id: string) => JSON.stringify([owner, contribution, id]);
  return <section data-testid="timeline-shader-section">
    <label>Timeline postprocess shader
      <select aria-label="Timeline postprocess shader" value={shader ? key(shader.extensionId, shader.contributionId, shader.shaderId) : NO_SHADER} onChange={event => {
        const record = snapshot.records.find(r => key(r.ownerExtensionId ?? '', r.contributionId, r.shaderId) === event.target.value);
        const next = event.target.value === NO_SHADER ? null : record ? createTimelinePostprocessShaderMetadata(record) : undefined;
        if (next === undefined) return;
        const command = shaderSlotCommand({ id: 'parent', value: config }, next, snapshot);
        if (!command) { setMessage('The selected shader is unavailable or does not match this timeline slot.'); return; }
        const app = { ...config.app }; if (next === null) delete app.shaderPostprocess; else app.shaderPostprocess = next;
        setMessage('');
        applyEdit({ type: 'config', resolvedConfig: { ...config, app } }, { selectedClipId: null, selectedTrackId: null, editCommands: [command] });
      }}>
        <option value={NO_SHADER}>None</option>
        {shader && !selectedShaderRecord(shader, 'postprocess', snapshot) && <option value={key(shader.extensionId, shader.contributionId, shader.shaderId)}>Unavailable: {shader.label ?? shader.shaderId}</option>}
        {snapshot.records.filter(record => getShaderPassKind(record) === 'postprocess').map(record => {
          const metadata = createTimelinePostprocessShaderMetadata(record);
          return <option key={key(metadata.extensionId, metadata.contributionId, metadata.shaderId)} value={key(metadata.extensionId, metadata.contributionId, metadata.shaderId)} disabled={!selectedShaderRecord(metadata, 'postprocess', snapshot)}>{record.label}</option>;
        })}
      </select>
    </label>
    {message && <p role="alert">{message}</p>}
  </section>;
}
