import React from 'react';
import { readFileSync } from 'node:fs';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import * as catalog from '@astrid/packs/rendering/editor/catalog';
import {
  contributedTimelineViewPanels, ContributedTimelineViews, readTimelineView,
  timelineViewsFromCatalog, type ViewBinding, type ViewResult,
} from './ContributedTimelineViews';

afterEach(cleanup);
const views = timelineViewsFromCatalog(catalog.ASTRID_TIMELINE_VIEW_CATALOG);
const view = views[0];
const binding: ViewBinding = { project: 'p', timeline: 't', revision_id: 'rev-0' };
const result = (): ViewResult => ({ view, data: {
  project_id: 'p', timeline_id: 't', revision_id: 'rev-0', content_digest: 'a'.repeat(64), fps: 30,
  ranges: [{ range: {name:'OPEN',kind:'chapter',from:'c1',to:'c2'},start_frame:0,end_frame:120 },
    {range:{name:'viral',kind:'beat',from:'"viral"',to:'after "viral"'},start_frame:39,end_frame:57}],
  legacy_chapters: [], findings: [{code:'unresolved-anchor',path:'ranges[2].from',message:'unknown word'}],
} });

describe('V3 contributed view panel on the existing extension surface', () => {
  it('lists the actual generated declaration without host/code execution', async () => {
    const host = vi.fn();
    const before = JSON.stringify(catalog.ASTRID_TIMELINE_VIEW_CATALOG);
    render(<ContributedTimelineViews views={views} binding={binding} host={host} />);
    expect(screen.getByRole('option', {name:view.descriptor.label})).toBeDefined();
    expect(screen.getByText(view.descriptor.description)).toBeDefined();
    expect(screen.getByText(view.descriptor.read_model)).toBeDefined();
    expect(screen.getByText('project, timeline, revision_id')).toBeDefined();
    expect(host).not.toHaveBeenCalled();
    expect(JSON.stringify(catalog.ASTRID_TIMELINE_VIEW_CATALOG)).toBe(before);
  });

  it('mounts via the generic panel contract and reports typed unsupported execution', async () => {
    const panels = contributedTimelineViewPanels(catalog);
    expect(panels).toHaveLength(1);
    expect(panels[0].placement).toBe('asset-panel');
    render(<>{panels[0].render({} as never)}</>);
    fireEvent.click(screen.getByRole('button', {name:'Read view'}));
    await waitFor(() => expect(screen.getByRole('alert').getAttribute('data-code')).toBe('unsupported'));
    expect(contributedTimelineViewPanels({})).toEqual([]);
  });

  it('passes exact binding/digest and renders schema fields, ranges and findings without writes', async () => {
    const value = result(); const original=JSON.stringify(value);
    const host = vi.fn(async () => value);
    const write = vi.spyOn(Storage.prototype, 'setItem');
    render(<ContributedTimelineViews views={views} binding={binding} host={host} />);
    fireEvent.click(screen.getByRole('button', {name:'Read view'}));
    await waitFor(() => expect(screen.getByText('"OPEN"')).toBeDefined());
    expect(screen.getByText('"beat"')).toBeDefined();
    expect(screen.getByText('"unknown word"')).toBeDefined();
    expect(screen.getByText('120')).toBeDefined();
    expect(screen.getByText('"rev-0"')).toBeDefined();
    expect(host).toHaveBeenCalledWith({...binding,identity:view.identity,implementation_digest:view.implementation_digest});
    expect(JSON.stringify(value)).toBe(original);
    expect(write).not.toHaveBeenCalled(); write.mockRestore();
  });

  it.each(['project_id','timeline_id','revision_id','content_digest'])('refuses mismatched %s', async field => {
    const value = result(); value.data[field]='wrong';
    await expect(readTimelineView(view,binding,async()=>value)).rejects.toMatchObject({code:'identity_mismatch'});
  });

  it('refuses changed declaration, malformed payload, missing host and duplicate catalog identities', async () => {
    const value=result();
    await expect(readTimelineView(view,binding,async()=>({...value,view:{...view,implementation_digest:'b'.repeat(64)}}))).rejects.toMatchObject({code:'identity_mismatch'});
    await expect(readTimelineView(view,binding,async()=>({...value,data:{...value.data,fps:'bad'}}))).rejects.toMatchObject({code:'invalid_result'});
    await expect(readTimelineView(view,binding)).rejects.toMatchObject({code:'unsupported'});
    expect(()=>timelineViewsFromCatalog([view,view])).toThrow();
    expect(()=>timelineViewsFromCatalog([{...view,descriptor:{...view.descriptor,reads:['file']}}])).toThrow();
  });

  it('refuses unsupported schema semantics and external references explicitly', async () => {
    for (const schema of [{...view.descriptor.schema,unevaluatedProperties:false}, {...view.descriptor.schema,$ref:'https://example.invalid/schema'}]) {
      const unsupported={...view,descriptor:{...view.descriptor,schema}};
      await expect(readTimelineView(unsupported,binding,async()=>({...result(),view:unsupported}))).rejects.toMatchObject({code:'unsupported'});
    }
  });

  it('discards pending results when the selected exact revision changes', async () => {
    let resolve!: (value:ViewResult)=>void;
    const host=vi.fn(()=>new Promise<ViewResult>(done=>{resolve=done;}));
    const ui=render(<ContributedTimelineViews views={views} binding={binding} host={host} />);
    fireEvent.click(screen.getByRole('button',{name:'Read view'}));
    ui.rerender(<ContributedTimelineViews views={views} binding={{...binding,revision_id:'rev-1'}} host={host} />);
    resolve(result());
    await waitFor(()=>expect(screen.queryByText('"OPEN"')).toBeNull());
  });
});

// Optional source-joined fixture from the actual I producer/J host test. This
// validates data consumption only and makes no Runtime transport claim.
it.skipIf(!process.env.ASTRID_EXT_VIEW_WITNESS)('consumes actual producer fixture through the generic schema panel', async () => {
  const witnessed = JSON.parse(readFileSync(process.env.ASTRID_EXT_VIEW_WITNESS!, 'utf8')) as ViewResult;
  expect(witnessed.view.identity).toBe(view.identity);
  expect(witnessed.view.implementation_digest).toBe(view.implementation_digest);
  render(<ContributedTimelineViews views={views} binding={binding} host={async()=>witnessed} />);
  fireEvent.click(screen.getByRole('button',{name:'Read view'}));
  await waitFor(()=>expect(screen.getByText('270')).toBeDefined());
  expect(screen.getByText('"LIVE"')).toBeDefined();
  expect(screen.getByText('57')).toBeDefined();
});
