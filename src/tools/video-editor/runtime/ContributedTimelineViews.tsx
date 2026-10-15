/** Schema-driven V3 read views. No Python/browser execution fallback. */
import { useEffect, useRef, useState } from 'react';
import Ajv from 'ajv';
import type { VideoEditorPanelDescriptor } from './extensionSurface';

export type ViewSchema = { readonly title?: string; readonly properties?: Readonly<Record<string, ViewSchema>>; readonly items?: ViewSchema; readonly [key: string]: unknown };
export type TimelineView = {
  readonly identity: string;
  readonly implementation_digest: string;
  readonly descriptor: {
    readonly point: 'timeline.view'; readonly id: string;
    readonly label: string; readonly description: string;
    readonly read_model: string; readonly reads: readonly string[];
    readonly schema: ViewSchema;
  };
};
export type ViewBinding = { project: string; timeline: string; revision_id: string };
export type ViewRequest = ViewBinding & { identity: string; implementation_digest: string };
export type ViewResult = { view: TimelineView; data: Record<string, unknown> };
export type ViewHost = (request: ViewRequest) => Promise<ViewResult>;
export class TimelineViewError extends Error {
  constructor(public readonly code: 'unsupported' | 'identity_mismatch' | 'invalid_result', message: string) {
    super(message); this.name = 'TimelineViewError';
  }
}

/** Accept only the declaration projection from the selected admitted build. */
export function timelineViewsFromCatalog(catalog: unknown): readonly TimelineView[] {
  if (!Array.isArray(catalog)) throw new TimelineViewError('unsupported', 'View catalog unavailable');
  const ids = new Set<string>();
  for (const row of catalog) {
    const d = row?.descriptor;
    if (!d || d.point !== 'timeline.view' || row.identity !== `timeline.view/${d.id}`
      || !/^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$/.test(d.id)
      || !/^[a-f0-9]{64}$/.test(row.implementation_digest)
      || typeof d.label !== 'string' || !d.label || typeof d.description !== 'string' || !d.description
      || !/^[a-z][a-z0-9_]*$/.test(d.read_model)
      || JSON.stringify(d.reads) !== JSON.stringify(['project', 'timeline', 'revision_id'])
      || !d.schema || typeof d.schema !== 'object' || Array.isArray(d.schema)
      || ids.has(row.identity)) {
      throw new TimelineViewError('unsupported', 'Invalid or duplicate view declaration');
    }
    ids.add(row.identity);
  }
  // Detach the inspection values; catalog discovery never loads code or a host.
  return JSON.parse(JSON.stringify(catalog)) as TimelineView[];
}

function stableJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(stableJson).join(',')}]`;
  if (value && typeof value === 'object') return `{${Object.entries(value).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => `${JSON.stringify(k)}:${stableJson(v)}`).join(',')}}`;
  return JSON.stringify(value) ?? 'null';
}

function validateSchema(schema: ViewSchema, value: unknown) {
  // The installed AJV host supports Draft 7. Refuse newer/unknown keywords
  // explicitly rather than silently weaken the admitted Draft 2020 schema.
  const keywords = new Set(['$ref', '$id', '$schema', '$comment', 'title', 'description', 'default', 'examples',
    'type', 'enum', 'const', 'properties', 'patternProperties', 'additionalProperties', 'required', 'propertyNames',
    'definitions', 'dependencies', 'items', 'additionalItems', 'contains', 'minItems', 'maxItems', 'uniqueItems',
    'minProperties', 'maxProperties', 'minLength', 'maxLength', 'pattern', 'format', 'minimum', 'maximum',
    'exclusiveMinimum', 'exclusiveMaximum', 'multipleOf', 'allOf', 'anyOf', 'oneOf', 'not', 'if', 'then', 'else',
    'readOnly', 'writeOnly']);
  const local = (node: unknown) => {
    if (typeof node === 'boolean') return;
    if (!node || typeof node !== 'object' || Array.isArray(node)) throw new TimelineViewError('unsupported', 'Invalid view schema');
    for (const [key, child] of Object.entries(node)) {
      if (!keywords.has(key) || (key === '$schema' && child !== 'http://json-schema.org/draft-07/schema#')) {
        throw new TimelineViewError('unsupported', `Unsupported view schema keyword: ${key}`);
      }
      if (key === '$ref' && (typeof child !== 'string' || !child.startsWith('#'))) {
        throw new TimelineViewError('unsupported', 'External view schema references are unsupported');
      }
      if (['properties', 'patternProperties', 'definitions'].includes(key)) Object.values(child as object).forEach(local);
      if (['allOf', 'anyOf', 'oneOf'].includes(key)) (child as unknown[]).forEach(local);
      if (['items', 'additionalItems', 'additionalProperties', 'propertyNames', 'contains', 'not', 'if', 'then', 'else'].includes(key)) {
        if (Array.isArray(child)) child.forEach(local); else local(child);
      }
      if (key === 'dependencies') Object.values(child as object).filter(v => !Array.isArray(v)).forEach(local);
    }
  };
  local(schema);
  const ajv = new Ajv({ allErrors: true });
  let valid;
  try { valid = ajv.compile(schema); }
  catch { throw new TimelineViewError('unsupported', 'View schema is unsupported by this host'); }
  if (!valid(value)) throw new TimelineViewError('invalid_result', ajv.errorsText(valid.errors));
}

export async function readTimelineView(view: TimelineView, binding?: ViewBinding, host?: ViewHost): Promise<ViewResult> {
  if (!host || !binding || !binding.project || !binding.timeline || !binding.revision_id) {
    throw new TimelineViewError('unsupported', 'Exact-revision view read transport is unavailable');
  }
  view = JSON.parse(JSON.stringify(view)) as TimelineView;
  binding = { ...binding };
  const result = await host({ ...binding, identity: view.identity, implementation_digest: view.implementation_digest });
  const data = result?.data;
  if (result?.view?.identity !== view.identity || result?.view?.implementation_digest !== view.implementation_digest
    || stableJson(result.view.descriptor) !== stableJson(view.descriptor)
    || !data || data.project_id !== binding.project || data.timeline_id !== binding.timeline
    || data.revision_id !== binding.revision_id || typeof data.content_digest !== 'string'
    || !/^[a-f0-9]{64}$/.test(data.content_digest)) {
    throw new TimelineViewError('identity_mismatch', 'View response does not match declaration and exact revision');
  }
  validateSchema(view.descriptor.schema, data);
  return JSON.parse(JSON.stringify(result)) as ViewResult;
}

function SchemaValue({ value, schema }: { value: unknown; schema: ViewSchema }) {
  if (Array.isArray(value)) return <ol>{value.map((child, index) => <li key={index}><SchemaValue value={child} schema={schema.items ?? {}} /></li>)}</ol>;
  if (value && typeof value === 'object') return <dl>{Object.entries(value).map(([key, child]) => {
    const sub = schema.properties?.[key] ?? {};
    return <div key={key}><dt>{sub.title ?? key}</dt><dd><SchemaValue value={child} schema={sub} /></dd></div>;
  })}</dl>;
  return <span>{JSON.stringify(value)}</span>;
}

export function ContributedTimelineViews({ views, binding, host }: { views: readonly TimelineView[]; binding?: ViewBinding; host?: ViewHost }) {
  const [selected, setSelected] = useState(views[0]?.identity ?? '');
  const view = views.find(v => v.identity === selected) ?? views[0];
  const [result, setResult] = useState<ViewResult>();
  const [error, setError] = useState<TimelineViewError>();
  const [pending, setPending] = useState(false);
  const generation = useRef(0);
  useEffect(() => { generation.current++; setResult(undefined); setError(undefined); setPending(false); return () => { generation.current++; }; }, [view, binding, host]);
  if (!view) return null;
  const read = async () => {
    const requestGeneration = ++generation.current;
    setPending(true); setResult(undefined); setError(undefined);
    try {
      const next = await readTimelineView(view, binding, host);
      if (requestGeneration === generation.current) setResult(next);
    } catch (e) {
      if (requestGeneration === generation.current) setError(e instanceof TimelineViewError ? e : new TimelineViewError('invalid_result', String(e)));
    } finally { if (requestGeneration === generation.current) setPending(false); }
  };
  return <section aria-label="Timeline views">
    <label>View <select value={view.identity} onChange={e => setSelected(e.target.value)}>{views.map(v => <option key={v.identity} value={v.identity}>{v.descriptor.label}</option>)}</select></label>
    <p>{view.descriptor.description}</p>
    <details><summary>View declaration</summary><dl><dt>Identity</dt><dd>{view.identity}</dd><dt>Declaration digest</dt><dd>{view.implementation_digest}</dd><dt>Read model</dt><dd>{view.descriptor.read_model}</dd><dt>Read inputs</dt><dd>{view.descriptor.reads.join(', ')}</dd></dl><pre>{JSON.stringify(view.descriptor.schema, null, 2)}</pre></details>
    <button type="button" disabled={pending} onClick={() => void read()}>Read view</button>
    {error && <p role="alert" data-code={error.code}>{error.code}: {error.message}</p>}
    {result && result.view.identity === view.identity && result.data.revision_id === binding?.revision_id && result.data.project_id === binding?.project && result.data.timeline_id === binding?.timeline && <SchemaValue value={result.data} schema={view.descriptor.schema} />}
  </section>;
}

/** Bind the admitted metadata to the existing generic asset-panel surface. */
export function contributedTimelineViewPanels(catalog: { readonly ASTRID_TIMELINE_VIEW_CATALOG?: unknown }): readonly VideoEditorPanelDescriptor[] {
  if (catalog.ASTRID_TIMELINE_VIEW_CATALOG === undefined) return [];
  const views = timelineViewsFromCatalog(catalog.ASTRID_TIMELINE_VIEW_CATALOG);
  if (views.length === 0) return [];
  return [{ id: 'astrid.timeline.views', placement: 'asset-panel', render: () => <ContributedTimelineViews views={views} /> }];
}
