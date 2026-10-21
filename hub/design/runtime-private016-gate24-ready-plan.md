# Runtime PRIVATE016 Gate2/Gate4 ready plan

Date: 2026-10-21 UTC

This is a bounded, source-only execution plan. No command below was executed
by this worker. The native/HTTP/RT03 bodies remain held until the reciprocal
artifact review is complete and a normal private016 Agent pin is supplied.

## Immutable Runtime candidate

The plan is bound to the corrected Runtime join, not to a historical Agent
consumer or to private015:

| field | required value |
| --- | --- |
| Runtime commit | `da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406` |
| Runtime tree | `486fe045f66182b33520bea971d31add3f713ea9` |
| b92 base | `b92d3e7a05eec65c142294ef4873edd059e9b31d` / tree `6abc2f117391de8e7e35c0283f575a002199894d` |
| Runtime version | `0.2.16` |
| Runtime schema/health digest | `sha256:97724260188a1b07c06520d2233bf3cbae52370185b0c0b6e4c9f0bf2accdfdd` |
| component manifest | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| raw Runtime bundle | `sha256:1bbc786daab05597f7a4d910ef0f8dcda531912b2d1e37318a35544ef039d7e9` |
| artifact manifest/version | `sha256:b045b4ecc9bfc026de12b64defa31b064b1187c3638554a129403e6a6356e7d5` |
| Agent command source | commit `10226a7f08a739ba3e41f8e91de6971eed63aa9d`, tree `e2c08fbe9b21a3082db7bcf62d9677babfc15e98` |
| Agent raw/canonical schema | `sha256:9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec` / `sha256:322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc` |
| schema inventory | 65 definitions / 37 closed clauses |

The Agent source row is provenance for the reviewed schema only. It is not a
normal pin and must not be placed in `ASTRID_CHECKOUT` for proof execution.
The future Agent pin must be a separate, clean checkout whose exact commit and
tree are recorded at run time.

## What changed and what needs proof

The private016 join changes the Runtime materialization join and inherited
allocation checks, raw-media capture, reference projection, transcript/source
input handling, and generated Python/TypeScript contract surfaces. The joined
Runtime test preparation already contains the following existing source tests:

- `tests/test_timeline_raw_capture.py` — owned raw declaration,
  descriptor recheck/no-write refusal, and ledger-first retry.
- `tests/test_timeline_unplaced_reference_projection.py` — accepted
  parent-owned reference projection, occupied/invalid custody refusal,
  removal/restoration, and retry.
- `tests/test_timeline_owned_reference_integration.py` — the prepared RT03
  Agent-provider original-preservation proof; it is collected under the
  existing `integration` marker and is intentionally separate from the
  Agent manager's matched native lifecycle pair.

The existing Gate2/Gate4 suites in `ORCH/tests/suites.conf` remain the source
of truth for the ordinary proof. No new suite or fixture is needed for this
plan, and `suites.conf` must not be changed merely to run these selectors.

## Evidence that is reused, with its boundary

The current Runtime full evidence is **6002 passed, 26 skipped, 15 xfailed,
12 warnings, exit 0** on Runtime tree `6abc2f117391de8e7e35c0283f575a002199894d`.
The current generated-client evidence is **61 TypeScript tests passed, 0
failed, exit 0** for the published 0.2.14/current tree. Neither result is
repeated here.

Those results remain valid evidence for unchanged ordinary paths only. They
do not qualify private016 materialization/raw/reference/transcript behavior.
In particular, the current TypeScript package and lock are changed by
private016, so its 61-test result cannot be relabeled as a private016 result;
the future private016 run below is required for Gate4 client evidence. This is
the only intentional new client run, and it is not a repeat of an unchanged
source tree.

## Preconditions before any body runs

The orchestrator must first record all of the following. The first four are
known; the Agent identity fields are deliberately missing until the normal
pin exists:

