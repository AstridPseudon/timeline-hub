import type { EditCommand } from '@/integrations/runtime/generated.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { attachGestureCommands, gestureCommandsFor, occurrenceIdentityFor } from './semanticGestures.ts';
import { positionResetFields } from './positionReset.ts';

const paths = Object.values(positionResetFields);
const keys = Object.keys(positionResetFields);
const scoped = (value: string): boolean => /^(?:parent|occurrence:[^/\s]+)\/clip:[^/\s]+$/.test(value);

/** Capture every guard and owner before the handler makes its optimistic edit.
 * Refuse the whole selection when the existing atomic route cannot bind it. */
export function positionResetCommands(data: TimelineData, ids: readonly string[]): EditCommand[] | undefined {
  if (!ids.length || new Set(ids).size !== ids.length) return undefined;
  const commands: EditCommand[] = [];
  for (const id of ids) {
    const clips = data.config.clips.filter(clip => clip.id === id);
    if (clips.length !== 1 || id.startsWith('uploading-')) return undefined;
    const clip = clips[0];
    if (data.tracks.find(track => track.id === clip.track)?.kind === 'audio') return undefined;
    const identity = occurrenceIdentityFor(data, id);
    if (clip.app?.canonical && !identity) return undefined;
    const select = identity ? `occurrence:${identity.occurrenceId}/clip:${identity.sourceClipId}` : `parent/clip:${id}`;
    if (!scoped(select)) return undefined;
    const source = (identity?.sourceClip ?? clip) as unknown as Record<string, unknown>;
    const expect: NonNullable<EditCommand['expect']> = {};
    for (const path of paths) {
      const value = source[path];
      if (value !== undefined && value !== null && (typeof value !== 'number' || !Number.isFinite(value))) return undefined;
      expect[path] = Object.prototype.hasOwnProperty.call(source, path) && value !== undefined
        ? { state: 'present', value: structuredClone(value) } : { state: 'absent' };
    }
    commands.push({ op: 'clip.clear', select, resolved: [select], args: { keys: [...keys] }, expect });
  }
  // Reuse the same captured occurrence routing check as the actual commit path.
  const captured = { ...data };
  attachGestureCommands(captured, commands, data);
  return gestureCommandsFor(captured) ? commands : undefined;
}
