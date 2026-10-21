import type { BrowserContext, Page, Response } from '@playwright/test';

/** A test-only Runtime timeline scope. */
export type TimelineScope = Readonly<{
  projectId: string;
  timelineId: string;
}>;

export type TimelineListItem = Readonly<{
  timeline_id: string;
  is_shot?: boolean;
}>;

export type TimelineListPage = Readonly<{
  items: readonly TimelineListItem[];
}>;

/** Build a Runtime timeline path from the scope chosen by the test. */
export function timelineBase(scope: TimelineScope): string {
  return `/v1/projects/${scope.projectId}/timelines/${scope.timelineId}`;
}

/** Select the exact canonical resource already chosen by the UI. */
export function timelineFromList(page: TimelineListPage, timelineId: string): TimelineListItem | undefined {
  return page.items.find((timeline) => timeline.timeline_id === timelineId);
}

type ProjectCreateResponse = Pick<Response, 'json' | 'request' | 'status' | 'url'>;

function bridgeProjectPath(bridgeBase: string): { origin: string; path: string } | undefined {
  try {
    const base = new URL(bridgeBase);
    const basePath = base.pathname.replace(/\/+$/, '');
    if ((base.protocol !== 'http:' && base.protocol !== 'https:')
      || basePath !== '/api/astrid' || base.search || base.hash || base.username || base.password) return undefined;
    return { origin: base.origin, path: `${basePath}/v1/projects` };
  } catch {
    return undefined;
  }
}

/** Match the App's actual project-create response without accepting another POST or project. */
export function isCreatedProjectResponse(
  response: ProjectCreateResponse,
  submittedName: string,
  bridgeBase: string,
): boolean {
  const projectPath = bridgeProjectPath(bridgeBase);
  if (!projectPath) return false;
  let url: URL;
  try {
    url = new URL(response.url());
  } catch {
    return false;
  }
  if (response.status() !== 201 || url.origin !== projectPath.origin || url.pathname !== projectPath.path
    || url.search || url.hash) return false;
  const request = response.request();
  if (request.method() !== 'POST') return false;
  try {
    const body = JSON.parse(request.postData() ?? '{}') as { name?: unknown };
    return body.name === submittedName.trim();
  } catch {
    return false;
  }
}

/** Read the strict project-create envelope after the synchronous event predicate matches. */
export async function readCreatedProjectResponse(
  response: ProjectCreateResponse,
  submittedName: string,
  bridgeBase: string,
): Promise<{ data: { project_id: string; name: string }; receipt: Record<string, unknown> }> {
  if (!isCreatedProjectResponse(response, submittedName, bridgeBase)) {
    throw new Error('response is not the configured bridge project-create response');
  }
  const payload = await response.json() as unknown;
  if (!payload || typeof payload !== 'object') throw new Error('project-create response is not an object');
  const data = (payload as Record<string, unknown>).data;
  const receipt = (payload as Record<string, unknown>).receipt;
  if (!data || typeof data !== 'object' || !receipt || typeof receipt !== 'object') {
    throw new Error('project-create response must contain data and receipt');
  }
  const project = data as Record<string, unknown>;
  const receiptRecord = receipt as Record<string, unknown>;
  if (typeof project.project_id !== 'string' || project.name !== submittedName.trim()
    || typeof receiptRecord.receipt_id !== 'string') {
    throw new Error('project-create response has the wrong project or receipt identity');
  }
  return { data: { project_id: project.project_id, name: project.name }, receipt: receiptRecord };
}

/** Observe the normal project-create response at the browser context boundary. */
export async function waitForCreatedProjectResponse(
  context: Pick<BrowserContext, 'waitForEvent'>,
  submittedName: string,
  bridgeBase: string,
  options: { timeout: number },
): Promise<Response> {
  return context.waitForEvent('response', {
    predicate: (response) => isCreatedProjectResponse(response, submittedName, bridgeBase),
    ...options,
  });
}

/** A click finishes before its async creator navigates away from the previous project. */
export async function waitForCreatedProjectUrl(
  page: Pick<Page, 'waitForURL' | 'url'>,
  projectId: string,
  options: { timeout: number },
): Promise<URL> {
  await page.waitForURL((url) => url.pathname === '/tools/video-editor'
    && url.searchParams.get('project') === projectId, options);
  return new URL(page.url());
}
