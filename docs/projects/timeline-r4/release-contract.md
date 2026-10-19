# Release contract: timeline-platform-r4, "One timeline, many hands"

Execution authority: [run.yaml](run.yaml) and the current [orchestrator goal](agent_goal.md) govern models, stages, custody and escalation. Historical names do not launch agents or override them.

**What r4 promises, to whom, when, and how we will know.** This file is for the orchestrator and the owner. Workers read their card in [cards.md](cards.md) and nothing else is required. **Design:** [spec.md](spec.md) (an index over six workstream specs), reached through a card's "Design detail" link. **Rulings and evidence:** `reviews/`. This contract states outcomes.

**The lens (the user):**
- **"Robust, simpler, elegant … ship very soon."**
- **Keep every capability,** each with the smallest mechanism that is correct for real usage: the App's actual saves, the agents' workflows, the v8 film.
- **Rare cases** get a clear refusal or conflict with a next step.
- **Long-term ideas** are one-line notes (spec.md Appendix E).

## 1. Who it is for
- **Agents** (fresh Claude agents, scripts; the CLI, SDK and sheet) need:
  - discoverable edits;
  - predictable timing;
  - a fast, truthful preview of each change;
  - knowing when the head moved;
  - recovery.
- **The user** (the App at astrid.haus, connected to the local runtime) needs:
  - gestures that hold after the next agent edit;
  - an honest "saved";
  - visible agent activity;
  - real conflict choices;
  - preview = render;
  - a laptop that stays safe.
- **Codex's owners** (the Runtime and the App) need:
  - small, reviewed PRs with real producers and consumers;
  - an atomic acceptance contract they own.

**The data:** `almost-ready` and its v8 film (one shot, 316 clips, 45 cuts, 8 chapters; the baseline is frozen by BASE and GOLDEN). **Portfolio:** ten projects, A–J, each run by its own manager under one orchestrator ([portfolio.md](portfolio.md), the playbook). Release 1 = the Release-1 cards of A–H. Release 2 = I + the Release-2 cards of C, D and F. Release 3 = J + the Release-3 cards of A, D, E and G. Dependencies are on milestones written `project#milestone` (for example `D#commit-service`); a milestone is complete when its card merges.

