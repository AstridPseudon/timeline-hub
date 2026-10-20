import type { LocalAgentId } from './localAgents.ts';

export function acpClientCapabilities(agent: LocalAgentId, platform: NodeJS.Platform = process.platform): { terminal?: true } {
  // OMP's terminal backend can choose the unusable Windows WSL bash stub.
  // Omitting this capability lets OMP use its embedded shell backend.
  return platform === 'win32' && agent === 'astrid' ? {} : { terminal: true };
}
