/**
 * The canned ACP replies the stub gave the editor's chat pane, and nothing more. These are not Runtime
 * routes and no existing fake serves them: with `VITE_ASTRID_ACP_BRIDGE_PORT` pointing at the fake, the
 * editor's cold reads (`AgentChat` -> `useProjectChat`, `acpRoutes.ts`) land here. Every other ACP path
 * answers 404, so a prompt or any other RPC can never be sent to the fake. The one write beyond the draft is the
 * chat's own session bookkeeping (create, select): the editor's chat creates a session when it opens on an empty
 * project, and a failed create showed as a red banner above the composer.
 *
 * `AgentChat` passes the Runtime's canonical project id (`runtime.project.projectId`), the old stub path
 * used the slug; both are accepted and the caller's own selector is echoed back.
 */
export type AcpReply = { status: number; body: unknown };

type Draft = { text: string; revision: number; queued_messages: unknown[] };
type ChatSession = { id: string; title: string };
type Chat = { revision: number; sessions: ChatSession[]; selected: string | null; operations: Map<string, string> };

export type FakeAcp = {
  /** `null` when the request is not an ACP path at all (the caller falls through to the other fakes). */
  handle(method: string, pathname: string, body: unknown): AcpReply | null;
  reset(): void;
};

const CONNECTION_ID = 'local-test-connection';
const emptyDraft = (): Draft => ({ text: '', revision: 0, queued_messages: [] });

const emptyChat = (): Chat => ({ revision: 0, sessions: [], selected: null, operations: new Map() });

export function createFakeAcp(projectSelectors: readonly string[]): FakeAcp {
  let draft = emptyDraft();
  // One chat for the one fake project (its id and slug name the same thing). Sessions exist only because the
  // editor's chat asked for one: nothing is ever prompted, so a session is just an id the chat can hold.
  let chat = emptyChat();

  function chatState(selector: string, operationSessionId?: string) {
    return {
      project_id: selector,
      scope_key: `project:${selector}`,
      revision: chat.revision,
      selected_session_id: chat.selected,
      ...(operationSessionId ? { operation_session_id: operationSessionId } : {}),
      sessions: chat.sessions,
      draft,
    };
  }

  /**
   * `ensure` and `ensure_main` keep the selected session, `new` always adds one; a repeated operation id replays.
   * There is no Main: the state omits `main_session_id`, as the fake always has.
   */
  function createSession(mode: unknown, operationId: unknown): string {
    const replay = typeof operationId === 'string' ? chat.operations.get(operationId) : undefined;
    if (replay) return replay;
    const existing = mode === 'new' ? null : chat.selected;
    let id = existing;
    if (!id) {
      id = `fake-session-${chat.sessions.length + 1}`;
      chat.sessions = [...chat.sessions, { id, title: chat.sessions.length === 0 ? 'Main' : `Chat ${chat.sessions.length + 1}` }];
      chat.selected = id;
      chat.revision += 1;
    }
    if (typeof operationId === 'string') chat.operations.set(operationId, id);
    return id;
  }

  return {
    reset() {
      draft = emptyDraft();
      chat = emptyChat();
    },
    handle(method, pathname, body) {
      const record = (body !== null && typeof body === 'object' ? body : {}) as Record<string, unknown>;
      const sessionCreate = /^\/projects\/([^/]+)\/chat\/sessions$/.exec(pathname);
      if (sessionCreate && method === 'POST') {
        const selector = decodeURIComponent(sessionCreate[1]!);
        if (!projectSelectors.includes(selector)) {
          return { status: 404, body: { error: 'not_found', detail: `Unknown project ${selector}` } };
        }
        if (typeof record.connection_id !== 'string' || record.connection_id !== CONNECTION_ID) {
          return { status: 404, body: { error: 'not_found', detail: 'Unknown ACP connection.' } };
        }
        const id = createSession(record.mode, record.operation_id);
        return { status: 200, body: chatState(selector, id) };
      }
      const chatRoute = /^\/projects\/([^/]+)\/chat(\/draft)?$/.exec(pathname);
      if (chatRoute) {
        const selector = decodeURIComponent(chatRoute[1]!);
        if (!projectSelectors.includes(selector)) {
          return { status: 404, body: { error: 'not_found', detail: `Unknown project ${selector}` } };
        }
        if (!chatRoute[2] && method === 'GET') return { status: 200, body: chatState(selector) };
        // Selecting one of the chat's own sessions (or none).
        if (!chatRoute[2] && method === 'PATCH' && 'selected_session_id' in record) {
          const target = record.selected_session_id;
          if (record.expected_revision !== chat.revision || !(target === null || chat.sessions.some((session) => session.id === target))) {
            return { status: 409, body: { error: 'chat_conflict', detail: 'The deterministic chat changed; reload before selecting.' } };
          }
          chat.selected = target as string | null;
          chat.revision += 1;
          return { status: 200, body: chatState(selector) };
        }
        if (chatRoute[2] && method === 'PATCH') {
          if (
            !Number.isInteger(record.expected_revision)
            || record.expected_revision !== draft.revision
            || typeof record.text !== 'string'
            || !Array.isArray(record.queued_messages)
          ) {
            return { status: 409, body: { error: 'draft_conflict', detail: 'The deterministic chat draft changed; reload before saving.' } };
          }
          draft = { text: record.text, revision: draft.revision + 1, queued_messages: record.queued_messages };
          return { status: 200, body: chatState(selector) };
        }
        return null;
      }
      // A cold editor can query the unscoped session list before project context settles. Give that exact
      // read a deterministic empty connection; no prompt, session creation or arbitrary RPC is served.
      // The chat pane's agent picker and model menu read these catalogs on mount (`acpRoutes.ts` agents(),
      // models()). One ready Astrid and no providers: enough for the pane to settle, nothing to pick.
      if (pathname === '/agents' && method === 'GET') {
        return { status: 200, body: { agents: [{ id: 'astrid', name: 'Astrid', state: 'ready', line: null }] } };
      }
      if (pathname === '/models' && method === 'GET') {
        return { status: 200, body: { providers: [], currentModel: null } };
      }
      if (pathname === '/connect' && method === 'POST') {
        return { status: 200, body: { connection_id: CONNECTION_ID, initialize: {} } };
      }
      if (pathname === `/${CONNECTION_ID}/rpc` && method === 'POST') {
        if (record.method === 'session/list') return { status: 200, body: { result: { sessions: [] } } };
        // Attaching a session the chat just created: it holds no history and no control claim.
        if (record.method === 'session/load') return { status: 200, body: { result: {} } };
        return { status: 404, body: { error: 'not_found', detail: 'Only the local session/list and session/load are stubbed.' } };
      }
      if (pathname === `/${CONNECTION_ID}/models` && method === 'GET') {
        return { status: 200, body: { models: null } };
      }
      if (pathname === `/${CONNECTION_ID}` && method === 'DELETE') {
        return { status: 200, body: { connection_id: CONNECTION_ID, closed: true } };
      }
      if (pathname === `/${CONNECTION_ID}/events` && method === 'GET') {
        return { status: 200, body: { notifications: [], disconnected: false } };
      }
      return null;
    },
  };
}
