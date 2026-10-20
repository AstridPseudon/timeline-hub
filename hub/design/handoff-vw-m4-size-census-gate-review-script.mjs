#!/usr/bin/env node

// Flat, read-only census for the 08:00 Timeline Core review.
// It reads committed Git blobs only; it never checks out, installs, builds,
// follows worktree files, or writes into any repository.

import {spawnSync} from 'node:child_process';

const repos = {
  composition: '/home/user/work/composition',
  agent: '/home/user/work/agent',
  app: '/home/user/work/app',
};

// These are the source snapshots used by tl/vw-m4-core-size-census.  The
// Agent and App values are historical candidate snapshots, not current
// tl/integration heads; keeping them pinned makes this audit reproducible.
const refs = {
  composition: {baseline: '67b8aa3d0d6831d3e3504a340ff583c3da253707', current: '5e06f40146573a529896cc812229eb890c53c81a'},
  agent: {baseline: 'a411628f8fd6129f9c58c332019b56769d997384', current: 'f7584fad7c7cbd548cf340bb501d09d3520ea9e3'},
  app: {baseline: '580508eed1bf6ed95caaf476c9d69a4672472a2f', current: '1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff'},
};

const adjacentRemotion = new Set([
  'remotion/src/LiveSceneClip.tsx',
  'remotion/src/ThreeTimelineComposition.tsx',
  'remotion/src/astrid-frame-worker.mjs',
]);

function git(repo, args, encoding = 'utf8') {
  const result = spawnSync('git', ['-C', repo, ...args], {encoding, maxBuffer: 64 * 1024 * 1024});
  if (result.status !== 0) throw new Error(`git ${args.join(' ')} failed in ${repo}: ${result.stderr}`);
  return result.stdout;
}

function tree(repo, ref, prefix) {
  return git(repo, ['ls-tree', '-r', '-z', '--name-only', ref, '--', prefix])
    .split('\0').filter(Boolean);
}

function allTree(repo, ref) {
  return git(repo, ['ls-tree', '-r', '-z', '--name-only', ref]).split('\0').filter(Boolean);
}

function blob(repo, ref, path) {
  return git(repo, ['show', `${ref}:${path}`], null);
}

function blobId(repo, ref, path) {
  return git(repos[repo], ['rev-parse', `${ref}:${path}`]).trim();
}

function isText(path) {
  return /\.(?:css|js|json|mjs|md|py|ts|tsx|yaml|yml)$/.test(path);
}

function nonblankLines(bytes) {
  return bytes.toString('utf8').split('\n').filter((line) => line.trim()).length;
}

