"""Gate 6: task effects have artifact authority, never canonical edit authority."""
from __future__ import annotations

import copy
import pytest

from http_helpers import Api
from runtime_protocol import service as service_module
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.errors import ValidationError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.util import canonical_json
from tests.test_generation_publish_v1_settlement import _effect as publish_effect
from tests.test_generation_publish_v1_settlement import _output as publish_output
from tests.test_generation_thumbnail_settlement import (
    CAPABILITY as GENERATION,
    _create_effect,
    _seed_generation,
    _thumbnail,
)
from tests.test_generation_variant_append_settlement import _output
from tests.test_runtime_child_delegation import (
    CHILD, IDENTITY, OTHER, PARENT, authority, digest, lease, load_task_spec, parent, store_task_spec,
)
from tests.test_timeline_commit_port import PreparedProvider


FORBIDDEN = ("timeline.update", "shot.update", "reference.update", "shot.text_binding.set")
ADMISSION_GAP = (
    "M2 commit-contract §5 requires unknown/canonical effects to refuse before admission; "
    "current create_task only validates publish_v1 and thumbnail.attach"
)


def _no_scene(*args, **kwargs):
    pytest.fail("task effects must not evaluate a scene")


def _seed(service):
    for capability in (PARENT, CHILD, OTHER, GENERATION):
        service.register_capability({"capability_id": capability, "definition_digest": digest(capability)})
    service.register_executor(
        {"executor_id": "worker", "capabilities": [PARENT, CHILD, OTHER, GENERATION], "max_concurrency": 64},
        idempotency_key="executor",
    )
    project = service.create_project({"slug": "effect-authority", "name": "Effect authority"})
    service.register_timeline_commit_provider(PreparedProvider())
    service.create_timeline(project["id"], "main", idempotency_key="bootstrap")
    # Real API-created unused resources, with their original receipts. No film
    # history or accepted command records are synthesized for these fixtures.
    service.create_project_shot(project["id"], {"shot_id": "shot", "name": "Unused shot"}, idempotency_key="shot")
    media = service.ingest(project["id"], b"reference", idempotency_key="reference-media")["data"]["object_id"]
    service.create_project_reference(project["id"], {
        "reference_id": "reference", "kind": "other", "name": "Unused reference", "media_id": media,
    }, idempotency_key="reference")
    binding = service.set_project_shot_text_binding(project["id"], {
        "shot_id": "shot", "kind": "transcript", "text": "Original text", "expected_head": 0,
    }, idempotency_key="binding")["data"]
    return project, binding["binding_id"]


@pytest.fixture(params=["service", "http"])
def boundary(request, tmp_path, monkeypatch):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    daemon = RuntimeDaemon(root, support_root=tmp_path / "support").start() if request.param == "http" else None
    service = daemon.service if daemon else RuntimeService(root)
    try:
        monkeypatch.setattr(service_module, "evaluate_closure", _no_scene)
        project, binding = _seed(service)
        value = {"service": service, "project": project, "binding": binding}
        if daemon:
            token, _ = daemon.credentials.provision(
                "worker", ["worker:execute"], metadata={"execution_binding": IDENTITY["execution_binding"]},
            )
            value.update(owner=Api(daemon.endpoint, daemon.token), worker=Api(daemon.endpoint, token))
        yield value
    finally:
        if daemon:
            daemon.stop()
        else:
            service.close()


