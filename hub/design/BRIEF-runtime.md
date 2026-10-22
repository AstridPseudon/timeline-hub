# Brief: Runtime lane (area runtime, prefix rt-, home repo runtime, main machine)

Read `$ORCH/PLAN.md` (v2.1) and `$ORCH/MANAGER-COMMON.md` first. Your tasks: **C0, U1, R2r, R5, P5**. The details are in PLAN §3.

## Order
1. **H0, in parallel:**
   - **C0** (Sol, HARD: cross-repo contract) writes `$ORCH/design/commit-v2.md`, covering every point of PLAN §2 with executable JSON examples. It reads the existing commit engine first: Runtime `runtime_protocol/timeline_commit_store.py` and `timeline_commit_execution.py`; Agent `astrid/sdk/timeline/commands.py` and `commit.py`, read-only via the hub refs.
     - Target: done within about 1 h.
     - When it is written, put "C0 READY FOR APPROVAL" in your Blockers. The orchestrator approves it. Nobody builds against it until BOARD-HEADER says "C0 APPROVED".
   - **U1** (Luna) merges upstream main into runtime tl/integration with `git rerere`. It is currently 5 commits behind, with 16 conflicts, mostly generated contract files: regenerate them with the generators, never by hand.
     - Renumber our commit tables to schema **v32**, after upstream's app-state v31, with an upgrade test that opens an upstream v31 realm.
     - Keep upstream's asset-identity changes.
     - Then regenerate the clients.
2. **R2r** (Luna), after C0 approval and U1: store labels, steps and per-step patches; set attribution from the authenticated actor; the history listing returns them.
3. **P5** (Luna), after R1/R2 merge in agent: carry over the original gate items (PLAN-v1 §6, gates 2–4): renderer-off save, door authorisation for the commit form, crash before/after commit, identical retry, changed payload under the same key.
4. **R5** (Luna), only once the board header says A3 and G4 are merged: refuse **and directly reject** every old save route, headless included (composition-revisions POST, publish-timeline-render, timeline-documents, documents with timeline ids, replace-clip, PATCH timeline, replace-parent-media). Delete their bodies, keeping a short 410 stub. One-writer test: extend `tests/test_timeline_legacy_authority.py`.

Keep rename, shell create, archive and recover as metadata routes.
