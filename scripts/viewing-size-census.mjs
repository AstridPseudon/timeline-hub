#!/usr/bin/env node

/**
 * Read-only TIMELINE CORE size census for the Viewing-owned slice.
 *
 * The script reads committed blobs through git; it never checks out a ref and
 * never reads the worktree.  With --json it emits the selected manifest as
 * well as byte and nonblank-line counts, so a later run can audit both the
 * boundary and the arithmetic.
 */

import {spawnSync} from 'node:child_process';

const repos = {
  composition: '/home/user/work/composition',
  agent: '/home/user/work/agent',
  app: '/home/user/work/app',
};

const refs = {
  composition: {
    baseline: '67b8aa3d0d6831d3e3504a340ff583c3da253707',
    current: '5e06f40146573a529896cc812229eb890c53c81a',
  },
  agent: {
    baseline: 'a411628f8fd6129f9c58c332019b56769d997384',
    current: 'f7584fad7c7cbd548cf340bb501d09d3520ea9e3',
  },
  app: {
    baseline: '580508eed1bf6ed95caaf476c9d69a4672472a2f',
    current: '1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff',
  },
};

function git(repo, args, encoding = 'utf8') {
  const result = spawnSync('git', ['-C', repo, ...args], {
    encoding,
    maxBuffer: 64 * 1024 * 1024,
  });
  if (result.status !== 0) {
    throw new Error(`git ${args.join(' ')} failed in ${repo}: ${result.stderr}`);
  }
  return result.stdout;
}

function tree(repo, ref, prefix) {
  const output = git(repo, ['ls-tree', '-r', '-z', '--name-only', ref, '--', prefix]);
  return output.split('\0').filter(Boolean);
}

function allTree(repo, ref) {
  const output = git(repo, ['ls-tree', '-r', '-z', '--name-only', ref]);
  return output.split('\0').filter(Boolean);
}

function blob(repo, ref, path) {
  return git(repo, ['show', `${ref}:${path}`], null);
}

function isTextPath(path) {
  return /\.(?:css|js|json|mjs|md|py|ts|tsx|yaml|yml)$/.test(path);
}

function nonblankLines(bytes) {
  return bytes.toString('utf8').split('\n').filter((line) => line.trim()).length;
}

function stats(repo, ref, paths) {
  let bytes = 0;
  let lines = 0;
  for (const path of paths) {
    const content = blob(repo, ref, path);
    bytes += content.length;
    lines += nonblankLines(content);
  }
  return {files: paths.length, bytes, nonblank_lines: lines, paths};
}

function without(paths, predicate) {
  return paths.filter((path) => !predicate(path));
}

function compositionManifest(ref) {
  const paths = tree(repos.composition, ref, 'typescript/src');
  const generated = paths.filter(
    (path) => path.includes('.generated.') || path.endsWith('remotion-timer-compat.d.ts'),
  );
  return {
    authored: without(paths, (path) => generated.includes(path)),
    generated,
  };
}

function agentManifest(ref) {
  const visualize = tree(repos.agent, ref, 'astrid/packs/rendering/actions/timeline_visualize');
  const visualizeGenerated = visualize.filter((path) => path.includes('/schemas/'));
  const visualizeAuthored = without(
    visualize,
    (path) =>
      path.endsWith('/STAGE.md') ||
      path.includes('/fonts/') ||
      path.includes('/inspector_assets/') ||
      visualizeGenerated.includes(path),
  );

  const explicit = [
    'astrid/core/timeline/onscreen.py',
    'astrid/core/timeline/scene_answers.py',
    'astrid/packs/rendering/actions/render/managed_timeline.py',
    'astrid/packs/rendering/actions/render/task_adapter.py',
    'astrid/packs/rendering/rendering/renderers/remotion/run.py',
    'astrid/packs/rendering/rendering/renderers/ffmpeg/run.py',
    'astrid/packs/rendering/elements/catalog.ts',
    'astrid/packs/rendering/shared/element_contracts.ts',
    'astrid/packs/rendering/shared/managed-media-policy.ts',
    'astrid/packs/rendering/shared/managed-media.tsx',
    'astrid/packs/rendering/shared/readiness-image.tsx',
  ];
  const elementPaths = tree(repos.agent, ref, 'astrid/packs/rendering/rendering/elements').filter(
    (path) => isTextPath(path),
  );
  const available = new Set(allTree(repos.agent, ref));
  const adapters = [...new Set([...explicit, ...elementPaths])].filter((path) => available.has(path));
  const scene = adapters.filter(
    (path) => path === 'astrid/core/timeline/onscreen.py' || path === 'astrid/core/timeline/scene_answers.py',
  );

  const remotion = tree(repos.agent, ref, 'remotion/src');
  const remotionGenerated = remotion.filter(
    (path) => path.endsWith('.d.ts') || path.includes('.generated.') || path.endsWith('.test.mjs'),
  );

  const archives = tree(repos.agent, ref, 'remotion/artifacts').filter((path) => !isTextPath(path));
  return {
    visualizeAuthored,
    visualizeGenerated,
    adapters: adapters.filter((path) => !scene.includes(path)),
    scene,
    remotionAuthored: without(remotion, (path) => remotionGenerated.includes(path)),
    remotionGenerated,
    archives,
  };
}

