# D69 odd-c semantic review

## Scope and result

Independent read-only review of exactly corrected odd immutable indexes
`69, 75, 81, 85, 89` from
`handoff-agt-F-D69-odd-inventory-return-1005.json`. The five indexes are
disjoint from the already reviewed odd/even batches. Old source is
`08e6b905114a3ee2b05c3e7980421f26b4abf15c`; captured corrected source is
`d6294843286c18e57af3c1874cf1996be42212d2`; current normal source is
`d0ecf1d69a7b37f86034bc52004f73f6c6231603`. All five current-normal target
blobs equal captured-new blobs.

Result: **5 functions reviewed; 1 PASS, 4 equivalent-approved; 0 FAIL, 0
UNRESOLVED.** The only apparent old-purpose change (index 75) is an explicit
approved policy change in `ecbd20a344`: scene findings are advisory
`CheckReport.problems`, while structural invalidity remains blocking. No
source or test repair was made.

## Per-function decisions

### Index 69 — `test_checkout_keeps_its_members_and_mixins`

Path: `tests/sdk/test_timeline_checkout_facade.py`; old line 116, new/current
line 151. Old body source-range SHA-256:
`008406e2a3d098f312e60ac2514af534b0751e9456614a9532bf4e799193899e`.
New/current body source-range SHA-256:
`cdcbe5afb1a1830d803fdddcbf8275c86d3e140ac0ea53b11a55358bb07cbf8c`.

Old assertions were `missing == []` and every name in `MIXINS` appears in
`Checkout.__mro__`. The added unit at current line 160 is:

```python
assert getattr(Checkout, name) is getattr(_CheckMixin, name)
```

Verdict: **PASS**. This is a stronger identity predicate inside the same
facade-members/mixins purpose; no old predicate is removed. The mounted
production caller is `astrid/sdk/timeline/checkout.py:16-33`, where
`_CheckMixin` is imported and mounted in `class Checkout(...)`; the mixin is
defined at `astrid/sdk/timeline/check.py:69`.

### Index 75 — `test_a_picture_gap_blocks_publishing_and_says_what_is_left_on_screen`

Path: `tests/sdk/test_timeline_reflow_golden.py`; old/new/current function line
230. Old body source-range SHA-256:
`130d8e1eb43203ab9834e5d6aceecd29134b9f324621c9daceb32644ff41328a`.
New/current body source-range SHA-256:
`caf5487b7cd10a7d7ca097279f3ac1454d1ff6cf2e748f2d45eb7f6797d9e192`.

Removed unit:

```python
assert any(line.startswith("picture") for line in tl.check().blocking)
```

Added unit at current line 239:

```python
assert any(line.startswith("picture") for line in report.problems) and not report.blocking
```

Verdict for both changed units: **equivalent-approved**. Commit
`ecbd20a344068a277b5fbf249217cf3fa069b209` explicitly moved picture gaps,
empty-cut findings, and dips through `_scene_problems` as advisory check
problems. Current production `astrid/sdk/timeline/check.py:232-237,653-675`
retains the exact picture text in `problems`; `astrid/sdk/timeline/publish.py:125-145`
uses `_check_core` for writer safety, while structural invalidity remains in
`blocking`. This is a settled source-policy replacement, not an unapproved
loss of the old assertion.

### Index 81 — `test_runtime_pin_flow_returns_old_script_after_binding_rebind`

Path: `tests/sdk/test_timeline_script.py`; old line 149, new/current line 157.
Old body source-range SHA-256:
`fe4fe378aa738301b410bd11c0d19349f861aa639c76200b54b3a5a4868675f8`.
New/current body source-range SHA-256:
`3a9416cb130bcc0ab28eadcb0e98eb56f8cb1aea57e966868cf8213dae433372`.

Removed unit:

```python
assert result.data["revision_id"] == "parent-2"
```

The current registered-commit route adds these exact units:

```python
assert binding_result["data"]["accepted_revision_id"]
assert rebound_result["data"]["accepted_revision_id"]
assert live["media_id"] == rebound["object_id"]
assert result.data["revision_id"] == expected_revision
```

