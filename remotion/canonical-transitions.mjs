import {readFileSync} from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
import {build} from 'esbuild';
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';

try {
  const project = process.argv[2];
  const require = createRequire(path.join(project, 'package.json'));
  const composition = await import(pathToFileURL(require.resolve('@banodoco/timeline-composition')));
  if (typeof composition.compileCanonicalTransitions !== 'function') {
    throw new Error('installed Composition has no canonical transition compiler (requires 0.0.9)');
  }
  const props = JSON.parse(readFileSync(0, 'utf8'));
  if (Object.hasOwn(props, 'compiledTransitions')) throw new Error('Root props already compiled');
  if (!props.theme?.visual?.canvas || !props.assets?.assets
    || !Array.isArray(props.timeline?.tracks) || !Array.isArray(props.timeline.clips)) {
    throw new Error('canonical compilation requires exact Root props and resolved runtime theme');
  }
  const canvas = props.timeline.theme_overrides?.visual?.canvas ?? props.theme.visual.canvas;
  if (![canvas.fps, canvas.width, canvas.height].every(n => Number.isFinite(n) && n > 0)) {
    throw new Error('canonical compilation requires the explicit Root frame basis');
  }
  // Load the same generated maps and pack aliases as Root and the scene host.
  // Like native-scene.mjs, leave package peers external and write no executable.
  const aliases = remotionPrimitiveAliasesFor(project)({}).resolve.alias;
  const result = await build({
    absWorkingDir: project, entryPoints: [path.join(project, 'src/host-registries.ts')],
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
  const entry = `data:text/javascript;base64,${Buffer.from(result.outputFiles[0].text).toString('base64')}`;
  const {resolveHostRegistries} = await import(entry);
  const theme = composition.toRuntimeTheme(props.theme);
  const tracks = [...props.timeline.tracks].reverse().filter(track => track.kind === 'visual')
    .map(track => ({track, clips: props.timeline.clips.filter(clip => clip.track === track.id)}));
  const compiled = composition.compileCanonicalTransitions(tracks, canvas.fps, theme, resolveHostRegistries(theme));
  process.stdout.write(JSON.stringify(compiled));
} catch (error) {
  process.stderr.write(`canonical transition compilation unavailable: ${error.message}\n`);
  process.exitCode = 1;
}
