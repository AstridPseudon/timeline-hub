# Open questions: timeline-platform-r4

Current execution authority: [run.yaml](run.yaml), [agent_goal.md](agent_goal.md) and [source-state.md](source-state.md). Quoted prior Otto adoption/service text below is historical and inert; it does not authorize a runtime or operational action.

Every ruling-level question is settled in `reviews/DECISIONS-*.md`. What remains:
1. **product decisions for the user;**
2. **Codex's items;**
3. **targets**, which apply unless the orchestrator overrides them.

Answers go into status.md's decision log, citing the id.

## 1. Product decisions for the user (each with a recommendation)

> **DECIDED, 11 Oct ~11:45 local.** The user: "I agree with all your recommendations." Every row in this table is decided as recommended:
> - Q-R1, Q-port, Q-own, Q-T (the paired relay), Q-S1–S6, Q-shot, Q-overlap, Q-text, Q7, Q-remote, Q18;
> - plus adopting the Otto branch, Codex running the one owner service, and Claude's admission.
>
> Relayed to Codex (root thread: Otto adoption/service/admission; merge thread: ownership, security, editing choices, Q-C1–C6). Still open with Codex:
> - naming the save/rebase reviewer + backup;
> - accepting Q-C1–C6.
>
> External prerequisites (15 Oct rework):
> - `transport-choice`: decided 11 Oct, the paired relay. Completed and removed from the setup.
> - `ownership-approved`: SATISFIED. Codex named the reviewer (`${OLD_OWNER_HANDLE}/reigh_source_finish`) and backup (`/root`, merge thread) and accepted Q-C1–C6 (CODEX-REPLY, 11 Oct ~11:44). Completed and removed from the setup.
> - `codex-port-published` is replaced by the internal milestone `A#base` and the one external `codex-accepts-base`, which gates only RELEASE-1.
| # | Decision | Recommendation | Gates |
|---|---|---|---|
| **Q-R1** | **Release 1's scope and date:** safe many-hands editing on the film (release-contract §2), the Release-1 cards of A–H, the forecast is generated from the tasklist and redone when `E#save-rebase` merges. | Accept. | the plan |
| **Q-port** | **The portfolio shape:** ten projects A–J with their own managers under one orchestrator, contract-first, milestone dependencies (portfolio.md) | Accept (re-cut per DECISIONS-portfolio-strategy). The folders are generated, so re-cutting is cheap. | the activation |
| **Q-own** | **Who writes the App/Runtime/connector code** (B's S-PRES; C; E; H; R-EVAL's App part)? **And who reviews it:** a named Codex reviewer and a named backup, with an agreed review window. | **r4 implements reviewed PRs; Codex's owners approve and merge within the window; one named reviewer for save/rebase (E, C) plus a backup.** The alternative, Codex implementing it, moves the dates onto Codex's queue. | Release 1's critical path |
| **Q-T** | **The ONE primary astrid.haus transport.** | **The paired relay** (the hosted path you intended; it gets its own complete acceptance record). The direct loopback gateway is tested separately. Both need H-TRANSPORT's route and size fixes. | H-TRANSPORT, E-4a |
| **Q-S1** | May the relay operator see the film's media, prompts and results? | Approve a trusted-relay model for stage 3 explicitly, or require end-to-end protection before real data. | H-TRANSPORT |
| **Q-S2** | The default authority of an App-invoked agent | Edit, visualize and render the selected project in a confined environment. Anything wider (shell, outside files, new network) needs local approval. | H-GRANT |
| **Q-S3** | The stage-3 credential and discovery files | A redacted, reproducible launch manifest and one credential format. Never weaken checks to make the demo run. | H-TRANSPORT |
| **Q-S4** | Revocation vs a running render | Stop delegated work and fence publication. Background continuation only with a separate, approved job grant. | H-GRANT |
| **Q-S6** | Who owns the security boundary (App, connector, Astrid host, Runtime) | One named integration owner. The Runtime owns grant validation and provenance; the local host owns confinement and revocation. | H-GRANT, H-TRANSPORT |
| **Q-shot** | What a shot edit applies to | **This occurrence by default.** Changing shared content is explicit and lists the affected occurrences. | G1, P3B |
| **Q-overlap** | Drag-overlap trims and duplicate ripples | Keep today's behaviours with explicit policies. Content tied to a word, the music or a neighbour is never silently trimmed or detached; a choice is offered. | P3B, M3 |
| **Q-text** | The look of existing `clipType: text` documents once the renderers converge | Preserve today's appearance through a compatibility adaptation; separate plain-text and card identities from now on (needs approved screenshots of representative saved documents). | R-EVAL |
| **Q7** | When the live film gets new keys (uids, ranges, …) | Never automatically. Only by a user-approved publish after its duplicate passes MIG-GOLDEN, at the first release that writes such keys to it. | E-4a/b |
| **Q-remote** | **Remote workspaces** (e.g. Codex cloud) for 1–2 extra lanes | **Yes, for independent lanes** (G's parity runs, I/J preparation), if the provider allows it. Remote inference alone doesn't remove local contention; remote workspaces do. | capacity beyond 3 local workers |
| **Q18** | Run bookkeeping | Superseded operational mechanism: use the current native Megado file ledger; no Otto registration, activation or sync. Historical decision retained in original-docs. | none |

## 2. Codex's items (the orchestrator relays them)
| # | Item | Recommendation |
|---|---|---|
| **Q-C1** | Accept **Runtime-owned request/result durability** (S-RT) + one coordinated schema change. The history-compatibility policy: keep old repeated-revision publications as separate events, use fresh revision ids for semantic commits, use distinct predecessor names. | Accept (the Runtime report's recommendation). |
| **Q-C2** | **An immutable merged-tree snapshot + a manifest** of generated registries and dependency bytes; the exact v8 revision, assets, fonts and approved render. | Needed by SPEC-0, R-PINS and MIG-GOLDEN. |
| **Q-C3** | **The App's capability inventory:** deterministic export vs live preview (shaders, live materials). | Keep everything, but freeze live inputs before claiming parity. |
| **Q-C4** | **One batched catalog/client regeneration** for the new V3 public actions (status/watch/refresh/review/revert/restore, the commit routes). | Batch after G1 and A-SYNC merge. |
| **Q-C5** | **A Runtime generic "required features" check** (COMPAT-1) at acceptance. | Add it with S-RT. |
| **Q-C6** | **The route/size changes** from H-TRANSPORT, and the astrid.haus redeploy for E-4a. | Schedule against Release 1's date. |
| **info** | Port-relevant bugs already sent: A1 `_legacy` loss, App preservation, relay route gaps, narration auto-retry overwrite, shot metadata on a fresh head, donor registry collisions/caching. | The port fixes them, or r4's cards do (H-DATA, S-PRES, H-TRANSPORT, S-RT). |

## 3. Targets the cards use (they apply unless overridden)
| # | Default |
|---|---|
| Q13 | **Commit responsiveness** (warm v8): commit p50 ≤ 300 ms, p95 ≤ 1 s; gesture-to-ack p95 ≤ 1.5 s. A miss → profile, then decide. |
| Q15 | **The timing compiler:** p95 ≤ 150 ms for a full v8 compile; incremental compile only if this misses. |
| Q-V | **The loaded verify loop,** from Round 1's 61 s p50 baseline: 3-agent p50 ≤ 15 s, p95 ≤ 45 s; single-client p50 ≤ 5 s. |
| Q24 | PRACTICE grades Release-2 features "not yet", never as a failure. |
| Q25 | An App picture-clip deletion offers "lift the cut" first. |
