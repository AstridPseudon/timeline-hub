# Shared graph drift audit — root-controller environment-fix follow-up

## Verdict

The affected object is the borrowed Remotion graph at:

`/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules`

It has topology drift, not package-byte corruption. The retained READY graph
manifest is still the last-good source of truth. The live graph contains all
of its prior entries unchanged, plus 106 package-directory symlinks that point
back to their containing package directory. Those links make recursive graph
inventory cycle and invalidate the root-smoke preparation. Do not use this
graph for a centrally qualified run until an owner restores the exact approved
topology or produces a newly reviewed equivalent manifest.

This is not evidence that the six Remotion/Player files or the 77-member
Composition archive changed. All six historical hashes and the 77-member
archive pin still match.

## Exact lease and last-good source

The missing source lease is the Agent root-smoke lease:

- lease/worktree: `/home/user/work/wt/vw-m3-root-smoke-central-ready`
- path status: absent
- retained branch ref: `tl/vw-m3-root-smoke-central-ready`
- last-good source commit: `5acd7233df676bf42b2086d86cb0a6358398bf5f`
- last-good source tree: `66898dd11df74e205af95903651782a29e9886b4`
- source file count: 2,900
- commit parent: `384918908aa8c75229c2b6ccdd8fda03b7ce24a1`

The commit and tree remain readable from the Agent object store, but the
recorded worktree was removed. The old READY document is therefore not a
replacement source lease. It is additionally stale because it records the
pre-environment-fix controller hash
`5728411e9254119723ca5af2736f0671b8c9e97b3ffeaf0679195c0eaf947acf`; the
fixed controller currently hashes to
`46e7c0dd5c5ccaf3e210556941f76f1c8adfa67190f33f1f434105294fe421a4`.

Do not confuse this with the separate Runtime lease, which is present and
clean at `/home/user/work/wt/vw-m3-runtime-source-lease2`:

- Runtime revision: `9f9b25c000485e919f30f1411831fe2d5a3c1316`
- Runtime tree: `5c3a7e7141047d7295ab130a8f05359f4fcb34bc`

That Runtime lease is not the missing source path and was not implicated by
this graph audit.

## Actual graph paths and minimal reproduction

The live graph has, without following symlinks:

- 21,429 regular files;
- 139 symlinks: 33 `.bin` links and 106 package-directory links.

The last-good controller-equivalent inventory had 21,495 entries: 21,462
file entries and 33 `.bin` link records. The controller records both a hash
for a symlink-to-file and its `@link` target, which is why the raw regular-file
count is lower than its file-entry count.

Comparing the retained
`handoff-vw-m3-root-smoke-central-ready-prepare-pre.json` manifest against a
cycle-safe current inventory gives:

| comparison | result |
| --- | ---: |
| prior entries missing | 0 |
| prior entries changed | 0 |
| added entries | 106 |
| added entries that are package-directory symlinks | 106 |
| added entries outside the graph | 0 |

Representative links are:

```text
@babel/code-frame/code-frame -> .../node_modules/@babel/code-frame
@babel/parser/parser         -> .../node_modules/@babel/parser
@remotion/player/player      -> .../node_modules/@remotion/player
```

All 106 targets are internal package roots. The 33 `.bin` links are the
expected pre-existing package-manager links recorded by the READY manifest;
they are not the new drift. The new package links were created as a batch at
2026-10-20 06:59:42Z (first through last observed link), after the retained
READY preparation. Their target topology is not represented by the retained
approved manifest. No causal install command was inferred or run.