Verdict: removed revision-name assertion is **equivalent-approved**; the first
three added receipt/live-binding units are **PASS**; the canonical revision
identity unit is **equivalent-approved**. The old `publish_parent_composition`
and mutable `set_project_shot_text_binding` setup is replaced by the registered
`create_runtime_commit_service()` provider, explicit `commit_timeline` v2
bodies, native capture, and an explicit `revision_id` selector. The mounted
reader is `astrid/sdk/timeline_script.py:10-89`: it passes the pinned revision
to `timelines.inspect`, rejects revision/snapshot drift, and reads the pinned
object bytes. The current test's provider registration and commit route are at
lines 168 and 206-209. Historical text remains asserted at lines 284-285.

### Index 85 — `test_joined_music_updates_source_and_literal_duration_for_publication`

Path: `tests/sdk/test_timeline_structure.py`; old line 82, new/current line
225. Old body source-range SHA-256:
`f4a04367eb20e3c84873d0c301b91fa311950d6635a27cda9ba585228cbe7cc0`.
New/current body source-range SHA-256:
`36cba9b4a9b6e853580842a373d818b74d534c09d153f4fceee0db08d61e8927`.

Removed units:

```python
assert publication["expected_head"] == "rev-0"
assert result["publication"]["data"]["new_head"] == publication["parent_revision_id"]
```

Added units at current lines 252-254 and 259:

```python
assert publication["base_revision_id"] == "parent-1"
assert publication["base_publication_id"] == "publication-1"
assert publication["api_version"] == 1
assert result["publication"]["data"]["new_head"] == result["publication"]["data"]["accepted_revision_id"]
```

Verdict: both removed units are **equivalent-approved**; all four added units
are **PASS**. C0/G5 retire `expected_head` and the old publication result
shape. The mounted production boundary is
`astrid/core/timeline/authoring_bundle.py:44-54,1833-1897`: the authoring
writer sends `commit_timeline` with the v2 base selectors and normalizes
`new_head` from `accepted_revision_id`. `astrid/sdk/timeline/publish.py:188-203`
is the normal Checkout commit caller. The retained music source, literal
duration, canonical document, and accepted-head authority are all still
asserted.

### Index 89 — `test_source_profile_provisions_explicit_render_runtime`

Path: `tests/stage1/test_cold_launch_autobootstrap.py`; old/new/current function
line 71. Old body source-range SHA-256:
`1d434ff1b5efaec5884e85acde721d04f8b61130324e7ff296b180260cc69782`.
New/current body source-range SHA-256:
`c2d079d3d1482f02c43ca6f8463071e7c35c2d59f996fd11ff108e7bc44af8df`.

Removed unit:

```python
assert child_env["ASTRID_TIMELINE_SCHEMA_PYTHONPATH"] == str(schema.parent.resolve())
```

Added unit at current line 97:

```python
assert child_env["ASTRID_TIMELINE_SCHEMA_PYTHONPATH"] == str(schema.resolve())
```

Verdict: **equivalent-approved**. Commit
`dfea1e17b7ed227b73bcb06aa9b334f9edc2fb5d` retires the obsolete external
Python schema subtree and binds the source profile to the canonical
Runtime-pinned schema file. The mounted caller is
`astrid/sdk/host_bootstrap.py:461-493`; it computes
`source_path / SCHEMA_RELATIVE_PATH` and assigns `verified_schema_path`, whose
checks are in `astrid/core/rendering/_local_schema.py:12,23-51`. The new test
also copies the canonical schema, lock, and reader inputs, so the path
assertion is exact source equivalence rather than a lexical path change.

## Conservation and verification

- Assigned functions: 5; removed assertion units: 8; added assertion units: 13.
- Original whole-audit conservation remains untouched: 129 functions, 113
  removed units, 287 added units; odd/even split remains 64/65, 67/46, and
  178/109 as recorded by inventory.
- Static source/blob identity and JSON membership checks: PASS.
- AST parse of all 15 old/captured/current target source blobs: PASS.
- `git diff --check` in the assigned Composition worktree: PASS.
- Tests, pytest, collection, typecheck, and lint: N/A for this read-only task;
  not run. No product/test/ledger/source edit was made.

Machine-readable row evidence: `workers/agt-F-D69-odd-c-1032/evidence/assigned-rows.json`.
