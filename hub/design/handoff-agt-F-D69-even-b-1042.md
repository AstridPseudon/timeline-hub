# D69 independent READ ONLY semantic review — even-b

Status: **COMPLETE ASSIGNED SUBSET; NOT WHOLE-AUDIT PASS**.

Reviewed exactly immutable `function_index` values `28, 30, 38, 46, 54` from
`handoff-agt-F-D69-residual-even-0945.json`. The review used complete old
`08e6b905`, captured-new `d6294843`, and current-normal `d0ecf1d` source. The
five current target file blobs in the Agent integration checkout equal their
captured-new/current-normal blobs exactly. No other function or reviewer
membership was inspected for ownership.

Subset result: **10 PASS, 2 equivalent-approved, 0 FAIL, 0 UNRESOLVED**.
The two equivalent-approved units are the retired generator non-vacuity guard
and retired `@workspace-effects` alias. The ten added units all preserve the
old purpose and are PASS. Global `129/113/287` conservation is unchanged.

## Per-function decisions

### Index 28 — equivalent-approved

`tests/packs/rendering/test_remotion_typecheck_mappings.py::test_every_scope_the_generator_emits_is_declared_and_mapped`

- Old body: lines 70–75, blob
  `443a1866d729126c49b63182b3c3aad475cd182a`, SHA-256
  `1d13df16301d86426684a5f0c2d2abdbbef19009f68c3d33b138eae413e2527e`.
- Current body: lines 72–82, blob
  `9428061ca456752e0050bd2f751bec54137cc7d6`, SHA-256
  `045ac58caed14ffaebb42bca6e99b2ca351e3116ab1fc402dbbae2f663831353`.
- Removed line 72: `assert emitted, f"the generator emitted no {kind} imports; the check would pass vacuously"` — **equivalent-approved**. Current generator behavior intentionally has a no-host-import case when Composition owns the public implementation. The current fallback checks the exact generated `resolveElementRegistries(DEFAULT_THEME).<kind>` source before returning, while the mapped-import assertion remains for host imports.
- Added line 78: `assert f"resolveElementRegistries(DEFAULT_THEME).{kind}" in generated` — **PASS**. This is the faithful non-vacuity successor for the Composition-owned branch.
- Mounted production callers: `astrid/core/rendering/_effect_registry.py:378-452` and `remotion/src/host-registries.ts:1-21`; host registries merge Composition's resolved maps with generated host maps. The named test migration is commit `42476c08a6`.

### Index 30 — equivalent-approved

`tests/packs/rendering/test_remotion_v3_aliases.py::test_native_defaults_and_explicit_roots_ignore_later_cwd`

- Old/current body lines: 93–111; old blob
  `69818c2fa167435a5b9bf79e9d069088b1aa4c75`, SHA-256
  `ef4a4db57dc5c2beedcd6f6f28a3d68ff3e4beaafe6605eaf6d35e71078abf68`;
  current blob `403701d74b1906dc9763b3fffc07a0988f42d261`, SHA-256
  `b56f07454d407e6450f6c48df7501787b29f046eb7986f67712640de35e4b2c5`.
- Removed line 111: `assert result['@workspace-effects'].startswith(str(ROOT / 'astrid/packs/rendering/'))` — **equivalent-approved**. `@workspace-effects` is no longer emitted by the declaration-driven V3 alias route.
- Added line 111: `assert result['@pack-rendering-elements-effects'].startswith(str(ROOT / 'astrid/packs/rendering/'))` — **PASS**. The current `packElementAliases` derives this selector from the rendering pack manifest and points it at the same owned element root; native/deferred alias equality and cwd independence remain intact.
- Mounted production callers: `remotion/webpack-alias.mjs:141-177,193-219` and `remotion/remotion.config.ts:30-32`. Commit `cbd91c3bc8` explicitly retires package-source aliases in favor of the immutable Composition package and declared pack aliases.

### Index 38 — PASS

`tests/packs/rendering/test_timeline_filmstrip_execution.py::test_input_only_is_a_materializable_compact_filmstrip_bundle`

- Old body lines 18–68, blob
  `2dd6eef31a4f05e739768ceb4d71f9c6ae3e6c6b`, SHA-256
  `e63ba04e286fb4ea63072095f07af380c79a5cfaebccdbdec61bad1bf8b46888`.
