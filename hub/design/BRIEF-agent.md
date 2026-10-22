# Brief: Agent lane (area agent, prefix agt-, home repo agent, Timeline Child 4)

Read `$ORCH/PLAN.md` (v2.1) and `$ORCH/MANAGER-COMMON.md` first. Your tasks: **U2, U4a, R1, R2, R3, V2, G2, G3, G4, G5**. The details are in PLAN §3. You hold most of the critical path, so keep the Sol tasks moving.

## Order
1. **H0: U2** (Luna) merges upstream main into agent tl/integration with `git rerere`. It is 93 commits behind with 13 conflicts:
   - in `sdk/timeline/publish.py` and `edits.py`, keep upstream's behaviour inside our native paths;
   - re-vendor the Runtime client with `scripts/vendor_lock.py`, never by hand;
   - regenerate `artifacts.json` with its tool.
2. **After "C0 APPROVED"** in `$ORCH/design/BOARD-HEADER.md`:
   - **R1** (Sol, HARD: core commit semantics): the `doc.patch` op in `astrid/sdk/timeline/commands.py` and the provider, with previous-value check, membership/order conflict, declared reads and inverse. It may start on the current tl/integration and merge forward after U2.
   - **G2** (Sol, HARD: conflict re-run semantics): `timeline.open()` / `tl.commit(label|fn, merge, dry_run)` with a bounded re-run. It can start against the contract in parallel with R1.
   - **Push R1's branch to the hub early** (hub-sync does this). The Proof lane's **P1** runs the H3 go/no-go against it.
3. **After R1:**
   - **R2** (Sol, HARD: guarded undo): whole and per-step undo; A→B→A.
   - **R3** (Luna): dry run plus structured errors.
   - **V2** (Luna): validator timing and structure rules, plus element and parameter checks.
4. **After G2:**
   - **G3** (Luna): the **document → doc.patch emitter** that replaces `document_diff.py`, plus helpers emitting semantic commands or patches with steps. CLI `edit`, `apply` and the sheet call them.
   - **G4** (Luna): `replace_parent_media`, `update-element`, narration (`publish.py:54-58`), `create_empty` and render publication all through commit.
5. **U4a** (Luna), after Runtime's U1: adopt the regenerated client and schema.
6. **G5** (Luna), **last, after G3 and G4 merge:** delete the native subparsers, `commands-file`, `apply --native`, `undo --publication`, `document_diff.py`, `store.three_way`, `publish_bundle` and the separate publish. Keep the behavioural tests.

You also merge other lanes' requests for the agent repo (Proof and Viewing) through your merge queue.
