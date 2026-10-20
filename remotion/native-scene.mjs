import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {build} from 'esbuild';
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';

export const loadHostScene = async (project) => {
  const aliases = remotionPrimitiveAliasesFor(project)({}).resolve.alias;
  const result = await build({
    absWorkingDir: project, entryPoints: [path.join(project, 'src/host-scene.ts')],
    bundle: true, write: false, platform: 'node', format: 'esm',
    nodePaths: [path.join(project, 'node_modules')], logLevel: 'silent',
    plugins: [{name: 'renderer-aliases', setup(builder) {
      builder.onResolve({filter: /^[^./]/}, async (args) => {
        if (args.pluginData?.resolvingPackage) return;
        const alias = Object.keys(aliases).find(key => args.path === key || args.path.startsWith(`${key}/`));
        if (!alias) {
          const resolved = await builder.resolve(args.path, {kind: args.kind,
            resolveDir: args.resolveDir, pluginData: {resolvingPackage: true}});
          if (resolved.errors.length) return {errors: resolved.errors};
          return {path: path.isAbsolute(resolved.path) ? pathToFileURL(resolved.path).href : resolved.path,
            external: true};
        }
        const target = path.join(aliases[alias], args.path.slice(alias.length).split('?')[0]);
        return builder.resolve(target, {kind: args.kind, resolveDir: project});
      });
    }}],
  });
  // No executable output is written after launch binding. Sources, aliases,
  // esbuild and installed dependencies are the selected runtime's bound inputs.
  const entry = `data:text/javascript;base64,${Buffer.from(result.outputFiles[0].text).toString('base64')}`;
  return (await import(entry)).prepareHostScene;
};

// Inactive read projection. The caller supplies its already-prepared public
// scene and the same installed querySceneFrame; no component is prepared here.
// Ranges are sorted, disjoint [start, end) pairs; maxFrames is mandatory.
// Each clip/key conserves totalFrames as numeric + unknown + absent-layer counts.
export const foldSceneMotion = (scene, querySceneFrame, request) => {
  const {ranges, clipIds, keys, maxFrames} = request ?? {};
  const uniqueNames = values => Array.isArray(values) && values.length > 0
    && values.every(value => typeof value === 'string' && value.length > 0)
    && new Set(values).size === values.length;
  if (!Number.isSafeInteger(maxFrames) || maxFrames < 1 || maxFrames > 3600
    || !uniqueNames(clipIds) || !uniqueNames(keys) || clipIds.length * keys.length > 64
    || !Array.isArray(ranges) || ranges.length < 1 || ranges.length > 64) {
    throw new Error('scene_motion_request_invalid');
  }
  let totalFrames = 0;
  let previousEnd = 0;
  for (const range of ranges) {
    if (!Array.isArray(range) || range.length !== 2
      || !range.every(frame => Number.isSafeInteger(frame) && frame >= 0)
      || range[0] >= range[1] || range[0] < previousEnd) {
      throw new Error('scene_motion_ranges_invalid');
    }
    totalFrames += range[1] - range[0];
    if (totalFrames > maxFrames) throw new Error('scene_motion_frame_limit');
    previousEnd = range[1];
  }
  // These are exact compiled IDs. Source/occurrence joins remain caller-owned.
  const identities = new Map();
  for (const {clips} of scene.tracks) {
    for (const clip of clips) identities.set(clip.id, (identities.get(clip.id) ?? 0) + 1);
  }
  if (clipIds.some(id => identities.get(id) !== 1)) {
    throw new Error('scene_motion_clip_identity_invalid');
  }
  const counts = clipIds.flatMap(clipId => keys.map(key => ({clipId, key,
    values: new Map(), unknownFrames: 0, absentFrames: 0, totalFrames})));
  for (const [start, end] of ranges) {
    for (let frame = start; frame < end; frame++) {
      const answer = querySceneFrame(scene, frame);
      if (answer?.frame !== frame || !Array.isArray(answer.layers)) {
        throw new Error('scene_motion_frame_invalid');
      }
      const layers = new Map();
      for (const layer of answer.layers) {
        if (!layer || typeof layer.clipId !== 'string' || layers.has(layer.clipId)) {
          throw new Error('scene_motion_layer_identity_invalid');
        }
        layers.set(layer.clipId, layer);
      }
      for (const count of counts) {
        const layer = layers.get(count.clipId);
        if (layer === undefined) {
          count.absentFrames++;
          continue;
        }
        // Intrinsic facts retain their meaning even when visible === false.
        const motion = layer.diagnostics?.motion;
        const value = motion && Object.hasOwn(motion, count.key) ? motion[count.key] : undefined;
        if (typeof value === 'number' && Number.isFinite(value)) {
          count.values.set(value, (count.values.get(value) ?? 0) + 1);
        } else {
          count.unknownFrames++;
        }
      }
    }
  }
  return {totalFrames, counts: counts.map(count => ({...count,
    values: [...count.values].sort(([a], [b]) => a - b).map(([value, n]) => ({value, count: n})),
  }))};
};