def _state(service, *, canonical_only=False):
    names = [row[0] for row in service.store.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    if canonical_only:
        names = [name for name in names if any(part in name for part in (
            "timeline", "shot", "reference", "composition", "document",
        ))]
    rows = {name: sorted((tuple(row) for row in service.store.conn.execute(f'SELECT * FROM "{name}"')), key=repr)
            for name in names}
    if canonical_only:
        return rows
    # Include task/admission/checkpoint/history/receipt/event/project sequence
    # tables as well as every existing CAS and staging file, byte for byte.
    files = {str(path.relative_to(service.store.root)): path.read_bytes()
             for root in (service.store.cas_root, service.store.staging_root)
             for path in root.rglob("*") if path.is_file()}
    return rows, files


def _effect(boundary, kind, *, fresh=False):
    target = {
        "timeline.update": "main", "shot.update": "shot", "reference.update": "reference",
        "shot.text_binding.set": boundary["binding"],
    }[kind]
    return {"effect_type": kind, "target_id": "fresh-" + target if fresh else target,
            "expected_version": 1, "payload": {"name": "Changed", "text": "Changed", "config": {"clips": []}}}


def _task_body(boundary, **fields):
    return {"project": boundary["project"]["id"], "capability_id": GENERATION,
            "capability_digest": digest(GENERATION), "input_object_ids": [], **fields}


def _admit(boundary, body, *, key="task"):
    if "owner" in boundary:
        return boundary["owner"].request("POST", "/v1/tasks", body, headers={"Idempotency-Key": key})["data"]
    return boundary["service"].create_task({**body, "idempotency_key": key}, enforce_readiness=True)


def _claim(boundary, *, capability=GENERATION, key="claim"):
    body = {"executor_id": "worker", "capability_ids": [capability],
            "runtime_epoch": boundary["service"].health()["runtime_epoch"]}
    if "worker" in boundary:
        return boundary["worker"].request("POST", "/v1/tasks/claim", body, headers={"Idempotency-Key": key})
    return boundary["service"].claim_next(body, idempotency_key=key, identity=IDENTITY)


def _settle(boundary, attempt, body, *, key="settle"):
    body = {**lease(attempt), **body}
    if "worker" in boundary:
        return boundary["worker"].request("POST", f"/v1/attempts/{attempt['attempt_id']}/settle", body,
                                          headers={"Idempotency-Key": key})
    return boundary["service"].settle_attempt(attempt["attempt_id"], body, idempotency_key=key, identity=IDENTITY)


def _authority(boundary, attempt):
    if "worker" in boundary:
        return boundary["worker"].request("POST", f"/v1/attempts/{attempt['attempt_id']}/child-authority", lease(attempt))
    return authority(boundary["service"], attempt)


def _delegate(boundary, receipt, task, *, key="child"):
    body = {"authority": receipt["authority"], "task": task}
    if "worker" in boundary:
        return boundary["worker"].request("POST", "/v1/delegated-tasks", body, headers={"Idempotency-Key": key})
    return boundary["service"].admit_delegated_child(body, idempotency_key=key, identity=IDENTITY)


def _assert_denied(boundary, action, *, match):
    before = _state(boundary["service"])
    error = None
    try:
        action()
    except (ValidationError, RuntimeError) as exc:
        error = exc
    assert _state(boundary["service"]) == before
    assert error is not None, "canonical effect was accepted"
    if isinstance(error, RuntimeError):
        assert error.status == 422
    assert match in str(error)


# These preserve the required refusal expectation. Admission currently writes
# task/run/receipt/event rows; settlement's closed dispatch does not excuse that
# §5 gap. No canonical execution escape has been found to authorize a writer fix.
@pytest.mark.xfail(strict=True, raises=AssertionError, reason=ADMISSION_GAP)
@pytest.mark.parametrize("kind", FORBIDDEN)
@pytest.mark.parametrize("fresh", [False, True], ids=["existing", "fresh"])
def test_canonical_effect_admission_is_zero_write(boundary, kind, fresh):
    effect = _effect(boundary, kind, fresh=fresh)
    _assert_denied(boundary, lambda: _admit(boundary, _task_body(boundary, settlement_effect=effect)), match="effect")


@pytest.mark.xfail(strict=True, raises=AssertionError, reason=ADMISSION_GAP)
@pytest.mark.parametrize("kind", FORBIDDEN)
def test_store_canonical_effect_admission_is_zero_write(boundary, kind):
    _assert_denied(boundary, lambda: boundary["service"].store.create_task(
        GENERATION, {}, project=boundary["project"]["id"], idempotency_key="store-task",
        expected_effect=_effect(boundary, kind), capability_digest=digest(GENERATION),
    ), match="effect")


def _final_policy(effect):
    capability = {"capability_id": CHILD, "capability_digest": digest(CHILD)}
    return {"capabilities": [capability], "targets": [{"kind": "default"}], "input_object_ids": [],
            "stages": [{"name": "verify", **capability, "target": {"kind": "default"}, "inputs": []},
                       {"name": "publish", **capability, "target": {"kind": "default"},
                        "inputs": [{"name": "verified", "producer_stage": "verify", "output_port": "video"}]}],
            "final_publication": {"stage": "publish", "verify_stage": "verify", "verify_output_port": "video", "effect": effect}}


@pytest.mark.parametrize("kind", FORBIDDEN)
def test_final_publication_cannot_declare_a_canonical_effect(boundary, kind):
    body = _task_body(boundary, child_delegation=_final_policy(_effect(boundary, kind)))
    _assert_denied(boundary, lambda: _admit(boundary, body), match="final publication requires generation.publish_v1")


@pytest.mark.parametrize("field", ["settlement_effect", "child_delegation", "spec"])
@pytest.mark.parametrize("kind", FORBIDDEN)
def test_delegated_admission_cannot_add_effects_or_redelegate(boundary, field, kind):
    service, project = boundary["service"], boundary["project"]["id"]
    # Use main's live parent/authority fixtures, including its signed policy.
    attempt = parent((service, project))
    receipt = _authority(boundary, attempt)
    policy = _final_policy(_effect(boundary, kind))
    task = {"capability_id": CHILD, "capability_digest": digest(CHILD),
            field: _effect(boundary, kind) if field == "settlement_effect" else
            {"child_delegation": policy} if field == "spec" else policy}
    _assert_denied(boundary, lambda: _delegate(boundary, receipt, task),
                   match="fields" if field != "spec" else "delegation fields")


@pytest.mark.parametrize("kind", FORBIDDEN)
def test_corrupted_stored_final_policy_is_revalidated_before_child_admission(boundary, kind):
    service, project = boundary["service"], boundary["project"]["id"]
    attempt = parent((service, project))
    receipt = _authority(boundary, attempt)
    # Controlled fixture corruption, not a historically admitted final policy.
    spec = load_task_spec(service, attempt["task_id"])
    spec["child_delegation"] = _final_policy(_effect(boundary, kind))
    store_task_spec(service, attempt["task_id"], spec)
    task = {"capability_id": CHILD, "capability_digest": digest(CHILD), "stage": "verify", "input_refs": []}
    _assert_denied(boundary, lambda: _delegate(boundary, receipt, task),
                   match="final publication requires generation.publish_v1")


@pytest.mark.parametrize("kind", FORBIDDEN)
@pytest.mark.parametrize("stored_forbidden", [False, True], ids=["undeclared", "corrupted-stored-fixture"])
def test_existing_attempt_cannot_settle_a_canonical_effect(boundary, kind, stored_forbidden):
    _admit(boundary, _task_body(boundary))
    attempt = _claim(boundary)
    effect = _effect(boundary, kind)
    if stored_forbidden:
        # Controlled fixture corruption models an old/foreign stored effect.
        # This is NOT evidence of genuine historical admission or film history.
        boundary["service"].store.conn.execute("UPDATE tasks SET expected_effect_json=? WHERE id=?",
                                              (canonical_json(effect), attempt["task_id"]))
    _assert_denied(boundary, lambda: _settle(boundary, attempt, {
        "effect": effect, "outputs": [_output(b"must-not-publish")],
    }), match="unsupported settlement effect_type" if stored_forbidden else "not predeclared")


@pytest.mark.parametrize("kind", FORBIDDEN)
@pytest.mark.parametrize("primitive", ["validate", "apply", "settle"])
def test_store_dispatch_refuses_canonical_effect_before_callbacks(boundary, kind, primitive):
    service = boundary["service"]
    effect = _effect(boundary, kind)
    _admit(boundary, _task_body(boundary))
    attempt = _claim(boundary)
    # Controlled stored-effect corruption; no fabricated acceptance receipt.
    service.store.conn.execute("UPDATE tasks SET expected_effect_json=? WHERE id=?",
                               (canonical_json(effect), attempt["task_id"]))
    callbacks = []
    def apply():
        if primitive == "validate":
            return service.store._validate_settlement_effect(effect, project_id=boundary["project"]["id"])
        if primitive == "apply":
            return service.store._apply_settlement_effect(effect, project_id=boundary["project"]["id"])
        return service.store._settle_attempt(
            attempt["task_id"], attempt["lease_id"], {"outputs": [_output(b"store-output")]},
            effect=effect, fence=attempt["fence"], attempt_id=attempt["attempt_id"],
            publish=lambda: callbacks.append("publish"), record=lambda *a, **k: callbacks.append("record"),
        )
    _assert_denied(boundary, apply, match="unsupported settlement effect_type")
    assert callbacks == []


@pytest.mark.parametrize("kind", ["generation.publish_v1", "generation.create_with_variant",
                                  "generation.variant.append", "generation.thumbnail.attach", "project.update", None])
def test_bounded_effects_preserve_canonical_state_and_opaque_data(boundary, kind):
    service, project = boundary["service"], boundary["project"]
    canonical = _state(service, canonical_only=True)
    opaque = {"example.org/editor/v1": {"effect_type": "timeline.update", "shot_id": "shot",
                                       "final_publication": {"effect": _effect(boundary, "reference.update")}}}
    effect, inputs = None, []
    outputs = [_output(b"ordinary-artifact")]
    if kind == "project.update":
        effect = {"effect_type": kind, "target_id": project["id"], "expected_version": project["version"],
                  "payload": {"name": "timeline.update is an innocuous name", "metadata": opaque}}
    elif kind == "generation.publish_v1":
        effect = publish_effect(project["id"], groups=[{"group_key": "main", "selectors": [
            {"selector": "one", "ordinal": 0, "variant_key": "original", "output_port": "video"},
        ]}])
        effect["payload"]["metadata"] = opaque
        outputs = [publish_output(b"published-video", output_port="video", group_key="main", variant_key="original", ordinal=0)]
    elif kind == "generation.create_with_variant":
        effect = _create_effect(project["id"], metadata=opaque)
        inputs = [service.ingest(project["id"], b"creation-input", idempotency_key="creation-input")["data"]["object_id"]]
        outputs = [{**_output(b"created-video", name="video"), "media_type": "video/mp4"}]
    elif kind in {"generation.variant.append", "generation.thumbnail.attach"}:
        seed = _seed_generation(service, project, key="seed", with_thumbnail=False)
        inputs = [seed["source_object_id"]]
        effect = {"effect_type": kind, "target_id": seed["generation_id"], "expected_version": 1}
        if kind == "generation.variant.append":
            effect["payload"] = {"source_variant_id": seed["variant_id"], "source_object_id": inputs[0],
                                 "variant_type": "edited", "output_name": "video", "output_ordinal": 0,
                                 "primary_policy": "preserve"}
            outputs = [{**_output(b"appended-video", name="video"), "media_type": "video/mp4"}]
        else:
            effect["payload"] = {"source_object_id": inputs[0], "output_name": "thumbnail.jpg",
                                 "output_ordinal": 0, "recipe_version": 1}
            outputs = [_thumbnail(b"thumbnail-jpeg", inputs)]
    _admit(boundary, _task_body(boundary, settlement_effect=effect, input_object_ids=inputs,
                               spec={"params": opaque}, generation_intent=copy.deepcopy(opaque)))
    attempt = _claim(boundary)
    body = {"outputs": outputs, "result": opaque}
    if effect is not None:
        body["effect"] = effect
    settled = _settle(boundary, attempt, body)
    assert _settle(boundary, attempt, body) == settled
    assert settled["data"]["state"] == "succeeded"
    assert settled["data"]["result"]["example.org/editor/v1"] == opaque["example.org/editor/v1"]
    assert service.cas.path_for(outputs[0]["digest"].removeprefix("sha256:")).exists()
    assert service.managed_outputs(attempt["task_id"])
    assert _state(service, canonical_only=True) == canonical
    if kind == "project.update":
        assert service.store.get_project(project["id"])["metadata"] == opaque
    elif kind is not None:
        result_key = {"generation.publish_v1": "generation_publish_v1",
                      "generation.thumbnail.attach": "generation_thumbnail"}.get(kind, "generation_variant")
        assert settled["data"]["result"][result_key]


def test_delegated_verified_final_publication_only_stores_artifacts(boundary):
    service, project = boundary["service"], boundary["project"]["id"]
    canonical = _state(service, canonical_only=True)
    effect = publish_effect(project, groups=[{"group_key": "main", "selectors": [
        {"selector": "verified", "ordinal": 0, "variant_key": "original", "output_port": "video"},
    ]}])
    _admit(boundary, _task_body(boundary, capability_id=PARENT, capability_digest=digest(PARENT),
                               child_delegation=_final_policy(effect)))
    root = _claim(boundary, capability=PARENT)
    receipt = _authority(boundary, root)
    _delegate(boundary, receipt, {"capability_id": CHILD, "capability_digest": digest(CHILD),
                                  "stage": "verify", "input_refs": []}, key="verify")
    verify = _claim(boundary, capability=CHILD, key="claim-verify")
    output = publish_output(b"verified-video", output_port="video", group_key="main", variant_key="original", ordinal=0)
    _settle(boundary, verify, {"outputs": [output]}, key="settle-verify")
    association = service.managed_outputs(verify["task_id"])[0]
    _delegate(boundary, receipt, {"capability_id": CHILD, "capability_digest": digest(CHILD), "stage": "publish",
                                  "input_refs": [{"name": "verified", "producer_task_id": verify["task_id"],
                                                  "association_id": association["association_id"], "output_port": "video"}]},
              key="publish")
    publish = _claim(boundary, capability=CHILD, key="claim-publish")
    assert publish["expected_effect"] == effect
    settled = _settle(boundary, publish, {"effect": effect, "outputs": [output]}, key="settle-publish")
    assert settled["data"]["result"]["generation_publish_v1"]["publications"]
    _settle(boundary, root, {"outputs": []}, key="settle-root")
    assert service.task(root["task_id"])["task"]["status"] == "completed"
    assert _state(service, canonical_only=True) == canonical
