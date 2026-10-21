# RT08 item/global witness independent review

## Verdict

REQUEST CHANGES. The changed test is structurally sound as a single positive
case, but the required targeted evidence says that two parameterizations are
expected. The exact selector collects only one node, and neither the test nor
its `film`, `agent`, or `astrid_importable` fixtures is parameterized. I did
not queue the central run because the prerequisite collection did not match
the settled brief.

## Review

The source setup uses `RuntimeService.publish_parent_composition`, not SQL
inserts or fabricated history. It reads the existing closure, adds one opaque
source item to each of `shot-2` and `shot-3`, updates the parent occurrence
revision pins, and publishes through the normal API. That API creates the
project-shot, shot-item, immutable revision, head, parent revision, dependency,
and timeline-event rows. The source item lookup in the test also makes an empty
source publication fail rather than silently passing.

The positive body uses the real Agent move command and the startup-loaded
provider. It checks the source shot pin, occurrence owner binding, source item
mapping, physical destination, opaque metadata preservation, restart plus
inverse restoration, and exact own-slot/id-map reuse. The unrelated writer is a
normal same-project `create_project_shot` plus `add_shot_item` call after the
candidate is prepared. The refusal snapshot is taken after that writer and
compares the complete SQLite `iterdump`, so the candidate refusal covers the
whole durable store. The test does not grant caller-supplied map authority:
the map is read from the recorded dependency pin and only used to select the
unrelated occupancy identity.

No schema bypass, direct history manipulation, hidden SQL writer, or source
edit was found in the changed test. The static Runtime path also confirms the
normal publication inserts the relevant nonzero rows; no explicit row-count
assertion is present, but the real source-item lookup and normal publication
path prevent an empty fixture from satisfying the body.

## Evidence

Prerequisite collection command:

```text
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-4b7a2712 PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-4b7a2712" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -p no:cacheprovider -m integration 'tests/test_timeline_projection_occupancy.py::test_startup_provider_materializes_source_items_and_refuses_global_item_occupancy'
```

Result: `1 test collected in 0.66s`; no parameterized node was collected.

Read-only import/pin check passed. Agent source imported from
`/home/user/work/wt/agt-pin-4b7a2712` at `4b7a27127fb9b642be8ad118e6aa663bd7761611`
(tree `a6126ed13a7b4dad8124894ebced1cf1b5977d5f`); Runtime is
`560f6bce54ed5bea400d8952b9b2d4b7df57e48c` (tree
`065e602ba4fa336e162977cac199b48388d97e30`). `git diff --check 42a7203..560f6bc`
passed. No socket body, central targeted run, broad suite, browser, render, or
install run was performed.

The central command that would have been used after a valid two-node
collection was deliberately not submitted:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-rt08-item-global-targeted-review-1156 private017-agent4b7-integration --files "tests/test_timeline_projection_occupancy.py::test_startup_provider_materializes_source_items_and_refuses_global_item_occupancy"
```

## Required follow-up

Add the intended two parameterizations (or correct the brief if one node is
actually intended), then recollect the exact selector and run exactly one
central targeted `private017-agent4b7-integration` request. The test body and
the existing limitations remain unverified until that run completes.
