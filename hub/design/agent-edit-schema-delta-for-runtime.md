# Agent edit-command schema delta for Runtime (Bundle #3 / current tuple)

Worker: agt-runtime-artifact-needs. Read-only: no repo files changed, no commit-msg written.
Schema path in every source: `astrid/core/timeline/schema/edit-command.schema.json`.

## Bottom line

1. **Runtime's current pin is behind Agent integration.** Runtime's `contract/schemas/edit-command.json` (sha256 `472622c4…aee9`, listed in `contract/artifacts.json`) is byte-identical to Agent commit `d4743e29` ("compose reviewed Bundle2 editing source"). It lacks `placement.create`, `placement.unplace` and `occurrence.duplicate` (and their three `$defs`), which are already on Agent `tl/integration` (408f3ba3, via stack-sync-3). So one regeneration must carry **six** new ops relative to Runtime's pin, not three.
2. **Three pending ops are purely additive** over integration: `clip.set-element`, `shot.set`, `shot.pool`. No existing op branch and no existing `$def` changes; the only edited def is `EditCommand`, which gets one new `allOf` branch per op.
3. **The three pending branches do not conflict.** Each one's parent is integration's schema (sha `429283b2…`), each adds distinct def names, and a textual 3-way merge (`git merge-file`, base = integration) exits 0 for all three.
4. **Runtime needs no port, validator or DTO code change.** Command meaning is loaded from the Agent provider; the Runtime has no op-keyed logic (grep of `runtime_protocol/` finds no op names). The only Runtime work is regeneration plus the pin/manifest update.
5. **Runtime's own published-floor compatibility check passes** for the integration schema and for the union (0 errors against `runtime-0.2.3`).

## Per-op table

Sha = sha256 of the schema file on that branch, as committed.

| op | branch (commit) | schema sha256 (file on branch) | additive? | Runtime generator / protocol change |
|---|---|---|---|---|
| `clip.set-element` | `tl/agt-m2-clip-set-element` (68e7adb9) | `b4a65ffeeba2403dc593bd59240a3661fc425e151879d76c76a2b99d87e72796` | yes: new op branch (`select` `parent\|occurrence:<id>/clip:<id>`, `version` "1"), new `$defs` `ElementRef`, `ClipSetElementArgs` | Regenerate only. Generated DTOs gain `ElementRef`, `ClipSetElementArgs`. No media, no port call, no created IDs, no id_map. |
| `shot.set` | `tl/agt-m2-shot-settings` (ded4fe8b) | `0bef9cca458c664664e59cc517d1968596ea53c54389dfffde2e2af66be30b08` | yes: new op branch (`select` `occurrence:<id>/shot`, intent `ownership: occurrence`), new `$def` `ShotSetArgs` | Regenerate only. Recorder gains an `entity` dependency (`shot.source`) and a `shot.owner` binding; both use kinds the schema already allows (`AgentDependency`, `AgentBinding`). No created IDs, no id_map, no port call. |
| `shot.pool` | `tl/agt-m2-shot-pool` (99da3734) | `f3cb6ed0a31df48a592ddec8cd7a0fa495fc4324bfffe1972d7df577698454c9` | yes: new op branch (`select` `occurrence:<id>`, intent `ownership: occurrence`), new `$def` `ShotPoolArgs` (`action` enum add/remove, `media` = `MediaSelection`) | Regenerate. Protocol: none new. Agent `commit.py` now sends `shot.pool` media through the existing `port.selected_media` (ABI 1, already implemented in `runtime_protocol/timeline_commit_port.py:272`). `add` on an absent asset alias records a `created` entry with `kind: "asset"` (Agent recorder; Runtime stores `created` generically, and `id_map` stays identity-only). |
| `placement.create` / `placement.unplace` / `occurrence.duplicate` (already on integration; stack-sync-3 `408f3ba3`) | `tl/agt-m2-stack-sync-3`, merged; also `tl/agt-m2-schema-superset-guard` (ffa5325c, schema = Runtime pin) | integration: `429283b2e740ab2bde2659b2ed3a3eb9db364ba6cd669924e0e5289fecfb85fc` (= stack-sync-3) | yes, additive over Runtime's pin (3 ops + `PlacementCreateArgs`, `PlacementUnplaceArgs`, `OccurrenceDuplicateArgs`) | Regenerate. `placement.create` already has its media in `commit.py`'s verified list. `placement.create` creates a `created` clip ID, and that path already exists. |
| `track.set` (label), foundation, popup/pack inputs | already in Runtime's pin | n/a | — | none; `TrackSetArgs`, `ClipSetParamsArgs.schema_source`/`DocumentPin` are identical in the pin and integration (checked: no def changed) |
| auto-placement chain (`fb21a629` completion, `d1277160` shared builder) | `tl/agt-m2-auto-placement-completion`, `tl/agt-m2-auto-placement-step2` | `429283b2…` (= integration) | no schema delta | none. These builders emit `placement.create` and `shot.pool`. The **pooling** half of the chain lives in `99da3734` (`tl/agt-m2-shot-pool`), so the chain's schema needs are covered by the `shot.pool` row, not by step2 alone. |

