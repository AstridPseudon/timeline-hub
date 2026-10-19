# Save path: one command history across surfaces

**Purpose:** current save and history guidance for the CLI, SDK, sheet, agents, and App.
**Authority:** [North Star](northstar.md), [architecture](architecture.md), [current cards](cards.md), and the applied [commit-hosting ruling](amendments/20261015-commit-hosting-seam.md) and [many-hands ruling](amendments/20261015-many-hands-elegance.md).

## Current contract

Every surface edits the same timeline through one evolving OpCall/EditCommand record and one durable command/rebase/history path. The durable operation is commit from a base revision with commands. Astrid owns command meaning and rebase; the Runtime authenticates the existing commit route and owns atomic acceptance, the head check, request identity, and durable result. The approved hosting seam composes one fixed Astrid provider inside the existing Runtime daemon. It adds no service, public writer, or second route. See [CONTRACT-COMMIT](cards.md#contract-commit-freeze-the-commit-contract), [RUNNER](cards.md#runner-one-editcommand-format-and-one-runner), [REBASE](cards.md#rebase-replay-pending-commands-onto-a-new-head), and the [Astra21 ruling](receipts/codex-exec/oracle-R4-COMMIT-HOSTING-SEAM-001.result.md).

The App may keep responsive drag, selection, and provisional state in its local interaction adapter. That state remains separate from durable history: the App emits meaningful commands at the gesture boundary, sends one save at a time with stable request identity, and consumes the commit route's dry-run rebase for its unsent suffix. The App does not implement another durable command, rebase, or history path. See [GESTURES](cards.md#gestures-main-editor-gestures-emit-editcommands), [SAVE-ROUTING](cards.md#save-routing-flag-gated-routing-one-save-in-flight), and [SUFFIX](cards.md#suffix-keep-newer-edits-after-an-accepted-save).

The sheet and external revisions enter as explicit commands with provenance. Ambiguous relation-sensitive imports are refused with a next step; rebase does not infer a gesture from a document diff. See [SHEET-EXTERNAL](cards.md#sheet-external-sheet-and-external-revisions-as-explicit-commands). Undo, revert, and restore keep their separate meanings while using the same commit path and journal; see [UNDO-REVERT](cards.md#undo-revert-undo-revert-and-restore-through-commit).

## Command meaning and current maturity

The current source increment validates the OpCall envelope and carries the existing five fields. That is an increment, not the complete semantic contract, a freeze, or card completion. The current [A source handback](projects/A-integration/receipts/CONTRACT-COMMAND-source-increment-001.md) and [A task status](projects/A-integration/tasklist.md) leave these behaviors open:

- **Preconditions:** each write needs its original expected value, including an explicit ABSENT state when the property was absent. The wire encoding is not established here.
- **Identity:** resolution must retain stable scoped identity and the occurrence a command targeted. Local IDs cannot silently become global or occurrence-scoped IDs.
- **References and results:** bind the references a command used, record IDs it created, and carry authorship/provenance and result bindings through runner, rebase, inverse/revert, proposal acceptance, and App suffix handling.
- **Call records:** canonicalization and compact call semantics must preserve folded setters' original preconditions and add-to-set dependencies in journal calls.

Keep values distinct. The current command source increment maps an explicit clear to **clip.clear**; omission preserves the property; JSON null is a value; opaque objects remain values unless a handler gives them meaning. In particular, an object shaped like {op:clear} is not a clear instruction. ABSENT in a precondition is distinct from omission, null, and clear. Do not infer or publish a new encoding here. The source-backed details are in the [current command handback](projects/A-integration/receipts/CONTRACT-COMMAND-source-increment-001.md) and the [Astra23 direction](amendments/20261015-many-hands-elegance.md).

The commit path checks the requested base/head and relies on Runtime compare-and-swap and the durable request identity. A retry of the same accepted request returns its original result; a changed body under that identity conflicts. A stale-base dry run performs the same semantic rebase and returns a preview or conflict without accepting or storing anything. See [COMMIT](cards.md#commit-one-commit-path), [SUFFIX](cards.md#suffix-keep-newer-edits-after-an-accepted-save), and [IP3–IP4](testing.md#3-integration-points-the-merge-manager-through-the-lease).

One transaction has one journaled command history and one undo step. Preview, Player, and export use the shared evaluation where the cards require frame agreement; they do not maintain hand-kept scene meanings. See [EVAL](cards.md#eval-shared-scene-evaluation-grown-from-plantrack), [PLAYER](cards.md#player-the-app-player-uses-the-same-evaluation), [RENDER-PARITY](cards.md#render-parity-player-versus-render-spot-check-harness), and [IP5](testing.md#3-integration-points-the-merge-manager-through-the-lease).

## Current examples and pending proof

The existing [COMMIT example](cards.md#commit-one-commit-path) keeps a 9-frame drag 9 frames after its narration word through a later retime. The [IP3–IP4 scenarios](testing.md#3-integration-points-the-merge-manager-through-the-lease) and X0 examples keep the anchored App drag, an intervening agent retime, a held save response plus a newer local edit, disjoint survival, a named overlap conflict, idempotent retry, and failed-suffix recovery. The [main editor](cards.md#x0-editor-record-the-main-editors-save-paths) and [shot popup](cards.md#x0-popup-record-the-shot-popups-save-paths) must have the same meaning. These are card-owned examples; this page does not claim their integration point or observations have passed.

X0 observations and named historical film proof remain pending where [status](status.md) and [X0-EDITOR](cards.md#x0-editor-record-the-main-editors-save-paths) say so. Synthetic fixtures exercise only their stated behavior; they are not historical film evidence. Editing this specification changes no card status, acceptance count, review allowance, or gate.

## Historical proposals retained as history

Earlier text proposed a **/publish-document** fallback endpoint, an **adapt-save** document-diff path with presence rules and T1–T10 gesture rows, and a **three_way** document merge. These are historical proposals, not active instructions: [COMMIT](cards.md#commit-one-commit-path) excludes a new /publish-document route, [WRITERS](cards.md#writers-convert-every-other-app-writer-then-switch-together) owns the eventual App cutover, and [REBASE](cards.md#rebase-replay-pending-commands-onto-a-new-head) plus [SHEET-EXTERNAL](cards.md#sheet-external-sheet-and-external-revisions-as-explicit-commands) own current behavior.

The former generic args example that treated {op:clear} as an encoding is also historical. The command source increment uses explicit **clip.clear**; an object value shaped like {op:clear} remains opaque data. See the [source handback](projects/A-integration/receipts/CONTRACT-COMMAND-source-increment-001.md).

## Shared documents and timeline adoption

Shared transcript and other project-document writes use the existing Runtime document CRUD/CAS/idempotency route. Preserve the existing hash-bound `config.app.transcript` managed-input declaration; media associations/defaults live at `config.app.transcript.references`, while each clip's authoritative immutable occurrence reference lives at `clip.app.transcript.binding`. Changing the default index does not retarget a bound clip unless the same explicit transaction includes a rebind command. Only the validated semantic import/binding operation may write provenance and snapshot fields; generic owner-property commands cannot forge them or rewrite derived timing. Corrections and association changes are explicit EditCommands, with no hidden post-publish refresh. A failed command leaves the prior immutable binding valid; retry uses the same source-write receipt and request identity. The timeline command pins the approved snapshot and never resolves mutable latest. Undo restores the prior reference without editing the shared document. There is no new publish-document route or combined document/timeline history. See [the Astra098 cross-owner contract](amendments/20261016-upstream-transcript-extension-integration.md).
