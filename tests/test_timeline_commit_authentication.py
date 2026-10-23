"""Sealed request/provider-record controls through the real service and port."""
from __future__ import annotations

import copy

import pytest
import test_timeline_commit_port as port_tests
from baseline_fixture import load_baseline_fixture
from test_timeline_commit_port import commit, request, rows

from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_auth import site
from runtime_protocol.timeline_commit_port import route_path
from runtime_protocol.timeline_commit_validation import digest, validate_commit_value

service = port_tests.service


def body(service):
    change = {"op": "set", "ref": "parent", "path": ["meta"],
              "before": {"state": "absent"}, "value": {"org.example.timeline": {"note": "opening"}}}
    command = {"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
               "args": {"changes": [change]}}
    return request(service, commands=[command], label="Annotate film", merge="fields", reads=[], steps=[{
        "id": "note", "label": "Opening note", "intent": "Annotate", "tags": [],
        "command_ordinals": [0], "patch": [change]}])


def candidate(context, port):
    request = context["request"]
    head = port.head()
    source = port.revision_closure(head["revision_id"])
    document = copy.deepcopy(source)
    change = copy.deepcopy(request["commands"][0]["args"]["changes"][0])
    parent = document["parent_revision"]
    parent["payload"]["meta"] = copy.deepcopy(change["value"])
    parent["revision_id"] = "annotated-" + context["idempotency_key"]
    parent["content_digest"] = digest(parent["payload"])
    step = {**copy.deepcopy(request["steps"][0]), "patch": [change],
            "dependencies": copy.deepcopy(request.get("reads", []))}
    step["dependencies"].extend(copy.deepcopy(step.get("reads", [])))
    binding = {"key": "doc.patch:0", "ref": "parent", "physical_ref": "parent",
               "revision_id": source["parent_revision"]["revision_id"],
               "content_digest": source["parent_revision"]["content_digest"],
               "policy": "fixed", "dependencies": [], "path": change["path"], "change": change,
               "write_range": [0, 1], "command_ordinal": 0, "change_ordinal": 0, "phase": "input",
               "boundary": {"base_revision_id": request["base_revision_id"],
                            "base_publication_id": request["base_publication_id"], "evaluated_head": head,
                            "command_ordinal": 0, "change_ordinal": 0, "step_id": step["id"], "phase": "input"}}
    record = {"ordinal": 0, "command": copy.deepcopy(request["commands"][0]),
              "writes": [{"ref": "parent", "path": change["path"], "before": change["before"],
                          "after": {"state": "present", "value": change["value"]}}],
              "reads": [], "selections": [], "bindings": [binding], "created": [],
              "dependencies": [], "derived_writes": []}
    value = {"expected_head": head, "canonical_document": document, "document_digest": digest(document),
             "records": {"schema_version": 1, "commands": [record], "undo_of": [], "restored_from": None,
                         "label": request["label"], "merge_mode": "fields", "steps": [step]},
             "id_map": {}, "semantic_events": [], "provider_version": "prepared-auth-1", "compiler_version": "fixture-1"}
    validate_commit_value(value, "PreparedCommit")
    return value


def provider(service, mutate=lambda value: None):
    def execute(context, port):
        value = candidate(context, port)
        mutate(value)
        validate_commit_value(value, "PreparedCommit")
        return port.preview(value) if context["request"].get("dry_run") else port.accept(value)
    service.test_provider.action = execute


@pytest.mark.parametrize("dry_run", [False, True])
def test_valid_record_accepts_and_retry_or_preview_preserves_authoritative_steps(service, dry_run):
    provider(service)
    submitted = body(service)
    submitted["dry_run"] = dry_run
    result = commit(service, submitted)
    assert result["data"]["status"] == ("preview" if dry_run else "accepted")
    assert result["data"]["steps"][0]["patch"] == submitted["steps"][0]["patch"]
    if not dry_run:
        assert commit(service, submitted) == result
        page = service.list_timeline_commits(service.test_project, "main", authorize=lambda: None)
        assert page["items"][-1]["steps"] == result["data"]["steps"]


