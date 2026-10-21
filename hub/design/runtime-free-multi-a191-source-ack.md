# Runtime bounded SOURCE ACK — Agent free-multi a191

Date: 2026-10-21 UTC

## Verdict

Bounded carrier/closure review is source-compatible, but the ACK is **not a
clean timing qualification**. One concrete existing Runtime mismatch remains:
the visual-seam timing evaluator rejects both rational FPS spellings approved
by Agent. No Runtime code, DTO, store, API, schema generation, pin, freeze, or
adoption was changed here.

## Exact source identities

- Agent proposal commit/tree: `a19192ea789a209260da46bfbdd5b616fc7cc4ac` /
  `f7f652366004a5517704ed1e4239c3792b4ab84a`.
- Agent command schema raw SHA-256:
  `f44b00983b2d5e8c3f137985baabb8b226fe00e821fed74e66444fa3fbdd3a69`.
- Agent schema normalized formatted-with-newline SHA-256:
  `ba0c42d6a9359c32d89d8088416f7bc9092481dbd05f236e4d7e6e019c9246e7`;
  60 definitions / 34 operation clauses / 12 explicit v2 clauses.
- Removing only `clip.move-set` reconstructs the exact `84fc` floor:
  `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`;
  59 definitions / 33 clauses / 12 explicit v2 clauses.
- Reviewed Runtime worktree HEAD/tree: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` /
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Current Runtime command-schema floor remains raw SHA-256
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
  its current generated bundle is raw SHA-256
  `6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3`.
  This source review therefore makes no claim that the current generated wire
  artifact advertises `clip.move-set`; generation/adoption is separate.

## Runtime source review

- The Agent carrier is explicitly parent-owned: `select: "parent"`, stable
  parent clip/track refs, preserved member argument order, and no occurrence
  writes. `_move_set.py` rejects any destination lane containing an occurrence
  (`move-set destination contains an unsupported occurrence`) and records the
  parent provenance before writes.
- Runtime closure admission keeps the existing ownership boundary. Parent
  `clips` and `config.clips` must be lists and agree when both exist;
  `RawClip`, `ParentComposition`, and `RawOutput` retain open/opaque fields.
  Occurrences remain required, uniquely identified, and complete against the
  supplied shot revisions and internal timelines. Existing revision rows use
  exact project/owner/payload/content-digest identity checks; parent occurrence
  rows also preserve authored ordinal/order. `_persist_closure` stores the
  accepted canonical parent payload with the existing `canonical_json` path.
- The existing `CommitAccepted` result shape already returns the canonical
  document, exact recorded commands, identity `id_map`, provider/compiler
  versions, and normal publication metadata. No new Runtime semantic writer or
  DTO/store/API field is required for this carrier.
- Agent forward replay source inspection confirms the corrected owner policy:
  `rebase.py` uses the existing identity-only forward path, then applies a
  second move-set check for structural/source/identity reads; inverse and
  restore paths remain strict. The move-set source retains selection/order,
  membership, lane/source, and opaque-field reads. The shared rational parser
  accepts mapping and two-item list forms and records a canonical numerator /
  denominator time-map dependency.

## Concrete mismatch

`runtime_protocol/visual_seam.py:141-143` computes FPS through `finite()`,
which accepts only scalar `int`/`float`. A direct current-Runtime probe gave:

```text
{'numerator': 30000, 'denominator': 1001} ValidationError visual timing fps must be finite and positive
[30000, 1001] ValidationError visual timing fps must be finite and positive
```

Thus Runtime raw closure/schema storage is lossless for the rational mapping
and list forms, but the existing visual-seam evaluator does not consume them.
This is the one executable compatibility negative for this review. It must be
resolved or explicitly bounded before claiming complete Runtime timing
compatibility for the a191 carrier; no clamp, scalar default, or millisecond
quantization should be introduced as the fix.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_current_union_contract.py::test_exact_frozen_schema_and_operation_inventory_are_packaged \
  tests/test_timeline_commit_port.py::test_opaque_foreign_looking_json_is_preserved \
  tests/test_timeline_commit_port.py::test_request_validation_uses_frozen_schema \
  tests/test_timeline_commit_closure_invariants.py::test_duplicate_occurrence_identity_refuses_before_acceptance \
  tests/test_timeline_commit_closure_invariants.py::test_accepted_dependency_and_occurrence_corruption_fails_closed \
  tests/test_timeline_raw_payload_contract.py::test_raw_conformance_payloads_validate_without_mutation \
  tests/test_timeline_raw_payload_contract.py::test_malformed_parent_containers_refuse_422 \
  tests/test_visual_seam_admission.py::test_fractional_occurrence_bounds_match_render_frames_and_preserve_real_gaps
25 passed in 2.25s
```

No full, browser, live-socket, render, generation, pin/freeze, adoption, or
integration suite was run.
