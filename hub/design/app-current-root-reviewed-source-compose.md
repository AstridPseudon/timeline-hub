# Current App reviewed root source composition

Source preparation is complete on the required CURRENT integration base. This is a source candidate, **not current-release, browser, render, pixel/audio parity, or final-pair qualification**. PLAN.md was read first. No settled decision was changed; no source-task blocker remains.

## Exact composition

| Item | Exact identity |
| --- | --- |
| Worktree / branch | `/home/user/work/wt/app-m3-current-root-reviewed-source-compose` / `tl/app-m3-current-root-reviewed-source-compose` |
| CURRENT base | `7bb885b638838588a0dff81b64b7c34960ac07f3`; tree `065b46ac13026d3e3a1d760b44bab1ab8e1e930e` |
| Approved root/label delta | `667498cc49b4ec2b1ccd3a515eb87311c5126c93` → `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c` |
| Approved residual alias delta | `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c` → `a69b65955d130fd8bce2feecf0711532ff4fae62` |
| Alias source tree | `a5edae0836143d07b93ca9c890e1f2dcf2460c15` |
| Final candidate tree | **`99f031ca5eccb646d038de764d417cfeea510ad0`** |
| Refreshed MAIN reference | `origin/main` = `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa` at audit time |

Both approved binary patches were checked and applied with `git apply --check` / `git apply` to the working tree. No commit, merge, checkout, rebase, push or ref mutation was performed. The harness supplies the eventual commit. Candidate tree identity was computed with Git's blob/tree encoding in Python without writing Git objects or an index; the encoder was cross-checked against the existing alias ref's tree.

**Exact final equation:** the complete `a69b659` source tree plus only the two CURRENT `7bb885b6` CORS blobs. Every working source blob and mode matches this equation, including additions/deletions. Relative to CURRENT: **169 paths; +6,034 / −4,165 text lines (net +1,869)**, plus the 58,444-byte public12 binary. Exact newline-delimited [allowlist](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/allowlist.txt), SHA-256 `d600c38b4f48becfc52a58b047546ef9a1554b0e944eb8245b41cafa0415142b`. Reproduction patches: [root/label](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/root-label.patch), [aliases](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/aliases.patch).

Changed authored `src/` product only, excluding tests, fixtures, generated contracts and vendor: **27 paths; 15,096 → 15,916 lines; +1,025 / −205; net +820**. This is a changed-path census, not the full Timeline-core size. The residual-alias delta remains exactly seven files, +13 / −120, net −107.

## Preserved boundaries and decisions

- **28 protected MAIN files** and **both CURRENT CORS files** are byte-identical to `7bb885b6`. The full path lists are in [audit.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/audit.json): provider/boot/digest/own-key lookup, auth/App root, canonical URL/bootstrap CAS, chat/proxy, render/admission/download, one mobile portal/lifecycle, raw ShotEditor/settings, save barrier and Runtime client. No old `320784` download cohort or Native None/PARAM/delete/split/trim/auto/requester/proxy/import-wiretypes cohort was composed.
- Initial verified projection, generation/disposal fences, root serializer/opaque settings/history safety, native parent-label capture, original guards and after-ACK scheduling remain the reviewed approved source. No whole-document fallback was introduced.
- **Owner 11:08 HOLD is preserved.** `canonicalCompositionState.ts` and `useTimelineCommandSession.ts` still call the current default-clamped projector. No transient renderConfig field, projector/default/renderer fade-clock change or new timing policy was added. The five-second source / four-second cap MAIN-source prediction remains **0.5 at frame 105/30fps** pending real MAIN pixels. The existing RAW-input renderer unit remains byte-equal to the approved source; its manually supplied raw input is a conditional compiler contract, not evidence that production supplies raw timing. No external opacity-1 RED was promoted into product behavior.
- **Label fixes are retained together:** untouched focus follows Remote after blur; typed `Original → Temporary → Original` stays explicit intent, uses the original capture/callback and retains refusal/draft state after remote changes/refocus. Existing empty-label, guard and recovery behavior remains. Prior independent 202/210 evidence is not recounted as a new run here; this run includes the current row/canvas/session/capture tests.
- **Mobile supersession is explicit:** the eight unmerged phone/tablet capture requirements are superseded by the owner’s MAIN mobile overhaul `44f0b9ca9`, as mapped in [app-root-main-mobile-test-supersession.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-root-main-mobile-test-supersession.md). They are not claimed passing. Desktop capture positives and phone/tablet Agent-selection/no-capture positives remain. Only the **three original drag markers** remain; no new expected failure, skip, disabled assertion or refusal rewrite was introduced.
- Gate 5 AST comparison against `04346844f^` preserves **all 6 migrated case bodies and all 21 helper bodies exactly**, adding one case and one helper. This reference is the approved migrated journey, not the older pre-migration writer assertions. MAIN row/canvas original assertions are preserved. All **64 surviving changed TS/TSX files parse**; parsing is not a project typecheck.

