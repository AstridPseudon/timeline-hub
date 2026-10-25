# Runtime R2r occurrence-boundary disposition

Disposition: **UNAPPLIED**. No product, test, pin, schema, generated, guard,
or authority change is justified by the retained evidence.

## Scope and source identity

- Runtime current released source: `7070f1378d1917fcce69857ebd33cd2b3015568b`, tree `cd68015cb9fe85a6ecd2d15dd7e2eac69f67e2b1`.
- Registered Agent source: `547e10456250c1b5bcf63b44a50c90ff0563ce1e`, tree `68df11fad2b082fa12d99ca20404e1e40e350cd7`.
- Runtime registration is `runtime_protocol/timeline_commit_provider.py:70-93`, importing `astrid.sdk.timeline.commit.create_runtime_commit_service`.
- Agent seams inspected: birth capture (`native_occurrence_create.py:53-61`), occurrence media capture (`native_occurrence_media_commands.py:277-284`), producer capture (`producer.py:28-44`), inverse (`inverse.py:1032-1219`), sequential capture (`_commit_preview.py:25-90`), and the registered `RuntimeCommitService.commit` (`commit.py:1160-1469`).
- Runtime verifier seams inspected: `_inverse_stage_boundaries` (`timeline_commit_auth.py:1415-1788`), `_project_created_child` (`1854-2111`), `command_output` (`2147-2293`), and `validate_sequential_capture` (`2521-2828`).

## What the retained packet proves

The existing `design/app-D118c-occurrence2-invalid-exact-1132-facts.json`
packet is tied to immutable Runtime `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`
(tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`). Both exact inputs reached
the migrated invalid-timing assertions and the unchanged-base no-write/history
checks. The false case then stopped at Runtime auth line 1645 during
`media_undo`; the true case stopped at Runtime auth line 2267 during grouped
birth. The packet does not prove which side owns either guard outcome.

## Boundary comparison

At line 1645, Runtime requires the source accepted history to contain a
`commit.effect` binding for the successor physical reference with its
before-image `revision_id` and `content_digest`, matching the inverse
materialization binding. The retained packet lacks the accepted source
`records.commands[*].bindings`, inverse `inverse.stage`/
`commit.materialization` bindings, and the source/inverse closure images needed
for that equality. Producer versus verifier ownership is therefore **not
proved**.

At line 2267, Runtime has a changed immutable shot/internal image without a
unique authenticated following alias/promotion. Attribution requires the
following child-media command bindings (physical reference, revision, digest,
boundary and owner metadata) plus original/landing sequential command outputs
and the prepared canonical closure. Those fields are absent from the retained
facts. Producer versus verifier ownership is therefore **not proved**.

Closest passing same-property controls are the current Runtime tests for the
real created-child birth → child-track → occurrence-media chain:

- `test_timeline_commit_authentication.py::test_created_child_public_sequential_birth_aliases_accept_fields_and_atomic`
- `test_timeline_commit_authentication.py::test_created_child_promotion_keeps_prior_parent_media_and_mirror_writes`
- `test_timeline_popup_fork_owner_projection.py::test_actual_agent_fork_add_media_reaches_owner_projection`
- `test_timeline_inverse_historical_image.py::test_redo_reopens_exact_retired_images_with_one_native_write`

They establish the intended authenticated record shape and passing caller path,
but cannot supply the missing occurrence2 record values. No broader root-cause
audit or new run was performed.

Evidence and source hashes: `workers/rt-R2-occurrence-boundaries-1152/evidence/`.
