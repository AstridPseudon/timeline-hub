# Default-theme owner-review proposal — UNAPPLIED

Bounded design complete. **Hold the candidate: it preserves existing Agent export defaults but changes the legacy App absent-theme preview.** This is a proved preservation conflict, not a green integration fix. No production source, core, provider, Runtime, pin, package, fixture, comparator or authored document changed. No rendering, browser, network, installation, full suite or central test request. PLAN and the three requested frame-zero handoffs read.

## Recommendation and owner decision

Recommend **one canonical default adapter in the App, sourced semantically from Agent `builtin_theme()`**, with the composition ground painted from that resolved theme. Keep Agent's existing exported-film default `#050814` and its complete type/color/motion defaults. Keep the public Composition package default unchanged for its other hosts. Do not apply the prior one-field core-to-black patch: it changes existing exported films and leaves typography/accent differences unresolved.

`UNAPPLIED-app-theme.patch` is the concrete two-file candidate: `installed-themes.ts` adapts only the no-installed-theme/default base; `TimelineRenderer.tsx` paints `theme.visual.color.bg`. The adapter is an explicitly documented compatibility copy, not a newly published authority or a new theme protocol. Its literal was extracted from the actual Agent constant using Python AST; exact full-object equality is tested. A future change to Agent's default requires reviewing this adapter too. There is no new field, endpoint, capability, package, theme discovery or task backend override.

**Evidence against immediate application:** App already has a passing behavior test for absent-theme Georgia/white/black preview. Matching the existing export default necessarily changes that preview. The original expectation remains byte-for-byte in the test patch, marked `it.fails` with the preservation requirement, as instructed. This expected failure is outstanding work, not approval to lose behavior. The orchestrator/owners must resolve preservation of legacy absent-theme App films before enabling the candidate. Preserve their intended style through an explicit authored selection using existing theme/overrides only if the owner authorizes that edit through the normal command path; this proposal does not rewrite films or fixtures and does not invent how a legacy film's intended source is identified. No claim that the current candidate preserves both incompatible implicit defaults.

Why no explicit task `theme` pass-through recommendation: normal managed admission does not have such a field or accept browser composition props as theme authority. Adding one would cross the provider/Runtime contract. Full authored `theme_overrides.visual` already exists, but silently filling it during a parity fixture/export would change authoring semantics and would hide the default mismatch. This proposal uses the existing App resolution seam and leaves that boundary untouched.

## Source findings and exact owners

Inspected Agent assigned HEAD `6b108a8ef5b8a658bae26de59b373342dec40c71`, leased/frozen host `b70b9d569b2c80885d72734c61cd57e64c3715a8`, current App `cc4dff86b845432acc38dd9407ccb079a6a5a677`, Composition `ff0536bb53d84db5008b859be304b932b1dd5252`. Also read frozen R4 SDK/App/Composition sources with `git show`; no checkout. Agent core default and shared theme resolver are unchanged between assigned HEAD and b70; frozen R4 also has the same default. App installed-theme resolver has no diff against frozen R4. Frozen R4 Composition default matches current source values below. These are source observations, not an executed cross-product tuple.

