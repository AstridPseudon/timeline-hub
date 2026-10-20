// @vitest-environment node
import { spawnSync } from 'node:child_process';
import { resolve } from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import fixture from './shotComposition.fixture.json';
import viewing from './shotCompositionAudio.fixture.json';
import agent from './shotCompositionAudio.agent.fixture.json';
import agentGraph from './shotCompositionAudio.agentGraph.fixture.json';
import reference from './shotCompositionAudio.reference.json';
import { createShotCompositionAdapter } from './shotCompositionAdapter.ts';
import { projectCanonicalComposition } from './shotCompositionProjection.ts';
import type { ResolvedTimelineClip } from '../types/index.ts';

type Graph = typeof fixture;
type Json = Record<string, unknown>;
function child(graph: Graph): Json {
  return graph.shot_revisions.find(row => row.shot_id === 'shot-alpha' && row.revision_id === 'rev-a')!
    .internal_timeline_revision.timeline.clips[1] as Json;
}

const cases = reference.results.map(row => {
  const graph = structuredClone(row.corpus === 'viewing' ? fixture : agentGraph) as Graph;
  if (row.corpus === 'viewing') {
    const vector = viewing.find(vector => vector.name === row.id)!;
    Object.assign(graph.occurrences[0], { duration_ms: 4000 }, vector.occurrence);
    const clips = graph.shot_revisions.find(row => row.shot_id === 'shot-alpha' && row.revision_id === 'rev-a')!
      .internal_timeline_revision.timeline.clips as Json[];
    clips[1] = { id: 'alpha-audio', clip_type: 'media', track: 'audio', at: 0.25, ...vector.clip };
  } else {
    const vector = agent.vectors.find(vector => vector.id === row.id)!;
    Object.assign(graph.occurrences[0], vector.occurrence);
    delete child(graph).duration_ms;
    Object.assign(child(graph), agent.base.child_default, vector.child);
  }
  return { ...row, graph };
});

// Transport reshaping only: keep the exact authored occurrence values and pins.
function closure(graph: Graph) {
  return {
    parent_revision: {
      project_id: graph.project.project_id,
      timeline_id: graph.primary_timeline.document_id,
      revision_id: graph.primary_timeline.head.revision_id,
      payload: { ...graph.parent_composition, config: graph.parent_composition?.config ?? {}, occurrences: graph.occurrences, registry: { assets: {} } },
    },
    shot_revisions: graph.shot_revisions.map(row => ({
      ...row, internal_timeline_revision_id: row.internal_timeline_revision.revision_id,
    })),
    internal_timeline_revisions: graph.shot_revisions.map(row => ({
      revision_id: row.internal_timeline_revision.revision_id, payload: row.internal_timeline_revision.timeline,
    })),
  };
}

function projectApp(graph: Graph) {
  const before = structuredClone(graph);
  const prepared = createShotCompositionAdapter({ load: async () => graph }).prepare(graph);
  const clip = projectCanonicalComposition(prepared).config.clips.find(clip => clip.id === 'occ-1:alpha-audio')!;
  expect(graph).toStrictEqual(before);
  return clip;
}

// Both real existing Agent entrypoints, with complete output clips compared below.
// No timing, gain, envelope or DSP implementation lives in this test bridge.
type Projection = { clip: ResolvedTimelineClip; graphClip: Json; config: { clips: Json[] }; registry: Json };
function projectAgent(inputs: { graph: Graph; closure: ReturnType<typeof closure> }[]): Projection[] {
  if (inputs.length > 1) return inputs.flatMap(input => projectAgent([input]));
  const checkout = process.env.ASTRID_CHECKOUT ?? resolve(process.cwd(), '../agent');
  const result = spawnSync(process.env.AUDIO_CONTRACT_PYTHON ?? 'python3', ['-c', `
import copy,json,sys
from astrid.core.timeline.shot_composition_projection import project_runtime_parent_composition,project_shot_composition
out=[]
for row in json.loads(sys.argv[1]):
    before=copy.deepcopy(row)
    runtime=project_runtime_parent_composition(**row['closure'])
    graph=project_shot_composition(row['graph'])
    assert row==before and runtime.graph==row['closure']
    pick=lambda p: next(c for c in p.config['clips'] if c['id']=='occ-1:alpha-audio')
    out.append({'clip':pick(runtime),'graphClip':pick(graph),'config':runtime.config,'registry':runtime.registry})
print(json.dumps(out))
`, JSON.stringify(inputs)], {
    timeout: 10000, encoding: 'utf8',
    env: { ...process.env, PYTHONPATH: checkout, PYTHONDONTWRITEBYTECODE: '1' },
  });
  expect(result.status, result.stderr).toBe(0);
  return JSON.parse(result.stdout) as Projection[];
}
let compiled: ReturnType<typeof projectAgent>;
beforeAll(() => { compiled = projectAgent(cases.map(row => ({ graph: row.graph, closure: closure(row.graph) }))); });

