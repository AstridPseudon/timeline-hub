# Timeline v2.1 final qualification inputs — PENDING

This document is the input to the final `delivery-build` README, not a release result. It intentionally contains no final ZIP receipt, final source pin, final tree identity, live-main refresh result, or all-gates-green claim. The Runtime candidate was authored from `tl/integration` base `becfe6db`; that authoring base is not a final delivery pin.

## Source and delivery boundary

F-final must perform one final live-upstream refresh per repository under D51, then build the final integrated tuple on Runtime main using the existing builder. The generated README sections, builder checks, and received receipts—not this draft—must provide the final `origin/main` SHAs, integration SHAs and trees, live-tip checks, patch counts, bundle mode, applied trees, bundle trees, and ZIP identity.

The patch and bundle routes remain equivalent tree-preserving installation routes. The synthetic `git am` commit is not a producer or publication identity. A failed pin, patch, bundle, tree, or live-tip check stops delivery and remains visible for the next refresh.

The final F-final source refresh is isolated delivery staging: it retains fresh upstream additions while applying and verifying this delivery's patches against the refreshed sources. It does not merge later upstream into the frozen gating integration tuple. Other D68 packaging changes are outside this document.

D135 ZIP base note: For each repository, the patch base is the current upstream `main` at the D59 cut, after that upstream has been merged forward into that repository's `tl/integration`. Package only the exact D59 cut tuple. The Agent tip comes from that tuple's home integration (the current checkpoint begins `a30e`), never from the historical proof pin beginning `547e1045`. An unmerged tree, or an integration tree behind current upstream `main`, is not packageable. No D59 cut, delivery build, or ZIP has occurred; final identities and all gates remain **PENDING**.

## D65 owner release order and App manifest guard

The owner merges Runtime first, then Agent, then runs the one guarded App manifest command from the App root, and only then merges App:

```sh
node scripts/installer/update-manifest.mjs --runtime-checkout /path/to/owner-merged/runtime --agent-checkout /path/to/owner-merged/agent --write
```

Before that write, App's adopted `runtime.lock.json` must name the exact Runtime checkout `HEAD`. If it names an earlier Runtime, the supported App rebind is `node scripts/sync-runtime-client.mjs /path/to/owner-merged/runtime`, which delegates to `node scripts/vendor-lock.mjs update runtime.lock.json --producer /path/to/owner-merged/runtime`; do not replace this with a tag, release label, fabricated SHA, or direct lock edit. The actual [manifest updater](app/scripts/installer/update-manifest.mjs) (`scripts/installer/update-manifest.mjs:11-27,81-117`) validates the Runtime lock source and equality of Runtime `packages/typescript/src/contract-metadata.ts` with App `src/integrations/runtime/generated-contract-metadata.ts`, then updates `agent.sha`, `runtime.sha`, and `runtime.schema_digest` (`:119-150`). The supported rebind sources are [sync-runtime-client.mjs](app/scripts/sync-runtime-client.mjs) (`scripts/sync-runtime-client.mjs:7-30`) and [vendor-lock.mjs](app/scripts/vendor-lock.mjs) (`scripts/vendor-lock.mjs:45-105`).

Runtime is the only writer. All production callers use the v2 commit door described in [`contract/commit-v2.md`](../contract/commit-v2.md): the exact project/timeline scope and base revision/publication pair, nonempty commands, label, step metadata and patches, merge mode, declared reads, dry-run flag, source/rationale/group annotations, and the HTTP idempotency key. Existing permission refusals remain stopped. No new trust backend, Farm access, schema-source access, alternate writer, or force-conflict route is authorized.

## D72 retired CLI migration — owner update

### Timeline write-route migration

The delivery retires the native `edit commands-file`/native-batch ingress and
the other separate native/publish writers (`edit --native`, `apply --native`,
`undo --publication`, `publish`, `publish_bundle`, and the old three-way
writer). A document edit now uses `timelines commit --file ... --message ...
--idempotency-key ...`; the Runtime `commitTimeline` door owns accepted,
merged, conflict, and invalid replies, durable exact-key retry, and the
receipt/history. A single move or trim uses the current native `timelines edit
...` route. Cut-sheet edits use the current `timelines apply <sheet> ...` /
`NativeSheet` route, which emits registered commands through that same Runtime
door and preserves the draft on refusal. No native packet envelope,
commands-file alias, detached document overwrite, or resurrected G5 interface
is included.

