Model: Sonnet fallback (Codex unavailable on the farm); independent third view; the Codex Sol run is on the Agent box.

Model: Sonnet fallback (Codex unavailable on the farm); follow-up to tf-extensibility-minimal-1450

Paths: ORCH = /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch. Agent code = checkout agt-pin-ec0a9f5b (read only). I did not re-read the first worker's code files, so "unchanged" below means "nothing in these four sources contradicts it".

## 1. The lead's job text (INBOX.md:2193-2198)

- :2193 says one read-only worker, no source writes, tests, renders or installs. Codex is unavailable, so the Sonnet fallback runs it.
- :2194 gives the owner intent: let users and their coding agents add **commands** on a timeline, **views** of it, and **add-ons to the visualized picture**.
- :2196 asks for five parts: (1) smallest set of primitives; (2) cut or defer; (3) file layout of ONE example pack (a beat-snap command, a beat-grid view and an overlay) with its API and how the agent discovers it via CLI/MCP; (4) estimate in days; (5) risks. The limit is under 500 words.
- :2198 says the Sonnet run is an independent third view and its first line must carry the Sonnet label. The Codex Sol run is on the Agent box.
- **The brief required the example pack to have a command, a view AND an overlay, and "how the agent discovers it via CLI/MCP".** Part (3) therefore has to answer discovery, and I show below that discovery is not free (sections 3 and 4).
- Note: the lead says the plan sections are "§4.1–4.3" (:2195).
- **Changes the design or estimate: no.** The first worker's three-primitive shape matches the stated intent. It changes how much part (3) has to prove (see section 4).

## 2. shot-layering-PLAN-v1.md §4.1-4.3 and the assessment

- **There are no §4.1-4.3 in this file.** `$ORCH/design/shot-layering-PLAN-v1.md` has sections 1-9, with no subsections. §4 (lines 77-78) is "Effects in use" for the film, which has nothing to do with extensibility. The file has no extensibility content at all (I read all 114 lines).
- The assessment `$ORCH/design/extensibility-followup-assessment-20261026.md:4` cites "PLAN-v1.md §4.2–4.3, the five extension types and the shared primitives". That text is **not in the PLAN-v1 in the hub**. It probably comes from a later or different plan file (PLAN-v2 / PLAN.md, which INBOX.md:2175 says were still arriving). **Unverified** which file; I did not search further. The only available description of the five types is the assessment table (lines 9-15).
- What the assessment says, and the effect on the minimal design:
  - **Five types.** Commands, Views, Elements, Checks, Producers. The owner's three (commands, views, add-ons) map to Commands, Views and Checks/Elements. The "overlay" the first worker used is the existing Layer, so it falls under the assessment's Views and Checks rows.
  - **Estimate.** 110-120 days, about 6 months, with a 4-week Phase 0 of foundation: unify the two commit paths, one registry and manifest with pack discovery, stable refs and one finding shape, rationale and group plumbing, and the `astrid ext new/test` scaffold. Compared with the first worker's 9-10 days, that is about 12x.
  - **Commands row (line 11).** It lists "Registry and decorator, pack discovery, a published op contract, rationale/group not exposed by `commit_many`, markers refused by the compiler, the `doc.patch` escape hatch, two commit paths" as gaps. The first worker said a command can be `fn(timeline, **args)` through `Timeline.commit`. The assessment suggests that path is thinner than assumed: the "two commit paths" and "rationale/group not exposed by `commit_many`" items would hit any command that wants undo grouping or a rationale. **I did not read commit_session.py, so I cannot say whether this is real.**
  - **Views row (line 12).** "Generic parse-to-commands (only the opt-in NativeSheet path does it)". This only matters for *editable* views. The beat-grid view is read-only, so it is not needed.
  - **Cross-cutting risks (lines 44-48).**
    - Third-party code runs in-process, in a trusted provider.
    - **SCHEMA_DIGEST couples command extensions to releases.** This is the one that could really bite the minimal design. A new command that writes new op types would change the digest. A command built only from existing ops (a beat-snap built from move/trim ops) avoids this.
    - Markers: "none anywhere; beats copied into clips and addressed by ordinal" (line 15). A beat-snap command must therefore read beats from clip data, not from a marker store.
- **Changes the design:** it adds one explicit constraint to the first worker's design: **commands must be expressible in existing ops (no new op types, no markers)**, or the 9-10 day figure no longer holds. I do not know whether the first worker already assumed this.
- **Changes the estimate: probably not for the minimal version, but the gap with the assessment is not reconciled.** The two estimates differ in scope, not in correctness. The assessment includes schema contracts, App panel hosts, TypeScript/Python resolver parity, a parity harness and conformance scaffolding; the minimal version has none of that. The owner should be told that explicitly.