@pytest.mark.parametrize("forged_allocation", [False, True])
def test_provider_command_normalizes_empty_allocation_claims_only(service, forged_allocation):
    def mutate(value):
        value["records"]["commands"][0]["command"]["created"] = ["parent/clip:forged"] if forged_allocation else []
    provider(service, mutate)
    submitted = body(service)
    before = rows(service)
    if forged_allocation:
        with pytest.raises(RuntimeErrorBase) as error:
            commit(service, submitted)
        assert error.value.details is not None and error.value.details["reason"] == "invalid_records"
        assert rows(service) == before
    else:
        result = commit(service, submitted)
        assert result["data"]["status"] == "accepted"
        assert commit(service, submitted) == result


@pytest.mark.parametrize("bad_pin", [None, "digest", "disagreement"])
def test_final_parent_reuse_keeps_the_exact_projected_effect_boundary(service, bad_pin):
    def mutate(value):
        record = value["records"]["commands"][0]
        binding = {key: copy.deepcopy(record["bindings"][0][key]) for key in (
            "ref", "physical_ref", "policy", "dependencies", "boundary", "path")}
        parent = value["canonical_document"]["parent_revision"]
        binding.update(key="commit.effect", revision_id="projected-parent", content_digest=parent["content_digest"],
                       effect_ordinal=0, step_id="note")
        binding["boundary"].update(phase="effect", side="after")
        if bad_pin == "digest":
            binding["content_digest"] = "sha256:" + "0" * 64
        record["bindings"].append(binding)
        if bad_pin == "disagreement":
            record["bindings"].append({**copy.deepcopy(binding), "revision_id": "foreign-parent"})
    provider(service, mutate)
    submitted = body(service)
    before = rows(service)
    if bad_pin:
        with pytest.raises(RuntimeErrorBase) as error:
            commit(service, submitted)
        assert error.value.details is not None and error.value.details["reason"] == "invalid_records"
        assert rows(service) == before
    else:
        result = commit(service, submitted)
        assert result["data"]["status"] == "accepted"
        assert commit(service, submitted) == result


@pytest.mark.parametrize("mutation", [
    "empty_patch", "different_command", "foreign_alias", "foreign_base", "foreign_publication",
    "foreign_head", "foreign_step", "foreign_ordinal", "foreign_phase", "different_path",
    "different_change", "outside_write_range", "output_image_as_input",
])
@pytest.mark.parametrize("dry_run", [False, True])
def test_forged_provider_records_are_rejected_without_writes(service, mutation, dry_run):
    def mutate(value):
        record = value["records"]["commands"][0]
        binding = record["bindings"][0]
        boundary = binding["boundary"]
        if mutation == "empty_patch":
            value["records"]["steps"][0]["patch"] = []
        elif mutation == "different_command":
            record["command"]["args"]["changes"][0]["value"] = {"forged": True}
        elif mutation == "foreign_alias":
            binding["ref"] = "foreign-alias"
        elif mutation == "foreign_base":
            boundary["base_revision_id"] = "foreign"
        elif mutation == "foreign_publication":
            boundary["base_publication_id"] = "foreign"
        elif mutation == "foreign_head":
            boundary["evaluated_head"] = {"revision_id": "foreign", "publication_id": "foreign"}
        elif mutation == "foreign_step":
            boundary["step_id"] = "foreign"
        elif mutation == "foreign_ordinal":
            boundary["command_ordinal"] = 1
        elif mutation == "foreign_phase":
            boundary["phase"] = "output"
        elif mutation == "different_path":
            binding["path"] = ["config"]
        elif mutation == "different_change":
            binding["change"]["value"] = {"forged": True}
        elif mutation == "outside_write_range":
            binding["write_range"] = [0, 2]
        elif mutation == "output_image_as_input":
            binding.update({key: value["canonical_document"]["parent_revision"][key]
                            for key in ("revision_id", "content_digest")})
    provider(service, mutate)
    submitted = body(service)
    submitted["dry_run"] = dry_run
    before = rows(service)
    with pytest.raises(RuntimeErrorBase) as error:
        commit(service, submitted)
    assert error.value.details is not None and error.value.details["reason"] == "invalid_records"
    assert rows(service) == before


