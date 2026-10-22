# Brief: Schema & viewing lane (area viewing, prefix vw-, home repo composition, Timeline Child 2)

Read `$ORCH/PLAN.md` (v2.1) and `$ORCH/MANAGER-COMMON.md` first. Your tasks: **V1, V3, V4**. The details are in PLAN §3.

## Order
1. **H0: V1 prep** (Luna, read-only first): inventory every copy of the timeline document schema across the four repos. The duplicate scan found four byte-identical copies. Confirm Runtime's contract schema as the **single source**, and list the generated copies with their drift checks.
2. **After "C0 APPROVED" and Runtime's U1: V1** (Luna):
   - add the open `meta` namespaces in the single source (project, timeline, shot, occurrence, track, clip), with size and type limits;
   - regenerate the copies with the tools;
   - make Composition and the renderer ignore unknown `meta`, with a test.

   Consumer copies land through the Agent and App lanes' U4 tasks, or through your merge requests.
3. **V3** (Luna), after U2 and U3: one Composition artifact. Pack the Composition head once and name it by commit, then adopt it in Agent (`remotion/package.json` and lock) and App (`package.json` and lock) through merge requests. Fix the stale pin tests.
4. **V4** (Luna, optional, first to cut), only after U2 and U3: delete the stale `ui/live-scenes` and `editor/live-scenes` dirs (agent), the duplicate `word_binding_recipe.py` copy (agent tests), and the duplicated `PropertiesPanel` block (app).
