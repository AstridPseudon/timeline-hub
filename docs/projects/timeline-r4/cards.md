# r4 cards (rework 15 Oct)

Current scope reconciliation: [Astra20 compiler-cycle exception and authenticated grant-session integration](amendments/20261015-compiler-cycle-and-grant-session.md). Original card identities, criteria, routes, estimates and acceptance dependencies below remain; COMPILER's behavior-preservation exclusion has only the expressly required cycle-refusal exception recorded there.

Latest scope amendment: [Release 3 kinds restored](amendments/r4-release3-extension-kinds-restored.md); [integration record](amendment-integration.md).

Latest scope amendment: [Release 3 kinds restored](amendments/r4-release3-extension-kinds-restored.md); [integration record](amendment-integration.md).

Execution authority: [run.yaml](run.yaml) and the current [orchestrator goal](agent_goal.md) govern models, stages, custody and escalation. Historical names do not launch agents or override them.

One card = one executor, one mergeable piece, at most 3 human-days. A card is done when its implementation and bounded checks are merged: its "Done when" passes on `timeline-r4/trunk`, plus its affected tests. Film-level proof (the real-film journey, full suites, parity, replays, measurements) is never in a card's "Done when": it belongs to the named integration points and the release acceptance cards (testing.md, RELEASE-1, FINAL-R3).

**Difficulty labels** follow the user's box 2 and the rubric ([archived boxes](review-20261015/00-boxes.md), [difficulty rubric](review-20261015/difficulty-rubric.md), [classification](review-20261015/difficulty-classification.md)). A card is `xhard` if it crosses repos or contracts, changes a load-bearing invariant (timing, identity, save/commit, migration, security) or risks silent data loss, **even if its tests are strong**: tests reduce the risk, they don't change the nature of the work. Otherwise the rubric's question decides: `normal` when the card's own checks and the existing tests catch a literal-minded worker's subtle mistake, `xhard` when they may not. The manager reads the diff of an xhard card. A `**Why xhard:**` line appears only on xhard cards.

Sources: [review-20261015/](review-20261015/) (decisions.md, the reviews and the drafts).

Drafted 15 Oct from `decisions.md` (including "Changes from the Opus premise review"), checked against the r4 base: the four repos in the "Base and trunk" table of `agent_goal.md` (GitHub branch `claude/fork-base-20261015`; Astrid a046263f). Old-card text: `${HISTORICAL_CONTROL_RUN_ROOT}` (GATES.md, WS-HARDEN.md, WS-SAVE.md) and `projects/{A,B,C}*/tasklist.md`.

Path shorthand: **Astrid** (`A/`), **Runtime** (`R/`), **App** (`P/`) and **composition** (`T/`, our fork of the timeline composition) are the four repos at the r4 base, as listed (GitHub URL, branch, SHA, local checkout) in the "Base and trunk" table of `agent_goal.md`; paths are relative to each repo's root. **Checkpoint** = `astrid-local/checkpoint-20261013` (our checkpoint line; not on the base).

---

## A: Integration

### BASE: pin the base, inventory it, record the baseline
`A · R1 · 2 d · normal · produces A#base (= A#base-pinned)` · replaces SPEC-0 (CARRY is done by the port)
**Goal:** The three combined branches are tagged and become trunk, and we know exactly what is on them, what is missing and what already fails.
**Done when:**
1. In all four repos the tag `timeline-r4/base-20261015` and the branch `timeline-r4/trunk` match the base table in `agent_goal.md` (GitHub branch `claude/fork-base-20261015` and its SHAs), and a fresh clone of each pushed GitHub branch has the same SHA (the composition's is not pushed yet; pushing needs the user's go). The live Runtime's port and root are written down. The base never moves.
2. Recorded in one file: the effective renderer closure (Astrid `remotion/package.json` pins composition v0.0.6 and Remotion 4.0.509; the App vendors composition 0.0.2 with Remotion 4.0.503; the film needs our fork v0.0.7 at `astrid-local/timeline-composition`) and the exact v8 identity.
3. The baseline failure list for Astrid, Runtime and App is recorded as a list of test ids, not a pass claim. This includes the two "PARKED WIP (unreviewed, untested)" commits (`061d1f6e`, `4ea29d38`) with a keep or revert call on each, backed by evidence recorded with its SHA: that commit's own tests run on trunk, or a review verdict. A call without evidence does not count.
4. The commit-service mount is decided and written in the card result: a Runtime route owned by ACCEPT (the App's `/api/astrid/*` already goes through the Runtime proxy).
5. Parity: uses FEATURE-PARITY's inventory; the base-vs-live diff it produces has no unexplained gap (tonight's five losses are already restored on trunk).
**Start from:** Astrid `astrid/packs/timeline/cli_parser.py`, `astrid/sdk/__init__.py`, `tests/test_cli_registration_conformance.py` (the existing registration checks); Astrid `remotion/package.json`; App `package.json`, `config/vite/astridBridgeProxy.ts`, `scripts/dev-local-workspace.mjs`; port reports in `production/review/optimization/port/`.
**Not in scope:** fixing failing tests (GREEN); porting the checkpoint line (CHECKPOINT-ASTRID, CHECKPOINT-RUNTIME); changing any pin (PINS-ASTRID, PINS-APP); building the mount (ACCEPT).
**Depends on:** A#feature-parity.

### FEATURE-PARITY: nothing that works today leaves without a written line
`A · R1 (wave 0) · 1 d · normal · produces A#feature-parity` · new (opus-feature-parity §4)
**Goal:** A feature that works today cannot leave the trunk without a line saying which card removed it and why.
**Done when:**
1. `tools/parity/inventory.py` writes `tests/parity/inventory.json`, generated from the code: `timelines` verbs and flags (with `required`/`choices`), public SDK names and signatures (`Checkout`, `Clip`, `Cut`, `Voice`, `StepSequence`, `Look`), check/lint finding codes, visualize presets, views and layers, render flags. Running it twice gives identical bytes.
2. `tests/parity/test_parity.py` fails on a planted removal (delete `--hold` from the parser) and on a planted broken best-effort import (the DAMAGED-ART class), and passes once the matching `tests/parity/removed.yaml` line (`{feature, card, reason, alias}`) is added; an alias that doesn't parse fails too. A line for an inventory entry that leaves with no `alias`, other than item 4's, also needs `approved: user <date>`, and the test fails without it: dropping a capability needs the user's approval, which the orchestrator escalates.
3. The inventory generated on the live line (`fix/v9-trial-tools`) and on trunk is diffed; every live entry missing on trunk is restored or has a `removed.yaml` line.
4. `removed.yaml` starts with r4's deliberate changes and their cards (`--set null` → `--clear`, `--remove` on a picture → `lift`, the opacity fix, `inverses.py`, stale draft expiry).
5. It runs in seconds, in every card's affected tests and at every GATE merge.
**Start from:** the generator scripts in `opus-feature-parity.md` Appendix A; Astrid `astrid/packs/timeline/cli.py` (`build_parser`, `COMMANDS`), `astrid/sdk/__init__.py` (~44-68), `astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py`, `layers/builtin_checks.py`, `astrid/sdk/timeline/check.py`.
**Not in scope:** testing what a flag does (the existing tests do that); App UI snapshots; Runtime route tests.
**Depends on:** none.

### CHECKPOINT-ASTRID: bring the checkpoint line's Astrid work onto trunk
`A · R1 · 1.5 d · normal · produces A#checkpoint-astrid` · split from CHECKPOINT-ASTRID + CHECKPOINT-RUNTIME (the Astrid half)
**Goal:** Everything our checkpoint line has in Astrid that the base lacks, including the real-film journey, is either on trunk, with tests, or deliberately dropped with a reason.
**Done when:**
1. Every non-merge Astrid commit of `video/checkpoint-20261013` not on the base (41) is listed as present, equivalent, ported or dropped, with the SHA and a reason for each drop.
2. Ported to Codex's structure on trunk, each with its test: the real-film journey (`astrid/core/dev/journey.py`, its fixes `eae016a4`, `d8863255`, `f79541a3`, `docs/development/journeys.md`, `tests/journeys/`), render `--range`, process-group reaping in tests (`04fc3727`).
3. Features already on the base by another route (e.g. `am-pixel-shape`) are marked equivalent, with the path.
4. The parity inventory from BASE has no new "missing" entry after the port.
5. `astrid-tools dev journey --help` runs on trunk.
**Start from:** Checkpoint `Astrid/astrid/core/dev/journey.py` (394 lines), `Astrid/tests/journeys/`, `Astrid/docs/development/journeys.md`; Astrid `astrid/core/gateway/dispatch.py` and `dev_operator.py` (where `dev` verbs register).
**Not in scope:** the Runtime commits, schema v28/v29, W3b replay identity and the upgraded realm clone (CHECKPOINT-RUNTIME); wiring the journey to a stack and the load-honest verdicts (GATE); the composition pin (PINS-ASTRID); copying code over Codex's re-architected structure.
**Depends on:** A#base.

### CHECKPOINT-RUNTIME: bring the checkpoint line's Runtime schema and replay identity onto trunk
`A · R1 · 1 d · xhard · produces A#checkpoint` · split from CHECKPOINT-ASTRID + CHECKPOINT-RUNTIME (the Runtime half)
**Goal:** Everything our checkpoint line has in the Runtime that the base lacks is either on trunk, with tests, or deliberately dropped with a reason, and the film's data upgrades through it unharmed.
**Done when:**
1. Every non-merge Runtime commit of `video/checkpoint-20261013` not on the base (18) is listed as present, equivalent, ported or dropped, with the SHA and a reason for each drop.
2. Ported to Codex's structure on trunk, each with its test: W3b replay identity ("join identical in-flight work, new task after failure", Runtime `feee7b3`) and Runtime schema v28 and v29 (specs by reference; the base is at v27).
3. The Runtime upgrade chain reaches the checkpoint schema.
4. The film's reference data is an APFS clone of the live film realm, upgraded through that chain; GATE, GOLDEN's frame half and REPLAYS use it.
5. The upgrade preserves the data, not only the version number: GOLDEN's document compare (compiled-document bytes, the 45 exact cut rows, the intent reads) passes on the upgraded clone exactly as on an unmigrated duplicate, and the live realm is never touched: a digest of its database and file listing, and their mtimes, are equal before and after.
**Start from:** Runtime `runtime_protocol/upgrade.py`, `runtime_protocol/canonical_schema.py`; the checkpoint specs for v28 and v29; the GOLDEN tool.
**Not in scope:** the Astrid commits and the journey (CHECKPOINT-ASTRID); wiring the journey to a stack (GATE); copying code over Codex's re-architected structure.
**Depends on:** A#base, A#golden-baseline.
**Why xhard:** ports Runtime schema v28/v29 (the base is at 27) and W3b replay identity onto a re-architected base; a wrong port or upgrade silently loses film data, and only the golden compare on the upgraded clone shows it.

### GREEN: suites green, xfails audited
`A · R1 · 2 d · normal · produces A#green` · replaces GATE-GREEN
**Goal:** A gate can read failures, not diffs, because the Astrid, Runtime and App suites are green apart from a short, owned quarantine list.
**Done when:**
1. Every baseline failure from BASE is fixed, deleted as obsolete, or quarantined. At most 10 quarantines, each with owner and expiry date.
2. Every xfail in both Python suites is live (with a reason) or removed. No fixed bug is still marked as expected-failure (four stale xfails hid a fixed bug on 15 Oct).
3. `make doc-refs` exists (a Makefile target running `scripts/reshape/check_doc_references.py`) and passes (about 80 examples omitted `kind=`).
4. The manifest-defaults test covers every action and passes. No test passes on zero matches.
5. If the measured failure count is far beyond about 50, the card says so and is split by repo before work starts.
6. Parity: a test is deleted as obsolete only with a `removed.yaml` line naming its feature; tests added by tonight's port and wave 2 are never obsolete.
7. No test is fixed by weakening it: a scan of the card's diff to test files flags every removed or commented-out assertion, every widened tolerance and every added skip, and each hit has a one-line justification in the PR that a reviewer has read. An unjustified hit fails the card.
**Start from:** Runtime `tests/test_i06_composed_proof.py` (imports a missing `source.runtime`); Astrid `tests/test_result_manifest.py`, `tests/packs/test_pack_yaml_schema.py`, `scripts/reshape/check_doc_references.py`, `Makefile`.
**Not in scope:** fixing real product bugs found on the way (route them to their cards); new tests beyond the named checks.
**Depends on:** A#base.

### X0-EDITOR: record the main editor's save paths
`A · R1 · 1.5 d · normal · produces A#x0-editor` · replaces X0 (main-editor half)
**Goal:** Every way the main editor saves has a recorded payload and an exact-reload oracle, so preservation and save work design against real data.
**Done when:**
1. Fixtures `tests/fixtures/app_payloads/x0-<case>-editor.json` exist for X0 cases 1-6 and 10-13 of WS-SAVE §5 (tier a), each with provenance, the B0-B6 capture points that apply, and the oracle (`status`, `expected_changes`, `must_preserve`, `must_remove`, `exact_reload`).
2. The README has one row per case for this provider: `captured` (with reload evidence), `known_failure` (with reproducible evidence), `unsupported` or `missing` (owner and next action). Nothing is inferred.
3. Each captured fixture replays on a disposable Runtime and matches its oracle. The disposable stack is built with `scripts/local_install.py`; no live realm is touched.
4. The README names the driver used, lists the writer entry points found, ranks the preservation failures, and lists which gestures already carry touched ids and intended values.
5. Time box: stop at 1.5 d and report the gaps; do not stretch.
**Start from:** App `src/tools/video-editor/contexts/VideoEditorProvider.tsx`, `contexts/editorRuntimeAssembly.tsx`, `hooks/useTimelineCommit.ts`, `hooks/useTimelinePersistence.ts`, `lib/serialize.ts`, `src/integrations/runtime/dataProvider.ts`; Astrid `scripts/local_install.py`.
**Not in scope:** repairs (PRES-REPAIRS); the shot popup (X0-POPUP); tier-b cases (7-9, 14-16), which their producing cards add; any change to App code.
**Depends on:** A#base.
**Design detail:** `briefs/WS-SAVE.md` §5 and the X0 card in §6.

### X0-POPUP: record the shot popup's save paths
`A · R1 · 1.25 d · normal · produces A#x0-popup` · replaces X0 (popup half)
**Goal:** The shot-popup provider's saves are recorded the same way, and one coverage matrix shows both providers.
**Done when:**
1. Fixtures `tests/fixtures/app_payloads/x0-<case>-popup.json` exist for the tier-a cases the popup supports, with the same oracle fields as X0-EDITOR.
2. `tests/fixtures/app_payloads/README.md` has the coverage matrix for both providers: one row per case and provider pair, each `captured`, `known_failure`, `unsupported` or `missing`. It lists which collections each provider lists completely (the future `scope.complete`).
3. Each captured popup fixture replays on a disposable Runtime and matches its oracle.
4. Each collection marked complete has evidence: a fixture in which the provider has an item the editor shows and the provider's listing omits it, or a recorded reason none can exist. A collection without that evidence is marked not complete. A wrong "complete" later turns an omission into a deletion.
**Start from:** App `src/tools/travel-between-images/components/shotTimelineDataProvider.ts`, `src/integrations/runtime/dataProvider.ts`; the fixture format from X0-EDITOR.
**Not in scope:** the main editor (X0-EDITOR); repairs; popup tier-b cases (8, 9, 14).
**Depends on:** A#base, A#x0-editor.

### GOLDEN: the v8 identity tool
`A · R1 · 1 d · normal · produces A#golden-baseline` · replaces MIG-GOLDEN
**Goal:** One tool records the film's identity and later proves that a compiled document, and separately the rendered frames and audio, are unchanged.
**Done when:**
1. `golden baseline` and `golden compare` run on an unmigrated duplicate of the film and pass. The compare covers compiled-document bytes, the 45 exact cut rows and the intent reads; it runs in seconds.
2. A planted 1-frame change, a planted gain change, a planted change in one cut row, a planted change in an intent read and a planted change in an `app` field each fail the compare.
3. The decoded-frame and audio compare is built and recorded against the base renderer closure, and exercised once before the card closes on a small fixture render: it passes unchanged and fails on a planted frame change and a planted gain change. It is not run per card; IP1 runs it on the v8 film once the composition pin lands. Its cost (disk at least 8 GiB, serial, through the compatible shared lease (source-custody.md)) is recorded in the card.
4. It keeps `app.astrid_render_clock` and never strips all of `app`.
**Start from:** Astrid `tests/test_compiler_golden.py`, `tests/sdk/test_timeline_reflow_golden.py`, `astrid/core/timeline/duration.py`; the v8/head references recorded by BASE.
**Not in scope:** the compiler itself (F); changing the film; running frame compares per card; running the frame and audio compare on the v8 film (IP1).
**Depends on:** A#base.

### GATE: the real-film journey as a merge gate
`A · R1 · 2 d · normal · produces A#gate`
**Goal:** Each integration point opens with a bounded real-film smoke whose every phase reports observed success, observed failure, or "not observed" when its deadline passes first.
**Done when:**
1. The ported journey runs against a throwaway App + Runtime + Astrid stack stood up by `scripts/local_install.py`, on a clone of the live film realm, in 5 minutes or less on a quiet machine.
2. Each phase reports one of three outcomes: observed success; observed failure (a failure seen before the deadline stays a failure, whatever the load); or "not observed (deadline N s reached)" with load, swap and free disk.
3. Controlled subprocess fixtures test each outcome: one that succeeds, one that fails before its deadline, and one still running at its deadline, which is stopped and reported "not observed".
4. A failed run keeps its Runtime and host log tails.
5. A scenario registry exists and the bounded smoke opens each named integration point (testing.md); producing cards add their own GATE scenario to it. This card adds none.
**Start from:** the journey ported by CHECKPOINT-ASTRID (`astrid/core/dev/journey.py` on trunk); Astrid `scripts/local_install.py`, `tests/stage1/test_final_cold_launch_matrix_luna.py`, `docs/testing/astrid-final-cold-launch-matrix.md`.
**Not in scope:** any scenario's content; per-card journeys; a new stack launcher; synthetic-load test apparatus.
**Depends on:** A#base, A#checkpoint-astrid, A#checkpoint.