## 3. astrid/core/pack/ (what a pack needs)

- **Manifest schema v3** (`astrid/core/pack/schemas/v3/pack.json`):
  - required fields: `schema_version` (const 3), `id` (`^[a-z][a-z0-9_]*$`), `name`, `version` (x.y.z), at `:7-12`.
  - **`additionalProperties: false` at :6 and an `anyOf` at :599-630** requiring at least one of `actions`, `ui`, `rendering`, `documents`, `documentation`, `resources`.
  - **There is no section for commands, views or layers.** Allowed contribution kinds are `actions` (:186), `ui` (:483, type `editor` or `tool`), `rendering` (:525, types renderer/planner/finalizer/element) and `documents` (:555).
  - Example: `astrid/packs/music/pack.yaml` (JSON-style YAML) declares `beats` as an action with an `invocation` of kind `command` and an argv, plus inputs and outputs; the resources list names the files.
- **How a beat-snap, a beat-grid and an overlay land in this manifest today:**
  - beat-snap as an **action** would be admitted through `astrid.omp_invoke` as a task run; it is not a `Timeline.commit` call and does not appear as a timeline verb.
  - the beat-grid view and the overlay have **no manifest slot**. The overlay is found by a filesystem glob (below), not by the manifest.
  - If the minimal design wants them declared in the manifest, that needs **a schema change to v3** (new keys, plus the loader that reads them). Cost: small in code, but it touches the schema files and the Agent's schema-contract tests (I did not look at those).
- **Discovery** (`astrid/core/pack/discovery.py:4-13`, `:45-47`): source < local < managed < extra < env layers; `ASTRID_PACKS_PATH` names read-only external roots. A broken external pack is skipped with a warning (strict only for the source tree). So an external pack with a valid manifest **is** found by the pack registries (executors/orchestrators/elements/actions).
- **Layout contract** (`validate_layout.py:85-99`): allowed top-level dirs are `actions/<name>`, `ui/`, `rendering/<name>`, `shared/`, `docs/SKILL.md`, `executors/`, `orchestrators/`, `elements/`, `fixtures/`, `docs/`, `examples/`, `schemas/`. A `visualize_layers/` directory at the pack root is **not canonical** (the layer discovery globs it anyway; see section 4).
- **The first worker's example location `astrid/packs/beatgrid/` has a problem.** `validate_first_party.py:22-51` lists the first-party pack ids in a hard-coded tuple (`_FIRST_PARTY_PACK_IDS`), and `:419-426` reports "missing first-party pack directory" and rejects unknown directories under `astrid/packs/` (`allowed` set at :423). A new first-party `beatgrid` pack fails the first-party inventory check unless the tuple is edited. **Unverified:** I did not read the tests that call this, so I do not know which fail. An example pack outside the tree (under `ASTRID_PACKS_PATH`, or in a docs/examples folder) avoids this and also proves the third-party path, which is the point.
- **Changes the design: yes.**
  1. Put the example pack outside `astrid/packs/` (for example `examples/packs/beatgrid/`) and load it through `ASTRID_PACKS_PATH`; or add the id to `_FIRST_PARTY_PACK_IDS` (one-line change) if it must ship in-tree.
  2. State whether the manifest gets new keys. The leanest choice is **no manifest change**: keep commands, views and overlays discovered by module convention (as layers already are) and use the manifest only for the pack identity and its docs. That costs nothing in schema but means those contributions are invisible to `pack validate`. Either way, say so.
- **Changes the estimate:** +0.5 to 1 day if a manifest key is added (schema v3 + loader + a validation test); +0 if module convention only. First-party-id edit: trivial.

## 4. Does MCP pick up pack CLI additions automatically?

