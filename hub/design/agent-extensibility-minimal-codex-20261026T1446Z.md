# Task X: smallest useful extensibility

Static opinion against Agent `ec0a9f5baef2c31bc5179087b83f044524575182`, tree `83b84c79941917fde535ee3ddba5533a776cace3`; no behavioral qualification. PLAN v2.1 and `design/commit-v2.md` govern; PLAN-v1 §4.1–4.3 is historical.

1. **Judgment/primitives.** Yes: 110–140 senior-engineer-days overbuilds commands, read-only views and inspection-picture add-ons. It estimates a broader platform. Start with ordinary pack actions, pinned reads and existing visualization layers. **Existing API:** actions become executor definitions (`astrid/core/execution/executor/registry.py:168`); `Timeline.command`, `move`, `commit(fn)` and conservative omitted-read handling exist (`astrid/sdk/timeline/commit_session.py:129`, `:146`, `:163`, `:232`). The operation table remains closed (`astrid/sdk/timeline/commands.py:29`, `:75`); extensions compose native commands or `doc.patch`, rather than introduce wire ops.

2. **Cut/defer.** No unified extension registry, decorators, generated controls, generic editable-view parser, new check/producer types, signals, proposals service, automatic marker-following or custom merge policies. Keep current commit semantics and Runtime as sole film writer. Do not make consolidation of internal commit paths a prerequisite for composing commands. App panel hosting and exported-film elements are separate scope.

3. **One PROPOSED pack, not implemented:**

   ```text
   beat_tools/
     pack.yaml                 # actions snap/grid; inputs/outputs/invocations
     docs/SKILL.md
     actions/snap.py
     actions/grid.py
     rendering/visualize_layers/beats.py
   ```

   **PROPOSED pack API:** `snap(project, timeline, clip_ids, dry_run=False)` calls `tl.commit(fn, dry_run=...)`; its callback recomputes nearest beats from the fresh bundle and stages `tl.move`. This snaps once; redetection never moves clips automatically. `grid(project, timeline, revision_id, window)` returns `{revision_id, publication_id, text}` from one pinned read. Existing `_run_python_action` would call both proposed functions (`astrid/core/execution/executor/runner.py:453`). Arbitrary document changes use existing `doc.patch`, preserving read guards.

   The proposed overlay exports `LAYER = Layer(...)`, `render(ctx) -> LayerResult`, using `ctx.beats`; existing `compose_motion_sheet` would call it (`astrid/packs/rendering/actions/timeline_visualize/motion/sheet.py:291`). Existing Layer API/discovery: `astrid/packs/rendering/actions/timeline_visualize/layers/base.py:114`, `:222`, `:349`.

   CLI discovery: `packs inspect beat_tools`; invocation: `tasks create --capability beat_tools.snap` with project/spec (`astrid/core/pack/cli_inspect.py:84`; `astrid/core/cli/domain_tasks.py:328`). MCP: `skills_list`/`skill_get`, then `invoke` (`astrid/mcp_server.py:438`). Grid is an action initially: `show --as` has fixed choices (`astrid/packs/timeline/cli.py:2343`). Overlay selection uses `visualize --view motion --layer beat-grid`. **PROPOSED core change:** layer `discover` and MCP `build_prompts` consume existing pack discovery (`astrid/core/pack/discovery.py:238`); both currently scan source folders (`layers/base.py:234` under the prefix above; `astrid/mcp_server.py:519`). No additional registry.

4. **Estimate:** 15–25 senior-engineer-days: action contracts/docs 3–5, snap 4–6, grid/overlay 3–5, discovery integration 2–4, review/integration 3–5. Assumes functioning commit foundation, existing beat analysis, trusted Python packs, CLI/MCP only; excludes App UI, sandboxing, automatic anchors and film rendering.

5. **Risks:** retry side effects, conservative conflicts, stale beat data, cue/timeline/frame conversion, and imported overlay code privileges. Revision pins identify inputs; they do not guarantee correctness. An overlay annotates the visualization picture/panels; an exported-film element needs renderer integration. No preview/export parity promise.
