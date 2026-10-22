# Brief: App lane (area app, prefix app-, home repo app, Timeline Child 1)

Read `$ORCH/PLAN.md` (v2.1) and `$ORCH/MANAGER-COMMON.md` first. Your tasks: **U3, U4p, A2, A3, A4**. The details are in PLAN §3.

## Order
1. **H0: U3**, split into three Luna workers. Merge upstream main into app tl/integration with `git rerere`; it is 189 commits behind with 55 conflicts.
   - **U3a:** the modify/delete conflicts (take upstream's deletions of the cloud product and dev extensions), plus docs, config and supabase.
   - **U3b:** editor, gesture and save-path files. **Take upstream's version**, except the parts A2 keeps: the persisted outbox (`commands/commitOutbox.ts`), the commit transport, and the Runtime client and door connection.
   - **U3c:** merge the e2e harness (`tests/e2e/local/support/*`, `three-products.spec.ts`) with upstream's QUICK tier.
   - Then re-vendor astrid-browser from the merged Agent with the tool. `provenance.json` is regenerated.
2. **After "C0 APPROVED" and U3b: A2** (Sol, HARD: dependent-edit chaining without an executor):
   - the save funnel sends semantic commands (split, ripple, per-occurrence fork) or `doc.patch` through the existing outbox;
   - dependent edits chain on the local document;
   - if a predecessor fails, re-validate or roll back with a message;
   - reply handling (accepted, merged, conflict, invalid);
   - no overwrite button.
3. **A3** (Luna), after A2: popup add/swap, placement, element and registerAsset saves through A2.
4. **U4p** (Luna), after Runtime's U1: adopt the regenerated client and schema.
5. **A4** (Luna), after A2 and A3: delete the TS executor, capture ports, generic patch adapter and goldens. Keep the behavioural tests.

You also merge other lanes' requests for the app repo (Proof and Viewing).