@pytest.mark.parametrize("alias", [
    "occurrence:missing/text-binding:voiceover_script",
    "occurrence:occurrence-1/text-binding:voiceover_script:forged",
    "occurrence:occurrence-1/collection:forged",
])
def test_native_text_alias_refusals_are_atomic(service, alias):
    def mutate(value):
        value["records"]["commands"][0]["bindings"][0].update(
            ref=alias, physical_ref="parent")

    provider(service, mutate)
    before = rows(service)
    with pytest.raises(RuntimeErrorBase) as error:
        commit(service, body(service), key="native-alias-refusal-" + alias.split(":", 1)[0])
    assert error.value.details is not None and error.value.details["reason"] == "invalid_records"
    assert rows(service) == before


def test_native_text_alias_duplicate_slot_is_ambiguous():
    boundary = {
        "parent": {"payload": {"occurrences": [{
            "occurrence_id": "occ-1", "shot_revision_id": "shot-r1",
        }]}},
        "shot-revision:shot-r1": {"revision_id": "shot-r1", "content_digest": "digest",
                                   "payload": {"text_bindings": [
                                       {"kind": "prompt", "slot": "hero"},
                                       {"kind": "prompt", "slot": "hero"},
                                   ]}},
    }
    with pytest.raises(CommitRejected):
        site(boundary, "occurrence:occ-1/text-binding:prompt:hero", [])


@pytest.mark.parametrize("step_read", [False, True])
@pytest.mark.parametrize("bad_state", [False, True])
def test_read_claims_are_checked_at_input_and_in_dependency_union(service, step_read, bad_state):
    provider(service, lambda value: value["records"]["steps"][0].update(dependencies=[]))
    submitted = body(service)
    read = {"kind": "field", "ref": "parent", "path": ["meta"],
            "state": {"state": "present", "value": {"org.example.forged": {"value": "forged"}}}
            if bad_state else {"state": "absent"}}
    if step_read:
        submitted["steps"][0]["reads"] = [read]
    else:
        submitted["reads"] = [read]
    before = rows(service)
    with pytest.raises(RuntimeErrorBase) as error:
        commit(service, submitted)
    assert error.value.details is not None and error.value.details["reason"] == "invalid_records"
    assert rows(service) == before


@pytest.mark.parametrize("scope", [False, True])
def test_valid_read_union_can_keep_extra_captures_or_conservative_scope(service, scope):
    def mutate(value):
        if scope:
            value["records"]["steps"][0]["dependencies"] = [{"kind": "scope", "ref": "parent", "path": []}]
        else:
            value["records"]["steps"][0]["dependencies"].append({"kind": "scope", "ref": "timeline", "path": []})
    provider(service, mutate)
    submitted = body(service)
    submitted["reads"] = [{"kind": "field", "ref": "parent", "path": ["meta"], "state": {"state": "absent"}}]
    assert commit(service, submitted)["data"]["status"] == "accepted"


@pytest.mark.parametrize("omit_scope", [False, True])
def test_atomic_mode_requires_authoritative_scope_dependencies(service, omit_scope):
    def mutate(value):
        value["records"]["merge_mode"] = "atomic"
        if not omit_scope:
            value["records"]["steps"][0]["dependencies"] = [{"kind": "scope", "ref": "parent", "path": []}]
    provider(service, mutate)
    submitted = body(service)
    submitted.pop("reads")
    if omit_scope:
        with pytest.raises(RuntimeErrorBase) as error:
            commit(service, submitted)
        assert error.value.details is not None and error.value.details["reason"] == "invalid_records"
    else:
        assert commit(service, submitted)["data"]["merge_mode"] == "atomic"