const soundKeys = ['at', 'from', 'to', 'hold', 'speed', 'volume', 'params', 'effects'] as const;
function sound(clip: ResolvedTimelineClip) {
  return Object.fromEntries(soundKeys.filter(key => Object.prototype.hasOwnProperty.call(clip, key)).map(key => [key, clip[key]]));
}

const knownDifferences = [
  { id: 'child times occurrence gain', wrong: { volume: 0.8 } },
  { id: 'boost times occurrence gain', wrong: { volume: 1.5 } },
  { id: 'occurrence source offset', wrong: { from: 0.475, to: 1.475 } },
  { id: 'occurrence speed without child speed', wrong: { speed: 1.5 } },
];

describe('two unchanged audio corpora through the ONE Agent projector', () => {
  it('retains 11 original Viewing vectors and 11 different Agent draft vectors', () => {
    expect(viewing).toHaveLength(11);
    expect(agent.vectors).toHaveLength(11);
    expect(cases).toHaveLength(22);
    expect(viewing.find(row => row.name === 'occurrence source offset')!.occurrence.source_offset).toBe(350);
    expect(agent.vectors.find(row => row.id === 'source-offset-is-metadata-only')!.occurrence.source_offset).toBe(0.35);
  });

  it.each(cases.map((row, index) => ({ ...row, index })))('$corpus: $id (complete fields)', row => {
    expect(compiled[row.index].clip).toStrictEqual(row.clip);
    expect(compiled[row.index].graphClip).toStrictEqual(row.graphClip);
    // The literal snapshots include every field, including opaque app provenance.
    const wrong = { ...compiled[row.index].clip, unexpected: true };
    expect(wrong).not.toStrictEqual(row.clip);
  });

  it('preserves opaque child data, parent native audio and source registries without authoring mutation', () => {
    const graph = structuredClone(cases[0].graph);
    const opaque = { vendor: { revision: 'native-1', data: [null, false, { future: 'keep' }] } };
    Object.assign(child(graph), { app: opaque, audio: { native: opaque }, unknown_audio: opaque });
    const pinned = closure(graph);
    const native = { id: 'native-parent', track: 'audio', at: 20, from: 0.125, to: 1.125,
      speed: 2, volume: 3, asset: 'native', audio: { native: opaque }, app: opaque };
    Object.assign(pinned.parent_revision.payload, { clips: [native], registry: { assets: { native: { file: 'native.aac', ...opaque } } } });
    const before = structuredClone({ graph, closure: pinned });
    const result = projectAgent([before])[0];
    expect(result.clip).toStrictEqual({
      ...compiled[0].clip, unknown_audio: opaque, audio: { native: opaque },
      app: { ...opaque, ...compiled[0].clip.app },
    });
    expect(result.config.clips[0]).toStrictEqual(native);
    expect(result.registry).toStrictEqual(pinned.parent_revision.payload.registry);
    expect({ graph, closure: pinned }).toStrictEqual(before);
  });
});

describe('current App requirements, with four known differences still RED', () => {
  it.each(cases.filter(row => row.corpus === 'viewing'))('$id', row => {
    expect(sound(projectApp(row.graph))).toStrictEqual(sound(row.clip as ResolvedTimelineClip));
  });

  it.each(knownDifferences)('negative control catches recorded wrong App output: $id', ({ id, wrong }) => {
    const row = cases.find(row => row.corpus === 'viewing' && row.id === id)!;
    const expected = sound(row.clip as ResolvedTimelineClip);
    expect({ ...expected, ...wrong }).not.toStrictEqual(expected);
  });
});