Notes on the other branch heads I checked: `tl/agt-m2-stack-sync-3` is an ancestor of integration with an identical schema. `tl/agt-m2-schema-superset-guard` (ffa5325c, one commit) carries Runtime's pinned schema exactly, so it adds nothing new for Runtime.

## Schema delta detail

Verified by a structural diff of each branch against integration (`$defs` and `allOf` keyed by op). Nothing else changed.

- `clip.set-element` args: `{elementRef: ElementRef}`, required, closed. No clear: a clip keeps its element. `ElementRef` = `{id, kind, revision}` required, `packId` optional, closed. Runtime needs no pack check here; the Agent checks that `id` and `kind` match the existing ref.
- `shot.set` args: `{values, clear}`, both required, closed, with `anyOf` requiring `values` minProperties 1 or `clear` minItems 1. `values` = `{name?: string, settings?: {<22 scalar roots>: scalar|null}}`. `clear` = enum of `name` and `settings.<root>`. Compound roots (`steerableMotionSettings`, `phaseConfig`, `pairConfigs`, `shotImageIds`, `loras`, `structureVideo`, `modelSettingsByModel`) are not in the schema, so they are refused by the closed args.
- `shot.pool` args: `{action: add|remove, media: MediaSelection}`, required, closed. `MediaSelection` is the existing five-field `$def`.
- `EditCommand.allOf` gains one `if`/`then` per new op, appended in the order the branches were written (clip, shot.set, shot.pool).

## Union (all three pending deltas on integration)

- Built by a textual 3-way `git merge-file` (base = integration; each branch as "theirs" in turn). Exit 0 for each step, so zero conflicts. Output: `scratchpad/schemas/union.json`.
- Structural check against integration: `ops added: [clip.set-element, shot.pool, shot.set]`, `defs added: [ClipSetElementArgs, ElementRef, ShotPoolArgs, ShotSetArgs]`, `ops changed: []`, `defs changed: [EditCommand]` only (the allOf append), top level unchanged.
- **File sha256 (what Runtime would pin byte-for-byte): `48becd142070d3336868b2aa7716a372034594b4c8822e816a3a036a69ad02bc`**
- Canonical-JSON sha256 (sort_keys, compact separators, for comparison only): `b368436e33f4c921febd44639c0ab545d84743499f05341141ce1bda0e5c099c`
- Relative to Runtime's pin (`472622c4…`), the union adds six ops and seven `$defs`: `placement.create`, `placement.unplace`, `occurrence.duplicate` and the three pending ones.

**Conflicts between branches:** none. The defs introduced by each branch are unique names: `ElementRef` and `ClipSetElementArgs` (clip.set-element), `ShotSetArgs` (shot.set), `ShotPoolArgs` (shot.pool). Each branch adds one unique op key. The only shared def, `EditCommand`, changes by appending to `allOf` in each branch, and the textual merge is clean.

**Superset guard / additive vs widened:** all deltas are additive. No existing op or def is narrowed or widened. The Runtime compat check (`generators/command_schema_compatibility.py`, floor `runtime-0.2.3.json`) returns 0 errors for integration, each single-op candidate, and the union.

## Runtime artifact regeneration

Method: I exported Runtime's `contract/`, `generators/`, `runtime_protocol/`, and `packages/{python/astrid_runtime_client,typescript/src}` from `tl/integration` (Runtime `9411426`) into a scratch tree, then ran Runtime's own generators (`timeline_commit_resources.render()` and `timeline_commit_types.render()`) with the candidate schema dropped in as `contract/schemas/edit-command.json`. Nothing in the Runtime repo was touched.

**Validation of the method:** run on Runtime's current pin, the generators reproduce the four tracked files byte-for-byte (`vs archive … identical` for all four). So the regenerated hashes below are trustworthy as "what the generator produces."

