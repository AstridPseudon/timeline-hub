# Independent bootstrap and group-view review

2026-10-20. **A: HOLD for one bounded completion-authority correction. B: HOLD; the branch contains no group-view implementation.** Both remain unwired. Neither clears production bootstrap/group-writer retirement or qualifies a current Agent/Runtime release. Review complete; dispatch follow-up work without waiting on this worker.

## Pins, scope and size

Read PLAN first; retained its canonical shot ownership, guarded migration, one accepted history/outbox and consumer-before-route-retirement decisions. No decision was changed.

| Source | Exact tree reviewed | Size relative to `090e1162da94b4baabff0295c3267e00cc3d330f` |
| --- | --- | --- |
| Assigned review base | App integration `1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff` | Read-only |
| A, `tl/app-m2-bootstrap-init-native-stage` | `f0112b846c1084b0902cdba091442cc840d8e88d` | 8 files, +702/-6; product +208/-6 across 3 files; TS tests +442; Python parity +51; one-line golden 15,448 bytes |
| B, `tl/app-m2-canonical-group-read-view-stage` | `090e1162da94b4baabff0295c3267e00cc3d330f` | **0 files, 0 lines changed** |
| Frozen init authority | Agent `31d02d45ad21f452724091b94b285478d00c9c21` | Native init/capture source; not a current registered release |
| Held group authority | Agent `4a1dc1a84080effdc6a30c740303e75d9d189295` | Migration/move/view source and two exact goldens |
| Other owner storage candidates | D13 `c195d1ee19464692712857d65648e91a9b93bee3`; auto-placement `f89cc8da5ca34f395a8bd99afc552015bb60d6cd` | Read-only composition review; no combined tree executed |

Source dependency distinction matters: integration `1be0efdde` pins Composition **0.0.8**, whereas the staged base/A/B pin **0.0.10**. At this review the existing shared installed package reports **0.0.10**. The one repository test ran from A's worktree using A's config/package context. No package, symlink or installation was changed.

Read both workers' reports, the bootstrap adoption review, group ownership/contract notes, automatic-placement outbox note, exact diffs and native goldens. The supplied `scratchpad/luna/reports/` directory does not exist here; this limits prior-report coverage, not completion of this review.

## A — HOLD: completion recovery trusts a local tag

**Required source correction A1.** [bootstrapInitialization.ts:123](/home/user/work/wt/app-m2-bootstrap-init-native-stage/src/integrations/runtime/bootstrapInitialization.ts:123) checks only `accepted.value.kind === 'timeline-initialized'` before returning `loadLatest`. In the already-accepted/reopened path it does not validate the saved init acceptance/result or establish its publication in Runtime history. The loaded current basis need not contain any init acceptance. A local discriminator therefore supplies the completion decision.

The external ordinary RED [counterexample:12](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-groupview-readonly-review/notes/completion-authority.red.test.ts:12) uses the real generic outbox API, persists an acceptance with only `{kind:'timeline-initialized'}` as its value, releases/reopens the owner, and provides a reload of pristine H0. There is no create reservation, init command, init receipt or init history. Recovery **resolves successfully**, failing the refusal assertion. This is an adapter/storage-boundary counterexample using synthetic local input and mocked reads, **not evidence that Runtime accepted a forged command or that current production reaches this state**. The generic store deliberately accepts adapter-supplied JSON; that JSON must not itself establish initialization. This finding implements the brief's explicit “no authority from local value kind” constraint.

Bounded fix: retain the tag only as a dispatch hint; validate the saved original init result/receipt/command identity and establish its accepted historical publication using the existing normal history/immutable-read authority. A missing or mismatching result must retain the owner and refuse completion. Continue loading today's verified basis for display: a later edit, undo, or equal-byte restore must remain valid without reinitializing or requiring today's head to equal the historical init head. Use existing owner storage and authority APIs; no second journal, status endpoint or general lifecycle model. Add the counterexample to the existing focused suite, plus a matching historical acceptance with a later undo/current head. Do not weaken the existing successful recovery assertions.

Other reviewed properties are sound within the source seam:

