# Composition root join — step 1 review

**Verdict: BLOCK the ancestry join.** Main is **not fully represented in the original integration root**. Six main paths are absent, including both compiler configurations and both test files. Later repairs must not be attributed to that root. Current integration also lacks main's Makefile; its `clean` convenience has no explicit replacement or settled retirement rationale. No join was performed, and steps 2–3 are not qualified.

Authority: [PLAN](../PLAN.md), especially settled decisions 1–2/9–10, M0/M3/M4, and the delivery decision; [Viewing INBOX, 07:53Z](../managers/viewing/INBOX.md). The latter requires proof against the **original root** before an `ours` merge, and escalation with the file list if proof fails. This report follows that condition rather than treating every inherited difference as intentional.

## Exact objects and scope

All objects were inspected read-only in `/home/user/work/wt/vw-m4-composition-root-coverage`. The primary repository's `origin/main` and `/home/user/work/composition`'s HEAD independently resolved to the main/current objects below.

| Role | Commit | Tree | Tracked paths |
|---|---|---|---:|
| `origin/main` (v0.0.6) | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` | 29 |
| Integration's only original root | `f9da6c0477feb73a7d0f13f37bed3e4861254cd2` | `1d92ed9b6a1a77ee382c84205419e878cf49ef4d` | 86 |
| Frozen R4 Composition / integration start | `c82eb7c459d0a41263954bf007071a6a0e8e0a6a` | `49975e7a54fd594e1b7fc807681fe28611d57864` | 92 |
| Current `tl/integration` and worker HEAD | `5e06f40146573a529896cc812229eb890c53c81a` | `61d54da1d6a5b1f26132602cec49e84bded87805` | 110 |

Main's only root is `a759dfe61ac93db6641aad7439e46ab38469053f`, tree `dc09c855bb3f5e543d5f2fd536bc9efd7b168ffd`. Integration has only `f9da6c0`, **not** `c82eb7c`, as its root. `git merge-base origin/main HEAD` produced no SHA and exited **1**. The histories remain unrelated.

The original-root commit body states: “This initial import contains the authenticated npm package payload only (86 members), not the former repository tests or history.” That explains the loss; it does not authorize deleting main's repository infrastructure under the forward-port plan.

[Flat classification](composition-root-join-files.tsv) contains **157 rows**, the complete union of all four trees, with path, mode, object type and full blob ID per tree, each comparison against main, and a class/replacement rationale. Equality means identical mode/type/blob, not filename similarity. All entries are ordinary `100644` blobs. Recursive NUL-delimited enumeration includes dotfiles, scripts, docs, configs and generated output; no source-only filter was used. Main contains one documentation file (`README.md`), no tracked LICENSE/LICENCE, separate docs directory, binary/media assets, symlinks or submodules. None were silently excluded.

| Comparison to all 29 main paths | Equal | Changed | Missing | Extra paths absent from main |
|---|---:|---:|---:|---:|
| Original root | 10 | 13 | 6 | 63 |
| Frozen R4 start | 10 | 13 | 6 | 69 |
| Current integration | 5 | 21 | 3 | 84 |

## Missing content: exact list and disposition

| Class | Main path absent in original root (also absent in frozen R4) | Actual current replacement / remaining gap |
|---|---|---|
| C1 | `.gitignore` | Restored by `6a3247d`; current ignores dependencies and generated/test output while tracking the lockfile. This is a later M0 repair, not root coverage. |
| G1 | `Makefile` | Still absent. `install`, `build`, `test` delegated to npm and have direct equivalents. `clean` removed `typescript/dist` and `node_modules`; current build only cleans `dist`. No make compatibility wrapper or full cleanup equivalent exists. No explicit settled decision retires it. |
| G2 | `typescript/tests/scaffold.test.ts` | Still absent. Its constant-equals-itself tag assertion fits PLAN's literal-test cut. Its other test checked generated registry existence and both exported registry symbols: real coverage, not just ceremony. Root has neither test nor replacement runner. Current `scripts/gen-registry.test.mjs`, `typescript/tests/registries.test.ts` and the package smoke exercise generation/exports instead (`6a3247d`, `ed897544`). |
| G3 | `typescript/tests/theme-api-smoke.ts` | Still absent. Main's downstream type probe imports `composeAnimations`, `useTheme`, `EffectProps`, `AnimationReferenceList`, `RuntimeTheme`. Root retains those exports but has no executable downstream typecheck replacement. Current `scripts/smoke-package.mjs` probes public ESM and strict NodeNext declarations; `typescript/tests/theme.test.ts` exercises `useTheme`/provider identity, and the strict source build checks the retained types. Replacement source exists now; no such smoke was run in this review. |
| G4 | `typescript/tsconfig.json` | Restored by `6a3247d`, then upgraded by `ed897544`: full strict source/declaration build, `noEmitOnError`, emitted declarations for built package, no host aliases. Root's `build`/`build:ts` reference this missing path; masked failure is not representation. |
| G4 | `typescript/tsconfig.test.json` | Restored by `6a3247d`; current compiles full source and `*.test.ts` to `typescript/test-dist`. Root's `build:test` references this missing path. Its `test` command additionally references absent `typescript/tests/register-extensionless.mjs` (not a main file, but another dangling reference). |

Thus even granting the documented current test replacements, the literal original-root condition fails. The Makefile deletion is also unresolved in the current-tree interpretation. Do not silently replace the requested original-root proof with “the current package builds.”

## Changed main content: intent and actual source replacement

These classifications account for main differences; they do **not** claim pixel/audio parity or retroactively qualify the root's missing build/test infrastructure. Paths below are relative to the repository; object-qualified references are readable with `git show <commit>:<path>`.

| Class / main files | Source-backed disposition and replacement |
|---|---|
| C0 — `typescript/src/lib/{duration.ts,effect-params.ts,render-bounds.ts,tracks.ts,trim.ts}` | Exact mode/blob equality in main, original root, frozen R4 and current. Duration, track selection/order helpers, placement/crop geometry, params and source trim implementations were not lost. |
| C1 — `package.json`, `.gitignore`, `typescript/tsconfig*.json` | PLAN M0 and explicit cut of stale `dist`/`|| true`; M3 one published package. `6a3247d` restores honest source checks, removes unused schema dependency and tracked generated JS; `31cbb92d` adds reproducible setup/lock; `ed897544` adds `scripts/build.mjs`, built ESM/declarations and exact React 18.3.1/Remotion 4.0.509 peers (INBOX 2026-10-19 source-ownership conditions). Source/deep generated subpaths are replaced by public `./{effects,animations,transitions}.generated`; `./theme-api`, root and theme registry remain public built entries. README explicitly documents the ESM-only surface and host migration. Root package extensions alone do not fix its missing configs. |
| C2 — `README.md` | Root retains main's complete scaffold/build prose and adds transition/evaluation/keyframe contracts. Current replaces obsolete monorepo scaffold instructions with actual package API, build and host-map guidance (M0 runnable instructions / M4 architecture guidance). No separate main docs were dropped. |
| C3 — `scripts/gen-registry.ts`, `typescript/src/{animations,effects,registry,transitions}.generated.ts` | **All five equal main in original root/frozen R4.** Current's `ed897544` implements the approved 13-component relocation from App: local `builtins/` plus `scripts/builtin-inputs.json`. Same six animation IDs/defaults, `text-card`/`text` alias, two transition IDs/defaults, four 2rp clip types. Package scanning of installed/workspace themes is intentionally replaced by host-owned resolved maps (`registries.ts`, `RegistryContext.tsx`, `TimelineComposition.registries`), preserving custom-pack dispatch through that seam. `760230ec` makes easing support registration-owned. Bundled 2rp is **0.1.0**; equality to external 0.1.1 is explicitly unverified, not assumed. Evidence sources: PLAN 2026-10-19 component decision, INBOX source-ownership conditions, `ed897544` body, current README “Scoped host elements”, registry tests. |
| C4 — `typescript/src/AudioTrack.tsx` | Root already replaces main's frame-sampled fade callback with `lib/use-audio-envelope.ts` → `lib/audio-envelope.ts` (`compileAudioEnvelope`, `applyAudioEnvelope`). Trim, playback-rate sanitization, mute and track×clip volume remain in the renderer. This is an **audible intended difference**, not equality: PLAN continuous PCM gain policy (up to ~0.7 dB mid-fade), honored `fadeInCurve`/`fadeOutCurve`, with owner-film review required. Player readiness/encoded-source behavior exists in the hook; not exercised here. |
| C5 — `typescript/src/TimelineComposition.tsx`, `VisualClip.tsx`, `lib/fade.ts`, `lib/transitions.tsx` | Root's scene/per-boundary planner, `ClipLook`, `TransitionLayer`, `lib/transition-spans.ts` and `lib/clip-look.ts` replace main's pair-only `renderTransitionGroup`/`CrossFadeLayer`/`TransitionSeries`. Authority is PLAN keep Composition evaluator / single See evaluator and the explicitly approved owner release `6bd784d8e51005ce15b7b9714ea9fb4df9730373` (tree `863366b1a698b51e71188e5bde0f462a08cce4be`): element opacity/crop/fades/entrance/exit, per-boundary dissolve vs dip/chains and speed remapping. Main's bare element clips therefore **change intentionally**, including overlapping independent fade DIP (PLAN revised 04:02Z). `VisualClip.applyOpacity` defaults true; the outer modifier path can own it once. `useFadeOpacity` delegates to the same pure linear ramp helper, with a zero-rounded-length guard. Current further adds explicit canonical incoming compilation (`92a6ba99`, PLAN incoming-transition decision), opt-in native pre-roll (`55342500`, INBOX 21:50Z), and public shared opacity (`899342b5`). Native outgoing vs canonical incoming contracts are documented separately; no blanket transition-equivalence claim is made. |
| C6 — `typescript/src/{effects-types.ts,index.ts,theme-api.ts,types.ts}`, `lib/animations.tsx` | Root retains main's named public exports/model fields and adds evaluator, modifier, keyframe/loop and clock contracts; main's animation hook/wrapper composition remains, with explicit easing/progress added. PLAN keeps the Composition evaluator and existing-film playback, and defines shared reference/element seams before extensions. Current adds scoped registry contracts, declared component capabilities/diagnostics, generic effect params, keyframes, canonical compiler output, media trim/rate exports (`7d663330`), registration-owned easing (`760230ec`), and shared animation phase. Replacement implementations live beside the public exports, not in a second viewer. These are additive source/API classifications, not authorization for M5 authoring or proof every downstream consumer is migrated. |
| C7 — `typescript/src/ThemeContext.tsx` (also Composition canvas ground) | Root changes only visibility of `toRuntimeTheme` to an export. Current `5d26afc5` / `35bca092` changes the **complete implicit default** from black/Georgia/white to existing Agent export navy/Arial/cyan, including sizes/weights/lineHeight/fadeMs and canvas ground. Authority: PLAN FINAL ~06:20Z plus 06:29/06:33 version correction, shipped as immutable 0.0.12. Explicit film themes still pass through the provider. Actual source replacements: `DEFAULT_THEME`, `TimelineComposition` default ground, `scripts/check-agent-default-theme.mjs`, `theme.test.ts`. This is an approved preview difference, not missing main styling silently described as equal. |
| C8 / C10 — all remaining non-main paths | Complete individual membership/blob inventory is in the TSV. New tests/loaders, local builtin assets (JSON/TSX), build scripts, registries and evaluator helpers are additions, not evidence main had them. Root/frozen generated `typescript/dist/**` is intentionally removed under PLAN's stale-output cut (`6a3247d`) and generated by the honest build instead. The root ID-specific animation-progress adapter is replaced by registered components/metadata (`ed897544`/`760230ec`), rather than kept as a duplicate path. |

## Checks performed and next authorized step

Read-only commands (repo cwd above):

```sh
git status --short
git rev-parse HEAD origin/main tl/integration origin/codex/handover-timeline-r4-20261019-candidate-composition
git rev-list --max-parents=0 tl/integration
git rev-list --max-parents=0 origin/main
git show -s --format='%H %T%n%P%n%s' origin/main f9da6c0 c82eb7c HEAD
git show -s --format=fuller f9da6c0
git ls-tree -rz --full-tree origin/main
git ls-tree -rz --full-tree f9da6c0
git ls-tree -rz --full-tree c82eb7c
git ls-tree -rz --full-tree HEAD
git diff --name-status --no-renames origin/main f9da6c0
git diff --name-status --no-renames origin/main HEAD
git merge-base origin/main HEAD
```

Results: clean worker tree; one integration root; counts and identities above; six original-root omissions / three current absent paths; merge-base exit 1. Per-file source diffs, original and replacement test/config bodies, and the cited change commits were inspected. TSV completeness/hash membership was checked against all four actual trees (157/157 rows, all 29 main paths represented in the classification; **PASS**).

**No product tests were run:** this is a read-only tree/source audit, with no product/test edits. No full, browser, socket, build, install, merge, ref mutation, or claim of dynamic compatibility. Existing test results elsewhere were not rerun or used as a substitute for this proof.

Area lead/orchestrator should resolve the failed condition before any external merge: acknowledge the six original-root omissions, decide whether later current-tree replacements satisfy a revised proof criterion, and restore or explicitly retire the uncovered Makefile interface. This worker does not alter those settled boundaries or repair product files. Only after accepted coverage proof should the authorized external executor perform INBOX steps 2–3 and verify unchanged tree plus merge-base/refresh behavior. Neither the `ours` join nor its postconditions are claimed here.
