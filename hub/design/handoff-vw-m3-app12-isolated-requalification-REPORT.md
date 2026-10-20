# App 136/137 public12 isolated requalification

## Verdict

**APPROVE the pure public12 behavior/import claims, with one correction:** the
current safety overlay runs 137 tests, not the previously reported 136. The
observed count is 137 passed in both the safety and current overlays; no test
failure, skip, or expected failure occurred.

The old shared-readonly wording is explicitly corrected. The qualification
used read-only individual symlinks into the existing shared App package roots,
and the shared graph was byte-identical before and after setup/tests. However,
the shared graph was already not a frozen historical baseline: it contained
the six newer symlink entries identified by the package-additions audit. This
run proves no mutation during qualification; it does not restore, approve, or
historically validate that shared baseline.

## Exact source/package identity

- Node: `v20.19.4` (`/tmp/vw-m3-agent-gate-node20.19.4/bin/node`).
- Safety source: `9d9101fef15470c813d060ed0169676fa7206c2e` plus safety12 patch
  SHA-256 `2f8622a48ecf983cffaaba58f7a190bd7b900fc9b934c60dfc35158206f3ef8f`.
- Current source: `1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff` plus current patch
  SHA-256 `91d95c22dc100b17bdf6e75d6384651e2c35830830a420ca35bfcf9572839eee`.
- Public12 archive: SHA-256
  `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`,
  58,444 bytes, exactly 77 extracted files. Both overlays match all 77
  archive members.
- Observed package versions: Composition `0.0.12`, React/React DOM `18.3.1`,
  Remotion/media/player/layout-utils `4.0.509`, Vitest `4.1.5`, TypeScript
  `5.9.3`.
- The six qualified source files have the handoff hashes from
  `handoff-vw-m3-app-current-viewer-cut-source.json`; the product worktree
  remained clean throughout.

## Import/default proof

In both fresh overlays, Node imported the package root, `/evaluation`, and
`/theme-api`; all realpaths are under that overlay's exact
`public12/package/dist`, never under shared `node_modules` or a private source
tree. Root exports `prepareCompositionScene` and
`compileCanonicalTransitions`; evaluation exports `prepareScene` and
`clipOpacity`.

The imported public `DEFAULT_THEME` exactly matched the navy full control:
`banodoco-default`, foreground `#FAFAFA`, background `#050814`, accent
`#67E8F9`, Arial/Arial/monospace, sizes `32/22/84`, weights `400/600`, line
height `1.2`, fade `450ms`, and canvas `1920x1080@30`.

TypeScript strict resolution passed in both overlays. `--traceResolution`
shows the Composition root/evaluation/theme-api declarations resolving to the
corresponding overlay `public12/package/dist/*.d.ts`, package ID `0.0.12`.

## Shared graph proof

The cycle-safe snapshot hashed every regular-file byte, symlink target byte,
entry kind, and mode without following links. Before and after setup/tests:

```text
entries  35618
files    32280
symlinks 193
dirs     3145
graph    5cee798b188c363cba6737bc53e7dfc5f65265cdcfeae21ae993797e9fc8b6d1
```

The six existing additions were present in both snapshots:
`@playwright/test/test`, `@remotion/player/player`, `@remotion/media/media`,
`@remotion/web-renderer/web-renderer`, `@remotion/layout-utils/layout-utils`,
and `@banodoco/timeline-composition/package`. No shared alias was used as an
overlay scope directory; `@banodoco`, `@remotion`, and `@playwright` were real
overlay directories with individually linked borrowed packages.

## Exact tests

The targeted command, run in each overlay with `--maxWorkers=1` (the final
recorded run was independently repeated after the initial qualification), was:

```sh
/tmp/vw-m3-agent-gate-node20.19.4/bin/node node_modules/vitest/vitest.mjs run --config qualification.config.ts \
  src/tools/video-editor/compositions/playerEvaluation.test.ts \
  src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx \
  src/tools/video-editor/compositions/VisualClip.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.dynamic.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.public-host.qualification.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.shots.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.test.tsx \
  --maxWorkers=1
```

Results for both safety12 and current12: `8 files passed; 137 tests passed;
0 failed; 0 skipped/expected failures`.

```sh
/tmp/vw-m3-agent-gate-node20.19.4/bin/node node_modules/typescript/bin/tsc \
  -p tsconfig.viewer.json --noEmit --traceResolution
```

Results for both overlays: exit 0.

Evidence files:

- Tests: `handoff-vw-m3-app12-isolated-requalification-{safety,current}-tests.log`
- Types/resolution: `handoff-vw-m3-app12-isolated-requalification-{safety,current}-types.log`
- Identity/import/default proof:
  `handoff-vw-m3-app12-isolated-requalification-qualification.json`
- Shared before/after summaries:
  `handoff-vw-m3-app12-isolated-requalification-shared-before.json`,
  `handoff-vw-m3-app12-isolated-requalification-shared-after-tests.json`, and
  `handoff-vw-m3-app12-isolated-requalification-final-check.json`

No install, browser, socket, full suite, central grant, root/lock pin edit,
source edit, shared dependency write, or other worktree write was performed.
Pixel/audio parity and live/browser behavior remain unverified, as required.

## Recommended next step

Carry forward the pure public12/import/type claims and the explicit graph
non-mutation evidence. Update any handoff that says “136 safety tests” to
“137 tests in the current v4.1.5 environment,” and replace the old shared
“readonly baseline” claim with the corrected wording above. Keep central
matched-tuple/browser qualification as a separate owner/orchestrator step.
