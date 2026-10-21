# Agent source-unions final contract review

## Verdict

**APPROVE — source contract only.**

Reviewed the completed bounded union at commit
`5672d2b7deee2bfe2ab375fd6db5fc35a192591d`.

- Committed Git tree: `6dd13b552c4f07fff5586b1fa772bdbdf64accba`.
- The source worker report also records its complete-worktree identity as
  `ba9229f4110070fbcf12e6a3bb8244bde7f1b5b4`; the committed Git tree above is
  the exact reproducible tree used for this review.
- Canonical schema:
  `astrid/core/timeline/schema/edit-command.schema.json`.
- Raw schema SHA-256:
  `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`.
- Canonical formatted schema SHA-256:
  `9c05ec496e957548fe4656ca655a67a7b936ff4f220bdedae474a680e6d32eb9`.
- Inventory: 62 definitions and 36 closed operation clauses.
- Activated callers: none.

## Contract findings

- The literal remove/mute/opacity union preserves the approved `f448c4b40`
  source. Explicit remove remains distinct from null/absence, opacity is
  bounded to `0..1`, opaque siblings survive, and the existing write,
  rebase, and strict ABA inverse guards remain in place.
- The corrected movement source is retained as the approved `3b3208c43`
  cohort. `clip.move-set@1` captures the complete member selection and order,
  destination identities, source/track/rate evidence, and exact quantization;
  it rejects membership, source, lane, timing, and identity changes. The
  parent after-clip birth is raw-anchor-only, clones the captured authored row
  while changing only reserved identities/timing, records order and peer
  guards, and keeps the derived clip mirror synchronized.
- `timeline.reference@1` is parent-only, role `source`, and carries only the
  existing two-field `MediaManifestEntry`. Raw metadata is obtained only from
  the optional scoped Runtime `raw_media_info` verification result; no managed
  tuple or caller metadata is treated as authority. Occupied reference and
  same-ID ordinary asset identities refuse atomically.
- `track.reorder@1` is parent-only and requires a complete same-owner
  permutation plus the captured expected order. Its `parent::track_order`
  address is virtual recorder state; raw track rows and opaque fields are not
  rebuilt. Membership/order changes and direct or A→B→A inverse interference
  refuse.
- All three additions are registered at version `1`, have closed schemas and
  matching registry parameters, and are covered by the exact composed-schema
  inventory. The diff adds no public caller, Runtime/App/Composition code,
  generated artifact, pin, freeze, or native adoption.

The compact reconstruction checks reproduce the exact `84fc0863`, `65bb68ac`,
`27f2e3ed`, `39211e63`, `613123b2`, and `6ba7b51` floors, as well as each
individual literal, movement, and reference/order source floor. No source unit
was dropped and no old schema was copied as the union.

## Evidence

All commands below ran against a private archive of the exact reviewed commit;
shared dependencies remained read-only.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TMP_REVIEW:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider "$TMP_REVIEW/tests/sdk/test_timeline_materialization_schema_union.py"
25 passed in 1.82s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TMP_REVIEW:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider "$TMP_REVIEW/tests/sdk/test_timeline_current_union_schema.py" "$TMP_REVIEW/tests/sdk/test_timeline_composed_schema.py"
39 passed in 192.60s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TMP_REVIEW:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider "$TMP_REVIEW/tests/editing_conformance/test_recipe_free_move_set.py"
79 passed in 11.89s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TMP_REVIEW:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider "$TMP_REVIEW/tests/editing_conformance/test_recipe_m2_parent_media.py"
91 passed in 19.75s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TMP_REVIEW:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider "$TMP_REVIEW/tests/editing_conformance/test_recipe_m2_parent_reference.py" "$TMP_REVIEW/tests/editing_conformance/test_recipe_track_order.py" "$TMP_REVIEW/tests/sdk/test_timing_compiler.py"
69 passed in 1.30s

git diff --check 5672d2b7deee2bfe2ab375fd6db5fc35a192591d^ 5672d2b7deee2bfe2ab375fd6db5fc35a192591d
PASS
```

No full, Runtime/App, browser, live-socket, generation, freeze, pin, or native
adoption suite was run or inferred. Runtime/App qualification and activation
remain later manager-owned work.