| Requirement | Evidence and limit |
| --- | --- |
| Before-POST durability | [bootstrapInitialization.ts:24](/home/user/work/wt/app-m2-bootstrap-init-native-stage/src/integrations/runtime/bootstrapInitialization.ts:24) freezes name/defaults and normal create bytes/key. [commitOutbox.ts:211](/home/user/work/wt/app-m2-bootstrap-init-native-stage/src/tools/video-editor/commands/commitOutbox.ts:211) reserves timeline identity through owner scope and intent/pending request atomically. Existing strict transaction completion precedes transmission at `:295`. Reservation failure prevents POST. |
| Actual H0, not a guessed empty head | Create ACK checks scoped create receipt and its returned revision/publication pair at adapter `:60`. Fresh capture at `:77` requires the same pair, sole bootstrap history, null predecessor, matching publication receipt/payload/digest, empty exact manifest/children, then `authoringBundleFromDocument`. Headless create keeps the flight; it does not invent H0. This relies on a real verified provider implementing the ports. |
| Native original guards and sequential tracks | [bootstrapCapture.ts:19](/home/user/work/wt/app-m2-bootstrap-init-native-stage/src/tools/video-editor/commands/bootstrapCapture.ts:19) matches frozen Agent `_init_commands.py:10-37`: five reads and four writes, preserving absent versus present/null. V1 and A1 are captured successively at `:28`; A1's membership/order guard includes V1. Native command/record/after/inverse/redo fixture is retained, including default output nulls, complete row order/fields and absent theme roots. |
| Exact uncertain retry | Adapter `:54` reuses reserved create; `:102` dispatches saved init. Outbox `:278` reuses pending bytes/key without invoking the builder. Captured commands persist before commit reservation. No load/current-head recapture occurs on pending init recovery. Definitive conflicts preserve the original batch/guards. |
| Later edits, undo and equal bytes | Fresh capture requires original H0 publication as well as revision and sole bootstrap history. Tests at [bootstrapInitialization.test.ts:187](/home/user/work/wt/app-m2-bootstrap-init-native-stage/src/integrations/runtime/bootstrapInitialization.test.ts:187) retain the original uncertain request through later undo and reload current state after historical ACK. The final-tag defect concerns proof of completion; I found no source path that reapplies defaults merely because current bytes are empty. |
| Seven original positives / production caller | Entire `createDefaultTimeline.ts` and its test file are byte-identical to the staged base: all original seven success expectations plus the later opaque-headed-reuse positive are retained. Production still calls its existing publisher. `rg` found no production caller of the new reserve/resume exports. Headless same-ID repair, selection and project metadata CAS have not been migrated. |

**Future storage composition is feasible, not yet proven.** A reuses only `astrid.command-outbox/owners`. At [commitOutbox.ts:197](/home/user/work/wt/app-m2-bootstrap-init-native-stage/src/tools/video-editor/commands/commitOutbox.ts:197) it detaches and rewrites the entire existing record, preserving unrelated JSON fields. Its create ACK extension at `:306` is narrow; replacing `accepted.creation` after init ACK is a phase transition, not loss of unrelated top-level continuations.

Do not resolve the upcoming ACK conflict by choosing one branch's block. D13's [ACK:331](/home/user/work/wt/app-m2-render-continuation-outbox-stage/src/tools/video-editor/commands/commitOutbox.ts:331) retains render continuations; auto-placement's [ACK:468](/home/user/work/wt/app-m2-auto-placement-outbox-storage/src/tools/video-editor/commands/commitOutbox.ts:468) also checkpoints the linked placement acceptance. A alone has neither hook and is not their composed replacement. The combined implementation must preserve creation retention, render retention, placement linkage, dependent `readyBase`, current rejection resolution and the broader realm/actor discovery API. Test older owners, pending ACK, later edit/inverse, cancelled placement and retained continuations in the same existing store. Existing command-session recovery assumes ordinary before/after payloads; route recovered creation owners to their bootstrap adapter before handing them to that consumer. No such consumer wiring is currently claimed.

**Activation gates, independently of A1:** official startup-registered Agent init plus matching Runtime artifact/normal Door create; actual create/H0/history/closure admission; same-ID truly headless repair with the original positive; exact create/init replay across server/browser restart and lost/unpersisted ACK; later edits/undo and inverse; deterministic Main/additional identities and metadata CAS; correct owner discovery/handoff; zero legacy publisher traffic. Frozen parity and the reported **139 source tests do not establish these gates**. Read-only inspection confirms Agent stack `2431ae1fcdb6c9baf568043d3c0dad7c602b0e49:astrid/sdk/timeline/commands.py:29-63` lacks `timeline.init`; no current server/provider registration was executed here.

## B — HOLD: useful fallback notes, no adapter to approve

The branch equals its comparison base exactly. [Worker report:4](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-canonical-group-read-view-stage/notes/report.md:4) accurately says the permitted external fallback is complete and the adapter is unimplemented. Accept the diagnostic as a fallback deliverable; do not count it as a completed group-view source port. This is an App implementation gap in addition to missing current release/admission evidence.

**Concrete source gap B1:** [shotCompositionProjection.ts:55](/home/user/work/wt/app-m2-canonical-group-read-view-stage/src/tools/video-editor/data/shotCompositionProjection.ts:55) and its return at `:603` expose config and clip/occurrence maps, with no derived group sidecar. The external [positive:88](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-canonical-group-read-view-stage/notes/read-view.red.test.ts:88) requests one. There is no implementation proving explicit raw group/member bindings, two rows for a repeated shared shot, detached unknown metadata, or exclusion from serialized authored config. Existing clip identity bindings at projection `:327` are a useful seam, not that proof.