| Runtime artifact (tracked in `contract/artifacts.json` unless noted) | current (pin = Agent d4743e29) | integration-only (+3 already-landed ops) | + clip.set-element only | + shot.set only | + shot.pool only | **union (all)** |
|---|---|---|---|---|---|---|
| `contract/schemas/edit-command.json` (byte-identical pin) | `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9` | `429283b2e740ab2bde2659b2ed3a3eb9db364ba6cd669924e0e5289fecfb85fc` | `b4a65ffeeba2403dc593bd59240a3661fc425e151879d76c76a2b99d87e72796` | `0bef9cca458c664664e59cc517d1968596ea53c54389dfffde2e2af66be30b08` | `f3cb6ed0a31df48a592ddec8cd7a0fa495fc4324bfffe1972d7df577698454c9` | **`48becd142070d3336868b2aa7716a372034594b4c8822e816a3a036a69ad02bc`** |
| `runtime_protocol/schemas/timeline-commit-bundle.json` (tracked, `artifacts.json`) | `37f31ffd6ce63f54897cb7880a7c89811e4cfed3125ab0183127d34774a02d32` | `5dc18eb36facbaa87242ead15b489e29bdc90fb1d6b03bb69c4f8dbbc06b87b6` | `6644e330e6df51b8faab0b11c36a380dc7ab68edeb5c24d475ddd1f9340ddd16` | `690c37e86cadbfe3ac0030e9fb73bd7874c355f1c1ec2cb4b6a0eff5146260b8` | `fce1fd72f9f8276686d221fe9cb91f6d08d853913a58424abefb43f5373c834a` | **`2f012ac1e060bfde96e3155917ee2bcbeca5fdc698df6e15c86102de9a1be0c4`** |
| `packages/python/astrid_runtime_client/timeline_commit_types.py` (tracked, `artifacts.json`) | `b036176f6862003243df9e2f4d98c79888b6e3304576fa8f6b0ee144a2a6e8a6` | `c8fa9afa23a7f6c7018c94a9ec6b12cbbd724a03f4cf2b74ed3710e40a393864` | `950b4bfe7ca943234ab37db7662ff92125ab7de09538563cf5e50de3c6a8940c` | `57f11890769544456add8a49f18d71035a1f336984180d99642d7d2d6d471e59` | `d9e474e10943e227a3a51a1edc0abc2e3baa5895a34a51cf434f8c27f3751b9b` | **`b7231cf7fa3ba8bfbb713a08d3599dafc2d1318ed0a035d3605492f27b4b5ecf`** |
| `runtime_protocol/timeline_commit_types.py` (identical copy; not in `artifacts.json`) | `b036176f…` (same as above) | `c8fa9afa…` | `950b4bfe…` | `57f11890…` | `d9e474e1…` | **`b7231cf7…`** |
| `packages/typescript/src/timeline-commit-types.ts` (tracked, `artifacts.json`) | `2e788219cda7f25c9bb88e84e7d2ccaabc9a4fe49c7aef1f3e199977cc73022e` | `a22ad74b7b8f6f3b9b90d16a27c32458043b933cdd1fe9beceadce16423eecd0` | `08ecc488c33a7e3fa21ade6628e135ea3d4847b5aaf20a29b11e5b3ec1a73ca5` | `27e657693fafbc8a1de15d7df88b87f1269169c1aef9ed0b6b0fd4e8c2cc91e3` | `c96a47d678f02434022b1809e4747e95fa53a190d6565ebfd71de435af99cf3f` | **`87bf82116f4df85bef1e85cb8bf4bb80bfe2f7694d48ccfd6014db41c06bca10`** |

Entries in `contract/artifacts.json` to update on release: `contract/schemas/edit-command.json`, `packages/python/astrid_runtime_client/timeline_commit_types.py`, `packages/typescript/src/timeline-commit-types.ts`, `runtime_protocol/schemas/timeline-commit-bundle.json`. `runtime_protocol/timeline_commit_types.py` is generated alongside the python client, and I found no `artifacts.json` entry for it. Check that `scripts/artifact_manifest.py` covers it before release.

Generated Python for the new defs (union): `ElementRef`, `ClipSetElementArgs`, `ShotPoolArgs` are plain TypedDicts; `ShotSetArgs` is `Union['ShotSetArgsVariant1', 'ShotSetArgsVariant2']`. The generator duplicates the `anyOf` branches, so each variant carries the full `values`/`clear` shape. The output compiles and no names collide with existing DTOs, but it is verbose. See decision 2 below.