| Owner | Exact repository path / seam | Finding / action |
|---|---|---|
| Agent core owner, read only | `astrid/core/theme/_schema.py:175` (`BUILTIN_DEFAULT_THEME`), `builtin_theme()` | Existing complete exported-film default. No proposed core edit. |
| Viewing | Agent `astrid/packs/rendering/shared/rendering_backend/__init__.py:89` (`_resolved_theme_for_render`) | Runtime-pinned `theme.json` wins as base; otherwise builtin; authored visual overrides overlay it. Historical slug is metadata, not filesystem lookup. No resolver edit. |
| Viewing | Agent `astrid/packs/rendering/rendering/renderers/remotion/run.py:1103` | Explicit resolved `theme` serialized in Remotion props, also supplied to timeline serialization as default id. |
| Viewing | Agent `remotion/src/Root.tsx:83` | Spreads incoming props to public `TimelineComposition`; resolves host registries from `props.theme ?? DEFAULT_THEME`. |
| App editing / producer owner | App `src/tools/video-editor/lib/renderRouter.ts:856`, `:935`, `:965` | `buildRenderTimelinePayload` retains theme id and timeline locally, but actual admission sends `timeline_ref`, optional expected version, selector, output name, and canonical identity metadata. No resolved theme document in task params. `theme_id` local fallback is `2rp`; it is not a materialized runtime theme or exported prop. Read only. |
| Runtime/provider owners, read only | Runtime `runtime_protocol/managed_render_snapshot.py`; Agent `astrid/packs/rendering/actions/render/managed_timeline.py`, `task_adapter.py` | Server snapshot/projector is authority. Current legacy adapter stages config and registry; caller backend options are forbidden. No proposed transport/provider change. |
| Viewing | App `src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx:90`, `:539` | Live Player mounts `PreviewComposition` -> `TimelineRenderer`, with config. |
| Viewing + App shared-file review | App `src/tools/video-editor/compositions/installed-themes.ts:90` | Existing installed theme or package default, then authored recursive overrides. Proposed default adapter lives here; `2rp`, custom installed themes, registry API and overrides stay on their existing path. |
| Viewing | App `src/tools/video-editor/compositions/TimelineRenderer.tsx:1591`, `:1727` | Live effects get resolved theme, but canvas ground is independently hardcoded black. Proposed ground uses resolved background. |
| Composition owner, read only | `typescript/src/ThemeContext.tsx:48`, `typescript/src/TimelineComposition.tsx:328`, `typescript/src/types.ts:99` | Public default black; optional existing `props.theme` used both for ground and provider. No package changes. |

**Source-name correction:** there is no tracked `publicComposition` file/symbol in the inspected current App or the retained native-frame candidate. Current live Player still uses `TimelineRenderer`. The public Composition default is the separate package's `DEFAULT_THEME`. Do not apply a patch to an inferred public-adapter path or claim current live Player has already migrated to it.

## Complete differences and actual fixture relevance

| Field | Agent builtin / unpinned export | Public package / App default |
|---|---|---|
| id | `banodoco-default` | `banodoco-default` |
| foreground | `#FAFAFA` | `#ffffff` |
| background | `#050814` | `#000000` |
| accent | `#67E8F9` | `#ffffff` |
| heading/body | Arial / Arial | Georgia, serif / Georgia, serif |
| mono | monospace | omitted |
| size base/small/large | 32 / 22 / 84 | 64 / 36 / 96 |
| normal/bold weight | 400 / 600 | 400 / 700 |
| line height | 1.2 | 1.1 |
| fadeMs | 450 | 250 |
| canvas | 1920x1080, 30fps | identical |

The retained native fixture has a still on V1 at frame0, video from frame120 to165 exclusive, and audio on A1; no authored theme override, text or themed element. Thus the theme ground is directly relevant to its uncovered contain sidebands. Typography/accent/motion do not explain those frame0 still pixels, but materially affect text-card and theme effects in real films (`typescript/src/builtins/effects/text-card/component.tsx:118` consumes foreground, heading, base size, weight and line height). App's plain `TextClip.tsx:43` also has independent Georgia/64/white fallback values: changing a resolved theme is not proof of all text rendering parity.

Reused offline evidence only: different-case unobstructed readiness versus positive export frame0 has **526658 / 2073600 pixels outside2, max20, mean3.033262**. Export encoded sideband sample `[5,6,20]`, readiness `[0,0,0]`; source navy is RGB `[5,8,20]`, so encoded samples are not asserted to equal the CSS triplet. This is not the same-case positive, not a substitute baseline, and not certification. Original positive was obscured by modal/backdrop; its comparator failure remains distinct. No image/media changed or decoded in this task. No claim that this proposal makes the strict comparator pass.

## Authored and custom cases

New App tests compare the full default for absent/default/uninstalled slugs, preserve package `DEFAULT_THEME`, preserve the entire installed `2rp` style plus authored background overlay, preserve a complete authored visual theme, and verify partial accent override isolation. Rendering tests paint resolved default, authored custom background and installed `2rp` ground using the existing main suite's DOM/Remotion mocks; these are CPU component tests, not pixel tests.

New Agent preservation tests prove unchanged builtin for historical `theme='2rp'` without a runtime pin, full explicit host style via existing runtime `theme.json`, and authored color overrides preserving the remaining builtin/host style. Existing Hype golden and profile tests also passed. Host file resolution, CSS/font availability and registry selection are untouched.