### CONTRACT-COMMIT: freeze the commit contract
`A · R1 · 2 d · xhard · produces A#contract-commit` · replaces C-FREEZE (commit half)
**Goal:** The commit request and result, its HTTP errors and the Runtime acceptance interface have one frozen definition that Astrid, the Runtime and the App generate from.
**Done when:**
1. CommitRequest, CommitResult, the HTTP errors and the Runtime acceptance interface (WS-SAVE §3.3-3.6) are in the Runtime's OpenAPI contract and schemas, with Python types generated for Astrid's client and TypeScript types for the App, and valid and invalid fixtures in the Runtime's `conformance/fixtures`.
2. No new `schemas/` tree in Astrid and no scene-plan or extension-manifest schemas in the Runtime OpenAPI contract. This does not prohibit the already-selected pack-v3 manifest admission/schema path for declared extension document kinds and owner namespaces; see the Astra098 supplement.
3. The App's suffix route is in the frozen contract: a commit request with `dry_run: true`, on the same Runtime route ACCEPT owns, rebases the given commands onto the head and returns the rebased, uncommitted commands or the conflict, storing nothing. After a network failure the App retries the dry run (it has no effect) and keeps the suffix in its recovery draft; the later commit retries under its original request id. Valid and invalid fixtures cover both outcomes.
4. One independent review call reviews the contract against the invariants: absent vs clear, `complete`, opaque fields, exact identity and retry, occurrence scope, timing units, the security boundary, the dry-run rebase. The verdict is recorded; findings are fixed or carded.
5. A generated-code check fails if the OpenAPI and the generated Python or TypeScript drift.
**Start from:** Runtime `contract/openapi/workspace-v1.yaml`, `contract/schemas/shot-composition.json`, `conformance/fixtures/`, `generators/generate.py`; Astrid `banodoco_workspace_client/generated.py`; App `src/integrations/runtime/generated.ts`.
**Not in scope:** implementing acceptance (ACCEPT) or the commit service (COMMIT); EditCommand (CONTRACT-COMMAND); a fake for every contract.
**Depends on:** A#base, A#x0-editor.
**Why xhard:** Rule 1: a frozen cross-repo contract encoding retry identity, absent vs clear, and the security boundary; its invariants are checked only by a configured review.
**Design detail:** `briefs/WS-SAVE.md` §3.

### CONTRACT-COMMAND: freeze the EditCommand format and the shared timing fixtures
`A · R1 · 2 d · xhard · produces A#contract-command` · replaces C-FREEZE (EditCommand half) and CONFORM
**Goal:** The EditCommand format is frozen with shared request/result and timing fixtures, and each repo proves only its own part against them.
**Done when:**
1. EditCommand is Astrid's draft `schemas/change-contract/opcall.schema.json` (OpCall) evolved, not a new vocabulary. Shared request/result fixtures and timing fixtures (anchors to frames, `_js_round`, clock conversions) live in the Runtime's `conformance/fixtures/`.
2. Each consumer proves its own part: Astrid parses the commands and its timing maths gives the fixture frames (both `_js_round` copies, `astrid/core/timeline/duration.py` and `astrid/packs/rendering/shared/rendering_backend/__init__.py`, are covered); the App's `src/tools/video-editor/commands/types.ts` validates and adapts the commands and its frame conversions give the same frames; the Runtime validates the commands and preserves them byte for byte. The Runtime gains no timing or rebase code.
3. A planted one-frame change fails the timing check in Astrid and the App; a planted one-field change fails validation in all three.
4. Parity: only the EditCommand envelope is frozen; the handler set stays open (registry). Every `edit` flag in the parity inventory has a row in a flag → handler fixture before the freeze.
**Start from:** Astrid `schemas/change-contract/{opcall,plan,patch,journal-record}.schema.json`, `tests/editing_conformance/runner.py`; App `src/tools/video-editor/commands/types.ts`, `commands/runner.ts`; Runtime `conformance/fixtures/`.
**Not in scope:** the runner implementation (D RUNNER); the apply/inverse/rebase round trip (REBASE); scene-plan fixtures; any new timing engine.
**Depends on:** A#contract-commit.
**Why xhard:** freezes the EditCommand envelope that Astrid, the Runtime and the App all consume; a wrong freeze propagates silently into every producer and consumer.

