# F-D22/V3: retained outer-geometry cause packet

## Disposition

**Source attribution: PASS. Behavioral/rendering qualification: not claimed.**

The three retained failures are faithful outputs of the approved Composition
0.0.14 evaluator and stale Agent capability-boundary expectations. They are not
an identified regression in the adopted artifact. No Composition, Agent test,
fixture, package, pin, lock, DTO, or parity behavior was changed.

The smallest owning source is Composition's public scene evaluator. The
smallest correction, if the V3 contract is to keep the now-adopted known
outer-geometry behavior, is Agent's three public12 expectation assertions:
retain the private positives and strict negative controls, but align these
three public assertions with the known `GAP` answers below. That correction was
not implemented here. Reverting the evaluator to `UNKNOWN` would contradict
the 0.0.14 release intent and would discard the V3 geometry source; it is not
justified by this evidence.

H9 V4 remains cut. This packet does not claim gate-6 parity, a full PASS, a
rendering PASS, or a new parity feature.

## Locked evidence and exact handoff result

The Agent handoff identifies the read-only base as Agent
`58316fd6e0ce8a1fb3b2b3826ec71906d29080de` (tree
`00c04` in the brief), with the retained profile Runtime
`3b926efab2eed122d374540baee297d4cdcec62a`, Node `v20.19.4`, Composition
`0.0.14`, and approved archive SHA-256
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

The profile correction changed only existing test support: Composition
0.0.13 -> 0.0.14, archive file count 77 -> 80/current chunk, current mapping
rules, and the locked 0.0.14 archive SHA. Product source, contract, lock,
archive, generated files, pins, dependencies, and environment were untouched.

The retained exact qualification command was:

```text
env PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/bin:/bin /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider
```

It was followed by the retained 40-node inventory in
`design/agent-F-D22-profile-fixtures-1454.md`; exact result: **34 passed, 6
failed, 1:50.75**. The six are the three outer-geometry nodes, the two audio
vectors owned by Agent, and the child-import/environment node owned by Agent.
The three untouched nodes are exactly:

```text
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_public12_outer_geometry_gap_does_not_erase_original_positive[outer0]
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_public12_outer_geometry_gap_does_not_erase_original_positive[outer1]
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_public12_outer_geometry_gap_does_not_erase_original_positive[outer2]
```

The independent full-run identity remains the retained Agent service
`agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679`, terminal FAIL,
exit 1, raw terminal SHA-256
`e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`, on
Agent `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`, Runtime 3b926, and the same
0.0.14 profile. It is retained as source evidence only; it is not a behavior
PASS.

## Production-caller trace

This is the mounted production path, not an unused helper:

1. Agent `scene_answers.host_frames_at` validates the exact Root props and
   delegates to `_query`; its source blob is
   `478e7b4c97e7deac4ee1086f373f9bf2d2fccd2f` at
   `astrid/core/rendering/scene_answers.py:99-124`. `_query` selects the
   admitted project, invokes `scene-query.mjs`, and passes the props/basis.
2. Agent `remotion/scene-query.mjs` source blob
   `7c0002a66af07ca73bffea56586cc49886792c5c` resolves the public installed
   export `@banodoco/timeline-composition/evaluation` at lines 7-10, loads
   `native-scene.mjs` for Root props at lines 15-18, and calls
   `querySceneFrame` at line 36.
3. Agent `remotion/src/host-scene.ts` blob
   `88876f3c393c238a563ba502d7ed13bf17558609` imports the installed package
   at line 1 and calls its `prepareCompositionScene` at lines 20-25.
   `remotion/src/host-registries.ts` blob
   `5e4c4165647e41c912a13d83d21a98a4ad54ed72` merges the generated host
   effect/animation/transition maps at lines 8-21, so the AM plate registry
   is in the evaluated closure.
4. The AM plate capability producer is Agent
   `astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/scene.ts`,
   blob `41ae6a8a0e6da584c3a5852dc598515a16194e2c`: `preparePlateScene`
   returns `presence: 'present'`, known full-canvas bounds, and rectangular
   opaque support when the declared background is an opaque hex color.
5. Composition `prepareCompositionScene` calls the resolved component's
   `prepareSceneCapability` before `querySceneFrame` (approved package
   source, `TimelineComposition.tsx:232-262, 258-260, 278-280`, current source blob
   `076163d3d049397e04abc547ba480e193700c9f6`). The approved package archive
   is the retained 0.0.14 artifact with SHA above.

## Exact source cause and evaluation math

