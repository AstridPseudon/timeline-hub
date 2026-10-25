# D108(2) applied-source manifest audit

The source-only worker produced a durable manifest:

`rt-F-D108-rehearsal-source-0645/evidence/d108-source-rehearsal-manifest.json`

Manifest SHA-256: `37e559e6e176f4d9b4c20db27cdf6de8b4f5ef532b5abedf35533caffb2a4504`.
The source stage reports `SOURCEONLY/PASS`; build, render, and ZIP remain
`PENDING` as required. This audit does not treat the source-stage status as
behavioural qualification.

## Applied trees and source receipts

| repo | applied commit | applied tree | patch bytes | patch SHA-256 | diff check |
|---|---|---|---:|---|---|
| Agent | `cd3f5480350d1ca68c9d8ec16aeae2863501c2a4` | `523893dcf54dbe756db8fe2915d14055b1da660b` | 12,425,282 | `348350d78ee5cea1f4736e5962990128a579e88836e0c84a9cfb8788b809da3e` | PASS |
| App | `5391d71d871c73458ef27710fc132694d57983dd` | `204a9216697953f765b5bd550aefa5822503a44c` | 9,741,492 | `e9897f363f5ee5971316d2dee9b00e68a864774a1bdd541f3e85ae8d0dd61f45` | PASS |
| Composition | `ccd3a1084a9a4adc8f391befe01828ca7f9612e8` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | 501,162 | `14f43521a1423d00fad4ac12774ed80e20ed3d5f4f0e235aec9cf5fff265aad3` | PASS |
| Runtime | `62040eeab98747dfb65abb6366236bf213109d6c` | `a522511414947e48e317a5e5c2103483b121a750` | 14,928,733 | `c93c3a1d00ddd9bb44ca51af3fdc71ab8311051846b07465d76183457f1b38b0` | PASS |

The applied staging worktrees were disposable, but the manifest is durable.
For every applied `A`/`M` source entry, the manifest `source_blob` matched the
captured tuple path blob: Agent 885/885, App 549/549, Composition 116/116,
Runtime 310/310. This makes the AST reconstruction below exact for changed
source entries; paths absent from the patch resolve to the approved fresh
upstream tree. Source and integration checkout before/after identities in the
manifest are byte-for-byte unchanged.

## Applied Python test predicate comparison

The parser compared top-level and class-member `test*` functions, whole-function
hashes, assertion-expression fingerprints, comparison operators, and
`skip`/`xfail`/`parametrize` decorator counts. It parsed source text only; no
test module was imported or executed.

| repo | upstream tests | applied tests | missing | added | changed body | removed assert fingerprints | added assert fingerprints | Eq decreases | In increases | added skip/xfail | dropped params |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Agent | 2,536 | 4,893 | 104 | 2,461 | 129 | 113 | 287 | 3 | 17 | 0 | 0 |
| Runtime | 525 | 1,494 | 10 | 979 | 113 | 72 | 205 | 5 | 3 | 0 | 0 |

No direct same-function `==`→membership pair was found. The operator deltas
are nevertheless audit signals, not clearance. No added skip/xfail or dropped
parametrization was detected in these Python scopes.

Missing top-level test predicates by source status:

* Agent: 104 total — 84 from deleted test files and 20 from modified files.
* Runtime: 10 total — all from modified files.

The missing Agent deleted-file families are `tests/core/extensions/` (model,
registry, scopes, sidecar), `tests/packs/rendering/test_timeline_inspector_viewer.py`,
and `tests/timeline/test_inverses.py`. Modified-file missing predicates include
the publish/old-writer families, rendering/effect registry, installer schema,
editing-helper, authoring-bundle, generic-host, runtime-response, and v10
creation tests. Runtime missing predicates are the ten selectors listed in
`initial-mechanical.md`.

## Fresh WelcomeConnection and installer retention

The initial captured-tuple diff showed two App deletions relative to fresh tip
`d11417a59`, but the applied manifest correctly applies the captured patch to
fresh tip `d11417a59` after the gating-base transition. Neither path appears in
the applied patch, and both therefore remain from fresh upstream:

* `src/app/onboarding/WelcomeConnection.sameOrigin.test.tsx`, fresh blob
  `52a491d8c5d483ad97ecc802fa0569b8bd0d42dd`.
* `src/app/onboarding/WelcomeJourney.integration.test.tsx`, fresh blob
  `9438787642d765e7c5a0fd6876b7a3a03b749e74`.

`src/app/onboarding/WelcomeConnection.tsx` is likewise retained from fresh
upstream (fresh blob `6563cdee28ee6a75b20b849d96e0d1b0c2fb11e4`); the applied
patch modifies `WelcomeConnection.test.tsx` with source blob
`26df345b4496372cc93d2e805976e89ccca4bb56`.

Agent installer coverage is retained and expanded: `test_installer_current.py`
and `test_installer_schema.py` are modified, `test_local_install.py` is outside
the patch and therefore fresh-upstream retained, and
`test_installer_bootstrap_schema.py` is an applied addition. The applied
manifest source blobs are recorded in its `source_upstream_blobs` list.

## Citation/weakening disposition

This independent pass gives finite mechanical counts and then applies only
exact approved decision/source entries. No changed predicate is cleared merely
because a replacement test has a similar name.

