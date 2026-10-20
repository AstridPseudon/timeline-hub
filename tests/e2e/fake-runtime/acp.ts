/**
 * The canned ACP replies the stub gave the editor's chat pane, and nothing more. These are not Runtime
 * routes and no existing fake serves them: with `VITE_ASTRID_ACP_BRIDGE_PORT` pointing at the fake, the
 * editor's cold reads (`AgentChat` -> `useProjectChat`, `acpRoutes.ts`) land here. Every other ACP path
 * answers 404, so a prompt, a session creation or any other RPC can never be sent to the fake.
 *
 * `AgentChat` passes the Runtime's canonical project id (`runtime.project.projectId`), the old stub path
 * used the slug; both are accepted and the caller's own selector is echoed back.
 */
export type AcpReply = { status: number; body: unknown };

type Draft = { text: string; revision: number; queued_messages: unknown[] };

export type FakeAcp = {
  /** `null` when the request is not an ACP path at all (the caller falls through to the other fakes). */
  handle(method: string, pathname: string, body: unknown): AcpReply | null;
  reset(): void;
};

const CONNECTION_ID = 'local-test-connection';
const emptyDraft = (): Draft => ({ text: '', revision: 0, queued_messages: [] });

export function createFakeAcp(projectSelectors: readonly string[]): FakeAcp {
  let draft = emptyDraft();

  function chatState(selector: string) {
    return {
      project_id: selector,
      scope_key: `project:${selector}`,
      revision: 0,
      selected_session_id: null,
      sessions: [],
      draft,
    };
  }

  return {
    reset() {
      draft = emptyDraft();
    },
    handle(method, pathname, body) {
      const record = (body !== null && typeof body === 'object' ? body : {}) as Record<string, unknown>;
      const chat = /^\/projects\/([^/]+)\/chat(\/draft)?$/.exec(pathname);
      if (chat) {
        const selector = decodeURIComponent(chat[1]!);
        if (!projectSelectors.includes(selector)) {
          return { status: 404, body: { error: 'not_found', detail: `Unknown project ${selector}` } };
        }
        if (!chat[2] && method === 'GET') return { status: 200, body: chatState(selector) };
        if (chat[2] && method === 'PATCH') {
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
        return { status: 404, body: { error: 'not_found', detail: 'Only the local session/list probe is stubbed.' } };
      }
      if (pathname === `/${CONNECTION_ID}/events` && method === 'GET') {
        return { status: 200, body: { notifications: [], disconnected: false } };
      }
      return null;
    },
  };
}
