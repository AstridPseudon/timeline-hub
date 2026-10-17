"""Authenticated COMMIT-scoped scene capability; Astrid owns wire and semantics."""

from __future__ import annotations

import base64
import copy
import dataclasses
import hashlib
import threading
import uuid

from .errors import AuthorizationError, ConflictError, ValidationError
from .timeline_commit import digest, _publisher


def _session(principal):
    grant = principal.get("_paired_session")
    if grant is not None:
        return digest(
            {
                k: getattr(grant, k)
                for k in (
                    "pair_id",
                    "connector_id",
                    "generation",
                    "realm_id",
                    "actor",
                    "credential_binding",
                    "project_id",
                    "handle",
                )
            }
        )
    binding = principal.get("_credential_binding")
    if not isinstance(binding, str) or not binding:
        raise AuthorizationError(
            "scene evaluation requires a live authenticated session"
        )
    return digest({"actor": principal["actor"], "credential_binding": binding})


def check_binding(service, relay):
    from astrid.core.execution.authoring_scene_startup import provider_digest

    relay.check_live()
    c = relay.config.binding
    if (
        c["runtime_realm_id"] != service.realm["id"]
        or c["runtime_instance_id"] != service.runtime_instance_id
        or c["runtime_session_id"] != service.runtime_session_id
        or c["provider_digest"] != provider_digest()
    ):
        raise ConflictError("authoring Runtime/provider incarnation changed")
    executor = service.store.conn.execute(
        "SELECT * FROM executors WHERE id=?", (c["executor_id"],)
    ).fetchone()
    if (
        executor is None
        or executor["readiness"] != "ready"
        or not service.store._executor_live(executor)
        or executor["runtime_epoch"] != service.store._current_runtime_epoch()
        or executor["source_epoch"] != c["source_epoch"]
        or any(
            "sha256:" + str(executor[k]).removeprefix("sha256:") != c["executor_" + k]
            for k in ("source_digest", "dependency_digest")
        )
    ):
        raise ConflictError("authoring Host admission changed")
    descriptor = service.store._executor_capability(
        executor, "rendering.timeline_visualize"
    )
    if (
        not descriptor
        or descriptor.get("status", "ready") != "ready"
        or descriptor.get("definition_digest") != c["capability_digest"]
    ):
        raise ConflictError("authoring Host source changed")


