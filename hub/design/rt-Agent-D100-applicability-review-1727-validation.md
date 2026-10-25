# D100 applicability source review

## Result

**PASS_SOURCE_ASSESSMENT** — held D100 source is applicable to the exact App
projection item-birth seam, while the current product remains unqualified.
This is a source disposition only; it is not a product functional pass and does
not authorize merging the held source.

## Findings

The retained App own9 evidence reaches the real registered `doc.patch` provider
and stops at `State._item_ids` in
`astrid/sdk/timeline/_command_state.py:369`. The authenticated source shot has
an empty `item_id_map`; the candidate replacement has one authored physical
item. Current `d4ba` requires exact correspondence with that empty map, so the
nine retained selectors fail during setup (9 errors, 0 failures, 0 skips) before
Runtime acceptance, persistence, canonical reread, or duplication.

The held `d3b5` change is the smallest proved applicable seam. Its new branch is
selected only when the source mapping points to the same physical shot ID. It
then verifies the exact source shot revision, internal revision, both content
digests, and an empty alias map. It validates nonempty unique physical item IDs
and returns identity mapping without extending placement aliases. The original
strict map path remains for copied/remapped placements; its malformed, duplicate,
unknown, retargeted, and missing-source refusal behavior is preserved by the
source diff and earlier R1 review. The `capture.py` portion of `d3b5` is exact
timing work and is not part of this applicability finding.

This is Agent-provider ownership, not Runtime guard blame: the first failing
call is inside provider execution before Runtime acceptance. C0 permits guarded
membership changes within an existing root, while closure roots, managed edges,
Runtime pins, allocation records, and request/reply shapes remain unchanged.

## Minimum next acceptance

Agent owner: normally adopt and independently review the relevant
`_command_state.py` seam, then run the exact retained nine own9 selectors against
the resulting Agent and pinned Runtime tuple. The genuine failing nodes are the
nine selectors in the retained `tests/sdk/test_timeline_capture_projection.py`
own9 packet; no substitute fixture, source reconstruction, or test weakening is
authorized. Runtime repair is not required by this source review. Product
qualification remains **UNVERIFIED** until that run passes.

The `fb9a` test-repair object and frozen candidate-SDK authored fixture route
are classified **EXACTMISSING** for this review; no fetch or reconstruction was
used. The available App-side f53 packet was consumed only as prior evidence.

## Read-only checks

Exact commands and results:

```text
git status --short && git rev-parse HEAD
  PASS; clean at d4ba991638f7d94e6b9f91f5a463cd3587af00eb

git diff --check
  PASS

git diff --check d4ba991638f7d94e6b9f91f5a463cd3587af00eb d3b5cfef76b4b3abef5db5f8288abc214a61354f
  PASS

AST parse current/held _command_state.py and capture.py
  PASS

AST SHA-256 comparison for State.shot_item_map, State._item_ids,
State.project_shot_items
  PASS; exact current/held hashes are in source-manifest.json

JSON parse of prior applicability, source-manifest, and App own9/whole-path facts
  PASS

df -B1 /tmp
  PASS for source-only work: 4,981,264,384 bytes available at check;
  above 4.6 GB source floor and 4 GB stop line
```

No pytest, typecheck, lint, service, browser, socket, full/family, native,
provider-body, P4, tour, acquisition, collector, SWAP, or WAL run was made.
Typecheck/lint/tests are N/A for this read-only source assessment, except for
the recorded prior App own9 result explicitly identified above.
