# spec.md: the design index and glossary for the timeline-platform portfolio (A–J)

**Status:** v4 (final pass), 11 Oct 2026. Every ruling is folded in: DECISIONS-astra-review (+ the ship-soon addendum), DECISIONS-app-deep-dive, DECISIONS-deep-dives-1 and DECISIONS-deep-dives-2 (all in `reviews/`). **The evidence lives in `reviews/`** and is cited, not restated. The reviewed v1 is in `archive/` for traceability only.

## 1. What to read (one sitting, in this order)

| Order | Document | Holds |
|---|---|---|
| 1 | [release-contract.md](release-contract.md) | the users; **Releases 1–3** with their scope and elapsed time; the invariants; the acceptance gates |
| 2 | [plan.md](plan.md) · [tasklist.md](tasklist.md) | workstreams × releases, the critical path, the first actions · one row per task, each linking a brief card |
| 3 | the workstream specs | [spec-save.md](spec-save.md) (commands, the commit path, adapt-save fallback, merge, history, the writer census, the App collaboration core) · [spec-timing.md](spec-timing.md) (the timing compiler, sequence identity, cuts) · [spec-rendering.md](spec-rendering.md) (capture, parity, one evaluator, coverage, the change view, pins) · [spec-hardening.md](spec-hardening.md) (MIG-0, COMPAT-1, MIG-GOLDEN, routes, the SEC gate) · [spec-agent.md](spec-agent.md) (agent sync, the verify loop, views, the skill, vocabulary) · [spec-later.md](spec-later.md) (Releases 2–3) |
| 4 | [briefs/](briefs/) | one owner-brief per workstream (WS-SAVE, WS-TIME, WS-RENDER, WS-HARDEN, WS-AGENT, WS-LATER) + GATES, each with task cards |
| 5 | [open-questions.md](open-questions.md) | the product decisions for the user, Codex's items, and the oracle defaults |

**The code root:** `${HISTORICAL_USER_HOME}/Developer/astrid-video/astrid-local/Astrid`, read at trunk `f840ec1c`. r4 runs on the **merged base**; SPEC-0 re-pins every path (GATES brief).