**Concrete vector/contract mismatch B2:** external [negatives:151](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-canonical-group-read-view-stage/notes/read-view.red.test.ts:151) demand refusal for missing/incomplete provenance member maps. Held native `tests/editing_conformance/test_recipe_m2_group_move.py:117-130` deliberately empties `members`, makes legacy `clipIds` stale, reverses current children, and expects a successful view with current canonical membership/order. `group_view.py:16-57` likewise uses provenance only for display metadata. Blindly importing all RED assertions would change the held source's behavior. Manager/Agent must settle which data validates aliases versus which data owns current membership; preserve current canonical ownership/order and report this discrepancy instead of silently making App authoritative. This is not a disagreement with PLAN option A.

Goldens inspected: migration provenance stores complete `legacy_group` and ordered `{legacy_clip_id,clip_id}` at held `new_group_commands.py:127-142`; normal provider `id_map` is not this carrier. Move golden has raw occurrence `new-occ`, member refs `occurrence:new-occ/clip:c1,c2`, raw child/parent lane V2, and original metadata still naming V1. Unknown nested collision keys, explicit nulls, snapshots and array order are retained. The two external copies are byte-exact native files (hashes in audit JSON). Their 62,420/78,945 bytes and external 193-line vector file are reference material, not added product size.

The external graph glue at vector `:23` constructs a display graph without accepted publication/closure authority; `prepare()` validation is not Runtime acceptance. Its four passing controls therefore cannot establish the brief's validated-closure rule. Future adapter input must join the existing verified `TimelineCommandBasis` head/canonical document and exact shot/internal pins, reuse authoring closure validation, and retain raw occurrence identity separately from display aliases. Never split display IDs or key rows by `(shotId,trackId)`. Parent placement offsets differ from nonzero source offset/time-map semantics: the held view explicitly refuses the latter. Shared movement remains separately gated; it does not justify collapsing two read rows.

All three original drag success bodies are unchanged versus `60aa26b95` after ignoring only their required `it.fails` markers and blank lines. The entire file is unchanged versus `090e`. Anchors: [useClipDrag.test.tsx:827](/home/user/work/wt/app-m2-canonical-group-read-view-stage/src/tools/video-editor/hooks/useClipDrag.test.tsx:827), [1173](/home/user/work/wt/app-m2-canonical-group-read-view-stage/src/tools/video-editor/hooks/useClipDrag.test.tsx:1173), [1283](/home/user/work/wt/app-m2-canonical-group-read-view-stage/src/tools/video-editor/hooks/useClipDrag.test.tsx:1283). No passing behavior was rewritten to require refusal.

Required gates: a bounded detached adapter plus main-suite positives for shared occurrences/raw bindings/current order/opaque metadata and no serialization; authoritative invalid-closure/ambiguous-binding cases; official migration and atomic move/retrack contracts; accepted current-pair migration → reload → movement → reload → guarded inverse, including exact legacy restoration; restore original three drag successes before activation/retirement. No new authored soft tags, wire DTO, or alternate group writer.

## Exact verification and limitations

Executed independently from `/home/user/work/wt/app-m2-bootstrap-init-native-stage`:

```sh
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts src/integrations/runtime/bootstrapInitialization.test.ts --maxWorkers=1 --no-file-parallelism
```

**PASS: 1 file, 20 tests, exit 0, 2.23s.** Mock ports/fake IndexedDB only; no server/browser durability claim.

```sh
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-groupview-readonly-review/notes/vitest.config.ts /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-groupview-readonly-review/notes/completion-authority.red.test.ts --maxWorkers=1 --no-file-parallelism
```

**RED as intended: 1 file, 1 failed test, exit 1, 1.78s.** Assertion failed because recovery resolved pristine H0 instead of refusing marker-only completion. [Full log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-groupview-readonly-review/notes/completion-authority.log).

From the assigned review worktree:

```sh
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-groupview-readonly-review/notes/source-audit.py
git diff --check 090e1162d tl/app-m2-bootstrap-init-native-stage
git status --short
```

**PASS, exit 0**: exact pins/diff size, original bootstrap files/dependencies unchanged, B empty diff, three drag bodies/markers preserved, native golden copies exact, three worktrees clean. [Audit JSON](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-groupview-readonly-review/notes/source-audit.json).

Prior-worker evidence read, not independently rerun: A's 139/5-file pass and native inverse/redo/replay probe; B's 48/2-file pass and external 12 RED/4 pass. These remain source/mock/reference evidence. No full, build, tsc, install, browser, live socket, central suite, real registered provider or current server was run. No repo source/test changes, commits, merges, ref mutations or external messages. Review task has no execution blocker; A1, B1/B2 and activation gates are follow-up findings, not reasons to wait here.

All new review artifacts are under the absolute ORCH `workers/app-m2-bootstrap-groupview-readonly-review/notes/` path above; `KEEP`, `commit-msg`, `DONE` are in its parent. The assigned product worktree remains clean.