## Public package and future pin seam

Composition is the same immutable **0.0.12**, **58,444 bytes**, **77 regular files**, SHA-256 **`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`**. All 77 private installed files equal the archive. The **entire actual public DEFAULT_THEME object** equals Agent `BUILTIN_DEFAULT_THEME` read from `/home/user/peteromallet/astrid-agent/astrid/core/theme/_schema.py`; explicit styles remain covered. This is source equality, not a qualified Agent package tuple.

The reviewed root/package/lock/vendor cut and alias cleanup are exact. Seven Vite configurations resolve public exports and shared peers, including embed; Node SSR imports public theme/registry. Retired embed theme/registry stubs, private Composition source probes, fake-runtime animation binding and complete_task retired vendor bindings are absent. The retained embed demo's unrelated workspace effect/animation aliases were left as approved. No broader repository-wide fallback deletion claim is made.

The affected Runtime **DEVELOPMENT-ONLY 0.2.9** normal pin is preserved exactly from `85efd`: source **`94114269d1ce23ab3224d7eca5a85138ce2b5fed`**, producer version **`sha256:e02a71b5b77479bdc8035a8a8d75ec57e9f1962b7f9195126739ab0d1ed063ac`**. `runtime.lock.json` and all **13 locked files** equal the recorded normal producer's bytes and hashes at `/home/user/work/wt/app-m3-runtime029-producer-source`; only the approved lock plus three generated TypeScript paths differ from CURRENT. No generator, ad-hoc staging 011/012/013 or hand-generated contract edit was performed.

For the imminent safe pin, retain the existing normal seam only: once Runtime publishes its safe producer and the matching Agent pin is ready, use `node scripts/vendor-lock.mjs update runtime.lock.json --producer <absolute-safe-published-runtime-source>` and its `check` counterpart. Do not substitute the development-only source for that prerequisite. The current normal artifact destinations are enumerated exactly in [future-pin-allowlist.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/future-pin-allowlist.txt) (**lock + 13 producer-owned destinations**); actual new published manifest changes require owner review rather than guessed edits. Then freeze the exact Runtime/Agent/public12/App tuple before the manager's reserved single project typecheck and qualification. This task deliberately supplies source/allowlist readiness, not a purported safe pin.

## Commands and evidence

Commands ran from the assigned worktree. `N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes`. The private runner config imports the repository config, supplies its legacy `__dirname`, and confines cacheDir to `N`. The complete 59-file selection is [test-files.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/test-files.txt).

```sh
node node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 $(cat "$N/test-files.txt")
node --test --test-reporter=spec config/vite/timelineCompositionPackage.test.mjs
node config/vite/timelineCompositionPackage.test.mjs
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime029-producer-source
node scripts/quality/check-known-failures.mjs
python "$N/audit.py"
node "$N/ast-audit.cjs"
node node_modules/eslint/bin/eslint.js --no-cache $(cat "$N/lint-files.txt")
git show HEAD:src/tools/video-editor/components/TimelineEditor/TimelineEditorCoreBody.tsx | node node_modules/eslint/bin/eslint.js --no-cache --stdin --stdin-filename src/tools/video-editor/components/TimelineEditor/TimelineEditorCoreBody.tsx
node --check tests/e2e/fake-runtime/launch.mjs
node --input-type=module -e "import fs from 'node:fs'; for (const p of ['tests/e2e/fake-runtime/tsconfig.json','supabase/functions/complete_task/deno.json']) JSON.parse(fs.readFileSync(p,'utf8'));"
rg -n 'stubs/timeline-composition|typescript/src/(theme-api|registry.generated)' examples/embed-demo
rg -n '@workspace-animations' tests/e2e/fake-runtime
rg -n 'vendor/(timeline-composition|timeline-theme-2rp)' supabase/functions/complete_task
git diff --check
```

