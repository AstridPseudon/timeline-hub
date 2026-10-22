# Timeline foundation (M0–M4): the 90:10 plan and scope of work

*Written 2026-10-22 while the project is paused. Research was read-only:*
- *Haiku research agents read the integration heads (Agent a086cc6db, App c85da5427, Runtime cc7410a1f, Composition 6c4d93421).*
- *The Agent and Viewing leads answered questions.*
- *I measured upstream drift today in scratch clones. No work repo, worker or Codex was touched.*
- *Line numbers refer to those heads, and will shift after the upstream merge (WP1).*

> **Read §16 first.** Two independent reviews ran on 22 Oct: Astra on over-engineering and scope creep, and Opus on speed and strategy. §16 lists the changes they led to. Where §16 conflicts with an earlier section, §16 wins. A clean v2 of this plan will be written once the owner settles the §16 decisions.

---

## 0. The short version

**Goal.** A delivery ZIP that applies cleanly to today's upstream main, in which:
- every everyday edit, in App and Agent, is saved as Runtime edit commands through one route (`POST …/commit`);
- the old whole-document save routes are deleted or refused;
- preview and export are shown to agree;
- a live browser suite proves the above by using the product. That means real drags and keypresses, watching the commits land, reading them back through the Agent CLI, reloading, undoing and restarting.

**What's left, in 12 work packages:**

| WP | What | Size (worker-hours) | Depends on |
|---|---|---|---|
| WP0 | Restart on the 90:10 operating model | 2–3 h orchestrator | owner go |
| WP1 | **Merge upstream main** into all three repos (now large; see §2) | 6–10 | WP0 |
| WP2 | One Runtime and one Composition pin, taken from the integration heads | 2–3 | WP1 |
| WP3 | Command vocabulary: track-targeted moves, transition values, content digest | 5–8 | WP1 |
| WP4 | App: everyday gestures go native; delete the old save funnel | 18–26 | WP3 (drags, transitions) |
| WP5 | Generic route with exact replay (App and Agent) | 4–6 | WP1 |
| WP6 | Agent: remaining whole-document writers | 12–18 | WP3, WP5 |
| WP7 | Runtime: refuse or delete the old routes, plus the one-writer proof | 4–6 | WP4, WP6 consumers gone |
| WP8 | Viewing rows plus the cheap gate 6 | 6–10 | WP2 |
| WP9 | **Live browser suite**, and a watcher for your own live sessions | 8–12 to build | WP1 (harness merge) |
| WP10 | Ledger close-out, main re-baseline, full suites on the farm | 3–4 | WP4–WP8 |
| WP11 | Final upstream refresh, gate 7, ZIP, your film viewing | 3–5 | all |

**Estimate.** About 2–2.5 days of wall-clock at the throughput we had before the pause, run in four parallel lanes (App, Agent, Runtime/Viewing, farm).
- The critical path is WP0 → WP1 → WP3 → WP4 drags and transitions → WP7 → WP11.
- My earlier 90:10 estimate was 1–1.5 days. It was too low for two reasons:
  - since the last fetch on 21 Oct, about 250 new upstream commits have landed (we are now 287 behind in total), which makes WP1 real work;
  - this inventory found that the refused drags and transition SET need new command shapes (WP3), not just rewiring.

**Three corrections to my earlier 90:10 answer**
1. **The upstream merge is substantial** (you were right). It was 3 conflicted files at the last fetch (21 Oct). It is **84 conflicted files today**, plus a Runtime database version clash (§2).
2. **Gate 6 cannot be "identical input, checked by hash".**
   - The App preview and the Agent export get differently shaped inputs.
   - The App preview's visual layer is a *hand-port* of the shared Composition component, not a call into it (`TimelineRenderer.tsx:74`).
   - The cheap equivalent compares the outputs of the shared *evaluator* at fixed frames instead (WP8).
3. **Four drag gestures are refused, not three.** Single-clip cross-track drag is refused too (`semanticGestures.ts:78`). That makes four gestures that work on main and fail on integration (WP4, G2).

---

## 1. Ground rules (the 90:10 operating model)

These apply to every work package. They are SYNTHESIS.md A–E, and need your yes (§9, decision 1).

- **No internal releases.** Agent and App consume Runtime and Composition straight from the integration heads (WP2). There is one real release at M4.
- **Work by slice, across repos.**
  - Each work item is "delete one named old writer". The Runtime op, the App or Agent caller, and its tests change together in one merge.
  - app2 folds into App.
- **Lighter interim proofs** (already your decision):
  - per merge: one review, targeted tests, typecheck and lint;
  - full suites and the live suite only at the 00/06/12/18Z checkpoints and the final gates, run on the test farm.
- **Freeze the precedents.** No new standing rules. Managers decide locally.
- **"Done" for a writer row** has three parts:
  - its non-test call sites are gone (a grep guard proves it);
  - the replacing command path has a targeted test;
  - the matching live scenario in WP9 shows zero old-route requests.

---

## 2. The upstream merge is now large (measured today)

Method: bare scratch clones that share the work repos' objects. Upstream `main` fetched at about 18:30Z. `git merge-tree` previewed our integration head against it. Raw output: `/tmp/claude-0/-home-user/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/drift2/`.

| repo | upstream commits we lack (21 Oct → today) | upstream churn since merge base | conflicted files (21 Oct → today) |
|---|---|---|---|
| Agent | 11 → **93** | 166 files, +18.6k / −1.5k | 1 → **13** (all content) |
| App | 22 → **189** | 2,935 files, +32k / **−223k** | 2 → **55** (38 content, 17 modify/delete) |
| Runtime | 0 → **5** | 36 files, +720 / −49 | 0 → **16** (all content) |
| Composition | 0 | — | 0 |

**What upstream did, and why each item matters to us:**

1. **Runtime added actor-owned app state** (`GET/PUT /v1/app-state/user/{key}`). This is **schema v31**.
   - Our timeline-commit tables are *also* schema v31 (`upgrade.py:75 TIMELINE_COMMIT_TARGET_SCHEMA_VERSION = 31`, against upstream `USER_APP_STATE_TARGET_SCHEMA_VERSION = 31`). That is a real clash.
   - Ours must become **v32** and upgrade from upstream's v31.
   - Realms created by our integration builds are dev and test data only. They are recreated, not migrated (§9, decision 3).
   - The contract files regenerate, which changes the schema digest, which in turn changes every consumer's Runtime lock. So Runtime merges first.
2. **App removed the cloud product** (about −223k lines: supabase functions and migrations, dev extensions, edge configs) and added the first-run tour.
   - The 17 modify/delete conflicts are files we touched that upstream deleted, such as `supabase/functions/complete_task/*`, `dev/scene-phase-markers/*` and `vitest.edge.*`. Default: **accept upstream's deletion**, unless our change carried a writer migration; then port that change to wherever the code now lives.
   - Two run the other way: `lib/compiler-canary.ts` and its test are deleted on our side but modified upstream. We keep our deletion and check what upstream's change was for.
3. **Upstream touched our writer files.** Our version wins structurally, but each upstream fix must be ported into the native path, not dropped:

   | File | Upstream change | Our change |
   |---|---|---|
   | `useTimelinePersistence.ts` | +23/−19 | +21/−6 |
   | `useTimelineCommandsService.ts` | +10/−10 | +170/−33 |
   | `useAssetManagement.ts` | +2/−89 | +49/−3 |
   | `dataProvider.ts` | +52/−13 | +591/−35 |
   | `ShotEditorView.tsx` | +30/−48 | +229/−31 |

   Upstream fixes to port:
   - "keep unknown asset-registry fields on save and parser merge" (313804005a);
   - "keep Astrid handle/source/pixel_provenance on registry entries" (cb98e249b9);
   - "one effective clip volume" (80cfa60312);
   - "imported media is written as a Runtime object route" (773bb7b14a).
4. **Upstream built its own live journey ("QUICK tier")**, in both Agent and App:
   - Astrid edits through the CLI, and the open App picks the edit up through its head poll;
   - the door port is chosen up front, so suites no longer fight over 17340.

   It conflicts with our `tests/e2e/local/support/{harness,app,astrid}.ts` and `three-products.spec.ts`: upstream changed harness.ts by +243 lines and three-products.spec.ts by +427, against our +437 and +1,901. This is good news for WP9, which builds on the merged harness rather than a second one.
5. **Agent:** our WC7 writer files conflict (`sdk/timeline/publish.py`, `sdk/timeline/edits.py`). So do `onscreen.py`, the vendored Runtime client and `runtime.lock.json`, plus the World Explorer/Lantern Valley rendering work.
   - App's `vendor/astrid-browser/` mirrors Agent's `astrid/`, so it is re-vendored from the *merged* Agent with the vendoring tool, never by hand.

**Strategy: merge, don't rebase.**
- The delivery is already a single squashed patch per repo on top of origin/main (`delivery-build`). Rebasing more than 500 commits per repo would cost hours and buy nothing.
- Merging main into `tl/integration` keeps every hub checkout valid.

**The drift will keep growing.** Upstream has been running at roughly 100+ commits a day in App and 50+ in Agent. Plan for:
- a merge at restart (WP1);
- a small merge at each 12-hourly checkpoint;
- the final refresh (WP11).