## 2. Glossary
| Term | Meaning |
|---|---|
| **the v8 film** | Project `almost-ready`, timeline `01M4GGKMHZ3J8V402C8CWSCE95`: one shot, 316 clips, 45 cuts, 8 chapters. Its exact baseline is frozen by SPEC-0/MIG-GOLDEN. **Workers use duplicates only.** |
| **clip / layer / line / Cut** | An item on a track · a non-picture visual over a cut (`c41.mink`) · a narration take holding its words (`n21`) · a span with one picture, with a stable id (`c08`, `c30b`) that is **never reused**; the **cut index** derives them, keeping gaps, overlaps and sequence ranges |
| **compiled fields / intent** | What the renderer reads (`at`, `hold`, `from`, `to`, params) / Astrid's meaning under `app.astrid` (A1, dual-read) |
| **time reference; Address / Selection / TimeRef** | Something timed against (a word, beat, cut, clip, the film's ends) · one thing / many things / one instant (`"viral" +9f`), all resolved by one lookup |
| **timing relation** | An authored tie of a timing property to a TimeRef (`on`, `until`, `for`, `formulas`, `sequence_fit`, the music policy, the film end). Absolute timing is valid where none is authored. |
| **timing compiler** | The only writer of compiled timing: `prepare_timing` → `compile_timing` over an explicit dependency graph |
| **preserve-anchor adjustment** | A drag of a TimeRef-tied clip keeps the reference and changes only the offset |
| **EditCommand** | One explicit edit: `command, target, args, resolved, expect, bindings, created, authorship` |
| **gesture command** | The App's EditCommand for one user gesture, sent from its transaction boundary. **The primary App path.** |
| **adapt-save** | **The fallback:** whole-document saves → commands, by enumerated rules. It never invents intent. |
| **runner / transaction / EditResult / ChangePreview** | Executes commands · one undo step + one edit record · the committed result / the dry-run result (both share the change description) |
| **commit path** | Astrid's semantic commit service (G1) + the Runtime's atomic acceptance (S-RT): CAS, a durable request identity (semantic hash vs attempt hash), the accepted result + evidence stored with the head move; an exact retry returns the original result |
| **canonical document / id_map** | The accepted revision in the request's scope / old → new ids (forks, created entities) |
| **scope** | `parent`, or `occurrence:<oid>` + base revisions + `content: this-occurrence \| shared-shot`; `complete` lists the collections where omission means deletion |
| **presence-aware** | Set, explicit clear, or untouched. **There is no global "null means delete".** |
| **merge** | A three-way merge at property level, presence-aware, occurrence-aware; conflicts are `same-property`, `dependent`, `delete-vs-edit` |
| **undo / revert / restore** | Undo my draft edit · revert a published change (a new commit, with preconditions) · restore a whole revision (a new commit, behind a dirty-save barrier) |
| **external revision** | Written outside the commit path; imported before any semantic edit |
| **capability declarations** | Astrid semantics use one `app.astrid.v` integer per timeline at the commit boundary; each admitted extension owns a separate `app.<stable-owner-id>.v` namespace version (H-DATA; no per-feature `requires`) |
| **rendered frame / coverage model / affected intervals** | Pixels from the one evaluator (P = App Player, R = full capture, F = fast lane, E = encoded) · metadata with per-property provenance and "unknown" · a conservative union of what may have changed (unknown → included) |
| **change view** | Before/after rendered frames + audio review over the affected intervals |
| **one evaluator** | P6's hybrid migration: the App keeps its asset, readiness and registry adapters; its semantics move to the package's pure `prepare` / `video` / `audio` |
| **MIG-GOLDEN** | The v8 identity gate (every frame + audio + intent) |
| **SEC gate** | H-GRANT, H-TRANSPORT, H-REVOKE + H-ROUTES; no real data on astrid.haus before it passes |
| **owners** | Astrid: us. Runtime, App, connector: Codex's owners merge our PRs (Q-own). Packages: the maintainers merge our fork PRs. |

## Appendix A: older ids, decoded
- **R-1…R-6:** r3's rulings (restated in plan.md).
- **XC-4 / API §G.10:** the runner / the old "reconcile" idea, now split into adapt-save, merge, restore and replay.
- **G-1, TX-1, M-1:** the journal, transactions, Selection (done).
- **T1-2/4/6/7/18:** the coverage model / tile addresses / next-edit lines / the alignment golden test / intent-aware lint.
- **T1-1, T1-20, X-41:** the sweep, the motion compare, the verify view, all folded into the change view.
- **F-060 / F-081 / F-085:** motion from the element / the c17 tear (the class the compiler removes) / drifting truths about one clip.
- **H-2/H-4/H-6:** layers lost in re-flow / nudge keeps the anchor / a sheet split re-created ids.
- **L1…L13:** the ticket families.
- **X1 / X2:** the exit tests (first five minutes / novelty).
- **Round 1 #1–#10:** ROUND-1's root causes.
- **ƒ(MARK):** a param relative to a spatial mark.
- **MO, MOD:** motion and modifier items.
- **R-n:** render-matrix rows.

## Appendix B: corrections to older sources (the evidence is in the cited review)
1. **The App computes timing consequences** (snapping, speed on resize, overlap, duplicate ripple), so it sends gesture commands: the App deep dive.
2. **App saves lose and resurrect data today** (`config.app` on the config paths; base-spread resurrection): the App deep dive §1.4.
3. **A1 is lossy across save** (`_strip_derived`, parent clips): the migration report.
4. **The Runtime's `parent_revision_id` is not ancestry:** the Runtime report.
5. **`FULL_FRAME` is in `reflow.py:91`, not in `check.py`.** The harness ran 3 paths, not 6. `TL@prev` and uids were never built. `duck` was never applied. These are from the v1 audit of the code.

## Appendix C: done before r4 (trunk f840ec1c; carried by the port)
S0 (its simulated App test is superseded by X0a/X0b) · A1 (+ the undo fix; MIG-0 fixes its loss) · L1 · CK2/CK4 (drafts; corrected in K2) · OPS1/OPS2 · G-1 · TX-1 · M-1.

## Appendix D: sources
- **Design:** `production/review/v8/audit/{ABSTRACTION-DECISION,ABSTRACTION-OPUS,API,EDITING-DESIGN,EXTENSIBILITY,CATALOGUE,RENDER-MATRIX,TRUTH,TICKETS,ROUND-0,ROUND-1}.md`.
- **Merge:** `production/review/merge/{TIMELINE-PLATFORM,WEB-EDIT-PATH,FINAL-E2E,ASTRID-HAUS,CODEX-REPLY}.md`.
- **Reviews and rulings:** `reviews/*.md`.

## Appendix E: long-term notes (not designs; not in r4)
- native Runtime groups / solver placements;
- schema enforce mode;
- incremental timing compile (only if the bench misses);
- keyframes tied to TimeRefs;
- renaming footage `slots` → `standins`;
- general nested timelines (refused);
- persisted App undo for every gesture;
- multi-shot cut semantics (refused, with a message);
- a universal relation store and wrapper rewrites (superseded);
- cross-film replay;
- CRDTs;
- whole-film locks;
- a general security policy engine;
- capacity beyond the v8 film.

## Astra098 current extension and transcript contract

For the current document facade, owner namespace, pinned transcript binding, per-operation compatibility, and chapter/track storage rules, follow [the applied Astra098 amendment](amendments/20261016-upstream-transcript-extension-integration.md). It qualifies existing cards and preserves their history; examples such as beats, analysis, and lyrics do not create new products or contribution kinds.
