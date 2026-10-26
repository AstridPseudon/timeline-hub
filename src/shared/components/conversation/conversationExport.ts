import { formatActionGroupEntries } from './actionGroupLogs';
import type { ConversationToolCallPair, ConversationTurn } from './contracts';

export type ConversationExportTurn = {
  turn: ConversationTurn;
  /** Editor requests extracted from assistant text, with any recorded host results. */
  editorActions?: readonly ConversationToolCallPair[];
  inProgress?: boolean;
};

export type ConversationExport = {
  title: string;
  agent: string;
  model?: string | null;
  thinkingLevel?: string | null;
  sessionId: string;
  capturedAt: string;
  inProgress: boolean;
  turns: readonly ConversationExportTurn[];
};

function safeMetadata(value: string | null | undefined): string {
  return value?.replace(/[\r\n]+/g, ' ').trim() || '(not recorded)';
}

function json(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

function attachmentLines(turn: ConversationTurn): string[] {
  if (!turn.attachments?.length) return [];
  return ['', 'Attachments:', ...turn.attachments.flatMap((attachment, index) => [
    `- ${attachment.shotName || attachment.clipId || `Attachment ${index + 1}`} (${attachment.mediaType}): ${attachment.url}`,
    `  Details: ${json(attachment)}`,
  ])];
}

function actionPairsAt(
  turns: readonly ConversationExportTurn[],
  start: number,
  consumedResults: Set<number>,
): { pairs: ConversationToolCallPair[]; nextIndex: number } {
  const pairs: ConversationToolCallPair[] = [];
  let index = start;
  while (index < turns.length && turns[index].turn.role === 'tool_call') {
    const call = turns[index].turn;
    let resultIndex = -1;
    for (let candidate = index + 1; candidate < turns.length; candidate += 1) {
      if (consumedResults.has(candidate) || turns[candidate].turn.role !== 'tool_result') continue;
      const result = turns[candidate].turn;
      if ((call.tool_call_id && result.tool_call_id === call.tool_call_id)
        || (!call.tool_call_id && candidate === index + 1 && !result.tool_call_id)) {
        resultIndex = candidate;
        break;
      }
    }
    if (resultIndex >= 0) consumedResults.add(resultIndex);
    pairs.push({ call, result: resultIndex >= 0 ? turns[resultIndex].turn : null });
    index += 1;
  }
  return { pairs, nextIndex: index };
}

/** Serialize every turn present in the session snapshot, including nested action results. */
export function formatConversationExport(exportData: ConversationExport): string {
  const { title, agent, model, thinkingLevel, sessionId, capturedAt, inProgress, turns } = exportData;
  const lines = [
    `# ${safeMetadata(title)}`,
    '',
    `- Agent: ${safeMetadata(agent)}`,
    `- Model: ${safeMetadata(model)}`,
    `- Thinking level: ${safeMetadata(thinkingLevel)}`,
    `- Session ID: ${safeMetadata(sessionId)}`,
    `- Captured at: ${safeMetadata(capturedAt)}`,
    `- Turn count: ${turns.length}`,
    `- In progress at capture: ${inProgress ? 'Yes' : 'No'}`,
    '',
    '---',
    '',
    'Observation timestamps reflect client receipt or replay, not execution times.',
    '',
  ];
  const consumedResults = new Set<number>();

  for (let index = 0; index < turns.length;) {
    const { turn, editorActions } = turns[index];
    if (turn.role === 'tool_call') {
      const group = actionPairsAt(turns, index, consumedResults);
      lines.push(`## Turn ${index + 1} — Tool/action calls — ${safeMetadata(turn.timestamp)}`, '', ...formatActionGroupEntries(group.pairs));
      index = group.nextIndex;
      continue;
    }

    if (turn.role === 'tool_result' && consumedResults.has(index)) {
      index += 1;
      continue;
    }

    const role = turn.role === 'tool_result' ? 'Tool result' : turn.role === 'user' ? 'User' : `Assistant${turns[index].inProgress ? ' (in progress at capture)' : ''}`;
    lines.push(`## Turn ${index + 1} — ${role} — ${safeMetadata(turn.timestamp)}`, '');
    if (turn.role === 'tool_result') {
      lines.push(`Call ID: ${safeMetadata(turn.tool_call_id)}`, `Status: ${safeMetadata(turn.tool_status)}`, 'Result:', turn.content || '(empty result)');
      if (turn.tool_output_details) lines.push('', 'Structured result details:', json(turn.tool_output_details));
      lines.push('');
      index += 1;
      continue;
    }
    lines.push(turn.content || '(no text)', ...attachmentLines(turn), '');
    if (editorActions?.length) {
      lines.push('Editor requests:', '', ...formatActionGroupEntries(editorActions));
    }
    index += 1;
  }

  return lines.join('\n').trimEnd() + '\n';
}

export function conversationExportFilename(title: string, capturedAt: Date): string {
  const slug = title.normalize('NFKD').toLowerCase()
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'chat';
  const pad = (value: number) => String(value).padStart(2, '0');
  return `${slug}-${capturedAt.getFullYear()}-${pad(capturedAt.getMonth() + 1)}-${pad(capturedAt.getDate())}-${pad(capturedAt.getHours())}${pad(capturedAt.getMinutes())}.md`;
}
