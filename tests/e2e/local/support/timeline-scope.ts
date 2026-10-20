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

type ProjectCreateResponse = Pick<Response, 'request' | 'status' | 'url'>;

function runtimePath(rawUrl: string): string {
  return new URL(rawUrl).pathname.replace(/^\/api\/runtime(?=\/)/, '');
}

/** Match the App's actual project-create response without accepting another POST or project. */
export function isCreatedProjectResponse(response: ProjectCreateResponse, submittedName: string): boolean {
  if (response.status() !== 201 || runtimePath(response.url()) !== '/v1/projects') return false;
  const request = response.request();
  if (request.method() !== 'POST') return false;
  try {
    const body = JSON.parse(request.postData() ?? '{}') as { name?: unknown };
    return body.name === submittedName;
  } catch {
    return false;
  }
}

/** Observe the normal project-create response at the browser context boundary. */
export async function waitForCreatedProjectResponse(
  context: Pick<BrowserContext, 'waitForEvent'>,
  submittedName: string,
  options: { timeout: number },
): Promise<Response> {
  return context.waitForEvent('response', {
    predicate: (response) => isCreatedProjectResponse(response, submittedName),
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