@pytest.mark.parametrize("forge_input", [False, True])
@pytest.mark.parametrize("same_step", [False, True])
def test_sequential_step_reads_use_the_prior_step_output_and_keep_batch_reads(service, forge_input, same_step):
    submitted = body(service)
    batch_read = {"kind": "field", "ref": "parent", "path": ["meta"], "state": {"state": "absent"}}
    submitted["reads"] = [batch_read]
    change = {"op": "set", "ref": "parent", "path": ["meta", "org.example.timeline", "note"],
              "before": {"state": "present", "value": "opening"}, "value": "ending"}
    submitted["commands"].append({"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
                                   "args": {"changes": [change]}})
    step_read = {"kind": "field", "ref": "parent", "path": ["meta", "org.example.timeline", "note"], "state": change["before"]}
    submitted["steps"].append({"id": "revise", "label": "Revise note", "intent": "Revise", "tags": [],
                               "command_ordinals": [1], "patch": [change], "reads": [step_read]})
    if same_step:
        submitted["steps"] = [{**submitted["steps"][0], "command_ordinals": [0, 1],
                               "patch": [submitted["steps"][0]["patch"][0], change]}]

    def execute(context, port):
        value = candidate(context, port)
        first_image = copy.deepcopy(value["canonical_document"]["parent_revision"])
        first_image["revision_id"] = "intermediate-parent"
        first_binding = value["records"]["commands"][0]["bindings"][0]
        effect_binding = {key: copy.deepcopy(first_binding[key]) for key in (
            "ref", "physical_ref", "policy", "dependencies", "boundary", "path")}
        effect_binding.update(key="commit.effect", revision_id=first_image["revision_id"],
                              content_digest=first_image["content_digest"], step_id="note", effect_ordinal=0)
        effect_binding["boundary"].update(phase="effect", side="after")
        if not same_step:
            value["records"]["commands"][0]["bindings"].append(effect_binding)
        second_binding = copy.deepcopy(first_binding)
        second_binding.update(path=change["path"], change=change, command_ordinal=1,
                              revision_id=first_image["revision_id"], content_digest=first_image["content_digest"])
        second_binding["boundary"].update(step_id="note" if same_step else "revise", command_ordinal=1)
        if forge_input:
            second_binding.update(revision_id=first_binding["revision_id"], content_digest=first_binding["content_digest"])
        value["records"]["commands"].append({"ordinal": 1, "command": submitted["commands"][1],
            "writes": [{"ref": "parent", "path": change["path"], "before": change["before"],
                        "after": {"state": "present", "value": change["value"]}}],
            "reads": [{"ref": "parent", "path": change["path"], "state": change["before"]}],
            "bindings": [second_binding], "created": [], "selections": [], "dependencies": [], "derived_writes": []})
        if same_step:
            value["records"]["steps"][0].update(patch=submitted["steps"][0]["patch"], dependencies=[batch_read, step_read])
        else:
            value["records"]["steps"].append({**submitted["steps"][1], "dependencies": [batch_read, step_read]})
        parent = value["canonical_document"]["parent_revision"]
        parent["payload"]["meta"]["org.example.timeline"]["note"] = "ending"
        parent["revision_id"] = "sequential-parent"
        parent["content_digest"] = digest(parent["payload"])
        value["document_digest"] = digest(value["canonical_document"])
        validate_commit_value(value, "PreparedCommit")
        return port.accept(value)
    service.test_provider.action = execute
    if forge_input:
        with pytest.raises(RuntimeErrorBase) as error:
            commit(service, submitted)
        assert error.value.details is not None and error.value.details["reason"] == "invalid_records"
    else:
        result = commit(service, submitted)
        assert result["data"]["steps"][-1]["dependencies"] == [batch_read, step_read]
        assert commit(service, submitted) == result