- Current body lines 18–91, blob
  `8f6b0610e0302164d81321af90e9e59ee74f453a`, SHA-256
  `8b11140859b32d8bfbc0b5a9b5dc680a44817d8ff0b15291193932af431a269b`.
- No removed units. Added lines 59–64 (five assertions) — **PASS**: exact `UNCERTIFIED preview (claimed revision R1)` label in the result, frame-index provenance, Markdown title/body, and drawn PNG text. All old manifest/schema/pages/inspection/audio/ZIP digest/SDK materialization assertions remain.
- Mounted production callers: `provenance.py:84-153` derives the label; `filmstrip_execution.py:147-167,248-273,333-335,388-440` propagates it to index, Markdown, and PNG; `filmstrip_cards.py:767-769,1030-1034` preserves provenance; `astrid/sdk/invocation.py:1693-1735` performs digest-checked bundle materialization. The source change is commit `8a0ac84acf`.

### Index 46 — PASS

`tests/packs/timeline/test_cli_edit_flags.py::test_edit_nudge_frames_set_and_close_gap`

- Old body lines 145–154, blob
  `b3b976c23837af668cce545c974009c5ac7185e2`, SHA-256
  `25138ace80e2060c204bd8277a34a6245f242406af7f64ddf7912ed0b704a864`.
- Current body lines 145–155, blob
  `81ff077be92f6de6bc012bd607e18f7044030ce1`, SHA-256
  `935328ef18a720d7a3278a03eaaa5389b72f86988106af05261d42d79ac69b93`.
- No removed units. Added line 155: `assert any(line.startswith("next: export the complete JSON candidate") for line in out.splitlines())` — **PASS**. It strengthens the existing final-line `next:` guidance assertion. Current `_cmd_edit` emits this exact candidate-export guidance after the `--file` edit/save path.
- Mounted production callers: `astrid/packs/timeline/cli.py:3188-3217,3241-3255,3321-3325` and `astrid/sdk/timeline/edits.py:288-305`. The retained-caller migration is commit `1794f0a2e2`.

### Index 54 — PASS

`tests/reshape/test_compare_baselines.py::test_structure_baseline_script_runs_directly_from_outside_the_checkout`

- Old body lines 106–123, blob
  `9800d8e95d598d8bd94e76055c5ae96cb9d73d8b`, SHA-256
  `32331649d98bed16d9213ecef6fdd28ac1a750c930dbd8cdb7e586bb2603b08a`.
- Current body lines 108–132, blob
  `0d31ba8abaa8dd3905874a1f8516ed8b9ba31a6d`, SHA-256
  `6b655d456334e95119ae6464e70777122380a28a83d8da2cdad53513d6fe03a4`.
- No removed units. Added lines 114–116: `assert runtime_spec is not None` and `assert runtime_spec.submodule_search_locations` — **PASS**. These are explicit guards for the current Runtime package dependency. The subprocess still removes the parent Agent `PYTHONPATH`, adds only the discovered Runtime package root, executes the script from outside the checkout, and keeps the original structure-output assertions.
- Mounted production callers: `scripts/reshape/compare_structure_baseline.py:17-25,43-65`; the imported structure path reaches Runtime-backed modules such as `astrid/core/execution/_child_bridge.py:23` and `astrid/core/foundation/atomic_io.py:16`. The fixture repair is commit `8ba22da442`.

## Static evidence and limits

Evidence files:

- `workers/agt-F-D69-even-b-1042/evidence/source-checks.json`
- `workers/agt-F-D69-even-b-1042/evidence/source-checks.txt`

Commands/results:

- Source-range SHA-256 and current blob conservation script: **PASS**, 5/5.
- Python `ast.parse` of the five target test files: **PASS**.
- `git -C /home/user/work/wt/agt-F-D69-even-b-1042 diff --check`: **PASS**.
- `git -C /home/user/work/agent diff --check`: **PASS**.
- Tests, typecheck, lint, imports, collection, helpers, services, and bodies: **not run; N/A for this immutable read-only review**.

No product, test, ledger, registry, pin, generated-file, foreign-output, or
worktree source changes were made. No tests were weakened or deleted. The
worker did not write `report.md`; the final worker report is supplied in the
completion message for the harness.
