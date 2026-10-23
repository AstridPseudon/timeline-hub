"""Authenticated Runtime boundaries for grouped inverse stages."""
from __future__ import annotations

import copy

import pytest
import test_timeline_commit_port as port_tests

from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.timeline_commit_port import digest, route_path
from runtime_protocol.timeline_commit_validation import validate_commit_value

service = port_tests.service


def _request(runtime, publication):
    head = runtime.get_project_timeline(runtime.test_project, "main")
    return {
        "api_version": 1,
        "project_id": runtime.test_project,
        "timeline_id": "main",
        "base_revision_id": head["head_revision_id"],
        "base_publication_id": head["head_publication_id"],
        "commands": [{
            "schema_version": 1,
            "op": "timeline.inverse",
            "version": "1",
            "select": None,
            "args": {"publications": [publication]},
        }],
        "label": "Grouped inverse",
        "merge": "fields",
        "reads": [],
        "steps": [{
            "id": "undo",
            "label": "Grouped inverse",
            "intent": "Undo",
            "tags": [],
            "command_ordinals": [0],
            "patch": [],
        }],
    }


def _prepared(context, port, mutation=None):
    request = context["request"]
    head = port.head()
    source = port.revision_closure(head["revision_id"])
    before_parent = copy.deepcopy(source["parent_revision"])
    first_payload = copy.deepcopy(before_parent["payload"])
    first_payload["meta"] = {"org.example.stage": {"one": True}}
    final_payload = copy.deepcopy(first_payload)
    final_payload["meta"]["org.example.stage"]["two"] = True

    effects = [
        {"op": "set", "ref": "parent", "path": ["meta"],
         "before": {"state": "absent"}, "value": first_payload["meta"]},
        {"op": "set", "ref": "parent", "path": ["meta", "org.example.stage", "two"],
         "before": {"state": "absent"}, "value": True},
    ]
    writes = [
        {"ref": "parent", "path": ["meta"], "before": effects[0]["before"],
         "after": {"state": "present", "value": first_payload["meta"]}},
        {"ref": "parent", "path": ["meta", "org.example.stage", "two"],
         "before": effects[1]["before"], "after": {"state": "present", "value": True}},
    ]

    def image(payload, revision_id):
        return {**copy.deepcopy(before_parent), "revision_id": revision_id,
                "content_digest": digest(payload), "payload": copy.deepcopy(payload)}

    first = image(first_payload, "inverse-stage-one")
    final = image(final_payload, "inverse-stage-two")
    document = copy.deepcopy(source)
    document["parent_revision"] = final
    common = {"base_revision_id": request["base_revision_id"],
              "base_publication_id": request["base_publication_id"],
              "evaluated_head": copy.deepcopy(head), "command_ordinal": 0,
              "step_id": "undo", "phase": "effect"}

    def effect_binding(index, side, boundary_image):
        boundary = {**common, "side": side}
        return {"key": "commit.effect", "ref": "parent", "physical_ref": "parent",
                "revision_id": boundary_image["revision_id"],
                "content_digest": boundary_image["content_digest"], "policy": "fixed",
                "dependencies": [], "path": effects[index]["path"],
                "boundary": boundary, "step_id": "undo", "effect_ordinal": index}

    publication = request["commands"][0]["args"]["publications"][0]
    stage_one = {"key": "inverse.stage", "ref": "parent", "policy": "fixed",
                 "dependencies": [], "boundary": {"publication_id": publication,
                 "step_id": "original-one", "command_ordinals": [0],
                 "native_write_range": [0, 1], "effect_range": [0, 1]}}
    stage_two = {"key": "inverse.stage", "ref": "parent", "policy": "fixed",
                 "dependencies": [], "boundary": {"publication_id": publication,
                 "step_id": "original-two", "command_ordinals": [1],
                 "native_write_range": [1, 2], "effect_range": [1, 2]}}
    bindings = [stage_one, stage_two,
                effect_binding(0, "before", before_parent), effect_binding(0, "after", first),
                effect_binding(1, "before", first),
                effect_binding(1, "after", final)]
    if mutation == "digest":
        bindings[-1]["content_digest"] = "sha256:" + "0" * 64
    elif mutation == "unrelated":
        unrelated = image({"unrelated": True}, "unrelated-image")
        bindings[-1].update(revision_id=unrelated["revision_id"], content_digest=unrelated["content_digest"])
    elif mutation == "overlap":
        stage_two["boundary"]["effect_range"] = [0, 2]
    elif mutation == "missing":
        stage_two["boundary"]["effect_range"] = [2, 2]
    elif mutation == "reordered":
        stage_two["boundary"]["effect_range"] = [0, 1]
    elif mutation == "missing-binding":
        bindings.pop()

    record = {"ordinal": 0, "command": copy.deepcopy(request["commands"][0]),
              "writes": writes, "reads": [], "selections": [], "bindings": bindings,
              "created": [], "dependencies": [], "derived_writes": []}
    step = {**copy.deepcopy(request["steps"][0]), "patch": effects, "dependencies": []}
    value = {"expected_head": head, "canonical_document": document,
             "document_digest": digest(document),
             "records": {"schema_version": 1, "commands": [record], "undo_of": [publication],
                         "restored_from": None, "label": request["label"], "merge_mode": "fields",
                         "steps": [step]}, "id_map": {}, "semantic_events": [],
             "provider_version": "inverse-stage-test", "compiler_version": "fixture-1"}
    validate_commit_value(value, "PreparedCommit")
    return value


@pytest.mark.parametrize("mutation", [None, "digest", "unrelated", "overlap", "missing", "reordered",
                                       "missing-binding"])
def test_grouped_inverse_effects_use_authenticated_stage_images(service, mutation):
    service.test_provider.action = lambda context, port: port.accept(port_tests.prepared(context, port))
    port_tests.commit(service, port_tests.request(service), key="inverse-stage-seed")
    history = service.list_timeline_commits(service.test_project, "main", authorize=lambda: None)
    publication = history["items"][-1]["publication_id"]
    request = _request(service, publication)

    def execute(context, port):
        return port.accept(_prepared(context, port, mutation))

    service.test_provider.action = execute
    if mutation is None:
        result = service.commit_timeline(service.test_project, "main", request,
                                         idempotency_key="inverse-stage-valid",
                                         publisher="editor", invocation_path=route_path(service.test_project, "main"),
                                         authorize=lambda: None)
        assert result["data"]["status"] == "accepted"
    else:
        with pytest.raises(RuntimeErrorBase) as error:
            service.commit_timeline(service.test_project, "main", request,
                                    idempotency_key="inverse-stage-" + mutation,
                                    publisher="editor", invocation_path=route_path(service.test_project, "main"),
                                    authorize=lambda: None)
        assert error.value.details is not None
        assert error.value.details["reason"] == "invalid_records"