@pytest.mark.parametrize("assert_effect", [False, True])
@pytest.mark.parametrize("omit_effect", [False, True])
def test_native_record_assertions_and_additional_effects_on_a_real_film(tmp_path, assert_effect, omit_effect):
    runtime, project, _ = load_baseline_fixture(tmp_path, variant="film")
    try:
        commits, _ = runtime._timeline_commits()
        head = commits.install_verified_baseline(project, "main", authorize=lambda: None)
        assert head is not None
        source = commits.revision_closure(project, "main", head["revision_id"])
        assert source is not None
        clip = source["parent_revision"]["payload"]["clips"][0]
        native = {"schema_version": 1, "op": "clip.move", "version": "1", "select": "parent/clip:" + clip["id"],
                  "args": {"on": clip["at"] + 1}}
        effect = {"op": "set", "ref": "parent", "path": ["config", "clips", "id:" + clip["id"], "at"],
                  "before": {"state": "present", "value": clip["at"]}, "value": clip["at"] + 1}
        step = {"id": "move", "label": "Move clip", "intent": "Move", "tags": [],
                "command_ordinals": [0], "patch": [effect] if assert_effect else []}
        submitted = {"api_version": 1, "project_id": project, "timeline_id": "main",
                     "base_revision_id": head["revision_id"], "base_publication_id": head["publication_id"],
                     "commands": [native], "label": "Move clip", "merge": "fields", "reads": [], "steps": [step]}

        def execute(context, port):
            observed_head = port.head()
            document = port.revision_closure(observed_head["revision_id"])
            parent = document["parent_revision"]
            collections = [parent["payload"]["clips"]]
            if "clips" in parent["payload"]["config"]:
                collections.append(parent["payload"]["config"]["clips"])
            for clips in collections:
                next(item for item in clips if item["id"] == clip["id"])["at"] = native["args"]["on"]
            # An additional authoritative observation is permitted even when
            # the caller asserts only its authored move (or asserts nothing).
            extra = {"op": "set", "ref": "parent", "path": ["meta"], "before": {"state": "absent"},
                     "value": {"org.example.provider": {"provider": "move"}}}
            parent["payload"]["meta"] = extra["value"]
            parent["revision_id"] = "native-moved"
            parent["content_digest"] = digest(parent["payload"])
            effects = [extra] if omit_effect else [effect, extra]
            record = {"ordinal": 0, "command": native, "writes": [{"ref": native["select"], "path": ["at"],
                      "before": effect["before"], "after": {"state": "present", "value": effect["value"]}}],
                      "reads": [], "selections": [], "bindings": [], "created": [], "dependencies": [], "derived_writes": []}
            value = {"expected_head": observed_head, "canonical_document": document, "document_digest": digest(document),
                     "records": {"schema_version": 1, "commands": [record], "undo_of": [], "restored_from": None,
                                 "label": "Move clip", "merge_mode": "fields", "steps": [{**step, "patch": effects, "dependencies": []}]},
                     "id_map": {}, "semantic_events": [], "provider_version": "prepared-auth-1", "compiler_version": "fixture-1"}
            validate_commit_value(value, "PreparedCommit")
            return port.accept(value)

        runtime.register_timeline_commit_provider(port_tests.PreparedProvider(execute))
        call = lambda: runtime.commit_timeline(project, "main", submitted, idempotency_key="native-move", publisher="editor",
                                              invocation_path=route_path(project, "main"), authorize=lambda: None)
        if omit_effect:
            with pytest.raises(RuntimeErrorBase) as error:
                call()
            assert error.value.details is not None and error.value.details["reason"] == "invalid_records"
        else:
            assert len(call()["data"]["steps"][0]["patch"]) == 2
    finally:
        runtime.close()


