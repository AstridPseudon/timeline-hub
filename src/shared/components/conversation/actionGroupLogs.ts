import type { ConversationToolCallPair } from './contracts';

/** OMP TaskToolDetails, received as ACP rawOutput.details, never parsed from prose. */
function nativeTaskResults(details: Record<string, unknown> | undefined): Array<Record<string, unknown> & { id: string; agent: string; exitCode: number }> | null {
  if (!details || !(details.projectAgentsDir === null || typeof details.projectAgentsDir === 'string')
    || typeof details.totalDurationMs !== 'number' || !Number.isFinite(details.totalDurationMs) || details.totalDurationMs < 0
    || !Array.isArray(details.results)) return null;
  const results = details.results;
  if (!results.every(result => result && typeof result === 'object' && !Array.isArray(result)
    && typeof result.id === 'string' && result.id.length > 0 && typeof result.agent === 'string' && result.agent.length > 0
    && Number.isSafeInteger(result.exitCode)
    && (result.aborted === undefined || typeof result.aborted === 'boolean')
    && (result.error === undefined || typeof result.error === 'string'))) return null;
  return results;
}

export function actionStatus(pair: ConversationToolCallPair): string {
  const transport = pair.result?.tool_status ?? pair.call.tool_status ?? (pair.result ? 'completed' : 'in_progress');
  if (transport !== 'completed') return transport;
  const results = nativeTaskResults(pair.result?.tool_output_details);
  return results?.some(result => result.exitCode !== 0 || result.aborted || result.error) ? 'failed' : transport;
}

/** Only the supplied action group; never the surrounding conversation/context. */
export function formatActionGroupLogs(pairs: readonly ConversationToolCallPair[], capturedAt: string): string {
  return ['Action logs', `Captured at: ${capturedAt}`, `Actions: ${pairs.length}`,
    'Observation timestamps reflect client receipt/replay, not execution times.', '', ...pairs.flatMap((pair, index) => [
      `Action ${index + 1}: ${pair.call.tool_name || 'Action'}`,
      `Call ID: ${pair.call.tool_call_id || '(not recorded)'}`,
      `Call observed at: ${pair.call.timestamp || '(not recorded)'}`,
      `Status: ${actionStatus(pair)}`,
      `Transport status: ${pair.result?.tool_status ?? pair.call.tool_status ?? '(not recorded)'}`,
      'Arguments:', pair.call.tool_args ? JSON.stringify(pair.call.tool_args, null, 2) : '(not recorded)',
      'Call:', pair.call.content || '(not recorded)',
      `Result observed at: ${pair.result?.timestamp || '(not recorded)'}`,
      'Result:', pair.result ? pair.result.content || '(empty result)' : '(pending at capture)',
      ...(pair.result?.tool_output_details ? ['Structured result details:', JSON.stringify(pair.result.tool_output_details, null, 2)] : []),
      '',
    ])].join('\n');
}

export function downloadActionGroupLogs(pairs: readonly ConversationToolCallPair[]): void {
  const capturedAt = new Date().toISOString();
  const blob = new Blob([formatActionGroupLogs(pairs, capturedAt)], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = `action-logs-${capturedAt.replace(/[:.]/g, '-')}.txt`;
  document.body.appendChild(anchor);
  try { anchor.click(); } finally { anchor.remove(); URL.revokeObjectURL(url); }
}