| Evidence | Exact result |
| --- | --- |
| **One broad necessary scoped Vitest run** | **Exit 0; 59 files / 1,571 tests passed; 151.63s**. Root, label, initial projection, source guards/public package consumers, raw settings/root serializer, outbox/history and generation cases; includes CURRENT CORS. No retries or second broad run. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/vitest.log). |
| Package/SSR guard | Exit 0; direct execution **9/9 checks pass**. `node --test` also passes its one outer-file wrapper. [Direct log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/package-guard-direct.log). No build/server/render. |
| Normal existing Runtime pin check | Exit 0; exact affected development producer matches. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/runtime-check.log). |
| Failure-marker guard | Exit 0; **3 authorized original drag markers, 0 forbidden**. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/known-failures.log). |
| Whole-tree, artifact, actual theme and 13-file pin audit | Exit 0. [JSON](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/audit.json), [script](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/audit.py). |
| AST preservation and syntax audit | Exit 0; **6/21 old members preserved**, 1/1 added, original MAIN row/canvas assertions preserved, 64 TS/TSX files parse. [JSON](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/ast-audit.json). Initial checker assumed the row file was append-only; corrected the checker to account for the approved additive phone/tablet cases. Product/tests were unchanged. |
| Scoped product ESLint | Exit 1; **one baseline** `react-hooks/exhaustive-deps` unnecessary `deviceClass` dependency in `TimelineEditorCoreBody.tsx:826`. Exact CURRENT HEAD stdin reproduces the same sole error at line 824. Left unchanged. [Candidate](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/eslint.log), [base](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/eslint-base.log). |
| Launch syntax / two JSON parses | Exit 0. |
| Three precise residual searches | No matches (expected rg exit 1); [results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/residual-check.json). A preliminary overbroad search also found the approved unrelated embed animation alias; it is outside the retired binding scope. |
| Whitespace check | Exit 0. |
| Shared dependencies/cache preservation | Before/final inventory identical: **35,616 entries** in `/home/user/work/app/node_modules`, **35,464** in `/tmp/app-coherent-deps12/node_modules`; compared path, mode, size, mtime_ns and symlink target. [Result](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current-root-reviewed-source-compose/notes/shared-deps-audit.json). |

Private public12 was extracted only under this worker's `notes/private12/node_modules`; retained packages/peers link read-only to the existing coherent dependencies. Only this worktree's ignored node_modules link was repointed. No shared dependency, shared cache, runtime or venv was modified. Private Vite caches were removed; no worktree build output or temporary source artifacts remain.

## Remaining gates / next steps

1. **Viewing golden remains OPEN:** obtain real decoded MAIN pixels against this exact candidate before revisiting opacity 1/renderConfig. Keep the existing clamp until that evidence supports an owner decision. Required final frame/audio parity and planted mismatches, and the settled owner-film theme/element-look/fade-curve disclosures, remain with Viewing; unit/public RAW tests do not close them.
2. **Safe final tuple remains OPEN:** Runtime publishes the corrected producer, Agent adopts the matching normal pin, then App uses its normal vendor-lock update/check. Freeze exact tuple and run the manager-reserved single project typecheck. The development-only 941 pin is not release authority.
3. **Current-pair qualification remains OPEN:** separately authorized real Runtime acceptance/retry/restart/undo, Gate 5 browser journey, current mobile one-portal behavior, render/admission/download and actual final media evidence. MAIN protected bytes and scoped unit tests do not replace these gates.

No full suite was requested, no full/build/browser/socket/install/project-tsc was run, and no current-release or actual render acceptance is claimed. Current-base historical `full25523` / 18,506-pass evidence is inherited context only and was not rerun or presented as candidate qualification. No tests were skipped, disabled, weakened or rewritten to encode lost behavior.

`commit-msg`, worker `report.md`, and `DONE` are supplied. `KEEP` retains this candidate/private12 overlay **only for the imminent normal safe pin and final-tuple qualifier**; it is not general retention or merge/release approval. Recycle normally once those consumers release the lease.
