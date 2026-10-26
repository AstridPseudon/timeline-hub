# Timeline v2.1 delivery, {{UTC}}

This ZIP is a delivery candidate for the `tl/integration` branch of each Timeline repository: agent, runtime, app, and composition. Each repository is carried in two forms: a git bundle of its integration history and one binary-capable patch series based on the pinned `origin/main` shown below. Nothing in this candidate has been pushed, and this candidate is not a release receipt. The final build uses the recorded D141 upstream cut bases and the frozen integration tuple; resulting build identities and verification receipts are still pending.

The patch series is based on the pinned `origin/main` commit and has the `tl/integration` tree. Its commit message lists the merged commits, one per line. Per-commit history is carried by the bundle.

The patch route is intentionally linearized: `git am` creates a synthetic commit, so its commit ID is not the source integration commit. The tree ID is the delivery identity. Do not report the synthetic patch commit as a producer or publication identity.

At build time, the patch series is applied with `git am` to a fresh repository holding only the pinned `origin/main`, and the resulting tree is compared with the immutable `tl/integration` tree. Every bundle is checked with `git bundle verify`, fetched, and compared with that same tree. The generated per-repository sections below are authoritative for the build that produced the README; final integration SHA, tree, and verification receipts remain pending until that build supplies them; the upstream cut bases are already recorded below.

D141 freezes the recorded upstream cut tips at 2026-10-25T23:42:41Z:

| Repository | Frozen upstream `main` base |
|---|---|
| Agent | `8b6ed2116fd1803d24b2be5bc08bd9490407fe4a` |
| Runtime | `fa9cd5464a8b37b02f971de375e56be846cd69e2` |
| App | `7ca61bb3280beca21d98a854af266a382f7ce5df` |
| Composition | `67b8aa3d0d6831d3e3504a340ff583c3da253707` |

Each lane makes the one final reviewed merge-forward to its recorded tip, then freezes integration for the cut. No further upstream chase or live-main refresh is part of F-final. These are recorded upstream bases, not final delivery integration identities. The complete four-repository delivery tuple and its authentic final receipts remain **PENDING**; individual recorded merge-forward heads do not themselves supply that receipt. The Farm `git apply --check` uses fresh upstream at these cut tips, with zero reverts; it does not select newer upstream tips.

D135 ZIP base note under D141: package only the recorded cut tuple after each integration includes its frozen upstream base. The D135 ancestor guard remains required. The Agent tip comes from the cut tuple’s home integration, never the historical proof pin beginning `547e1045` or an older checkpoint. An unmerged tree or one missing its recorded cut base is not packageable. Final integration identities, build verification and ZIP receipts remain **PENDING**.

## Contents

- `README.md`: this file.
- `bundles/<repo>.bundle`: git bundles of `tl/integration`. A ranged bundle holds only commits after `origin/main` and needs `origin/main` present. A full bundle holds all history and clones on its own.
- `patches/<repo>/*.patch`: the binary-capable linearized patch series from the pinned `origin/main` tree to `tl/integration`.
- `SHA256SUMS`: checksums of every other file in this ZIP.

## Delivery status

**PENDING.** The upstream cut bases are recorded above. Final acceptance receipts, ZIP identity, integration source tuple and trees, and cut-base verification results await authentic delivery receipts. The delivery owner must include those receipts before release.

## D141 morning cut (policy; receipts pending)

D141 sets the cut ship bar to P1, P3, P4, and P5 **GO**, plus the six passing P2 gestures. SWAP and Element are documented known gaps. The only permitted fixing gate is a zero per-ID regression result against pristine upstream (D54a) on the frozen cut tuple. Our own failures that the authentic cut-versus-pristine comparison proves are not regressions remain unchanged, visible, and listed by root-cause cluster. Nothing is skipped, xfailed, weakened, retired, or rewritten as a refusal expectation.

This is the settled policy, not a receipt. No passing cut, full-suite, REG0, or ZIP result is claimed here before authentic final receipts. The final per-ID REG/known-gap list is pending the actual cut full suites, pristine comparators, and their source-bound result diff.

## D65 owner release order

The owner performs this release sequence: (1) merge the Runtime patches; (2) merge the Agent patches; (3) from the owner App root, run the one guarded manifest update below against those owner-merged checkouts; then (4) merge App. The updater writes only the installer pins: it does not publish a release, invent a tag, or treat a worktree branch name as an identity.

Before the updater, App's adopted `runtime.lock.json` must have `source_commit` equal to the exact `HEAD` of `/path/to/owner-merged/runtime`. If the adopted lock still names an earlier Runtime, use the supported App vendor-rebind seam first, from the App root:

```sh
node scripts/sync-runtime-client.mjs /path/to/owner-merged/runtime
```

That seam delegates to `node scripts/vendor-lock.mjs update runtime.lock.json --producer /path/to/owner-merged/runtime` and regenerates the adopted Runtime bytes and lock hashes. It is the supported source rebind; do not bypass it with a tag, release label, fabricated SHA, or direct lock edit. The D65 manifest write then runs exactly once:

