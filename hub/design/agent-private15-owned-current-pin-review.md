# Agent private15 owned current pin review

Date: 2026-10-21 UTC

## Decision

**APPROVE — normal PRIVATE C3d consumer pin for source-only staging.**

This approves the exact Agent consumer tree for the unpublished Runtime c3d
producer. It does not approve Runtime/Agent integration adoption, publication,
activation, release, App pairing, rendering, or any live/native/outer workflow.

## Exact identities

- Agent consumer commit/tree: 8444290337e2f7cb22e39b995834a80cb1cc1ef2 /
  238da4afbb635ca4ba3ea4730494a7bdb14c38e2.
- Current-Main parent: 6efc81500a0e0688c2bb41e736503f0fc3e04abb /
  2ed2b8a12b5b3391ca221ba6ff05390f71a73556.
- Runtime producer checkout: /home/user/work/wt/rt-pin-c3d26567.
- Runtime producer commit/tree: c3d26567ff6fe4e20a959476d40aff90ad23a0ca /
  f3ae49d38454ce73a9c91a954bb530b3ce51c122; checkout was detached and clean.

## Pin and release-boundary review

The normal updater and checker were run against the exact producer:

    PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/vendor_lock.py update runtime.lock.json --producer /home/user/work/wt/rt-pin-c3d26567
    updated runtime.lock.json from astrid-runtime c3d26567ff6f

    PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-c3d26567
    ok runtime.lock.json (matches producer manifest)

    git diff --check
    pass

The updater left the worktree clean. Direct byte/hash inspection found 15
locked consumer files, 76 producer manifest artifacts, zero consumer/lock/
manifest mismatches, and the full c3d26567... source selector. The distinct
producer identities are retained:

- health/schema: sha256:07c0668b2fb16226475429ec65637404c0b2e885e1b88e67f896e249089d6680;
- raw timeline bundle: sha256:bbbae375837456b267d9f0c7de89b962966da79a24abe7c4720301423b333bcb;
- artifact-manifest version: sha256:2df8ebf4fb17cae1b62e78a262b2b20b393770d045d0ef8748207ac7efacbfbb.

The Agent schema is byte-identical to the producer contract schema at
sha256:84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc.
The imported generated client reports contract 0.2.15, the 07c... schema
digest, and exports the four private argument roots. No release/package
metadata or integration reference was changed.

## Semantic source and preservation review

The bounded floor/inventory lane passed:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-private15-floor tests/sdk/test_timeline_materialization_schema_union.py tests/sdk/test_timeline_current_union_schema.py::test_next_successor_is_exactly_complete_frozen_s2_plus_reviewed_additions tests/sdk/test_timeline_current_union_schema.py::test_each_added_definition_and_operation_matches_its_approved_source tests/sdk/test_timeline_current_union_schema.py::test_all_published_floors_preserve_every_field_with_only_historical_pattern_widening tests/sdk/test_timeline_current_union_schema.py::test_closed_union_operation_inventory_is_exactly_the_supported_cohort tests/sdk/test_timeline_composed_schema.py::test_every_registered_operation_has_closed_canonical_args_and_a_valid_golden
    27 passed in 4.46s

This verified the exact 59 definitions, 33 closed operation clauses, 12 v2
clauses, and the ordinary, group, project-data, carrier, voiceover, extent,
published, and frozen-S2 floors. A direct schema probe confirmed clip.move-set
is absent, project-data mode is only replace, TrackSet has no mute field,
ClipSet has no opacity/reference carrier, and occurrence media args have no
film-reference carrier.

The selected current-main infrastructure/safety/restore/Scene/PARAM/rational
source files were byte-identical parent-to-target: 16/16 protected files. The
pure preservation lane passed against the exact c3d checkout:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-c3d26567" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-private15-preservation-c3d tests/sdk/test_scene_caller_preservation.py tests/sdk/test_scene_dispatch_contract.py tests/sdk/test_scene_save_core.py tests/sdk/test_timeline_param_values.py tests/sdk/test_timeline_selected_param_authority.py tests/sdk/test_timing_compiler.py tests/sdk/test_timing_cycles.py tests/sdk/test_timeline_checkout_restore_recovery.py tests/timeline/test_shot_composition_projection.py tests/timeline/test_authoring_bundle.py
    216 passed, 2 skipped, 1 deselected in 45.20s

The changed authoring_bundle/shot_composition code is limited to the explicit
source-closure and guarded group-migration semantic delta. The target
voiceover file is 227 lines smaller than the rejected outer-proposal commit;
the rejected _trusted_outer_producer, settled-proposal, and speech-runtime
helper markers are absent from the target delta. No free-multi, project-data
remove, track-mute, opacity, film-reference, or outer-helper source was added.

Generated Ruff was compared with the producer rather than manually repaired:
both consumer and producer generated-client checks exit 1 with 56 identical
normalized findings (51 E701, 3 F821, 2 I001). This is a generator baseline,
not a pin mismatch.

## Limits and notes

- No full suite, live socket/localhost suite, browser, renderer, release,
  adoption, integration mutation, or public tuple was run or claimed.
- An initial preservation command used /home/user/work/runtime and stopped at
  collection because that integration checkout lacks durable_replace; the
  same bounded tests were rerun with the exact c3d producer checkout above and
  passed. This was test setup, not product evidence.
- An initial import probe incorrectly expected SCHEMA_DIGEST at the package
  root; the corrected import from contract_metadata/generated passed and
  reported the exact 07c... digest. No source was changed.

Recommended next step: retain this as staging-only approval and let the
orchestrator coordinate any separately authorized paired consumer/adoption
qualification; do not relabel this evidence as a release or integration pin.

