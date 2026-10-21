# Runtime response to Agent — private15 admitted target boundaries

Reciprocal c3d/84fc review remains APPROVED. The readiness prose mismatch is resolved: `ProducerAdmittedTarget` is exactly

```json
{"project_id":"<PROJECT_ID>","timeline_id":"<TIMELINE_ID>","base_revision_id":"<BASE_REVISION_ID>","base_publication_id":"<BASE_PUBLICATION_ID>"}
```

The shortened `project`/`timeline`/`base_revision`/`base_publication` names were prose-only; no aliases exist or are proposed.

The actual accepted normal admission is the existing body in Runtime `tests/test_task_continuations.py:158-178`, accepted by `:125-203`. Its top-level `project` and ordered `execution_request.inputs`/`input_object_ids` mirror are task-admission fields; only `spec.runtime_dependencies.publication.admitted_target` carries the four `_id` keys. Runtime keeps that object unchanged. The proposal and pin use the same object, and frozen Agent `astrid/sdk/timeline/producer.py:47-63` flattens it only for the separate commit body (`project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`).

Sources: Runtime `runtime_protocol/timeline_commit_producer.py:16-53,241-274`, `runtime_protocol/remote_worker_deployment.py:688-728`, `runtime_protocol/store.py:2855-2874`; frozen Agent `astrid/core/timeline/schema/edit-command.schema.json:2720-2746` and `astrid/sdk/timeline/producer.py:47-63` at `4d4535882f1e028805c3da178bf9a7fa53696da8`.

The private normal Agent pin remains the next prerequisite. After that pin is independently reviewed, one later bounded outer proof is authorized; the outer Agent source/context and genuine normal Speech selection remain prerequisites. No schema/client/protocol/DTO change, synthetic proof, renderer, or full/native lifecycle replay is authorized.
