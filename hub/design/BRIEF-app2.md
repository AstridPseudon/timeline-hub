# Brief: Proof lane (area app2, prefix ap2-, Timeline Child 3; no home repo, merge requests go to app / agent / runtime)

Read `$ORCH/PLAN.md` (v2.1) and `$ORCH/MANAGER-COMMON.md` first. Your tasks: **P1, P2, P3, P4**. The details are in PLAN §3. Your **P1 decides the H3 go/no-go**, so start it at H0.

## Order
1. **H0: P1 case collection** (Luna):
   - gather real timeline documents and real edits from the Agent and App fixtures, the e2e seeds, the editing-conformance cases and sample projects;
   - write them as a data-driven test set for `doc.patch` round-trip and merge;
   - write the **H3 chain scenario**: split → trim of the new clip → intervening Agent edit → lost acknowledgement → restart, covering accepted, merged and refused replies, against App plus Runtime plus Agent.

   As soon as the Agent lane's R1 branch and the App lane's A2 branch exist on the hub, run the set and the chain against them. Then report **P1 RESULT: GO or NO-GO** with evidence in your board's Blockers line.
2. **P2** (Luna), after A2 and A3: the gesture tour on `three-products`. For each gesture, check the commit sent, zero old-route traffic (network plus Runtime `/commits`, not the door log), only the intended fields changed, reload and undo.
3. **P3** (Luna): the gate-5 journey on the new path.
4. **P4** (Luna), after G2, G3 and R2: Agent CLI, Python and sheet coverage, including **10 notes as one commit with per-step undo**, plus conflict and re-run.

Heavy runs are requested from the farm (put them in Blockers). Your branches merge through `bin/request-merge-remote <repo> <worker>`.
