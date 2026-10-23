"""Authenticated Runtime boundaries for grouped inverse stages."""
from __future__ import annotations

import copy

import pytest
import test_timeline_commit_integration as real_tests
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


def _seed_request(runtime):
    head = runtime.get_project_timeline(runtime.test_project, "main")
    changes = [
        {"op": "set", "ref": "parent", "path": ["unknown"],
         "before": {"state": "absent"}, "value": {"stage": {"one": True, "two": True}}},
        {"op": "set", "ref": "parent", "path": ["unknown", "stage", "two"],
         "before": {"state": "present", "value": True}, "value": True},
    ]
    return {"api_version": 1, "project_id": runtime.test_project, "timeline_id": "main",
            "base_revision_id": head["head_revision_id"], "base_publication_id": head["head_publication_id"],
            "commands": [{"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
                          "args": {"changes": [changes[0]]}},
                         {"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
                          "args": {"changes": [changes[1]]}}],
            "label": "Seed grouped source", "merge": "fields", "reads": [],
            "steps": [{"id": "original-one", "label": "One", "intent": "Seed", "tags": [],
                       "command_ordinals": [0], "patch": [changes[0]]},
                      {"id": "original-two", "label": "Two", "intent": "Seed", "tags": [],
                       "command_ordinals": [1], "patch": [changes[1]]}]}


def _seed(context, port):
    request = context["request"]
    head = port.head()
    source = port.revision_closure(head["revision_id"])
    document = copy.deepcopy(source)
    parent = document["parent_revision"]
    first = request["commands"][0]["args"]["changes"][0]
    second = request["commands"][1]["args"]["changes"][0]
    parent["payload"]["unknown"] = copy.deepcopy(first["value"])
    parent["payload"]["unknown"]["stage"]["two"] = second["value"]
    parent["revision_id"] = "seed-parent"
    parent["content_digest"] = digest(parent["payload"])

    def record(ordinal, command, change, step_id, before, after):
        boundary = {"base_revision_id": request["base_revision_id"],
                    "base_publication_id": request["base_publication_id"],
                    "evaluated_head": copy.deepcopy(head), "command_ordinal": ordinal,
                    "step_id": step_id, "phase": "input", "change_ordinal": 0}
        binding = {"key": "doc.patch:0", "ref": "parent", "physical_ref": "parent",
                   "revision_id": before["revision_id"], "content_digest": before["content_digest"],
                   "policy": "fixed", "dependencies": [], "path": change["path"],
                   "change": copy.deepcopy(change), "write_range": [0, 1], "boundary": boundary}
        effect_boundary = {**boundary, "phase": "effect"}
        effect_bindings = []
        for side, image in (("before", before), ("after", after)):
            effect_bindings.append({"key": "commit.effect", "ref": "parent", "physical_ref": "parent",
                                    "revision_id": image["revision_id"], "content_digest": image["content_digest"],
                                    "policy": "fixed", "dependencies": [], "path": change["path"],
                                    "boundary": {**effect_boundary, "side": side}, "effect_ordinal": 0})
        return {"ordinal": ordinal, "command": copy.deepcopy(command),
                "writes": [{"ref": "parent", "path": change["path"], "before": change["before"],
                            "after": {"state": "present", "value": copy.deepcopy(after["payload"])}}],
                "reads": [], "selections": [], "bindings": [binding, *effect_bindings], "created": [],
                "dependencies": [], "derived_writes": []}

    before = copy.deepcopy(source["parent_revision"])
    first_parent = copy.deepcopy(before)
    first_parent["payload"]["unknown"] = copy.deepcopy(first["value"])
    first_parent["content_digest"] = digest(first_parent["payload"])
    second_parent = copy.deepcopy(first_parent)
    second_parent["payload"]["unknown"]["stage"]["two"] = second["value"]
    records = {"schema_version": 1,
               "commands": [record(0, request["commands"][0], first, "original-one", before,
                                    first_parent),
                            record(1, request["commands"][1], second, "original-two", first_parent,
                                    second_parent)],
               "undo_of": [], "restored_from": None, "label": request["label"], "merge_mode": "fields",
               "steps": [{**request["steps"][0], "dependencies": []},
                         {**request["steps"][1], "dependencies": []}]}
    value = {"expected_head": head, "canonical_document": document,
             "document_digest": digest(document), "records": records, "id_map": {},
             "semantic_events": [], "provider_version": "inverse-stage-seed",
             "compiler_version": "fixture-1"}
    validate_commit_value(value, "PreparedCommit")
    return port.accept(value)


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

    if mutation == "missing-history":
        request["commands"][0]["args"]["publications"] = ["missing-publication"]
    publication = request["commands"][0]["args"]["publications"][0]
    stage_one = {"key": "inverse.stage", "ref": "parent", "policy": "fixed",
                 "dependencies": [], "boundary": {"publication_id": publication,
                 "step_id": "original-two", "command_ordinals": [1],
                 "native_write_range": [0, 1], "effect_range": [0, 1]}}
    stage_two = {"key": "inverse.stage", "ref": "parent", "policy": "fixed",
                 "dependencies": [], "boundary": {"publication_id": publication,
                 "step_id": "original-one", "command_ordinals": [0],
                 "native_write_range": [1, 2], "effect_range": [1, 2]}}
    bindings = [stage_one, stage_two,
                effect_binding(0, "before", before_parent), effect_binding(0, "after", first),
                effect_binding(1, "before", first), effect_binding(1, "after", final)]
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
    elif mutation == "publication":
        stage_one["boundary"]["publication_id"] = "foreign-publication"
    elif mutation == "step":
        stage_one["boundary"]["step_id"] = "foreign-step"
    elif mutation == "command-ordinal":
        stage_one["boundary"]["command_ordinals"] = [0]
    elif mutation == "native-range":
        stage_one["boundary"]["native_write_range"] = [0, 2]
    elif mutation == "ref":
        stage_one["ref"] = "foreign-stage-ref"
    elif mutation == "policy":
        stage_one["policy"] = "follow"
    elif mutation == "dependency":
        stage_one["dependencies"] = ["forged-dependency"]

    record = {"ordinal": 0, "command": copy.deepcopy(request["commands"][0]),
              "writes": writes, "reads": [], "selections": [], "bindings": bindings,
              "created": [], "dependencies": [], "derived_writes": []}
    step = {**copy.deepcopy(request["steps"][0]), "patch": effects, "dependencies": []}
    value = {"expected_head": head, "canonical_document": document,
             "document_digest": digest(document),
             "records": {"schema_version": 1, "commands": [record], "undo_of": [publication],
                         "restored_from": None, "label": request["label"], "merge_mode": "fields",
                         "steps": [step]},
             "id_map": {}, "semantic_events": [],
             "provider_version": "inverse-stage-test", "compiler_version": "fixture-1"}
    validate_commit_value(value, "PreparedCommit")
    return value