```text
RUNTIME_COMMIT=da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406
RUNTIME_TREE=486fe045f66182b33520bea971d31add3f713ea9
RUNTIME_SCHEMA_DIGEST=sha256:97724260188a1b07c06520d2233bf3cbae52370185b0c0b6e4c9f0bf2accdfdd
RUNTIME_ARTIFACT_VERSION=sha256:b045b4ecc9bfc026de12b64defa31b064b1187c3638554a129403e6a6356e7d5
AGENT_PIN_ROOT=<missing: future clean normal private016 Agent checkout>
AGENT_PIN_COMMIT=<missing: future normal Agent commit, not 10226/C3d>
AGENT_PIN_TREE=<missing: future normal Agent tree>
AGENT_PIN_SCHEMA_DIGEST=sha256:97724260188a1b07c06520d2233bf3cbae52370185b0c0b6e4c9f0bf2accdfdd
AGENT_PIN_CONTRACT_VERSION=0.2.16
AGENT_PIN_RUNTIME_SOURCE_COMMIT=da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406
AGENT_PIN_RUNTIME_PRODUCER_VERSION=sha256:b045b4ecc9bfc026de12b64defa31b064b1187c3638554a129403e6a6356e7d5
```

The Agent pin's `runtime.lock.json`, generated Python metadata, and generated
TypeScript metadata must resolve to those last four private016 values. The
future Agent commit/tree, clean status, and actual pin result ID are not
available now; they are a hard precondition, not values to infer from the
reviewed 10226 source.

Before requesting a central run, perform this read-only preflight in the
Runtime snapshot. It verifies the exact Runtime identity, the future pin
identity, metadata, required files, existing markers/imports, and the
private016 schema/artifact values. It intentionally does not import the Agent
provider or execute a test body:

```sh
set -eu
: "${AGENT_PIN_ROOT:?set to the actual future normal private016 Agent checkout}"
: "${AGENT_PIN_COMMIT:?set the actual future Agent commit}"
: "${AGENT_PIN_TREE:?set the actual future Agent tree}"
test "$(git rev-parse HEAD)" = da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406
test "$(git rev-parse HEAD^{tree})" = 486fe045f66182b33520bea971d31add3f713ea9
test "$(git -C "$AGENT_PIN_ROOT" rev-parse HEAD)" = "$AGENT_PIN_COMMIT"
test "$(git -C "$AGENT_PIN_ROOT" rev-parse HEAD^{tree})" = "$AGENT_PIN_TREE"
test -z "$(git -C "$AGENT_PIN_ROOT" status --porcelain)"
test -f runtime_protocol/timeline_materialization.py
test -f runtime_protocol/timeline_commit_reference_projection.py
test -f tests/test_timeline_raw_capture.py
test -f tests/test_timeline_unplaced_reference_projection.py
test -f tests/test_timeline_owned_reference_integration.py
rg -q '^pytestmark = pytest\.mark\.integration$' tests/test_timeline_owned_reference_integration.py
rg -q 'from test_timeline_commit_integration import agent' tests/test_timeline_owned_reference_integration.py
rg -q 'native_parent_reference_commands import capture_timeline_reference' tests/test_timeline_owned_reference_integration.py
PYTHONPATH="$PWD:$AGENT_PIN_ROOT" /home/user/work/venv-runtime/bin/python - "$AGENT_PIN_ROOT" <<'PY'
import json, pathlib, sys
root = pathlib.Path.cwd()
agent = pathlib.Path(sys.argv[1])
from astrid_runtime_client import contract_metadata
assert contract_metadata.CONTRACT_VERSION == "0.2.16"
assert contract_metadata.SCHEMA_DIGEST == "sha256:97724260188a1b07c06520d2233bf3cbae52370185b0c0b6e4c9f0bf2accdfdd"
assert contract_metadata.COMPONENT_MANIFEST_SHA256 == "sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5"
lock = json.loads((agent / "runtime.lock.json").read_text())
assert lock["source_commit"] == "da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406"
assert lock["producer_version"] == "sha256:b045b4ecc9bfc026de12b64defa31b064b1187c3638554a129403e6a6356e7d5"
manifest = json.loads((root / "contract/artifacts.json").read_text())
assert manifest["version"] == "sha256:b045b4ecc9bfc026de12b64defa31b064b1187c3638554a129403e6a6356e7d5"
assert len(manifest["artifacts"]) == 76
PY
```

