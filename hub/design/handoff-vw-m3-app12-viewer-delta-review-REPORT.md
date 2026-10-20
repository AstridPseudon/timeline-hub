# APPROVE — App viewer safety12 delta

## Verdict

**APPROVE.** No defect found in the exact handoff patch
`handoff-vw-m3-app-current-viewer-cut-UNAPPLIED-safety12.patch`.

Patch SHA-256: `2f8622a48ecf983cffaaba58f7a190bd7b900fc9b934c60dfc35158206f3ef8f`.
It is exactly two files, `+36/-72`: one renderer line and one test file.

## Review findings

- Against the selected App safety cohort `9d9101fef15470c813d060ed0169676fa7206c2e`, the patch applies cleanly.
- The only product change is `backgroundColor: 'black'` to `backgroundColor: theme.visual.color.bg`. `theme` is the existing `resolveTimelineRenderTheme(renderConfig)` result, so fallback, installed themes, and authored `theme_overrides` use the same resolved theme already passed to viewers.
- The test change preserves the existing full runtime-theme mock and actual public exports, replaces stale literal default assertions with the public package `DEFAULT_THEME`, adds fallback canvas coverage, and adds explicit authored-background coverage.
- The duplicate partial `theme-api` mock is removed. No new evaluator, private-package import, adapter growth, projection/root-pin edit, or product fallback writer is introduced.
- The existing explicit/custom/dynamic/live dispatch, native crop/half-open/opacity behavior, and painter/native paths are untouched by the two-file patch. The adapter source in the safety cohort remains byte-identical to the approved source (`addb46bd84fae79763e52815f29902c83e33ee0bfcb385ae23479628123f32b2`).

## Evidence

Exact safety-cohort overlay (`9d9101f…` + safety12 patch + public12 package):

```text
vitest: 8 files, 136 tests passed, 0 failed
tsc -p tsconfig.viewer.json --noEmit: exit 0
```

Current handoff overlay (`1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff` + current six-file handoff + public12 package):

```text
vitest: 8 files, 137 tests passed, 0 failed
tsc -p tsconfig.viewer.json --noEmit: exit 0
```

Vitest command in both runs:

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

These are direct jsdom/unit runs against public12. No browser, socket, full suite, install, or network run was performed; renderer pixel/audio parity remains unverified here.

## App-owner apply instruction

Apply exactly this absolute patch to the selected safety cohort / coherent App refresh:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app-current-viewer-cut-UNAPPLIED-safety12.patch`

Preserve the current theme-ground tests and the already-approved adapter. Do not re-port or grow the root/viewer adapter, infer canonical projection semantics, or edit root/package pins as part of this delta. If applying to current integration `1be0efd…`, this delta is already present and should not be force-applied.

## Blockers / next step

None for this review. The App owner should apply the patch only in the selected safety-cohort refresh, then run the central matched-tuple qualification when the reserved package/runtime pins are integrated.