@pytest.mark.parametrize("foreign_alias", [False, True])
def test_created_child_is_a_valid_later_step_read_boundary(service, foreign_alias):
    submitted = body(service)
    create = {"schema_version": 1, "op": "occurrence.create", "version": "1", "select": "parent",
              "args": {"occurrence_id": "occ-new", "shot_id": "shot-new", "name": "Opening",
                       "track": "picture", "on": 0, "duration": 1}}
    submitted["commands"].insert(0, create)
    submitted["steps"][0]["command_ordinals"] = [1]
    read = {"kind": "field", "ref": "shot:shot-new", "path": ["name"],
            "state": {"state": "present", "value": "Opening"}}
    submitted["steps"][0]["reads"] = [read]
    submitted["steps"].insert(0, {"id": "create", "label": "Create opening", "intent": "Create",
                                   "tags": [], "command_ordinals": [0], "patch": []})

    def execute(context, port):
        head = port.head()
        source = port.revision_closure(head["revision_id"])
        internal_payload = {"clips": [], "tracks": []}
        internal = {"timeline_id": "shot:shot-new", "revision_id": "internal-new", "payload": internal_payload,
                    "content_digest": digest(internal_payload)}
        shot_payload = {"name": "Opening", "metadata": {}, "items": [], "internal_timeline_revision_id": "internal-new"}
        shot = {"shot_id": "shot-new", "revision_id": "shot-new-r1", "internal_timeline_revision_id": "internal-new",
                "payload": shot_payload, "content_digest": digest(shot_payload)}
        occurrence = {"occurrence_id": "occ-new", "shot_id": "shot-new", "shot_revision_id": "shot-new-r1",
                      "placement": {"start_ms": 0}, "duration_ms": 1000, "source_offset": 0,
                      "speed": {"numerator": 1, "denominator": 1}, "track": "picture", "transform": {},
                      "gain": 1, "muted": False, "provenance": {}}
        created = copy.deepcopy(source)
        created["shot_revisions"], created["internal_timeline_revisions"] = [shot], [internal]
        created["parent_revision"]["payload"]["occurrences"] = [occurrence]
        created["parent_revision"]["revision_id"] = "created-parent"
        created["parent_revision"]["content_digest"] = digest(created["parent_revision"]["payload"])
        created["dependency_manifest"]["shots"] = [{key: shot[key] for key in (
            "shot_id", "revision_id", "internal_timeline_revision_id", "content_digest")}]
        created["dependency_manifest"]["internal_timelines"] = [{key: internal[key] for key in (
            "timeline_id", "revision_id", "content_digest")}]
        effects = [{"op": "set", "ref": "internal-revision:internal-new", "path": [],
                    "before": {"state": "absent"}, "value": internal_payload},
                   {"op": "set", "ref": "shot-revision:shot-new-r1", "path": [],
                    "before": {"state": "absent"}, "value": shot_payload},
                   {"op": "set", "ref": "parent", "path": ["occurrences"],
                    "before": {"state": "present", "value": []}, "value": [occurrence]}]
        common = {"base_revision_id": submitted["base_revision_id"], "base_publication_id": submitted["base_publication_id"],
                  "evaluated_head": head, "command_ordinal": 0, "step_id": "create", "phase": "effect", "side": "after"}
        effect_binding = {"key": "commit.effect", "ref": "parent", "physical_ref": "parent", "policy": "fixed",
                          "dependencies": [], "path": ["occurrences"], "boundary": common, "effect_ordinal": 2,
                          "step_id": "create", "revision_id": "created-parent",
                          "content_digest": created["parent_revision"]["content_digest"]}
        first = {"ordinal": 0, "command": create, "writes": [], "reads": [], "selections": [],
                 "bindings": [effect_binding], "created": [], "dependencies": [], "derived_writes": []}
        # Reuse the normal complete annotation record on the now-created boundary.
        patch_context = copy.deepcopy(context)
        patch_context["request"] = {**submitted, "commands": submitted["commands"][1:], "steps": submitted["steps"][1:]}
        class BoundaryPort:
            def head(self):
                return head
            def revision_closure(self, revision):
                return copy.deepcopy(created)
        value = candidate(patch_context, BoundaryPort())
        second = value["records"]["commands"][0]
        second["ordinal"] = 1
        for binding in second["bindings"]:
            binding["command_ordinal"] = binding["boundary"]["command_ordinal"] = 1
        normalized_read = {**read, "ref": "shot-revision:shot-new-r1"}
        second["bindings"].append({"key": "commit.read", "ref": "shot:foreign" if foreign_alias else read["ref"],
            "physical_ref": normalized_read["ref"], "revision_id": shot["revision_id"], "content_digest": shot["content_digest"],
            "policy": "fixed", "dependencies": [], "path": ["name"], "dependency": normalized_read,
            "boundary": {**common, "command_ordinal": 1, "step_id": "note", "phase": "input"}})
        value["records"]["commands"] = [first, second]
        value["records"]["steps"][0]["dependencies"] = [normalized_read]
        value["records"]["steps"].insert(0, {**submitted["steps"][0], "patch": effects, "dependencies": []})
        validate_commit_value(value, "PreparedCommit")
        return port.accept(value)
    service.test_provider.action = execute
    if foreign_alias:
        with pytest.raises(RuntimeErrorBase) as error:
            commit(service, submitted)
        assert error.value.details is not None and error.value.details["reason"] == "invalid_records"
    else:
        result = commit(service, submitted)
        assert result["data"]["steps"][1]["dependencies"][0]["ref"] == "shot-revision:shot-new-r1"
        assert commit(service, submitted) == result