Upstream is authored by AstridPseudon and its Claude sessions. If those are yours, the cheapest lever is to keep upstream work off the editor's save path files until we land (§9, decision 2).

---

## 3. Work packages

Each work package lists: what changes (with file:line at the paused heads), the ledger rows it closes, its acceptance criteria and its live scenarios (the IDs refer to §4).

### WP0 — Restart on the new model (orchestrator, 2–3 h)
1. Write your chosen SYNTHESIS changes into MANAGER-COMMON, PLAN and the lead work lists *before* any manager starts. Freeze the precedents.
2. Restart main's hub-syncd, and on the farm do the Codex sign-in (you'll get a device code) and start its dispatcher.
3. Close or reassign the interrupted workers listed in RESUME.md. Most are superseded by this plan; continue only:
   - Runtime's rt08 fixture;
   - Agent's a086cc6db follow-ups.
4. Fold app2's queue into App.

**Accept when** every lead's work list names only WP items, and the farm has passed one hello worker.

### WP1 — Merge upstream main (6–10 h; Runtime → Agent → App, in that order)
1. **Runtime** (16 conflicts):
   - merge;
   - renumber our commit tables to schema v32, with an upgrade path from upstream's v31 (app state) and a test that opens a v31 upstream realm and upgrades it;
   - regenerate the contract with the repo's generator, never by hand: `contract/artifacts.json`, `manifest.json`, `contract_metadata.py` and the generated Python and TS clients;
   - keep upstream's asset-identity changes (1462b9e24, 4563bb5ff).
2. **Agent** (13 conflicts):
   - merge;
   - re-vendor the Runtime client from the merged Runtime (`scripts/vendor_lock.py update runtime.lock.json --producer …`);
   - resolve `publish.py` and `edits.py`, keeping upstream's behaviour changes ("say when a reused working copy is behind the head", "parent clips stay one list", "find clips on the parent composition") inside our native paths;
   - regenerate `artifacts.json` with its tool.
3. **App** (55 conflicts):
   - merge;
   - take upstream's deletions (see §2);
   - port the four upstream fixes into the native path;
   - merge the e2e harness with upstream's QUICK tier;
   - re-vendor the Runtime client (`node scripts/sync-runtime-client.mjs …`) and astrid-browser from the merged Agent; `provenance.json` is regenerated by the tool.
4. **Audit upstream for new old-route callers.** Grep the merged trees for every old-writer symbol (saveTimeline*, publishParentComposition, composition-revisions POST, publish_bundle, replace_parent_media, publish_timeline_render). Every new upstream caller becomes a row in the matching WP.
   - Upstream's app-state settings store is a **non-film** writer and stays (KEEP).

**Accept when:**
- `merge-tree` against the fetched main is clean;
- typecheck and lint are green in all repos;
- the targeted tests of every conflicted file pass;
- the Runtime upgrade test passes;
- the vendor-lock checks pass (`tests/test_vendor_lock.py`, `vendorLock.test.ts`);
- a farm full-suite run of **upstream main itself** has been recorded as the new baseline, replacing PLAN.md:267-269, because main has changed.

### WP2 — One pin per dependency, from the heads (2–3 h)
- **Runtime.** Both consumers point `runtime.lock.json` `source_commit` at the merged Runtime head.
  - Today the locked files are byte-identical at the head, so this is metadata-only.
  - After WP1 the generated files change, so it is a re-vendor.
- **Composition.** One artifact for both consumers:
  - pack the Composition head once (`make build && make test && npm pack`; smoke it with `npm run test:package -- <tgz>`);
  - name the tgz by commit, since every head package says 0.0.14;
  - Agent: `remotion/package.json:18`, `package-lock.json:425-426`, `_remotion_package.py:10`, `test_composition_package.py:20-21,40,43-45,52`;
  - App, which moves 0.0.13 → head: `package.json:124`, `package-lock.json:210-213`, `config/vite/timelineCompositionPackage.test.mjs:25-54`.
- Fix the stale pin tests (`test_am_snap_plate_scene_capability.py:38-40`, `test_d09_managed_scene_only.py:110-111`) and delete the tgz files nothing references.
- **Known gap, for the release.** Upstream CI checks producers out by SHA (`agent ci.yml:224-226`, `app test.yml:36-40`), and our heads exist only on the hub. At M4 the release step (yours) pushes or tags the producers, then repoints the pins at those tags. Until then CI on a hub-only SHA is expected to fail. The farm results stand in for it.

**Accept when** both consumers report the same Composition sha512 and the same Runtime source_commit, and every guard test listed in pins.md §5 passes.

### WP3 — Command vocabulary (Runtime, one contract change; 5–8 h)
The App's refused gestures and transition SET cannot be expressed today:
- `ClipMoveArgs` has only `on`, with no target track (edit-command.json:438);
- `ClipSetArgs` values allow only `{hold}` (:2095).

One additive contract change. Each part is implemented in the Python executor **and** the App's TS twin, with shared conformance cases:

| Change | Shape | Unblocks |
|---|---|---|
| Track-targeted move | `clip.move {on, track?}`. Without `track` the clip stays on its own track. The target must exist and be the same kind. | single cross-track drag; group drag across tracks |
| New track in the same commit | `track.create` followed by `clip.move {track}` in **one** commit. No new op; the commit is atomic. | drop onto a new track |
| Multi-clip and group moves | N `clip.move` commands in one commit. Pinned-group membership is checked by the executor. | multi-select drag; pinned-group drag |
| Transition values | `clip.set {values: {transition: {kind, duration_s, …}}}`. This is the approved 0.2.18 carrier. | transition SET; bulk reset |
| `Document.content_digest` | a derived, additive field on read (already approved) | the undo-equals-before checks in WP9 |

**Accept when:**
- the schema, executor and TS twin are updated;
- the conformance cases pass on both sides: each op, refusal of a wrong-kind or missing track, a group with an outside member, and transition round-trip including clear;
- the Agent's `document_diff` and the App's generic adapter accept the new shapes.

### WP4 — App: everyday gestures go native, then the old funnel is deleted (18–26 h; App lead, about 3 lanes)
Today every un-migrated gesture goes `applyEdit` → `useTimelineCommit.ts:410 scheduleSave` → `useTimelinePersistence.ts:403-407` → `dataProvider.saveTimelineAtHead/saveTimeline/saveTimelineInOrder` (`dataProvider.ts:1000/1014/1030`) → `POST …/composition-revisions`.

| # | Gesture | Today | Change | Rows | Live |
|---|---|---|---|---|---|
| G1 | Split (S key, menu, split here) | legacy `useClipEditing.ts:115,119` | `clip.split {on, right_id}` through the outbox | D01-app-split | L01–L02 |
| G2 | Drags: single cross-track, multi-select, to a new track, pinned group across tracks or to a new track | **refused**: `semanticGestures.ts:78`, `useClipDrag.helpers.ts:333,336` | WP3 shapes. The three `it.fails` tests (`useClipDrag.test.tsx:774,1120,1230`) become ordinary passing tests. | D01-app-original-three-drag | L04–L08 |
| G3 | Edge-drag trim | legacy `useClipResize.ts:330,364` | `clip.trim` (source-window trim is already native) | D01 trim | L09–L10 |
| G4 | Delete: keyboard and non-parent | legacy `TimelineEditorShellCore.tsx:340`, `useClipDeletion.ts:61` | `clip.delete` | D01 delete | L12–L13 |
| G5 | Transition SET and bulk reset | legacy `useClipEditing.ts:288` and `:209` | `clip.set {transition}` (WP3) | D01 transition | L14, L16 |
| G6 | Image drop | legacy `useAssetManagement.ts:326` | the same prepared-media command as video, submitted natively | D01-app-parent-media | L17 |
| G7 | Video add after a clip, and drop-replace | **refused** `useTimelineCommandsService.ts:482-492` | allow `afterClipId` and `removeClipId` as add plus delete in one commit | D01-app-parent-media | L19–L20 |
| G8 | Popup ADD | native port with no UI caller (`commitSession.ts:577`); legacy popup writer `shotTimelineDataProvider.ts:510` | wire the dialog to `occurrenceAddMedia`, then delete the popup writer | D01-app-popup-add, D01a | L21 |
| G9 | Popup SWAP | dormant (`VideoEditorProvider.tsx:771`) | activate the consumer | D01-app-popup-swap | L22 |
| G10 | Ordinary batch (`useTimelineOps.ts:290/318`) | snapshot fallback | generic route with exact replay (WP5); unrepresentable batches are refused visibly with the draft kept | D01-app-ordinary-batch | L25, X05 |
| G11 | Element routes (`element-adapter.ts:101,104`) | save/CAS | `clip.set-params` / `clip.set-element` | D01-app-element-routes | L25 |
| G12 | Placement service (`placementService.ts:106`) | CAS write | `placement.*` commands | D01-app-placement, D01b | L23 |
| G13 | Bootstrap headless repair | publish | `timeline.init` | D01-app-bootstrap | R05 |
| G14 | Shot name and settings, gallery/list writers | snapshot | `shot.set` (the only row with a clean fit today) | D01-app-shot-graph-settings | L26 |
| G15 | Shot-composition publish port (`dataProvider.ts:295`, from `shotCompositionAdapter.ts:319-338`, `ShotEditorView.tsx:251`) | composition POST | commit | D01 | L26 |
| G16 | `registerAsset` (`dataProvider.ts:1275`) | saveTimelineInOrder | a native asset command, or no film write at all (registry only) | D01 | L17 |
| G17 | Snapshot rollback and history | local | Runtime history undo/redo | D02 | every L (undo step) |

