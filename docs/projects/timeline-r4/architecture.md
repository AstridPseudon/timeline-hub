# Architecture: one timeline, one change path (r4, 15 Oct 2026)

The design behind [cards.md](cards.md): what each card builds and why the pieces fit. The cards say what to do; this page says why.

**Basis:** the North Star (one change path, anchored time with one compiler, one evaluated scene); the 14 Oct film work; `production/review/optimization/opus-r4-overengineering-20261014.md`; the 15 Oct reviews in `production/review/optimization/r4-review-20261015/`.

**The problem it solves:** before r4 there were four change vocabularies, a Python mirror of the renderer, two timing engines, and "re-apply recorded commands onto a newer head" designed six times. r4 keeps every capability and builds each mechanism once.

## 1. The six pieces

| # | Piece | What it is | Lives in | Cards |
|---|---|---|---|---|
| 1 | **Timeline document** | The stored truth: tracks, clips, params; time anchored to words, beats or other clips; media referenced by content handle. Every version is an immutable Runtime revision. `app.astrid.v` protects Astrid semantics; each admitted extension protects its own semantic keys with its separately versioned owner namespace. | Astrid `sdk/timeline`; Runtime revisions | H-DATA, IDENTITY, CUTS, STORY |
| 2 | **EditCommand** | The only change verb: Astrid's draft OpCall evolved, typed, with `expect` preconditions; its inverse comes from the command registry. Only the envelope is frozen; the handler set stays open. The registry holds what execution needs (handler, inverse, canonical name, aliases) and generates the reference docs; the CLI, SDK, sheet and App reach it through small explicit adapters. | Astrid `sdk/timeline` (runner, registry); App `commands/types.ts` | CONTRACT-COMMAND, RUNNER, REGISTRY, APPLY-FILES, BYPASSES |
| 3 | **Commit + rebase** | The only write path. `commit(base, commands)` gives a new revision and a receipt. A stale head gives `rebase(commands, onto=head)`: accepted, or a named conflict. The one rebase serves every case: the App's unsent suffix (through the commit route's dry run), an agent's `checkout` refresh, revert (inverse commands), sheet and external imports, and replay. The Runtime accepts atomically, with a durable request identity, so a retry returns the original result. | Astrid's commit service, mounted on a Runtime route; Runtime acceptance | CONTRACT-COMMIT, REBASE, SHEET-EXTERNAL, COMMIT, ACCEPT, SUFFIX, UNDO-REVERT, AGENT-SYNC |
| 4 | **Timing compiler** | `compile_timing(inputs, commands)`: anchors in, frames out; pure, deterministic, **the only writer of resolved timing**. It is extracted unchanged first, then fixed: one fit store, references bound to the word or step they meant, never rebound silently. | Astrid | CHARACTERIZE, COMPILER, TIMING-FIXES, MUSIC-SEGMENTS |
| 5 | **Shared evaluation** | Grown from the composition's own `planTrack` / `DrawPlan` / `layerOpacity`: prepare a revision once, then answer queries for requested frames (layer order, opacity, coverage, bounds), with "unknown" where a component declares nothing. The renderer and the App Player draw through it; Python asks the warm renderer and caches per revision digest and renderer closure. Pure role and metadata queries (such as `role_of`) stay in Python, so editing and reflow never need a renderer. | the composition repo (`T/`); a Python client in Astrid | EVAL, PLAYER, CHECKS, CHANGE-VIEW, LINT, RETIRE-EVAL |
| 6 | **Revision + receipt** | The Runtime's existing idempotent replay, conditional head move, receipts and compare-and-swap, plus an evidence digest, ancestry and a compact head read. | Runtime `runtime_protocol` | ACCEPT, HISTORY-WIRE, HISTORY |

The flow is the same for everyone (the App, an agent, an extension):

```
read revision → produce commands → commit (rebase if the head moved) → compile timing
                                                                        → the shared evaluation answers frame queries
                                                                            ├─ the renderer and the Player draw
                                                                            ├─ checks and lint read visibility
                                                                            └─ the change view lists the intervals that may have changed
```

## 2. The four faces of `astrid timelines`

| Face | What it is | Cards |
|---|---|---|
| **show** (text) | Document text (tracks, clips, words, anchors) is pure Python and instant; what is visible at a frame comes from the shared evaluation. | SHOW, VISUALIZE |
| **visualize** (images) | The renderer draws chosen frames; filmstrip, contact, overview and motion are frame selections and layouts. | VISUALIZE, CAPTURE, SHARED-CAPTURE |
| **check** | Schema checks in Python; on-screen rules read the shared evaluation. | CHECKS, LINT |
| **edit** | Commands → commit (rebase if stale) → recompile; the other three faces read the new revision. | RUNNER, COMMIT |

**Invariant:** for one revision, text, images and checks read the same compiled document and the same evaluation, so they cannot disagree about timing or visibility.

**The change view** lists the frame and audio intervals that may have changed between two revisions, from the commands and what they depend on. An unknown dependency widens the interval, so it never under-reports (CHANGE-VIEW).

## 3. Extensions: five kinds, each proven with its first consumer