| repo | missing predicates | cited by exact approved decision + source entry | cleared | restore-needed / unresolved |
|---|---:|---:|---:|---:|
| Agent | 104 | 96 | 96 | 8 |
| Runtime | 10 | 0 | 0 | 10 |
| App | 0 in the retained WelcomeConnection paths; TS assertion census not run | 0 | 0 | TS predicate census pending |
| Composition | 2 deleted unrelated TS test paths; TS assertion census not run | 0 | 0 | TS predicate census pending |

Agent's per-file/count mapping is:

| exact original test scope | count | approved decision/source entry |
|---|---:|---|
| `tests/core/extensions/{test_model,test_registry,test_scopes,test_sidecar}.py` | 70 | D06 `deletion-ledger.agent.md:52`; Pack discovery/catalog replacements named there |
| `tests/timeline/test_inverses.py` | 9 | D05 `deletion-ledger.agent.md:51`; native inverse/ABA replacement selectors named there |
| `tests/packs/rendering/test_effect_registry_target.py` | 2 | D10 `deletion-ledger.agent.md:172`; canonical effect-registry replacement files named there |
| `tests/packs/video_editing/test_runtime_publication_chain.py` | 1 | D13/D72 `agt-F-D69-failures-render-1646.md:18`; requester-owned publication path |
| `tests/packs/timeline/{test_cli_parity,test_cli_status_publish,test_verbs_working_copy}.py` | 7 | D69/G5/D72 `agt-F-D69-failures-cli-1646.md:15`; bounded CLI port record |
| `tests/sdk/test_runtime_response_conformance.py` | 1 | D69/D72 `agt-F-D69-failures-sdk-1646.md:24`; retired response route |
| `tests/test_installer_schema.py` | 2 | D72/D77 `agt-F-D69-failures-render-1646.md:19`; local schema/installer scope |
| `tests/timeline/test_authoring_bundle.py` | 2 | D69/D72 `agt-F-D69-failures-core-1646.md:19-22`; `commit_timeline()` replacement |
| `tests/v10/test_timelines_create.py` | 1 | D69/D72 `agt-F-D69-failures-core-1646.md:24`; canonical session path |

Agent's 96 exact citations are logged in the approved deletion/failure
records: D06 `deletion-ledger.agent.md:52` for the 70 extension predicates;
D05 `:51` for the 9 inverse predicates; D10 `:172` for 2 effect-registry
predicates; D13/D72 in `agt-F-D69-failures-render-1646.md:18` for the generic
host and publication-chain predicates; D69/G5/D72 in
`agt-F-D69-failures-cli-1646.md:15` and `agent-G5-current-ready-port-1958.md`
for 7 CLI predicates; D69/D72 in `agt-F-D69-failures-sdk-1646.md:24` for the
1 retired response route; D72/D77 in the render failure record for 2 installer
predicates; and D69/D72 in `agt-F-D69-failures-core-1646.md:19-24` for the 2
authoring-bundle and 1 v10-create predicates. Each cited family has the exact
current selector/source replacement recorded there; no old writer or route is
restored.

The eight Agent restore-needed predicates are the five selectors in
`tests/packs/rendering/test_timeline_inspector_viewer.py` (viewer/vendor
deletion has no exact per-selector approved replacement in the consulted
ledgers) and the three positive retime/ripple selectors in
`tests/test_timeline_editing_helpers.py`. D07's review
(`agent-review-d07-current.md:18-29`) explicitly says those three replacements
are incomplete; they remain restore-needed, not PASS.

The ten Runtime predicates remain restore-needed because the prior Runtime D69
map was for current source hash `8b32cacea617c6d45241d7db90b34893a06d3026`,
not D108 Runtime `1daca2a33…`; no exact current selector/source map was reused.
The exact selectors are:

* `tests/test_canonical_render_admission.py::test_canonical_stale_head_rejected_when_legacy_version_is_unchanged`;
* `tests/test_runtime_domains.py::test_generated_domains_preserve_project_media_and_timeline_recovery`;
  `::test_project_media_mutations_roll_back_before_idempotency_replay`;
* `tests/test_runtime_e2e.py::test_project_shot_reference_crud_isolated_idempotent_and_restart_durable`;
* `tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`;
* `tests/test_runtime_p1_blockers.py::test_project_updates_require_idempotency_keys_at_service_boundary`;
* `tests/test_shot_composition_contract.py::test_materialized_canonical_timeline_schema_is_the_nested_runtime_contract`;
  `::test_materialized_timeline_schema_provenance_tracks_role_extension_and_nested_hashes`;
  `::test_schema_declares_two_owner_boundary_without_a_second_timeline_schema`;
* `tests/test_spec_reference.py::test_working_copy_uses_cas_and_requires_its_saved_base_at_claim`.

The initial tuple-only census also surfaced two nested/non-top-level names
(`test_project_media_mutations_roll_back_before_idempotency_replay.fail` and
`test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart.prepare_then_crash`);
they are not counted as applied top-level/class-member predicates.
D107 legacy-ten coverage remains a gap unless its current equivalent is
independently present; it is not fabricated as PASS. No added skip/xfail or
parameter weakening was found in either Python AST census.

## Verdict

Applied trees are present and source identity is verified. The source-stage
audit is **FAIL**: 8 Agent predicates require approved restoration/mapping and
10 Runtime predicates remain unmapped under the exact-hash rule. App
WelcomeConnection retention and Agent installer retention pass the requested
source-presence checks. Build/render/ZIP remain pending in the source-applier
manifest. No test, build, render, ZIP, import, or provider command was run.