Then **delete the funnel**:
- `scheduleSave`'s save branch, `saveTimeline*` (`dataProvider.ts:1000-1131`) and `browser-runtime.ts:113`;
- the `publishParentComposition` wrapper (`client.ts:722-728`);
- the unused facades (`commands.splitClip/trimClip/deleteClip/setClipParams`, which have no UI callers).

**Accept when:**
- a guard test fails on any non-test reference to these symbols;
- the selected-PARAM refusal text and retained schema behaviour are unchanged;
- every listed live scenario shows 0 old-route requests.

### WP5 — Generic route with exact replay (4–6 h)
- **App** `genericPatchCapture.ts`:
  - after capture, build the document the old path *would* have saved;
  - replay the captured commands onto the base;
  - require canonical equality, otherwise throw `GenericPatchRefusal` (keep the draft, show a toast);
  - today this equality is only asserted in tests (`genericPatchCapture.test.ts:71`);
  - also emit `shot.set` and `clip.set-params` so G10, G11 and G14 fit.
- **Agent** `document_diff.py`: before `return` (about :480), add `canonical(working) == canonical(candidate)` over the same projection, otherwise raise `DocumentDiffError`. That is 20–40 lines (the Agent lead's estimate).
- **Tests:**
  - one round-trip per field class (parent, shot clips, registry, payload, config);
  - null vs absent for `hold`;
  - a planted unrepresentable field, which must be refused with the candidate untouched;
  - the same planted case through the App toast path.

**Accept when** all of these pass, and live X05 shows the refusal visibly with the draft kept.

### WP6 — Agent: the remaining whole-document writers (12–18 h; Agent lead)

| Row | Writer | Change |
|---|---|---|
| WC1 | `authoring_bundle.py publish_authoring_candidate` (about :1620) | through `document_diff` (WP5); fields outside it are refused |
| WC3 | `remote.py replace_parent_media` (:1278-1503 → composition POST at :1406-1420) | native media-replace via `native_parent_media_commands.py` (exists); keep the original success semantics (`tests/test_timeline_clip_replacement.py`) |
| WC5 | `draft_voiceover.py:475` | `text-binding.set` plus the verified text descriptor |
| AG-M2-TB01 | `remote.py:2446,2456`, `publish.py:173`, `timeline_document.py:179`, `shots/cli.py:135` | `text-binding.set` route (the spike test exists) |
| WC7, AG02 | `store.py:257/305-352 publish_bundle` ← `publish.py:44` ← `tl publish` (`cli.py:2983`) | attached cases are already native. **90:10 proposal:** detached and mixed working copies are *refused* with a clear message ("re-checkout attached") instead of migrated (§9, decision 4). |
| WC8 | `store.py three_way/_merge`, `checkout.py:203`, `cli.py:2808` | server-side rebase of retained commands; occurrence source-window semantics come from Runtime (the gap Runtime already sent) |
| AG03 | `timeline_sheet.py` local undo (`_history_dir`) | `timelines undo/redo` (Runtime history) |
| AG-MAT-V01..03 | unsafe new v1 submissions | refuse; qualify the equivalent v2 path |
| create_empty | `remote.py:483-537` (used by `cli.py:186`, `timeline_duplicate.py:194`) | `timeline.init` |
| D13 assembler | render publication (caller removed in 5be2918c4; startup hooks fixed in a086cc6db) | native render request → settled proposal → requester commits; send Runtime the final caller count |

**Accept when:**
- a grep guard shows no non-test caller of `publish_bundle`, `publish_authoring_candidate`, `replace_parent_media → composition POST` or `create_empty → composition POST`;
- each replacement has its targeted test;
- live X01, X02, X05 and X06 pass.

### WP7 — Runtime: delete the old routes, prove one writer (4–6 h; after the WP4 and WP6 consumers are gone)
- **Composition-revisions POST** (`service.py:2779`): remove the headless branch (:2818), so every timeline is refused with 409 `timeline_commit_required`. Rows D04 and WC10. Then delete the body once no consumer remains.
- **publish-timeline-render** (`service.py:7534`, raw SQL at :7641): refuse after D13 migrates (RT07). Close the raw-SQL bypass of the documents guard (`:4430-4434`).
- **Already refused, keep:** timeline-documents, replace-clip, PATCH timeline, replace-parent-media, shot/reference writes.
- **Non-film metadata, keep** and list in `owner-film-differences.md` (§9, decision 5): rename (`service.py:1677`), shell create (`:1698`), archive and recover (`:4071/4111`).
- **RT08:** finish allocation and source-owner joins. **D13 admission:** consumer fencing qualification.
- **The one-writer test** extends `tests/test_timeline_legacy_authority.py` and `test_timeline_authority_door.py` into one test over a tracked timeline with one accepted commit:
  - send every old route twice, with a fresh key and with the accepted key;
  - replay and event appends are patched to fail;
  - expect 410 `retired_route`, or 409 `timeline_commit_required` for composition and render;
  - the DB snapshot is unchanged (iterdump plus CAS bytes plus total_changes);
  - door `classify()` returns None;
  - positive control: a valid `/commit` advances the version.

**Accept when** that test passes and live W01 passes.

### WP8 — Viewing rows and a cheap gate 6 (6–10 h; Viewing lead)
- **Rows:**
  - D08a: the initial preview consumes the verified compiled projection, including cold open;
  - D08b: continuous PCM policy;
  - D09: drop the private visibility and timing math and use the Composition evaluator;
  - VW-D09a: the `mouth_state` fallback uses the shared timing;
  - VW-D09-LEGACY-FADE: element-fade qualification;
  - VW-AUDIO-STEP: same-tuple positives and planted negatives.
- **Staging fix first** (Viewing lead): 3 missing SceneSurface files plus a closure witness. This is what stopped the last physical run at 10%.
- **Theme:** make the preview's compiled-transitions scene use the output theme. It uses the default today (`playerEvaluation.ts:84` vs `:61`). Check that App and Agent resolve `theme.visual` the same way.
- **Cheap gate 6** (a unit or integration test, no browser):
  - for each frame in `PARITY_FRAMES` [0,37,44,45,52,89,90,120,121,135,143,164], compare the App's `preparePlayerTrack` plan (`playerEvaluation.ts:69-136`) with the Agent's `host_frames_at` (`scene_answers.py:99`);
  - compare layer lists (clip id, drawStart, ownFrame, contentFrame, opacity), resolved transitions, the `theme.visual` hash, and the audio envelope key plus `audioEnvelopeAt` at fixed times;
  - **planted negatives**: shift one transition by 1 frame, change one fade curve, change one theme override; each must flip the digest.
- **One physical run** at the final checkpoint, on the farm: `player-export-frame-parity.spec.ts` cases `:278` (frames ≤2/255 on ≤0.1% of pixels), `:288` (audio with a ×0.5 planted negative) and `:328` (magenta planted negative).
- **Honest limit:** evaluator equality does not prove pixels, because the App's visual layer is still the hand-port. The physical run and your viewing cover that. Replacing the hand-port with the package component is deferred cleanup (§9, decision 7).

**Accept when** the cheap gate is green with all three negatives flipping, and the physical run passes once on the final tuple.

### WP9 — The live browser suite (8–12 h to build; then run at every checkpoint) — see §4

### WP10 — Close-out (3–4 h)
- Update the ledger: each REQUIRED row is DELETED with its evidence (commit plus test plus live scenario), or moved to `owner-film-differences.md` with your sign-off.
- Run full suites on the farm (Runtime, App, Agent) on one tuple. Pass means **no new failures against the WP1 main baseline**.
- Run the live suite (all scenarios) and the cheap gate 6 on the same tuple.

### WP11 — Final refresh and delivery (3–5 h)
1. Re-fetch upstream main, merge again (expect another day of drift; see §2), and re-run the WP1 audit.
2. Re-run the gates on the final tuple:
   - targeted tests, typecheck, lint;
   - full suites on the farm;
   - the live suite;
   - the cheap gate 6 and the single physical parity run.
3. Gate 7: `ORCH/bin/delivery-build`:
   - squash each repo onto origin/main, then `format-patch` plus a bundle;
   - in a fresh clone, `git am` the series;
   - the applied tree must equal both the bundle tree and `tl/integration`.

   Then fill in `gate-results.md` and build the ZIP.
4. **Your viewing:**
   - the ZIP's README gives exact steps: clone main, apply the patches, `npm ci`, then start Runtime, App and Agent with one command (the WP9 launcher);
   - open the sample film, make each everyday edit, watch the watcher print the commits, then render and play the export.

---

## 4. The live browser suite (WP9)

### 4.1 What it is
A Playwright suite that drives the **real** product: hosted App build, real Runtime with door, real Agent CLI.
- It runs on the farm, one worker, built on the merged e2e harness from WP1 (DirectHarness, AstridCli and upstream's QUICK tier).
- It lives at `playwright.live-timeline.config.ts` (extends three-products) plus `tests/e2e/local/live-timeline/*.spec.ts`, with one shared fixture, `tests/e2e/local/support/live.ts` (about 300 lines).
- It is not a one-off launcher; the "no new bespoke launchers" precedent still holds.

### 4.2 What it observes (the fixture `live.ts`)

| Observer | How | Gives |
|---|---|---|
| Commit recorder | `page.on('request'/'response')` on `/v1/projects/*/timelines/*/commit` | per commit: ops list, Idempotency-Key, status, returned revision |
| Old-route detector | the same, on `POST …/composition-revisions` (without `/restore`), `POST /v1/attempts/*/publish-timeline-render`, and `PATCH/POST …/documents/timeline:*`. Non-timeline document PATCHes (`dataProvider.ts:417,478`) are ignored. | count per step (must be 0) |
| Runtime head | `GET …/composition-revisions?limit=1` (is_current_head), `GET …/commits?limit=50` | head before and after, commit source and key |
| Document diff | `GET …/composition-revisions/{rev}`, canonicalised; structural diff of tracks, clips (at, from/to, track, transition, hold, params) and shots | exactly which fields changed |
| Agent read-back | `python -m astrid timelines show --published --json`, `history --json` | that the Agent sees the same head and fields |
| Door audit | the `--door-audit-log` JSONL since a marker | every browser request that reached Runtime |
| UI read-back | clip DOM boxes (data-clip-id → left and width → seconds at the current zoom) and track membership | what the screen shows |
| Evidence | Playwright trace plus video per scenario, and a JSON **journal** per step (action → commits → head → field diff → Agent view → UI view) | the record of *how* the timeline data updated; attached to the delivery |

### 4.3 The standard check for every gesture scenario
1. Seed fixture **F**: 2 video tracks, 1 audio track, 6 clips (one image, one with a transition, two in a pinned group), and 1 shot with a popup.
2. Record `H0` = head and `D0` = document.
3. **Do the gesture for real** (mouse drag with intermediate steps, the S key, Delete, panel controls).
4. Within 5 s:
   - exactly the expected commit POSTs (count and ops), status 2xx;
   - **0 old-route requests**.
5. The head moved to `H1`, and the top commit carries our key and the App source.
   - `diff(D0, D1)` equals **exactly** the intended fields.
   - Every other field is unchanged. This is the "no silent loss" check.
6. The UI matches `D1` to within one frame.
7. **The Agent agrees:** `show --published` reflects `D1`.
8. **Reload the page:** the UI still matches `D1`.
9. **Undo** (Cmd/Ctrl+Z): one commit, and `content_digest(D2) == content_digest(D0)`. **Redo:** `D3 == D1`.
10. On the tagged scenarios, **restart Runtime**: the head is unchanged, the App reconnects, and the UI still matches `D1`.

### 4.4 Scenarios
"Today" is what I expect from the code on the integration head. The first suite run (WP9 step 3) replaces it with measured fact.

**Gestures**

| ID | Scenario | Expected commands | Today |
|---|---|---|---|
| L01 | Split at playhead (S) | clip.split | old route |
| L02 | Split via context menu | clip.split | old route |
| L03 | Drag one clip along its track | clip.move | native ✓ |
| L04 | Drag one clip to another track | clip.move{track} | **refused** |
| L05 | Multi-select drag | N × clip.move | **refused** |
| L06 | Drag onto a new track | track.create + clip.move{track} | **refused** |
| L07 | Pinned group across tracks | N × clip.move{track} | **refused** |
| L08 | Pinned group onto a new track | track.create + N × clip.move | **refused** |
| L09–L10 | Edge-drag trim, left and right edge | clip.trim | old route |
| L11 | Source-window trim (panel) | clip.trim | native ✓ |
| L12 | Delete key | clip.delete | old route |
| L13 | Delete via menu (parent and non-parent) | clip.delete / clip.remove | mixed |
| L14 | Transition SET (type and duration) | clip.set{transition} | old route |
| L15 | Transition reset / remove | clip.set clear | native ✓ |
| L16 | Bulk transition reset | N × clip.set | old route |
| L17 | Image drop from the asset panel | prepared-media add | old route |
| L18 | Video drop | prepared-media add | native ✓ |
| L19 | Generation "add after" | add + order | **refused** |
| L20 | Drop-replace | add + delete | **refused** |
| L21 | Popup ADD | occurrence.add-media | old popup writer |
| L22 | Popup SWAP | occurrence.swap-media | dormant |
| L23 | Automatic image placement | placement.* | native ✓ |
| L24 | Selected PARAM edit | clip.set-params | native ✓ |
| L25 | Element params / ordinary batch | clip.set-params / generic | old route |
| L26 | Shot name and settings | shot.set | old route |
| L27 | Track label | track.set | native ✓ |
| L28 | Timeline rename | (metadata route; kept) | metadata |

**Live updates across tools (the "does the open App see it" checks)**

| ID | Scenario | Pass when |
|---|---|---|
| X01 | Agent edits while the App is open: `timelines edit move REF --clip parent/clip:ID --on S` | The App shows it **without reload** within the head-poll interval. The latency is measured and recorded; upstream's poll is now 30 s. The UI matches the Agent's `D1`. |
| X02 | App edit, then the Agent reads | `show --published` shows it at once; `history --json` lists the App source |
| X03 | Concurrent edits from the same base: App drags A, Agent moves B | both land (server rebase); the App shows both; nothing is lost |
| X04 | Conflicting edits to the same clip | one is accepted; the other is refused or rebased **visibly**; the App draft is kept; no silent overwrite |
| X05 | Agent document route (`timeline_document checkout → edit → check → publish`) with a field outside the native ops; then a planted unrepresentable field | the first goes through the generic route with exact replay; the second is refused with a message, and the candidate file is kept |
| X06 | `timelines undo` from the Agent | the App updates; the digest equals the pre-edit document |

**Resilience**

| ID | Scenario | Pass when |
|---|---|---|
| R01 | Lost acknowledgement: the server accepts but the browser never sees the reply (`route` aborts the response) | the App retries with the **same** Idempotency-Key; history shows exactly one new commit |
| R02 | Runtime killed in the middle of a gesture, then restarted | the App shows offline; the edit waits in the outbox and lands once; nothing doubles |
| R03 | Renderer off (no Remotion) | every gesture still saves |
| R04 | Two tabs on one timeline | both converge to the same head |
| R05 | New project and first open | bootstrap uses `timeline.init`; no old route |

**One writer, and viewing**

| ID | Scenario | Pass when |
|---|---|---|
| W01 | Direct HTTP to each old route on a tracked timeline (outside the browser) | 410 / 409, the DB snapshot is unchanged, and the door refuses |
| W02 | Whole suite | old-route requests total exactly **0** (checked once after all scenarios) |
| V01 | After L01–L27, the preview evaluator digest equals the export evaluator digest | it matches at PARITY_FRAMES |
| V02 | The player frame visibly changes after each commit | screenshot of the player before and after; they differ where expected and match elsewhere |
| V03 | Physical parity (final checkpoint only) | the WP8 physical run |

### 4.5 Order of building and running it
1. Build `live.ts` and the standard check. Use L03 (native) and L01 (old route) as the first two scenarios, to prove the detector sees both kinds.
2. Add all scenarios. Scenarios for not-yet-migrated gestures are expected to fail on "0 old-route requests" or "refused". That is the point: the suite is the **progress meter**.
3. **First run right after WP1**, on the farm. Its table, in the format of §4.4 with measured values, is the honest "how the timeline data updates today" answer you asked for. I'll send it to you.
4. Run it at every checkpoint after that. A WP4/WP6 item is closed only when its scenario is green.
5. **Regression rule:** a gesture that works on upstream main must not be refused on integration. Run L04–L08 on upstream main too, as a control.

### 4.6 Watching it yourself
`tests/e2e/local/support/live-watch.mjs` (about 100 lines, generic). It polls `…/commits` and prints one line per commit: time, source (App or Agent), ops, and the changed fields from the document diff.

Owner session, one command (it becomes the ZIP README's viewing step):

```
npm run live:session      # starts Runtime with door, the hosted App and an Agent identity;
                          # prints the App URL and starts live-watch in the same terminal
```

1. Open the URL and edit.
2. In a second terminal, the Agent can edit the same timeline: `python -m astrid timelines edit move …`.
3. Watch both kinds of edit appear in the watcher, and in the open editor.

---

## 5. Rows closed by this plan
All 39 REQUIRED rows from the 21 Oct triage are covered:

| Package | Rows |
|---|---|
| WP4 | D01, D01a, D01b, all D01-app-* REQUIRED, D02 |
| WP6 | AG02, AG03, AG-M2-TB01, AG-MAT-V01..03, WC1, WC3, WC5, WC7, WC8, D13 assembler |
| WP7 | D04, WC10 (both entries), RT07, RT08, D13 admission |
| WP8 | D08a, D08b, D09, VW-AUDIO-STEP, VW-D09a, VW-D09-LEGACY-FADE |

The 8 DEFERRED rows stay in `owner-film-differences.md`. The 17 KEEP rows are unchanged.

---

## 6. Order of work and parallel lanes

```
Day 1  AM  WP0 restart ─► WP1 Runtime merge ─► WP1 Agent merge ─► WP1 App merge
           (farm)  sign-in, main baseline        (Viewing) staging fix, theme fix
Day 1  PM  WP2 pins ─► WP3 vocabulary (Runtime)   WP5 exact replay (App+Agent)
           WP9 fixture + first live run (farm)    WP6 WC3/WC5/TB01/create_empty (Agent)
           WP4 G1 split, G3 trim, G4 delete, G6 image drop (App, needs no WP3)
Day 2      WP4 G2 drags, G5 transitions (after WP3) · G7–G17 · funnel delete
           WP6 WC1/WC7/WC8/AG03/D13 · WP8 rows + cheap gate 6
           checkpoint merge of upstream main (12Z)
Day 2–3    WP7 route cuts + one-writer test · WP10 close-out on farm
           WP11 final refresh · gates · ZIP · your viewing
```

**What moves the estimate most:**
- how much more upstream lands before WP11 (§9, decision 2);
- WP4 G2/G5 against WP3, which is the longest chain;
- whether the first live run turns up gestures that already fail on the harness side (the 21 Oct "setup failures" risk). The farm and the merged QUICK harness should reduce this.

---

## 7. What you give up (unchanged from the 90:10, with one clarification)
- **No physical preview-vs-export comparison at every checkpoint.** It runs once, at the end, alongside your viewing.
- **The App preview's visual layer stays a hand-port** of the Composition component. They share the evaluator, not the component. Merging them is deferred cleanup.
- **Detached and mixed Agent working copies are refused** instead of migrated (if you agree).
- The 8 deferred viewer and fixture rows stay as listed.
- Less per-version traceability. Code size stays above ideal until the cleanup step: the TS twin of the edit semantics and the large fixtures remain.

## 8. Kept exactly
- Concurrency and crash safety, and lost-acknowledgement retry (R01, R02, Runtime gate 2).
- Renderer-independent saving (R03).
- Lossless round-trip, including null vs absent (WP5).
- Unsafe old edits are refused (W01, AG-MAT).
- The fresh-clone ZIP check (gate 7).
- Never pushing upstream; never weakening tests; no M5.

## 9. Decisions I need from you before restart
1. **Adopt the operating model** in §1 (SYNTHESIS A–E)? *Recommended: yes.*
2. **Upstream coordination.** Upstream (AstridPseudon and its Claude sessions) landed about 250 commits since 21 Oct. If those sessions are yours, can they keep off the editor's save path files until we deliver? These are `useTimelinePersistence`, `useTimelineCommandsService`, `dataProvider`, `useAssetManagement`, `ShotEditorView`, the e2e local harness, and the Agent's `sdk/timeline/*`. *Recommended: yes. It is the cheapest way to shrink WP1 and WP11.*
3. **Runtime schema.** Renumber our commit tables to v32 after upstream's v31, and recreate dev and test realms rather than migrate them. *Recommended: yes.*
4. **Detached and mixed Agent publish:** refuse with a clear message (90:10), or migrate (adds about 4–6 h)? *Recommended: refuse.*
5. **Rename, shell create, archive and recover** stay as non-film metadata routes, listed in `owner-film-differences.md`? *Recommended: yes.*
6. **Gate 6:** the cheap evaluator gate at checkpoints, one physical run at the end, plus your viewing? *Recommended: yes.*
7. **App preview hand-port:** accept it for M4, with the shared evaluator as the "one viewer"? Or replace it with the package component (adds about 1 day)? *Recommended: accept, as later cleanup.*

On your go, WP0 starts. Nothing runs until then.

---

## 10. Task breakdown by manager and difficulty

**Difficulty**, under your 20 Oct model rule:
- **Normal** tasks run on Luna at high effort. That covers all reviews, test-only work, merge-forward and docs.
- **XHard** tasks run on Sol at high effort, and their brief starts with a `HARD:` line. The rule allows only three reasons: cross-repo contract, undo/rebase semantics, or a failure Luna already missed.
- No task uses xhigh.

**Sizes** are agent worker-hours: S ≤ 2, M 2–4, L 4–8. Every task gets one Luna review before merge. XHard tasks also get one independent data-safety review.

**Managers:**
- Runtime (main machine);
- Agent (Child 4);
- App (Child 1, plus Child 3, the former app2 machine, on one App work list; Child 3 owns the live suite);
- Viewing (Child 2);
- Farm (Child 5; runs proofs, never writes code);
- me (no Codex).

### Runtime manager (main machine)

| ID | Task | WP | Kind | Size | Needs |
|---|---|---|---|---|---|
| RT-1 | Merge upstream main; resolve service.py and upgrade.py; regenerate the contract and clients with the generators | WP1 | Normal | M | WP0 |
| RT-2 | Renumber our commit tables to schema v32, with an upgrade from upstream's v31 (app state) and a test that opens a v31 upstream realm | WP1 | **XHard** (migration order over a shipped upstream version) | M | RT-1 |
| RT-3 | `clip.move {track}`, multi-clip and pinned-group moves in the schema and the Python executor | WP3 | **XHard** (cross-repo contract) | L | RT-2 |
| RT-4 | `clip.set {transition}` values (the approved 0.2.18 carrier) and `Document.content_digest` | WP3 | Normal | M | RT-2 |
| RT-5 | Shared conformance cases for the RT-3 and RT-4 ops, used by both executors | WP3 | Normal (test-only) | S | RT-3, RT-4 |
| RT-6 | RT08: allocation and source-owner joins | WP7 | **XHard** (a wrong join overwrites film data) | M | RT-1 |
| RT-7 | D13 admission: consumer fencing | WP7 | **XHard** (concurrency fencing) | M | RT-1 |
| RT-8 | Refuse composition POST for every timeline (remove the headless branch); refuse publish-timeline-render; close the raw-SQL documents bypass | WP7 | Normal | M | AG-13, APP-24 (consumers gone) |
| RT-9 | The one-writer rejection test | WP7 | Normal (test-only) | M | RT-8 |

### Agent manager (Child 4)

| ID | Task | WP | Kind | Size | Needs |
|---|---|---|---|---|---|
| AG-1 | Merge upstream main (13 conflicts); keep upstream's working-copy and parent-clip behaviour inside the native paths | WP1 | Normal | M | RT-1 |
| AG-2 | Re-vendor the Runtime client from the merged Runtime; regenerate `artifacts.json` | WP1 | Normal | S | RT-2 |
| AG-3 | Composition pin to the shared head tgz; fix the stale pin tests | WP2 | Normal | S | VW-1 |
| AG-4 | `document_diff`: final whole-document equality check, plus tests per field class | WP5 | Normal | S | AG-1 |
| AG-5 | WC1: candidate publish through `document_diff`; refuse what it can't express | WP6 | Normal | M | AG-4 |
| AG-6 | WC3: native media replace (keep the original success semantics) | WP6 | Normal | M | AG-1 |
| AG-7 | AG-M2-TB01: text-binding writers to `text-binding.set` | WP6 | Normal | M | AG-1 |
| AG-8 | WC5: voiceover as a producer proposal the requester commits | WP6 | **XHard** (cross-repo proposal contract) | M | AG-7, RT-7 |
| AG-9 | `create_empty` to `timeline.init` | WP6 | Normal | S | AG-1 |
| AG-10 | WC7/AG02: refuse detached and mixed publish with a clear message; remove the `publish_bundle` callers | WP6 | Normal | M | decision 4 |
| AG-11 | WC8: three-way merge replaced by server-side rebase of retained commands | WP6 | **XHard** (rebase semantics) | L | AG-1 |
| AG-12 | AG03: sheet-local undo to Runtime undo/redo | WP6 | **XHard** (undo semantics) | M | AG-1 |
| AG-13 | D13 assembler: native render request, settled proposal, requester commits; give Runtime the final caller count | WP6 | **XHard** (cross-repo, with RT-7) | L | RT-7 |
| AG-14 | AG-MAT-V01..03: refuse unsafe v1; qualify v2 | WP6 | Normal | M | AG-1 |
| AG-15 | Grep guard test against the old writers | WP6 | Normal (test-only) | S | AG-5 to AG-13 |

### App manager (Child 1; Child 3 on the same work list)

| ID | Task | WP | Kind | Size | Needs |
|---|---|---|---|---|---|
| APP-1 | Merge part 1: modify/delete (take upstream's deletions), docs, config, supabase | WP1 | Normal | M | RT-1 |
| APP-2 | Merge part 2: editor writer files; port the four upstream fixes into the native path | WP1 | Normal (+ data-safety review) | M | APP-1 |
| APP-3 | Merge part 3: e2e harness with upstream's QUICK tier (Child 3) | WP1 | Normal | M | APP-1 |
| APP-4 | Re-vendor the Runtime client and astrid-browser (tool-generated provenance) | WP1 | Normal | S | AG-1, RT-2 |
| APP-5 | Composition pin 0.0.13 to the shared head tgz (0.0.14 moves pixels: tell Viewing) | WP2 | Normal | S | VW-1 |
| APP-6 | TS twin of the RT-3 and RT-4 ops, passing RT-5's conformance cases | WP3 | **XHard** (cross-repo contract parity) | M | RT-5 |
| APP-7 | G1: split | WP4 | Normal | M | APP-2 |
| APP-8 | G2a: single cross-track drag and drag to a new track; flip their `it.fails` tests | WP4 | Normal | M | APP-6 |
| APP-9 | G2b: multi-select and pinned-group drags; flip their `it.fails` tests | WP4 | **XHard** (group semantics; the regression we caused) | M | APP-8 |
| APP-10 | G3: edge-drag trim | WP4 | Normal | S | APP-2 |
| APP-11 | G4: keyboard and non-parent delete | WP4 | Normal | S | APP-2 |
| APP-12 | G5: transition SET and bulk reset | WP4 | Normal | M | APP-6 |
| APP-13 | G6 + G16: image drop and `registerAsset` | WP4 | Normal | M | APP-2 |
| APP-14 | G7: add-after and drop-replace | WP4 | Normal | M | APP-2 |
| APP-15 | G8: popup ADD wired to the native port; delete the popup writer | WP4 | Normal | M | APP-2 |
| APP-16 | G9: activate popup SWAP | WP4 | Normal | S | APP-15 |
| APP-17 | WP5 App: exact replay in the generic adapter, plus `shot.set` / `clip.set-params` emission | WP5 | Normal (+ data-safety review) | M | APP-2 |
| APP-18 | G10 + G11: ordinary batch and element routes through the generic route | WP4 | Normal | M | APP-17 |
| APP-19 | G12: placement service to `placement.*` (with server rebase) | WP4 | **XHard** (rebase semantics) | M | APP-2 |
| APP-20 | G13: bootstrap repair to `timeline.init` | WP4 | Normal | S | APP-2 |
| APP-21 | G14 + G15: shot settings and the shot-port publish | WP4 | Normal | M | APP-17 |
| APP-22 | G17/D02: snapshot history to Runtime undo/redo | WP4 | **XHard** (undo semantics) | M | APP-2 |
| APP-23 | Delete the save funnel and unused facades; add the guard test | WP4 | Normal | M | APP-7 to APP-22 |
| APP-24 | Confirm zero App callers of composition POST (input to RT-8) | WP7 | Normal | S | APP-23 |
| LIVE-1 | `live.ts` fixture, the standard check, L01 and L03 first (Child 3) | WP9 | Normal (test-only) | M | APP-3 |
| LIVE-2 | Scenarios L01–L28 (Child 3) | WP9 | Normal (test-only) | L | LIVE-1 |
| LIVE-3 | Scenarios X01–X06, R01–R05, W02, V02 (Child 3) | WP9 | Normal (test-only) | L | LIVE-1 |
| LIVE-4 | `live-watch.mjs` and `npm run live:session` (Child 3) | WP9 | Normal | S | LIVE-1 |

### Viewing manager (Child 2)

| ID | Task | WP | Kind | Size | Needs |
|---|---|---|---|---|---|
| VW-1 | Pack the Composition head once (build, test, smoke); name the tgz by commit | WP2 | Normal | S | WP0 |
| VW-2 | Staging fix: the 3 missing SceneSurface files plus a closure witness | WP8 | Normal | S | WP0 |
| VW-3 | Theme: the compiled-transitions scene uses the output theme; check App and Agent theme resolution match | WP8 | Normal | S | APP-2 |
| VW-4 | Cheap gate 6: evaluator digests at PARITY_FRAMES, with 3 planted negatives | WP8 | Normal (test-only) | M | VW-3, APP-5, AG-3 |
| VW-5 | D08a: cold-open compiled projection | WP8 | Normal | M | APP-2 |
| VW-6 | D08b + VW-AUDIO-STEP: continuous PCM policy, positives and planted negatives | WP8 | Normal | M | VW-2 |
| VW-7 | D09: private timing math replaced by the evaluator | WP8 | Normal | M | VW-1 |
| VW-8 | VW-D09a: `mouth_state` on the shared timing | WP8 | Normal | S | VW-7 |
| VW-9 | VW-D09-LEGACY-FADE qualification | WP8 | Normal | S | VW-7 |
| VW-10 | Write the farm request for the final physical parity run | WP8 | Normal (docs) | S | VW-4 |

### Farm manager (Child 5; no product code)

| ID | Task | When |
|---|---|---|
| FARM-1 | Codex sign-in, hello worker | WP0 |
| FARM-2 | Full suites on **upstream main** (new baselines for 3 repos) | right after WP0, in parallel with the merges |
| FARM-3 | First live-suite run on the merged tuple (the "how it updates today" table) | after LIVE-2 |
| FARM-4 | At each checkpoint: full suites, live suite, cheap gate 6 | 00/06/12/18Z |
| FARM-5 | Final: everything above plus the one physical parity run | WP11 |

### Orchestrator (me)

| ID | Task | When |
|---|---|---|
| ORC-1 | Write your decisions into the docs, freeze the precedents, issue the work lists | WP0 |
| ORC-2 | Trigger and audit the 12-hourly upstream merges; track the WP1 audit's new rows | throughout |
| ORC-3 | Ledger close-out check (row → commit → test → live scenario) | WP10 |
| ORC-4 | Final refresh, `delivery-build`, fresh-clone check, ZIP, viewing README | WP11 |

### Totals

| Manager | Tasks | XHard | Worker-hours (S≈1.5, M≈3, L≈6) |
|---|---|---|---|
| Runtime | 9 | 4 | ~28 (range 19–38) |
| Agent | 15 | 4 | ~44 (range 29–58) |
| App (incl. live suite) | 28 | 4 | ~78 (range 52–104) |
| Viewing | 10 | 0 | ~21 (range 14–28) |
| Farm | 5 (runs only) | — | — |
| **Total** | **62** | **12** | **~170 (range 115–230)** |

That makes **12 XHard tasks out of 62** code tasks.
- App carries the most work. That is why Child 3 takes the live suite and App runs about three lanes in parallel.

**This total is higher than the 75–110 hours in §0,** because counting task by task includes each task's own review and merge.

**The wall-clock estimate still stands.** It is set by the longest dependent chain, not by total hours, since the areas run 4–6 workers each at once. That chain is about 30 worker-hours done one after another:

RT-1 → RT-2 → RT-3 → RT-5 → APP-6 → APP-9 → APP-23 → APP-24 → RT-8 → RT-9 → WP11

With reviews, checkpoints and waits, that is 2–2.5 days.

**Give the XHard tasks on that chain (RT-2, RT-3, APP-6, APP-9) Sol from the start,** rather than waiting for Luna to fail. A failed first attempt there delays everything behind it.

---

## 11. Future-proofing: design rules only, nothing built in M4

**The target (for later).**
- Runtime is the only executor of edit commands.
- Clients send commands and show a quick *prediction* until Runtime's result arrives.
- There is no byte-identical client copy of the edit logic.

This one design works with a local Runtime (replies in milliseconds) and with a per-user cloud Runtime (replies in 20–200 ms). Nothing has to be removed or rebuilt when moving between them.

**Already compatible, no change needed:**
- the single `/commit` route;
- idempotency keys and the outbox;
- server rebase and visible conflicts;
- shared history and undo;
- Agent and App reading the same head.

**M4 design rules.** These are constraints on work we're doing anyway, not new work:
1. **Gesture commands come from intent.** WP4 gesture code builds commands from what the user did (clip ids, target track, time), with ids generated on the client. It must not need to execute a command locally to know what to send.
2. **Keep the TypeScript copy minimal.** WP3/APP-6 extends it only as far as the existing App commit path strictly needs. Ask the App lead first. Anything added there is known to be temporary.
3. **No hard-coded Runtime address.** New live-suite code reads the Runtime and door addresses from config, not a hard-coded 127.0.0.1:17340.

**Not in M4:**
- the predictor;
- the dry-run call;
- removing the TypeScript copy;
- a latency-injection test;
- anything cloud-specific.

---

## 12. End state at delivery (M4)

**Product behaviour**
- Runtime is the only writer of film data. Every App and Agent film edit is a small command through `/commit`, and the old routes refuse film writes, proved by a test.
- The open App picks up Agent edits without a reload, with the delay measured. The Agent sees App edits at once.
- History and undo are shared.
- Simultaneous edits merge, and real conflicts are visible with the draft kept.
- Retries and crashes never double or drop an edit.
- Saving works with the renderer off.
- Everyday gestures are native, including the four repaired drags.
- Rare edits that can't be expressed exactly are refused with a message.

**What you hold**
- A ZIP: one squashed patch and one bundle per repo, on top of the day's upstream main, verified on a fresh clone.
- Gate results.
- The live-suite evidence.
- A viewing README.

**Known leftovers, all documented**
- About +40k net product lines, against about +12k for a clean version.
- The TypeScript copy of the edit logic and about 56k lines of byte-identical fixtures.
- The hand-copied App preview renderer.
- The 8 deferred rows.
- Non-film metadata routes outside `/commit`.

**After that, the owner's release step:** push or tag the producers, repoint the pins, and get upstream CI green. Only the owner pushes upstream.

---

## 13. After delivery, before M5: cleanup pass (about 1 day of agent work)

**Why it's needed.** About a third of the effort was inherent and two thirds came from how the work was built:
- internal releases;
- splitting the work by repo;
- one new rule per incident;
- no stable test environment;
- adding the new path alongside the old one;
- keeping the edit logic in two languages.

The process causes are removed by §1. The code causes need this pass. Without it, every M5 feature is built twice and fixture-tested across languages.

**Work**
1. Make Runtime the single executor:
   - delete the TypeScript copy (about 7.8k lines) and most fixtures (about 45–50k);
   - per-op tests become shared scenarios run against Runtime;
   - add a small visual predictor for move, trim, split, delete and transition (a few hundred lines, no fixtures);
   - add a Runtime dry-run call for exact pre-commit checks.

   Start with a latency spike on one gesture. If it is under about 50 ms locally, go fully server-authoritative.
2. App preview uses the shared Composition component instead of the hand port.
3. Delete old route bodies with no callers left. A short refusal stays for old clients.
4. Remove the transitional bridges, guards and tests that only proved intermediate states.
5. Close or consciously keep the 8 deferred rows.
6. Decide the rare refused edits: give each a native command, or leave it refused.

**Measurable targets**
- Net product lines ≤ about +15k.
- One executor and one renderer.
- No code reachable only from tests.
- No file that exists only to bridge old and new.

**Independent review.** A reviewer that didn't build any of this is asked: "what is the simplest design that meets these guarantees, and how far is this code from it?" Each gap becomes a task or a written exception.

---

## 14. Future, only if chosen: a per-user cloud Runtime

**The save design works unchanged.** It already assumes a fallible network. The §13 predictor carries the feel at 20–200 ms. Very fast chained edits (repeated splits, arrow-key nudges) would also need the outbox to send commands on top of predicted results.

**Separate work, all additive:**
- per-user sign-in and TLS in front of the door;
- media in object storage (upstream has begun moving imports to Runtime object routes);
- cloud rendering;
- per-user storage and backups;
- start and idle-shutdown, and the cost model;
- the Agent next to Runtime, or reaching it over the network.

**Only if very fast chained editing in the cloud becomes a priority:** consider one shared executor implementation for client and server. That is a large rewrite; not planned.

---

## 15. How we'll run it (proposals from 22 Oct, owner to confirm)

1. **One central task board** in the hub: the §10 table with a status per task. Managers claim and close their rows, cross-repo tasks list both owners, and the orchestrator audits the board. It replaces the per-area work lists.
2. **Contract first.** The WP3 schema and shared conformance cases (RT-5) are written first. Then RT-3 (Python) and APP-6 (TypeScript) are built in parallel against them. That saves about 3–6 hours on the critical path.
3. **Codex quota:**
   - each machine keeps its existing sign-in;
   - the farm runs on Claude (it only executes tests, and needs no sign-in);
   - per-merge reviews could move to Claude to save about a third of worker runs (this changes the owner's rule that reviews use Luna);
   - the automatic Claude fallback stays.
4. **Upstream coordination** (§9, decision 2), and a small upstream merge at each 12-hourly checkpoint.
5. **XHard tasks on the critical path get Sol from the start:** RT-2, RT-3, APP-6, APP-9.

---

## 16. Review outcome (22 Oct): Astra (over-engineering, scope creep) and Opus (speed, strategy)

**Full reviews:**
- `/tmp/claude-0/-home-user/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/review-20261022/astra-review.md`
- `/tmp/claude-0/-home-user/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/review-20261022/opus-review.md`

**Where they agree.** The goal, inventory and core work (WP1–WP7) are right, and the plan still overbuilds its proof machinery and its task structure.
- Opus judged 2–2.5 days **not credible as written** (3–4 days), and realistic with the changes below.
- Astra: "finish the existing migrations and the seven gates using existing harnesses, with required deletions included before M4."

### A. Adopted (verified, or both reviews agree)
1. **Corrected critical path.**
   - The command definitions (`astrid/core/timeline/schema/edit-command.schema.json`) and their Python executor (`astrid/sdk/timeline/commands.py`) live in **Agent**. Runtime holds a byte-identical copy (verified).
   - So:
     - WP3 does not wait for the Runtime schema renumber (RT-2);
     - the three upstream merges start **in parallel** (Agent and App wait on Runtime only for the re-vendor step);
     - the conformance cases are written first, then the Agent executor and APP-6 are built in parallel against them;
     - RT-2 becomes a Luna task off the critical path.
   - New chain: App merge ‖ (cases → executor ‖ TS copy) → drags and transitions → funnel deletion → route cut → final. **Saves about 6–10 h.**
2. **Deletion is the unit of work.**
   - The 62 per-repo tasks of §10 become about **10 slices**. Each slice moves every caller of one old writer across repos, deletes the writer **and** its adapters, bridges and obsolete tests, and gives one behavioural proof. Each slice has one owner and one review.
   - The two critical-path slices, **"vocabulary and drags"** and **"route cut"**, each have a single owner across repos. The route-cut test is written test-first, so the cut lands right after the App funnel is gone.
   - **Saves 4–6 hand-offs, about 5–12 h.**
3. **Deletions happen in M4, not later.**
   - Old route bodies are deleted in M4. Only a short 410 refusal stays for old clients.
   - Bridges and guards go with each writer.
   - §13 shrinks to the optional TypeScript-copy removal and renderer decision, decided separately, with no automatic commitment.
4. **The live suite becomes one gesture tour.** It is data-driven and extends `three-products.spec.ts`. That spec already covers:
   - an Agent edit showing in the open App (:408);
   - concurrent edits (:495);
   - a Runtime restart (:665);
   - the full gate-5 sequence (:1115).

   For each gesture, the tour checks:
   - the commits sent;
   - **zero old-route requests**;
   - only the intended fields changed;
   - the result survives a reload;
   - undo restores the previous state.

   Lost acknowledgement, restart and concurrency are proved once, by the existing gate-5 journey.
   - **Cut:** the watcher and launcher, the per-step journal, and the 44 separate scenarios.
   - **Kept:** the film-viewing instructions, which the goal requires.
   - **Saves about 8–10 worker-hours,** plus the reruns of flaky tests.
5. **Cut `Document.content_digest`.** Its only consumer was a test, which compares canonical documents instead.
6. **Strike "add a Runtime dry-run call".** It already exists: `CommitRequest.dry_run`, `timeline_commit_port.py:524` (verified).
7. **Mechanical work moves off Codex.** Scripts or Claude handle, with no worker or extra review:
   - generated-file and modify/delete conflicts (regenerate or accept);
   - re-vendors and pins;
   - grep audits;
   - the ledger.

   Only product-code merges get reviews. **About 25–35% fewer Codex runs.**
8. **Audit holes, now covered:**
   - Upstream 874366eae added an extension-panel clip drag that saves through `applyEdit` and never names `saveTimeline*`. The true caller list comes from deleting the funnel on a scratch branch and letting typecheck list every caller.
   - Upstream deed0eb3e's install-manifest skew test will fail against our new Runtime contract until the owner's release moves `public/install-manifest.json`. Added to the release-step gap in §12.
9. **Popup ADD and SWAP are a risk spike, not Normal tasks.** Native ADD never reached the editor, and SWAP has an unsettled mismatch between projections. Spike both with Sol in the first hours.
10. **Merge cadence:**
    - turn on `git rerere`;
    - run a free merge preview at each checkpoint;
    - do real merges only at restart, at the end of day 1 and at the final refresh;
    - ask for an upstream freeze window of about 6 h before the final refresh.
11. **Delivery additions** (Astra):
    - prove that the ZIP's dependencies resolve **without any push** (the Runtime and Composition artifacts are included, since hub-only pins leave CI unresolved);
    - one architecture page;
    - an honest size report;
    - the documented visual differences;
    - film viewing on **a duplicate of your own film**, not a sample;
    - managers and loops stopped at the end.
12. **§11 and §14.** Keep only the two design rules: commands come from what the user did, and the Runtime address comes from config. The cloud discussion moves out of the work order into a separate note.
13. **Prove early, in the first 6 hours:**
    - that the farm's browser lanes reach a test body;
    - a `delivery-build` dry run;
    - the popup spike.

    Then make a **go/no-go call at H6**, with a fresh estimate from what was measured.

### B. Where the reviews disagree: my recommendation
- **Gate 6.**
  - Astra: cut the cheap evaluator gate, and make the existing physical parity tests (which already have planted mismatches) actually run.
  - Opus: keep the cheap gate.
  - **Recommendation: the physical run is the gate.** Fix the environment (VW-2 and the theme fix) and prove the farm's browser lane by H6. Build the cheap evaluator check **only if** the physical run still can't be made to run by then.

### C. New or sharpened owner decisions (adding to §9)
- **Decision 8: WC8 becomes a refusal.**
  - An Agent working copy that has fallen behind the head is refused and pointed to a fresh checkout. Upstream 4eea1dd24 already says so.
  - Rebuilding the three-way merge would cost about 6–8 h of Sol.
  - Astra's caution applies: this removes a capability, so it needs your explicit yes, like decision 4.
- **Decision 9: the rare refused edits.** After the first tour run, you get the specific list of edits that would be refused. You accept each by name, or it gets a native command. No blanket refusal.
- **Decision 10: reviews on Claude** instead of Luna, to save quota.
- **Decision 11: an upstream freeze window** of about 6 h before the final refresh.

### D. Effect on the estimate
- **Opus:** 3–4 days as written, and 2–2.5 days with A1–A7 adopted.
- **Mine:** with §16 adopted, 2–2.5 days remains the target. It gets confirmed or revised at the H6 go/no-go call from measured progress, not before.

---

## 17. Fit with the likely end state: Turso/libSQL and the agent tools on a remote machine (Opus review, 22 Oct)

Full review: `/tmp/claude-0/-home-user/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/review-20261022/opus-turso-review.md`. Code claims were checked against the code; Turso behaviour is inference.

**Verdict.** Nothing this plan builds has to be removed or rebuilt. The following all carry over:
- the commit protocol;
- the idempotency key: a database primary key, `canonical_schema.py:213-219`;
- the head compare-and-set: `timeline_commit_store.py:1103-1106`;
- optimistic rebase;
- the outbox;
- the v32 migration, the live tests, the pins and the delivery.

**What doesn't fit is underneath, and is mostly upstream code:**
- **Runtime's storage layer.** It uses one shared `sqlite3` connection behind an in-process lock (`store.py:745,1137`). Each commit runs dozens of statements inside one `BEGIN IMMEDIATE`. WAL, backup, VACUUM and admission all work on the database file.
  - Fine if Runtime owns a local libSQL file on the remote machine (option **a**).
  - Needs a storage redesign if Turso is a separate network database (option **b**): every statement becomes a round trip while the write lock is held. An embedded replica probably sends its writes to the primary, so it behaves like (b) for commits; this needs checking.
- **The door and the loopback rules.** The door binds to 127.0.0.1 and uses one shared credential file, so every browser user is the same actor. Runtime and the Agent SDK accept only loopback. Runtime hands out local file paths for media. A remote setup *replaces* these (real per-user auth, object routes); it doesn't extend them.

**Design rules added to M4 (cost 0–1 h in total):**
1. The v32 migration is plain SQL on a connection: no `executescript`, no file access, no VACUUM.
2. Commit correctness comes only from the ledger key and the head compare-and-set, never from the in-process lock. Nothing new goes inside the commit's write transaction.
3. New code reads media bytes through Runtime's object routes, never local file paths.
4. The live tour's "zero old-route requests" proof comes from the browser's network traffic plus Runtime's `/commits`, not the door's audit log file.
5. Optional (0.5 h): the WP7 one-writer test compares a per-table SQL digest instead of `iterdump()`.
6. **Don't deepen the local assumptions:** no new door features, no new loopback checks, no new users of local media paths.

**For the owner:**
- **Pick (a) or (b) on paper now; it costs nothing.**
  - (a) Runtime and the Agent on one remote machine, Runtime owning a local libSQL file, and Turso used for replication and backup. This is the cheap, coherent end state.
  - (b) Runtime talking to a separate Turso database over the network. This means redesigning the storage layer to use fewer, batched statements per commit.
- §14's "the save design works unchanged" holds for the protocol, and for the storage layer only under (a).
- "Turso" also names the newer Rust rewrite, which is still beta. Check its support for savepoints, `json_each` and the pragmas Runtime uses before relying on it.

---

## 18. Owner direction (22 Oct) and recommended speed-ups

**Cloud direction (owner).** Open-minded on Turso. The cloud version must:
- run on our domain;
- use the normal Runtime and the same SQLite as normal;
- have as little cloud-specific code as possible.

**Resulting target, for later; nothing built in M4.** The normal Runtime runs with its normal local SQLite file on a server on our domain.
- **Turso is not required.**
- **One container per user,** each with its own disk. The Runtime is unchanged and needs no multi-tenant code; the existing per-realm credential works per container.
- **The only cloud-specific parts:**
  - a reverse proxy for TLS and sign-in, which routes each user to their container;
  - backups, through Runtime's existing backup or disk snapshots;
  - media through Runtime's object routes.
- §17's M4 design rules keep that path open.

**Speed-ups recommended,** given that all coding work runs on Codex:
- **Adopt:**
  - §16 A1–A13 (corrected critical path, parallel merges, contract first, deletion slices with single owners, the gesture tour, scripted mechanical work, the early proofs and the H6 go/no-go);
  - decision 8 (WC8 refusal);
  - decision 11 (upstream freeze on the save-path files, then a final merge);
  - Sol from the start on the hard chain tasks;
  - the slice list instead of the ledger;
  - a one-page rulebook;
  - acceptance mapped to the seven gates.
- **Coordination on Claude, not Codex:**
  - slice managers on Sonnet;
  - the farm, which only runs tests;
  - the orchestrator.

  All product code and reviews stay on Codex (Luna, or Sol for XHard).
- **Not recommended:**
  - reviews on Claude (decision 10: no);
  - more machines;
  - pulling the TypeScript-copy removal into M4;
  - building the cheap gate 6, except as the H6 fallback.

---

## 19. End state vs the owner's goals (second Astra review, 22 Oct)

Full review: `/tmp/claude-0/-home-user/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/review-20261022/astra2-review.md`.

**Verdict.** The M4 direction is sound, but the promised end state is not yet secured.

| Goal | Astra | Change adopted |
|---|---|---|
| M0–M4 delivered | Partly met | The cheap check is a diagnostic only and never passes gate 6. Refused capabilities are accepted by name. After the merge of the edit logic, the affected gates are re-run and an updated ZIP is built. |
| Simple, nothing rebuilt | Partly met | The merge of the edit logic replaces client behaviour, so its design is settled *before* M4 ends (below). |
| Edit logic exists once | **Missed as written** | §16 A3 made the merge optional. **It is now a required milestone before M5.** The predictor must never decide guards or accepted state. |
| Clean base for M5 | Partly met | Settle the renderer question by ownership before M5: keep legitimate host integration, and fold anything that duplicates Composition behaviour into Composition. |
| Cloud: normal Runtime and SQLite on our domain | Met as a direction | Also document: where the Agent and its provider run, how the proxy reaches the loopback-only door and passes its Host/Origin checks (`door.py:528`), and the browser connection config. No Turso-driven work. |
| Coding and reviews on Codex | Partly met | §16 A7 is narrowed. **All code changes and merge decisions run on Codex,** including conflict resolution, pins and generated files, done by a Codex worker as part of each merge task. Claude only coordinates and runs predetermined commands (farm, audits). |
| 2–2.5 days | Partly met | That is **M4 only**. The required merge milestone is estimated separately once its design spike is done. |

**Correction (verified).** Runtime has **no separate Python copy** of the edit logic. It imports the Agent's provider (`timeline_commit_provider.py:79`: `astrid.sdk.timeline.commit`). Python is already one implementation, so the only duplicate is the App's TypeScript copy.

**Sequence:**
1. M4 delivery, then stop.
2. **Required merge milestone:** Runtime/Agent becomes the single executor, the App's TypeScript copy is deleted, and the renderer duplication is resolved by ownership.
3. Gates re-run and an updated ZIP.
4. M5, only when separately authorised.
5. Cloud deployment later, informed now by the §17–§18 rules.

**Design spike for the merge, run during M4** by one Sol worker as a short, read-mostly design:
- how dependent queued edits work without a local executor, e.g. split then trim, with a lost acknowledgement and a restart, under realistic remote delay;
- how the original guards, offline chaining, restart recovery and exact retry survive;
- how WP5's exact-replay check works without local replay.

If preserving this behaviour needs shared executable semantics, that is decided explicitly, not discovered halfway through deletion. The existing dry run does not solve offline execution.

---

## 20. Structural debt: what this project fixes (owner question, 22 Oct)

**Fixed in this project, in the required merge milestone, because the same code is already being changed:**
1. **Edit semantics are owned by Runtime.** The command definitions and the executor move from the Agent repo (`astrid/sdk/timeline/*`, `edit-command.schema.json`) into Runtime, or into one small shared Python package that Runtime owns. The Agent imports them, and Runtime no longer imports the Agent (`timeline_commit_provider.py:79`). This also simplifies the per-user cloud container. About +0.5 day.
2. **Leftover viewing duplicates.**
   - One theme resolver, starting from the M4 theme fix.
   - One audio track volume rule.
   - The Python curve mirror is deleted if it has no caller.
   - Settled together with the renderer-by-ownership work. About 2–4 h.

**"No worse" rules in M4, at zero cost:**
- no new vendored copies or committed tgz beyond the single Composition artifact;
- no growth of the very large files (deleting writers shrinks them);
- no new unknown-field preservation hacks.

**Not in this project. Owner decisions or small cleanups before M5:**
- **(3) Repo structure.** Should Runtime, Composition and the shared edit logic live in one repo? Decide this before (2), because a monorepo makes most of the packaging question disappear.
- **(2) Packaging** instead of vendoring: the Runtime client and the App's copy of the Agent browser code.
- **(8) Agent working copies:** keep them as a feature on top of commands, or remove them.
- **(6) Main's own failing tests:** get the baseline green.

**Opportunistic only:**
- **(4)** split big files where a slice touches them;
- **(9)** tighten the document schema once there is one writer.

**Leave alone:** (5), the storage layer. One user per container fits it.
