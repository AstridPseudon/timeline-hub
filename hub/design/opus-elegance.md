# What it would take to make the end state elegant (Opus, 22 Oct)

*Read-only. No Haiku tool was available, so I measured the integration heads myself (agent a086cc6db, app c85da5427, runtime cc7410a1f, composition 6c4d93421). **Facts** carry file:line or counts. Every fix, cost and "when" is **judgement**.*

## Verdict
After §13, §19 and §20 the system will be correct, and far less tangled than today. It still won't be elegant. Four things stand in the way, and the plan doesn't name them.
- **The wire command still carries the executor's internals.** The client works out reads and expectations before sending.
- **The App has three edit vocabularies.** The one M5 extensions are told to use isn't the one Runtime executes.
- **The Python edit core can't be cleanly moved yet.** It reaches into Agent pack discovery.
- **§13 plans to build a predictor that already exists.**

Each is cheap while the merge milestone is open. Without the fixes, a new command touches about a dozen product files in three repos; with them, three files in one repo. My estimate (judgement) is that elegance costs roughly 6–10 Codex worker-days in total, against about 1.5 in the plan. Two thirds is work the plan already requires, re-estimated.

## The elegant end state (judgement)
**Layout.** There are three repos. A platform repo holds:
- `runtime_protocol/`;
- `timeline_core/`: the document model, the command registry and executor, projections and curves;
- `contract/`: the document, edit-command, theme-default and audio-curve JSON, each as one file, with generated TS and Python types checked by `--check`;
- `packages/` (generated clients);
- `composition/`.

App and Agent each pin one platform commit. No tgz files are committed and nothing is vendored.