class RequestSceneEvaluation:
    def __init__(self, service, request, principal):
        self.service, self.request, self.principal = (
            service,
            copy.deepcopy(request),
            principal,
        )
        self.request_hash = digest(request)
        self.session = _session(principal)
        with service.store._mutex:
            self._authority()
        self.selection = getattr(service, "_authoring_scene_selection", None)
        self.relay = getattr(service, "_authoring_scene_relay", None)
        if self.relay is None and self.selection is not None:
            self.relay = self.selection.resolve()
        self.context = (
            copy.deepcopy(self.relay.config.binding) if self.relay is not None else None
        )
        self.cancelled = threading.Event()
        self.fence = uuid.uuid4().hex
        self.proof = None
        self.dependencies = {}
        self.active = None

    def _authority(self):
        _publisher(self.principal, self.request.get("asserted_actor"))
        if (
            self.principal.get("execution_binding")
            or {"worker:execute", "worker:register"}
            & set(self.principal.get("scopes", []))
            and "admin" not in self.principal.get("scopes", [])
        ):
            raise AuthorizationError(
                "worker credentials cannot evaluate authoring scenes"
            )
        self.service._assert_commit_authority(
            self.principal, self.request["project_id"]
        )
        self.service._assert_mutation_admitted()
        project = self.service.store.get_project(self.request["project_id"])
        if (
            project["id"] != self.request["project_id"]
            or project["realm_id"] != self.service.realm["id"]
        ):
            raise AuthorizationError("foreign project")
        if "_credential_binding" in self.principal:
            issuer = self.service._task_credentials
            if issuer is None:
                raise AuthorizationError("caller credential issuer unavailable")
            issuer.validate_binding(
                self.principal["actor"],
                self.principal["_credential_binding"],
                "projects:write",
            )
        if (
            _session(self.principal) != self.session
            or digest(self.request) != self.request_hash
        ):
            raise AuthorizationError("scene invocation binding changed")

    def check(self):
        with self.service.store._mutex:
            if (
                self.cancelled.is_set()
                or self.relay is None
                or getattr(self.service, "_authoring_scene_relay", None)
                is not self.relay
            ):
                raise AuthorizationError("authoring invocation revoked or unavailable")
            if self.relay.config.binding != self.context:
                raise AuthorizationError("authoring source/owner changed")
            self._authority()
            if self.selection is not None:
                if (
                    getattr(self.service, "_authoring_scene_selection", None)
                    is not self.selection
                ):
                    raise AuthorizationError("selected authoring Host changed")
                self.selection.check()
            check_binding(self.service, self.relay)

    def check_dependencies(self):
        from astrid.core.execution import authoring_scene_protocol as wire

        if self.dependencies:
            if not {"objects:read", "admin"} & set(self.principal.get("scopes", [])):
                raise AuthorizationError("scene dependencies require objects:read")
            if "_credential_binding" in self.principal:
                self.service._task_credentials.validate_binding(
                    self.principal["actor"],
                    self.principal["_credential_binding"],
                    "objects:read",
                )
        for oid, captured in self.dependencies.items():
            self.service.object_location(self.request["project_id"], oid)
            metadata, stream = self.service.open_object(oid)
            with stream:
                raw = stream.read(wire.LIMIT + 1)
            if (
                len(raw) > wire.LIMIT
                or "sha256:" + hashlib.sha256(raw).hexdigest() != oid
                or metadata["media_type"] != captured
            ):
                raise ConflictError("scene dependency changed before acceptance")

    def evaluator(self, candidate):
        self.check()
        self.dependencies = {}
        self.proof = None  # A retry cannot consume the preceding candidate's proof.
        self.active = CandidateEvaluator(self, candidate)
        return self.active

    def accept(self, prepared):
        self.check()
        self.check_dependencies()
        if self.proof is None or self.proof != digest(
            prepared["result"]["canonical_document"]
        ):
            raise AuthorizationError(
                "acceptance requires this post-rebase candidate evaluation"
            )

    def close(self):
        self.cancelled.set()
        self.active = None
        self.proof = None


class CandidateEvaluator:
    def __init__(self, invocation, candidate):
        self.invocation = invocation
        self.candidate_digest = digest(candidate)
        self.binding = dict(
            invocation_id=uuid.uuid4().hex,
            actor=invocation.principal["actor"],
            actor_session=invocation.session,
            project_id=invocation.request["project_id"],
            timeline_id=invocation.request["timeline_id"],
            request_id=invocation.request["request_id"],
            request_hash=invocation.request_hash,
            candidate_digest=self.candidate_digest,
            fence=invocation.fence,
        )
        self.closed = False
        self.queries = 0

    def query_scene(self, *, revision_digest, scene, frames):
        from astrid.core.execution import authoring_scene_protocol as wire
        from astrid.core.execution.remotion_frame_owner import FrameOwnerError

        try:
            if self.closed or self.invocation.active is not self:
                raise FrameOwnerError("evaluation_closed")
            self.invocation.check()
            scene = copy.deepcopy(scene)
            if revision_digest != wire.digest(scene)[7:]:
                raise FrameOwnerError("scene_digest_mismatch")
            dependencies = {}
            service = self.invocation.service
            with service.store._mutex:
                for oid in wire.assets(scene):
                    # The candidate contributes immutable IDs, never a file path
                    # or URL. Runtime resolves only project-member CAS objects.
                    if not {"objects:read", "admin"} & set(
                        self.invocation.principal.get("scopes", [])
                    ):
                        raise AuthorizationError("scene assets require objects:read")
                    if "_credential_binding" in self.invocation.principal:
                        service._task_credentials.validate_binding(
                            self.invocation.principal["actor"],
                            self.invocation.principal["_credential_binding"],
                            "objects:read",
                        )
                    service.object_location(self.invocation.request["project_id"], oid)
                    metadata, stream = service.open_object(oid)
                    with stream:
                        raw = stream.read(wire.LIMIT + 1)
                    if (
                        len(raw) > wire.LIMIT
                        or "sha256:" + hashlib.sha256(raw).hexdigest() != oid
                    ):
                        raise ValidationError("scene dependency digest/size mismatch")
                    dependencies[oid] = dict(
                        media_type=metadata["media_type"],
                        bytes=base64.b64encode(raw).decode(),
                    )
                    self.invocation.dependencies[oid] = metadata["media_type"]
            request = dict(
                protocol=wire.PROTOCOL,
                operation=wire.OPERATION,
                purpose=wire.PURPOSE,
                context=copy.deepcopy(self.invocation.relay.config.binding),
                invocation=self.binding,
                scene_digest=wire.digest(scene),
                scene=scene,
                dependencies=dependencies,
                frames=list(frames),
            )
            result = self.invocation.relay.exchange(
                request,
                guard=self.invocation.check,
                cancelled=self.invocation.cancelled,
            )
            self.invocation.check()
            self.invocation.check_dependencies()
            if self.closed or self.invocation.active is not self:
                raise FrameOwnerError("evaluation_superseded")
            wire.validate_evaluation(result, list(frames))
            self.queries += 1
            return result
        except FrameOwnerError:
            raise
        except Exception as exc:
            raise FrameOwnerError("authoring_evaluation_refused") from exc

    def complete(self, *, empty=False):
        from astrid.core.execution.remotion_frame_owner import FrameOwnerError

        self.invocation.check()
        if (
            self.closed
            or self.invocation.active is not self
            or type(empty) is not bool
            or empty != (self.queries == 0)
        ):
            raise FrameOwnerError("evaluation_incomplete")
        self.invocation.proof = self.candidate_digest

    def close(self):
        self.closed = True