```sh
node scripts/installer/update-manifest.mjs --runtime-checkout /path/to/owner-merged/runtime --agent-checkout /path/to/owner-merged/agent --write
```

These paths and flags are the actual App [manifest updater](app/scripts/installer/update-manifest.mjs) (`scripts/installer/update-manifest.mjs:11-27`). Before writing, it reads the full Runtime and Agent `HEAD`s (`:81-89`), requires Runtime `HEAD == runtime.lock.json.source_commit` (`:92-112`), and requires the Runtime generated digest at `packages/typescript/src/contract-metadata.ts` to equal App's `src/integrations/runtime/generated-contract-metadata.ts` (`:113-117`). It then updates `agent.sha`, `runtime.sha`, and `runtime.schema_digest` (`:119-150`). The rebind seam is [sync-runtime-client.mjs](app/scripts/sync-runtime-client.mjs) (`scripts/sync-runtime-client.mjs:7-30`), delegating to [vendor-lock.mjs](app/scripts/vendor-lock.mjs) (`scripts/vendor-lock.mjs:45-105`).

The source contract is [`contract/commit-v2.md`](runtime/contract/commit-v2.md). Runtime is the only writer. App, Agent, CLI, Python, scripts, and sheets use the v2 commit door; there is no document-overwrite route, TypeScript executor, or force-conflict option. Existing permission refusals remain stopped. D140 assigns Farm the merged-cut ship-grade Agent child/core; Agent retains source ownership. D141 carries that Farm work on the critical path. These notes record that existing assignment and add no trust backend, source acquisition, or execution authorization.

## Retired CLI migration (D72 / G5 / R5)

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