The `PYTHONPATH` order is deliberate: Runtime protocol first, then the actual
Agent pin. A missing or mismatched value stops the run; no fallback checkout
or historical C3d client is permitted.

## Gate2: minimal changed-source proof

Run only after the preconditions and reciprocal artifact review. This is the
Runtime atomicity cohort; it does not repeat the ordinary 51-case lifecycle
suite and does not claim the Agent manager's native pair. The selected nodes
are existing tests and are grouped by the private016 source they exercise:

```sh
env ASTRID_RUNTIME_CHECKOUT=$PWD \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="$PWD:$AGENT_PIN_ROOT" \
    /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
    tests/test_timeline_commit_execution.py::test_commit_duplicate_move_winner_between_lookup_and_execution \
    tests/test_timeline_commit_execution.py::test_commit_duplicate_add_winner_between_lookup_and_execution \
    tests/test_timeline_commit_execution.py::test_equal_waiters_share_entry_and_never_hold_store_mutex \
    tests/test_timeline_commit_execution.py::test_all_provider_completions_reconcile_a_durable_winner \
    tests/test_timeline_commit_execution.py::test_active_hash_mismatch_does_no_provider_work \
    tests/test_timeline_commit_execution.py::test_claimed_acceptance_without_ledger_is_protocol_failure \
    tests/test_timeline_commit_execution.py::test_readback_failure_is_unknown_outcome \
    tests/test_timeline_commit_execution.py::test_authority_is_rechecked_before_disclosing_acceptance \
    tests/test_timeline_commit_execution.py::test_concurrent_different_keys_cas_one_winner \
    tests/test_timeline_commit_execution.py::test_durable_original_wins_while_changed_hash_is_active_before_lookup \
    tests/test_timeline_commit_execution.py::test_corrupt_durable_recorder_never_reruns_provider_even_after_restart \
    tests/test_timeline_commit_acceptance.py::test_atomic_acceptance_exact_recorder_projection_and_same_content_edge \
    tests/test_timeline_commit_acceptance.py::test_identical_retry_after_restart_and_head_advance \
    tests/test_timeline_commit_acceptance.py::test_changed_payload_and_publication_only_cas_refuse_without_writes \
    tests/test_timeline_commit_acceptance.py::test_failure_after_receipt_rolls_back_every_row \
    tests/test_timeline_commit_acceptance.py::test_failure_between_projection_steps_rolls_back_and_restart_retry_publishes_once \
    tests/test_timeline_commit_acceptance.py::test_complete_recorder_roundtrip_and_replay_after_restart \
    tests/test_timeline_commit_acceptance.py::test_real_acceptance_links_consumed_inputs_and_keeps_old_bytes_after_restart \
    tests/test_timeline_commit_acceptance.py::test_live_capture_accept_race_rolls_back_history_receipt_and_input_links \
    tests/test_timeline_commit_acceptance.py::test_complete_detached_child_closure_projects_and_reuses_exact_rows \
    tests/test_timeline_commit_inputs.py::test_transcript_v1_is_retained_after_v2_and_database_reopen \
    tests/test_timeline_commit_inputs.py::test_rejected_batch_rolls_back_all_content_bindings_and_links \
    tests/test_timeline_commit_inputs.py::test_foreign_guessed_and_revoked_source_pins_are_denied \
    tests/test_timeline_commit_inputs.py::test_retained_lookup_requires_reachability_and_rejects_missing_or_corrupt_bytes \
    tests/test_timeline_commit_inputs.py::test_retained_capture_does_not_heal_missing_or_corrupt_content \
    tests/test_timeline_commit_inputs.py::test_stored_source_header_mismatch_is_refused_at_accept \
    tests/test_timeline_commit_inputs.py::test_first_use_capture_rechecks_exact_header \
    tests/test_timeline_raw_capture.py::test_owned_raw_capture_from_empty_parent_is_unplaced_and_exact \
    tests/test_timeline_raw_capture.py::test_raw_capture_refuses_missing_unowned_or_foreign_object_without_writes \
    tests/test_timeline_raw_capture.py::test_raw_capture_rechecks_same_descriptor_before_writes \
    tests/test_timeline_raw_capture.py::test_exact_retry_after_restart_replays_ledger_before_raw_capture \
    tests/test_timeline_unplaced_reference_projection.py::test_owned_unplaced_reference_projects_row_and_snapshot_and_preserves_unrelated \
    tests/test_timeline_unplaced_reference_projection.py::test_occupied_or_invalid_custody_refuses_before_any_write \
    tests/test_timeline_unplaced_reference_projection.py::test_inverse_shaped_removal_and_restoration_are_exactly_projected \
    tests/test_timeline_unplaced_reference_projection.py::test_ledger_first_retry_after_restart_does_not_reexecute_projection_provider
```

