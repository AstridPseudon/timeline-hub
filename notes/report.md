# Runtime retirement census — handoff

HEAD `845db0a`; the 43-test `test_shot_composition_runtime.py` map is intentionally excluded. Static scan found surviving positive legacy consumers in these families:

- `test_timeline_clip_replacement.py`: 9 positive source/CAS/retry/http nodes; migrate to a clip replacement command and immutable media selection.
- `test_timeline_render_publication.py`: 3 positive fence/cancel/crash-retry nodes; migrate to revision-pinned `rendering.render` settlement.
- `test_runtime_e2e.py::test_project_shot_reference_crud_isolated_idempotent_and_restart_durable`: full project shot/item/reference/association/restart journey; needs Agent commands and Runtime media/reference pins.
- `test_shot_text_bindings.py`: 4 set/rebind/validation/digest nodes; needs Agent binding commands and Runtime immutable text selection.
- `test_shot_candidate_promotion.py`: 2 promotion/provenance nodes; needs canonical shot ownership, exact media pins, and guarded invalidation.
- `test_runtime_domains.py` and `test_runtime_exact_idempotency.py`: positive timeline, shot, and reference domain/idempotency journeys; not route-retirement proofs.

Fixture-only old publication setup remains in `test_timeline_native_inspection.py` (20 inspection families), restore-port `_seed`, cutover `_service`, realm-admission legacy dependency boundaries, streaming-media concurrency, and visual-seam/render setup. Replace setup with captured/verified commit fixtures while preserving read, restore, closure, media, and health assertions.

Canonical `timeline:*` document writes are retired; ordinary config/transcript/source document updates remain supported and are not findings. Canonical task effects are already zero-write covered by `test_timeline_effect_authority.py`; `project.update` effects remain outside this retirement.

Next three smallest patches: text bindings (4), revision-pinned render publication (3), candidate promotion (2). Cross-manager dependencies are Agent command schemas/captures, Runtime exact pins/fences, and App producer conversion; Viewing owns advisory scene evaluation and render parity.

Evidence: selected `pytest --collect-only` run collected 724/748 tests (24 deselected), with only the pre-existing unknown `timeout` warning. No test execution/full suite was run.