**Each concept lives once:**
- **Command semantics:** the `timeline_core` registry (today's `commands.py:60-95` `Operation` table, moved).
- **Document schema:** `contract/`.
- **Rendering and evaluation:** Composition. The App keeps only host adapters (media URLs, element host, player).
- **Themes:** one resolver, in Composition.
- **Audio:** one curve registry and one gain/volume rule, in Composition. Python checks read the generated table.
- **Client contract:** OpenAPI, from which the clients are generated.

**Interfaces:**
- **App → Runtime.** `POST …/commit` with a base head and `[{op, select, args, intent, group_id}]`, with client-allocated ids (already in the schema: `ClipSplitArgs.right_id`). Runtime alone computes reads, guards, records and rebase. The App previews with the `TimelinePatch` it already builds for each gesture, and swaps in the accepted document when it arrives.
- **Agent → Runtime.** The same API, through the generated Python client.
- **Composition.** A pure function from document to frames, used by both preview and export.

**Adding a command:** one schema `$def`, one registered function and one YAML scenario. That's three files in one repo. The CLI verb and the TS types are derived from these. An App gesture is optional: one intent-to-command builder. An M5 `@command` extension is the same function, registered from a pack.

## Gap table
| # | Gap | Evidence (fact) | Fix (judgement) | Cost | When |
|---|---|---|---|---|---|
| 1 | Client computes executor internals | `EditCommand` carries optional `resolved/expect/bindings/created/authorship/reads/selections` (`timeline-commit-types.ts:33`). The outbox advances local state with `bundle = payload.after` (`commitSession.ts:411-419`). growth-tests found that 55% of golden bytes are recorded reads. | Make the wire command `{op, select, args, intent, group_id}`, and have Runtime compute the records. Delete the TS capture port (49 non-test files, about 13.0k lines in `commands/`, of which about 7.8k is the port). | 12–20 h, high risk (gates 2 and 5) | **Now** (§19) |
| 2 | §13 adds a "small visual predictor" | Every gesture already submits `{command, preview: TimelinePatch}` (`commitSession.ts:54,72,128`), and pending previews are re-projected on the accepted basis (`:295-301`). Some gestures pass `preview: null` (`:600`). | Don't build a predictor. Keep the patch preview, add patches for the null cases, and drop `before/after`. | −(plan's work), +3 h | **Now** |
| 3 | The edit core can't be lifted out of Agent | Runtime loads it via `importlib` (`timeline_commit_provider.py:18,79`). Its static import closure is 43 modules and 12.7k lines at load, and up to 393 modules and 166k lines through lazy imports. The coupling runs through pack discovery (`core/timeline/kinds.py:21`) and element admission (`commit.py:485`, `_scalar_commands.py:99`). | Extract `timeline_core` (about 10k lines of `sdk/timeline` plus the 14.7k-line `core/timeline`) and give it an element and kind *port* that Runtime fills from pack snapshots it already stores. Delete the provider ABI and the Agent-side `RuntimeCommitService` (`commit.py:749`). | 10–16 h, medium (plan: 4 h) | **Now** (§20.1) |
| 4 | Three edit vocabularies in App | Public SDK `TimelinePatch` (`src/sdk/video/timeline/patch.ts:12` `@publicContract`, 13 op families). The local `TimelineCommand` runner (`commands/runner.ts` 607, `media.ts` 818; upstream). Runtime's `EditCommand`. Two diff-to-command adapters: `genericPatchCapture.ts` (696) and `document_diff.py` (497). The M5 design says editable views "only emit existing Commands" (ORIGINAL-PLAN:131). | Map the patch op families 1:1 onto EditCommands (`clip.update`→`clip.set`, `track.add`→`track.create`, …) and keep the patch only as the preview shape. Retire the runner once add/swap media are native commands. Keep one generic adapter or none. | 8–12 h, medium (public API) | Decide in the §19 spike (it deletes `genericPatchCapture`); build **before M5** |
| 5 | Schema copies with no source | The document schema exists as 4 byte-identical copies (sha f52b8202…): Agent, Runtime `contract/`, and App `vendor/timeline-schema` (Python and TS dist). Its provenance commit 242f9c43 is in none of the four repos. The edit-command schema has 2 copies (sha 6ba7b51e…) with no equality check. | Runtime `contract/` becomes the only source, and the others become generated artifacts pinned with the Runtime pin. | 2–4 h, low | **Now**, inside #3 |
| 6 | Renderer, theme, volume and curves duplicated | `TimelineRenderer.tsx` (1,798 lines) "mirrors" `TimelineComposition.tsx` (386) (`:71-74`). Theme merge exists three times (`resolveTheme.ts:15`, `installed-themes.ts:70`, `theme.py`). The volume rule exists four times (App `AudioTrack.tsx:373`, Composition `AudioTrack.tsx:39-41`, Agent `storage.py:510`, `readable_timing.py:188`). Composition's curves have drifted (`audio-curves.generated.ts:10`, `exponential-moderate`, absent in Agent). | Fold by ownership, as planned. | Renderer 8–16 h, medium-high (gate 6). Others 3–5 h (plan: 2–4 h for all of it) | **Now** (§19/§20.2) |
| 7 | Process residue | Schema "floors" for internal versions that were never published: `generate.py:100-120`, plus Runtime `published-command-schemas` (8 files, 9.8k lines) and Agent `current-union-command-schemas` (12 files, 14.3k). App run-named launchers `current013-*`, `current014-gate3*` and `main95-*` (20 files, 3.6k lines). Playwright configs went from 6 on main to 17. The stale `ui/` and `editor/live-scenes` dirs (6 files, 1.7k lines, zero callers). | Delete them. Keep one refusal test per old route. | 3–4 h, low | **Now** (WP10, or the first merge-milestone slice) |
| 8 | Test bulk | Added test plus fixture lines: Agent 52.1k + 55.6k, App 33.2k + 15.4k, Runtime 28.4k + 10.5k, Composition 2.2k. That's about 197k, against about 40k net product. Agent `editing_conformance` alone is 124 files and 65.5k lines. Upstream already has a scenario harness (`tests/editing_scenarios/*.yaml`, with cli/sheet/python forms). | Convert the per-op goldens to scenarios, and check the generic properties (undo, retry, rebase) once per registered op. Keep the `three-products` gate-5 journey. | 8–12 h, low (mechanical) | **Now**, with #1 |
| 9 | One command, many places | `clip.trim` appears in 7 Agent product files (`commands.py:85`, `timeline_sheet.py:757` capture table, `native_checkout.py:394`, `cli.py:3453`, `sync.py:370`, …), 2 Runtime schema copies and 5 App files, plus 39 test files. | Derive the sheet and CLI tables from the registry. `capture.py` and `native_checkout` go with #1. | 4–8 h, low | Before M5 (M5's `@command` builds on it) |
| 10 | God files we added | `commitSession.ts` 1,424 lines (37 imports, every gesture port in one closure), `dataProvider.ts` 2,492 (+556), `timeline_commit_store.py` 1,225, `_port.py` 1,019, `timeline_sheet.py` 1,466 (+414). | `commitSession` shrinks to the outbox after #1. Split the others only where a slice touches them. | Falls out of #1/#3, plus 3 h | Now, opportunistic |
| 11 | Pins and tgz | App pins Composition 0.0.13 (`package.json:124`) while Agent pins 0.0.14 (`remotion/package.json:18`). Three tgz are committed in each repo (0.0.8–0.0.14). | WP2's one pin. Delete the stale tgz now. #12 removes the rest. | 0.5 h | Now (WP2) |
| 12 | Repo boundaries | Runtime imports Agent (#3), while Agent vendors Runtime's client (`astrid_runtime_client`, 1,679 lines). Composition is 102 non-test files, shipped as tgz into two repos. | One platform repo: Runtime, `timeline_core`, contract and Composition. | 4–8 h, low-medium; owner decision | **Before M5**, decided before #3 lands |
| 13 | Unsynced logic, upstream | Shot projection exists three times (App `shotCompositionProjection.ts` 643, Agent `shot_composition_projection.py` 686, Runtime `managed_render_snapshot.py`). Shot dependencies exist twice (Agent `dependencies.py:155`, Runtime `shot_dependencies.py:89`). The asset-conflict rules differ (`asset-registry.ts:90` vs `managed_timeline.py:576`). | The Python copies collapse into `timeline_core` as it moves. The App asks Runtime instead of recomputing. | Python 3–5 h now; TS 6–8 h | Python now, TS before M5 |
| 14 | Element mirror | App `vendor/astrid-browser` (146 files, 11.5 MB) and `astrid-build-inputs` (66 files, 13.9 MB), whose `primary/` and `public/` subtrees duplicate each other (9.9k lines). They are pinned to Agent 091aa23e, not the head. Upstream, and guarded. | Elements become a built package, the way Composition's registry already works. | 8–16 h, upstream-owned | Owner decision before M5 (Elements are an M5 type) |

## Recommended order (judgement)
1. **M4 as planned.** Add #7 and #11 to WP2 and WP10 (about 4 h). Then stop.
2. **Widen the §19 spike** so it settles #1 (the wire shape), #2 (the existing preview is the predictor), #3 (the element and kind port) and #4 (patch to command), on paper, before any deletion.
3. **Owner decides #12.** If yes, the move in #3 lands straight in the platform repo, so nothing is moved twice.
4. **Merge milestone, in slices:** #3 with #5 and #13-Python, then #1 with #2 and #8, then #6. Re-run gates 2, 5 and 6 and rebuild the ZIP.
5. **Pre-M5 cleanup:** #4, #9, #13-TS, and the #14 decision. Then test the three-file recipe on one real command; any extra file is the first bug.

Owner's rule: #1–#3, #5–#8 and #13-Python touch code we are already changing, or would be built twice. #4 and #9 are M5's base. #12 is cheapest before #3 moves code.

## What not to do
- **No shared or offline executor** (generated TS or WASM) for local chaining. Client-allocated ids and server rebase already cover dependent edits; §14 calls it a large rewrite.
- **No four-repo monorepo.** App and Agent keep their own upstream life and CI.
- **Don't split upstream god files for their own sake:** `generic_host.py` (13,936 lines), `service.py` (8,873), `store.py` (6,911), `cli.py` (4,043).
- **Don't refactor the 710 benign clone pairs** (23.8k lines, mostly upstream forks and tests).
- **Don't replace the vendor-lock and hash guards with a new mechanism** if #12 is declined. They work (130 guarded pairs).
- **Don't chase the +15k line target** by deleting behavioural tests.
- **Don't redesign storage** or generate the edit-command schema from Python types.
- **Don't build a plugin framework ahead of M5.** The `Operation` table already is the registry.
