import type { EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import type { PreparedShotComposition } from '../data/shotCompositionAdapter.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import { freezeJson } from './clipMovePrimitives.ts';
import { captureShotSet, finishShotSet, type ExistingShotSetArgs, type ShotSetBasis } from './shotSetCapture.ts';

export type ShotSetCaptureCurrent = Pick<PreparedShotComposition, 'projectId' | 'parentDocumentId' | 'headRevisionId'>;

export interface ShotSetCapturePort {
  capture(input: { occurrenceId: string; current: ShotSetCaptureCurrent; args?: ExistingShotSetArgs }): JSON;
  finish(basis: JSON, args: ExistingShotSetArgs): { command: EditCommand; bundle: AuthoredBundle };
  submit(input: { command: EditCommand }): void | Promise<void>;
}

export interface CapturedShotSetEdit {
  readonly occurrenceId: string;
  readonly basis: JSON;
  readonly port: ShotSetCapturePort;
}

export function captureShotNameEdit(
  port: ShotSetCapturePort | undefined,
  current: ShotSetCaptureCurrent,
  occurrenceId: string,
): CapturedShotSetEdit {
  if (!port) throw new Error('shot.set name capture is unavailable.');
  const basis = freezeJson(structuredClone(port.capture({ occurrenceId, current })));
  return Object.freeze({ occurrenceId, basis, port });
}

export function submitShotNameEdit(captured: CapturedShotSetEdit, name: string): void | Promise<void> {
  if (typeof name !== 'string') throw new Error('shot.set name requires a string.');
  const result = captured.port.finish(captured.basis, { values: { name }, clear: [] });
  if (result.command.schema_version !== 1 || result.command.op !== 'shot.set'
    || result.command.version !== '1' || result.command.select !== `occurrence:${captured.occurrenceId}/shot`
    || JSON.stringify(result.command.args) !== JSON.stringify({ values: { name }, clear: [] })) {
    throw new Error('Unsupported shot.set name capture result.');
  }
  return captured.port.submit({ command: freezeJson(structuredClone(result.command)) });
}

export function captureShotPromptEdit(
  port: ShotSetCapturePort | undefined,
  current: ShotSetCaptureCurrent,
  occurrenceId: string,
  prompt: string,
): CapturedShotSetEdit {
  if (!port) throw new Error('shot.set prompt capture is unavailable.');
  if (typeof prompt !== 'string') throw new Error('shot.set prompt capture requires a string.');
  const basis = freezeJson(structuredClone(port.capture({ occurrenceId, current,
    args: { values: { settings: { prompt } }, clear: [] } })));
  return Object.freeze({ occurrenceId, basis, port });
}

export function submitShotPromptEdit(captured: CapturedShotSetEdit, prompt: string): void | Promise<void> {
  if (typeof prompt !== 'string') throw new Error('shot.set prompt requires a string.');
  const args: ExistingShotSetArgs = { values: { settings: { prompt } }, clear: [] };
  const result = captured.port.finish(captured.basis, args);
  if (result.command.schema_version !== 1 || result.command.op !== 'shot.set'
    || result.command.version !== '1' || result.command.select !== `occurrence:${captured.occurrenceId}/shot`
    || JSON.stringify(result.command.args) !== JSON.stringify(args)) {
    throw new Error('Unsupported shot.set prompt capture result.');
  }
  return captured.port.submit({ command: freezeJson(structuredClone(result.command)) });
}

export type { ExistingShotSetArgs, ShotSetBasis };
export { captureShotSet, finishShotSet };
