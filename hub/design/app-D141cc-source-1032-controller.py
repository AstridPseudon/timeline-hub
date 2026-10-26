"""Private, harmless custody-control model for D141cc.

This module deliberately models the supported submit-owner procedure without
calling a service, a test runner, a process manager, or the production builder.
The fake service records request calls so the controls can prove that recovery
adopts an existing request instead of issuing a second normal request.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
import hashlib
import json
import sys


class CustodyError(RuntimeError):
    """A finite custody failure; the selector must stop, not retry."""


class DiskStop(CustodyError):
    """The exact request reached the standing disk stop."""

    def __init__(self, request_id: str, available_bytes: int) -> None:
        super().__init__(f"disk stop for {request_id}: {available_bytes} bytes")
        self.request_id = request_id
        self.available_bytes = available_bytes


class RequestStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


SOURCE_TUPLE = {
    "app": {"sha": "82e9e13ddf1d7ec6c736521b2eb091dca9877598", "tree": "6a6e49eb4461b5ca1a7fa1247653bc794f26d710", "checkout": "/home/user/work/wt/app-pin-82e9e13d"},
    "agent": {"sha": "ecdc242ed9b673f641759ecf029f95e89a2c6f92", "tree": "d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735", "checkout": "/home/user/work/wt/agt-pin-ecdc242e"},
    "runtime": {"sha": "95d98f038320d5d46bd679ac000ab3e15825c935", "tree": "78df31d62c5b9ba4c84dee4ea346e43a767718c1", "checkout": "/home/user/work/wt/rt-pin-95d98f03"},
    "composition": {"sha": "635f4de06fda22a85fc2e4cfc764d0153a4c9f40", "tree": "5ab5191a296980a0a6bcd1178ab6902d6478a148", "checkout": "/home/user/work/wt/vw-pin-635f4de0"},
}

BUILDER_SHA256 = "2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f"
BUILDER_BLOB = "59b65214bc74c1ca118b097bc3b13c0ffe480a93"
TARGET = "app-pin-82e9e13d"
STOP_BYTES = 4_000_000_000

SELECTORS = (
    "p2-automatic-child-placement",
    "p2-popup-add",
    "p2-parent-move",
    "p2-transition-none-single",
    "p2-transition-none-bulk",
    "p2-register-asset",
    "p1",
    "p3",
)

# These are the source-publication hashes from the unchanged pure builder.
# They are conservation anchors, not reconstructed command or row contents.
SOURCE_HASHES = {
    "p2-automatic-child-placement": ("ee68699ee18022ce9e77c40173fb85db2112204bc7d3df6b705edde3211ecedb", "cf48fac96e4f97bd7c1646a11b01edfa0aa269c9cee772fc90bcebc19a7cf934"),
    "p2-popup-add": ("27fcd174df3f214502bbca1e67b0eb366c361c11e1f5ae5c0c48d7a987582501", "71efa748b4b2f84a054e411fd2d76161b096060447f6e82b1a70ffc08f6dcb09"),
    "p2-parent-move": ("c77b6a97e0807d43a2590624e3d47590a5e76d5ed5841f7f214f3aa9176c8f04", "ff98c12644fed8ba786a453ae49fde0ba7648160e8a2c1bf7ab75fc07d3c898d"),
    "p2-transition-none-single": ("00ee17b1b120f8907c537bb73879a6020f0f32aca9942a4402cb399d137b52ee", "f287fea597ca4fbe7c875b7678c92f3a27be08066712d8cb2be70bf1c474498b"),
    "p2-transition-none-bulk": ("b9dbc7f4f69d9bde52d84e8c96b50e0519c33245b4d2de304ca021740f609db3", "3636c3aec938363dd71350cafbce79434fa852463e7c2733fa30deaa4cb36bbd"),
    "p2-register-asset": ("06852ebd4ab501e51704f8df7d5709063a4e8a1d675b3c018eb39226f0ce2df8", "c5f318d16964e88df19e41544d5bf73920542ed138c587681e2771d15c015a0b"),
    "p1": ("513dd6421d52e745bb3ba54daaa79eb4c05cfa0d1bd464c27cb03997969245e6", "890320b6c6608fc53e356268bce7cb8890d144b8c4d8151cf2fc6dfc8c730db6"),
    "p3": ("8323d9cc07a099a8234f6b2fda34b1250b78f7df9ffcbcb8ab66ec2e3fd90cb4", "6ccf671ffe56b9fc5625317761f5e2a437be89d8d58ad77dca301c3fb610071f"),
}


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Recipe:
    selector: str
    attempt_scope: str = "original"
    target: str = TARGET
    source_digest: str = ""
    command_digest: str = ""
    row_digest: str = ""
    command_bytes: bytes = b""
    row_bytes: bytes = b""
    suite: str = ""
    preflight_suite: str = ""
    output_path: str = ""
    plan_path: str = ""
    environment: tuple[tuple[str, str], ...] = ()


def _source_digest() -> str:
    return _digest(json.dumps(SOURCE_TUPLE, sort_keys=True, separators=(",", ":")))


def production_recipe(selector: str, attempt_scope: str = "original") -> Recipe:
    """Return the exact-shape recipe produced by the unchanged source builder.

    The attempt scope is private controller metadata.  It changes only the
    unique suite/output/plan namespace for an explicitly authorized retry;
    command/spec/source tuple inputs remain conserved.
    """

    if selector not in SELECTORS:
        raise ValueError(f"unknown selector: {selector}")
    if not attempt_scope or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for ch in attempt_scope):
        raise ValueError("invalid attempt scope")
    normal_suffix = f"-{attempt_scope}" if attempt_scope != "original" else ""
    suite = f"full-d141-{selector}-82e9e13d-submit{normal_suffix}"
    preflight_suite = f"{suite}-preflight"
    command_bytes = f"production-command:{selector}".encode("utf-8")
    row_bytes = f"production-row:{selector}:{suite}\n".encode("utf-8")
    original_command, original_row = SOURCE_HASHES[selector]
    command_digest = original_command if attempt_scope == "original" else _digest(command_bytes.decode())
    row_digest = original_row if attempt_scope == "original" else _digest(row_bytes.decode())
    environment = tuple(
        (f"D66_{name}_{part}", SOURCE_TUPLE[name.lower()][part.lower()])
        for name in ("APP", "AGENT", "RUNTIME", "COMPOSITION")
        for part in ("SHA", "TREE", "CHECKOUT")
    )
    root = f"/private/controller/full-d141/{suite}"
    return Recipe(
        selector=selector,
        attempt_scope=attempt_scope,
        source_digest=_source_digest(),
        command_digest=command_digest,
        row_digest=row_digest,
        command_bytes=command_bytes,
        row_bytes=row_bytes,
        suite=suite,
        preflight_suite=preflight_suite,
        output_path=f"{root}/output",
        plan_path=f"{root}/submit-plan.json",
        environment=environment,
    )


@dataclass
class Request:
    request_id: str
    phase: str
    status: RequestStatus
    recipe: Recipe
    owner: str
    artifact_digest: str
    body_calls: int = 0


@dataclass
class Artifact:
    recipe: Recipe
    owner: str
    preflight_id: str | None = None
    normal_id: str | None = None
    durable: bool = False
    immutable_digest: str = ""


@dataclass
class ArtifactStore:
    records: dict[str, Artifact] = field(default_factory=dict)
    fail_next_normal_persist: bool = False

    def persist(self, artifact: Artifact, phase: str) -> None:
        if phase == "normal" and self.fail_next_normal_persist:
            self.fail_next_normal_persist = False
            raise CustodyError("normal request exists before artifact is durable")
        artifact.durable = True
        self.records[artifact.recipe.suite] = artifact

    def get(self, recipe: Recipe) -> Artifact | None:
        return self.records.get(recipe.suite)


class FakeService:
    """No-op service double with authoritative request records."""

    def __init__(self) -> None:
        self.requests: dict[str, Request] = {}
        self.preflight_calls = 0
        self.normal_calls = 0
        self.body_calls = 0
        self._counter = 0

    def _new_id(self, phase: str) -> str:
        self._counter += 1
        return f"stub-{phase}-{self._counter}"

    def create_preflight(self, recipe: Recipe, owner: str) -> Request:
        self.preflight_calls += 1
        request = Request(self._new_id("preflight"), "preflight", RequestStatus.COMPLETED, recipe, owner, _digest(recipe.preflight_suite))
        self.requests[request.request_id] = request
        return request

    def create_normal(self, recipe: Recipe, owner: str) -> Request:
        self.normal_calls += 1
        request = Request(self._new_id("normal"), "normal", RequestStatus.QUEUED, recipe, owner, _digest(recipe.suite))
        self.requests[request.request_id] = request
        return request

    def run_body_once(self, request_id: str) -> None:
        request = self.requests[request_id]
        if request.body_calls:
            raise CustodyError(f"duplicate body call for {request_id}")
        request.body_calls += 1
        self.body_calls += 1
        request.status = RequestStatus.COMPLETED

    def same_target_suite(self, recipe: Recipe) -> list[Request]:
        return [
            request
            for request in self.requests.values()
            if request.recipe.target == recipe.target and request.recipe.suite == recipe.suite
        ]

    def exact_candidates(self, recipe: Recipe, phase: str) -> list[Request]:
        return [
            request
            for request in self.same_target_suite(recipe)
            if request.phase == phase
            and request.recipe.source_digest == recipe.source_digest
            and request.recipe.command_bytes == recipe.command_bytes
            and request.recipe.row_bytes == recipe.row_bytes
        ]


class SubmitOwnerController:
    """One selector owner; recovery inspects authoritative state first."""

    def __init__(self, service: FakeService, store: ArtifactStore, owner: str) -> None:
        self.service = service
        self.store = store
        self.owner = owner

    def _validate_recipe(self, recipe: Recipe) -> None:
        if recipe.target != TARGET or recipe.source_digest != _source_digest():
            raise CustodyError("source or target binding mismatch")
        if recipe.output_path == "" or recipe.plan_path == "":
            raise CustodyError("missing unique artifact paths")
        if len({recipe.suite, recipe.preflight_suite, recipe.output_path, recipe.plan_path}) != 4:
            raise CustodyError("non-unique suite/output/plan namespace")

    def _inspect(self, recipe: Recipe) -> tuple[Artifact | None, Request | None, Request | None]:
        self._validate_recipe(recipe)
        existing = self.store.get(recipe)
        same = self.service.same_target_suite(recipe)
        if any(request.recipe.source_digest != recipe.source_digest for request in same):
            raise CustodyError("same target/suite has mismatched source")
        preflights = self.service.exact_candidates(recipe, "preflight")
        normals = self.service.exact_candidates(recipe, "normal")
        if len(preflights) > 1 or len(normals) > 1:
            raise CustodyError("multiple exact request candidates")
        preflight = preflights[0] if preflights else None
        normal = normals[0] if normals else None
        if existing is not None:
            if existing.owner != self.owner and existing.normal_id is None:
                raise CustodyError("live or unknown submit owner; cannot prove death")
            if existing.normal_id and (normal is None or normal.request_id != existing.normal_id):
                raise CustodyError("artifact normal ID is not authoritative")
            if existing.preflight_id and (preflight is None or preflight.request_id != existing.preflight_id):
                raise CustodyError("artifact preflight ID is not authoritative")
        return existing, preflight, normal

    def recover_or_adopt(self, recipe: Recipe) -> dict[str, object]:
        artifact, preflight, normal = self._inspect(recipe)
        if normal is not None:
            return {
                "action": "adopt",
                "request_id": normal.request_id,
                "status": normal.status.value,
                "current_proof": normal.status != RequestStatus.CANCELLED,
                "owner": normal.owner,
            }
        if preflight is not None:
            if preflight.owner != self.owner:
                raise CustodyError("preflight-only artifact belongs to another unproven owner")
            if artifact is None:
                raise CustodyError("preflight exists without durable artifact")
            normal = self._create_normal(recipe, artifact)
            return {"action": "created-after-resume", "request_id": normal.request_id, "status": normal.status.value, "current_proof": True, "owner": self.owner}
        if artifact is not None:
            raise CustodyError("artifact exists without an authentic request")
        artifact = Artifact(recipe, self.owner, immutable_digest=_digest(recipe.suite))
        preflight = self.service.create_preflight(recipe, self.owner)
        artifact.preflight_id = preflight.request_id
        self.store.persist(artifact, "preflight")
        normal = self._create_normal(recipe, artifact)
        return {"action": "created", "request_id": normal.request_id, "status": normal.status.value, "current_proof": True, "owner": self.owner}

    def _create_normal(self, recipe: Recipe, artifact: Artifact) -> Request:
        normal = self.service.create_normal(recipe, self.owner)
        artifact.normal_id = normal.request_id
        self.store.persist(artifact, "normal")
        return normal

    def disk_guard(self, request_id: str, available_bytes: int) -> None:
        if available_bytes <= STOP_BYTES:
            raise DiskStop(request_id, available_bytes)


def _expect_error(action, text: str) -> CustodyError:
    try:
        action()
    except CustodyError as error:
        if text not in str(error):
            raise AssertionError(f"wrong error: {error}") from error
        return error
    raise AssertionError(f"expected CustodyError containing {text!r}")


def _fresh(selector: str = "p2-parent-move", attempt_scope: str = "original") -> tuple[Recipe, FakeService, ArtifactStore]:
    return production_recipe(selector, attempt_scope), FakeService(), ArtifactStore()


def scenario_corrected_initial() -> None:
    recipe, service, store = _fresh()
    result = SubmitOwnerController(service, store, "owner-A").recover_or_adopt(recipe)
    assert result["action"] == "created"
    assert service.preflight_calls == service.normal_calls == 1
    assert store.get(recipe).durable is True


def scenario_live_preflight_owner() -> None:
    recipe, service, store = _fresh()
    preflight = service.create_preflight(recipe, "owner-A")
    artifact = Artifact(recipe, "owner-A", preflight_id=preflight.request_id, immutable_digest=_digest(recipe.suite))
    store.persist(artifact, "preflight")
    _expect_error(lambda: SubmitOwnerController(service, store, "owner-B").recover_or_adopt(recipe), "cannot prove death")
    resumed = SubmitOwnerController(service, store, "owner-A").recover_or_adopt(recipe)
    assert resumed["action"] == "created-after-resume" and service.normal_calls == 1


def scenario_normal_before_artifact_durable() -> None:
    recipe, service, store = _fresh()
    store.fail_next_normal_persist = True
    controller = SubmitOwnerController(service, store, "owner-A")
    _expect_error(lambda: controller.recover_or_adopt(recipe), "before artifact is durable")
    adopted = SubmitOwnerController(service, store, "owner-B").recover_or_adopt(recipe)
    assert adopted["action"] == "adopt" and service.normal_calls == 1


def scenario_session_resume_vs_new_invocation() -> None:
    recipe, service, store = _fresh()
    preflight = service.create_preflight(recipe, "owner-A")
    artifact = Artifact(recipe, "owner-A", preflight_id=preflight.request_id, immutable_digest=_digest(recipe.suite))
    store.persist(artifact, "preflight")
    resumed = SubmitOwnerController(service, store, "owner-A").recover_or_adopt(recipe)
    assert resumed["action"] == "created-after-resume"
    adopted = SubmitOwnerController(service, store, "owner-B").recover_or_adopt(recipe)
    assert adopted["action"] == "adopt" and service.normal_calls == 1


def scenario_adopt_statuses() -> None:
    for status in RequestStatus:
        recipe, service, store = _fresh(attempt_scope=f"status-{status.value}")
        request = service.create_normal(recipe, "owner-A")
        request.status = status
        result = SubmitOwnerController(service, store, "owner-B").recover_or_adopt(recipe)
        assert result["action"] == "adopt" and result["status"] == status.value
        assert result["current_proof"] is (status != RequestStatus.CANCELLED)


def scenario_reject_multiple_and_mismatched_source() -> None:
    recipe, service, store = _fresh(attempt_scope="ambiguous")
    service.create_normal(recipe, "owner-A")
    service.create_normal(recipe, "owner-A")
    _expect_error(lambda: SubmitOwnerController(service, store, "owner-B").recover_or_adopt(recipe), "multiple exact")
    recipe2, service2, store2 = _fresh(attempt_scope="mismatch")
    bad = Recipe(**{**recipe2.__dict__, "source_digest": "wrong-source"})
    service2.create_normal(bad, "owner-A")
    _expect_error(lambda: SubmitOwnerController(service2, store2, "owner-B").recover_or_adopt(recipe2), "mismatched source")


def scenario_cancelled_old_attempt() -> None:
    old_recipe, service, store = _fresh("p2-popup-add", "original-cancelled")
    old_request = service.create_normal(old_recipe, "old-owner")
    old_request.status = RequestStatus.CANCELLED
    new_recipe = production_recipe("p2-popup-add", "popup-retry-1")
    result = SubmitOwnerController(service, store, "new-owner").recover_or_adopt(new_recipe)
    assert result["action"] == "created" and service.normal_calls == 2
    assert result["request_id"] != old_request.request_id
    assert old_request.status == RequestStatus.CANCELLED


def scenario_independent_selector_faults() -> None:
    outcomes: dict[str, str] = {}
    for selector in ("p2-parent-move", "p2-transition-none-single", "p2-transition-none-bulk"):
        recipe, service, store = _fresh(selector)
        if selector == "p2-transition-none-single":
            service.create_preflight(recipe, "foreign-owner")
            outcomes[selector] = _expect_error(lambda: SubmitOwnerController(service, store, "owner-A").recover_or_adopt(recipe), "preflight-only").__class__.__name__
        else:
            outcomes[selector] = str(SubmitOwnerController(service, store, "owner-A").recover_or_adopt(recipe)["action"])
    assert outcomes == {"p2-parent-move": "created", "p2-transition-none-single": "CustodyError", "p2-transition-none-bulk": "created"}


def scenario_disk_stop_exact_id() -> None:
    recipe, service, store = _fresh()
    result = SubmitOwnerController(service, store, "owner-A").recover_or_adopt(recipe)
    request_id = str(result["request_id"])
    error = _expect_error(lambda: SubmitOwnerController(service, store, "owner-A").disk_guard(request_id, STOP_BYTES), "disk stop")
    assert isinstance(error, DiskStop) and error.request_id == request_id


def scenario_original_overlap_is_failure() -> None:
    recipe, service, _store = _fresh("p2-popup-add", "original-overlap")
    first = service.create_normal(recipe, "owner-A")
    second = service.create_normal(recipe, "owner-B")
    assert first.request_id != second.request_id and service.normal_calls == 2
    # This is the proved old failure shape: two invocations each made one call.
    if service.normal_calls != 1:
        return
    raise AssertionError("overlap control failed to expose duplicate normal request")


def scenario_no_duplicate_submit_or_body_calls() -> None:
    recipe, service, store = _fresh("p2-register-asset")
    first = SubmitOwnerController(service, store, "owner-A").recover_or_adopt(recipe)
    service.run_body_once(str(first["request_id"]))
    for owner in ("owner-B", "owner-C", "owner-D"):
        adopted = SubmitOwnerController(service, store, owner).recover_or_adopt(recipe)
        assert adopted["request_id"] == first["request_id"]
    assert service.preflight_calls == 1 and service.normal_calls == 1 and service.body_calls == 1


def conservation_checks() -> None:
    for selector in SELECTORS:
        recipe = production_recipe(selector)
        assert recipe.source_digest == _source_digest()
        assert (recipe.command_digest, recipe.row_digest) == SOURCE_HASHES[selector]
        assert len(recipe.environment) == 12
        assert recipe.suite.startswith("full-d141-")
        assert recipe.preflight_suite == f"{recipe.suite}-preflight"
    retry = production_recipe("p2-popup-add", "popup-retry-1")
    assert retry.suite != production_recipe("p2-popup-add").suite
    assert retry.output_path != production_recipe("p2-popup-add").output_path
    assert retry.plan_path != production_recipe("p2-popup-add").plan_path


def run_all() -> list[str]:
    checks = [
        conservation_checks,
        scenario_corrected_initial,
        scenario_live_preflight_owner,
        scenario_normal_before_artifact_durable,
        scenario_session_resume_vs_new_invocation,
        scenario_adopt_statuses,
        scenario_reject_multiple_and_mismatched_source,
        scenario_cancelled_old_attempt,
        scenario_independent_selector_faults,
        scenario_disk_stop_exact_id,
        scenario_original_overlap_is_failure,
        scenario_no_duplicate_submit_or_body_calls,
    ]
    for check in checks:
        check()
    return [check.__name__ for check in checks]


if __name__ == "__main__":
    if sys.argv[1:] != ["--self-test"]:
        raise SystemExit("usage: controller.py --self-test")
    print(json.dumps({"status": "PASS", "checks": run_all()}, sort_keys=True))
