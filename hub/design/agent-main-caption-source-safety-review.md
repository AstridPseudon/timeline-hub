# Agent Main caption source-safety review

## Disposition

**FINDING — not approved.** The exact generated-only witness path is source-safe for the witness payload, but the implementation has an ownership-injection hole when a generated refresh also supplies `app.managedBy`.

## Scope and exact sources

- Plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`.
- App2 witness: `ap2-m2-fresh-caption-main-joint-case-handoff-0447.json` and `.md`.
  - Exact Main source identity: commit `860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`.
  - Builder/compiler references: `extension.ts:288-476,754-774`; `timeline-patch.ts:1012-1029,1098-1183,1207-1316,1936-1978`; Runtime projection `dataProvider.ts:1072-1098,1131-1144`.
  - Witness row: `transcript-caption-ca055bff87805488`, `at=1`, `hold=1`, geometry `x=128,y=418,width=1024,height=101`, text `Zażółć 🌍`, generated extension `haus.astrid.transcript-lane`, contribution `transcript-caption-foundry`, schema `astrid.transcript_segment/v1`, generator `1.3.0`, policy `preserve-output`, and no `managedBy`.
- Agent implementation: `astrid/sdk/timeline/_clip_scalar_commands.py:21-99,207-210`.
- Command schema: `astrid/core/timeline/schema/edit-command.schema.json:2576-2633`. The `app` values schema allows a non-empty `managedBy` alongside `__generated__`; therefore this is an executable source-contract case, not an invalid-schema-only payload.

## What passed

The witness-shaped generated-only birth/refresh path passed the focused regression and an independent read-only probe:

- Existing carrier is required and malformed/no-carrier, user, foreign-owner, empty identity, and identity-adoption controls refuse with `unsupported_ownership`.
- Captured refresh reads include the full original clip basis, `app` with `managedBy` absent, and the exact prior `app.__generated__` carrier; the expectation guard contains the prior generated carrier.
- Witness geometry and timing remain exact (`at=1`, `hold=1`, `x=128`, `y=418`, `width=1024`, `height=101`); `managedBy` remains absent.
- Exact inverse and deep-JSON reload/re-execution both equal the expected bundle.
- The successful generated-only refresh preserves the opaque sibling and both parent/config clip rows.

## Concrete finding

For a persisted witness-shaped row with `app.__generated__` established and `managedBy` absent, a refresh with:

```json
{
  "app": {
    "managedBy": "evil.owner",
    "__generated__": "same established extension/contribution and valid refreshed provenance"
  }
}
```

is accepted and writes `managedBy: "evil.owner"` to the row. The cause is:

1. `_producer_app` falls back to the established extension when current `managedBy` is absent (`_clip_scalar_commands.py:83-90`) but never rejects an incoming `managedBy` in that branch.
2. `clip_set` then writes every incoming app leaf (`_clip_scalar_commands.py:207-210`).

The same path accepts a non-empty owner equal to the generated extension, which also synthesizes an owner. An empty-string incoming owner is rejected by the schema's `minLength`, but that does not cover the non-empty foreign-owner case.

This violates the witness contract that `managedBy` is absent in both operations and remains absent, and the requested no-owner-synthesis / foreign-owner exclusion boundary. The fix should be made in source before approval: when the persisted row has no `managedBy`, any incoming `managedBy` must refuse atomically (including a matching owner); the generated-only witness payload must continue to work without materializing the field.

## Verification

```text
PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_producer_clip_set.py -k 'main_complete_birth_and_generated_only_refresh or generated_refresh_refuses_without_established_exact_carrier or producer_metadata_refuses_user_foreign_and_identity_adoption_without_writes or main_shaped_producer_capture_preserves_opaque_siblings_and_roundtrips'
4 passed, 1 deselected
```

Independent read-only Python probe: witness-shaped birth, generated-only refresh, read/expect inspection, geometry/timing, inverse, reload, and incoming foreign-owner control. Result: witness path exact; incoming `managedBy='evil.owner'` **accepted** and persisted.

No source, schema, generated, native, public activation, or test files were changed. No full suite, `not196/34` replay, browser, HTTP, or live persistence run was performed.
