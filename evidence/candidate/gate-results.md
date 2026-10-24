# Timeline v2.1 final qualification inputs — PENDING

This document is the input to the final `delivery-build` README, not a release result. It intentionally contains no final ZIP receipt, final source pin, final tree identity, live-main refresh result, or all-gates-green claim. The Runtime candidate was authored from `tl/integration` base `becfe6db`; that authoring base is not a final delivery pin.

## Source and delivery boundary

F-final must perform one final live-upstream refresh per repository under D51, then build the final integrated tuple on Runtime main using the existing builder. The generated README sections, builder checks, and received receipts—not this draft—must provide the final `origin/main` SHAs, integration SHAs and trees, live-tip checks, patch counts, bundle mode, applied trees, bundle trees, and ZIP identity.

The patch and bundle routes remain equivalent tree-preserving installation routes. The synthetic `git am` commit is not a producer or publication identity. A failed pin, patch, bundle, tree, or live-tip check stops delivery and remains visible for the next refresh.

Runtime is the only writer. All production callers use the v2 commit door described in [`contract/commit-v2.md`](../contract/commit-v2.md): the exact project/timeline scope and base revision/publication pair, nonempty commands, label, step metadata and patches, merge mode, declared reads, dry-run flag, source/rationale/group annotations, and the HTTP idempotency key. Existing permission refusals remain stopped. No new trust backend, Farm access, schema-source access, alternate writer, or force-conflict route is authorized.

## Final proof status

All outcomes are **PENDING** until actual final-tuple receipts are attached. Historical runs are retained only as historical scope and cannot close these rows.

| Proof | Required final evidence | Status |
|---|---|---|
| P1 | Final integrated real-document split → trim-new-ID → intervening Agent edit → lost acknowledgement → restart chain, covering accepted, merged, and refused replies. | **PENDING** |
| P2 | Final integrated App core gestures, commit-door traffic, intended-field preservation, reload, undo, and no old save route. App-owned verdict. | **PENDING** |
| P3 | Final integrated Gate-5 journey with exact retry accounting, newer local edit, restart/reload, undo, and zero legacy snapshot traffic. App-owned verdict plus the required independent verdict review. | **PENDING** |
| P4 | Final integrated Agent CLI/Python/sheet single edit, ten-note per-step undo, conflict/re-run, and show/history evidence. | **PENDING** |
| P5 | Final integrated Runtime renderer-off save, door authorization, crash/retry points, and changed payload under one idempotency key. | **PENDING** |

**Core Timeline suites: PENDING.** The required core surface is EditCommand, the commit door, undo/redo, history, split/trim/move/placement/occurrence, show/sheet/visualize, the App save path, and the Agent editing runner, rebase, and inverse. D54 requires this core set and P1–P5 to be green on the final tuple.

## Final venues and receipts

- **F-final / ZIP:** Runtime manager on main, after the D51 refresh and final integrated qualification; status **PENDING**.
- **Runtime:** its lane-owned service; status **PENDING**.
- **Agent:** its lane-owned service; status **PENDING**.
- **App:** its lane-owned service; App owns P2/P3 execution and verdicts; status **PENDING**.
- **Composition:** final full suite on main; status **PENDING**.
- **Farm and schema-access work:** stopped under D56; no new child, preflight, checkpoint, source acquisition, or permission-refusal retry is a receipt.

The final receipt must show the v2 reply shapes. `accepted` and `merged` include the canonical document and full receipt/records, with steps, dependencies, bindings, effects, history, actor, and undo. A successful preview reports `would_status` and a null receipt. `conflict` and `invalid` include structured `code`, `path`, `hint`, `current`, and `suggested_command` details. A mutation request includes `api_version`, project/timeline, exact base pair, nonempty commands, label, steps (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), merge, reads, dry-run, source, rationale, group ID, and the HTTP idempotency key.

## Historical evidence and limits

Historical bounded evidence must remain labeled as historical and scoped to its original source tuple. Existing links include [the retained P1 actual-cause report](design/app-A2-P1-17985-actual-cause-sol-2017.md), [the retained integrated P4 symbol report](design/agent-F-P4-symbol-integrated-0023.md), and [the retained App P4/P5 registration report](design/app-F-P4-P5-registration-cumulative-0838.md). They are not final-tuple receipts and do not establish final GO.

The D54a known-gap rule is strict: each non-green node needs evidence identifying one category—environment/setup, upstream-identical/pre-existing, D52 deliberate deprecation with caller proof, or owner-deferred scope. A caused regression is fixed or reverted. No test of live behavior is weakened, skipped, deleted, or converted into a refusal expectation.

Rendering/parity remains deferred. Relational timing remains deferred. The M5 extension-model rewrite remains deferred. Deferred relay, remote-provider, and provider-child scope remains fail-closed. These boundaries do not resurrect prior acceptance criteria or add delivery extras.

## Pending installer fields

The installer must return, at minimum:

- final live-main refresh receipt for Agent, Runtime, App, and Composition;
- each repository’s exact `origin/main` base SHA, `tl/integration` tip SHA, and integration tree;
- each generated patch count, bundle mode, applied tree, bundle tree, and verification status;
- final P1, P2, P3, P4, P5, and core-suite receipts, with source tuple and venue;
- App’s P2/P3 verdicts and the required independent verdict review;
- Composition main full-suite receipt;
- F-final builder result, final ZIP SHA256, and `SHA256SUMS`.

Until those fields are received, every final status in this document remains **PENDING**.
