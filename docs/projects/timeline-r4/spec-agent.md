# Agent experience: one vocabulary, exact revisions

**Purpose:** guidance for agents using the shared timeline through the CLI, SDK, sheet, and App.
**Authority:** [North Star](northstar.md), [architecture](architecture.md), [current cards](cards.md), and the applied [many-hands ruling](amendments/20261015-many-hands-elegance.md).

## The current edit loop

Use the shared vocabulary and meaning across surfaces: find, show, edit, see, publish. The current nouns and verbs are in the [North Star](northstar.md); the live registry and adapters are owned by [REGISTRY](cards.md#registry-registry-metadata-and-explicit-adapters). Do not add a second agent command language.

The [AGENT-SYNC card](cards.md#agent-sync-status-watch-checkout-refresh-exact-revision-verify) owns the shared behavior:

- **timelines status** reports the checkout base, observed head, accepted revision, unimported external revisions, and conflicts.
- Refreshing an existing checkout reapplies its recorded commands through the single rebase operation. Verification and post-commit reset read the exact receipt revision.
- Accepted work from another writer appears as activity; it is not evidence that this agent's own revision was verified.

There are no separate **refresh**, **watch**, or **review** verbs. Head observation belongs to status; checkout refresh uses rebase; proposal review is the per-agent App mode in [REVIEW](cards.md#review-review-an-agents-proposal-before-accepting), where a proposal is a base revision plus commands and acceptance is rebase plus commit.

## Current recipes and views

The generated skill is owned by [SKILL](cards.md#skill-one-generated-skill) and draws spellings from the registry. Examples that remain current include adding a layer with **--add CUT --like ADDRESS** ([ADD](cards.md#add-add-a-layer-in-one-command)), and reviewing orphan suggestions through the sheet and existing edit path ([REHOME](cards.md#rehome-re-home-orphans-in-bulk)). The explicit CLI clear flag **--clear KEY** is owned by [RUNNER](cards.md#runner-one-editcommand-format-and-one-runner); null is not a substitute for clear where the property schema forbids null.

Views remain readings of the same revision and addresses. [SHOW](cards.md#show-show-filters-cut-ranges-and-quiet-output) owns text and filters; [VISUALIZE](cards.md#visualize-views-agree-with-show-and-the-sheet) owns images and frames; checks and render visibility use the shared evaluator where their cards require it. App preview and export follow [PLAYER](cards.md#player-the-app-player-uses-the-same-evaluation) and [RENDER-PARITY](cards.md#render-parity-player-versus-render-spot-check-harness).

## Current demonstrations

The examples in [IP3–IP8](testing.md#3-integration-points-the-merge-manager-through-the-lease) remain the portfolio's named demonstrations, not new acceptance criteria in this page. They cover the commit retry and no-write dry run; an anchored App gesture plus a held response and a newer edit; shared preview/render/audio evaluation; two agents and the App seeing accepted provenance and exact revisions; and the first real extension consumers. The [Astra23 direction](amendments/20261015-many-hands-elegance.md) keeps these existing demonstrations and the X0 cases.

X0 observations and named historical proof remain visibly pending in [status](status.md). A synthetic scenario is not a substitute for an observed App payload or historical film comparison.

## Historical proposals retained as history

An earlier draft proposed three separate commands: **timelines refresh**, **timelines watch**, and **timelines review**. They are not current spellings; the current [AGENT-SYNC card](cards.md#agent-sync-status-watch-checkout-refresh-exact-revision-verify) explicitly has no such verbs. An earlier A/B vocabulary exercise also proposed freezing both grammars before choosing a winner. That experiment is superseded by the one shared vocabulary and registry aliases; the old comparison is not an active task.

The Round 1 figures previously quoted here—365 seconds median per ticket and 61 seconds verify p50—are dated study context, not current acceptance targets. Current performance and practice evidence remains with its owning cards and run records.

## Declared shared documents and edit-owned extension data

The first shared-record consumer is the transcript panel/Caption Foundry. Use the declared facade `documents.read/list/write(kind, subject, source)` over existing Runtime project-document operations; listing may paginate and filter locally. Kind/schema declarations and actor/project grants both apply. Writes use the actual per-kind deterministic ID rule, expected version, schema validation, and idempotency; a missing write grant makes writes unavailable while reads/caption flow may continue. Do not write timeline documents through this facade.

For timeline-owned extension data, `timelineData(namespace)` reads immutable revision data and builds existing set/add/remove/clear commands only on owned, declared paths. It does not provide a direct mutation or bypass Astrid's timing, identity, registry, or compiler rules. Preserve the managed declaration at `config.app.transcript`; its `.references` member indexes media associations/defaults. Bind each occurrence at `clip.app.transcript.binding` to an immutable approved snapshot, never latest, and never let a default-index change silently retarget it. Caption text and association changes use EditCommands. Caption Foundry invokes the admitted transcript host's validated binding operation or owns only its separately declared data; it cannot forge transcript provenance through generic owner properties. REVIEW uses a pinned base revision, ordered commands, and source binding/digest. Follow [the Astra098 amendment](amendments/20261016-upstream-transcript-extension-integration.md) for exact identity, mapping, retry, and migration behavior.
