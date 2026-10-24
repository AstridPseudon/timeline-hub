# F/R2 exact existing evidence retention

This publication records only evidence already present in
`agt-R2-legacy-inverse-home-1435`'s retained worker files. F/R2 did not run
tests or product source. The prior worker reported actual integrated Agent
head `68e82c0c2c` with Runtime fixture `e68cf231`, production caller coverage,
and an exact 13-node PASS. The prior worker's finalizer removed
`/tmp/w-bda7eb9404`; the XML files are therefore not in original-file custody.

The full retained log is copied byte-for-byte at
[`evidence/agt-F-home13-retained-receipt-1440/prior-worker-log.txt`](../../evidence/agt-F-home13-retained-receipt-1440/prior-worker-log.txt).
The map, selectors, source hashes, byte ranges, custody limitation, and all 13
names/outcomes are in
[`source-selector-map.md`](../../evidence/agt-F-home13-retained-receipt-1440/source-selector-map.md).

## Transcript-retained XML

The following three payloads are copied verbatim from log lines 4011–4013;
they are transcript-retained XML, not recovered original files.

```text
<?xml version="1.0" encoding="utf-8"?><testsuites name="pytest tests"><testsuite name="pytest" errors="0" failures="0" skipped="0" tests="6" time="5.283" timestamp="2026-10-24T14:36:31.171464+00:00" hostname="vm"><testcase classname="tests.sdk.test_timeline_producer_guard_runtime" name="test_settled_artifact_mutation_refuses_without_history_or_head_changes[number]" time="0.795" /><testcase classname="tests.sdk.test_timeline_producer_guard_runtime" name="test_settled_artifact_mutation_refuses_without_history_or_head_changes[boolean]" time="0.428" /><testcase classname="tests.sdk.test_timeline_producer_guard_runtime" name="test_settled_artifact_mutation_refuses_without_history_or_head_changes[reason]" time="0.514" /><testcase classname="tests.sdk.test_timeline_producer_guard_runtime" name="test_settled_artifact_mutation_refuses_without_history_or_head_changes[digest]" time="0.640" /><testcase classname="tests.sdk.test_timeline_producer_guard_runtime" name="test_settled_proposal_queue_refuses_tampering_preserves_draft_then_accepts_fresh_request[digest]" time="0.963" /><testcase classname="tests.sdk.test_timeline_producer_guard_runtime" name="test_settled_proposal_queue_refuses_tampering_preserves_draft_then_accepts_fresh_request[target]" time="0.677" /></testsuite></testsuites>
<?xml version="1.0" encoding="utf-8"?><testsuites name="pytest tests"><testsuite name="pytest" errors="0" failures="0" skipped="0" tests="6" time="6.000" timestamp="2026-10-24T14:36:20.699893+00:00" hostname="vm"><testcase classname="tests.sdk.test_timeline_legacy_inverse_bindings" name="test_legacy_producer_forward_inverse_and_redo_bind_every_stage_effect" time="1.969" /><testcase classname="tests.sdk.test_timeline_legacy_inverse_bindings" name="test_legacy_inverse_rejects_incomplete_or_misattributed_effect_binding[missing]" time="0.647" /><testcase classname="tests.sdk.test_timeline_legacy_inverse_bindings" name="test_legacy_inverse_rejects_incomplete_or_misattributed_effect_binding[duplicate]" time="0.653" /><testcase classname="tests.sdk.test_timeline_legacy_inverse_bindings" name="test_legacy_inverse_rejects_incomplete_or_misattributed_effect_binding[wrongside]" time="0.725" /><testcase classname="tests.sdk.test_timeline_legacy_inverse_bindings" name="test_legacy_inverse_rejects_incomplete_or_misattributed_effect_binding[wrongeffect]" time="0.807" /><testcase classname="tests.sdk.test_timeline_legacy_inverse_bindings" name="test_legacy_inverse_rejects_incomplete_or_misattributed_effect_binding[wrongphysicalsource]" time="0.795" /></testsuite></testsuites>
<?xml version="1.0" encoding="utf-8"?><testsuites name="pytest tests"><testsuite name="pytest" errors="0" failures="0" skipped="0" tests="1" time="2.117" timestamp="2026-10-24T14:36:27.978345+00:00" hostname="vm"><testcase classname="tests.sdk.test_timeline_producer_guard_runtime" name="test_settled_numeric_proposal_accepts_retries_after_restart_and_undoes" time="1.684" /></testsuite></testsuites>
```

The exact source-log byte ranges and SHA256 values are recorded in the map;
the three extracted files are also retained in the evidence directory.

## Contract retention checklist

The approved v2 contract scope remains represented without claiming new
implementation proof: request `api_version`, `project_id`, `timeline_id`,
`base_revision_id`, `base_publication_id`, `commands`, `label`, and steps with
`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, and `reads`; merge
`fields|atomic`; request `reads`; `dry_run`; `source`, `rationale`, and
`group_id`; and HTTP `Idempotency-Key`. Reply scope remains accepted/merged
canonical closure with IDs, digests, commands, `id_map`, records, steps,
dependencies, effects, bindings, history, and durable receipt; dry-run
`would_status` with null receipt; conflict reason/head; and invalid code/path,
hint, and suggested command. This is a contract checklist, not a new test or
source claim.

## Prior observed result and limitation

- Recoverable result: 6 + 1 + 6 = **13 PASS**, with zero failures/errors/skips
  in the three transcript-retained XML payloads.
- Production caller was reported as `queue_proposal → flush → producer batch →
  RuntimeCommitService → inverse validation`.
- Prior static output reported Ruff, scoped mypy, vendor-lock,
  artifact-manifest, and diff checks passing.
- Exact missing scope: original XML files, lane logs, pre/post hash files,
  and final-verification file under the removed `/tmp/w-bda7eb9404` directory.
  No absent original bytes are reconstructed or relabeled.
- The prior report's seven remaining scoped core blockers are preserved as a
  prior observation only; F/R2 does not reclassify them.

