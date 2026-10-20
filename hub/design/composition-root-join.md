# Composition root join — step 1 review

**Verdict: ROOTJOIN READY for the accepted CURRENT-coverage criterion.** The original integration root did omit six main paths, but the 08:20 decision accepts the later M0 repairs and the two explicit test retirements. Current HEAD now contains main's Makefile byte-for-byte via the approved wrapper merge. No history join has been performed; merge-base and dry-run postconditions remain for the lead.

Authority: [PLAN](../PLAN.md), especially settled decisions 1–2/9–10, M0/M3/M4, and the delivery decision; [Viewing INBOX, 08:20Z](../managers/viewing/INBOX.md). The accepted criterion is current-tree coverage after the documented M0 repairs, not the failed original-root criterion. This report preserves the original-root loss as history, while classifying every main path in the current tree.

## Exact objects and scope

All objects were inspected read-only in `/home/user/work/wt/vw-m4-root-current-coverage-final`. The primary repository's `origin/main` and current `HEAD` independently resolved to the main/current objects below.

| Role | Commit | Tree | Tracked paths |
|---|---|---|---:|
| `origin/main` (v0.0.6) | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` | 29 |
| Integration's only original root | `f9da6c0477feb73a7d0f13f37bed3e4861254cd2` | `1d92ed9b6a1a77ee382c84205419e878cf49ef4d` | 86 |
| Frozen R4 Composition / integration start | `c82eb7c459d0a41263954bf007071a6a0e8e0a6a` | `49975e7a54fd594e1b7fc807681fe28611d57864` | 92 |
| Current `tl/integration` and worker HEAD | `024f69501cfceb7f80d1c0c3fd26e6dd52568784` | `628286fa4d3128d53f2fc3a37fb3402b51d3232c` | 111 |

Main's only root is `a759dfe61ac93db6641aad7439e46ab38469053f`, tree `dc09c855bb3f5e543d5f2fd536bc9efd7b168ffd`. Integration still has only `f9da6c0`, **not** `c82eb7c`, as its root. `git merge-base origin/main HEAD` currently produces no SHA and exits **1** because the lead has not yet performed the history join. The histories remain unrelated until that authorized operation.

The original-root commit body states: “This initial import contains the authenticated npm package payload only (86 members), not the former repository tests or history.” That explains the loss; it does not authorize deleting main's repository infrastructure under the forward-port plan.

[Flat classification](composition-root-join-files.tsv) contains **157 rows**, the complete union of all four trees, with path, mode, object type and full blob ID per tree, each comparison against main, and a class/replacement rationale. Equality means identical mode/type/blob, not filename similarity. All entries are ordinary `100644` blobs. Recursive NUL-delimited enumeration includes dotfiles, scripts, docs, configs and generated output; no source-only filter was used. Main contains one documentation file (`README.md`), no tracked LICENSE/LICENCE, separate docs directory, binary/media assets, symlinks or submodules. None were silently excluded.

| Comparison to all 29 main paths | Equal | Changed | Missing | Extra paths absent from main |
|---|---:|---:|---:|---:|
| Original root | 10 | 13 | 6 | 63 |
| Frozen R4 start | 10 | 13 | 6 | 69 |
| Current integration | 6 | 21 | 2 | 84 |

For the accepted current-coverage classification, the six equal paths are `Makefile`, `typescript/src/lib/duration.ts`, `typescript/src/lib/effect-params.ts`, `typescript/src/lib/render-bounds.ts`, `typescript/src/lib/tracks.ts`, and `typescript/src/lib/trim.ts`. The 21 changed paths are intentional, source-backed forward-port differences recorded below. The only two current absences are replaced tests, not unaccounted main content: `typescript/tests/scaffold.test.ts` and `typescript/tests/theme-api-smoke.ts`. The four-tree union remains 157 unique paths, with 157/157 represented in the flat table and 84 current additions relative to main.

## Missing content: exact list and disposition

| Class | Main path absent in original root (also absent in frozen R4) | Actual current replacement / remaining gap |
|---|---|---|
| C1 | `.gitignore` | Restored by `6a3247d`; current ignores dependencies and generated/test output while tracking the lockfile. This is a later M0 repair, not root coverage. |
| G1 | `Makefile` | Restored by the approved `tl/vw-m4-restore-main-makefile` work and observed in current merge `024f69501`; its blob is byte-identical to main. `install`, `build`, and `test` delegate to npm, and `clean` removes `typescript/dist` and `node_modules` as main specifies. |
| G2 | `typescript/tests/scaffold.test.ts` | Retired by the accepted current-coverage decision. Its constant-equals-itself tag assertion is the PLAN literal-test cut. Its meaningful registry existence/symbol check is replaced by `scripts/gen-registry.test.mjs` (generation/check behavior) and `typescript/tests/registries.test.ts` (runtime registry dispatch), with the public package smoke in `scripts/smoke-package.mjs` referencing the registry exports. |
| G3 | `typescript/tests/theme-api-smoke.ts` | Retired by the accepted current-coverage decision. Its replacement names are the existing public-package consumer in `scripts/smoke-package.mjs`, `typescript/tests/theme.test.ts` for provider/runtime identity, and the strict source/declaration build. The 08:20 extension that adds explicit `useTheme`, `AnimationReferenceList`, `THEME_PACKAGE_CLIP_TYPES`, and `THEME_PACKAGE_REGISTRY` consumer references is on candidate `1ffb8d7` (runtime assertion follow-up `44e9de5`), **not current HEAD**; this report does not claim those candidate edits are merged. |
| G4 | `typescript/tsconfig.json` | Restored by `6a3247d`, then upgraded by `ed897544`: full strict source/declaration build, `noEmitOnError`, emitted declarations for the built package, and no host aliases. Current package scripts use this config honestly. |
| G4 | `typescript/tsconfig.test.json` | Restored by `6a3247d`; current compiles full source and `*.test.ts` to `typescript/test-dist`. The current test command uses the extensionless loader that exists in the current tree; no main path is silently omitted. |

The literal original-root condition still fails historically, and this report does not rewrite that fact. Under the explicitly accepted current-tree criterion, however, all 29 main paths are accounted for as equal, intentional, or replaced; the Makefile owner merge is present at current HEAD. This is a coverage readiness statement, not a claim that the history join already happened.

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

Results: clean worker tree; one integration root; counts and identities above; six original-root omissions / two current retired-test paths; Makefile blob equal to main. Per-file source diffs, original and replacement test/config bodies, and the cited change commits were inspected. TSV completeness/hash membership was independently checked against all four actual trees (157/157 rows, all 29 main paths represented; **PASS**). Current-vs-main classification is 6 equal, 21 intentional changes, and 2 replaced absences.

**No product tests were run:** this is a read-only tree/source audit, with no product/test edits. No full, browser, socket, build, install, merge, ref mutation, or claim of dynamic compatibility. Existing targeted results from the Makefile/API-smoke workers are not re-used as this audit's test evidence.

The lead may now perform the authorized history join outside this sandbox. Required lead commands (run on `/home/user/work/composition`, on `tl/integration`; this worker did not run them):

```sh
before_tree=$(git rev-parse HEAD^{tree})
git merge -s ours --allow-unrelated-histories 67b8aa3d0d6831d3e3504a340ff583c3da253707 \
  -m 'join history to upstream main 67b8aa3 (tree unchanged)'
after_tree=$(git rev-parse HEAD^{tree})
test "$before_tree" = "$after_tree"
test "$(git merge-base origin/main tl/integration)" = 67b8aa3d0d6831d3e3504a340ff583c3da253707
git merge --no-commit origin/main
test "$(git rev-parse HEAD^{tree})" = "$after_tree"
test -z "$(git status --porcelain)"
```

The `ours` join and its tree/merge-base/dry-run postconditions are intentionally not claimed until the lead observes them.
