import { describe, expect, it } from 'vitest';
import { classifyPairedRoute, type PairedService } from '../../../config/vite/pairedRoutePolicy';

const P = 'proj-1';
const T = 'tl-1';
const R = 'rev-1';

// Every call the App's product code sends through the relay, as
// [method, path under /api/<prefix>, expected service].
const runtime = (path: string) => `/api/runtime${path}`;
const astrid = (path: string) => `/api/astrid${path}`;
const productCalls: ReadonlyArray<readonly [string, string, PairedService]> = [
  // RuntimeClient (src/integrations/runtime/client.ts, dataProvider.ts)
  ['GET', runtime('/v1/health'), 'runtime'],
  ['POST', runtime('/v1/handshake'), 'runtime'],
  ['GET', runtime('/v1/realm'), 'runtime'],
  ['GET', runtime('/v1/projects?limit=50&cursor=c1'), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}`), 'runtime'],
  ['PATCH', runtime(`/v1/projects/${P}`), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}/timelines?limit=50`), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}/timelines/${T}`), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}/timelines/${T}/revisions/${R}`), 'runtime'],
  ['POST', runtime(`/v1/projects/${P}/timelines/${T}/composition-revisions`), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}/timelines/${T}/composition-revisions?limit=50`), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}/timelines/${T}/composition-revisions/${R}`), 'runtime'],
  ['POST', runtime(`/v1/projects/${P}/timelines/${T}/composition-revisions/${R}/restore`), 'runtime'],
  ['POST', runtime(`/v1/projects/${P}/timelines/${T}/inspect`), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}/shots/shot-1/revisions/${R}`), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}/thumbnails/source-frame?media_id=m1&time=1`), 'runtime'],
  ['POST', runtime(`/v1/projects/${P}/thumbnails/source-frame`), 'runtime'],
  ['POST', runtime(`/v1/projects/${P}/objects`), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}/objects/obj-1/location`), 'runtime'],
  ['POST', runtime(`/v1/projects/${P}/media-imports`), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}/media-imports/op-1`), 'runtime'],
  ['GET', runtime('/v1/objects/obj-1'), 'runtime'],
  ['HEAD', runtime('/v1/objects/obj-1'), 'runtime'],
  ['POST', runtime('/v1/tasks'), 'runtime'],
  ['GET', runtime('/v1/tasks/task-1'), 'runtime'],
  ['POST', runtime('/v1/tasks/task-1/cancel'), 'runtime'],
  ['POST', runtime('/v1/tasks/task-1/retry'), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}/tasks?limit=50`), 'runtime'],
  ['GET', runtime('/v1/tasks/task-1/managed-outputs?limit=50'), 'runtime'],
  ['GET', runtime('/v1/managed-outputs/assoc-1'), 'runtime'],
  ['POST', runtime('/v1/managed-outputs/assoc-1/export'), 'runtime'],
  ['GET', runtime('/v1/events?limit=50&aggregate_id=a1'), 'runtime'],
  ['GET', runtime(`/v1/projects/${P}/generations?limit=50`), 'runtime'],
  ['GET', runtime('/v1/generations/gen-1'), 'runtime'],
  ['GET', runtime('/v1/generations/gen-1/variants?limit=50'), 'runtime'],
  ['POST', runtime('/v1/variants/var-1/viewed'), 'runtime'],
  ['POST', runtime('/v1/generations/gen-1/variants/viewed'), 'runtime'],
  // AstridLocalClient (src/integrations/astrid/*Routes.ts, renderRouter.ts)
  ['GET', astrid('/v1/capabilities?limit=50'), 'astrid'],
  ['POST', astrid('/v1/tasks'), 'astrid'],
  ['GET', astrid('/v1/tasks/task-1'), 'astrid'],
  ['POST', astrid('/v1/tasks/task-1/cancel'), 'astrid'],
  ['GET', astrid('/v1/events?limit=50'), 'astrid'],
  ['GET', astrid(`/v1/projects/${P}/tasks?limit=1`), 'astrid'],
  ['GET', astrid(`/v1/projects/${P}/generations?limit=1`), 'astrid'],
  ['GET', astrid('/v1/generations/gen-1/variants?limit=50'), 'astrid'],
  ['POST', astrid(`/v1/projects/${P}/objects`), 'astrid'],
  ['GET', astrid('/v1/projects'), 'astrid'],
  ['PATCH', astrid(`/v1/projects/${P}`), 'astrid'],
  // ACP agent chat (acpRoutes.ts)
  ['POST', astrid('/acp/connect'), 'acp'],
  ['POST', astrid('/acp/conn-1/rpc'), 'acp'],
  ['GET', astrid('/acp/conn-1/events'), 'acp'],
  ['POST', astrid('/acp/conn-1/cancel'), 'acp'],
  ['POST', astrid('/acp/conn-1/reconnect'), 'acp'],
  ['GET', astrid(`/acp/projects/${P}/chat`), 'acp'],
  ['POST', astrid(`/acp/projects/${P}/chat`), 'acp'],
  ['POST', astrid(`/acp/projects/${P}/chat/sessions`), 'acp'],
  ['GET', astrid(`/acp/projects/${P}/chat/unassigned?connection_id=conn-1`), 'acp'],
  ['POST', astrid(`/acp/projects/${P}/chat/associate`), 'acp'],
  ['PATCH', astrid(`/acp/projects/${P}/chat/draft`), 'acp'],
  ['PATCH', astrid(`/acp/projects/${P}/chat/main`), 'acp'],
  ['POST', astrid(`/acp/projects/${P}/chat/prompt`), 'acp'],
];

const forbidden: ReadonlyArray<readonly [string, string]> = [
  ['GET', runtime('/v1/doctor')],
  ['POST', runtime('/v1/backup')],
  ['POST', runtime('/v1/restore')],
  ['GET', runtime('/v1/export')],
  ['POST', runtime('/v1/realm/tombstone')],
  ['POST', runtime('/v1/realm/recover')],
  ['POST', runtime('/v1/realm/purge')],
  ['POST', runtime('/v1/realm/replace')],
  ['POST', runtime('/v1/tasks/claim')],
  ['POST', runtime('/v1/attempts/att-1/settle')],
  ['POST', runtime('/v1/recovery/checkpoint')],
  ['POST', runtime('/v1/executors')],
  ['GET', runtime('/v1/executors/ex-1')],
  ['POST', runtime('/v1/capabilities')],
  ['GET', runtime('/v1/capabilities')],
  ['POST', astrid('/v1/capabilities')],
  ['PUT', astrid('/v1/capabilities/cap-1')],
  ['POST', astrid('/v1/tasks/claim')],
  ['GET', astrid('/v1/doctor')],
  ['POST', astrid('/v1/realm/purge')],
  ['POST', astrid('/v1/attempts/att-1/settle')],
  ['POST', astrid('/v1/executors')],
  ['POST', runtime('/v1/tasks/task-1/remote-credential')],
  ['POST', runtime('/v1/tasks/task-1/placement-recovery')],
  ['POST', runtime(`/v1/projects/${P}/timelines/${T}/replace-parent-media`)],
  ['POST', runtime(`/v1/projects/${P}/timelines/${T}/composition-revisions/${R}/restore/extra`)],
  ['POST', runtime(`/v1/projects/${P}/timelines/${T}/composition-revisions/${R}/purge`)],
  ['POST', runtime(`/v1/projects/${P}/timelines/${T}/doctor`)],
  ['POST', runtime(`/v1/projects/${P}/timelines/${T}/composition-revisions/`)],
  ['GET', runtime(`/v1/projects/${P}/timelines/${T}/composition-revisions/${R}/../../../doctor`)],
  ['GET', runtime(`/v1/projects/${P}/timelines/${T}/composition-revisions/%2e%2e/doctor`)],
  ['GET', runtime(`/v1/projects/${P}/timelines/${T}/composition-revisions//x`)],
  ['GET', runtime(`/v1/projects/${P}/timelines/${T}/inspect/../../../../doctor`)],
  ['GET', runtime(`/v1/projects/${P}/thumbnails/other`)],
  ['GET', runtime(`/v1/projects/${P}/objects/obj-1/location/extra`)],
  ['GET', runtime('/v1/unknown')],
  ['GET', astrid(`/acp/projects/${P}/chat/unknown`)],
  ['GET', astrid(`/acp/projects/${P}/chat/../../x`)],
  ['TRACE', runtime('/v1/health')],
];

describe('paired route policy', () => {
  it.each(productCalls)('allows product call %s %s', (method, path, service) => {
    const route = classifyPairedRoute(path, method);
    expect(route?.service).toBe(service);
    expect(route?.upstreamPath).toBe(path.replace(/^\/api\/(?:runtime|astrid)/, ''));
  });

  it.each(forbidden)('rejects %s %s', (method, path) => {
    expect(classifyPairedRoute(path, method)).toBeNull();
  });
});
