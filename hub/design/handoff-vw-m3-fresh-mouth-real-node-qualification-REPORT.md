# Fresh mouth context-carry: actual registered-Node qualification

## Result

**QUALIFIED within scope.** The final central lane ran the actual registered
presenter query with the retained Node 20.19.4 runtime, immutable Composition
0.0.12 package, and read-only f816 peer tree. The intended group was selected
explicitly and passed **4 tests in 3.57s**, with zero skips and zero
deselections:

- fresh public facts drive the existing consumer;
- planted stale clip identity refuses the public facts;
- planted forged ROI refuses the public facts;
- missing public fact refuses the public facts.

The retained PNGs, selected keys `[0, 3, 4, 5]`, strict 2% comparator,
denominator, cached/mixed fallback, and final-properties checks were not
replaced or weakened.

## Environment and identity

The central command uses the fixture's actual environment keys:
`ASTRID_NODE_EXECUTABLE`, `ASTRID_COMPOSITION_TEST_ARTIFACT`, and
`ASTRID_COMPOSITION_TEST_NODE_MODULES`; `NODE_OPTIONS` and `NODE_PATH` are
unset. The exact identities were checked before the final run:

| Input | Identity |
|---|---|
| Node | `v20.19.4`; SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490` |
| Composition package | public12; SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; 77 members |
| Peer root | `/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules`, read-only |
| Retained f816 peer graph | 21,488 entries; SHA-256 `9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425`; 21,429 files |
| Registered owner | discovered `pack:astrid_motion`; root is this checkout's `am-presenter` directory |
| Peer module origins | fixture preflight resolves React/React-DOM from the peer root at 18.3.1 and Remotion packages at 4.0.509; pre/post peer identity maps were equal |

The fixture generates the ordinary host registries, extracts the immutable
tarball, and runs the public `querySceneFrame` against the prepared Root. It
does not copy Python geometry/clock/codebook logic, construct a fake source
certificate, or stub Node/scene/registry.

## Owned fixes and compatibility decision

The public query fixture had a genuine caller defect: it called
`querySceneFrame` without importing it. The smallest fix adds the normal
Composition evaluation import.

The current branch still contains the pre-`ee710` presenter source. Its public
normalizer gives raw partial `{x, y}` a width-19 ROI while the legacy private
crop remains width 16 (697 px). The owned consumer now requires a complete,
valid raw `{x, y, w}` anchor before activating fresh public ROI facts. Default,
partial, clamped, malformed, or fractional anchors retain private
crop/statistics fallback until the owner capability is current. Explicit
`{x: 151, y: 104, w: 19}` remains the qualified positive. No unqualified
component swap or source activation was claimed.

## Evidence

- Central service result:
  `vw-m3-fresh-mouth-real-node-qualification-integration-viewing-mouth-fresh-context-carry-1020153431-24440`
  — **4 passed in 3.57s**, exit 0.
- Local final aggregate lane — **21 passed in 4.34s**.
- Local neighboring crop-equivalence lane — **9 passed in 3.71s**.
- Ruff, Node `--check`, and `git diff --check` — passed.
- The final source tree was `6eefc775bd35441be522e7ccbb03dbb86794945d` in the
  central snapshot.

No browser, decoded-pixel capture, renderer, localhost/live socket, install,
network, or full suite was run. Prior 40-pure/71-central runs with environment
errors and a missing artifact remain non-equivalence evidence and are not
relabelled.

## Scope and next steps

Changed product/test-owned files are limited to the adapter guard, the query
fixture import, and two compatibility regression cases. Private crop math,
statistics, thresholds, cached/mixed fallback, source factory, DTOs, public
API, store, and geometry-copy paths were not changed. The next owner step is
to land the exact `ee710` presenter capability source, then separately qualify
any broader activation or private-crop retirement; this result does not claim
those changes.
