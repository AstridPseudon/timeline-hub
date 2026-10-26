Model: Sonnet fallback (Codex unavailable on the farm); independent third view. The Codex Sol run is on the Agent box.

Verdict: yes, over-engineered (about 110-120 days, five types, a manifest, a parity harness) for the owner's intent of commands, views and add-ons. Agent files read at ec0a9f5b. I did not read the lead's job text (INBOX grep for "NEW lead" matched nothing) or shot-layering-PLAN §4.1-4.3 (heading grep matched nothing). I did not open the Runtime/App/Composition code. I did not verify the App panel claims.

## 1. Smallest set of primitives
Three, all of which already have a precedent in the code:
1. **Command = a Python function `fn(timeline, **args)`** run through `Timeline.commit(fn)` (`astrid/sdk/timeline/commit_session.py:163`). That path already gives retry (up to 3 evaluations, :203), undo, a label taken from `fn.__name__` (:178), and atomic merge for arbitrary Python (:232). No op-table entry and no schema are needed: the function composes the existing recording API (`clip.set`, `clip.move`, and so on). The 30-entry `operations()` table (`commands.py:75`) is the wire contract for the built-in ops, and it stays closed.
2. **View = `name -> render(timeline) -> text/JSON`.** Today `--as` is a hard-coded `choices=("cuts","script","code","sheet")` (`packs/timeline/cli.py:2341-2343`). Make the choices come from the registry.
3. **Overlay = the existing `Layer`** (`timeline_visualize/layers/base.py:114`), with `Check` (:93) beside it. Discovery is a glob of `<pack>/rendering/visualize_layers/*.py` plus a broken-module quarantine (:234-268, `broken()` :201). This is the pattern to copy, not to redesign.

One shared mechanism: a pack drops a module in a known directory; the discovery loop imports it, collects named lists (`COMMANDS`, `VIEWS`, `LAYERS`, `CHECKS`), isolates failures, and refuses shadowing (:174). Generalise `discover()` rather than writing a second one.

## 2. Cut or defer
- **Defer**: Elements and signals (38 days, plus parity risk). Defer until after shot-layering.
- **Defer**: markers and a Runtime proposals channel. The beat example reads `ctx.beats` (`NEEDS` includes "beats", `base.py:13`) and needs neither.
- **Cut**: the manifest and `astrid ext new/test` scaffold. A pack's directory is its manifest, and pytest is the harness.
- **Cut**: the conformance harness. Keep it to a few tests that load the example pack.
- **Cut**: unifying the two commit paths, unless a command hits a real bug.
- **Cut**: publishing a stable ref/finding contract. `Finding` already has `fix` (:43).
- **Defer**: a sandbox, and the App panel host. Views are CLI/JSON first.
- **Cut**: the "registry plus decorator" for ops. Commands are functions, not ops.

## 3. Example pack: `astrid/packs/beatgrid/`
```
beatgrid/
  commands/beat_snap.py          # COMMANDS = [Command("beat-snap", fn, help)]
  views/beat_grid.py             # VIEWS = [View("beat-grid", render, help)]
  rendering/visualize_layers/beats.py   # LAYER = Layer("beat-ticks", ..., needs=("doc","beats"))
                                 #   (CHECK = Check("off-beat") may carry fix={"clip":id,"move_s":d})
  tests/test_beatgrid.py
```
API: `Command(name, run, help, params)` with `params` a JSON-schema dict, and `View(name, render, help)`. `beat_snap(tl, tolerance=0.1)` moves the clips whose start lies within tolerance of the nearest beat, through the recording API.
Discovery:
- **CLI**: `astrid-tools timelines run beat-snap --tolerance 0.1` and `timelines show --as beat-grid`. `--list-commands` and `--list-views` mirror `--list-layers` (`base.py:299`). The `Add one:` hint line (:316) becomes the agent's how-to.
- **MCP**: no new code for commands. `mcp_server.py:50` (`_leaves`) turns every argparse leaf into a tool, so `timelines run` shows up. To get per-command tools, build one subparser per command. Not verified: that `build_tools` picks up pack CLI additions automatically.
- Pack declaration: `astrid/core/pack/discovery.py` and `manifest.py` exist. I did not read them, so whether a new pack needs a manifest entry is unverified.

## 4. Estimate (senior-engineer days)
- Generalised discovery plus `run` verb: 3.
- Dynamic `--as`: 1.
- `beatgrid` example pack plus tests: 3.
- MCP check, docs, `--list-*` hints: 2.
- Total: **~9-10 days**, against 110-120 in the assessment. Add 3-5 if the Runtime API route must also carry packs. The assessment says Runtime proposals are client-side only, which I did not verify.

## 5. Risks
- Commands run in-process with arbitrary Python and no sandbox. That is acceptable for local packs and wrong for a shared marketplace.
- Ops added by a function are not replayable by Runtime or the App. They are Agent-side macros that emit built-in ops. If the owner needs App-visible commands, a real op registry is needed, with SCHEMA_DIGEST coupling (assessment line 46).
- `commit(fn)` rejects reruns after non-conflict failures and re-evaluates up to 3 times, so commands must be pure and idempotent.
- Name shadowing across packs relies on the `source` check (:174).
- The overlay `Layer` is PNG/PIL-oriented (`LayerResult.image`). It does not give an App-side overlay. Anything App-side is unverified and out of scope.