The current Agent parser lists `commit`, `edit`, `apply`, `undo`, and `redo`, but not `publish`; see [the current command registry](agent/astrid/packs/timeline/cli.py#L3831-L3839) and the live help from `python3 -m astrid timelines --help`.

Use the supported forms below, according to the input already in hand:

- `python3 -m astrid timelines edit REF --project PROJECT ... --idempotency-key KEY` for the literal clip move/trim forms. Current `edit --help` says that literal moves and trims commit through the durable timeline session; other flags edit a detached working copy. The supported trim/move flags and their guarded dispatch are in [cli.py](agent/astrid/packs/timeline/cli.py#L3624-L3645) and [cli_native.py](agent/astrid/packs/timeline/cli_native.py#L176-L224).
- `python3 -m astrid timelines apply REF SHEET --project PROJECT [--dry-run] [--idempotency-key KEY] [--json]` for the current sheet path. `apply --help` has no `--native` option. The retained `show --native --as sheet` is read/export only; feed its sheet to `apply` (see [the retained projection](agent/astrid/packs/timeline/cli_native.py#L227-L238)).
- `python3 -m astrid timelines undo REF --commit RECEIPT_ID --project PROJECT [--dry-run] [--idempotency-key KEY]` and the corresponding `redo` form. Current help names `--commit RECEIPT_ID`: it reverses an accepted Runtime commit, while `redo --commit` reverses the accepted undo. There is no publication flag; the implementation dispatches these forms through the guarded commit path ([cli.py](agent/astrid/packs/timeline/cli.py#L3532-L3548)).
- `python3 -m astrid timelines commit REF --project PROJECT --file FILE -m MESSAGE --idempotency-key KEY [--dry-run] [--json]` for a detached JSON document. The parser requires the file, nonempty message, and idempotency key ([cli.py](agent/astrid/packs/timeline/cli.py#L3596-L3608)); it does not provide a separate publish command.
- Python callers use `from astrid.sdk import timeline`, `tl = timeline.open(PROJECT, TIMELINE)`, stage supported commands/helpers, then call `tl.commit(label_or_fn, merge="fields"|"atomic", dry_run=..., reads=..., idempotency_key=...)`. `Timeline.commit` permits bounded function re-evaluation only for an explicit conflict and retries an unknown transport outcome with the durable original request/key; see [commit_session.py](agent/astrid/sdk/timeline/commit_session.py#L163-L171) and [open()](agent/astrid/sdk/timeline/commit_session.py#L263-L280).

At the Runtime boundary, legacy timeline document/CAS and direct save routes are rejected with HTTP 410 through `_require_timeline_command`; their replacement is `POST /v1/projects/{project_id}/timelines/{timeline_id}/commit` (`commitTimeline`) with the exact base revision/publication pair, CAS/conflict handling, and `Idempotency-Key`. The route and refusal text are in [server.py](runtime/runtime_protocol/server.py#L522-L544) and [service.py](runtime/runtime_protocol/service.py#L1653-L1666); the accepted context checks the exact base pair and `commitTimeline` operation ([timeline_commit_store.py](runtime/runtime_protocol/timeline_commit_store.py#L337-L345)). Metadata remains separate and supported: timeline create (including the existing empty-shell adoption), rename, archive, and recover ([server.py](runtime/runtime_protocol/server.py#L524-L544), [service.py](runtime/runtime_protocol/service.py#L1697-L1763), [server.py](runtime/runtime_protocol/server.py#L657-L662)).

This migration does not change the v2 request/reply shape. The optional `HistoryEntry.recorder_abi` remains `1|2` (absent is the legacy ABI1 form). Automatic relational timing—anchors and pinned markers—remains deferred; these notes do not claim every deferred timing case passes. D72 protects the replacement path's idempotency, conflict/CAS, clean-copy, and output behavior; it does not turn a deferred or unqualified case into a final-tuple result. Use the Agent D72 family disposition and deletion ledger for test classification; this README does not duplicate that classifier.

## Summary

{{REPO_SUMMARY}}

Line counts come from `git diff --numstat --no-renames origin/main tl/integration`. A file counts as a test when a path segment is `tests`, `test`, `__tests__`, `e2e`, or `spec`, or its name is `test_*`, `*_test.py`, `*.test.*`, or `*.spec.*`. Everything else counts as non-test/product for this diff summary. These counts describe the delivery diff; they are not a qualification result.

## Applying

Start from a fresh clone or checkout whose local `origin/main` is exactly the commit listed in that repository’s generated section. Do not substitute a newer remote commit. Verify the pin before applying:

```sh
test "$(git rev-parse origin/main)" = "<pinned origin/main from this README>"
```

The per-repository sections are authoritative for the build that produced this README: they supply the pinned IDs, whether the bundle is ranged or full, the patch count, and the expected integration tree. The command examples require the values from those generated sections; `delivery-build` supplies the sections, not substitutions inside these examples. Use only the values for this build.

Use exactly one of these two equivalent routes for each repository:

- **Patches:** `git switch -c tl/integration origin/main`, then `git am /path/to/patches/<repo>/*.patch`. Verify that `git rev-parse HEAD^{tree}` equals the `tl/integration` tree listed in the repository section. The result has the same tree as `tl/integration`, but linearized history.
- **Bundle:** for a ranged bundle, run `git bundle verify /path/to/bundles/<repo>.bundle`, then `git fetch /path/to/bundles/<repo>.bundle tl/integration` and `git switch -c tl/integration FETCH_HEAD`; verify the fetched commit/tree against the section. For a full bundle, run `git bundle verify /path/to/bundles/<repo>.bundle` and `git clone -b tl/integration /path/to/bundles/<repo>.bundle <dir>`.

Replace `/path/to/` with the folder this ZIP was unpacked into.

Do not combine the routes on one checkout or force either route onto a newer base. If a pin, bundle verification, patch application, commit, or tree check fails, stop and retain the failure for disposition against the frozen cut tuple.

## The v2 commit door

Production callers use `POST /v1/projects/{project_id}/timelines/{timeline_id}/commit` (`commitTimeline`), with `api_version: 1` and the C0 v2 semantics. The HTTP `Idempotency-Key` is required for a mutation and is separate from its document base. The approved field definitions are in Runtime [`contract/commit-v2.md`](runtime/contract/commit-v2.md), [`timeline-commit.json`](runtime/contract/schemas/timeline-commit.json), [`edit-command.json`](runtime/contract/schemas/edit-command.json), and the referenced [`CommittedMutation` receipt](runtime/contract/openapi/workspace-v1.yaml).

The request body’s required fields are `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, and the nonempty ordered `commands` array. New App/Agent producers supply nonempty `label` and `steps`; compatibility omission normalizes the label to `Timeline edit` and synthesizes one provider-completed step. The other body fields are optional: `merge` (`fields` or `atomic`, default `fields`), `reads`, `dry_run` (default false), `source`, `rationale`, and `group_id`. `source` requires `via` (`cli`, `python`, `app`, `script`, or `sheet`) and optionally `detail`.

Each command requires `schema_version`, `op`, `version`, `select`, and `args`. Its optional fields are `resolved`, `expect`, `bindings`, `created`, `authorship`, `reads`, `selections`, `intent`, `rationale`, and `group_id`; caller recorder fields remain checked claims. `label` and `steps` belong to the request, not each command. Each requested step requires `id`, `label`, `intent`, `tags`, `command_ordinals`, and `patch`, with optional `reads`. Accepted steps have those fields plus optional provider-derived `dependencies`; caller-supplied step dependencies are invalid. Steps partition the commands into nonempty contiguous runs in execution order.

Commands execute in array order as one transaction, using registered semantic commands or `doc.patch`. Patches are id-addressed, carry previous-value checks, preserve ordered-list rules, and record authoritative effects. A request containing `doc.patch` with omitted request `reads` has effective `merge_mode: atomic` over its complete touched scopes; explicit `reads: []` does not erase captured or step-local dependencies. Accepted step patches and dependencies come from verified provider execution.

A successful mutation has the envelope `data` and non-null `receipt`. `data` requires `status`, `base_revision_id`, `base_publication_id`, `previous_revision_id`, `previous_publication_id`, `accepted_revision_id`, `rebased_onto`, `canonical_document`, `document_digest`, `commands`, `id_map`, `provider_version`, `compiler_version`, and `publisher`. Its other schema fields are `merge_mode`, `steps`, `source`, `label`, `rationale`, and `group_id`; C0 v2 results expose effective merge mode and complete authoritative steps and echo supplied annotations. New results use `accepted` at the requested base and `merged` for a disjoint landing head; `rebased_onto` is null for accepted or the landing `revision_id`/`publication_id` pair for merged. The schema also accepts historical `rebased` results; exact retries preserve the original durable spelling.

`canonical_document` contains `schema_version`, `project_id`, `timeline_id`, `parent_revision`, `shot_revisions`, `internal_timeline_revisions`, and `dependency_manifest`. Clients adopt the complete canonical closure, including the other party’s changes in a merged reply. The receipt’s exact fields are `receipt_id`, `command_kind`, `idempotency_key`, `request_hash`, `project_id`, `project_seq`, `event_ids`, `result`, and `created_at`. `receipt.result` equals the accepted `data`; `receipt.receipt_id` is the resulting publication ID. History separately exposes `records`, including authoritative command captures and step patches/dependencies used by guarded undo; these are not additional mutation-envelope or receipt fields.

Send a dry run with `dry_run: true` and a separate key. A successful dry run has `data.status: preview` and `receipt: null`. Preview data requires `status`, `would_status` (`accepted` or `merged`), `base_revision_id`, `base_publication_id`, `evaluated_head`, `canonical_document`, `document_digest`, `commands`, `id_map`, `provider_version`, and `compiler_version`; its other schema fields are `merge_mode` and `steps`. It exposes complete provider-derived steps and effective merge mode. Candidate IDs are provisional; preview accepts no write, persists no history or durable idempotency winner, and may evaluate a newer head on repetition.

Failures have exactly the outer fields `http_status`, `code`, `message`, and `details`, with no acceptance receipt. `details` requires `status`, `reason`, `base`, `current`, and `conflicts`; the additional structured diagnostic fields are `code`, `path`, `hint`, and `suggested_command`. `details.status` is `conflict`, `refused`, or `invalid`. A conflict returns 409, outer `code: conflict`, and the actual head pair in `details.current`; each `details.conflicts` entry has `kind`, `ref`, `path`, `base`, `theirs`, `ours`, and `choices`. A malformed/invalid-at-base request returns 422, outer `code: validation_error`, and `details.status: invalid`; `current` is null only before the authorized head can be loaded. Legacy refusals retain 409 and `details.status: refused`. A later-head guard failure is not an invalid-base diagnosis, and an invalid document is not a successful merge.

Committing after preview uses a new key and `dry_run: false`, repeats validation, and may conflict. An exact retry of a durable accepted mutation returns the original `data`/`receipt` without executing again or adding history. A changed body or principal under the same key is `idempotency_mismatch`, not a second edit. An unknown transport outcome retries the original request/key before deciding to reauthor; a successful preview has no durable accepted reply to replay.

## Final qualification

The D141 ship bar on the frozen cut tuple is P1/P3/P4/P5 GO plus the six passing P2 gestures. ZERO REG versus pristine is the sole fixing gate. Comparator-proven own nonREG failures in core or other suites stay unchanged, visibly failing, listed by root-cause cluster, and non-gating. All outcomes below are **PENDING** until authentic cut receipts arrive. Historical results do not establish a final GO.

| Proof | Final requirement | Venue / owner | Status |
|---|---|---|---|
| P1 | Real-document chain: split, trim the new ID, intervening Agent edit, lost acknowledgement, restart; accepted, merged, and refused replies all remain correct. | App service, with final Agent/Runtime/Composition tuple | **PENDING — D141 requires GO** |
| P2 | Core App editing gestures send commits through the door, preserve intended fields, reload, and undo; no old-route traffic. | App service; App owns the verdict | **PENDING — D141 requires six passing gestures** |
| P3 | Gate-5 journey on the v2 path, including exact retry, newer local work, restart/reload, undo, and zero legacy snapshot traffic. | App service; App owns the verdict and independent verdict review | **PENDING — D141 requires GO** |
| P4 | Agent CLI, Python, and sheet coverage: single edit, ten notes in one commit with per-step undo, conflict/re-run, and show/history readback. | Agent source lane / cut proof venue; App owns the cut verdicts | **PENDING — D141 requires GO** |
| P5 | Runtime acceptance carried forward: renderer-off save, commit-door authorization, crash/retry points, and changed payload under the same key. | Runtime service | **PENDING — D141 requires GO** |

Core qualification covers the end-state model: EditCommand, commit door, undo/redo, history, split/trim/move/placement/occurrence, show/sheet/visualize projections, the App save path, and the Agent editing runner, rebase, and inverse. **Core suites: PENDING.**

F-final is also **PENDING**. Runtime runs the existing delivery builder on main against the frozen D141 tuple, retaining the D135 ancestor guard. The production caller reads the installed README template and gate-results input; these private candidates require the later authorized reviewed installation at those inputs. A controlled four-repository `render_readme` stub checks documentation wiring only. D140 Farm owns the merged-cut ship-grade Agent child/core, including the D141 in-child import check and dry preflight; Agent retains source ownership. Runtime and App use their lane services, Composition’s final full suite runs on main, and App owns the cut P1/P2/P3/P4/P5 verdicts, including P2/P3 execution. Required authentic receipts include the full/pristine comparisons, source-bound per-ID REG diff, source SHAs, recorded upstream bases, integration trees, patch/bundle verification, Farm cut-tip `git apply --check` with zero reverts, and ZIP identity. The already recorded App `d11417a59` (`WelcomeConnection.test.tsx` overlap) and Agent `08e6b90511` (installer service/test overlap) packaging concerns remain checks within the frozen cut, with the App full-suite and Agent installer service/test evidence still required; they are not a new upstream refresh. No receipt is invented here.

The D87 coverage audit is source evidence only: its 24 retained selectors plus one separate checkout case are mapped with zero current promised capability gaps, while the other six checkout cases remain live. It does not promote D87 coverage to functional PASS or promote the historical P4 result to a current 45-second PASS.

Runtime's frozen D141 targeted join is not a substitute for the missing full/pristine and final-gate receipts.
Gate3 current companion selector `tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_gate3_reload_undo_and_visualize_report_unavailable` is deferred and remains a visible failure: the protected `parent/clip:card.on` word choice (`"again"` in line #2 +1f) still sources `occurrence:occ/clip:voice`, so Gate3's required `occurrence:occ` deletion has a protected word-choice/topology dependency; the current field/source remains unchanged, and the future semantic owner is Agent G3/R2. The three other transcript-bound companions remain separate and unmodified; no blanket word waiver applies.
D139a installed schema input: the approved test-child schema input is the authenticated installed `banodoco-timeline-schema==0.0.2` distribution. Its `direct_url.json` names the pinned ArtAgents commit `242f9c4306bf3b501222cb041a9eb246ef47bc85` at `packages/timeline-schema/python`. Its exact RECORD closure has 18 rows: 12 hashed rows plus these six named standard unhashed rows: `banodoco_timeline_schema-0.0.2.dist-info/RECORD`, `banodoco_timeline_schema/__pycache__/__init__.cpython-313.pyc`, `banodoco_timeline_schema/__pycache__/generated.cpython-313.pyc`, `banodoco_timeline_schema/__pycache__/materialize.cpython-313.pyc`, `banodoco_timeline_schema/__pycache__/theme.cpython-313.pyc`, and `banodoco_timeline_schema/__pycache__/validate.cpython-313.pyc`. This is an installed-distribution input, not a fresh source build. The pinned source-tree tie `75a5a697f630affee40632e500b3f5b704a9b834` is **UNAVAILABLE** because no genuine pinned object was held and no acquisition occurred. The D139a installed review `2314` records PASS_INSTALLED_CUSTODY for the exact reviewed maker (`fd83c9e2017f75fb0d76a2d633d4a63aed090df37c4d7417b03152e7a4fc22b5`, 111171 bytes), wrapper and checker. That receipt is custody-only: it does not establish normal hub publication, Farm receiving, child acceptance, core, render or release PASS. Those results remain unverified in this note; no new installation or acquisition is performed here.
fake-runtime contract: retired-write check now uses POST, because GET became a valid read
`A2 D141 REG: duplicate-shot-group retains the upstream two-read predicate; its test mock adds only the approved authenticated basis/display reader interface, with every original input/assertion unchanged and all 16 placement guards passing (protected review PASS; integrated-head journey reproof and final ZIP qualification remain downstream).`
P2 placement expectation updated to the D124 materialization contract.
App unit admission used a reformatted disk witness (DERIVED_DATA_PROJECTION_NOT_ORIGINAL_STDOUT) containing authentic retained disk readings, independently reviewed in 0600. The witness records derived data; original stdout and a continuous historical disk peak were not retained.

Historical bounded evidence may be consulted only at its recorded scope. For example, the historical P1 material is [the retained P1 actual-cause report](design/app-A2-P1-17985-actual-cause-sol-2017.md), P4 material is [the retained integrated P4 symbol report](design/agent-F-P4-symbol-integrated-0023.md), and P5 material is [the retained App P4/P5 registration report](design/app-F-P4-P5-registration-cumulative-0838.md). These links do not establish final-tuple proof or a final GO.

# D141 documented known gaps

**SWAP.** The independent D125 terminal packet `3250` is overall **NO-GO**: five original tails passed, two failed, and one was serially not run; the SWAP predicate expected accepted HTTP 200 but received the public `history_unavailable` result. The separate D130-held SWAP/WAL worker `1537` ended in an automatic classifier refusal, not a product assertion failure, and no retry or alternate qualification was attempted. SWAP is therefore a documented known gap; future proof is owed.

**Element.** Independent actual requests `32016` and `15200` both failed unchanged at the five-second `applied` status predicate. Their Runtime-bound lifecycles completed internally with HTTP 200 (32016: 21.740631 s handler / 13.780929 s provider; 15200: 19.557721 s handler / 12.290285 s provider), while App/provider/caller/browser outcomes remain **UNKNOWN**. The D112 waiter path is conditionally reachable, but its occurrence, duration, and causal attribution are unproved; no cause, fix, profile, or ETA is claimed. Element is therefore a documented known gap; future proof is owed.

## D141 current-cut failure disposition

The retained D134 root-cluster inventory is historical evidence only: 370 unique IDs, with 132 setup/expectation, 0 proved product, 212 UNKNOWN, 14 unverified current REG, and 12 prior UNKNOWN. Its retained log, XML/receipt/core-count gaps, and missing causal records remain exactly as recorded; the missing XML is not a current-cut finding and the historical UNKNOWN rows are not a current-cut nonREG assumption. The retained-log SHA-256 is `65def166348d4ffde949d530bff1a7bcba820ad674ca85b8ccc3e708c781ae8e`. The existing qualified root-cluster evidence remains the source for that historical map; it does not close any current-cut ID.

Until the actual full and pristine runs are compared, every current-cut failure classification and final per-ID REG/known-gap list is **PENDING**. Own failures remain unchanged and visible. A current-cut failure may be called nonREG only after the authentic D141 comparator proves it; no UNKNOWN is promoted to pre-existing, upstream-identical, or nonREG in advance.

D141 known gaps and holds are explicit: D130 records the SWAP D127 WAL-recovery safety stop as surfaced to the owner; the held source branch `tl/rt-P2-D127-WAL-sol-1537` remains unreviewed and unmerged; the related SWAP acceptance worker is stopped; and no retry, rephrase, machine transfer, alternate test route, or D112 rollback occurred. SWAP remains on its D112 safety hold; Element remains delayed, and the suspected D112 timeout is explicitly **UNPROVED**; D77 installed render is **NOTRUN**; original9/B022 remain **UNKNOWN** because the required evidence is missing. Gate3 and deferred relational timing remain deferred, not passed. Existing installation/platform limits, including the unavailable genuine D13 installed native tuple and its required source, environment, browser, media-tool, seven-key, and symlink-free bindings, remain visible environment limits rather than current functional results.

## Known gaps and deferred scope

D54a evidence distinguishes environment/setup, upstream-identical/pre-existing behavior, D52 deliberate deprecation with caller proof, and owner-deferred scope. D141 controls the cut: comparator-proven own nonREG failures stay unchanged, visible, listed by root-cause cluster, and non-gating. UNKNOWN is not nonREG. A caused regression is fixed or reverted. No live-behavior test is weakened, skipped, deleted, xfailed, or rewritten to expect a refusal.

Under D62, Runtime does not prove a v2 producer's native coverage is complete at submit (Sol1422's 8 omission packets); such commits fail closed at fork/inverse use. This is the existing Runtime deletion-ledger row D62 ([`design/deletion-ledger.runtime.md`](design/deletion-ledger.runtime.md)), with BOARD-HEADER D62 as its decision source. It is post-delivery hardening, not a new final gate PASS.

Rendering/parity remains deferred, including the unified renderer/viewing parity work. Relational timing (anchors and pinned markers), the M5 extension-model rewrite, push updates, proposals/watch, and the repo-structure decision remain deferred. The deferred relay and remote-provider scope stays fail-closed; no new authority backend or provider-child custody path is part of delivery. These deferrals do not add acceptance criteria or extras to P1–P5.

## Per repository

{{REPO_SECTIONS}}

## Gate receipts

{{GATE_RESULTS}}

# D13 installed native preflight (post-install check)

Run this only after a genuine, non-editable installed Agent/Runtime deployment and its real selected tool inputs exist. It is a check, not an installer or input-provisioning command. The current delivery environment does not provide this tuple; D13 is therefore a known, visible environment gap and is not a core-blocking result.

From the Agent source checkout, with the selected installed environment's Python:

```sh
<runtime-environment>/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight
```

The selector reads these required, non-empty environment variables. D13 supplies no defaults or optional names:

```text
ASTRID_D13_SOURCE_PROFILE
ASTRID_D13_EXPECTED_BINDINGS
ASTRID_NODE_EXECUTABLE
ASTRID_D13_NODE_SHA256
ASTRID_REMOTION_PROJECT_DIR
ASTRID_D13_REMOTION_LOCK_SHA256
ASTRID_REMOTION_BROWSER_EXECUTABLE
ASTRID_D13_BROWSER_SHA256
ASTRID_FFMPEG_EXECUTABLE
ASTRID_D13_FFMPEG_SHA256
ASTRID_FFPROBE_EXECUTABLE
ASTRID_D13_FFPROBE_SHA256
ASTRID_TEST_NODE_MODULES
```

`ASTRID_D13_EXPECTED_BINDINGS` must name a regular, non-symlink JSON file whose object has exactly these seven non-empty string keys—no missing or extra keys:

```json
{
  "agent_commit": "<full 40-hex Agent commit>",
  "agent_tree": "<full 40-hex Agent tree>",
  "agent_wheel": "<regular non-symlink Agent wheel path>",
  "agent_wheel_sha256": "<64-hex SHA-256>",
  "source_checkout": "<absolute symlink-free installed source root>",
  "source_digest": "<64-hex source_checkout_digest>",
  "runtime_environment": "<absolute symlink-free installed environment>"
}
```

`ASTRID_D13_SOURCE_PROFILE` must be a regular, non-symlink JSON file with exactly this existing four-field carrier (D13 rejects optional Runtime profile fields):

```json
{
  "profile": "astrid",
  "runtime_checkout": "<the same selected installed tree as source_checkout>",
  "source_checkout": "<the source_checkout binding>",
  "runtime_environment": "<the runtime_environment binding>"
}
```

The source and runtime checkout must be the same absolute, symlink-free installed tree; the environment must be an absolute, symlink-free directory containing a regular, non-symlink `bin/python`, and the pytest interpreter must resolve to that interpreter. The installed origin probe must find `host`, `child`, `action`, `client`, `sdk`, `runtime_protocol`, `runtime_protocol.platform`, and `astrid_runtime` wholly inside that selected tree, without source aliases or symlinks. The selected source's `astrid/packs` digest must equal `source_digest`; the wheel, its Git/source archive members, and installed RECORD/package bytes must also agree with the declared commit/tree and wheel hash.

Tool inputs must be genuine regular, non-symlink inputs matching their declared hashes: Node (`ASTRID_NODE_EXECUTABLE` + `ASTRID_D13_NODE_SHA256`); the Remotion project (`ASTRID_REMOTION_PROJECT_DIR`) with hashed `package-lock.json` (`ASTRID_D13_REMOTION_LOCK_SHA256`) and non-empty, regular, non-zero `public/fonts/*.woff2` plus `FONT_PROVENANCE.md`; the browser (`ASTRID_REMOTION_BROWSER_EXECUTABLE` + `ASTRID_D13_BROWSER_SHA256`); ffmpeg (`ASTRID_FFMPEG_EXECUTABLE` + `ASTRID_D13_FFMPEG_SHA256`); and ffprobe (`ASTRID_FFPROBE_EXECUTABLE` + `ASTRID_D13_FFPROBE_SHA256`). `ASTRID_TEST_NODE_MODULES` must be a genuine regular, non-symlink directory. No placeholder paths, fabricated hashes, copied credentials, or unacquired inputs satisfy this check.

The selector itself only performs this preflight and does not open Runtime or native tools. Runtime’s normal consumer separately accepts `--source-manifest` (or the `ASTRID_RUNTIME_SOURCE_MANIFEST` fallback) and loads/validates its source profile; that runtime variable is not a required input to this D13 selector.

## D141 final App unit disclosure (source-only)

The final App unit disclosure is a bounded documentary comparison, not an App or Main installation. The authentic current App source is `4de54db14bdc9ddc2ce2e5887258b03acbffd30d` / tree `84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`: registered full `app-full-1026060654-8638` exited 1 with 19,745 passed and 32 failed tests across four failed files, plus a separate module-level collection error; its chained Node phase was **NOTRUN**. Standalone Node `app-full-d141-node-phase-1026063009-19156` exited 1 with 296 passed, 2 failed, and 26 actual skipped tests (324 tests in 33 suites; 27 declared skip entries are distinct). The exact pristine d822 source is `d822d2f5d2bd05187b4ff5b6071c3e13945d4747` / tree `2af40a015057779ceb4e4b37cad62e1469aa7e36`: full `app-pin-d822d2f5-full-1026063854-17524` exited 1 with 17,866 passed and 18 failed tests across three failed files, with chained Node **NOTRUN**; standalone Node `app-pin-d822d2f5-full-d141-node-phase-1026072325-11111` exited 1 with 289 passed, 2 failed, and 26 actual skipped tests (317 tests in 33 suites; 27 declared skip entries are distinct). The independent finite comparison qualifies all 32 current full failure IDs as `OWN/N/A`: five files are absent upstream and 27 exact titles or predicates are absent from the present upstream file; no renamed equivalent was found, and the upstream-absent `genericPatch` collection file remains a separate collection error rather than a test ID. The two same-kind Node failures are independent `ssh-keygen ENOENT` failures at the retained callsites and source blobs, classified non-regression for that finite Node pair only. The current `82e9e13ddf1d7ec6c736521b2eb091dca9877598` / tree `6a6e49eb4461b5ca1a7fa1247653bc794f26d710` catch-up is separate applicability evidence and does not retarget the original `4de` measurements; its targeted 255 tests and both TypeScript checks passed, while exactly three inherited `AgentSetupCard` `react-hooks/exhaustive-deps` findings remain and no lint pass is claimed. The retained receipts use their own five-second sampled traces and 4,000,000,000-byte stop; they do not establish a continuous peak. This narrow App unit scope claims no global REG0, gate, ZIP, popup-not-reproduced, product, or final PASS; missing originals are reported at their exact retained paths/statuses rather than reconstructed, and the existing SWAP, Element, mock/placement, derived-witness, historical-receipt, placeholder, and C0 scopes remain unchanged. Main later owns one independent protected documentary check and the guarded two-document CAS; this source-only candidate is not a canonical install and an App inventory is not a Main inventory.


## D141ff popup ADD known gap (bounded documentary note)

D141ff records the popup ADD as a documented known gap on the frozen final tuple, alongside SWAP and Element. The genuine normal service result `app-pin-82e9e13d-full-d141-p2-popup-add-82e9e13d-submit-popup-retry-1-1026111307-27026` exited 1 in 207 s: readiness **PASS**, popup **FAIL**, because the `f2-occurrence-copy` shared-occurrence label was absent within 5 s. Cause: **UNKNOWN**. The retained original pointer is `app-pin-867cb273-d141-p2-popup-add-867cb273-submit-1026014140-1368`; this note does not reconstruct it.

The cancelled operational attempts `app-pin-82e9e13d-full-d141-p2-popup-add-82e9e13d-submit-1026102149-13234` and `app-pin-82e9e13d-full-d141-p2-popup-add-82e9e13d-submit-1026102155-20413` remain custody failures with no functional verdict and are not credited. Independent actual custody review remains pending unless its genuine published verdict arrives; neither source publication nor author receipts establish custodyPASS. The owner wording is: "failing since the freeze-1 upstream merge (4de era); cause under diagnosis".

This is our own non-REG P2 known gap and is non-blocking for ZIP. Diagnostic is **NOTRUN** and non-blocking; D141j permits it only after the six selectors and first four-field visibility proof. No diagnostic action is taken here. Final pins, installation, and build remain separately gated.


## D141gg parent move PASS accepted with first-tool trace gap (bounded documentary note)

Author result: the original qualified parent-move attempt used the exact four-repository tuple App `82e9e13ddf1d7ec6c736521b2eb091dca9877598` (tree `6a6e49eb4461b5ca1a7fa1247653bc794f26d710`), Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92` (tree `d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`), Runtime `95d98f038320d5d46bd679ac000ab3e15825c935` (tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`), and Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` (tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`). The paired preflight `app-pin-82e9e13d-full-d141-p2-parent-move-82e9e13d-submit-preflight-1026112242-25487` was PASS, exit 0. The original normal service result `app-pin-82e9e13d-full-d141-p2-parent-move-82e9e13d-submit-1026112312-16601` was PASS, exit 0 in 237 s.

The author result records D28 mounted readiness PASS and the original `P2 mounted single parent move: v2 commit, exact field delta, reload and guarded Undo` predicate PASS. The service body is therefore a bounded parent-move PASS: one readiness check and one parent-move journey passed. Native submit session `59630` exited 0 and was reaped; the same normal result was waited through session `51172`, which exited 0 and was reaped. The author's 72-sample trace genuinely covers the service body, but not the worker's first-tool window.

Independent custody result: publication `app-D141cc-parent-custody-publication-1135.json` remains `FAIL_CUSTODY_NATIVE_TEST_PASS`, with review verdict `FAIL_CUSTODY` and finding F-001. The first sampler command failed because `mkdir .../tmpdir` found a regular file, so no trace was written by that first tool. The later 72 samples are genuine and cover the whole body, but the first-tool window before the sampler started is uncovered and cannot be backfilled. This is not custodyPASS and is not a whole-worker trace; no retry or reproof is claimed.

Main disposition: BOARD-HEADER D141gg at 11:35 accepts the parent-move PASS with this trace gap disclosed and calls for no re-proof. That disposition keeps the author service result, the independent custody failure, and the disclosed first-tool limit distinct. It makes no final-build, REG0, ZIP, or other selector claim.


## D141hh single PASS accepted with both procedural gaps (bounded documentary note)

Main D141hh at 12:00 accepts the author result for the exact four-repository tuple App `82e9e13ddf1d7ec6c736521b2eb091dca9877598` (tree `6a6e49eb4461b5ca1a7fa1247653bc794f26d710`), Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92` (tree `d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`), Runtime `95d98f038320d5d46bd679ac000ab3e15825c935` (tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`), and Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` (tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`); preflight `app-pin-82e9e13d-full-d141-p2-transition-none-single-82e9e13d-submit-single-scope-2-preflight-1026114656-9320` PASS/exit 0 and normal `app-pin-82e9e13d-full-d141-p2-transition-none-single-82e9e13d-submit-single-scope-2-1026114726-24271` PASS/exit 0 in 257 s, with D28 mounted readiness and the exact P2 mounted transition-None single predicate PASS. The accepted service PASS retains both procedural gaps: the raw KEEP was added prospectively at `2026-10-26T11:49:29.082850+00:00` after the request/body window, and only the future output, plan, lock, stdout and stderr paths were relocated; the custody review found no product-affecting deviation and the raw evidence is intact. Independent custody remains `FAIL_CUSTODY` with CUSTODY-RAW-KEEP and CUSTODY-RECIPE-PATH, so the author result, custody findings and Main disposition remain distinct; this is not a custody PASS. The original first single no-body attempt from 1135 remains NOTRUN, was not retargeted or reproofed, and is not claimed repaired; D141hh-a TEST_KEEP applies to future submits only and does not backfill historical custody. Native custody recorded 54 samples (`5029826560`–`5477560320` bytes, maximum gap 5.006048 s, no 4 GB stop); author sampling is session-only (158 samples, `5029302272`–`5479276544` bytes). Main accepts this bounded service PASS with both gaps disclosed and no reproof, and makes no final REG0, build, ZIP or selector claim.