function appManifest(ref) {
  const active = [];
  for (const prefix of [
    'src/tools/video-editor/components/PreviewPanel',
    'src/tools/video-editor/compositions',
    'src/tools/video-editor/render',
  ]) {
    for (const path of tree(repos.app, ref, prefix)) {
      if (!isTextPath(path)) continue;
      if (path.includes('/__tests__/') || path.includes('.test.') || path.includes('.spec.')) continue;
      if (path.includes('/compositions/fallback/')) continue;
      active.push(path);
    }
  }

  const fallback = [
    'src/tools/video-editor/compositions/fallback/registry.generated.tsx',
    'src/tools/video-editor/compositions/fallback/theme-api.tsx',
    'src/tools/video-editor/lib/theme-api.fallback.tsx',
    'src/tools/video-editor/lib/registry.generated.fallback.ts',
  ].filter((path) => allTree(repos.app, ref).includes(path));
  const vendorSource = tree(repos.app, ref, 'vendor/timeline-composition/typescript/src').filter(isTextPath);
  const vendorGenerated = vendorSource.filter(
    (path) => path.includes('.generated.') || path.endsWith('.d.ts'),
  );
  const archives = tree(repos.app, ref, 'vendor/artifacts').filter((path) => !isTextPath(path));
  return {
    active: [...new Set(active)],
    fallback,
    vendorAuthored: without(vendorSource, (path) => vendorGenerated.includes(path)),
    vendorGenerated,
    archives,
  };
}

function measure(label, repoKey, ref, paths) {
  return {label, repo: repoKey, ref, ...stats(repos[repoKey], ref, paths)};
}

function snapshot(refKind) {
  const composition = compositionManifest(refs.composition[refKind]);
  const agent = agentManifest(refs.agent[refKind]);
  const app = appManifest(refs.app[refKind]);
  return {
    canonical: [
      measure('Composition evaluator/default source', 'composition', refs.composition[refKind], composition.authored),
      measure('Agent timeline_visualize adapters', 'agent', refs.agent[refKind], agent.visualizeAuthored),
      measure('Agent scene/render adapters', 'agent', refs.agent[refKind], agent.adapters),
      measure('Agent public/private scene adapters', 'agent', refs.agent[refKind], agent.scene),
      measure('Agent Remotion scene host', 'agent', refs.agent[refKind], agent.remotionAuthored),
      measure('App preview/player/render adapters', 'app', refs.app[refKind], app.active),
    ],
    generated: [
      measure('Composition generated registries/curves/timer declaration', 'composition', refs.composition[refKind], composition.generated),
      measure('Agent visualize schemas', 'agent', refs.agent[refKind], agent.visualizeGenerated),
      measure('Agent Remotion generated/declaration source', 'agent', refs.agent[refKind], agent.remotionGenerated),
      measure('App fallback registries/theme shims', 'app', refs.app[refKind], app.fallback),
    ],
    duplicate: measure('App vendored Composition source', 'app', refs.app[refKind], [
      ...app.vendorAuthored,
      ...app.vendorGenerated,
    ]),
    duplicateGenerated: measure('App vendored generated/declaration source', 'app', refs.app[refKind], app.vendorGenerated),
    archives: [
      measure('Agent built package archive', 'agent', refs.agent[refKind], agent.archives),
      measure('App built package archive', 'app', refs.app[refKind], app.archives),
    ],
  };
}

function main() {
  const baseline = snapshot('baseline');
  const current = snapshot('current');
  if (process.argv.includes('--json')) {
    console.log(JSON.stringify({repos, refs, baseline, current}, null, 2));
    return;
  }
  console.log('viewing-size-census');
  console.log(JSON.stringify({repos, refs, baseline, current}, null, 2));
}

main();