@pytest.mark.parametrize("forged_successor", [False, True])
def test_rebased_child_bindings_follow_only_authenticated_owner_edges(tmp_path, forged_successor):
    runtime, project, _ = load_baseline_fixture(tmp_path, variant="single")
    try:
        commits, _ = runtime._timeline_commits()
        base = commits.install_verified_baseline(project, "main", authorize=lambda: None)
        original = commits.revision_closure(project, "main", base["revision_id"])
        assert original is not None
        occurrence_id = original["parent_revision"]["payload"]["occurrences"][0]["occurrence_id"]
        shot_id = original["parent_revision"]["payload"]["occurrences"][0]["shot_revision_id"]
        original_shot = next(row for row in original["shot_revisions"] if row["revision_id"] == shot_id)
        original_ref = "internal-revision:" + original_shot["internal_timeline_revision_id"]

        def execute(context, port):
            request = context["request"]
            head = port.head()
            source = port.revision_closure(head["revision_id"])
            document = copy.deepcopy(source)
            occurrence = next(row for row in document["parent_revision"]["payload"]["occurrences"]
                              if row["occurrence_id"] == occurrence_id)
            shot = next(row for row in document["shot_revisions"] if row["revision_id"] == occurrence["shot_revision_id"])
            internal = next(row for row in document["internal_timeline_revisions"]
                            if row["revision_id"] == shot["internal_timeline_revision_id"])
            old_shot, old_internal = copy.deepcopy((shot, internal))
            call = request["commands"][0]
            claim = call["args"]["changes"][0]
            internal["payload"][claim["path"][0]] = copy.deepcopy(claim["value"])
            internal.update(revision_id="internal-" + context["idempotency_key"], content_digest=digest(internal["payload"]))
            shot["payload"]["internal_timeline_revision_id"] = internal["revision_id"]
            shot.update(revision_id="shot-" + context["idempotency_key"],
                        internal_timeline_revision_id=internal["revision_id"], content_digest=digest(shot["payload"]))
            occurrence["shot_revision_id"] = shot["revision_id"]
            parent = document["parent_revision"]
            parent.update(revision_id="parent-" + context["idempotency_key"], content_digest=digest(parent["payload"]))
            for family, before, after in (("shots", old_shot, shot), ("internal_timelines", old_internal, internal)):
                pin = next(row for row in document["dependency_manifest"][family] if row["revision_id"] == before["revision_id"])
                pin.update({key: after[key] for key in pin})
            old_s, new_s = "shot-revision:" + old_shot["revision_id"], "shot-revision:" + shot["revision_id"]
            old_i, new_i = "internal-revision:" + old_internal["revision_id"], "internal-revision:" + internal["revision_id"]
            effects = [
                {"op": "set", "ref": new_i, "path": [], "before": {"state": "absent"}, "value": internal["payload"]},
                {"op": "set", "ref": new_s, "path": [], "before": {"state": "absent"}, "value": shot["payload"]},
                {"op": "set", "ref": "parent", "path": ["occurrences"],
                 "before": {"state": "present", "value": source["parent_revision"]["payload"]["occurrences"]},
                 "value": parent["payload"]["occurrences"]},
                {"op": "remove", "ref": old_s, "path": [], "before": {"state": "present", "value": old_shot["payload"]}},
                {"op": "remove", "ref": old_i, "path": [], "before": {"state": "present", "value": old_internal["payload"]}},
            ]
            boundary = {"base_revision_id": request["base_revision_id"], "base_publication_id": request["base_publication_id"],
                        "evaluated_head": head, "command_ordinal": 0, "step_id": "edit", "phase": "input"}
            binding = {"key": "doc.patch:0", "ref": claim["ref"], "physical_ref": old_i,
                       "revision_id": old_internal["revision_id"], "content_digest": old_internal["content_digest"],
                       "policy": "fixed", "dependencies": [], "boundary": {**boundary, "change_ordinal": 0},
                       "path": claim["path"], "change": {**claim, "ref": old_i}, "write_range": [0, 1]}
            bindings = [binding]
            for before, after, edge_before, edge_after, image in (
                    (old_s, new_s, old_i, new_i, old_shot), (old_i, new_i, old_s, new_s, old_internal)):
                bindings.append({"key": "commit.materialization", "ref": before, "physical_ref": before,
                    "revision_id": image["revision_id"], "content_digest": image["content_digest"],
                    "policy": "fixed", "dependencies": [], "boundary": boundary,
                    "owner": "occurrence:foreign/shot" if forged_successor and request["label"] == "second" else "occurrence:" + occurrence_id + "/shot",
                    "successor": after, "edge_before": edge_before, "edge_after": edge_after})
            record = {"ordinal": 0, "command": call, "bindings": bindings,
                      "writes": [{"ref": old_i, "path": claim["path"], "before": claim["before"],
                                  "after": {"state": "present", "value": claim["value"]}}],
                      "reads": [], "selections": [], "created": [], "dependencies": [], "derived_writes": []}
            value = {"expected_head": head, "canonical_document": document, "document_digest": digest(document),
                     "records": {"schema_version": 1, "commands": [record], "undo_of": [], "restored_from": None,
                                 "label": request["label"], "merge_mode": "fields", "steps": [{
                                     "id": "edit", "label": request["label"], "intent": "", "tags": [],
                                     "command_ordinals": [0], "patch": effects, "dependencies": []}]},
                     "id_map": {}, "semantic_events": [], "provider_version": "prepared-auth-1", "compiler_version": "fixture-1"}
            return port.accept(value)

        runtime.register_timeline_commit_provider(port_tests.PreparedProvider(execute))
        first = None
        for label, field, value in (("first", "meta", {"org.example.timeline": {"note": "first"}}), ("second", "registry", {"assets": {}})):
            initial = next(row for row in original["internal_timeline_revisions"] if "internal-revision:" + row["revision_id"] == original_ref)
            assert initial is not None
            change = {"op": "set", "ref": original_ref, "path": [field], "value": value,
                      "before": {"state": "present", "value": initial["payload"][field]} if field in initial["payload"] else {"state": "absent"}}
            submitted = {"api_version": 1, "project_id": project, "timeline_id": "main",
                "base_revision_id": base["revision_id"], "base_publication_id": base["publication_id"],
                "label": label, "merge": "fields", "reads": [], "commands": [{
                    "schema_version": 1, "op": "doc.patch", "version": "1", "select": None, "args": {"changes": [change]}}]}
            def publish(submitted=submitted, label=label):
                return runtime.commit_timeline(project, "main", submitted, idempotency_key=label, publisher="editor",
                                               invocation_path=route_path(project, "main"), authorize=lambda: None)
            if label == "second" and forged_successor:
                before = rows(runtime)
                with pytest.raises(RuntimeErrorBase) as error:
                    publish()
                assert error.value.details is not None and error.value.details["reason"] == "invalid_records"
                assert rows(runtime) == before
            else:
                result = publish()
                assert result["data"]["status"] == ("accepted" if first is None else "merged")
                assert publish() == result
                first = result
    finally:
        runtime.close()
