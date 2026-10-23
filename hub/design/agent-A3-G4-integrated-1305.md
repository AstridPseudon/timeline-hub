# A3/G4 integrated qualification — source-ready packet

## Result

Bounded qualification PASS for the reviewed A3/G4 source slice. This is a
source-ready P1 packet, not a P1 end-to-end GO and not a P2/P3/inverse claim.
No product, test, schema, generated, pin, contract, dependency, or configuration
file was edited by this worker.

Agent source: `f6116e1b658514021cbbf08d5a6f16a240523f1a`, tree
`26f260e0674161f9f786bf93b15a1477a5e63a86`.

The merge has the requested ancestry: first parent `1045d1f6f6fd5c68a296f6452e6f7e7ff174a0ba`
(R1 atomic + copied-source baseline) and second parent
`8eb98564075b7c084f00c29d5746f15ab36365a6` (image-hold source). The first-parent
delta is exactly the three reviewed image-hold paths; the second-parent delta is
the five expected R1/copied-source paths. No additional merge churn is present.

## Exact reviewed source retention

The following current blobs are byte-identical to the approved review sources:

- review 1246 / `bfcf78db9`: `authoring_bundle.py`
  `c00323f0755d2d6b2409df952a61c9e154c85d95`,
  `native_occurrence_duplicate.py`
  `4338045a2272765dd1e35ff17bbca357ccc4fe04`, and
  `test_occurrence_fork_source_baseline.py`
  `dad27a538885ab45dd03242ee167e00ff615dd3`;
- review 1248 / `8eb985640`: `native_occurrence_media_commands.py`
  `4f573fedef947cfd39858f616adb49a9846df0ad`,
  `test_occurrence_hold_current_runtime.py`
  `94de6273cb814b77f9963418da59a8af6e2668d1`, and
  `test_recipe_occurrence_media.py`
  `072b777aa723d73527ac56e9a4877553ca9f3615`.

Resolver/hydration source is retained in the reviewed `authoring_bundle.py` and
`native_occurrence_duplicate.py` blobs above. R1 atomic
`astrid/sdk/timeline/_commit_patch.py` is exact against qualified `5b1b4db82`:
blob `c2993997edecda94ad6bd9853cbc40a2e3ce804d` on both trees.

## Runtime and retained pins

The only Runtime execution used here is current Runtime 3b:

- checkout `/home/user/work/wt/rt-pin-3b926efa`;
- commit `3b926efab2eed122d374540baee297d4cdcec62a`;
- tree `b794170504544b259781e50d7ca4d61b6729e67c`.

Runtime 9345 (`9345cb58fe8c54f114d666929e167bbeb5899c6c`) was not run or credited;
its publichold4 evidence remains HELD. The Runtime fork+patch whole-commit undo
failure was not rerun.

Retained ABI/provenance checks are unchanged: `runtime.lock.json` still pins
normal frozen Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc`; the canonical
edit-command schema has SHA-256
`d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`; and the
Composition archive remains SHA-256
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
The full-v2 request/reply surface remains represented by the existing production
caller and witness: scope/base pair, commands/select/args, label, complete steps
(id/label/intent/tags/ordinals/patch/reads), merge, reads, idempotency, dry-run,
source/rationale/group_id, and authoritative accepted/merged/conflict/invalid,
canonical/records/bindings/effects/dependencies/history/undo_steps, preview
`would_status`, and structured errors. No alternate executor or invented reads
were introduced.

## Tests and checks

Exact targeted command, with explicit lane selection:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m 'not integration' tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_recipe_occurrence_media.py
```

Result: **82 passed, 1 explicitly declared integration deselection** in 7.49s.
The deselected case was `test_current_runtime_retained_fork_then_emitter`.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_recipe_occurrence_media.py
```

Result: **1 passed, 82 explicitly declared non-integration deselections** in
4.42s. Collection was 83 total cases: 16 fork-source controls, 1 Runtime 3b
witness, and 66 recipe-media controls.

Additional checks:

- scoped Ruff on the six reviewed source/test paths: **pass**;
- private mypy on the three changed source modules: **no issues**;
- `scripts/vendor_lock.py check runtime.lock.json`: **ok**;
- `scripts/artifact_manifest.py --check`: **current**;
- `git diff --check`: **pass**.

Normal reviewed evidence is reused rather than duplicated: exact retained blobs
carry the prior **2149/2149 Ruff** and **1912/1912 mypy** results.

Not run or claimed: full suite, browser/HTTP/P1–P4 live journeys, native14/58,
Runtime 9345 publichold4, and inverse/whole-commit qualification.