- EXT-ONE builds the operation kind and chooses one extension mechanism while proving `fit_to_beats`, preferring the production pack-v3 manifest path; freeze the other mechanism without deleting unknown callers.
- EXT-VIEW builds the view kind with fresh-agent `story_overview` in `show`, `visualize` and the App; views never mutate.
- EXT-COMPONENT builds the component kind with fresh-agent `vignette`; write the modifier contract first and obtain the orchestrator's consequential oracle decision before build. Player/export parity and declared bounds (or explicit unknown) protect renderer meaning.
- EXT-CHECK-GEN builds check/generator support by converting existing DAMAGED-ART and `chiptune.compose`, preserving existing checks and media-handle semantics.
- EXT-CURVES admits curves, transitions, music actions and command macros by one declaration each, preserving one undoable macro step.
- Each kind's CLI/SDK/App/view support is built in its first-extension card. No adapter or generic machinery is built ahead of a real consumer. These are the five contributor-facing kinds: operation, view, component, check, generator.
- Operations return commands and generators return asset handles; admission retains capability/source digests and declared network/file needs. Proposals are (base revision, commands), accepted through rebase plus commit. Advisory presence remains excluded.

Authority: [15 October user amendment](amendments/r4-release3-extension-kinds-restored.md); technical card details are in [cards.md](cards.md). The modifier-contract decision uses existing oracle routing, not an extra independent review stage.

## 4. What goes away

| Removed | Replaced by | Card |
|---|---|---|
| `core/timeline/inverses.py` (783 lines, used only by its own test) | inverses in the command registry | BYPASSES |
| `sdk/timeline_editing.py`'s retime helpers as a second timing engine | the compiler (the helpers stay as thin wrappers, or deprecated) | COMPILER |
| `core/timeline/onscreen.py`, the Python mirror of the renderer | the shared evaluation (visibility) and a pure role module (metadata) | EVAL, LINT, RETIRE-EVAL |
| six rebase designs (merge, App suffix, agent refresh, stale head, revert, replay) | one `rebase(commands, onto)` | REBASE |
| `/publish-document` and the App's app-save adapter | App writers emitting commands through the commit route | GESTURES, WRITERS |
| per-feature `requires` arrays | one Astrid integer `app.astrid.v`; each extension has its own owner namespace/version | H-DATA |
| the staged narration record (3 states) | narration bindings and the head in one SQLite transaction, if HISTORY finds it needed | HISTORY, SCRIPT-REFLOW |

## 5. Decided: one editing surface (the owner, 14 Oct)

- **Checkout plus the runner is the editing surface.** Every write (CLI, SDK, sheet, App, extensions) is an EditCommand run by it (RUNNER).
- **The authoring bundle is the storage adapter:** how a timeline is serialized, read and written. It is not an editing model.
- **`sdk/timeline_editing.py`'s timing helpers move into the compiler** (COMPILER); its write paths go through the runner (RUNNER).
- **Adapter period:** `sdk/remote.py` and the visualize fast lane keep reading through the bundle until RUNNER lands, then call the runner. No cut-over day.
- **The App:** every App writer emits commands in Release 1 (GESTURES, WRITERS). We write the PRs; the App's maintainers review when available, which doesn't block.
- **Why:** the film was edited through Checkout's journaled mutators and agents use them; two editing models drift.

## 6. What crosses repos

- **Two frozen contracts**, in their existing homes:
  - CONTRACT-COMMIT: CommitRequest/Result, the HTTP errors, the Runtime acceptance interface, and the dry-run rebase that gives the App its rebased suffix;
  - CONTRACT-COMMAND: the EditCommand envelope with shared request/result and timing fixtures.
  Each consumer proves its own part against the shared fixtures: Astrid the semantics, the App the adaptation, the Runtime validation, preservation, acceptance and replay. The real commit path is tested end to end at IP3. A change to either contract is a card the orchestrator approves. Astrid-internal APIs are not frozen.
- **One renderer closure:** the composition fork (`T/`, v0.0.7), pinned by Astrid and the App to the same artifact (PINS-ASTRID, PINS-APP).
- **How the programme runs** (dispatch, merging, integration points, the machine): [agent_goal.md](agent_goal.md), [manager-brief.md](manager-brief.md), [testing.md](testing.md).

## 7. Shared documents, transcript bindings, and storage encoding

The complete cross-owner contract is in [the Astra098 amendment](amendments/20261016-upstream-transcript-extension-integration.md). Shared project documents remain Runtime-owned records accessed through a thin declared facade over existing CRUD/CAS/pagination; edit-owned extension values live in versioned owner namespaces and change only through EditCommands. Preserve the existing managed-input declaration at `config.app.transcript`; media associations/defaults use `config.app.transcript.references`, and each clip occurrence binds immutably at `clip.app.transcript.binding`. The compiler derives word times; a default association change cannot silently retarget a clip. The authoring-bundle adapter owns the flat logical view and chapter storage encoding. Track definitions have one canonical film owner; chapter references and renderer projections are derived. These rules add no Runtime interpreter, second history, timeline writer, storage service, top-level transcript field, or extension kind.