Why these selectors are required:

| selector | changed-source reason |
| --- | --- |
| the 11 named `test_timeline_commit_execution.py` nodes | exercises durable winner selection, concurrent keys, CAS, and no-provider-rerun behavior in the changed commit store |
| acceptance atomicity/retry/rollback nodes | materialization and reference projection now participate in accepted-row, receipt, restart, and rollback verification |
| `test_real_acceptance_links_consumed_inputs_and_keeps_old_bytes_after_restart` | verifies source/input materialization closure and retained immutable bytes |
| `test_live_capture_accept_race_rolls_back_history_receipt_and_input_links` | verifies an input race cannot leave partial links/history |
| `test_complete_detached_child_closure_projects_and_reuses_exact_rows` | verifies the materialization join and exact child allocation reuse |
| seven named `test_timeline_commit_inputs.py` nodes | verifies transcript retention, source reachability, immutable bytes, and atomic input rechecks |
| four named raw-capture nodes | verifies owned raw admission, descriptor recheck, no-write refusal, and ledger-first retry |
| four named unplaced-projection nodes | verifies reference identity occupancy, source role/digest, projection closure, removal/restoration, and retry atomicity |

The named raw-capture and unplaced-projection nodes are existing Runtime tests
from the private016 candidate; they are not new fixtures. They use trusted
fixture providers and are not a substitute for RT03's actual Agent provider
proof.

## RT03 original-preservation proof (separate lane)

Run the prepared node separately from the Agent lifecycle suite, with the
same future normal pin and the same Runtime candidate. Do not combine it with
the ordinary 51-case Gate2 command and do not use `10226a7f`, C3d, or a
historical Agent checkout:

```sh
env ASTRID_RUNTIME_CHECKOUT=$PWD \
    ASTRID_CHECKOUT="$AGENT_PIN_ROOT" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="$PWD:$AGENT_PIN_ROOT" \
    /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
    tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract
```

This is the Runtime-owned original-preservation witness: actual Agent
`timeline.reference`, real raw custody descriptors, normal commit acceptance,
zero placement/shot/occurrence writes, exact reference identity/role/digest,
and exact retry/readback. The Agent manager's one matched native lifecycle
pair remains its own proof and is not duplicated here.

## Gate4: minimal changed admission/transport proof

Use the existing Gate4 door selectors for route, origin, credentials,
project-scope, response-lock, and generated-client admission, plus the
changed transcript/reference/raw admission neighbors:

```sh
env ASTRID_RUNTIME_CHECKOUT=$PWD \
    ASTRID_CHECKOUT="$AGENT_PIN_ROOT" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="$PWD:$AGENT_PIN_ROOT" \
    /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
    tests/test_timeline_commit_routes.py::test_commit_route_passes_exact_service_shape_and_rechecks_authority \
    tests/test_timeline_commit_routes.py::test_commit_route_leaves_semantic_schema_validation_to_service \
    tests/test_timeline_commit_routes.py::test_commit_route_rejects_path_mismatch_before_service \
    tests/test_timeline_commit_routes.py::test_commit_route_rejects_duplicate_fields_and_nonfinite_overflow \
    tests/test_timeline_commit_routes.py::test_commit_route_preserves_opaque_json_and_encoded_identity \
    tests/test_timeline_commit_routes.py::test_new_door_routes_are_exact \
    tests/test_http_response_lock.py::test_stalled_response_does_not_block_other_database_route \
    tests/test_http_response_lock.py::test_abandoned_response_does_not_attempt_second_response \
    tests/test_http_response_lock.py::test_slow_request_body_is_read_before_the_shared_database_lock \
    tests/test_door_transport.py::test_admission_order_host_origin_and_route \
    tests/test_door_transport.py::test_browser_credentials_are_refused \
    tests/test_door_transport.py::test_preflight_allows_listed_request \
    tests/test_door_transport.py::test_preflight_refusals \
    tests/test_timeline_commit_integration.py::test_real_door_commit_admission_checks_origin_auth_and_project_scope \
    tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider \
    tests/test_timeline_commit_acceptance.py::test_real_provider_two_projects_keep_local_ids_and_commit_authority_isolated \
    tests/test_timeline_reference_authority.py::test_http_timeline_reference_writers_refuse_without_writes \
    tests/test_timeline_source_document_boundary.py::test_http_transcript_source_reads_retained_v1_without_pack_object \
    tests/test_timeline_commit_inputs.py::test_transcript_v1_is_retained_after_v2_and_database_reopen \
    tests/test_generated_client.py::test_generated_client_smoke_and_scoped_handshake \
    tests/test_generated_client.py::test_acquisition_selected_python_renderer_parity \
    tests/test_client_parity.py::test_product_clients_match_canonical_contract_projection \
    tests/test_client_parity.py::test_recoverable_snapshot_client_projection_is_canonical
```

The four door selectors and response-lock/route files are existing Gate4
coverage. The reference, transcript, and generated-client selectors are the
minimal admission neighbors made relevant by this private016 source and
artifact delta. The raw positive is deliberately covered by the separate RT03
lane; its direct refusal/recheck behavior is in the Gate2 raw module.

The generated TypeScript client must then be run once against the private016
package already present in the Runtime snapshot, without installing or
mutating shared dependencies:

```sh
cd packages/typescript
PATH=/home/user/work/app/node_modules/typescript/bin:$PATH npm test
```

Record the exact test count and exit status. The old current 0.2.14 result of
61 passed remains a baseline only; it must not be reported as this command's
private016 result.

## Collection and zero-test guard

Every future command above must be preceded by `--collect-only -q` over the
same argv, and the runner must fail if collection is nonzero-exit, reports
`0 tests collected`, or the real run does not report at least one passed test.
For the central service, use a private log outside the worktree and enforce
the guard as follows; this is a guard, not a new test framework:

```sh
run_bounded() {
    log="$(mktemp /tmp/runtime-private016-gate24.XXXXXX.log)"
    set +e
    "$PYTHON" -m pytest -q -p no:cacheprovider --collect-only "$@" >"$log" 2>&1
    status=$?
    set -e
    test "$status" -eq 0
    grep -Eq '[1-9][0-9]* tests? collected' "$log"
    set +e
    "$PYTHON" -m pytest -q -p no:cacheprovider "$@" 2>&1 | tee "$log"
    status=${PIPESTATUS[0]}
    set -e
    test "$status" -eq 0
    grep -Eq '[1-9][0-9]* passed' "$log"
    ! grep -Eq '0 tests? collected|0 passed' "$log"
}
```

The central test service snapshots the worktree and supplies its own command
environment; it must apply the same guard and report the selected collection
count. No `-k` broad expression, blanket deselection, skip, xfail, assertion
rewrite, or historical fallback is allowed.

## Not run / not claimed

- No native, HTTP, RT03, renderer, browser, install, generation, pin,
  publication, adoption, or full-suite execution was performed for this
  preflight.
- The ordinary Runtime full6002 and current TypeScript61 results were not
  repeated and are not private016 Gate2/Gate4 passes.
- No normal Agent pin identity exists yet. The exact missing values are the
  future Agent commit, tree, clean status, actual pin/result identity, and
  the matching lock/metadata verification above.
- No test-support gap requires source changes. The prepared RT03 node,
  existing raw/reference modules, existing transcript/input nodes, and the
  existing Gate2/Gate4 selectors are sufficient; only the future normal pin
  and reciprocal review are missing.