- **MCP tools come from `family_parsers()`** (`astrid/mcp_server.py:101-149`), called at server start (`main()`, :578). `family_parsers()` (`astrid/core/cli/domain_product.py:295-305`) imports the **static** map `FAMILY_PARSER_MODULES` (:282-292, with the comment "never discovered" repeated at :347-348) and calls `module.build_parser(None)`. Every leaf of the argparse tree becomes one tool (`_leaves`, :50-58). Argparse `choices` become a JSON-schema `enum` (:78-79), a `store_true` becomes a boolean, a JSON-typed flag becomes an object.
- Consequences for the example pack:
  1. **A new verb or flag added to the `timelines` parser appears in MCP automatically** after a server restart (the tool list is built once, `listChanged: false`, :548). No `mcp_server.py` change.
  2. **`show --as`** choices are hard-coded at `astrid/packs/timeline/cli.py:2343` (`"cuts", "script", "code", "sheet"`) and again at :2478 (`"cuts","script","code"`, a second parser, not read further). If the first worker's registry fills `choices=` when the parser is built, the MCP enum updates by itself. If `--as` is changed to a free string, the MCP schema loses the list, so the agent can no longer discover views from the tool schema. **Keep `choices=` fed from the registry.**
  3. **`--list-views` does not exist** in this checkout (no match in any `.py`). What exists is `--list-layers` (`cli_visualize.py:621`, handler :654) and `--list-checks` (`cli_working.py:268`). If the first worker's design assumed `--list-views`, it must be added (small) or replaced by the registry-fed `choices`.
  4. **`--layer` is a free string** (`cli.py:2594-2596`, `append`, no choices). MCP shows it as an array of strings with no enum, so the agent learns layer names only from `--list-layers`, a boolean flag that MCP also exposes. Fine, but not self-describing.
  5. **Each tool call shells out to `astrid-tools ... --json`** (`mcp_server.py:266-268`) with `os.environ` copied (`_astrid_env`, :211-218). The subprocess therefore sees `ASTRID_PACKS_PATH`; a pack added there is seen by the CLI at call time, but the MCP **tool list** (schemas) was built at server start.
- **Overlay/layer discovery does NOT see external packs.** `layers/base.py:197-198` sets the root to the Astrid source `astrid/packs` directory; `:234-235` globs `*/rendering/visualize_layers/*.py` and `*/visualize_layers/*.py` under it only. The `packs_root=` argument (:222) exists for tests; nothing passes `ASTRID_PACKS_PATH`. The docstring (:223) says "declared" modules, but nothing is declared in a manifest; it is a filename glob. Modules are imported by path with `exec_module` (:242-247): in-process, no sandbox. Failures go to `_BROKEN` and are shown by `broken_line`.
  - So an overlay in an external pack is **not picked up today**. The first worker's "overlays reuse Layer/Check discovery in layers/base.py" holds for in-tree packs only.
- **MCP prompts (skills) have the same limit:** `build_prompts()` (`mcp_server.py:516-531`) rglobs `SKILL.md` under the Astrid `packs` directory only. A third-party pack's SKILL.md is not offered as an MCP prompt.
- **Pack actions are reachable in MCP** only through the generic `invoke` tool (:443-454), as a capability run that returns a task id.
- **Changes the design: yes.**
  - Overlay discovery must be widened (a few lines in `discover()`: also glob the roots from the pack discovery or `ASTRID_PACKS_PATH`), or the example pack must live in-tree. Which one is the owner's call; the wider version is the one that serves "users and their coding agents add ...".
  - `--as` and the `--layer` listing must be registry-fed, not hand-listed.
  - The agent discovery story for the example is: CLI `timelines show --help` / `--list-layers` / `--list-checks`; MCP schema enum for `--as`, `--list-layers` as a tool flag, and a new command verb appearing as a new tool after restart.
- **Changes the estimate:** +0.5 to 1 day for widening layer discovery and its test; +0.5 for `--list-views` or enum plumbing if not already counted. About +1 to 1.5 days in total. I cannot tell whether the first worker's 9-10 days already included this.

## Summary against the first worker's design

| Item | Changes minimal design? | Estimate effect |
|---|---|---|
| Lead's job text | No; it fixes the required content of part (3) | none |
| PLAN-v1 §4.1-4.3 | The sections do not exist in this file; the assessment's source is elsewhere (unverified). New constraint: commands built from existing ops only (digest coupling) | none for minimal; gap to the assessment's 110-120 days stays unexplained |
| core/pack | Yes: example pack outside `astrid/packs/` or add its id; decide manifest keys vs module convention | +0 to 1 day |
| MCP/CLI | Yes: overlays not found outside source packs; `--as` must stay registry-fed `choices`; no `--list-views` exists | +1 to 1.5 days |

Net: about 10-12.5 days instead of 9-10 (my estimate on top of the first worker's, not independently derived).

## Not verified

- `commands.py`, `commit_session.py`, the `show` handler: not read. Statements about commit paths rely on the assessment only.
- The tests that pin the first-party pack list and the schema contract: not read; which ones fail with a new pack or new manifest key is unknown.
- Which document holds the real "§4.2-4.3" extension-types text.
- Whether the second `--as` parser at `cli.py:2478` is a different verb that should also be registry-fed.
- Nothing was run: no tests, installs, renders or network.
