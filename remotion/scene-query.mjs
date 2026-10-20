import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

try {
  // Resolve the public export from the validated host install, never this checkout.
  const require = createRequire(path.join(process.argv[2], 'package.json'));
  const {prepareScene, querySceneFrame, querySceneOcclusion} = await import(pathToFileURL(
    require.resolve('@banodoco/timeline-composition/evaluation')));
  const input = JSON.parse(readFileSync(0, 'utf8'));
  const {scene, props, basis, roles: hostRoles, frames} = input;
  if (input.query === 'occlusion') {
    if (typeof querySceneOcclusion !== 'function') throw new Error('scene_occlusion_export_missing');
    if (!Array.isArray(input.answers) || !Array.isArray(input.targets)) {
      throw new Error('scene_occlusion_inputs_invalid');
    }
    const answers = new Map(input.answers.map(answer => [answer.frame, answer]));
    const results = input.targets.map(target => {
      const answer = answers.get(target.frame);
      if (answer === undefined) {
        return {status: 'unavailable', reason: `SceneFrame for frame ${target.frame} is unavailable`};
      }
      return querySceneOcclusion(answer, target.clip_id, target.min_fraction);
    });
    process.stdout.write(JSON.stringify(results));
  } else if (input.query === 'motion') {
    if (typeof querySceneFrame !== 'function') throw new Error('scene_motion_export_missing');
    if (!props) throw new Error('scene_motion_requires_root_props');
    const {loadHostScene, foldSceneMotion} = await import('./native-scene.mjs');
    const prepare = await loadHostScene(process.argv[2]);
    const prepared = prepare(props, basis, hostRoles ?? {});
    const folded = foldSceneMotion(prepared, querySceneFrame, input.motion);
    process.stdout.write(JSON.stringify([{...folded, ranges: input.motion.ranges}]));
  } else {
  if (!Array.isArray(frames)) throw new Error('scene_frames_invalid');
  let prepared;
  if (props) {
    const {loadHostScene} = await import('./native-scene.mjs');
    const prepare = await loadHostScene(process.argv[2]);
    prepared = prepare(props, basis, hostRoles ?? {});
  } else {
    const {tracks, assets, fps, width, height, roles, elements} = scene;
    if (!Array.isArray(tracks) || !Array.isArray(frames) || !assets?.assets) {
      throw new Error('scene_inputs_invalid');
    }
    for (const {track, clips, transitions} of tracks) {
      if (track?.kind !== 'visual' || !Array.isArray(clips) || !Array.isArray(transitions)
        || transitions.length !== Math.max(0, clips.length - 1)
        || clips.some((clip, i) => i > 0 && clip.at < clips[i - 1].at)
        || transitions.some(t => t !== null && (!Number.isFinite(t.T) || t.T <= 0
          || !['dip', 'dissolve'].includes(t.kind) || !['start', 'center', 'end'].includes(t.align)))) {
        throw new Error('scene_requires_renderer_order_and_resolved_transitions');
      }
    }
    prepared = prepareScene(tracks, assets, fps, width, height,
      {roles, elements: new Set(elements ?? [])});
  }
  process.stdout.write(JSON.stringify(frames.map(frame => querySceneFrame(prepared, frame))));
  }
} catch (error) {
  process.stderr.write(`scene evaluation unavailable: ${error.message}\n`);
  process.exitCode = 1;
}