class SelectedHostScene:
    """Closed daemon composition from the launcher-owned retained Host handle."""

    def __init__(self, service, preparer, profile, handle):
        self.service, self.preparer, self.profile, self.handle = (
            service,
            preparer,
            profile,
            handle,
        )
        self.relay = None

    def check(self):
        if self.preparer.current_handle() is not self.handle or self.handle.closed:
            raise ConflictError("selected authoring Host lifecycle changed")
        report = self.preparer.report(self.handle)
        if report["owner_epoch"] != self.service.runtime_instance_id:
            raise ConflictError("selected Host Runtime incarnation changed")
        return report

    def resolve(self):
        import json
        import os
        from pathlib import Path
        from astrid.core.execution.authoring_scene_transport import (
            AuthoringSceneConfig,
            AuthoringSceneRelay,
            _actor,
        )
        from astrid.core.execution.storage_preparation_transport import (
            ProcessIdentity,
            _directory,
        )
        from astrid.core.execution import authoring_scene_protocol as wire
        from banodoco_local.custody_broker import AuthenticatedCleanupActor

        report = self.check()
        root = Path(self.profile.support_root)
        directory = _directory(root / "authoring-scene")
        try:
            fd = os.open(
                "ready.json",
                os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                dir_fd=directory,
            )
            try:
                raw = os.read(fd, wire.LIMIT + 1)
            finally:
                os.close(fd)
        finally:
            os.close(directory)
        record = json.loads(raw)
        if wire.encoded(record) + b"\n" != raw:
            raise ConflictError("noncanonical authoring startup record")
        host = ProcessIdentity(**record["host_peer"])
        host.matches(_actor(host).verify())
        if any(
            report["processes"]["host"][k] != getattr(host, k)
            for k in ("pid", "birth_id")
        ):
            raise ConflictError("authoring endpoint is not the retained selected Host")
        runtime = ProcessIdentity(**AuthenticatedCleanupActor.current().verify())
        if record["runtime_peer"] != dataclasses.asdict(runtime):
            raise ConflictError("authoring endpoint bound another Runtime")
        config = AuthoringSceneConfig(
            root, host, runtime, record["context"], record["boot_manifest_hash"]
        )
        if record != config.record or config.boot_manifest_hash != str(
            self.preparer.config["boot_manifest_hash"]
        ).removeprefix("sha256:"):
            raise ConflictError("authoring endpoint source boot differs")
        relay = AuthoringSceneRelay(config)
        check_binding(self.service, relay)
        self.relay = relay
        self.service._authoring_scene_relay = relay
        return relay