@pytest.mark.parametrize("mutation", [None, "digest", "unrelated", "overlap", "missing", "reordered",
                                       "missing-binding", "publication", "step", "command-ordinal",
                                       "native-range", "ref", "policy", "dependency", "missing-history"])
def test_grouped_inverse_effects_use_authenticated_stage_images(service, mutation):
    service.test_provider.action = _seed
    seed_request = _seed_request(service)
    port_tests.commit(service, seed_request, key="inverse-stage-seed")
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
        replay = service.list_timeline_commits(service.test_project, "main", authorize=lambda: None)
        assert replay["items"][-1]["records"]["undo_of"] == [publication]
    else:
        with pytest.raises(RuntimeErrorBase) as error:
            service.commit_timeline(service.test_project, "main", request,
                                    idempotency_key="inverse-stage-" + mutation,
                                    publisher="editor", invocation_path=route_path(service.test_project, "main"),
                                    authorize=lambda: None)
        assert error.value.details is not None
        assert error.value.details["reason"] == ("history_unavailable" if mutation == "missing-history"
                                                   else "invalid_records")


# Use the captured film and installed production provider, including its native
# recorder aliases and canonical effect images, in the normal Runtime suite.
film = real_tests.film
agent = real_tests.agent
editing = real_tests.editing