The bounded controller reproduction was:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python - <<'PY'
import importlib.util
from pathlib import Path
p = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-controller.py')
s = importlib.util.spec_from_file_location('root_smoke_controller', p)
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
try:
    m.inventory(Path('/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules'))
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))
PY
```

Result:

```text
RuntimeError: symlink cycle: /home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules/@babel/code-frame/code-frame
```

The first link resolves to its parent package directory, so recursive
descent returns to an already visited directory. This is a bounded cycle
diagnostic; no unbounded traversal was attempted.

## Prior 77/six-peer comparison

The root READY record retains the 77-member public10 Composition archive with
SHA-256
`cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`.
The current graph still matches all six historical target hashes:

| path | SHA-256 |
| --- | --- |
| `@remotion/player/dist/cjs/PlayerUI.js` | `5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb` |
| `@remotion/player/dist/cjs/use-player-methods.js` | `ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46` |
| `@remotion/player/dist/cjs/use-playback.js` | `6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0` |
| `@remotion/player/dist/esm/index.mjs` | `d3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12` |
| `remotion/dist/esm/index.mjs` | `9fdfe58f3f34e6a72564a811ac5d374d1c97a0f535e2a0e3aac198670d9b7ff8` |
| `remotion/dist/cjs/audio/shared-audio-tags.js` | `471b33916a91f5b9529c477bdf0ec586cb700d5a7179ab910a82dd932e172f6c` |

Therefore the correct classification is: approved `.bin` links and package
bytes are pre-existing/preserved; the 106 package-root links are real
filesystem drift because they were absent from the approved graph and make
the graph non-inventoryable. This is a topology failure, not evidence to
relabel the six-peer or 77-member content facts.

## Impact by graph

- **Root smoke / shared Composition consumers:** blocked before any browser
  or renderer work. The root controller’s `inventory(GRAPH)` fails at the
  first package self-link; reprepare cannot truthfully create a new READY
  document from this graph. The same shared path is named by the presenter and
  mouth qualification handoffs, so their graph-inventory/preflight paths must
  be treated as unqualified until the topology is restored. Direct Node
  package resolution is not proven broken by this audit; recursive inventory
  is definitively broken.

- **PCM:** the current inactive PCM evidence uses its own ORCH-local graph at
  `workers/vw-m3-normal-pcm-producer-current/checks/remotion/node_modules`.
  That graph has six deliberate peer symlinks (Composition package, React,
  Remotion media/layout peers) and no package self-links. The current shared
  graph’s 106-link drift therefore has no demonstrated impact on that
  inactive PCM test graph. PCM activation/HTTP/server lifetime remains
  unqualified as its handoff already states.

- **Frame:** the retained frame-candidate preflight names separate App and
  Agent graph roots, not the current `scene-host-plumbing` graph; those
  candidate worktree paths are now absent. Its six render hashes are therefore
  historical byte facts only, not evidence that this live shared graph is
  usable. Any future frame preflight that borrows the affected shared path
  will fail at the same bounded inventory step before browser capture.

- **Tab:** tab qualification is primarily App `playwright-core` plus the App
  Remotion/Player hash checks. The affected shared graph is not the App
  `playwright-core` tree, and no direct tab graph corruption was found here.
  The six Remotion/Player hashes matching is insufficient to qualify the tab
  graph’s complete topology; browser/live-socket qualification remains
  unrun. The separate App Playwright fingerprint/controller issue must not be
  conflated with this 106-link drift.

## Minimal lead recovery

1. Keep the affected graph untouched and do not grant or run root smoke,
   presenter, or mouth qualification against it.
2. Have the Viewing manager nominate an exact retained last-good graph copy,
   or an owner-reviewed equivalent, whose controller-equivalent manifest is
   the retained 21,495-entry manifest plus no package-directory self-links.
   Do not use an arbitrary fresh install or broad setup replacement.
3. Recreate/retain the Agent source lease at commit
   `5acd7233df676bf42b2086d86cb0a6358398bf5f` / tree
   `66898dd11df74e205af95903651782a29e9886b4`, then rerun the fixed
   controller’s offline `prepare` and existing verifier. The fixed controller
   hash must be recorded; the old READY JSON must not be relabeled.
4. Only after source and graph equality is proven should a new manager grant
   be considered. No dependency repair, reinstall, deletion, or substitution
   was performed by this audit.

## Scope and commands

Read-only checks performed:

- `git show-ref`, `git cat-file`, `git worktree list` on the Agent repo for
  source/lease facts;
- `find -P`, `readlink`, `stat`, and bounded `os.scandir` inventory of the
  affected graph and named PCM/App/Composition/retained-Agent graphs;
- cycle-safe manifest comparison against
  `handoff-vw-m3-root-smoke-central-ready-prepare-pre.json`;
- six `sha256sum` checks against the controller constants;
- the bounded controller `inventory()` reproduction above;
- `git status --porcelain=v1 --untracked-files=all` in the assigned worktree.

Results: all read-only checks completed; assigned worktree remained clean.
No browser, socket, renderer, install, reinstall, delete, dependency repair,
network, central test service, full suite, or product/repository change was
made. No commit message or DONE marker was created, per this task’s explicit
read-only handoff scope.