Limits: a host-custom theme file is not currently transported to App simply by a matching slug. The existing App installed registry and explicit full authored visual override remain intact, but arbitrary host-theme preview parity is unproved and is not solved by this default adapter. Existing App recursive merge versus Agent's shallower merge of nested type/family overrides is another distinct source-level gap; no speculative merge-policy change is included.

## Exact commands and evidence

`W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-default-theme-owner-proposal`
`D=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-default-theme-owner-proposal-`
`NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node`

In a private offline App tree under `$W/offline-app`, unchanged source/dependencies are read-only links; the candidate production/test files are private copies. The existing App Vitest config is extended only to point at those copies, retain the App setup/aliases, disable test cache, and select two files. No app/integration/other-worker file was edited.

```sh
cd "$W/offline-app"
$NODE /home/user/work/app/node_modules/vitest/vitest.mjs run --config offline-vitest.config.ts --maxWorkers=1
# Original product + proposed assertions (original legacy test unmarked): exit1,
# 6 FAIL / 48 PASS; red.log. Six failures are actual semantic assertions.
# Candidate product, original legacy behavior expectation still unmarked: exit1,
# 1 FAIL / 53 PASS; candidate-regression.log. Failing legacy assertion is kept.
# Candidate product + final UNAPPLIED test patch: exit0,
# 53 PASS / 1 EXPECTED FAIL; candidate-with-preservation-xfail.log.
$NODE /home/user/work/app/node_modules/eslint/bin/eslint.js src/tools/video-editor/compositions/installed-themes.ts src/tools/video-editor/compositions/installed-themes.test.ts src/tools/video-editor/compositions/TimelineRenderer.tsx src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx --max-warnings 0
# exit0, lint.log empty.

cd /home/user/work/wt/vw-m3-default-theme-owner-proposal
PYTHONPATH=/home/user/work/wt/vw-m3-default-theme-owner-proposal /home/user/work/venv-agent/bin/python -m pytest -q "$W/test_default_theme_resolution.py" tests/packs/rendering/test_remotion_backend.py::test_hype_merged_render_props_match_golden tests/packs/rendering/test_remotion_backend.py::test_explicit_missing_theme_path_does_not_fall_back_to_workspace_theme tests/core/rendering/test_profile.py
# exit0: 15 PASS in3.02s; agent-targeted.log. New3 + existing12.
cd "$W"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-host-agent-source /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider test_default_theme_resolution.py
# exit0: 3 PASS in2.73s; b70-preservation.log.

git -C /home/user/work/app apply --check "${D}UNAPPLIED-app-theme.patch" "${D}UNAPPLIED-app-tests.patch"
git -C /home/user/work/wt/vw-m3-default-theme-owner-proposal apply --check "${D}UNAPPLIED-agent-tests.patch"
git -C /home/user/work/wt/vw-m3-default-theme-owner-proposal diff --check
# all exit0; check only, no apply.
```

The proposed tests are patches destined for main's existing Vitest/pytest suites, executed here only in private copies / standalone pytest placement because other owners' files are read only. Main suite registration after actual application is not claimed. Typecheck, browser, actual render, audio/PCM, planted negative, normal task end-to-end and full suites were NOT run. No test was skipped, deleted or weakened to manufacture a pass.

Flat artifacts: `UNAPPLIED-app-theme.patch`, `UNAPPLIED-app-tests.patch`, `UNAPPLIED-agent-tests.patch`, all named logs above, the Agent test source and `replay.py`. Replay reconstructs the private App tree from current source and cleans it afterwards: `python3 "${D}replay.py"` reproduces the six semantic red cases; add `--candidate` for the explicitly disclosed expected-fail candidate. This replay is offline unit testing, not normal-profile rendering. Patches remain unapplied in every repository.

## Next action

Route the two App production paths and preserved failing legacy expectation to App/Viewing owners, with Agent owner confirming that existing export styling remains authoritative. Resolve the legacy App absent-theme preservation requirement before application; if that requirement is unconditional, reject this global adapter rather than deleting the test. Keep runtime/custom-theme transport and nested override gaps explicit. After an approved source-policy patch is integrated, the manager may separately authorize a frozen normal-profile same-case render comparison, with the unchanged four cases,2/.001 bounds, successful positive baseline before planted negative, and the outstanding result-video abort handled independently. This design is no M3 gate or completion claim.
