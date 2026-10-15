/** Browser-consumed ACP routes. Both the client and relay policy use this contract. */
export const ACP_ROUTES = {
  projectChat: { method: 'GET', template: '/acp/projects/:projectId/chat' },
  createProjectSession: { method: 'POST', template: '/acp/projects/:projectId/chat/sessions' },
  unassignedProjectSessions: { method: 'GET', template: '/acp/projects/:projectId/chat/unassigned' },
  associateProjectSession: { method: 'POST', template: '/acp/projects/:projectId/chat/associate' },
  saveProjectDraft: { method: 'PATCH', template: '/acp/projects/:projectId/chat/draft' },
  selectProjectSession: { method: 'PATCH', template: '/acp/projects/:projectId/chat' },
  setMainProjectSession: { method: 'PATCH', template: '/acp/projects/:projectId/chat/main' },
  promptProjectSession: { method: 'POST', template: '/acp/projects/:projectId/chat/prompt' },
  connect: { method: 'POST', template: '/acp/connect' },
  reconnect: { method: 'POST', template: '/acp/:connectionId/reconnect' },
  cancelSession: { method: 'POST', template: '/acp/:connectionId/cancel' },
  events: { method: 'GET', template: '/acp/:connectionId/events' },
  disconnect: { method: 'DELETE', template: '/acp/:connectionId' },
  rpc: { method: 'POST', template: '/acp/:connectionId/rpc' },
} as const;

export const ACP_ROUTE_ENTRIES = Object.values(ACP_ROUTES);
export type AcpRouteName = keyof typeof ACP_ROUTES;

export function buildAcpPath(
  name: AcpRouteName,
  params: Readonly<Record<string, string>> = {},
  query: Readonly<Record<string, string>> = {},
): string {
  const path = ACP_ROUTES[name].template.replace(/:([A-Za-z]+)/g, (_match, key: string) => {
    const value = params[key];
    if (!value) throw new Error(`Missing ACP route parameter: ${key}`);
    return encodeURIComponent(value);
  });
  const search = Object.entries(query)
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
    .join('&');
  return search ? `${path}?${search}` : path;
}