The current Agent registry lists `commit`, `edit`, `apply`, `undo`, and `redo`, but not `publish`; use the live `python3 -m astrid timelines --help` output and [the current registry](agent/astrid/packs/timeline/cli.py#L3831-L3839), without restoring aliases or bypasses.

Supported current forms are: `timelines edit REF --project PROJECT ... --idempotency-key KEY` for literal moves/trims; `timelines apply REF SHEET --project PROJECT [--dry-run] [--idempotency-key KEY] [--json]`; `timelines undo REF --commit RECEIPT_ID ...` and the corresponding `redo` form; and `timelines commit REF --project PROJECT --file FILE -m MESSAGE --idempotency-key KEY [--dry-run] [--json]` for a detached JSON document. Current help has no `--native` apply option or `--publication` undo/redo option. `show --native --as sheet` remains a read/export projection whose sheet feeds `apply`. Python callers use `from astrid.sdk import timeline`, `timeline.open(...)`, then `tl.commit(..., merge="fields"|"atomic", dry_run=..., reads=..., idempotency_key=...)`; the commit wrapper preserves the bounded conflict/unknown-transport behavior ([commit_session.py](agent/astrid/sdk/timeline/commit_session.py#L163-L171)).

Runtime old save/CAS/document routes are refused with HTTP 410 through `_require_timeline_command`; the replacement is `POST /v1/projects/{project_id}/timelines/{timeline_id}/commit` (`commitTimeline`) with the exact base revision/publication pair and `Idempotency-Key` ([server.py](runtime/runtime_protocol/server.py#L522-L544), [service.py](runtime/runtime_protocol/service.py#L1653-L1666), [timeline_commit_store.py](runtime/runtime_protocol/timeline_commit_store.py#L337-L345)). Timeline create/rename/archive/recover remain supported metadata operations. Automatic relational timing—anchors and pinned markers—remains deferred; this update does not claim every deferred case passes. D72 protects replacement idempotency/conflict, clean-copy, and output behavior, not an unqualified final-tuple result; use the Agent family disposition rather than duplicating its classifier.

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

The final receipt must show the v2 reply shapes. A mutation request includes `api_version`, `project_id`, `timeline_id`, the exact `base_revision_id` / `base_publication_id` pair, ordered nonempty commands (`schema_version`, `op`, `version`, `select`, `args`, `created`), label, steps (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), `merge` (`fields` or `atomic`), request `reads`, `dry_run`, `source`, `rationale`, `group_id`, and the HTTP `Idempotency-Key`. `accepted` and `merged` include `data` and a full `receipt` with the canonical document, `digest`, `id_map`, authoritative commands, steps, dependencies, effects, base/previous/accepted pairs, versions, publisher, history, guarded undo, and `receipt_id`. A successful preview reports `would_status` and a null receipt. `conflict` includes its reason and head; `invalid` includes structured `code`, `path`, `hint`, and `suggested_command` details. Exact retries return the original durable reply without another history entry.

## Historical evidence and limits

Historical bounded evidence must remain labeled as historical and scoped to its original source tuple. Existing links include [the retained P1 actual-cause report](design/app-A2-P1-17985-actual-cause-sol-2017.md), [the retained integrated P4 symbol report](design/agent-F-P4-symbol-integrated-0023.md), and [the retained App P4/P5 registration report](design/app-F-P4-P5-registration-cumulative-0838.md). They are not final-tuple receipts and do not establish final GO.

The D54a known-gap rule is strict: each non-green node needs evidence identifying one category—environment/setup, upstream-identical/pre-existing, D52 deliberate deprecation with caller proof, or owner-deferred scope. A caused regression is fixed or reverted. No test of live behavior is weakened, skipped, deleted, or converted into a refusal expectation.

Under D62, Runtime does not prove a v2 producer's native coverage is complete at submit (Sol1422's 8 omission packets); such commits fail closed at fork/inverse use. This is the existing Runtime deletion-ledger row D62 ([`design/deletion-ledger.runtime.md`](design/deletion-ledger.runtime.md)), with BOARD-HEADER D62 as its decision source. It is post-delivery hardening, not a new final gate PASS.

Rendering/parity remains deferred. Relational timing remains deferred. The M5 extension-model rewrite remains deferred. Deferred relay, remote-provider, and provider-child scope remains fail-closed. These boundaries do not resurrect prior acceptance criteria or add delivery extras. The existing installed delivery builder is the production caller for the README template and gate-results input; a controlled four-repository stub render is only a documentation wiring check, not a build or qualification receipt.

D87 coverage is source evidence only: 24 retained selectors plus one separate checkout case are mapped with zero current promised capability gaps, and the other six checkout cases remain live. It does not establish functional PASS, and the historical P4 result is not a current 45-second PASS. The fresh-upstream packaging-only requirements at App `d11417a59` (including the `WelcomeConnection.test.tsx` overlap) and Agent `08e6b90511` (including the installer service/test overlap) remain in the final checklist; after applying that fresh-upstream result, run the full App suite and Agent installer service/tests.
Gate3 current companion selector `tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_gate3_reload_undo_and_visualize_report_unavailable` is deferred and remains a visible failure: the protected `parent/clip:card.on` word choice (`"again"` in line #2 +1f) still sources `occurrence:occ/clip:voice`, so Gate3's required `occurrence:occ` deletion has a protected word-choice/topology dependency; the current field/source remains unchanged, and the future semantic owner is Agent G3/R2. The three other transcript-bound companions remain separate and unmodified; no blanket word waiver applies.
fake-runtime contract: retired-write check now uses POST, because GET became a valid read

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
