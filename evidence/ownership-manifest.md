# D115 effect83 read-only ownership evidence

Disposition: CONFIRMED minimal Runtime seam; no product or test edits.

## Inputs and source bindings

- Runtime base: `tl/integration` and worker HEAD `d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e`.
- Agent current integration: `547e10456250c1b5bcf63b44a50c90ff0563ce1e`.
- Agent retained regression branch: `f6d5d518368b3e4730f742e9f1993e426b10bbaa`.
- Agent provider blobs are identical on current integration and retained regression branch:
  - `astrid/sdk/timeline/commit.py`: blob `0ab8cb16761c9ce6a971fae3e8600f35f391760e`.
  - `astrid/sdk/timeline/_commit_preview.py`: blob `daeed358b72e852abe9ee4bad367dc454bd91ba1`.
- Retained regression test blob:
  - `tests/sdk/test_effect_image_prepared_candidate_runtime.py`: blob `d47e04780ce310432bbd72c53fad7b95ea45cf8f`.
- Runtime source SHA-256 bindings:
  - `runtime_protocol/service.py`: `5a051f014e01698746dfe48b39ecadc9042b228a7a26df1bb439a79aa77b2666`.
  - `runtime_protocol/timeline_commit_port.py`: `e1d9397bc8164af8b4afd7f2b8d3133805c7404bce26b25cad32432d1f17badd`.
  - `runtime_protocol/timeline_commit_execution.py`: `334c161f8cc652a6f645fb94d5b7667ad345fd33a44f1560b01547e5f765f655`.
  - `runtime_protocol/timeline_commit_auth.py`: `357d7c473d8e1af42646aea57657222123cc039adde16f2700629991d25beafd`.
  - `runtime_protocol/timeline_commit_store.py`: `f0867b6bf083aef2ca280c3f1bcbbbc926c7dfc448c519836e286022f5e3d59a`.
  - `runtime_protocol/timeline_commit_inputs.py`: `bf04dc5d26fd6e6283ae11c7d0fa55fa5730c45f19e1c55bda529062cab696e4`.
  - `contract/commit-v2.md`: `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`.

## Whole-path source trace

1. `service.py:2445-2515` authenticates the canonical `commitTimeline` route and constructs the request-scoped `RequestCommitPort`.
2. `timeline_commit_execution.py:241-247` invokes the registered Agent provider and verifies its returned outcome.
3. `timeline_commit_port.py:640-675` sends the prepared candidate to the Runtime store and retains only the private sequential capture for that attempt.
4. Agent `commit.py:1331-1444` prepares the candidate, records the provider result, and calls `port.accept(prepared)`; `_commit_preview.py:25-90` carries original/landing command boundaries and prepared-record metadata.
5. Runtime `timeline_commit_store.py:1459-1533` calls authenticated record validation; `timeline_commit_store.py:1800-1855` performs the guarded acceptance and durable receipt.

## Confirmed seam

The retained genuine-provider regression has three controls: unchanged final parent PASS, the same commands grouped into one step PASS, and unchanged intermediate parent FAIL at the Runtime auth guard. The failure is structurally explained by the current code:

- Agent `_commit_patch.py:512-601` computes each step's authoritative effect patch from that step's input/output. An unchanged semantic step can legitimately produce `step.patch == []`.
- Agent `_commit_patch.py:618-634` emits `commit.effect` bindings only for actual effect entries. It must not invent an effect ordinal for an empty patch.
- Runtime `timeline_commit_auth.py:773-844` starts `step_output()` from the authenticated step boundary and applies the step patch. For an unchanged parent with no parent effect binding, lines `835-839` require the projected image to equal `accepted` (the final candidate), unless it is a recognized materialization reconciliation.
- Runtime `timeline_commit_auth.py:2794-2897` iterates steps in order, passes the current ordinal boundary to `step_output()`, then requires the final accumulated boundary to equal the accepted closure. Thus the failing intermediate check is comparing an unchanged intermediate image with the final candidate, not with its actual ordinal boundary.

The 2-pass controls are consistent with this: when the unchanged parent is final, the actual boundary equals `accepted`; when commands are grouped, the step's patch includes the later parent change and its output reaches `accepted`. Only a later command after the empty intermediate step separates the actual intermediate parent from the final candidate.

## Guard preservation

The proposed ownership does not relax authentication. Runtime still must preserve effect-ordinal bounds (`timeline_commit_auth.py:2416-2420`), binding phase/ordinal/head checks (`:467-535`), physical owner/source/pin checks, strict closure and managed-field refusals, and store-side CAS/idempotency/receipt validation. Empty `media.admit` must remain an empty effect set; adding an effect ordinal would be an invalid fabricated claim.

## Smallest later author scope

- One Runtime author, one narrow source change in `runtime_protocol/timeline_commit_auth.py`, limited to the no-effect intermediate-parent projection in `step_output()` and its directly required boundary assertion. The comparison must use the authenticated ordinal/step boundary for an unchanged image, while retaining the final accumulated-boundary equality and all existing effect/materialization guards.
- One regression scope: retain the existing Agent selector `tests/sdk/test_effect_image_prepared_candidate_runtime.py::test_unchanged_step_preserves_its_parent_image[unchanged-intermediate-parent]` and add/adjust only the Runtime-side focused authentication fixture needed to exercise the same three-step shape. Keep the two passing controls and all original refusal/guard expectations unchanged. No media effect, source/pin workaround, Agent provider change, body collector, full suite, P4, or App change is authorized by this finding.

## Missing retained artifacts

The following exact Agent worker artifacts are absent locally and were not recreated:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D115-effect83-sol-0932/report.md`.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D115-effect83-sol-0932/evidence/effect83-source-manifest.json`.
- The retained genuine-provider 2-pass/1-fail XML and recipe were not present under the shared scratchpad with exact filenames or hashes.

These are needed only for independent functional custody/replay attribution: the exact path, SHA-256, and safe count/class summary for the XML/recipe, plus the worker report/manifest. No replay, service contact, raw payload, auth material, stack, or new probe was attempted.

## Validation

- AST parse of all six Runtime source files and both Agent provider helper files: PASS.
- `git diff --check`: PASS; worktree remained unchanged before evidence output.
- Existing Runtime auth focused tests: PASS, 4 passed, 110 deselected.
- Existing Runtime private sequential-capture tests: PASS, 17 passed, 50 deselected.
- Broader sequential-verifier/provider probe was not treated as qualification: 56 passed, 1 failed, 10 errors; the failure used an incomplete in-memory store fixture (`db_path` absent), and the errors lacked the Agent package (`ModuleNotFoundError: astrid`).