## Port / validator / recorder changes, by op

- **Port:** no new port method. `shot.pool` is the only pending op that needs media pin verification, and it uses the existing `selected_media` (ABI 1). The `verified_media` list in `commit.py` gains `shot.pool`, which is Agent-side code. `placement.create` already verifies media.
- **Validator:** `validate_command` is Agent-side and loads the schema from the provider. Runtime's acceptance checks finite JSON, closure identity and recorder consistency, and they are op-agnostic. No Runtime validator change is needed.
- **Recorder / created / id_map:**
  - `clip.set-element`: standard element-write record. No created IDs, no id_map change.
  - `shot.set`: adds `dependencies` (`shot.source`, kind `entity`) and `bindings` (`shot.owner`). Both kinds are already allowed.
  - `shot.pool` add: a `created` entry (`kind: "asset"`, `owner`) when the alias is absent. Remove creates nothing. The `id_map` stays identity-only, which Runtime already enforces (`timeline_commit_port.py:403`).
  - `placement.create`, `placement.unplace` and `occurrence.duplicate` (already on integration): `occurrence.duplicate` records `created` shot and occurrence entities (`create_entity`), and `placement.create` records a `created` clip identity through the shared media path. `placement.unplace` does not create identities (I did not trace it line by line). These paths are already on integration and need no new Runtime handling.

## Decisions for the orchestrator

1. **One release, six-op delta.** Runtime's pin must advance from `d4743e29` to the union, not just to the three pending branches, because `placement.create`/`unplace` and `occurrence.duplicate` are on integration but not in the pin. A release that regenerates only the three pending deltas would leave the pin behind integration.
2. **`ShotSetArgs` `anyOf` shape (decide before any Agent schema change).** The `anyOf` in `ShotSetArgs` (values minProperties 1 / clear minItems 1) makes the generator duplicate the object, which bloats the generated DTOs. Any Agent edit to this def changes all five hashes above. My recommendation is to keep it as it is for this release, since the Agent owns the schema and the behaviour is correct. If Agent wants a leaner DTO, the change belongs in the same pre-release commit, before regeneration.
3. **Compatibility floor.** `generators/generate.py` `validate_command_schema()` checks the candidate against the hard-coded floor `runtime-0.2.3.json`. The union passes against it. Per the `generate.py` docstring, the floor advances only after an authorized publication. At release, add `tests/fixtures/published-command-schemas/runtime-0.2.4.json` (the union bytes), add its entry to `sources.json`, and advance the floor. This is a release step, not something I applied.
4. **Agent must commit the union as a branch.** Runtime's pin is "byte-identical Agent-owned". The union I built is a scratch file from a textual merge. Agent has to produce the same bytes on a real `tl/integration`-based branch (e.g. by merging the three pending branches in the order above), and the Runtime pin should be copied from that commit. I did not verify that Agent's own suites pass on the union.
5. **shot.pool commit history.** The branch's own commit message says "Runtime artifact regeneration for the new args is a follow-up." This report is that follow-up's input; no code was changed here.

## Unverified / not done

- I did not run Agent's test suites (`make check`, pytest lanes, `tests/editing_conformance`) on the union or the single-op candidates. I only used read-only git and structural/textual checks.
- I did not run Runtime's test suite. I ran only Runtime's generators on a scratch copy and its compatibility function.
- The union hash is for a scratch merge. It stands until Agent commits the file.
- Runtime's `tl/integration` is at `9411426`, and I used that tree for the generator run. The pin I compared against is the Agent commit `d4743e29`, which I located by hashing every historical version of the schema on all refs.

## Reproducibility (scratch only, nothing in repos)

Scratch dir: `/tmp/claude-0/-home-user-work-wt-agt-runtime-artifact-needs/78eeb74c-4354-46c3-b468-edfe0e272acf/scratchpad/`
- `schemas/` holds the per-branch schema exports, `delta.py` (structural diff), `merge.py` (3-way merge), `union.json`, `compat_run.py` (floor check), `findpin.py` (finds the Agent commit whose schema hashes to the Runtime pin).
- `rt/regen.py` (generator driver), `rt.tar` (Runtime archive), `rt/{baseline,integration-only,only-*,union}/` (regenerated outputs).
- Commands: `/home/user/work/venv-runtime/bin/python -I .../rt/regen.py <label> [candidate.json]` and `/home/user/work/venv-runtime/bin/python -I .../schemas/compat_run.py`. The venv was used only to run; nothing was installed into it.
