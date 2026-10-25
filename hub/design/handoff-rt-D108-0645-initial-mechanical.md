# D108(2) initial mechanical source collection

Status: `AUDIT-PENDING` for applied rehearsal trees. This file records read-only
facts from the exact D108 tuple and approved upstream tips. No tests, imports,
providers, builders, renders, or package commands were run.

## Exact source identities

| repo | captured commit | captured tree | approved upstream tip | upstream tree |
|---|---|---|---|---|
| Agent | `d6294843286c18e57af3c1874cf1996be42212d2` | `6aeae30f0892a424104a4348bca6fd74ba1315d6` | `08e6b905114a3ee2b05c3e7980421f26b4abf15c` | `2694ae8d2709526b40fa037bda8b159cf412769d` |
| Runtime | `1daca2a33f6d7b10053e07c539a54843e3984e19` | `a522511414947e48e317a5e5c2103483b121a750` | `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad` | `1d3e06f4d59ed6d459646d24ab185c36eb5be075` |
| App | `0b6cee269f32079c5446036bbca8a484176799bc` | `9456c9edf3229ddcfd824b0f626516f2c602ccfa` | `d11417a59b5edbb617e0311212b79069620538a7` | `e9079c61a1789b4a58cf1575b7ed8cbe63919dbb` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` |

The captured commits and upstream tips resolve in their existing source clones.
No fetch or ref mutation was attempted. The live `/home/user/work/runtime`
and `/home/user/work/app` integration worktrees were not used as source input:
their HEADs were `c91626f5e905f9336b51aae0486a071d83f0bac7` and
`51239c79e26ff743623218b9c09fdce1629ec90c`, respectively, rather than the
specified tuple commits.

## Captured tuple versus approved upstream: file-level delta

Counts are `git diff --name-status upstream captured`. `testlike` is a
mechanical path heuristic (tests, e2e, `__tests__`, or `.test/.spec` files),
not a claim that each file is a behavioural predicate.

| repo | all files A/M/D | testlike files A/M/D |
|---|---:|---:|
| Agent | 524 / 363 / 32 | 391 / 169 / 7 |
| Runtime | 207 / 103 / 1 | 157 / 51 / 0 |
| App | 324 / 254 / 19 | 197 / 82 / 4 |
| Composition | 93 / 23 / 2 | 17 / 1 / 2 |

The corresponding total file counts are Agent 919, Runtime 311, App 597, and
Composition 118. These are source deltas, not applied-tree qualification.

## Python test AST comparison

This is parser-only comparison of Python test-like files changed by the tuple
diff. Qualified function names and whole-function source hashes were compared;
no Python module was imported or executed.

| repo | changed Python test files | upstream funcs | captured funcs | missing | added | changed body | removed assert fingerprints | added assert fingerprints |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Agent | 453 | 3,884 | 7,230 | 153 | 3,499 | 166 | 113 | 289 |
| Runtime | 172 | 757 | 2,206 | 12 | 1,461 | 127 | 72 | 205 |

No added `skip`/`xfail` decorators or dropped `parametrize` decorators were
found by this AST pass in either Agent or Runtime. Equality-operation decreases
and membership-operation increases were not paired in one common function:
Agent `Eq -3`, `In +17`; Runtime `Eq -5`, `In +3`. This does not by itself
clear any changed predicate; exact selector/assertion mapping awaits the
applied-source manifest and approved citations.

Runtime missing upstream qualified functions (all 12):

* `tests/test_canonical_render_admission.py:test_canonical_stale_head_rejected_when_legacy_version_is_unchanged`
* `tests/test_runtime_domains.py:test_generated_domains_preserve_project_media_and_timeline_recovery`
* `tests/test_runtime_domains.py:test_project_media_mutations_roll_back_before_idempotency_replay`
* `tests/test_runtime_domains.py:test_project_media_mutations_roll_back_before_idempotency_replay.fail`
* `tests/test_runtime_e2e.py:test_project_shot_reference_crud_isolated_idempotent_and_restart_durable`
* `tests/test_runtime_exact_idempotency.py:test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`
* `tests/test_runtime_p1_blockers.py:test_project_updates_require_idempotency_keys_at_service_boundary`
* `tests/test_shot_composition_contract.py:test_materialized_canonical_timeline_schema_is_the_nested_runtime_contract`
* `tests/test_shot_composition_contract.py:test_materialized_timeline_schema_provenance_tracks_role_extension_and_nested_hashes`
* `tests/test_shot_composition_contract.py:test_schema_declares_two_owner_boundary_without_a_second_timeline_schema`
* `tests/test_spec_reference.py:test_working_copy_uses_cas_and_requires_its_saved_base_at_claim`
* `tests/test_timeline_render_publication.py:test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart.prepare_then_crash`

The prior Runtime D69 audit used current `8b32cacea617c6d45241d7db90b34893a06d3026`
and upstream `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`; those source hashes do
not equal this D108 captured Runtime commit, so its per-predicate map is not
reused as qualification evidence.

## Explicit retained/deleted checks

App WelcomeConnection:

* `src/app/onboarding/WelcomeConnection.tsx`: modified, upstream blob
  `6563cdee28ee6a75b20b849d96e0d1b0c2fb11e4`, captured blob
  `6b38667fc32632ff64c00d250c97467544808624`.
* `src/app/onboarding/WelcomeConnection.test.tsx`: modified, upstream blob
  `13de70b05d0ad287b83205ded4be91e962294b8b`, captured blob
  `26df345b4496372cc93d2e805976e89ccca4bb56`.
* `src/app/onboarding/WelcomeConnection.sameOrigin.test.tsx`: **deleted**;
  upstream blob `52a491d8c5d483ad97ecc802fa0569b8bd0d42dd`.
* `src/app/onboarding/WelcomeJourney.integration.test.tsx`: **deleted**;
  upstream blob `9438787642d765e7c5a0fd6876b7a3a03b749e74`.

Agent installer checks:

* `tests/test_installer_schema.py`: modified, blobs
  `ede759060078ab18a9eac75fd682ddb429073518` ->
  `00ba669033726fc84b305144acd2c9c40eb314df`.
* `tests/test_installer_current.py`: modified, blobs
  `7aee55852294666b7f47057052432eda1763f77c` ->
  `ca258322f6b7992288d52071ab2525f698ffe54a`.
* `tests/test_local_install.py`: unchanged, blob
  `49fdc3f50a515b50687211fa44b85e4d0affb936`.
* New captured installer-adjacent tests are present:
  `tests/test_installer_bootstrap_schema.py`,
  `tests/core/rendering/test_installed_registry_security.py`, and
  `tests/sdk/test_installed_runtime_source_identity.py`.

The two deleted App WelcomeConnection suites are an unresolved source finding
at this stage. No approved D105a text authorizes deleting them; D105a instead
requires preserving the product's upstream DOM identity and adapting only the
two owned placement selectors. Final disposition is withheld until the actual
applied-source manifest maps each original predicate.

## Applied-source handoff state (historical initial capture)

At initial collection time the source-applier evidence directory contained only:

* `agent.base-to-capture.patch` (12,425,282 bytes).

No four-repo applied tree, applied commit/tree IDs, applied diff hashes, source
blob receipts, unchanged-upstream-test receipts, or per-assertion manifest was
available at that point. The later durable manifest and final classification
are recorded in `applied-manifest-audit.md`; this historical handoff section
must not be read as the final verdict.