function stats(repo, ref, paths) {
  let bytes = 0;
  let lines = 0;
  for (const path of paths) {
    const content = blob(repos[repo], ref, path);
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
  const generated = paths.filter((path) => path.includes('.generated.') || path.endsWith('remotion-timer-compat.d.ts'));
  return {authored: without(paths, (path) => generated.includes(path)), generated};
}

function agentManifest(ref) {
  const visualize = tree(repos.agent, ref, 'astrid/packs/rendering/actions/timeline_visualize');
  const visualizeGenerated = visualize.filter((path) => path.includes('/schemas/'));
  const visualizeAuthored = without(visualize, (path) =>
    path.endsWith('/STAGE.md') || path.includes('/fonts/') || path.includes('/inspector_assets/') || visualizeGenerated.includes(path));

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
  const elementPaths = tree(repos.agent, ref, 'astrid/packs/rendering/rendering/elements').filter(isText);
  const available = new Set(allTree(repos.agent, ref));
  const selectedAdapters = [...new Set([...explicit, ...elementPaths])].filter((path) => available.has(path));
  const scene = selectedAdapters.filter((path) => path === 'astrid/core/timeline/onscreen.py' || path === 'astrid/core/timeline/scene_answers.py');
  const adapters = selectedAdapters.filter((path) => !scene.includes(path));

  const remotion = tree(repos.agent, ref, 'remotion/src');
  const remotionGenerated = remotion.filter((path) => path.endsWith('.d.ts') || path.includes('.generated.') || path.endsWith('.test.mjs'));
  const remotionAuthored = without(remotion, (path) => remotionGenerated.includes(path));
  const remotionCore = without(remotionAuthored, (path) => adjacentRemotion.has(path));
  const adjacent = remotionAuthored.filter((path) => adjacentRemotion.has(path));
  const archives = tree(repos.agent, ref, 'remotion/artifacts').filter((path) => !isText(path));
  const oldReference = tree(repos.agent, ref, 'docs/reference/timeline-composition-v0.0.6').filter(isText);
  return {visualizeAuthored, visualizeGenerated, adapters, scene, remotionCore, remotionAuthored, remotionGenerated, adjacent, archives, oldReference};
}

function appManifest(ref) {
  const active = [];
  for (const prefix of ['src/tools/video-editor/components/PreviewPanel', 'src/tools/video-editor/compositions', 'src/tools/video-editor/render']) {
    for (const path of tree(repos.app, ref, prefix)) {
      if (isText(path) && !path.includes('/__tests__/') && !path.includes('.test.') && !path.includes('.spec.') && !path.includes('/compositions/fallback/')) active.push(path);
    }
  }
  const all = new Set(allTree(repos.app, ref));
  const fallback = [
    'src/tools/video-editor/compositions/fallback/registry.generated.tsx',
    'src/tools/video-editor/compositions/fallback/theme-api.tsx',
    'src/tools/video-editor/lib/theme-api.fallback.tsx',
    'src/tools/video-editor/lib/registry.generated.fallback.ts',
  ].filter((path) => all.has(path));
  const vendorComposition = tree(repos.app, ref, 'vendor/timeline-composition/typescript/src').filter(isText);
  const vendorCompositionGenerated = vendorComposition.filter((path) => path.includes('.generated.') || path.endsWith('.d.ts'));
  const vendorAgent = [...new Set([
    ...tree(repos.app, ref, 'vendor/astrid-browser').filter((path) => isText(path) && (path.startsWith('vendor/astrid-browser/astrid/') || path.startsWith('vendor/astrid-browser/remotion/src/'))),
    ...tree(repos.app, ref, 'vendor/astrid-build-inputs/primary').filter((path) => isText(path) && path.startsWith('vendor/astrid-build-inputs/primary/astrid/')),
  ])];
  const archives = tree(repos.app, ref, 'vendor/artifacts').filter((path) => !isText(path));
  return {active: [...new Set(active)], fallback, vendorComposition, vendorCompositionGenerated, vendorAgent, archives};
}

function measure(label, repo, ref, paths) {
  return {label, repo, ref, ...stats(repo, ref, paths)};
}

function exactMappedStats(repo, ref, paths, targetRepo, targetRef, mapPath, targetFilter = () => true) {
  const exact = [];
  const targets = [];
  for (const path of paths) {
    const target = mapPath(path);
    if (!targetFilter(target)) continue;
    try {
      if (blobId(repo, ref, path) === blobId(targetRepo, targetRef, target)) {
        exact.push(path);
        targets.push(target);
      }
    } catch {
      // A vendor path without a corresponding target path is not a duplicate.
    }
  }
  return {...stats(repo, ref, exact), target_paths: targets};
}

function snapshot(kind) {
  const c = compositionManifest(refs.composition[kind]);
  const a = agentManifest(refs.agent[kind]);
  const p = appManifest(refs.app[kind]);
  const canonicalAgentPaths = new Set([...a.visualizeAuthored, ...a.adapters, ...a.scene, ...a.remotionCore]);
  const mapVendorAgentPath = (path) =>
    path.startsWith('vendor/astrid-browser/')
      ? path.slice('vendor/astrid-browser/'.length)
      : path.slice('vendor/astrid-build-inputs/primary/'.length);
  return {
    canonical: [
      measure('Composition evaluator/default source', 'composition', refs.composition[kind], c.authored),
      measure('Agent timeline_visualize adapters', 'agent', refs.agent[kind], a.visualizeAuthored),
      measure('Agent scene/render adapters', 'agent', refs.agent[kind], a.adapters),
      measure('Agent public/private scene adapters', 'agent', refs.agent[kind], a.scene),
      measure('Agent Remotion core host (adjacent files removed)', 'agent', refs.agent[kind], a.remotionCore),
      measure('App preview/player/render adapters', 'app', refs.app[kind], p.active),
    ],
    adjacent: measure('Agent Remotion adjacent/live-scene/execution files', 'agent', refs.agent[kind], a.adjacent),
    generated: [
      measure('Composition generated registries/curves/timer declaration', 'composition', refs.composition[kind], c.generated),
      measure('Agent visualize schemas', 'agent', refs.agent[kind], a.visualizeGenerated),
      measure('Agent Remotion generated/declaration source', 'agent', refs.agent[kind], a.remotionGenerated),
      measure('App fallback registries/theme shims', 'app', refs.app[kind], p.fallback),
    ],
    duplicates: {
      appComposition: measure('App vendored Composition source', 'app', refs.app[kind], p.vendorComposition),
      appCompositionGenerated: measure('App vendored Composition generated/declaration source', 'app', refs.app[kind], p.vendorCompositionGenerated),
      appAgentVendor: measure('App vendored Agent/browser source (all text)', 'app', refs.app[kind], p.vendorAgent),
      appAgentExact: exactMappedStats('app', refs.app[kind], p.vendorAgent, 'agent', refs.agent[kind], mapVendorAgentPath),
      appAgentCanonicalExact: exactMappedStats('app', refs.app[kind], p.vendorAgent, 'agent', refs.agent[kind], mapVendorAgentPath, (path) => canonicalAgentPaths.has(path)),
      agentOldCompositionReference: measure('Agent old Composition reference source', 'agent', refs.agent[kind], a.oldReference),
    },
    archives: [
      measure('Agent built package archive', 'agent', refs.agent[kind], a.archives),
      measure('App built package archive', 'app', refs.app[kind], p.archives),
    ],
  };
}

const baseline = snapshot('baseline');
const current = snapshot('current');
console.log(JSON.stringify({repos, refs, adjacentRemotion: [...adjacentRemotion], baseline, current}, null, 2));