**The deployment:** the union runtime on this Mac, reached from astrid.haus over ONE primary transport (the user's decision, Q-T).

## 2. Releases (nothing is dropped; each release ships)
### Release 1: safe many-hands editing on the film
1. **One commit path for the App and agents.** The App sends gesture EditCommands; agents use the CLI/SDK. Astrid's commit service applies them on the exact base, and the Runtime accepts atomically with a durable request identity. A retry returns the original result.
2. **No data loss.**
   - App saves stop losing and resurrecting fields (presence-aware, opaque fields kept).
   - A1's migration is lossless.
   - Semantic keys are protected by capability declarations.
   - Accepted results rebase newer local edits.
3. **Timing keeps its meaning** for today's behaviours: one compiler, characterized first, with frames byte-identical on v8. Drags keep their anchors. Sequence steps keep other hands' edits. Cuts are stable.
4. **A truthful preview for the film's features:** the App preview converges on one evaluator for every feature v8 uses; a change view (conservative intervals + audio); coverage that says "unknown"; a fast loaded verify loop.
5. **History, undo, revert, restore,** plus agent sync (`status --watch` and a `checkout` refresh; no new verbs).
6. **The App collaboration core:** status line, activity feed, newer-changes, conflict panel, intent in the inspector.
7. **The astrid.haus security gate** (grant, confinement, revocation, transport, routes, credentials) passes before any real data.

**Early checkpoint, R1.0 :** App preservation fixes (`B#preservation`), capability protection (`B#compat`), one renderer pin set (`G#pins`), and the golden baseline (`A#golden-baseline`). It is integration point IP1 ([testing.md](testing.md)) and ships as soon as those cards have merged.

**Ownership of the sync verbs:** the Astrid CLI/SDK sync (`status --watch`, `checkout` refresh) is the AGENT-SYNC card in project D. HISTORY supplies `head()`; UNDO-REVERT supplies history/revert; SAVE-ROUTING and SUFFIX persist recovery state and COLLAB-UX displays collaboration state. These boundaries do not transfer agent-sync implementation to the App cards.

### Release 2: richer editing (project I + the Release-2 cards of C, D, F)
- timing repairs (`F#repairs`);
- transitions + duck, with a real audio consumer (`I#audio`);
- story ranges: chapters + beats (`I#story`);
- motion iteration, L13 (`I#motion`);
- targeted lint (`I#lint`);
- the Runtime schema warn report (`C#schema-warn`).

**Release 2 is complete** when its cards have merged with their checks green; the chapters' start frames stay exact (GOLDEN).

### Release 3: the open platform, proven (project J + the Release-3 cards of A, D, E, G)
- Five contributor-facing extension kinds, each admitted through one mechanism and built with its first real consumer: operation `fit_to_beats` (`J#ext-one`), view `story_overview` (`J#ext-view`), component `vignette` (`J#ext-component`), and existing check DAMAGED-ART plus generator `chiptune.compose` converted to declarations (`J#proofs`).
- Curves, transitions, music actions and command macros, each added by one declaration (`J#curves`).
- Review-before-accept of an agent's proposal (`E#review`); advisory presence remains excluded.
- Purge of archived/branching duplicates (`D#retention`).
- The full parity matrix, every supported row passing, including contributed components and transitions, and one evaluator per repo (`G#full-parity`).
- The final campaign, existing examiner round and owner's film viewing (`A#r3-accepted`); live migration waits for explicit user go.

Each kind's CLI/SDK/App/view support ships in its first-extension card; no adapter or generic machinery is built ahead of a real consumer. The EXT-COMPONENT modifier contract is a consequential root decision before its build: the orchestrator routes that specific contract judgment to the configured oracle. It adds no independent model-review stage or allowance. [Latest user amendment](amendments/r4-release3-extension-kinds-restored.md) supersedes the original narrowed Release-3 wording.

## 3. Invariants (every task)
| # | Invariant |
|---|---|
| **I1 No data loss** | No path drops intent, opaque keys or another owner's fields. Clears are explicit. Migrations are lossless and idempotent. Published revisions are never rewritten. The live film changes only by a user-approved publish after GOLDEN. |
| **I2 Exact identity** | Every commit names its exact base. The Runtime accepts atomically under CAS with a durable request identity. An exact retry returns the original result. |
| **I3 One write path** | Every writer in the census goes through the commit path, or is listed as a compatibility path imported before semantic edits. |
| **I4 Compatible formats and meaning** | Wire formats are additive. Semantic keys are written only behind declared capabilities. Old documents read and render the same. |
| **I5 Attribution** | One undo step + one edit record per draft transaction. An authenticated publisher, an asserted actor and retrievable evidence per publication. |
| **I6 Safe exposure** | No real data on astrid.haus until the SEC verification matrix passes on the transport actually used. |

## 3b. Shipped behaviours this contract guarantees in Release 1
**Drags:**
- a drag of word/music/neighbour-tied content keeps its tie and adjusts the offset;
- an overlap trim or a duplicate ripple that would touch tied content **offers a choice** instead of silently trimming or detaching it;
- a sequence-step drag offers detach / keep.

**Shot edits:**
- an edit applies **to this occurrence by default**;
- editing shared content is explicit and lists the affected occurrences.

**Media:**
- a new SFX takes its natural duration;
- non-intrinsic media with no duration is refused, with the next step.

## 4. Acceptance gates
A card is complete when its implementation and bounded checks merge; the milestone it produces completes with it. Film-level proof belongs to the integration points ([testing.md](testing.md)) and to RELEASE-1 and FINAL-R3, never to a card. People and models review in only three places, marked ★.

| Gate (card) | Release | Pass |
|---|---|---|
| **BASE** | first | The three branches tagged and become trunk; feature-parity inventory; renderer closure; v8 identity; baseline failure list (IP0). |
| **GREEN** | 1, right after BASE | The Runtime, Astrid and App suites green on trunk (any quarantine has an owner and an expiry, at most 10); `make doc-refs` green. |
| **GATE** | 1 | The real-film journey on a clone, as a bounded smoke at each named integration point and in full at the release candidates. Each phase reports observed success, observed failure, or "not observed" when its deadline passes first. |
| **R1.0 (IP1)** | 1 | `B#preservation` (X0 cases through real App functions + exact reload); `B#compat`; `G#pins`; `A#golden-baseline`. |
| **★ CONTRACT-COMMIT** | 1 | The commit contract frozen in its existing home. **One independent review call** reviews the schema against the invariants before it freezes; three repos consume it. |
| **★ COMMIT** | 1 | **One independent review call on the rebase and commit diff**, inside the card: "never invents intent" is a semantic claim the implementer's own tests tend to mirror. |
| **REPLAYS, PRACTICE** | 1 | REPLAYS builds the v9 and v11 scenarios; IP6 proves them. PRACTICE is a measurement round and gates nothing: metrics recorded, stumbles become cards. |
| **★ RELEASE-1** | 1 | The owner watches the film. First IP6 green on one recorded revision set (including the replays and the SEC matrix on the paired relay with disposable data), zero "fallback" App writers, and `codex-accepts-base`. Then on astrid.haus: `almost-ready` with its real title, 45 cuts, narration and music; an App edit appears in `timelines log` and survives a re-flow. |
| **Release 2** | 2 | Each card's check on trunk. The chapters' start frames stay exact (GOLDEN). |
| **★ FINAL-R3** | 3 | IP7 and IP8 green. One examiner round over the full capability set, FINAL-E2E and the GOLDEN compare on a migrated duplicate, and **the owner watches the film** before the live migration. |

## 5. When (a hypothesis, revised after the first real save/rebase slice)
**Assumptions:**
- the plan: <!-- generated:figures -->95 cards, 137.25 worker-days: R1 69 cards / 97 d, R2 15 cards / 21 d, R3 11 cards / 19.25 d; 38 normal, 57 xhard; largest card 2.5 d. The original two-worker arithmetic was about 48.5 working days before coordination losses; that is historical forecast arithmetic, not the current admission policy or a delivery promise.<!-- /generated --> (generated from [cards.md](cards.md) by the archived inert generator; per project in [tasklist.md](tasklist.md));
- adaptive useful concurrency on the actual 16 GiB Mac under current run.yaml and human amendments; native capacity plus authorized Codex Exec, with A coordinating actual shared-heavy contention;
- we implement every share, including the App and Runtime PRs; Codex's review does not block, except `codex-accepts-base` for RELEASE-1.

**The Release 1 forecast is redone when `E#save-rebase` merges.** That is the first point where real producer → consumer integration across the Runtime, Astrid and the App has been measured.

**The risks to Release 1's date:**
- measured memory/disk/test contention, model-service capacity and integration throughput; no fixed coding-worker ceiling;
- Codex's acceptance of the base (`codex-accepts-base`) and the astrid.haus redeploy;
- the hosted route proof (`H#route-proof`).