### REPLAYS: the v9 and v11 re-flows as GATE scenarios
`A · R1 · 1.5 d · normal · produces A#replays` · replaces the replay half of E-1
**Goal:** The v9 and v11 structural re-flows are scripted as two GATE scenarios, using only documented tools, so IP6 can prove them on a duplicate of the film.
**Done when:**
1. The v9 scenario, on a duplicate: re-flow `production/script/vo-v8.json` to `vo-v9.json` and reproduce `v9-vision-trial`; it passes only if the orphans are resolved in 3 commands or fewer with no intent edited by hand.
2. The v11 scenario, at 23a6a4f8: re-flow `vo-v9.json` to `vo-v11.json` (18 new takes, 8 lines removed, the vision/not-ready restructure) and reproduce 15eac948; it passes only if the orphans are resolved in 10 commands or fewer.
3. Both scenarios also check: a word-anchor diff (each moment's bound word, before and after) with zero unexpected entries, any entry reported as a choice; one music bed with listed seams and unique ids; the result matches cut by cut, or each difference is a reported choice.
4. Each scenario runs once through the lease (the new-scenario rule) and its result is recorded; a planted failure (an intent edited by hand, a moved word anchor) makes it report "failed". A red result becomes cards for the owning projects; the replays passing is IP6's condition, not this card's.
**Start from:** `production/script/vo-v8.json`, `vo-v9.json`, `vo-v11.json`; Astrid `astrid/sdk/timeline/reflow.py`; the journey scenario registry from GATE.
**Not in scope:** changing the film or any tool (route stumbles to cards); per-card replays; on-screen copy that quotes the script (COPY-SYNC, R2).
**Depends on:** D#rehome, D#add-layer, F#compiler, F#timing-fixes, F#music-segments, F#cuts, G#change-view, A#gate.

### PRACTICE: fresh agents use only the skill
`A · R1 · 1.25 d · normal · produces A#practice` · replaces the measurement half of E-1
**Goal:** We know where fresh agents stumble on the documented tools, and every stumble is routed to a card.
**Done when:**
1. Up to 3 fresh agents at a time, in a worktree at the served commit, use only the skill to do the practice tickets (L9-L13 and X1/X2 where expressible; R2 features graded "not yet").
2. `ROUND-2.md` has the metrics and each stumble routed to a card or a deliberate "won't fix".
3. Nothing is gated on the result.
4. Three metrics recorded: doc lines read before the first correct edit; hits on dead hints (target 0); commands per ticket against Round 1.
**Start from:** Astrid `astrid/packs/rendering/docs/SKILL.md`; the practice tickets under `production/review/optimization/`.
**Not in scope:** fixing the stumbles; acceptance; replays (REPLAYS).
**Depends on:** D#skill.

### SEC-MATRIX: the security canaries
`A · R1 · 1.5 d · xhard · produces A#sec-matrix`
**Goal:** Each security boundary fails the attack it is meant to stop, on a disposable fixture.
**Done when:**
1. Each of SEC-1 to SEC-5 (spec-hardening §6) has a canary that fails at its enforced boundary on the paired relay: files and credentials outside the grant, unapproved egress, a deceptive tool title, an MCP-config widening, a forged actor or session, a cross-project claim, unauthenticated or hostile-Origin helper calls, cross-connector injection, an HTML/SVG canary, and a revive-after-restart check.
2. The matrix records the transport chosen and the result for each canary.
3. Only disposable data is used; no real data on astrid.haus.
4. Each canary is red with its boundary disabled and fails with the specific refusal code when the boundary is enabled; a canary that passes for any other refusal (a generic 4xx, a 404, a timeout) does not count.
**Start from:** `${HISTORICAL_CONTROL_RUN_ROOT}` §6; the H cards' outputs (not yet on base).
**Not in scope:** building any boundary (H cards); the astrid.haus deploy.
**Depends on:** H#transport, H#grant.
**Why xhard:** Rule 1: an auth canary can pass for the wrong reason (any refusal, or a 404), so each canary must be shown red with its boundary off.

### RELEASE-1: the Release 1 acceptance
`A · R1 · 0.75 d · normal · produces A#r1-accepted` · replaces E-4a
**Goal:** Release 1 is shown working on astrid.haus and the owner has watched the film.
**Done when:**
1. IP6 is green on one recorded revision set (testing.md): every condition of "Done = Release 1 accepted" in agent_goal.md holds, including the v9 and v11 replay scenarios and SEC-1…5.
2. WRITERS' census has zero "fallback" rows, and `/publish-document` and the app-save adapter are no longer used by the App.
3. FINAL-E2E stage 3 passes on astrid.haus after the user's deploy: pair, see `almost-ready`, open the film with all 45 cuts, one visualize and one small edit plus render through the local Runtime, with screenshots and receipts.
4. The external gate `codex-accepts-base` is met (Codex's film render proof and focused tests on their combined tips).
5. The owner watches the film; the release is recorded.
**Start from:** `production/review/merge/FINAL-E2E.md` (stage 3); testing.md IP6.
**Not in scope:** stages 1 and 2 (the gate and the replays already cover them); a second review; PRACTICE (it gates nothing).
**Depends on:** A#replays, A#sec-matrix, A#green, C#provider-retry, D#apply, D#drafts, D#sheet-external, D#skill, D#skill-0, D#ux-loop, E#all-writers, E#collab-ux, E#gesture-choices, G#checks, G#render-parity, G#verify-loop, G#vocab, external codex-accepts-base. (These are the R1 graph's leaves: every R1 card except PRACTICE is covered transitively, and `projects/generate.py` fails otherwise.)

### FINAL-R3: the last campaign
`A · R3 · 2.5 d · normal · produces A#r3-accepted` · replaces E-2 and E-4b
**Goal:** The full capability set passes one final campaign and the owner has watched the film before any live migration.
**Done when:**
1. IP7 (Release 2) and IP8 are green, each on one recorded revision set (testing.md); every supported row of the full parity matrix passes.
2. One examiner round over the full capability set, with findings routed.
3. FINAL-E2E passes on a migrated duplicate, and the GOLDEN compare, including frames and audio, passes on that migrated duplicate.
4. The owner's sign-off is recorded. The live migration happens only on the user's go.
**Start from:** the GOLDEN tool; `production/review/merge/FINAL-E2E.md`; testing.md IP7 and IP8.
**Not in scope:** the live-film migration itself.
**Depends on:** A#r1-accepted, I#*, C#schema-warn, D#script, D#retention, F#repairs, E#review, G#full-parity, J#curves, J#ext-view, J#ext-component, J#proofs.

---

## B: Preservation

### H-DATA: the compat integer and owned-only stripping
`B · R1 · 1.5 d · xhard · produces B#compat` · replaces H-DATA
**Goal:** Loading, saving and migrating never drop or resurrect a value Astrid does not own, and a writer that does not understand a feature-bearing head is refused.
**Done when:**
1. `_strip_derived` strips only the owned derived paths (`_index`, `_timeline`), not every `_` key at every depth. Parent clips are walked; malformed and colliding values are kept.
2. The collision fixture (an `app.astrid._legacy` collision, parent clips, opaque underscore keys) is unchanged through load, save, publish, reopen, merge and undo. This is a red-before, green-after fix: the fixture fails on the base.
3. Migrating twice gives the same bytes as migrating once.
4. One `app.astrid.v` integer is checked at the commit boundary: a writer lacking the head's value is refused with an explicit error, and an unknown feature fails explicitly. Astrid's own publish and restore paths cannot skip it (a test drives each against a feature-bearing head).
5. An enumeration test fails if any `_`-prefixed key the Astrid code writes is neither in the owned list (`_index`, `_timeline`) nor deliberately kept with a reason; the one collision fixture is not the only coverage.
6. The v8 film (on a duplicate) is byte-identical through load, save, publish and reopen.
**Start from:** Astrid `astrid/sdk/timeline/doc.py` (`_strip_derived` ~160, `_serialize`), `astrid/sdk/timeline/_common.py` (`DERIVED_PREFIX`), `astrid/sdk/timeline/publish.py`, `astrid/core/timeline/astrid_ns.py` (the dual read and `_legacy` collisions), `astrid/sdk/timeline/checkout.py`.
**Not in scope:** the Runtime's own readers, unless a test shows they need the bump; per-feature `requires` arrays; new features behind the integer.
**Depends on:** A#base.
**Why xhard:** changes the migration and compatibility invariant: which keys are stripped and which writers are refused decides, silently, whether data is dropped or resurrected.
**Design detail:** `${HISTORICAL_CONTROL_RUN_ROOT}` §2-§3.

### PRES-HARNESS: the preservation contract and the round-trip harness
`B · R1 · 1.5 d · normal · produces B#pres-harness` · replaces S-PRES (contract and harness)
**Goal:** A written contract says what an App save must keep, and a harness shows where today's code still loses data.
**Done when:**
1. The contract is written (opaque and unknown fields kept: config, `config.app` namespaces, clip and track `app`, unknown clip fields, registry metadata, the bundle; a clear is explicit and only within its declared coverage; removed values never resurrect), in the PR description and code comments.
2. The harness runs the X0 sentinels through the real App functions and an exact Runtime reload, for both providers, using the X0 fixtures.
3. The harness lists the losses still present on the base. Known today: `serializeForDisk` rebuilds a selected field set and its tests reject unknown siblings. The `config.app` spread (`config-utils.ts`) and transition deletion are already fixed; the harness must show them as passing, not as losses.
4. Unchanged paths are proved unchanged: the harness passes where nothing is lost.
5. GATE scenario 1 is added: open the editor, then the popup, and no save is emitted without an edit.
**Start from:** App `src/tools/video-editor/lib/serialize.ts`, `lib/serialize.test.ts`, `lib/config-utils.ts` (`resolveTimelineConfig`, ~182) and `config-utils.test.ts`, `src/integrations/runtime/dataProvider.ts` (`reconcileParentClips`, ~1266), `src/tools/travel-between-images/components/shotTimelineDataProvider.ts`; the `tests/fixtures/app_payloads/` fixtures from X0.
**Not in scope:** repairs (PRES-REPAIRS); the commit route or EditCommands; running every X0 case on every path (cases 1-3 only).
**Depends on:** A#x0-editor, A#x0-popup.
**Design detail:** `briefs/WS-SAVE.md` S-PRES card.

### PRES-REPAIRS: fix the losses the harness found
`B · R1 · 1.25 d · xhard · produces B#preservation` · replaces S-PRES (repairs)
**Goal:** Every loss the harness found is fixed in the App, so opaque fields and explicit clears survive a save.
**Done when:**
1. One repair per failing path from PRES-HARNESS, each shown red before and green after in the PR.
2. Opaque and unknown fields survive; an explicit clear removes only the field it names; nothing is resurrected after an exact reload.
3. Paths that were already passing are unchanged (the harness stays green for them).
4. The change goes to Codex's App owner as a PR; trunk takes it when the checks pass.
**Start from:** App `src/tools/video-editor/lib/serialize.ts` (`serializeForDisk`), the other paths named by the harness result.
**Not in scope:** converting writers to EditCommands (E cards); new fields; fixing paths the harness did not flag.
**Depends on:** B#pres-harness.
**Why xhard:** fixes silent data loss in another repo's save path; a wrong repair drops user fields quietly.

---

## C: Runtime (PRs to Codex's Runtime owner)

### ACCEPT: atomic acceptance and the commit route
`C · R1 · 1.5 d · xhard · produces C#acceptance` · replaces S-RT (acceptance half)
**Goal:** The Runtime accepts a commit once, atomically, with evidence, and serves the commit HTTP route.
**Done when:**
1. First, the commit cost is measured on a duplicate of the film (warm and cold, two sessions, lock-hold time) and the table is in the PR.
2. A retry after the head moved returns the original stored result. The same request id with a changed body gives `RequestIdConflict`. The existing "idempotency key was already used with different input" conflict at `service.py:1977-1991` is the starting point, not a rebuild.
3. A crash injected between the head move and the response recovers to exactly one revision and the stored result. The test uses a budget that scales with load, and no xfail.
4. Evidence is retrievable by digest; the publisher is authenticated and the asserted actor is recorded; `no_change` is stored without a revision; a dry run is never stored.
5. The commit HTTP route is served by the Runtime (in the OpenAPI), reachable through the App's existing `/api/astrid/*` proxy. Old clients still publish unchanged while the head carries no feature beyond their `app.astrid.v`; on a feature-bearing head HISTORY's check refuses them.
6. Parity: premise fixed: the App polls every 30 s, not 2 s.
**Start from:** Runtime `runtime_protocol/service.py` (`_command_replay_state` ~1977, the publish path), `runtime_protocol/canonical_schema.py` (`parent_composition_revisions` ~337, `parent_composition_heads` ~352), `contract/openapi/workspace-v1.yaml`; App `config/vite/astridBridgeProxy.ts`.
**Not in scope:** the head read, ancestry and provenance (HISTORY) and the list and restore wiring (HISTORY-WIRE); a staged narration record; the commit service logic (D COMMIT).
**Depends on:** A#contract-commit.
**Why xhard:** f4 = 2: atomic acceptance, idempotent retry and recovery from a crash between the head move and the response are the card.
**Design detail:** `briefs/WS-SAVE.md` §3.6 and the S-RT card.

### HISTORY-WIRE: wire revision lists and restore to the Runtime's existing calls
`C · R1 · 0.5 d · normal · produces C#history-wire` · split from HISTORY (the wiring half)
**Goal:** Revision lists and restore work from Astrid over the Runtime's existing calls, and the legacy history routes keep answering.
**Done when:**
1. `RuntimeRevisions.list` (`astrid/sdk/timeline/revisions.py`, which still says "cannot list") is wired to the Runtime's list and restore calls (`generated.py:847,853`). `TL@prev` and `TL@-2` resolve after two publishes.
2. Parity: the legacy history/diff/archive/recover routes still answer.
**Start from:** Runtime `runtime_protocol/service.py` (`list_project_parent_composition_revisions` ~2354, `restore_project_parent_composition_revision` ~2389); Astrid `astrid/sdk/timeline/revisions.py`, `astrid/packs/timeline/cli_history.py`, `banodoco_workspace_client/generated.py`.
**Not in scope:** the compact head read, ancestry, provenance and the narration decision (HISTORY); `revert` (D UNDO-REVERT).
**Depends on:** A#base.

### HISTORY: the head read, ancestry and provenance
`C · R1 · 0.75 d · xhard · produces C#history` · replaces S-RT (history half) and H1a (the ancestry half; wiring is HISTORY-WIRE)
**Goal:** Revisions carry ancestry and provenance, and the head can be read cheaply, so undo, restore and rebase have something true to stand on.
**Done when:**
1. A compact `head()` read returns revision id, publication id and updated time, and never hits `inspect`'s caps; a head change is seen within one poll.
2. Revisions carry ancestry (`previous_revision_id`, `previous_publication_id`, `restored_from_revision_id`) and provenance. The existing publication field `parent_revision_id` is not used as ancestry (the table has no parent column today).
3. The `app.astrid.v` check from H-DATA runs at acceptance, and the legacy publish and restore routes cannot bypass it: on a feature-bearing head, each refuses a writer below the head's value (one test per route). Old clients publish unchanged only while the head is compatible.
4. Narration: confirm first whether `shot_text_bindings` (`canonical_schema.py:244`, same SQLite database as the heads) needs to move in the head transaction. If yes, do it in one transaction; if not, say so in the PR and do nothing.
5. Fake-Runtime unit test of the ancestry walk. Old repeated-revision publications stay separate events.
6. Parity: text-binding set/show/list/rebind still answer after the narration decision (item 4).
7. The ancestry migration is checked on a duplicate of the film: existing revisions get null or derived ancestry as specified, none is invented, and running the upgrade chain twice gives the same bytes as once.
**Start from:** Runtime `runtime_protocol/service.py`, `runtime_protocol/canonical_schema.py`; Astrid `astrid/sdk/timeline/revisions.py`, `astrid/packs/timeline/cli_history.py`.
**Not in scope:** the list and restore wiring and the legacy routes (HISTORY-WIRE); `revert` (D UNDO-REVERT); the App's 2 s poll switch; retention and purge.
**Depends on:** C#acceptance, C#history-wire.
**Why xhard:** Rule 1: adds ancestry columns to Runtime revisions and a narration-transaction decision; wrong ancestry only shows up later, in revert and undo.

### TASK-IDENTITY: a fixed tool runs again
`C · R1 · 1 d · xhard · produces C#task-replay` · split from TASK-REPLAY (identity and replay; carry ledger "Found, not fixed"; F-097)
**Goal:** After an executor's code changes, identical inputs run again instead of replaying the old failure, and unchanged code keeps its identity.
**Done when:**
1. The capability digest covers executor source: changing an executor's code makes identical inputs admit a new task (red before, green after; 14 Oct: de796f65 stayed unchanged across 2db7af6f/af87f50f and the old failure replayed).
2. Unchanged executor code keeps its capability digest and is replayed as before: a different checkout path, a changed mtime and a regenerated `.pyc` each leave the digest equal (test).
3. A failed task is never silently replayed for new code; a deliberate replay of an unchanged failure says so (the SDK already labels replays: `rerun=True`).
4. `tasks retry` either runs or fails within 30 s naming the digest mismatch; it never sits `queued` forever.
**Start from:** Runtime `runtime_protocol/store.py` (task admission, `command_idempotency`), the capability digest computation (find it from `tasks show`'s digest field); Astrid `astrid/sdk/invocation.py` (replay detection, `rerun`).
**Not in scope:** provider retry and pacing (PROVIDER-RETRY); a general job scheduler.
**Depends on:** A#base.
**Why xhard:** changes task identity across the Runtime and Astrid; a digest that covers too little replays stale failures, one that covers too much re-runs paid work, and both are silent.

### PROVIDER-RETRY: the Runtime retries providers
`C · R1 · 0.75 d · xhard · produces C#provider-retry` · split from TASK-REPLAY (provider backoff and pacing)
**Goal:** Provider rate limits are retried and paced by the Runtime, not by each executor.
**Done when:**
1. Executors label failures as retryable (with a retry-after) or final; a fake provider returning 429 then 200 is retried by the Runtime and succeeds once, as one task.
2. The Runtime owns backoff and per-provider pacing: two tasks against one rate-limited fake provider are spaced by its retry-after, and a final failure is not retried (tests).
3. The speech executor's stopgap 429 backoff (`3/8/20 s`, af87f50f) is removed; a speech task against the 429 fake still succeeds.
**Start from:** Runtime `runtime_protocol/store.py` (task admission and the task run loop); Astrid `astrid/packs/generation/actions/generate_speech/run.py` (the stopgap), `astrid/sdk/invocation.py`.
**Not in scope:** task identity (TASK-IDENTITY); a general job scheduler; per-provider quotas beyond pacing.
**Depends on:** C#task-replay.
**Why xhard:** crosses the Runtime and Astrid's executors and owns retry semantics; a wrong retry duplicates a paid generation or hides a final failure.

### SCHEMA-WARN: warn-mode schema findings on receipts
`C · R2 · 0.5 d · normal · produces C#schema-warn` · replaces R3
**Goal:** The Runtime records schema findings on receipts and never rejects a publication because of them.
**Done when:**
1. A valid publication has an empty `schema_report`.
2. A legacy loose key adds exactly one finding.
3. No publication is rejected; the existing Runtime publication tests still pass.
**Start from:** Runtime `contract/schemas/timeline-config.schema.json` (the authored projection; confirm this is the schema before starting) and the receipt path in `runtime_protocol/service.py`; the Runtime checks only track roles today (~2262-2273).
**Not in scope:** rejecting anything (enforcement is a later decision); new schemas.
**Depends on:** A#contract-command.

---

## D: Semantic editing

### RUNNER: one EditCommand format and one runner
`D · R1 · 2.5 d · xhard · produces D#commands` · replaces M2, UX-CLEAR
**Goal:** Every public timeline write is an EditCommand run by one runner, and a clear is an explicit command instead of a silent null-pop.
**Done when:**
1. All scenarios under `tests/editing_scenarios/` (49 YAML files, not the old 47) pass on the 3 harness paths (cli, sheet, python) with journal equality: records equal apart from source, actor, at, id, seq, prev, hash. Journal `calls` is filled (today `Plan.calls` is never passed a value).
2. A refused command leaves the document unchanged and returns a typed error. A crash never counts as a refusal.
3. A mutator-enumeration test fails when a public `Clip`/`Checkout`/`Cut` mutator is not a runner entry. `timelines edit TL --command '<JSON>' [--dry-run]` returns a change preview.
4. `--clear KEY` clears presence-aware. `--set KEY=null` is refused where the element schema forbids null, and the refusal names `--clear`. `--set italicWord=null` on an am-type is refused; `--clear italicWord` leaves the element default. The interim null-pop test (`model.py:630`) is replaced by an equivalent.
5. The runner converts canvas px once, as `set` does (a past bug: `tl.add` stored raw px). The harness xfails are re-checked, none left stale.
6. Parity: every `edit` flag in the inventory maps to a registry entry or a `removed.yaml` alias (generated table); `tests/packs/timeline/test_cli_edit_flags.py`, `test_cli_media.py`, `test_cli_look.py`, `test_cli_voice_bindings.py`, `test_verbs_working_copy.py`, `test_cli_history.py` pass unmodified (or the change has a `tests/parity/removed.yaml` line); `edit --file F` and `words --file F` still work (journaled); old journals still `log` and `log --verify`; `undo N` / `redo N` kept.
**Start from:** `schemas/change-contract/opcall.schema.json` (EditCommand evolves this draft; no new schema tree), `astrid/sdk/timeline/transaction.py` (`Plan` :18, `edit_transaction` :103), `astrid/sdk/timeline/journal.py`, `astrid/sdk/timeline/store.py` (`_journaled` :117), `astrid/sdk/timeline/model.py` (`Clip.set` ~:630), `astrid/sdk/timeline/edits.py` (`add` :36), `astrid/packs/timeline/cli.py` (`_cmd_edit` :3079), `tests/editing_conformance/runner.py` (`PATHS` :40).
**Not in scope:** generated TypeScript or an App registry (the App keeps its own `commands/types.ts` and an explicit adapter); "run" and "bridge" harness paths; a contributed no-op fixture command; restore/revert; the five bypass closures (BYPASSES).
**Depends on:** A#base, B#compat
**Why xhard:** f3 = 2: a new mechanism (no OpCall producer exists) that routes every write, the journal and clears through one runner.
**Design detail:** `${HISTORICAL_CONTROL_RUN_ROOT}` M2 and §4.1.

### REGISTRY: registry metadata and explicit adapters
`D · R1 · 0.75 d · normal · produces D#registry` · new (M2's projection half; opus-agent-experience §5)
**Goal:** Each command's registry entry holds what execution needs (handler, inverse, canonical name, aliases), the reference docs are generated from it, and the CLI, SDK and sheet reach it through small explicit adapters.
**Done when:**
1. Each registry entry declares its handler, inverse, canonical name and `aliases`; aliases parse and are journaled under the canonical id; `--help`, `show REF`'s edit line and the skill's flag reference list canonical spellings only, generated from the registry.
2. The CLI, SDK and sheet reach entries through explicit adapters, not generated parsers: a flag → handler check fails when an `edit` flag maps to no entry or to two, and one representative round trip per adapter (CLI, SDK, sheet) gives equal journal records.
3. `--crossfade` and `--add-media` are entries. `--set opacity=0.6` resolves to `look.opacity` when the element has no `opacity` parameter.
4. The "add an operation" recipe (≤ 40 lines, in the timeline skill's reference) exists, and a fresh configured normal worker follows it once, adding a no-op that touches only the declaration, its adapter line and one scenario YAML.
**Start from:** the RUNNER's registry; `astrid/packs/timeline/cli.py` (`_configure_edit`, `build_parser`), `cli_look.py`; `astrid/sdk/timeline/edits.py`; `astrid/sdk/timeline_sheet.py`.
**Not in scope:** removing spellings (VOCAB); `apply` of files (APPLY-FILES); generating CLI flags, SDK methods or sheet tokens from the registry; generated TypeScript for the App.
**Depends on:** D#commands.

### APPLY-FILES: apply a sheet, JSONL or `.py` file as one transaction
`D · R1 · 0.5 d · normal · produces D#apply` · split from REGISTRY (atomic `apply`)
**Goal:** `apply TL FILE` runs a sheet, a commands JSONL file or a `.py` file as one transaction, all or nothing.
**Done when:**
1. `apply TL FILE` takes a sheet, a commands JSONL file or a `.py` file and runs it as one runner transaction (one journal record set, one undo step); there is no `timelines run` verb.
2. A failure injected partway through a sheet, a JSONL file and a `.py` file each leaves the document and the journal byte-identical to before the call.
**Start from:** `astrid/packs/timeline/cli.py` (`apply`), `astrid/sdk/timeline_sheet.py` (`apply_sheet` :662), `astrid/sdk/timeline/transaction.py` (`edit_transaction` :103).
**Not in scope:** new sheet fields; the sheet adapter (SHEET-EXTERNAL); a script sandbox.
**Depends on:** D#commands.

### BYPASSES: close the five bypasses
`D · R1 · 0.75 d · xhard · produces D#no-bypass` · replaces M2 remainder
**Goal:** Nothing reaches the document, the history or a publication except through the runner.
**Done when:**
1. One test per bypass, each red before and green after: `save()` to a non-draft path drops the journal and undo; `save()` without a path writes into the cwd (`checkout.py:115`); undo/redo run without the lock or merge check (`checkout.py:219`, `:241`); raw `tl.bundle` mutation is refused at save by a digest backstop; `publish()` without a path is unrecorded (`publish.py:53`, `if self.path`).
2. `astrid/core/timeline/inverses.py` (783 lines, imported only by `tests/timeline/test_inverses.py`) is deleted if the runner's inverses supersede it, with its test replaced by registry inverse tests. Before deletion, a list maps every case `test_inverses.py` covers to a registry inverse test that covers it; deletion fails the card if any case is unmapped.
**Start from:** `astrid/sdk/timeline/checkout.py`, `astrid/sdk/timeline/publish.py`, `astrid/core/timeline/inverses.py`, `astrid/packs/timeline/cli_working.py`.
**Not in scope:** draft expiry, the status listing of unpublished drafts and crash-safe undo/redo (DRAFTS); purge of timelines, branching duplicates, payload dedupe (RETENTION); new verbs.
**Depends on:** D#commands
**Why xhard:** closes save/undo/publish paths that bypass the journal; a missed bypass is invisible corruption.
**Design detail:** WS-SAVE M2 "Close these bypasses".

### DRAFTS: expire stale drafts, list unpublished ones, crash-safe undo and redo
`D · R1 · 0.75 d · xhard · produces D#drafts` · split from BYPASSES; replaces TL-LIFECYCLE (draft expiry only)
**Goal:** Stale clean drafts go away safely, drafts with unpublished work are never removed without an explicit discard, and undo and redo cannot lose a step.
**Done when:**
1. A clean draft (no unpublished edits) with no lease and no change for N days is removed automatically, with its journal and markers. A leased draft is never removed. The film's head and history are byte-identical afterwards.
2. A dirty draft (unpublished edits) never expires: `status` lists it, and only an explicit `timelines discard` (`cli_working.py` `_cmd_discard` :421) removes it (test: a dirty draft past N days is still there).
3. Undo and redo survive an injected crash without losing a step: a crash between writing the target and removing the step, and the reverse, each leaves one consistent state, and the next undo or redo recovers.
**Start from:** `astrid/sdk/timeline/checkout.py` (undo/redo ~:219, :241), `astrid/packs/timeline/cli_working.py`, `astrid/packs/timeline/cli.py` (`_cmd_status` :2783).
**Not in scope:** the five bypass closures and the `inverses.py` deletion (BYPASSES); purge of timelines, branching duplicates, payload dedupe (RETENTION); new verbs.
**Depends on:** D#commands, D#no-bypass
**Why xhard:** deletes drafts by lease and age, and rewrites undo/redo step order; a wrong lease check or write order loses authored work or history quietly.
**Design detail:** TL-LIFECYCLE (draft expiry) and WS-SAVE M2.

### IDENTITY: identities survive split, duplicate, fork and merge
`D · R1 · 1 d · xhard · produces D#identities` · replaces U1
**Goal:** Clip and cut identities survive split, duplicate, detach-audio, forks and merges, and cut ids are never reused.
**Done when:**
1. Identity tests run on the real runner mutators for split, duplicate, detach-audio and cut-id reservation. Decision made here: cut ids use reservation, not tombstones. The next id comes from a persisted high-water mark that never goes down, so `_next_cut_id` (`edits.py:143`), which today checks only present entities, can no longer reissue a removed id.
2. A merge is keyed by occurrence, not `shot_id`. Forks appear in `id_map`.
3. Compiled output is unchanged on the X0 fixtures.
4. A note lists the flows that need the `app.astrid.uid` scheme. Add the scheme only for a flow that demonstrably fails.
5. An orphaned cut still resolves by its id (`tl.cut("c06")` failed on 14 Oct while status listed its orphans).
6. A property test (fixed seeds, at least 200 random sequences of remove, split, save, reload, merge and undo) shows a removed cut id is never reissued across save, reload, merge and undo.
**Start from:** `astrid/core/timeline/astrid_ns.py` (`CLIP_INTENT_KEYS`), `astrid/sdk/timeline/edits.py` (`_split_cut` :153, `_next_cut_id` :143), `astrid/sdk/timeline/checkout.py` (`draft` :284, `_same_document` :403), `astrid/sdk/timeline/lookup.py`. Tests import `astrid.sdk.timeline_checkout`, the documented path.
**Not in scope:** adapt-save matching or merge behaviour (REBASE); `add --from` unless RUNNER built it.
**Depends on:** D#commands, A#x0-editor
**Why xhard:** changes clip and cut identity across split, merge and undo; a reissued or lost id moves content silently, and the damage shows far away.
**Design detail:** WS-SAVE U1.

### REBASE: replay pending commands onto a new head
`D · R1 · 2 d · xhard · produces D#merge` · replaces M3 core
**Goal:** Pending commands are re-run on a newer head, and anything that does not fit is reported with a concrete next step.
**Done when:**
1. `rebase(commands, onto)` returns accepted (with `id_map`) or a conflict. One unit test each for: accepted with id_map, `same-property` (base, theirs, ours), `delete-vs-edit`, `dependent` (id collision, vanished reference, new blocking finding).
2. A gap retime upstream of a replayed drag keeps its meaning. An add + set chain keeps its ids.
3. Ambiguous cases are refused with a next step. No gesture inference, no T1–T10 table.
4. Existing merge tests (`three_way`) stay green against the recorded baseline.
5. Parity: named rebase cases: two writers on one working copy; `publish --force` → "keep mine" (or a `removed.yaml` line).
6. Astrid's suite runs apply, inverse and rebase over CONTRACT-COMMAND's shared request/result fixtures. Only Astrid implements rebase: the App proves its adaptation (GESTURES, SUFFIX) and the Runtime its validation, acceptance and replay (ACCEPT) against the same fixtures, and the real commit-path test runs at IP3.
**Start from:** `astrid/sdk/timeline/store.py` (`three_way` :169), `astrid/sdk/timeline/checkout.py`, the RUNNER commands. Until the compiler lands, resolve timing with `Checkout.resolve()` (`astrid/sdk/timeline/reflow.py:783`).
**Not in scope:** sheet or external imports (SHEET-EXTERNAL); the commit path; the per-caller tests (stale head, suffix, refresh, revert), which belong to the cards that call rebase.
**Depends on:** D#commands, A#contract-command (the compiler is not required; swap to `compile_timing` when it lands, output is byte-identical)
**Why xhard:** A new rebase that must "keep its meaning"; nothing exists on the base.
**Design detail:** WS-SAVE §4.4 and M3.

### SHEET-EXTERNAL: sheet and external revisions as explicit commands
`D · R1 · 1.5 d · xhard · produces D#sheet-external` · replaces M3 remainder
**Goal:** The sheet and revisions made outside Astrid enter through explicit commands and rebase, never by guessing a gesture.
**Done when:**
1. The sheet adapter emits commands from its known editable fields; the sheet round trip is equal.
2. An external revision becomes one `import_external` checkpoint with provenance. Pending commands rebase onto it. `timelines status` names unimported external revisions on its first line.
3. A hand-edited draft on load becomes one `import_external` transaction.
4. Every relation-sensitive ambiguous import listed in WS-SAVE §4.6 is a fixture (one file each), and each is refused with a next step.
5. Parity: the sheet applied over a later edit (a clash names the layer); `test_a_sheet_exported_before_an_edit_never_reverts_it` unmodified (or the change has a `tests/parity/removed.yaml` line).
6. Exporting a sheet and applying it back with no edit emits zero commands (the head does not move).
**Start from:** `astrid/sdk/timeline_sheet.py` (`apply_sheet` :662), `astrid/sdk/timeline/store.py` (`three_way` :169), `astrid/packs/timeline/cli.py` (`_cmd_status` :2783).
**Not in scope:** T1–T10 gesture rows; App writers (E cards).
**Depends on:** D#merge
**Why xhard:** imports revisions made outside Astrid and rebases onto them; a wrong import or a guessed relation changes intent silently.
**Design detail:** WS-SAVE §4.3 and §4.6.

### COMMIT: one commit path
`D · R1 · 2 d · xhard · produces D#commit-service` · replaces G1, RS-1
**Goal:** Every save, from CLI, Python and App, goes through one idempotent commit path that rebases when the head moved.
**Done when:**
1. The X0 oracle rows pass through `commit()`: a 9-frame drag then a narration retime keeps the clip 9 f after its word; no-op gives `no_change`; old base with a disjoint property is accepted with `rebased_onto`; same property gives `same-property`; a clear stays cleared after an exact reload; a writer below `app.astrid.v` gets `unsupported_feature`.
2. A lost response retried after the head moved returns the original result, one revision. A changed body under the same request id gives `RequestIdConflict`.
3. Injected `StaleHead` rebases within a bound (at most twice), otherwise a conflict. A `dry_run` request returns the rebased commands or the conflict and stores nothing (the App's suffix route, CONTRACT-COMMIT).
4. One independent review call reviews the rebase and commit diff with "never invents intent"; findings are fixed or carded.
5. Adds GATE scenario 4 (Astrid half).
6. `timelines publish` retried after a lost response with no key given returns the original receipt: the CLI derives the request id from (base, draft digest).
**Start from:** `astrid/sdk/timeline/publish.py` (`publish` :25), `astrid/sdk/timeline/store.py`, `astrid/sdk/workspace_client.py`; new `astrid/sdk/timeline/commit.py`. Mount on ACCEPT's Runtime route (the App already reaches the Runtime through its `/api/astrid/*` proxy).
**Not in scope:** `/publish-document` or `publish_document`; any new HTTP host; transport and auth (H cards); a no-conflict HTTP route of its own.
**Depends on:** D#merge, C#acceptance, A#contract-commit
**Why xhard:** A new idempotent commit path with a bounded rebase loop, checked by "never invents intent".
**Design detail:** WS-SAVE §4.2 and G1.

### UNDO-REVERT: undo, revert and restore through commit
`D · R1 · 1.5 d · xhard · produces D#history` · replaces H1
**Goal:** Undo, revert and restore are named commits, and history, refs and diff read the real Runtime revisions.
**Done when:**
1. After two publishes, `TL@prev` and `TL@-2` resolve; `timelines history` shows id, time, source and message. Starting point: HISTORY-WIRE (C) wires `RuntimeRevisions.list` to the Runtime's existing list call; do not rebuild it.
2. `timelines revert <publication>` is a new commit of the inverse commands rebased onto head. A revert with later overlapping work gives a `same-property` conflict naming the later publication.
3. `timelines restore` records `restored_from_revision_id`. L6-01 on a duplicate: `restore c17 --from @prev` keeps 45 cuts.
4. A fake-Runtime unit test covers the ancestry walk.
5. Only `restore` is added. `undo` on a clean working copy right after your own publish stages that publication's inverse (published like any edit); with later overlapping work it gives a conflict naming `restore`; `revert` is an alias.
**Start from:** `astrid/sdk/timeline/revisions.py` (`RuntimeRevisions` :59, `CANNOT_LIST` :23), `astrid/packs/timeline/cli_history.py`, **Runtime** `runtime_protocol/service.py` (`list_project_parent_composition_revisions` :2354, `restore_project_parent_composition_revision` :2389), `astrid/sdk/timeline/store.py`.
**Not in scope:** the App's dirty-save barrier (SAVE-ROUTING and SUFFIX); undo of drafts beyond today's.
**Depends on:** D#commit-service, C#history, C#history-wire
**Why xhard:** Rule 1: inverse commands rebased onto a moved head, plus restore provenance across Astrid and the Runtime.
**Design detail:** WS-SAVE §4.7.

### AGENT-SYNC: status, watch, checkout refresh, exact-revision verify
`D · R1 · 2.5 d · xhard · produces D#agent-sync`
**Goal:** Several agents and the App see each other's accepted work, refresh without loss, and verify exactly what they published.
**Done when:**
1. `timelines status` shows base, observed head, accepted revision, unimported externals and conflicts.
2. `checkout` on an existing working copy refreshes it: `rebase(my commands, onto=head)`, accepted or a conflict with choices.
3. `status --watch` uses the Runtime's compact head read.
4. Verify and the post-publish reset read the exact receipt revision. A republish by another writer shows as activity, never as my verification.
5. Two agents on one duplicate see each other's work, refresh without loss, and verify what they published. (The App joins this session at IP6.)
6. Parity: `status --text/--human/--all/--render/--json` are kept; the new fields are added to them.
7. No new verbs (`refresh`, `watch` and `review` do not parse); an agent's commits show as `agent:<name>` in `history` and `log`.
**Start from:** `astrid/packs/timeline/cli.py` (`_cmd_status` :2783), `astrid/sdk/timeline/publish.py`, `astrid/sdk/timeline/checkout.py` (`draft` :284), the REBASE function.
**Not in scope:** review-before-accept (REVIEW, E); change-view widening.
**Depends on:** D#commit-service, C#history
**Why xhard:** f4 = 2: several concurrent writers; verifying the exact revision vs another writer's republish is a quiet identity bug.

### SKILL: one generated skill
`D · R1 · 0.75 d · normal · produces D#skill` · replaces A-SKILL (the refresh of SKILL-0, not its first version)
**Goal:** A fresh agent can follow one short skill without meeting a verb that does not exist.
**Done when:**
1. SKILL-0's timeline skill gains a flag reference generated from the registry's canonical set, plus sync, history and restore recipes; the skill stays ≤ 150 lines plus the generated reference, and SKILL-0's doc test stays green.
2. Every fenced command runs in a test against the built CLI. No `astrid executors run` or `astrid agent` hints remain (the chiptune skill showed one; the CLI hints at the other).
3. The recipes (orientation, the edit loop, history/revert, sync) are harness scenarios. Skills keep their frontmatter.
**Start from:** `astrid/packs/rendering/docs/SKILL.md`, `astrid/packs/rendering/docs/references/document-checkout.md`, `astrid/agent_profiles/astrid.md`, the CLI specs in `astrid/packs/timeline/cli.py`.
**Not in scope:** the App; the extension skill (J).
**Depends on:** D#agent-sync, G#views
**Design detail:** WS-AGENT A-SKILL; apply `opus-agent-experience.md` outline if it exists.

### ADD: add a layer in one command
`D · R1 · 0.75 d · normal · produces D#add-layer` · replaces UX-ADD
**Goal:** One command adds a layer to a cut by copying another layer.
**Done when:**
1. `--add CUT --like ADDRESS [--set …] [--on …]` adds one layer with that element and look. On a duplicate of the film, v9's "PART 01 · EVERY CAPABILITY" label is 1 command.
2. The existing cut-free media add (`--add-media`, `--trim-in/--trim-out`, `--slip`) runs through the runner and keeps working: the film's three plain music clips rebuilt keep track, source span and gain; adding a bed never assigns c01 and refuses a zero source range.
**Start from:** `astrid/packs/timeline/cli.py` (`_add_media` :3334), `astrid/sdk/timeline/edits.py` (`add` :36), the RUNNER registry.
**Not in scope:** `adopt music-bed` or any clock inferred from asset names (I cards).
**Depends on:** D#commands

### REHOME: re-home orphans in bulk
`D · R1 · 1.25 d · normal · produces D#rehome` · replaces UX-REHOME
**Goal:** Orphaned cuts are re-homed as units from one reviewed sheet.
**Done when:**
1. `timelines show TL --as sheet --orphans` writes one line per orphan, grouped by cut, prefilled with a suggestion from the rule in item 5; `apply` of the edited sheet re-homes them; `edit --accept-suggestions` prints the preview, then applies every suggestion. There is no `rehome` verb.
2. `edit --cut cNN --on MOMENT` moves a cut with its layers' offsets.
3. An orphan keeps its published place and length until re-homed; never piled at one instant (v11: 143 orphans at 62.23 s or 147.67 s).
4. Delivered through `show --as sheet --orphans` + `apply`, `edit --accept-suggestions` and the existing `--cut cNN --on`: `timelines rehome` does not parse.
5. The suggestion rule is fixed here and written into the card result and the skill's re-home recipe, one test per clause. For each orphan: (a) if the word it was bound to before the re-flow survives exactly once in the new script (word identity, not ordinal), suggest that word's moment; (b) otherwise, if its old text matches exactly one phrase in the new script, suggest that phrase's start; (c) otherwise leave the line blank with the reason, and `--accept-suggestions` skips it and lists it. The orphans of one cut move together keeping layer offsets; if their suggestions disagree, the cut gets no suggestion. A suggestion is never chosen by nearest time. A different rule needs a new card.
**Start from:** `astrid/packs/timeline/cli.py` (`tl.cut_picture` use ~:3267, `--keep` :3544), `astrid/sdk/timeline_sheet.py` (`apply_sheet` :662), `astrid/sdk/timeline/check.py` (`orphans()`). Uses the same fit store `check` reads.
**Not in scope:** quiet output (SHOW); the one fit store (TIMING-FIXES).
**Depends on:** D#commands (use `Checkout.resolve()` until the compiler lands; it needs only the fit store, which TIMING-FIXES unifies)

### SKILL-0: one timeline skill, true today
`D · R1 (wave 1) · 1 d · normal · produces D#skill-0` · new (opus-agent-experience §5)
**Goal:** A fresh agent learns find → show → edit → see → publish from one short skill whose every command runs on trunk.
**Done when:**
1. `astrid/packs/timeline/docs/SKILL.md` exists, ≤ 150 lines, following the outline in `opus-agent-experience.md` §1. `_core`, `pack-builder`, `video_editing` and the `show`/`visualize` epilogs route timeline edits to it; the `rendering` SKILL's JSON-bundle material moves to a reference with its stale claims gone; root `AGENTS.md` points to a file that exists.
2. Every fenced command in the timeline, `_core` and `rendering` skills names an existing family, verb and flags (checked by extending `tests/verify_docs_commands.sh`); each edit recipe is a scenario YAML.
3. A test scans every hint, `next:` and `recovery_command` string and fails on `astrid agent`, `executors run`, `references/editing.md`, `skill.scripts`, hard-coded film addresses (`c30.cover`, `Astrid`) or a literal `TL`.
4. `ASTRID_ACTOR` is documented; `python3 -m astrid pixel` lists its actions with the `sdk.invoke` form.
**Start from:** `astrid/packs/rendering/docs/SKILL.md` ("CLI checks and journal", "direct detached-draft editing"); `astrid/sdk/timeline_checkout.py:1-25`; `astrid/packs/timeline/cli_common.py:150-158`; `astrid/core/gateway/hivemind.py:178`; `tests/editing_scenarios/`, `tests/verify_docs_commands.sh`.
**Not in scope:** new verbs or flags; rewriting the JSON-bundle docs (move, don't rewrite); a generated flag reference (SKILL).
**Depends on:** A#base.

### UX-LOOP: the loop verbs answer like the rest of the CLI
`D · R1 (wave 1) · 1 d · normal · produces D#ux-loop` · new (opus-agent-experience §5)
**Goal:** Every `timelines` verb answers a human first, takes the same project, units and addresses, and each failure names the next command.
**Done when:**
1. `status`, `publish`, `history`, `diff`, `list`, `render` and `checkout` (including its errors) print a human summary by default with `--json` for the envelope; `edit`, `check`, `find`, `undo` and `apply` gain `--json`.
2. `--project` is optional on every `timelines` verb (the selected project); every length or shift flag accepts `0.6`, `0.6s` and `18f` (`--for 18f`, `--nudge 3f`).
3. `next:` and hint lines use the current timeline's own addresses with `TL` filled in; `media import` prints `handle: sha256:…` and the `--swap-asset` line that uses it.
4. Human-mode errors print `details.next_action`; a bad flag prints ≤ 3 lines naming the verb, the flag and the nearest valid one; `--clip <a cut>` says to use `--cut`.
5. The console script dispatches `status` and `dev` to the gateway; Hivemind's login commands stay under `astrid auth …`.
6. Every internal machine consumer (the App proxy, the journey, skill recipes, tests) passes `--json`: a scan lists each call site of the seven verbs whose default changed, and the suite is run once with the human default to show nothing parses human text. Making `--project` optional is checked for the wrong project: with two projects and none selected, a verb refuses and names the choices; with one selected, it acts on that project and names it on its first line.
**Start from:** `astrid/packs/timeline/cli.py` (`_add_json_flag`), `cli_common.py:150`, `cli_parser.py:27`; `astrid/core/cli/domain_output.py:167`, `astrid/core/cli/domain_media.py:142`; `astrid/sdk/timeline/lookup.py:407`, `astrid/sdk/timeline/_common.py:67`.
**Not in scope:** removing or renaming spellings (VOCAB); help length (VOCAB); new verbs.
**Depends on:** A#base.

### SCRIPT-EDIT: edit narration text in the timeline's history
`D · R2 · 1.5 d · normal · produces D#script-edit` · replaces SCRIPT part 1
**Goal:** The film knows its script and a text edit becomes line operations.
**Done when:**
1. `timelines lines TL` (narration one line per take; the verb exists, extend it, no new verb) accepts line edits. `timelines script TL` stays read-only and rejects any edit flag.
2. `--takes` accepts several folders, later ones winning.
3. The timeline records the script path and digest; `status` names them. No `vo-v*.json` hand files.
4. Parity: today's `script` read form (`--revision --occurrence --kind`) stays as `script TL` with no edit flags.
5. Script editing lands on `lines` (narration line by line), so `script` keeps one meaning (read).
**Start from:** `astrid/sdk/timeline_script.py` (`read_composition_script` :10), `astrid/packs/timeline/cli.py` (`_cmd_script` :2295, narration options ~:3619), `astrid/sdk/remote.py`.
**Not in scope:** recording speech, word timing, re-flow (SCRIPT-REFLOW).
**Depends on:** D#commands

### SCRIPT-REFLOW: re-flow a script edit in one transaction
`D · R2 · 2 d · xhard · produces D#script` · replaces SCRIPT part 2
**Goal:** Changed script lines are recorded, word-timed and re-flowed in one transaction.
**Done when:**
1. Changed or new lines are recorded through the speech capability (voice and rate per line); unchanged lines keep their takes.
2. Re-flow is one transaction. Every take matches its text word for word.
3. The music bed is fitted once per re-flow, not per line.
4. Parity: `edit --from-script FILE` and the narration flags keep working (or get `removed.yaml` lines).
**Start from:** SCRIPT-EDIT, `astrid/sdk/timeline/reflow.py`, **Runtime** `runtime_protocol/canonical_schema.py` (narration binding and head in one SQLite transaction).
**Not in scope:** on-screen copy quoting (COPY-SYNC).
**Depends on:** D#script-edit, F#timing-fixes
**Why xhard:** One transaction spanning speech generation, word timing, re-flow and the Runtime narration binding; open design.
**Design detail:** `${HISTORICAL_CONTROL_RUN_ROOT}` SCRIPT.

### RETENTION: purge and branching duplicates
`D · R3 · 2 d · xhard · produces D#retention` · replaces TL-LIFECYCLE remainder
**Goal:** Archived duplicates can be purged safely, and a duplicate of the film adds only changed shots.
**Done when:**
1. Revision-payload growth is measured first and recorded; payload dedupe is built only if the number demands it.
2. Purging the v8 tester duplicates reclaims their revisions and payloads. A purge refuses any timeline that is published or referenced, including the film.
3. The film's head and history are byte-identical before and after. Only duplicates are ever touched.
4. Parity: `duplicate --slug/--name`, notes, narration re-bind, invalid-head refusal and all-or-nothing are kept (the duplicate tests in `test_verbs_working_copy.py` pass unmodified (or the change has a `tests/parity/removed.yaml` line)).
5. After a purge the Runtime database passes `PRAGMA foreign_key_check` with no rows, and every remaining timeline's history and payloads load (a loop over all timelines, none failing).
**Start from:** `astrid/sdk/timeline_duplicate.py`, `astrid/packs/timeline/cli.py` (archive ~:1293), **Runtime** `runtime_protocol/service.py` (`archive_timeline` ~:3946), `runtime_protocol/canonical_schema.py` (payload stored inline).
**Not in scope:** draft expiry (DRAFTS); content-addressed storage without a measurement.
**Depends on:** D#history
**Why xhard:** Rule 1: purge deletes revisions and payloads, and whether "referenced" is complete fails quietly; crosses Astrid and the Runtime.

## E: App saving (PRs to Codex's App owner)

### GESTURES: main-editor gestures emit EditCommands
`E · R1 · 1.5 d · xhard · produces E#gestures` · replaces P3B part 1 (ordinary command emission)
**Goal:** Each ordinary main-editor gesture sends one commit with the matching EditCommand and its occurrence identity.
**Done when:**
1. One test per gesture (move, resize, property, split, duplicate, delete, add media, track ops) asserts one commit with the expected command. No diff inference.
2. A 9-frame drag appears in the journal with `via: app`; a later narration retime keeps it 9 f after its word.
3. Explicit semantic clears use `clip.clear`. Ordinary object values remain ordinary values; absent and present-null expectations use the admitted tagged encoding. Legacy save representations remain characterized compatibility behavior; explicit removal and no resurrection are preserved.
4. Parity: the App gesture census (opus-feature-parity §2.8, ~45 gestures) is the checklist; this card converts the main-editor rows, each with one test.
**Start from:** **App** `src/tools/video-editor/hooks/useTimelineCommit.ts` (the transaction boundary), `src/tools/video-editor/commands/types.ts`, `src/tools/video-editor/lib/timeline-patch.ts`, `src/integrations/runtime/generated.ts`.
**Not in scope:** relation-sensitive choices (GESTURE-CHOICES); popup, shot, catalog, restore, proposals (WRITERS); flag routing (SAVE-ROUTING).
**Depends on:** A#contract-command, D#identities, D#commit-service
**Why xhard:** crosses the App and the EditCommand contract and carries occurrence identity; a gesture that sends the wrong command still saves, silently.
**Design detail:** WS-SAVE P3B gesture table.

### GESTURE-CHOICES: gestures that touch tied content offer a choice
`E · R1 · 1 d · xhard · produces E#gesture-choices` · replaces P3B part 1 (relation-sensitive choices and their UI)
**Goal:** A gesture that would trim, detach or ripple tied content asks instead of doing it silently, and sends the chosen commands.
**Done when:**
1. Overlap trims, duplicate ripples and sequence-step or bed drags that touch content tied to a word, the music or a neighbour show the choice (keep, detach, adjust offset, re-anchor); one test per gesture asserts the commands sent for each choice, and cancelling sends nothing.
2. A plain drag of tied content keeps its tie and adjusts the offset, with no choice shown (release-contract §3b).
3. The relation is read from the document's anchors (word, music, neighbour, sequence step), not from on-screen overlap; one fixture per relation.
**Start from:** **App** `src/tools/video-editor/hooks/useTimelineCommit.ts`, `src/tools/video-editor/commands/types.ts`; GESTURES' command emission.
**Not in scope:** ordinary gestures (GESTURES); the conflict panel (COLLAB-UX).
**Depends on:** E#gestures
**Why xhard:** silently trimming or detaching anchored content is the data loss this card prevents; the relation rules cross the App and the command contract.
**Design detail:** WS-SAVE P3B gesture table.

### WRITERS: convert every other App writer, then switch together
`E · R1 · 2 d · xhard · produces E#all-writers` · replaces P3B part 2
**Goal:** Every remaining App writer emits commands and all switch to `/commit` together.
**Done when:**
1. Shot name/settings/duplication (with captured base and `expect`), restore/undo, asset registration, the element-catalog adapter, the standalone hook and proposals each have a test showing the matching command.
2. The old compatibility route is untouched until the last writer is converted; no new intermediate endpoint. Then `/publish-document` and the `app-save` adapter are not used.
3. The shot-popup provider's metadata edits carry the captured base.
4. Parity: every remaining census row (keyframes, effects, transitions, text, shot pin/update/switch, track properties, mute-all, …) emits a command (one test each) or is marked "fallback"; the existing `/publish-document` route and the app-save adapter are removed **only when no row says fallback**.
5. A network-intercept test runs the census scenarios and fails on any `/publish-document` request made by a row not marked "fallback".
**Start from:** **App** `src/tools/travel-between-images/components/shotTimelineDataProvider.ts`, `src/integrations/runtime/dataProvider.ts`, `src/tools/video-editor/lib/proposal-runtime.ts`, `src/tools/video-editor/hooks/useTimelineCommit.ts`.
**Not in scope:** save routing and rebase (SAVE-ROUTING, SUFFIX).
**Depends on:** E#gestures
**Why xhard:** cuts every remaining App writer over to the commit contract; a missed writer keeps saving through the old route with no test going red. (RELEASE-1 requires zero "fallback" rows.)

### SAVE-ROUTING: flag-gated routing, one save in flight
`E · R1 · 1.25 d · xhard · produces E#save-routing` · replaces P1 part 1
**Goal:** With the flag on, saves go through `/commit` with a stable request identity; with it off, nothing changes.
**Done when:**
1. A flag-off snapshot test: request bytes equal today's.
2. One save in flight per timeline; a newer edit waits.
3. A retry after `runtime_unavailable` reuses the same request identity and `Idempotency-Key`.
4. X0 cases 9–14 and 16 pass. Adds GATE scenario 3.
**Start from:** **App** `src/integrations/runtime/dataProvider.ts` (save path ~:593), `src/tools/video-editor/hooks/useTimelinePersistence.ts`, `src/tools/video-editor/hooks/useTimelineCommit.ts`.
**Not in scope:** suffix rebase and recovery drafts (SUFFIX); UI.
**Depends on:** E#gestures, B#preservation
**Why xhard:** f4 = 2: one save in flight and a stable retry identity are the card.
**Design detail:** WS-SAVE P1.

### SUFFIX: keep newer edits after an accepted save
`E · R1 · 1.75 d · xhard · produces E#save-rebase` · replaces P1 part 2
**Goal:** A save accepted after a newer local edit gives the accepted state plus the preserved newer edits, and two tabs lose nothing.
**Done when:**
1. A held response plus a newer edit gives A′ + B on one canonical head: the App gets the rebased suffix from the commit route's dry run (CONTRACT-COMMIT item 3) and commits it; there is no second rebase in the App.
2. The queued save no longer just advances its base head without replaying (Astra; `useTimelinePersistence.ts` `baseHead` ~:640 and `baseHeadAdvance` ~:701). Red before, green after.
3. A lost response retried after the head moved returns the original; one publication. A network failure during the dry run keeps the suffix as a recoverable draft and the dry run is retried (test).
4. Session-scoped recovery drafts keyed by realm, project, timeline, scope and session: two tabs lose no draft. A failed suffix `expect` keeps the whole suffix as a recoverable draft.
5. Adds GATE scenario 4 (App half). An App edit on a v8 duplicate appears in `timelines log` with `source.via = "app"`.
**Start from:** **App** `src/tools/video-editor/hooks/useTimelinePersistence.ts`, `src/integrations/runtime/dataProvider.ts`.
**Not in scope:** conflict UI (COLLAB-UX).
**Depends on:** E#save-routing, A#contract-commit, D#commit-service
**Why xhard:** crosses the App, the commit contract and the Runtime route; whether newer edits survive a held response, a network failure or a second tab is decided here, and a mistake loses them silently.

### COLLAB-UX: status, activity, conflicts, undo
`E · R1 · 2.5 d · normal · produces E#collab-ux` · replaces UX-1
**Goal:** The user can tell whether their save is real, see others' changes and resolve a conflict.
**Done when:**
1. The status line says "saved" only after an accepted commit.
2. An agent publish while the user edits raises a banner and an activity entry with provenance, in the existing `RuntimeActivityDock` (no second feed).
3. A conflict shows only server-valid choices. Undo-mine is local; revert-published is a commit.
4. Inspector shows `starts on "viral" +9f · 12.37 s`; this-occurrence edits show a fork warning.
5. A scripted session on a duplicate: agent publishes while the user edits, banner, conflict with valid choices, revert works. X0 cases 15–16 pass.
6. Parity: manual checkpoints / jump-to-checkpoint and Reload / Save-as-copy are kept or have a `removed.yaml` line; the App's local undo keeps working, and the change to "revert a publication after autosave" is announced in the App.
7. Against a fake Runtime, the status line shows "saved" only after an accepted commit, and the conflict choices shown equal the ones the server returned (unit tests).
**Start from:** **App** `src/features/tasks/components/TasksPane/RuntimeActivityDock.tsx`, `src/integrations/runtime/dataProvider.ts`, `src/integrations/runtime/generated.ts`.
**Not in scope:** review-before-accept (REVIEW); agent verbs (AGENT-SYNC); advisory presence.
**Depends on:** E#save-rebase, D#history, C#history
**Design detail:** WS-SAVE UX-1. Kept whole: one UI surface. Labelled normal: its semantic risks ("saved" means accepted; the conflict choices) belong to SUFFIX and HISTORY.

### REVIEW: review an agent's proposal before accepting
`E · R3 · 1 d · normal · produces E#review` · replaces UX-2
**Goal:** A user can review an agent's proposal, and accepting is one commit.
**Done when:**
1. A scripted review session accepts one proposal and rejects another; a rejected proposal changes nothing.
2. A proposal is (base revision, commands); accepting is rebase plus commit.
**Start from:** **App** `src/tools/video-editor/components/ProposalPanel/ProposalPanel.tsx`, `src/tools/video-editor/lib/proposal-runtime.ts`.
**Not in scope:** advisory presence.
**Depends on:** E#collab-ux

## F: Timing

### CHARACTERIZE: lock today's timing output
`F · R1 · 1 d · normal · produces F#characterized` · replaces M1a
**Goal:** Today's timing output is locked by tests so the compiler cannot change it silently.
**Done when:**
1. Each spec-timing §3.7 bullet has a test citing its source line: first-word picture exception, unanchored SFX, narration-piece splitting, music seams, ripple clustering, quantizers, gap ownership, trimmed-media `until`, 60 ms insert tail, split audio.
2. Known bugs (bed seams accumulating across re-flows, ~29 overlapping pieces in v11; duplicate piece ids) are expected-failures, each with its reason and owning card (TIMING-FIXES, MUSIC-SEGMENTS). First check whether the duplicate-id fix is already on the base; if so it is a normal test.
3. The golden re-flow suites pass unchanged. The diff touches tests only.
**Start from:** `astrid/sdk/timeline_editing.py` (`retime` :351, `retime_with_ripple` :367, `source_to_timeline_time` :455), `astrid/sdk/timeline/reflow.py` (`_fit_sequences` :717), `tests/editing_scenarios/timing/`, `${HISTORICAL_CONTROL_RUN_ROOT}` §3.7.
**Not in scope:** any behaviour change; fixing the bugs found.
**Depends on:** A#base

### COMPILER: one timing engine, extracted unchanged
`F · R1 · 1.25 d · xhard · produces F#compiler` · replaces M1b core (behaviour-preserving extraction)
**Goal:** One compiler, `compile_timing(inputs, commands)`, owns resolved timing, extracted from today's code with byte-identical output.
**Done when:**
1. `compile_timing` is the only writer of resolved timing: reflow, `Checkout.resolve()` and the CLI call it, and its inputs are immutable (a test shows a compile mutates nothing). A timing cycle is rejected with its path (a compile must terminate).
2. The CHARACTERIZE suite and the golden suites pass unchanged; the v8 golden is byte-identical; CHARACTERIZE's expected-failures stay expected-failures (TIMING-FIXES and MUSIC-SEGMENTS fix them). Compile-time bench p95 at most 150 ms (a miss is a decision request, not a failure).
3. Helpers are kept or wrapped: `frame_time`, `source_to_timeline_time`, `timeline_to_source_time`, `quantize_time`, `quantize_interval` stay pure conversions; `retime`, `retime_with_ripple`, `sequence`, `align`, `fit_duration` become thin wrappers over the compiler, or are marked deprecated where they have no internal caller (or get `removed.yaml` lines plus updated `docs/references/document-checkout.md` and `docs/timeline-authoring-capabilities.md`). Premise fixed: adopt/structure/duplicate call `add_authoring_shot`, not retime.
**Start from:** `astrid/sdk/timeline_editing.py`, `astrid/sdk/timeline/model.py` (`StepSequence.fit` :824), `astrid/sdk/timeline/reflow.py` (:661–800), `astrid/sdk/timeline_intent.py` (`sequence_fit` :205), `astrid/packs/rendering/docs/references/document-checkout.md`.
**Not in scope:** any behaviour change (TIMING-FIXES); music segments, switches, envelopes (MUSIC-SEGMENTS, I cards); additive keys and the compat integer (B#compat owns them); pins.
**Depends on:** F#characterized, B#compat, A#golden-baseline
**Why xhard:** replaces the timing logic spread over many callers; a drift is silent and surfaces as data loss far from its cause, so the manager reads the diff even though the golden is strong.
**Design detail:** `${HISTORICAL_CONTROL_RUN_ROOT}` M1b.

### TIMING-FIXES: timing binds to the words and steps it meant
`F · R1 · 1.25 d · xhard · produces F#timing-fixes` · replaces M1b core (the bug fixes) and WORD-ID
**Goal:** The compiler keeps one fit store and binds references to the spoken word or sequence step they meant, and never rebinds one silently.
**Done when:** (each a bug fix, red before and green after)
1. One fit store (`sequence.land`): SDK `fit()`, CLI `--fit-sequence` and the orphan check read and write the same field (14 Oct: the SDK wrote `until`, the check read `sequence_fit.land`, the CLI said "No change").
2. Word identity: the v9 m11 case keeps c14 on "and share" and c15 on "And the LLMs" (`test_a_take_that_says_a_word_again_keeps_each_moment_on_the_word_it_meant`, `tests/sdk/test_timeline_checkout.py:233`, passes on the compiler); `#n` spellings rewritten are reported; v11 "And" cases (three in y08, four in y09) resolve by phrase.
3. An unmatched reference becomes ORPHAN and is never rebound; a missing sequence step is a conflict, never rebound by ordinal; another hand's step edit survives a narration refit.
4. The golden suites pass unchanged except where a fix is listed; each CHARACTERIZE expected-failure these fixes cover becomes a passing test.
**Start from:** the COMPILER; `astrid/sdk/timeline/lookup.py` (phrase lookup ~:176), `astrid/sdk/timeline_intent.py` (`sequence_fit` :205), `astrid/sdk/timeline/model.py` (`StepSequence.fit` :824).
**Not in scope:** music segments (MUSIC-SEGMENTS); ambiguity refusals and the other §3.8 repairs (REPAIRS-STRUCT, REPAIRS-REST).
**Depends on:** F#compiler
**Why xhard:** changes which word or step a timing reference binds to; a wrong binding moves content silently.
**Design detail:** `${HISTORICAL_CONTROL_RUN_ROOT}` M1b, WORD-ID.

### MUSIC-SEGMENTS: rebuild the music bed on every compile
`F · R1 · 1.25 d · xhard · produces F#music-segments` · replaces M1b music part
**Goal:** Bed segments are derived from the authored bed on every compile and never become inputs.
**Done when:**
1. Two re-flows in a row (the v9 to v11 shape) give deterministic unique segment ids, no seam on a seam, and seams only where the film needs them.
2. An equal-delta, different-location music seam test passes.
3. The c17/c18/c19 spanning case is unchanged; untouched/unmanaged ordinary clips and their materialized audio keep byte-identical output; the v8 golden is byte-identical. A first actual managed keep-end edit deliberately adds the authored source carrier and format declaration; this does not claim edited-document byte identity across that format change.
**Start from:** `astrid/core/timeline/music_edit.py`, `astrid/sdk/timeline/reflow.py` (keep-end code), `astrid/packs/timeline/cli_music.py`, the COMPILER.
**Not in scope:** switches on words and envelopes (MUSIC-CLOCK, V-3).
**Depends on:** F#compiler
**Why xhard:** f4 = 2: deterministic segment ids and no seam on a seam across repeated re-flows (idempotency).

### CUTS: one cut index for every consumer
`F · R1 · 2.5 d · xhard · produces F#cuts` · replaces M4
**Goal:** Every consumer sees the same cut for a given id, including orphaned cuts.
**Done when:**
1. One cut index (gaps, overlaps, sequence ranges spanning cuts); every consumer's output is identical before and after over every golden fixture (tiny, golden, v8, v9, v11) and the v9 and v11 film duplicates.
2. `tl.cut("c06")` resolves whenever `c06.*` does, including an orphaned cut (red before, green after).
3. Split, lift and remove follow spec-timing §6.3; a sheet split keeps layer ids; cut ids are never reused.
4. Sound lane: cut-free music, VO and SFX stay cut-free; no bed becomes a c01 layer; lift and split never clone or re-home a bed. The c17/c18/c19 fixture and the film's cut-free music give identical intersections in cut table, sheet and visualize.
5. The addressing and remove scenarios pass on every harness path. A note in spec-timing §6.4 records the demonstration result; no cut record.
6. Parity: the consumer list is re-pinned on the base (including the nine consumers in opus-feature-parity §3); `lift` is listed as a new verb; ordinals are still accepted as input (`--cut N`, `--cuts`, `--edited`).
7. A test fails if any consumer still calls `picture_cuts`, `find_cut` or `_cut_groups` directly; only the index may.
**Start from:** `astrid/core/timeline/cuts.py` (`picture_cuts` :141, `find_cut` :217), `astrid/sdk/timeline/lookup.py` (`cut` :78, `_cut_groups` :295), `astrid/sdk/timeline_cuts.py`, `astrid/sdk/timeline/edits.py`.
**Not in scope:** a cut record; views beyond the filter.
**Depends on:** F#compiler, D#commands, D#identities
**Why xhard:** replaces nine consumers' cut semantics with one index, a timing and identity invariant; drift on an edge case the fixtures miss is silent.
**Design detail:** WS-TIME M4; spec-timing §6.

### REPAIRS-STRUCT: reject cycles and ambiguity
`F · R2 · 1 d · xhard · produces F#repairs-1` · replaces M1c part 1
**Goal:** Timing cycles and ambiguous references are refused with a message instead of silently resolved.
**Done when:**
1. The music/film feedback cycle and self-cycles are rejected with their path; a terminal `until="end"` is imported as a compatibility basis.
2. An existing reference is no longer rewritten to the nearest occurrence (`reflow.py:539–586`); ambiguity is refused.
3. One scenario each; the behaviour changes are listed in the release notes; golden suites pass except where the notes say so.
**Start from:** `astrid/sdk/timeline/reflow.py` (:539–586), the COMPILER cycle check, spec-timing §3.8.
**Not in scope:** the other §3.8 items.
**Depends on:** F#timing-fixes
**Why xhard:** changes timing behaviour (cycles, ambiguity) in the compiler, a load-bearing invariant.

### REPAIRS-REST: remaining timing repairs
`F · R2 · 1.5 d · xhard · produces F#repairs` · replaces M1c part 2
**Goal:** The remaining named repairs ship as deliberate, listed behaviour changes.
**Done when:**
1. Trimmed-media end and trim/speed corrections, and bed-scoped beat references with deterministic overlap ownership, each have their own scenario.
2. Changes are listed in the release notes.
3. Pins remain excluded; source-timed transcript binding is now required. The binding pins the exact immutable transcript snapshot and source clock and is compiled through the existing timing functions; see the Astra098 supplement below.
4. The golden re-flow suites and the CHARACTERIZE suite pass unchanged except where the release notes list a deliberate change; every golden fixture diff is accounted for by one of the three repairs (as in REPAIRS-STRUCT).
**Start from:** `astrid/sdk/timeline/reflow.py`, `astrid/sdk/timeline_editing.py` (`source_to_timeline_time` :455), spec-timing §3.8.
**Not in scope:** word identity and sequence identity (TIMING-FIXES); pins.
**Depends on:** F#repairs-1
**Why xhard:** f4 = 2: trim, speed and beat-reference timing corrections, each a deliberate timing change.

## G: Rendering and views

### PINS-ASTRID: one renderer closure in Astrid, on composition v0.0.7
`G · R1 (wave 0) · 1 d · xhard · produces G#pins-astrid` · replaces R-PINS (Astrid half)
**Goal:** Astrid renders with our composition fork v0.0.7 (clip looks, per-boundary transitions, speed remaps), and the capture cache changes only when the closure changes.
**Done when:**
1. `remotion/package.json` pins the fork's v0.0.7 tag (`e2ab21a7`) instead of upstream v0.0.6. Remotion stays 4.0.509.
2. The track `role` field (`output` / `source`) is in the schema, with generated allow-lists. A source-role test fails before and passes after. (There is no "S0 xfail" on the base to flip; write the test.)
3. A test shows the cache identity changes when a component, the composition package or a font changes, and does not change for an unrelated edit.
4. The existing remotion tests (`tests/packs/rendering/test_remotion_backend.py`, `test_remotion_locking.py`, `test_composed_frame_capture.py`) pass unchanged. (The v8 film's frame and audio compare on the new pin is IP1's.)
**Start from:** `A/remotion/package.json` (line 18 pins v0.0.6); `T/typescript/src/` (the v0.0.7 source); `A/astrid/core/timeline/clip_fields.py` and `clip_fields.yaml`; `A/scripts/gen_remotion_types.py` and `gen_element_catalog.py` (allow-list generators); `A/astrid/packs/rendering/rendering/renderers/remotion/run.py` (owner identity hash).
**Not in scope:** the App pin (PINS-APP); new render features; schema changes beyond `role`.
**Depends on:** A#base, A#golden-baseline.
**Why xhard:** changes the renderer contract every frame depends on; a wrong pin silently changes how the film looks.
**Design detail:** `${HISTORICAL_CONTROL_RUN_ROOT}` (R-PINS row).

### PINS-APP: the App moves to the same closure
`G · R1 · 1.5 d · xhard · produces G#pins` · replaces R-PINS (App half)
**Goal:** The App uses the same composition v0.0.7 and Remotion 4.0.509 as Astrid, as a PR.
**Done when:**
1. `P/vendor/timeline-composition` is the fork's v0.0.7 (today it is 0.0.2). `P/package.json` Remotion versions are 4.0.509 (today 4.0.503).
2. The postinstall patch `scripts/patches/remotion-4.0.503-audio-resume.mjs` is ported to 4.0.509, or shown unnecessary with a test of the audio-resume behaviour it fixes.
3. One test asserts one composition version and one Remotion version across Astrid and the App (a single value each).
4. The App's existing build and video-editor unit tests pass; the App Player still renders a v8 film frame.
5. Player frames at five chosen v8 event frames are captured before the pin and compared after the 0.0.2 to 0.0.7 jump (pixel MAE at most 2/255, region at most 8/255, the tolerances RENDER-PARITY uses); each difference is fixed or listed with a reason. RENDER-PARITY later covers audio and the full set.
**Start from:** `P/package.json` (lines ~136-164); `P/vendor/timeline-composition/package.json` and `typescript/src/types.ts` (`TrackRole` already present, line 51); `P/scripts/patches/remotion-4.0.503-audio-resume.mjs`; `P/src/tools/video-editor/compositions/TimelineRenderer.tsx`.
**Not in scope:** making the Player use the shared evaluation (PLAYER); new App features.
**Depends on:** G#pins-astrid.
**Why xhard:** crosses repos and the pinned renderer contract; a wrong pin silently changes every film in the App.
**Design detail:** `briefs/WS-RENDER.md` (R-PINS row).

### CAPTURE: bounded, cancellable capture on the existing warm owner
`G · R1 · 1.5 d · xhard · produces G#capture` · replaces CAP-G (part 1)
**Goal:** A draft or revision frame capture is bounded in time and memory, and cancelling it leaves nothing behind.
**Done when:**
1. First, measure the current lane on the base and record it in the card's notes: one `check --at` / `edit --verify` today renders a whole candidate preview and decodes it. The "53-66 s to 6 s" speedup was measured on a worker that is not on the base, so treat it as unverified.
2. Capture requests go through the existing owner (`RemotionFrameOwner`, `astrid/core/execution/remotion_frame_owner.py`, currently unwired) and render only the requested frames. The worker queue in `astrid-frame-worker.mjs` is kept, not replaced.
3. Cancelling mid-capture leaves zero orphan processes, sockets and launchd jobs. `native_cleanup` is proven by a test, no longer `"UNPROVED"`.
4. A frame and time budget is enforced: over-budget requests fail with a named error. A cold-browser failure is retried once and the final error reports both causes.
5. Parity: bounds capture, muted PNG capture, frame diagnostics and the scratch guard are kept: `test_bounds_plumbing.py`, `test_composed_frame_capture.py`, `test_remotion_scratch_guards.py` pass unmodified (or the change has a `tests/parity/removed.yaml` line).
**Start from:** `A/astrid/core/execution/remotion_frame_owner.py` (`RemotionFrameOwner`, line 218); `A/astrid/core/execution/remotion_host_session.py` (`HostRemotionSession`); `A/astrid/core/execution/generic_host.py` (~5353, the lease); `A/remotion/src/astrid-frame-worker.mjs` (queue at ~363); `A/astrid/packs/rendering/rendering/renderers/remotion/run.py` (`_owner_paths` 174, `_launch_owner` 209, `_ensure_owner` 296, `native_cleanup` 198/206/554); `A/astrid/packs/rendering/actions/timeline_visualize/fast_lane.py` (`prepare_pair` 139, `decode_frames` 351, `verify` 775).
**Not in scope:** sharing one owner across agents (SHARED-CAPTURE); the historical-base policy (deferred); a new renderer; any change to the machine lease beyond calling it.
**Depends on:** G#pins-astrid.
**Why xhard:** f4 = 2: wires the unused frame owner; cancellation and orphaned processes and launchd jobs (`native_cleanup` "UNPROVED") are the card.
**Design detail:** `briefs/WS-RENDER.md` (CAP-G row).

### SHARED-CAPTURE: concurrent agents share one owner
`G · R1 · 1.5 d · xhard · produces G#verify-loop` · replaces CAP-G (part 2)
**Goal:** Several agents asking for frames queue on one warm owner instead of each starting a browser.
**Done when:**
1. Two concurrent capture requests are served in order by one owner, and neither starts a second browser (test).
2. Admission is bounded: a request over the limit waits or is refused with a named error, never a silent failure. Heavy capture goes through the machine lease. (The 3-agent measurement is IP5's.)
**Start from:** the same files as CAPTURE, especially `RemotionFrameOwner` (queue, lease, cleanup) and `run.py::_ensure_owner`; `A/astrid/packs/rendering/actions/timeline_visualize/composed_frame.py` (`warm_owner_idle_seconds`, line 31).
**Not in scope:** a second queue; per-card benchmarking; rewriting shared machine admission.
**Depends on:** G#capture.
**Why xhard:** f4 = 2: concurrent queueing and bounded admission on one owner.
**Design detail:** `briefs/WS-RENDER.md` (CAP-G row).

### EVAL: shared scene evaluation, grown from planTrack
`G · R1 · 2.5 d · xhard · produces G#eval` · replaces R-EVAL (renderer side) + SCENE-PLAN
**Goal:** Renderer-side code answers "what is visible at frame N" once, Astrid's visibility checks use it instead of a Python mirror, and editing never needs a renderer.
**Done when:**
1. A pure shared function set (prepare, then frame queries) is extracted from the composition package, starting from `planTrack` / `DrawPlan` / `layerOpacity` in `T/typescript/src/lib/transition-spans.ts` (line 44). It answers queries for requested frames only and does not serialise the whole film. The composition draws through it (one copy), and its existing tests pass unchanged. (Agreement on the v8 film's cut boundaries is IP5's.)
2. A Python client asks the warm owner and caches each answer per revision digest and renderer closure: a repeat is served in under 100 ms, and a changed component, composition package version or font forces a recompute while an unrelated edit does not (tests).
3. Renderer visibility moves to the shared evaluation: the publish-blocking GAP/`picture` and EMPTY checks and the `--labels` overlay read visibility, coverage and bounds from it. Unknown component internals (e.g. text-card transforms) are "unknown", never guessed; the element template shows the bounds declaration, and a component without bounds gives coverage "unknown" with a named finding.
4. Pure role and metadata queries stay in Python and read the element declarations: `role_of`, which `reflow._doomed_cuts` uses to tell picture and background clips apart, moves to a small pure module with its tests. Command application and structural reflow never start or wait for a renderer (test: the reflow and edit suites pass with the warm owner unavailable).
5. Nothing but its own tests imports `onscreen.py`; the file itself is deleted by LINT (R2), not here.
**Start from:** `T/typescript/src/lib/transition-spans.ts`, `tracks.ts`, `render-bounds.ts`; `A/astrid/core/timeline/onscreen.py` (`role_of` 138, `layout_bounds` 193, `visible_at` 374, `coverage` 424); callers `A/astrid/sdk/timeline/check.py`, `A/astrid/sdk/timeline/reflow.py` (~986-1001, `role_of`), `A/astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py` (~26-31); `A/astrid/core/timeline/duration.py` (Python mirror of timing); tests `A/tests/core/timeline/test_onscreen.py`, `test_onscreen_more.py`, `A/tests/packs/rendering/test_labels_overlay.py`, `test_bounds_plumbing.py`. Use `Checkout.resolve()` for the document until the compiler lands.
**Not in scope:** the App Player (PLAYER); audio mix serialisation; per-component internals; motion and extensions (R3).
**Depends on:** G#pins-astrid (the App pin matters only for PLAYER). (The compiler dependency is dropped: the evaluation reads compiled fields that `resolve()` already writes.)
**Why xhard:** A new shared evaluation extracted from the composition, with a cross-language client and cache; it feeds publish-blocking checks.
**Design detail:** `production/review/optimization/r4-review-20261015/astra-overengineering.md` section 1.

### PLAYER: the App Player uses the same evaluation
`G · R1 · 2 d · xhard · produces G#evaluator-film` · replaces R-EVAL (App side)
**Goal:** The App Player and the renderer agree on what is drawn and heard for every feature the v8 film uses.
**Done when:**
1. The Player consumes the shared evaluation through an injected asset and component host, for: output roles, occurrence projection, source mapping, track scale, transition ownership (including the App's incoming-transition conversion), element speed, audio fades.
2. Legacy text and card fixtures look unchanged (preservation: same output as before the card).
3. Text and card identities are separate and there is one transform order; existing films keep their look.
4. The App's affected unit tests pass.
**Start from:** `P/src/tools/video-editor/compositions/TimelineRenderer.tsx` (about 1,870 lines); `P/src/tools/video-editor/transitions/registry/TransitionRegistry.ts`, `transitions/validation.ts`; `P/src/tools/video-editor/render/renderPipeline.ts`; `P/vendor/timeline-composition/typescript/src/`; `A/remotion/src/Root.tsx`.
**Not in scope:** the parity harness (PARITY); motion, extensions, new transitions (R3); the 45-boundary matrix.
**Depends on:** G#eval, G#pins.
**Why xhard:** Rule 1: re-bases the 1,871-line Player on the shared evaluation; a legacy film's look or sound can change quietly.
**Design detail:** `briefs/WS-RENDER.md` (R-EVAL row).

### RENDER-PARITY: Player versus render spot-check harness
`G · R1 · 1 d · normal · produces G#render-parity` · replaces R-EVAL (checks)
**Goal:** A harness proves the Player and the render agree at chosen frames and samples, and catches a planted difference.
**Done when:**
1. A harness runs Player vs render with audio at event-centred frames (pixel MAE <= 2/255; region <= 8/255) and audio (PCM 1 sample / 0.1 dB).
2. A planted 1 px shift and a planted 0.5 dB gain change each fail it (tests).
3. It runs only at integration points, never per card.
4. GATE scenario 5 is added and runs this harness on the v8 film.
**Start from:** `A/tests/editing_conformance/runner.py` (the existing harness); `A/tests/editing_scenarios/`; `A/tests/golden/`; `A/astrid/packs/rendering/actions/timeline_visualize/composed_frame.py`. Place the GATE scenario beside the others the GATE card (A) creates.
**Not in scope:** motion or extension rows (FULL-MOTION, FULL-AUDIO-EXT); running the full 45-boundary matrix per card.
**Depends on:** G#evaluator-film.
**Design detail:** `briefs/WS-RENDER.md` (R-EVAL row).

### CHANGE-VIEW: changed-frame intervals that never under-report
`G · R1 · 2.5 d · xhard · produces G#change-view` · replaces R-SEE
**Goal:** Given two revisions, the tool lists the frame and audio intervals that may have changed, and never omits a changed frame.
**Done when:**
1. Every changed frame or sample in the exhaustive synthetic fixtures lies inside the reported intervals (test). An unknown dependency widens the interval; skipped intervals are listed.
2. Coverage questions ("is this layer visible here?") are answered from the shared evaluation with an explicit "unknown": the fixtures are two half-opacity plates, sprite holes, crop/mask, stale bounds, source-only layers, and the past-end case.
3. The existing `verify`, `sweep` and `compare` still work and call the new intervals; no new verbs.
4. Rendering the intervals is not part of the card's tests.
5. Parity: the aliases are kept: `edit --verify/--sweep/--no-sweep` (and the auto sweep), `check --at/--sweep/--labels/--timings/--zoom/--region`, `visualize --compare published`; `test_cli_verify.py`, `test_fast_lane_words.py`, `test_sweep_verdicts.py`, `test_cli_v3_sweep_log.py`, `test_labels_overlay.py` pass unmodified (or the change has a `tests/parity/removed.yaml` line).
**Start from:** `A/astrid/packs/rendering/actions/timeline_visualize/revision_diff.py`; `fast_lane.py::verify` (775); `sweep.py`; `A/astrid/sdk/authoring_revision_diff.py` and `A/astrid/core/timeline/authoring_revision_diff.py`; tests `A/tests/sdk/test_timeline_revision_diff_admission.py`, `A/tests/sdk/test_authoring_revision_diff.py`, `A/tests/packs/rendering/test_fast_lane.py`; the shared evaluation from EVAL.
**Not in scope:** pixel comparison as the source of truth; new command verbs; audio review beyond the intervals.
**Depends on:** G#eval, D#commands.
**Why xhard:** "Never under-reports" needs dependency and interval analysis, and under-reporting is silent by nature.
**Design detail:** none; kept whole (do not split).

### CHECKS: typed param validation and change descriptions
`G · R1 · 1.25 d · normal · produces G#checks` · replaces UX-CHECK + UX-CHANGES
**Goal:** `check` rejects any stored param the schema would reject, including null, and every re-flow lists the changes it made beyond the request.
**Done when:**
1. `check` runs the existing `validate_param_value` over stored params and no longer skips None. A stored `italicWord: null` fails as `c11.row1.italicWord: null is not a string` (red before, green after).
2. A valid film's `check` output is unchanged (preservation).
3. The change description lists beyond-request changes: bed seams (count, times), rewritten reference spellings (old to new, e.g. c14, c15), clamps, moments that moved to a different word. The v9 re-flow fixture lists its 5 bed seams and both renumbered references.
4. After a second re-flow, no duplicate piece ids and no seam on a seam appear in the description fixture (the cause is fixed by the timing cards; this card only reports what is there).
5. Parity: every blocking and note code in the parity inventory fires identically on the v8 duplicate before and after (GAP/`picture`, EMPTY, DIP, OFFCANVAS, MIXED-SCALE, DAMAGED-ART, `why`, `text`, `look`), except the deliberate opacity fix (listed in `removed.yaml`).
6. A parameter or look field the pinned renderer ignores is named on the edit line itself, not only in the check block; `visualize-extend.md`'s check recipe moves to the shared-evaluation interface, and an existing `CHECK` module still loads.
**Start from:** `A/astrid/sdk/timeline/model.py` (`validate_param_value` 101, skips None at 111; called at ~495); `A/astrid/sdk/timeline/check.py` (`_type_mismatches` 488, `describe_changes` 762); `A/astrid/sdk/timeline/reflow.py` (notes ~162-171, 272-279); `A/astrid/core/timeline/music_edit.py` (`plan_keep_end` 180); tests `A/tests/sdk/test_timeline_param_values.py`, `test_timeline_reflow_golden.py`, `test_timeline_reflow_keep.py`.
**Not in scope:** the on-screen rules (OFFCANVAS, MIXED-SCALE, `check --at`), which move with EVAL; fitting the bed once per re-flow (BED-CLOCK); a full v11 replay.
**Depends on:** none (configured review: the schema half has no dependencies; the seam text reads what reflow already records).
**Design detail:** `briefs/WS-AGENT.md` (UX-CHECK, UX-CHANGES rows).

### SHOW: show filters, cut ranges and quiet output
`G · R1 · 1.5 d · normal · produces G#show` · replaces V-1 (part 1) + UX-QUIET's reminder half
**Goal:** `show` answers cut ranges, references and filters honestly, and prints each orphan and reminder once.
**Done when:**
1. `show --as script --range c06..c12` returns that cut range. Today it fails with "could not convert string to float: 'c06'" (path: `cli_show.py:289-292` to `timeline_cuts._parse_range` to `float()`). Resolve cut ids the way `cli_show.py` ~226-238 already does. Red before, green after.
2. `show REF` accepts qualified paths and prints a ready edit line. Filters say what they excluded. Machine output (`--json`) is uncapped.
3. "Why still true?" reminders appear only for cuts whose words or picture changed (the v9 re-flow reminds only c07, c08, c10, c11, c13). Each orphan is named once per save, not once per edit.
4. `show` has one filter family (addresses); the bounded-inspection flags are kept as aliases.
5. Parity: `test_timeline_show_views.py` and the v10 show tests pass unmodified (or the change has a `tests/parity/removed.yaml` line).
**Start from:** `A/astrid/packs/timeline/cli_show.py` (289-292); `A/astrid/sdk/timeline_cuts.py` (`_parse_range` ~514); `A/astrid/sdk/timeline_views.py`; `A/astrid/sdk/timeline_script.py`; `A/astrid/sdk/timeline/checkout.py` (notes ~40, 141, 319-325); `A/astrid/sdk/timeline/reflow.py` (~170); `A/astrid/packs/timeline/cli.py` and `cli_parser.py` (edit help); tests `A/tests/sdk/test_timeline_show_views.py`, `test_timeline_script.py`, `test_timeline_cuts.py`.
**Not in scope:** `tasks list` / `runs show` output; `media open --materialize`; visualize views (VISUALIZE); changing what counts as an orphan.
**Depends on:** D#commands, F#cuts.
**Design detail:** `briefs/WS-AGENT.md` (V-1, UX-QUIET rows).

### VOCAB: one spelling per meaning
`G · R1 · 1 d · normal · produces G#vocab` · new (UX-QUIET's help half, grown per opus-agent-experience §2)
**Goal:** Each meaning has one spelling in help and in the skill; an old spelling becomes a hidden alias only where it means the same thing.
**Done when:**
1. `edit --help` is ≤ 40 lines showing the ~16 canonical flags (`opus-agent-experience.md` §2), with `--help-all` listing every alias.
2. A spelling folds into a canonical verb as a hidden alias only where it means the same thing, proven by item 5; one that fails item 5 stays its own verb. `words` (spoken words) and `lines` (narration lines), `log` (the edit journal) and `history` (revisions and lifecycle), and the read-only `script` (SCRIPT-EDIT) stay separate verbs. Narration edit flags move to `lines`; old spellings still parse.
3. `visualize` has one compare spelling.
4. The conformance scenarios pass unchanged through the old spellings; the parity test shows no removal.
5. Each folded alias gives output equal to its canonical verb on the same fixture, byte for byte apart from the invoked name (one test per alias).
**Start from:** the REGISTRY's alias declarations; `astrid/packs/timeline/cli.py` (`COMMANDS`, `_configure_edit`); `opus-agent-experience.md` §2 (the proposed 22-verb set).
**Not in scope:** removing any alias or verb; folding verbs that mean different things; new verbs.
**Depends on:** D#registry.

### VISUALIZE: views agree with show and the sheet
`G · R1 · 1.5 d · normal · produces G#views` · replaces V-1 (part 2)
**Goal:** `visualize`, `show` and the sheet give the same cut, time and frame answers for one fixture.
**Done when:**
1. One agreement fixture checks the cut table, the sheet, the script view, the frame index and the revision diff against each other (same cut ids, times, frame numbers).
2. `visualize` at a cut address draws a middle frame, not the first.
3. Tonight's restored visualize presets and working copy are the starting point and still work (their existing tests pass).
4. The test uses document text and the shared evaluation only; it renders no frames.
5. Parity: every preset, view and layer in the inventory still parses and renders; `test_timeline_visualize_overview.py`, `test_timeline_visualize_motion_views.py`, `test_visualize_drafts.py`, `test_visualize_export.py`, `test_render_review.py`, `test_timeline_visualize_cli_grammar.py` and the v10 visualize tests pass unmodified (or the change has a `tests/parity/removed.yaml` line).
**Start from:** `A/astrid/packs/timeline/cli_visualize.py`; `A/astrid/packs/rendering/actions/timeline_visualize/` (`contact_sheet.py`, `filmstrip_*.py`, `navigation.py`, `revision_diff.py`, `sweep.py`); `A/astrid/sdk/timeline_sheet.py`; `A/astrid/sdk/timeline_views.py`; tests `A/tests/sdk/test_timeline_sheet.py`, `test_timeline_show_views.py`, `test_timeline_visualize_public_surface.py`, `A/tests/packs/rendering/test_inspector_navigation.py`.
**Not in scope:** a new viewer; the audio lane (AUDIO-LANE); rendering in tests.
**Depends on:** G#show, G#eval.
**Design detail:** `briefs/WS-AGENT.md` (V-1 row).

### FULL-MOTION: motion rows in the parity matrix
`G · R3 · 1.5 d · normal · produces G#full-motion` · replaces R-FULL (motion)
**Goal:** Every motion row passes Player-versus-render parity.
**Done when:**
1. The PARITY harness has a row for each motion feature MOTION adds (easing, loop phase on a beat, fit curves, modifiers), and every row passes. There is no "blocked" row: a failing row becomes a fix card in its owning project, and this card waits for it.
2. The planted-change tests still fail correctly with these rows included.
**Start from:** the PARITY harness; `A/astrid/packs/astrid_motion/` (`A/tests/packs/astrid_motion/`); `P/src/tools/video-editor/keyframes/index.ts`.
**Not in scope:** new motion features; extension rows.
**Depends on:** G#render-parity, I#motion.

### FULL-AUDIO-EXT: audio and extension rows in the parity matrix
`G · R3 · 1.5 d · normal · produces G#full-audio-ext` · replaces R-FULL (audio + extensions)
**Goal:** Audio (envelopes, switches, ducks) and the proven extension contributions pass parity.
**Done when:**
1. Rows exist for envelope fades, a paired crossfade, a seam fade, a duck, a contributed curve, a contributed transition and a contributed component, and every row passes. There is no "blocked" row: a failing row becomes a fix card in its owning project, and this card waits for it.
2. Planted +-1 dB and 1 sample changes fail.
**Start from:** the PARITY harness; `A/astrid/core/timeline/audio_curves.json` and `audio_curves.py`; `A/tests/test_audio_curves.py`; the ENVELOPE, EXT-CURVES and EXT-COMPONENT outputs.
**Not in scope:** new audio features; the music bed itself (BED-CLOCK).
**Depends on:** G#render-parity, I#audio, J#curves, J#ext-component.

### RETIRE-EVAL: delete the duplicate evaluators
`G · R3 · 0.75 d · normal · produces G#full-parity` · replaces R-FULL (retirement)
**Goal:** One evaluation is left in each repo; the duplicates and their tests are gone.
**Done when:**
1. `core/timeline/onscreen.py` (if still present), the Python timing mirror used only for visibility, and the App-only duplicate semantics are deleted with their tests.
2. No importer of a deleted module remains (grep is clean); the affected tests and the PARITY harness pass.
**Start from:** `A/astrid/core/timeline/onscreen.py`, `A/astrid/core/timeline/duration.py`; `A/tests/core/timeline/test_onscreen*.py`; the Player code PLAYER left in place.
**Not in scope:** new behaviour.
**Depends on:** G#full-motion, G#full-audio-ext.

---

## H: Hosted security (Q-T = the paired relay and Q-S1–S6 were decided on 11 Oct, as recommended)

Run adversarial checks on disposable fixtures first. No real film data goes through any of these until the matching canaries fail as specified.

### ROUTES: route allowlists and size caps
`H · R1 · 1.5 d · xhard · produces H#route-proof` · replaces H-TRANSPORT (part 1)
**Goal:** The hosted relay lets through exactly the routes and headers the App uses, with explicit size handling, proven on disposable data.
**Done when:**
1. Allowlists are generated from their consumers (the App's generated client, project chat, inspect, history/restore, the commit route on the Runtime). Every other route and header is denied by test.
2. Today's relay lacks the editing routes (regex at `pairedRoutePolicy.ts:27` has no composition-revisions or commit routes); they pass after this card.
3. Size: v8's save payloads are measured; the 128 KiB JSON cap is raised, chunked or sent as an object, and a v8 save passes. The loopback cap (1 MiB) is tested separately.
4. A hostile-header canary is refused.
**Start from:** `P/config/vite/pairedRoutePolicy.ts` (`PAIRED_MAX_JSON_BYTES` line 4); `P/config/vite/pairedRelay.ts`, `pairedRegistry.ts`, `astridProxySecurity.ts`, `astridBridgeProxy.ts`; `R/runtime_protocol/daemon.py` (allowlist). The spec says the relay strips `X-Astrid-Session`; that string was not found in the App or Astrid, so confirm it before writing a test for it.
**Not in scope:** credentials; WSS; the grant.
**Depends on:** A#base.
**Why xhard:** Rule 1: the allowlist is an auth boundary; one that is too wide fails silently, and "every other route is denied" can't be enumerated.
**Design detail:** `spec-hardening.md` section 5.

### CREDENTIALS: one credential format and the commit mount
`H · R1 · 1.5 d · xhard · produces H#credentials` · replaces H-TRANSPORT (part 2)
**Goal:** One versioned credential returns its granted scopes, expires, and is the only way to reach the commit route.
**Done when:**
1. An expired credential is refused; a credential in an old format is refused with a named error; the parser returns the granted scopes.
2. The commit route (on the Runtime, owned by ACCEPT) is reachable on both the relay and the loopback transport with the scoped credential only.
3. A request with no credential, or with a credential for another project, is refused (canary).
**Start from:** `A/astrid/core/execution/provider_route_grant.py` (existing grant shape); `R/runtime_protocol/service.py`; `R/runtime_protocol/daemon.py`; `P/config/vite/astridProxySecurity.ts`.
**Not in scope:** the local agent grant (GRANT); WSS.
**Depends on:** H#route-proof, D#commit-service.
**Why xhard:** f4 = 2: credential format, scopes and expiry on two transports; the threat model is the card.
**Design detail:** `spec-hardening.md` section 5.

### TRANSPORT: the paired relay, helpers and sandbox
`H · R1 · 2 d · xhard · produces H#transport` · replaces H-TRANSPORT (part 3)
**Goal:** The paired relay (the user's 11 Oct choice) is enforced, helpers reject hostile callers, and active content cannot reach the app origin.
**Done when:**
1. The existing relay binding is extended and tested, not rebuilt: `P/config/vite/pairedRelay.ts` (~216, `onConnectorMessage`) already accepts a response only from the connector and generation that took the request. The relay is served over WSS, and a cross-connector or stale-generation response injection is refused (canaries).
2. Internal helper calls are authenticated with exact endpoint identity and loopback-bind assertions. A second LAN machine and a hostile-Origin call cannot reach a helper (canaries).
3. An HTML/SVG canary runs only on a sandboxed origin.
**Start from:** `R/runtime_protocol/daemon.py`; `R/runtime_protocol/service.py`; `P/config/vite/pairedRelay.ts`, `pairedRegistry.ts`, `astridProxySecurity.ts`; `P/scripts/dev-local-workspace.mjs`.
**Not in scope:** the grant and revocation; per-card real-traffic runs.
**Depends on:** H#credentials.
**Why xhard:** hardens the paired relay's binding, helper authentication and a sandboxed origin across the App and the Runtime; security is central.
**Design detail:** `spec-hardening.md` sections 5-6.

### GRANT: a bound local grant
`H · R1 · 1.5 d · xhard · produces H#grant-core` · replaces H-GRANT (part 1)
**Goal:** A local grant bounds what a browser session's agent may do.
**Done when:**
1. A grant is bound to {realm, browser session, projects, operations, expiry}. A request outside it is refused with a named structured decision (no title-based approval).
2. An expired grant is refused; a forged actor or session and a cross-project claim are refused (canaries).
3. An authorised visualize, edit and render still works.
4. Per the Q-S1..S6 decisions (11 Oct) (the default authority is edit, visualize and render of the selected project; anything wider needs local approval).
**Start from:** `A/astrid/core/execution/provider_route_grant.py`; `A/astrid/core/execution/custody_broker.py`; `R/runtime_protocol/service.py` (capability decision path); `A/astrid/omp_agent.py` and `P/scripts/reigh-acp-bridge.ts` (how agents launch today).
**Not in scope:** confinement; revocation.
**Depends on:** H#route-proof.
**Why xhard:** f4 = 2: enforcing a grant over session, project and operation; the threat model is the card.
**Design detail:** `spec-hardening.md` section 6 (SEC-1).

### CONFINE-SPIKE: choose the confinement mechanism
`H · R1 · 0.5 d · xhard · produces H#confine-mechanism` · split from CONFINE (the spike)
**Goal:** The mechanism that confines an agent and its descendants is chosen and named from what exists, and CONFINE is sized from it.
**Done when:**
1. What exists is inventoried in the card result: pack code's attempt-scoped channel with no credential access (`_child_bridge.py`), the ACP bridge, the local worker supervisor, and what each confines today.
2. The mechanism is named, with one proof-of-concept canary showing it refuses a file read outside a grant.
3. CONFINE is re-estimated from the spike; above 3 d, the orchestrator splits it before it starts.
**Start from:** `A/astrid/sdk/_child_bridge.py`; `A/astrid/omp_agent.py`; `P/scripts/reigh-acp-bridge.ts`; `R/runtime_protocol/local_worker.py`, `local_execution_supervisor.py`; `A/tests/sdk/test_child_bridge_d18.py`.
**Not in scope:** building the confinement (CONFINE); the grant (GRANT).
**Depends on:** A#base.
**Why xhard:** an open security design decision; a mechanism that looks confining but leaks descendants passes a shallow canary.
**Design detail:** `spec-hardening.md` section 6 (SEC-1).

### CONFINE: confinement of delegated work
`H · R1 · 1.5 d · xhard · produces H#confine` · replaces H-GRANT (part 2); size provisional until CONFINE-SPIKE
**Goal:** An agent and its descendants cannot reach outside the grant.
**Done when:**
1. Built on the mechanism CONFINE-SPIKE named: reading outside files or credentials, writing outside, and unapproved egress are refused, for the agent and a descendant process (canaries).
2. The agent environment is sanitised; caller MCP config cannot widen the grant.
3. A deceptive tool title does not get approval.
**Start from:** CONFINE-SPIKE's result; `A/astrid/sdk/_child_bridge.py`; `A/astrid/omp_agent.py`; `P/scripts/reigh-acp-bridge.ts`; `R/runtime_protocol/local_worker.py`, `local_execution_supervisor.py`; `A/astrid/core/execution/custody_broker.py`; `A/tests/sdk/test_child_bridge_d18.py`.
**Not in scope:** revocation.
**Depends on:** H#grant-core, H#confine-mechanism.
**Why xhard:** a security boundary across Astrid, the Runtime and the App's bridge, which canaries can show only partially.
**Design detail:** `spec-hardening.md` section 6 (SEC-1).

### REVOKE: revocation and fencing
`H · R1 · 1 d · xhard · produces H#grant` · replaces H-GRANT (part 3)
**Goal:** Revoking a grant stops delegated work and no restart revives it.
**Done when:**
1. "Disconnect", "revoke the grant" and "stop delegated work" are three separate actions. A revoke during an upload, a prompt or a render is honoured (running renders follow Q-S4: stop and fence publication).
2. New actions and commits after revoke are refused (fenced).
3. A reconnect or restart does not revive the grant, without relying on the close-reason string (canaries).
**Start from:** `R/runtime_protocol/daemon.py` (disconnect/reconnect); `R/runtime_protocol/service.py`; `R/runtime_protocol/local_execution_supervisor.py`.
**Not in scope:** the grant format; the full E-4 matrix (an integration point).
**Depends on:** H#confine.
**Why xhard:** f4 = 2: fencing, revoking mid-render, and no revival after a restart.
**Design detail:** `spec-hardening.md` section 6 (SEC-3).

---

## I: Story, motion, audio (Release 2)

### STORY: chapters keep their target kind
`I · R2 · 1.5 d · xhard · produces I#story` · replaces M8
**Goal:** Story ranges migrate so each chapter start frame is exactly where it is today.
**Done when:**
1. Story ranges (chapters and beats) are stored as `app.astrid.ranges`, half-open, chapters non-overlapping, and migration keeps the resolved target kind (the first-word picture exception). Every chapter and beat start frame is identical before and after migration on every fixture film (tiny, golden, v8, v9, v11); on v8 the 8 chapter start frames equal the golden baseline.
2. `swap` does not move chapters; `move n20a` moves its chapter and nothing else.
3. An unanchored cut keeps a legacy range plus a finding. Migrating twice changes nothing.
**Start from:** `A/astrid/core/timeline/astrid_ns.py` (`FILM_INTENT_KEYS` line 22 has `chapters`); `A/astrid/sdk/timeline/reflow.py` (chapter handling ~670-690); `A/astrid/sdk/timeline/store.py`; `A/tests/golden/`.
**Not in scope:** story UI; beat detection; chapter authoring commands.
**Depends on:** F#compiler, F#cuts, A#golden-baseline.
**Why xhard:** migrates story ranges, a timing invariant; a chapter that moves by a frame is silent until someone watches.
**Design detail:** `spec-later.md` (M8 row).

### MOTION-CONTRACT: the clock, trim and keyframe origin
`I · R2 · 1 d · xhard · produces I#motion-contract` · replaces MO (part 1)
**Goal:** Keyframes have one declared clip-local origin, and the App and Astrid read it the same way.
**Done when:**
1. The origin is declared per clip. A trim does not shift keyframe times.
2. The App's timeline-seconds keys and the donor's local-frame sprite keys each have an adapter with a test.
3. L13-01 to L13-03 pass.
4. Existing films keep their keyframes: on tiny, golden and v8 (every clip with keyframes), keyframe times compile identically and frames at the keyframe instants render identically once the origin is declared; a legacy clip with no declared origin defaults to the origin it uses today.
**Start from:** `P/src/tools/video-editor/keyframes/index.ts` (`interpolateLinear` 56, `interpolateHold` 73, `resolveAnimatedParams` 411); `A/astrid/core/timeline/clip_fields.py` (`_EASINGS` ~32); `A/astrid/packs/astrid_motion/`; `T/typescript/src/lib/animations.tsx`, `trim.ts`.
**Not in scope:** easing curves, loop phase, modifiers (MOTION).
**Depends on:** F#compiler, G#eval.
**Why xhard:** f4 = 2: clock, trim and keyframe-origin algebra across App, Astrid and the composition; existing keyframes can shift silently.
**Design detail:** `spec-later.md` (MO row).

### MOTION: easing, loop phase, fit curves, modifiers
`I · R2 · 1.5 d · xhard · produces I#motion` · replaces MO (part 2)
**Goal:** Motion features run on the contract, with Player/render parity rows.
**Done when:**
1. Easing, a loop phase landing on a beat, and fit curves work; the R-13 matrix row passes; modifiers are components with a declared contract.
2. L13-04 and L13-05 pass.
3. Existing films' keyframes are unchanged by the motion features: the MOTION-CONTRACT check on tiny, golden and v8 passes again after this card.
**Start from:** the MOTION-CONTRACT adapters; `P/src/tools/video-editor/keyframes/index.ts`; `A/astrid/core/timeline/clip_fields.py`; `A/astrid/packs/local/rendering/elements/` and `A/astrid/packs/rendering/rendering/elements/` (existing components).
**Not in scope:** new motion UI; the full parity run (FULL-MOTION).
**Depends on:** I#motion-contract.
**Why xhard:** f3 = 2: the modifier contract is undecided; new features across 3 repos.

### TRANSITIONS: one ownership rule
`I · R2 · 1 d · xhard · produces I#transitions` · replaces V-3 (part 1)
**Goal:** Each transition has one owner on a track and a declared implementation.
**Done when:**
1. A same-track overlap is refused with a next step (one rule: refused, never resolved; test, with gaps and overlaps).
2. The App's `{type, duration, params}` converts to the declaration; legacy transitions compile unchanged, checked over all transition fixtures (`fixture_transition.json` and the others) and v8's boundaries.
3. An unsupported host is refused explicitly.
**Start from:** `P/src/tools/video-editor/transitions/registry/TransitionRegistry.ts`, `transitions/validation.ts`, `catalog.ts`; `T/typescript/src/lib/transition-spans.ts`, `transitions.tsx`; `A/tests/golden/fixture_transition.json`.
**Not in scope:** audio crossfades and envelopes (ENVELOPE).
**Depends on:** G#eval.
**Why xhard:** changes transition ownership across the App, the composition and Astrid; a legacy transition that compiles differently changes the film silently.
**Design detail:** `spec-later.md` (V-3 row).

### ENVELOPE: one audio gain primitive
`I · R2 · 2 d · xhard · produces I#audio` · replaces V-3 (part 2)
**Goal:** Fades, paired switches, seam fades and duck all compile to one `audio.envelope` that the renderer and Player consume.
**Done when:**
1. `audio.envelope` is ordered keyframes `{at, value}` with a curve id per segment, evaluated at sample time. Curve shapes come only from the registry (`audio_curves.json`: linear, equal-power, exponential-fast, exponential-slow, s-curve), which the packaged composition must read (today it does not read `fadeInCurve`/`fadeOutCurve`).
2. Legacy `fadeIn`/`fadeOut` compile to linear segments and the sound is unchanged (preservation). The renderer does not apply a legacy fade again after projection.
3. A narration duck follows a re-flow within +-1 dB, and a planted +-1 dB change fails (sample level). Where ducks overlap, the strongest applies.
4. One generic paired crossfade and one seam fade match between Player and encoded output; an unknown curve or unsupported host is refused with a named code (`ENVELOPE_UNRENDERED`, `DUCK_UNRENDERED`).
5. The existing R-7 cells pass.
**Start from:** `A/astrid/core/timeline/audio_curves.json`, `audio_curves.py`, `audio_curves.generated.ts`; `A/scripts/gen_audio_curves.py`; `A/astrid/core/timeline/clip_fields.py` (fades ~505-565); `A/astrid/packs/rendering/rendering/renderers/ffmpeg/support.py` (~257); `T/typescript/src/lib/fade.ts`; `A/tests/test_audio_curves.py`, `A/tests/packs/rendering/test_ffmpeg_support.py`, `A/tests/packs/test_audio_render.py`. No duck exists in the timeline renderer today (only in the chiptune synth).
**Not in scope:** the music-bed arrangement switches (BED-ADOPT/BED-CLOCK); loudness normalisation; a fade renderer per curve type.
**Depends on:** G#evaluator-film, F#music-segments.
**Why xhard:** A new audio primitive evaluated at sample time, with a double-fade risk and ducks (the timeline renderer has none today).
**Design detail:** `production/review/optimization/fleet/m4-music-clock.out.md` section 2.

### LINT: targeted lint over the shared evaluation
`I · R2 · 1 d · normal · produces I#lint` · replaces V-2
**Goal:** Lint finds a frozen sequence or a blank plate from the shared evaluation, and the last `onscreen.py` caller is gone.
**Done when:**
1. The L6-01 fixture flags; the carried-layer and shift fixtures are clean; no false UNEXPECTED; the stale-why text is consistent.
2. Nothing imports `core/timeline/onscreen.py` (if EVAL left a caller, move it here, then delete the file with its tests).
3. Parity: deletes `core/timeline/onscreen.py` once EVAL has moved its callers; motion-lint codes (FACE FRAME SAFE SMALL COVER EDGE SYNC SFX BEAT SHORT HOLD LONG SHARE LEVEL FROZEN) and `lint --rules/--list-checks/--strict/--only` are kept; `boxes_at` stays a labelled "estimated" source until the evaluation supplies boxes.
**Start from:** `A/astrid/core/timeline/onscreen.py`; `A/astrid/sdk/timeline/check.py`; `A/astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py`; `A/tests/core/timeline/test_onscreen*.py`.
**Not in scope:** a lint framework; visualize changes.
**Depends on:** G#eval.

### COPY-SYNC: on-screen copy that quotes the script
`I · R2 · 1 d · xhard · produces I#copy-sync`
**Goal:** A text layer declares the words it quotes, and a script change lists every layer that quotes them.
**Done when:**
1. A quote declaration on a text layer survives save and reload.
2. A script change lists every quoting layer as stale.
3. The v11 copy list ("58 days.", "LIFETIME", "Problem 01/02", "PART 02", "READY:", the agents' goals) comes out of the tool with no hand search.
4. Lint flags on-screen text that no longer matches nearby speech (three fixtures).
**Start from:** `A/astrid/sdk/timeline/reflow.py` (script change path); `A/astrid/sdk/timeline/check.py`; `A/astrid/sdk/timeline_script.py`; word identity from F; `A/astrid/core/timeline/moments.py`; the change intervals from CHANGE-VIEW (or the reflow record if absent).
**Not in scope:** automatic copy rewriting; LLM matching.
**Depends on:** F#timing-fixes, G#change-view.
**Why xhard:** f3 = 2: detecting quotes without an LLM (the v11 copy list "with no hand search") is open design.

### BED-ADOPT: adopt a music bed
`I · R2 · 2 d · xhard · produces I#bed` · replaces MUSIC-CLOCK (part 1)
**Goal:** Aligned plain music clips become one authored, cut-free bed with named arrangements and word-centred switches, without changing what is heard.
**Done when:**
1. `adopt music-bed` (a new verb; note `timeline_adopt.py` is a different feature) checks alignment and writes the bed under `app.astrid.bed`: arrangements `{id, asset, source_offset_s, rate, gain}` and ordered switches `{id, on: TimeRef, duration, curve}`. It refuses an ambiguous or low-confidence alignment.
2. On a duplicate of film-5898e92b, adoption preserves today's three source spans, gains and the 3 s / 4 s overlaps. Switch 1 is `"First" in y08 #1 +1f` (3 s); switch 2 is `"A" in y20c #1 -2f` (4 s). Source minus film offsets are 0, 0 and 39.06 s.
3. A film with plain clips that is not adopted compiles byte-identical to today.
4. A switch on a word re-resolves, or becomes `ORPHAN` with a re-home action; it is never re-bound to the nearest word. Overlapping switch windows implying three active arrangements, a window outside source coverage, or a negative interval are refused.
5. Older clients refuse edits to an adopted bed by capability check.
**Start from:** `A/astrid/core/timeline/music_edit.py` (`plan_keep_end` 180); `A/astrid/sdk/timeline/reflow.py` (`_apply_bed_cuts` 1139); `A/astrid/packs/music/actions/align/run.py` (evidence only, never an automatic retime), `level`, `beats`; `A/astrid/core/timeline/astrid_ns.py`; `A/astrid/core/timeline/moments.py`; `A/astrid/packs/timeline/cli_music.py`; the film snapshot `production/review/optimization/fleet/evidence/film-5898e92b.json`; tests `A/tests/core/timeline/test_music_edit.py`, `A/tests/sdk/test_timeline_music_policy.py`, `test_timeline_reflow_keep.py`, `A/tests/packs/music/test_music_pack.py`.
**Not in scope:** keep-end changes (BED-CLOCK); the audio lane; a clock per arrangement; auto-normalising loudness; a beat detector in the compiler; reading every overlapping music clip as one tune.
**Depends on:** F#music-segments, D#commands.
**Why xhard:** f4 = 2: a new verb that rewrites the music as a bed "without changing what is heard"; TimeRef and offset algebra.
**Design detail:** `production/review/optimization/fleet/m4-music-clock.out.md` section 1.

### BED-CLOCK: one keep-end clock for every arrangement
`I · R2 · 2 d · xhard · produces I#music-clock` · replaces MUSIC-CLOCK (part 2)
**Goal:** A keep-end ripple makes one shared seam across all arrangements, and re-flows are idempotent.
**Done when:**
1. The musical coordinate `u` runs from the bed's start; arrangement `i` reads source time `source_offset_i + rate_i * u(t)`. A re-flow moving `"A" in y20c #1 -2f` moves the second overlap while the orchestral source stays at `u + 39.06`.
2. A keep-end ripple makes one shared seam (250 ms), compiled once from bed intent and ripple records, before projecting arrangements. A removal skips the same `u` span for all active sources; an opening repeats it.
3. Two re-flows of the v9-to-v11 shape give unique deterministic piece ids, no seam on a seam, and identical results the second time. Generated pieces are discarded and rebuilt each compile, never used as the next compile's input.
4. `plays_on` keeps `u` continuous and the change description warns that the bed may no longer end with the film.
5. The legacy evaluator and `:b` repair remain for un-enrolled ordinary/previously segmented legacy clips. An intact source enrolled by MUSIC-SEGMENTS uses the corrected source-derived compiler. Adopted arrangements extend that compiler, not a second keep-end engine.
**Start from:** `A/astrid/core/timeline/music_edit.py`; `A/astrid/sdk/timeline/reflow.py` (`_apply_bed_cuts` 1139); the compiler's `bed.seams` node from F; the ENVELOPE primitive for the seam fade.
**Not in scope:** the lane display; a persistent cut record; a new timeline clock or store.
**Depends on:** I#bed, I#audio.
**Why xhard:** f4 = 2: a shared musical coordinate, seam algebra and idempotent re-flows.
**Design detail:** `fleet/m4-music-clock.out.md` sections 1-2.

### AUDIO-LANE: one audio lane in sheet and visualize
`I · R2 · 1.5 d · normal · produces I#audio-lane` · replaces MUSIC-CLOCK (part 3)
**Goal:** The sheet, visualize and the App show the same resolved bed switches.
**Done when:**
1. `show --as sheet`'s `sound` section shows one bed row with indented arrangement spans: resolved `on` word and time, source window, gain (linear and dB), switch overlap bounds and curve, seam skip/repeat. Generated spans are marked read-only (`~`) with a ready command for their authored source.
2. Visualize draws the same lane model: spans, switch centres with TimeRef labels, seam markers.
3. For one fixture, show, sheet, visualize and the App agree on switch frames and generated ids. The final film-level run of this fixture is the MUSIC-CLOCK integration check.
4. Older clients are refused by a capability check, not silently. Machine output is uncapped.
**Start from:** `A/astrid/sdk/timeline_sheet.py` (`sound` section ~155, parsing ~324); `A/astrid/sdk/timeline_views.py`; `A/astrid/packs/rendering/actions/timeline_visualize/` (`render_svg.py`, `navigation.py`, `audio_analysis.py`); tests `A/tests/sdk/test_timeline_sheet.py`.
**Not in scope:** a waveform cache; a bespoke App panel; editing generated spans.
**Depends on:** I#music-clock, G#views.
**Design detail:** `fleet/m4-music-clock.out.md` section 4.

---

## J: Extensions (Release 3)

### EXT-ONE: one real contribution, end to end
`J · R3 · 2.5 d · xhard · produces J#ext-one` · replaces M9 (core) + SK-2
**Goal:** One contributed operation is admitted, invoked and identified through one extension mechanism, and a fresh agent can repeat it from a recipe.
**Done when:**
1. The mechanism is chosen while proving the operation in item 2, preferring the route production already uses: pack v3's manifest `extensions` (`permissions.py`, read by `core/pack/loader.py` and `core/rendering/registry.py`) over the restored `core/extensions/*` registry (89 tests, no production consumer). The choice and its reason are in the card result. The other mechanism is frozen (no new callers), not deleted, until its callers and compatibility obligations are known.
2. An operation that returns commands runs through discovery, schema and invocation using that mechanism, and passes the harness extension path. A same-name neighbour file cannot replace it (point-qualified identity); the implementation digest changes when the code changes.
3. A pack-builder recipe (one skill) is written, and a fresh agent follows it to build `fit_to_beats` (an operation); build time and stumbles are recorded.
4. Unsupported surfaces report "unsupported" explicitly.
**Start from:** `A/astrid/core/extensions/` (`registry.py`, `model.py`, `sidecar.py`, `scopes.py`; tests `A/tests/core/extensions/`); `A/astrid/core/pack/permissions.py` (lines 123-284: manifest `extensions`); `A/astrid/packs/rendering/pack.yaml` (V3 declarations); `A/tests/editing_conformance/runner.py` (the harness).
**Not in scope:** the view, component, check and generator kinds (EXT-VIEW, EXT-COMPONENT, EXT-CHECK-GEN build each with its first user); deleting the other mechanism; a bespoke App panel.
**Depends on:** D#commands, G#evaluator-film.
**Why xhard:** chooses the platform's extension mechanism, an open design decision, and a contribution's identity (point-qualified, digest over its code) is a load-bearing invariant.
**Design detail:** `fleet/m4-music-clock.out.md` section 3.

### EXT-VIEW: the view kind, proven by a fresh agent
`J · R3 · 2 d · xhard · produces J#ext-view` · new (restores the view kind of the five)
**Goal:** A contributed read-only view, declared once, appears in `show`, in `visualize` and in the App's views, and a fresh agent can build one from the recipe.
**Done when:**
1. A view declaration (id, schema, the read model it consumes, label/help) is admitted through the EXT-ONE mechanism; `timelines show --as <view>` and `visualize --view <view>` list and render it without per-view code.
2. The App lists the declared view in its views from the declaration (generic panel from the schema; no bespoke UI) via its extension surface.
3. A fresh agent follows the recipe to build `story_overview` (chapters and story beats at a glance); build time and stumbles are recorded.
4. A view never mutates: a test asserts zero journal entries and an unchanged document after rendering every declared view. An unsupported host reports "unsupported".
**Start from:** `A/astrid/sdk/timeline_views.py`; `A/astrid/packs/rendering/actions/timeline_visualize/layers/` (`builtin.py`, `base.py`); `P/src/tools/video-editor/runtime/extensionSurface.ts`, `useExtensionLoaderWiring.ts`; `reviews/astra-high-extensions.md` (view contract).
**Not in scope:** views that edit; a bespoke App panel per view.
**Depends on:** J#ext-one, G#views, I#story.
**Why xhard:** crosses Astrid and the App, and fixes the view contract every later contributed view relies on.

### EXT-COMPONENT: the component kind, proven by a fresh agent
`J · R3 · 2.5 d · xhard · produces J#ext-component` · new (restores the component kind of the five)
**Goal:** A contributed visual element, declared once, renders identically in the App Player and in exports, and a fresh agent can build one from the recipe.
**Done when:**
1. The modifier contract (how a component modifies the frame beneath it: inputs, bounds declaration, time origin) is written first and reviewed by the orchestrator before the build.
2. A component declaration (element id, params schema, bounds, render implementation) is admitted through the EXT-ONE mechanism; it is addable with `edit --add` and the App's add menu without per-element code; the shared evaluation reports its bounds (or "unknown").
3. A fresh agent follows the recipe to build `vignette` (darkened edges); Player and export agree on it at event-centred frames (the RENDER-PARITY harness; planted 1 px change fails).
4. A component without declared bounds gives coverage "unknown" with a named finding; an unsupported host refuses explicitly.
**Start from:** `A/astrid/packs/rendering/elements/` (`catalog.ts`), `A/astrid/core/rendering/registry.py`; the shared evaluation from EVAL; `P/src/tools/video-editor/clip-types/`, `effects/`, `runtime/extensionSurface.ts`; `reviews/astra-high-extensions.md` (component and modifier contracts).
**Not in scope:** new built-in elements; motion modifiers beyond what `vignette` needs.
**Depends on:** J#ext-one, G#render-parity, I#motion-contract.
**Why xhard:** the component contract crosses Astrid, the composition package and the App, and a mismatch silently changes how contributed elements look.

### EXT-CHECK-GEN: the check and generator kinds, each with a real first user
`J · R3 · 1.5 d · normal · produces J#proofs` · new (restores the check and generator kinds of the five)
**Goal:** A check and a generator are each declared once and appear where users meet them, proven by converting an existing one of each.
**Done when:**
1. Check kind: one existing check (e.g. DAMAGED-ART) becomes a declaration (finding codes, severity, what it reads) admitted through the EXT-ONE mechanism; `check` and `lint` run it unchanged (its existing tests pass unmodified) and list its codes in `lint --list-checks`.
2. Generator kind: one existing generator (e.g. `chiptune.compose`) becomes a declaration (inputs, the assets it produces) admitted the same way; its output lands as project media with the handle printed; the App's action form for it comes from the declaration.
3. The five kinds (operation, view, component, check, generator) are listed in the pack-builder recipe, each with its proof card and one example.
4. An unsupported host gets an explicit refusal.
**Start from:** `A/astrid/packs/rendering/actions/timeline_visualize/layers/builtin_checks.py`, `A/astrid/sdk/timeline/check.py`; `A/astrid/packs/chiptune/actions/compose/`; `P/src/tools/video-editor/capabilityManifest.ts`; the EXT-ONE mechanism.
**Not in scope:** new checks or generators beyond the two conversions.
**Depends on:** J#ext-one, J#curves, G#checks.

### EXT-CURVES: curves, transitions, music actions and command macros as declared contributions
`J · R3 · 1.5 d · normal · produces J#curves` · replaces M9 (remainder)
**Goal:** A new audio curve, transition, music action or command macro is added by one declaration, with no per-kind dispatch edit.
**Done when:**
1. A new curve entry appears in the Python and TypeScript consumers without editing dispatch (generated tables agree; endpoint and legacy-linear identity tests).
2. A contributed transition appears in the App registry and passes Player/render parity.
3. The music pack's actions (`music.align/level/beats`) are admitted as declared contributions through the EXT-ONE mechanism and appear in the CLI and SDK without per-action code; a command macro (an operation built from existing commands) is one declaration and journals as one undoable step.
4. An unsupported host gets an explicit refusal.
**Start from:** `A/astrid/core/timeline/audio_curves.json`, `A/scripts/gen_audio_curves.py`; `P/src/tools/video-editor/transitions/registry/`; `A/astrid/packs/music/`; the EXT-ONE mechanism.
**Not in scope:** new curve or transition designs beyond one each for the proof.
**Depends on:** J#ext-one, I#audio, I#transitions, G#render-parity.

## Astra098 supplemental requirements for existing cards

**Executable101 additions:** [exact contract](receipts/root-Astra101-transcript-producer-contract.md), SHA256 `3a8016f2eabf8f195129bc9ad9dfc4c99ebabe302ff75de8eab6b3d7bff63109`. D RUNNER/COMMIT/REBASE/SCRIPT-REFLOW must implement real authenticated `publish_transcript_source` (validated `media.transcript/v1`, one shared ID adapter, immutable CAS snapshot then document expectedVersion/idempotency), registered `transcript.bind`/`transcript.reference`, explicit source dependency/provenance validation and actual canonical persistence/inverse. B H-DATA/PRES-HARNESS must prove shared kind/ID schema goldens and lossless explicit legacy migration; F TIMING-FIXES/REPAIRS-REST connects source seconds/identity/maps/orphans through the existing clock/compiler. J EXT-CHECK-GEN and E GESTURES/WRITERS/REVIEW must prove an authenticated read-only mounted Caption Foundry callback submits those commands plus ordinary caption edits in one transaction, with persisted reload/undo/offline replay and zero source writes by the consumer. D/E's `ownerData.update` persists only declared owned nonreserved properties through the same runner, independently of caption binding. Full101 supplies exact fields, absent/clear/expectation rules, real synthetic positive flow and all provenance/revocation/mapping/migration negatives. This removes the absent-producer hold by assigning implementation; it does not claim upstream recovery, external film authority, acceptance or a new card/review stage.

The full cross-owner binding contract is in [the Astra098 amendment](amendments/20261016-upstream-transcript-extension-integration.md). These additions qualify existing cards and do not create card IDs, graph edges, or acceptance history:

- **A `CHECKPOINT-ASTRID`, `CHECKPOINT-RUNTIME`, `CONTRACT-COMMIT`:** selectively admit exact source tuples; combine upstream operations with the R4 commit/media/purge operations; regenerate one OpenAPI contract and generated clients. Do not blanket-rebase or reset accepted base proof.
- **B `H-DATA`, `PRES-HARNESS`:** preserve the existing hash-bound `config.app.transcript` declaration and its required fields/opaque metadata while adding `.references`; prove coexistence, round-trip, and explicit conflict-preserving migration from top-level `transcriptReferences`. Retain owner namespace/schema versions, opaque preservation, version refusal, and legacy track migration.
- **C `ACCEPT`, `HISTORY-WIRE`, `HISTORY`:** generate a finite supported-semantic-version set per operation and scope required profiles to features used. Test old baseline clients against additive `[1,2]` support, optional-feature absence while baseline works, baseline denial before realm load/mutation, false newer-version compatibility, legacy scalar-as-singleton, exact health/handshake identity/digest, and all existing grants. Names, events, cursor behavior, task batching, and schema migration remain supplementary checkpoint evidence.
- **D `RUNNER`, `COMMIT`, `REBASE`, `SCRIPT-REFLOW`:** use `config.app.transcript.references` for media associations/defaults and authoritative immutable `clip.app.transcript.binding` per occurrence. Only the validated semantic import/binding command writes provenance/snapshot fields; generic owner properties cannot forge provenance or derived timing. Default changes do not retarget clips without same-transaction rebind commands. Preserve pinned snapshot replay/undo boundaries and the authoring-bundle storage adapter with one film-owned track definition.
- **E `GESTURES`, `WRITERS`, `SAVE-ROUTING`, `REVIEW`:** preserve command-only writes and no hidden post-publish refresh. Review proposals pin base revision, ordered commands, and transcript bindings/digests; reject is unchanged, accept uses rebase/commit, retry is idempotent, and ACK grants no write authority.
- **F `TIMING-FIXES`, `REPAIRS-REST`:** preserve validated one-to-one word identity, explicit take mapping, orphan/refusal semantics, and source-clock trim/speed compilation through the existing compiler. Criterion 3 of REPAIRS-REST is amended above; no WORD-ID card is added.
- **G `PINS-ASTRID`, `PINS-APP`, `EVAL`, `PLAYER`, `RENDER-PARITY`:** retain renderer pin qualification and shared evaluation; transcript/track projections are derived and their dependencies are explicit.
- **H `ROUTES`, `CREDENTIALS`, `GRANT`:** prove the facade and compatibility advertisement do not widen route, project, actor, scope, endpoint, or runtime-identity authority.
- **I `STORY`, `MOTION-CONTRACT`, and existing audio/story cards:** validate chapter, occurrence, and source-clock preservation when consuming the storage adapter; no new product request or broad restart.
- **J `EXT-CHECK-GEN`:** add the thin document facade and schema/namespace declarations. Caption Foundry invokes the admitted transcript host's validated binding operation or owns only separately declared data; it cannot claim `transcript` ownership by name alone. Keep it alongside existing DAMAGED-ART, chiptune, and five-kind proofs. `EXT-ONE` remains accepted against its original four criteria and history.

---
