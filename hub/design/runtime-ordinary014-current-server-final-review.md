# Runtime ordinary014 current-server final review

## Verdict: REJECT pending one exact test carry-forward

Review target: immutable Runtime commit `9cde47523803607f4dfd8d39885a9526de4ce8e7`,
tree `ea1ffe7e09ebf679abf409b060e753c17bdabe0d`, with parents
official producer `a0dca16975dfe8f5e762703b99d9791a16cf7fd7` (tree
`4b7dd0fe44be973c344bab3de568eaf0bdd28476`) and current-server parent
`9f211fcdb66023a577a14111f99c87fb32ef573c`. This is an unpublished review
candidate only; no pin, merge, publication, or activation is approved.

The official contract/artifact identity is correct:

- frozen Agent source: `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`;
  raw schema `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
- Runtime wire schema: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`;
- unpublished package: `0.2.14`;
- artifact version: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`;
  manifest SHA-256 `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`;
- 75 artifact paths, 55 schema definitions, 29 command operations, and 133
  unique HTTP operations.

Independent immutable-tree checks found zero artifact manifest/hash failures;
all 75 artifact bytes match official `a0dca169`. The final-vs-current diff is
exactly the 20 official generated/contract paths, and those bytes match `a0`;
the current CAS, promotion/text, catalog-fence, clip-replacement, audit, and
shell files match `9f211fc`. No private carrier, v2 surface, source factory,
producer/audio tuple, new endpoint, or public-013 mutation was found. The
current integration release remains `0.2.13` at `6ab3243`.

## Blocking finding

The current integration commit `6ab3243972f8dc49105819e6d7ba7aef1a2888b8`
contains the required clip-parity strengthening introduced by
`1f75756cfe2f391397e6e3282a81c6e50c3eb567`:

`tests/test_timeline_clip_replacement.py::test_native_clip_swap_rebases_after_disjoint_intervening_edit`

That exact test is absent from both current-server parent `9f211fc` and
candidate `9cde475`. Its assertions cover the disjoint intervening edit,
`status == "rebased"`, exact `rebased_onto` revision/publication identity,
exact replacement, and preservation of the intervening parent hold. This is a
required current-6ab test carry-forward, not an optional duplicate.

Reject adoption until that exact test-strengthening is carried forward into the
candidate and the relevant targeted/central socket lane is rerun. The
candidate can be re-reviewed as APPROVE (still unpublished) if the final tree
retains the exact official `a0` contract/artifact cohort, the `9f` current
server behavior, and this test with green evidence. Any artifact/source/producer
mismatch, private carrier, public-013 change, or consumer pin before
that requalification remains a rejection condition.

## Evidence

Worker/central evidence on the exact candidate snapshot:

- `/home/user/work/venv-runtime/bin/python generators/generate.py --check`:
  passed;
- `node tools/generate_typescript_conformance.mjs --contract
  contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json
  --component-manifest contract/component-manifest.json --check --source-root
  "$PWD" --fixture-root "$PWD/conformance/fixtures"`: passed;
- `/home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py
  --check`: passed;
- `/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p
  no:cacheprovider tests/test_timeline_current_union_contract.py
  tests/test_artifact_manifest.py tests/test_client_release.py
  tests/test_command_schema_compatibility.py tests/test_contract_fixtures.py
  tests/test_schema_validation.py tests/test_spec_dedup.py
  tests/test_timeline_bundle2_contract.py tests/test_timeline_commit_contract.py
  tests/test_timeline_commit_type_generator.py`: **300 passed**;
- central `request-test rt-m2-ordinary014-current-server-compose targeted
  --files "tests/test_door_transport.py tests/test_shot_text_bindings.py
  tests/test_shot_candidate_promotion.py::test_candidate_promotion_is_atomic_fixed_point_and_byte_stable_on_replay
  tests/test_shot_candidate_promotion.py::test_candidate_provenance_is_verified_before_promotion
  tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route
  tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_public_http_route
  tests/test_timeline_shot_authority.py::test_authenticated_http_shot_writes_are_retired
  tests/test_timeline_shot_authority.py::test_http_auth_and_scope_checks_precede_retirement
  tests/test_timeline_shot_authority.py::test_http_foreign_project_never_mutates_shot
  tests/test_timeline_shot_authority.py::test_http_text_binding_auth_and_film_scope_checks_precede_writes"`:
  **77 passed, 1 deselected, 1 existing strict xfail** (retired direct clip
  route);
- central `request-test rt-m2-ordinary014-current-server-compose
  commit-integration --files "tests/test_timeline_commit_integration.py"`:
  **9 passed**.

No full suite was run. Consumer-native qualification was not claimed. No
product files were changed by this review.