Composition source at HEAD `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree
`5ab5191a296980a0a6bcd1178ab6902d6478a148`, has these relevant blobs:

- `scene-evaluation.ts`: `f8254482c8a7f38603460bb353cd2b36edc13204`;
- `lib/render-bounds.ts`: `146f0802e74814eebb38fcb2c4df6a37aa2169d5`;
- `lib/clip-look.ts`: `b35d1f8c546edf7b42b26b83c9ff27348f10f7ae`.

The exact source behavior is:

- `scene-evaluation.ts:226-232` treats `am-snap-plate` as an element and
  obtains its capability's target bounds.
- `:242-259` recognizes crop, evaluates built-in `fade-up`/`scale-in`,
  transforms known bounds, and applies element crop after the transform.
- `:306-322` derives `fullFrame`, layer coverage, and findings.
- `:335-341` returns `COVERED` only when the opaque rectangles cover the whole
  canvas; otherwise a known, non-dipping partial rectangle is `GAP`.
- `lib/render-bounds.ts:30-50,53-66,82-97` clamps crop values and clips
  render bounds to the 200x100 canvas.
- `lib/clip-look.ts:158-197` makes entrance active for frame `< duration`,
  and maps frame-0 built-ins to zero opacity; `scale-in` starts at 0.85 and
  `fade-up` starts translated down by 40 px.

For the fixture's frame 0, basis 200x100, fps 24, `src` and the default opaque
paper backing provide known full-canvas support. The expected-vs-source map is:

| node | retained test expectation | adopted 0.0.14 source result at frame 0 | cause / owning correction |
|---|---|---|---|
| `outer0`, `cropLeft: 0.2` | `UNKNOWN`, unknown bounds, `unknown-animation-geometry` | known bounds `{x:40,y:0,width:160,height:100}`, opacity `1`, visible `true`, `fullFrame:false`, opaque rect, no findings; coverage `GAP`, content `null` | **Stale expectation.** `scene-evaluation.ts:257-260` applies known element crop. No Composition source fix; Agent public assertion is the smallest correction if V3 semantics are retained. |
| `outer1`, `entrance: {type:'scale-in', duration:0.5}` | `UNKNOWN`, unknown bounds, `unknown-animation-geometry` | duration is 12 frames; known transformed bounds `{x:15,y:7.5,width:170,height:85}`, opacity `0`, visible `false`, `fullFrame:false`, no findings; coverage `GAP`, content `null` | **Stale expectation.** `:248-255` evaluates the declared built-in and `render-bounds.ts:82-97` clips the known result. No source fix justified. |
| `outer2`, `entrance: {type:'fade-up', duration:0.5}` | `UNKNOWN`, unknown bounds, `unknown-animation-geometry` | known transformed/clipped bounds `{x:0,y:40,width:200,height:60}`, opacity `0`, visible `false`, `fullFrame:false`, no findings; coverage `GAP`, content `null` | **Stale expectation.** Same known built-in path; no source fix justified. |

The `UNKNOWN` expectation would only be produced by the frozen pre-V3 logic,
which marked any entrance/crop as unknown. The frozen R4 candidate Composition
source does exactly that at its old `scene-evaluation.ts:84-88`. The adopted
V3 source was intentionally introduced by Composition commit
`c1f4c0b5e24742b61090fdb2a47774e2189709db` (`fix(composition): port reviewed
unpublished14 source`), which added the known clip-look/crop evaluator; the
current `CHANGELOG.md` records 0.0.14 as “Evaluate known clip-look scene
geometry, including renderer-aligned off-center crop and entrance transforms.”
That is direct evidence of an intentional source-boundary change, not an
accidental regression.

## Controls and limits

The profile handoff says the original SSR and painted-backing positives and
strict unproven-backing negatives passed under the corrected 0.0.14 profile.
The three private positives in the retained test remain meaningful and must be
kept: crop remains private `full_frame=False, opacity=1`; scale-in remains
private `full_frame=False, opacity=1`; fade-up remains private `full_frame=True,
opacity=0`. The four strict negative backing cases must also remain unchanged.
No claim is made that pixel alpha, media capture, renderer output, or full
parity has been proven by these scene answers.

## Contract boundary

This report performs no DTO or commit-semantics work. The full v2 request shape
remains preserved: `api_version`, `project_id`, `timeline_id`,
`base_revision_id`, `base_publication_id`, `commands`, `label`, and complete
`steps` (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`,
`reads`), plus `merge`, request `reads`, idempotency key, `dry_run`, `source`,
`rationale`, and `group_id`. The full `{data, receipt}` replies remain
accepted/merged (with historical rebased accepted), including canonical
closure/head/records/dependencies/effects/steps/history/undo_steps; previews
retain `would_status`; conflicts retain reason and head; invalid replies
retain code, path, hint, and suggested command. Nothing here changes that
contract or its production caller.

## Check status

Required report-only checks were reused or run as follows:

- retained qualification command: **reused**, 34 passed / 6 failed;
- full Agent run: **reused**, terminal FAIL only as source evidence;
- tests/typecheck/lint/full suite/browser/host scripts: **not run**, per brief;
- `git diff --check`: run after report creation; expected PASS;
- `git status --porcelain`: run after report creation; expected report-only
  untracked files;
- `git rev-parse HEAD HEAD^{tree}`: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`
  and `5ab5191a296980a0a6bcd1178ab6902d6478a148`;
- prescribed `$ORCH/artifacts/banodoco-timeline-composition-0.0.14.tgz`
  check: **FAIL in this environment** — observed
  `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`, not
  the required `819acf6b...2040234`;
- matching locked artifact retained in the prior Composition evidence:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-DB-composition-first-return-0757/controlled-pack-635f-20261023/banodoco-timeline-composition-0.0.14.tgz`
  hashes to the required
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` and
  was read without extraction or installation.

The artifact-path mismatch is an evidence-environment limitation to report,
not a reason to repin, copy, extract, install, or alter the package.