@pytest.mark.integration
@pytest.mark.parametrize("recipe", ["move", "track", "multistage"])
def test_current_agent_inverse_stage_round_trip(editing, monkeypatch, recipe):
    original = editing.document()
    if recipe == "move":
        body = editing.body([editing.move("music-bed", 1)])
    elif recipe == "track":
        track = {"id": "stage-audio", "kind": "audio", "extension": {"opaque": [None, "kept"]}}
        body = editing.body([editing.agent.track(editing.agent.bundle(original), "parent", track)])
    else:
        changes = [
            {"op": "set", "ref": "parent", "path": ["meta"], "before": {"state": "absent"},
             "value": {"org.example.stage": {"one": True}}},
            {"op": "set", "ref": "parent", "path": ["meta", "org.example.stage", "two"],
             "before": {"state": "absent"}, "value": True},
        ]
        body = editing.body([{"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
                              "args": {"changes": [change]}} for change in changes])
        body["steps"] = [{"id": "source-" + str(index), "label": "Stage " + str(index),
                          "intent": "Sequential patch", "tags": [], "command_ordinals": [index],
                          "patch": [change], "reads": []} for index, change in enumerate(changes)]
    first = editing.commit(body, "stage-source")
    expected = copy.deepcopy(original)
    if recipe == "move":
        newer = editing.commit(editing.body([editing.move("music-other", 2)]), "stage-disjoint")
        expected = copy.deepcopy(newer["data"]["canonical_document"])
        for container in ([], ["config"]):
            target = expected["parent_revision"]["payload"]
            baseline = original["parent_revision"]["payload"]
            for key in container:
                target, baseline = target[key], baseline[key]
            target["clips"] = [copy.deepcopy(next(row for row in baseline["clips"] if row["id"] == clip["id"]))
                               if clip["id"] == "music-bed" else clip for clip in target["clips"]]
    history = copy.deepcopy(editing.history())
    undo = editing.body([real_tests.inverse(first["receipt"]["receipt_id"])])
    before = real_tests.rows(editing.service)
    preview = editing.commit({**copy.deepcopy(undo), "dry_run": True}, "stage-preview")
    assert preview["data"]["status"] == "preview" and preview["receipt"] is None
    assert real_tests.rows(editing.service) == before
    result = editing.commit(undo, "stage-undo")
    actual = result["data"]["canonical_document"]
    # Generated parent revision names may change; every document byte they
    # authenticate, including all closure families, must be restored exactly.
    expected["parent_revision"]["revision_id"] = actual["parent_revision"]["revision_id"]
    expected["parent_revision"]["content_digest"] = digest(expected["parent_revision"]["payload"])
    real_tests.assert_json_equal(actual, expected)
    real_tests.assert_json_equal(preview["data"]["canonical_document"]["parent_revision"]["payload"],
                                 actual["parent_revision"]["payload"])
    assert editing.history()[:-1] == history
    record = editing.history()[-1]["records"]["commands"][0]
    stages = [binding["boundary"] for binding in record["bindings"] if binding["key"] == "inverse.stage"]
    assert [stage["publication_id"] for stage in stages] == [first["receipt"]["receipt_id"]] * len(stages)
    assert [stage["step_id"] for stage in stages] == (["source-1", "source-0"] if recipe == "multistage" else ["edit"])
    after = real_tests.rows(editing.service)

    def forbidden(self, context, port):
        raise AssertionError("exact retry executed Agent")

    monkeypatch.setattr(type(editing.service._timeline_commit_provider), "commit", forbidden)
    assert editing.commit(copy.deepcopy(undo), "stage-undo") == result
    assert real_tests.rows(editing.service) == after
    editing.assert_readback(first)
    editing.assert_readback(result)


@pytest.mark.integration
@pytest.mark.parametrize("mutation", ["sequential-before", "sequential-after", "publication", "step",
                                      "command-ordinal", "ref"])
def test_current_agent_inverse_rejects_forged_stage(editing, monkeypatch, mutation):
    from runtime_protocol.timeline_commit_port import RequestCommitPort

    first = editing.commit(editing.body([editing.move("music-bed", 1)]), "forgery-source")
    before, history = real_tests.rows(editing.service), copy.deepcopy(editing.history())
    accept = RequestCommitPort.accept
    reached = []

    def forged_accept(port, prepared):
        value = copy.deepcopy(prepared)
        record = value["records"]["commands"][0]
        if mutation.startswith("sequential-"):
            write = next(write for write in record["writes"] if write["path"] == ["app", "astrid"])
            assert write["before"] == {"state": "present", "value": {}}
            write[mutation.removeprefix("sequential-")] = {"state": "present", "value": {"forged": True}}
        else:
            stage = next(binding for binding in record["bindings"] if binding["key"] == "inverse.stage")
            if mutation == "ref":
                stage["ref"] = "forged-stage-ref"
            else:
                key, replacement = {"publication": ("publication_id", "foreign-publication"),
                                    "step": ("step_id", "foreign-step"),
                                    "command-ordinal": ("command_ordinals", [1])}[mutation]
                stage["boundary"][key] = replacement
        reached.append(True)
        return accept(port, value)

    monkeypatch.setattr(RequestCommitPort, "accept", forged_accept)
    with pytest.raises(RuntimeErrorBase) as error:
        editing.commit(editing.body([real_tests.inverse(first["receipt"]["receipt_id"])]), "forged-stage")
    assert reached == [True]
    assert error.value.details["reason"] == "invalid_records"
    assert real_tests.rows(editing.service) == before
    assert editing.history() == history


@pytest.mark.integration
@pytest.mark.parametrize("mutation", ["replace", "add", "remove", "changed-path", "duplicate", "reorder"])
def test_current_agent_inverse_native_membership_is_authenticated(editing, monkeypatch, mutation):
    from runtime_protocol.timeline_commit_port import RequestCommitPort

    first = editing.commit(editing.body([editing.move("music-bed", 1)]), "native-forgery-source")
    before, history = real_tests.rows(editing.service), copy.deepcopy(editing.history())
    accept = RequestCommitPort.accept
    reached = []

    def forged_accept(port, prepared):
        value = copy.deepcopy(prepared)
        record = value["records"]["commands"][0]
        forged = {"ref": "parent", "path": ["config", "forged-native-write"],
                  "before": {"state": "absent"}, "after": {"state": "absent"}}
        if mutation == "replace":
            record["writes"][0] = forged
        elif mutation == "add":
            record["writes"].append(forged)
            stage = next(binding for binding in record["bindings"] if binding["key"] == "inverse.stage")
            stage["boundary"]["native_write_range"][1] += 1
        elif mutation == "remove":
            # Removing an absent-to-absent observation cannot change output.
            index = next(index for index, write in enumerate(record["writes"])
                         if write["before"] == write["after"] == {"state": "absent"})
            record["writes"].pop(index)
            stage = next(binding for binding in record["bindings"] if binding["key"] == "inverse.stage")
            stage["boundary"]["native_write_range"][1] -= 1
        else:
            index = next(index for index, write in enumerate(record["writes"])
                         if write["before"] == write["after"] == {"state": "absent"})
            if mutation == "changed-path":
                # Remain inside the canonical removed app container. Footprint
                # overlap alone must not authorize a different native fact.
                record["writes"][index]["path"] = ["app", "astrid", "forged-native-write"]
            elif mutation == "duplicate":
                record["writes"][index] = copy.deepcopy(record["writes"][index + 1])
            else:
                record["writes"][index], record["writes"][index + 1] = (
                    record["writes"][index + 1], record["writes"][index])
        reached.append(True)
        return accept(port, value)

    monkeypatch.setattr(RequestCommitPort, "accept", forged_accept)
    with pytest.raises(RuntimeErrorBase) as error:
        editing.commit(editing.body([real_tests.inverse(first["receipt"]["receipt_id"])]), "native-forgery")
    assert reached == [True]
    assert error.value.details["reason"] == "invalid_records"
    assert real_tests.rows(editing.service) == before
    assert editing.history() == history


@pytest.mark.parametrize("mutation", ["reviewer", "source-sites-without-effects"])
def test_reviewer_replaced_native_write_is_refused_before_persistence(service, mutation):
    service.test_provider.action = _seed
    port_tests.commit(service, _seed_request(service), key="reviewer-seed")
    publication = service.list_timeline_commits(
        service.test_project, "main", authorize=lambda: None)["items"][-1]["publication_id"]
    request = _request(service, publication)
    before = real_tests.rows(service)
    history = copy.deepcopy(service.list_timeline_commits(service.test_project, "main", authorize=lambda: None))

    def execute(context, port):
        value = _prepared(context, port)
        writes = value["records"]["commands"][0]["writes"]
        if mutation == "reviewer":
            writes[0]["path"] = ["config", "forged-native-write"]
            writes[0]["before"] = {"state": "absent"}
            writes[0]["after"] = {"state": "absent"}
        else:
            # Exact source membership alone cannot prove that native captures
            # cover the independently authenticated canonical stage image.
            payload = port.revision_closure(port.head()["revision_id"])["parent_revision"]["payload"]
            for write, path, observed in ((writes[0], ["unknown", "stage", "two"], True),
                                          (writes[1], ["unknown"], payload["unknown"])):
                write["path"] = path
                write["before"] = {"state": "present", "value": copy.deepcopy(observed)}
                write["after"] = copy.deepcopy(write["before"])
        return port.accept(value)

    service.test_provider.action = execute
    with pytest.raises(RuntimeErrorBase) as error:
        service.commit_timeline(service.test_project, "main", request,
                                idempotency_key="reviewer-forged-write", publisher="editor",
                                invocation_path=route_path(service.test_project, "main"), authorize=lambda: None)
    assert error.value.details["reason"] == "invalid_records"
    assert real_tests.rows(service) == before
    assert service.list_timeline_commits(service.test_project, "main", authorize=lambda: None) == history


def test_grouped_canonical_stage_observations_retry_exactly(service):
    service.test_provider.action = _seed
    port_tests.commit(service, _seed_request(service), key="canonical-stage-seed")
    publication = service.list_timeline_commits(
        service.test_project, "main", authorize=lambda: None)["items"][-1]["publication_id"]
    request = _request(service, publication)
    service.test_provider.action = lambda context, port: port.accept(_prepared(context, port))

    def commit():
        return service.commit_timeline(service.test_project, "main", copy.deepcopy(request),
                                       idempotency_key="canonical-stage-retry", publisher="editor",
                                       invocation_path=route_path(service.test_project, "main"), authorize=lambda: None)

    result = commit()
    before = real_tests.rows(service)

    def forbidden(context, port):
        raise AssertionError("exact canonical-stage retry executed the provider")

    service.test_provider.action = forbidden
    assert commit() == result
    assert real_tests.rows(service) == before
