"""Derive authoring ownership solely from accepted Host startup custody."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

from . import authoring_scene_protocol as wire
from . import custody_broker as custody
from .authoring_scene_transport import AuthoringSceneConfig
from .remotion_frame_owner import FrameOwnerError
from .storage_preparation_transport import ProcessIdentity
from astrid.core.rendering.remotion_runtime import _validation_timing


def provider_digest():
    from astrid.sdk.timeline import commit

    return "sha256:" + hashlib.sha256(Path(commit.__file__).read_bytes()).hexdigest()


@_validation_timing('authoring_renderer_binding')
def renderer_closure(host, environment):
    from astrid.packs.rendering.actions.timeline_visualize.composed_frame import (
        renderer_environment_identity,
    )

    project = Path(environment.get("ASTRID_REMOTION_PROJECT_DIR", ""))
    node = Path(environment.get("ASTRID_NODE_EXECUTABLE", ""))
    if (
        not project.is_absolute()
        or project.resolve(strict=True) != project
        or not node.is_absolute()
        or node.resolve(strict=True) != node
        or any(
            os.environ.get(k) != environment.get(k)
            for k in ("ASTRID_REMOTION_PROJECT_DIR", "ASTRID_NODE_EXECUTABLE")
        )
    ):
        raise FrameOwnerError("renderer_selection_unavailable")
    selected = getattr(host, "_host_renderer_selection", None)
    if selected is not None:
        from .host_renderer_selection import HostRendererSelection
        try:
            if type(selected) is not HostRendererSelection or selected.node.executable.path != node:
                raise ValueError("selected Node differs")
            selected.node.verify()
        except Exception as exc:
            raise FrameOwnerError("renderer_selection_unavailable") from exc
    if host._remotion_closure_binding is not None:
        host._remotion_closure_binding.validate(project)
    from .remotion_host_session import _file_identity

    selected = [
        _file_identity(p).sha256
        for p in (
            node,
            project / "src/astrid-frame-worker.mjs",
            (project / "node_modules/@remotion/cli/remotion-cli.js").resolve(strict=True),
        )
    ]
    return wire.digest([renderer_environment_identity(), selected])


@_validation_timing('authoring_host_binding')
def validate_host(host, config, environment):
    from .generic_host import (
        _admitted_source_roots,
        _canonical_digest,
        _capability_digest,
        _dependency_digest,
        _is_withdrawn,
        _verify_admitted_source,
    )

    c = config.binding
    runtime = host._registered_runtime_state
    record = host.capabilities.get("rendering.timeline_visualize")
    if (
        host._shutdown.is_set()
        or host._cleanup_uncertain
        or host.executor_id != c["executor_id"]
        or host.source_epoch != c["source_epoch"]
        or host.boot_manifest_hash != config.boot_manifest_hash
        or host.boot_manifest_path is None
        or not host.boot_manifest_path.is_relative_to(config.support_root)
        or host.boot_manifest_provenance()
        != {"kind": "astrid.boot_manifest", "sha256": config.boot_manifest_hash}
        or any(
            runtime.get(k) != c[k]
            for k in ("runtime_instance_id", "runtime_session_id", "source_epoch")
        )
        or record is None
        or record.approval_reason
        or _is_withdrawn(record)
        or not record.ready
        or "sha256:" + record.source_digest != c["source_digest"]
        or "sha256:" + record.dependency_digest != c["dependency_digest"]
        or _dependency_digest(record.definition, host.capabilities) != record.dependency_digest
        or _capability_digest(record.definition.to_dict()) != record.capability_digest
        or record.capability_digest != c["capability_digest"]
        or "sha256:" + _canonical_digest({k: v.source_digest for k, v in host.capabilities.items()})
        != c["executor_source_digest"]
        or "sha256:"
        + _canonical_digest({k: v.dependency_digest for k, v in host.capabilities.items()})
        != c["executor_dependency_digest"]
        or provider_digest() != c["provider_digest"]
        or renderer_closure(host, environment) != c["renderer_closure"]
    ):
        raise FrameOwnerError("host_source_or_owner_changed")
    _verify_admitted_source(
        {
            "source_digest": record.source_digest,
            "source_roots": [
                str(p) for p in _admitted_source_roots(record.source_root, record.definition)
            ],
        }
    )
    owner = host._remotion_host_session
    if owner is not None and (
        owner._closed
        or owner.execution_invalidated
        or owner.uncertain
        or owner.frame_owner.generation != c["owner_generation"]
    ):
        raise FrameOwnerError("owner_changed")


def configuration_from_activation(preparation):
    from . import hosted_contract
    from .generic_host import _ACTIVATION_RECEIPT_MODE, _canonical_digest

    host, request, grant = (
        preparation._claim_host,
        preparation._request,
        preparation._activation_grant,
    )
    binding = getattr(preparation, "_hosted_binding", None)
    if (
        host is None
        or request is None
        or grant is None
        or binding is None
        or preparation.result is None
        or preparation._aborted
        or preparation.control_error is not None
        or preparation._retained_relay_actor is None
    ):
        raise FrameOwnerError("activation_unavailable")
    if (
        binding.get("role") != "host"
        or binding.get("purpose") != "runtime-host-control/v1"
        or set(binding.get("sockets", {})) != {"control", "activation"}
    ):
        raise FrameOwnerError("activation_unavailable")
    hosted_contract.verify_preparation(
        binding,
        request,
        custody.RoleCustodyAuthority(Path(binding["scope"]), "host"),
        actor=preparation._retained_relay_actor,
    )
    owner = request["runtime_owner"]
    # The protected Runtime launch request binds the original Runtime triple.
    # Native audit-token observation upgrades that exact live incarnation; the
    # relay's own identity is never accepted as Runtime authority.
    runtime_peer = ProcessIdentity(
        **custody.AuthenticatedCleanupActor(
            lambda: custody.current_process_audit_token(owner["pid"]),
            custody.default_process_identity,
        ).verify()
    )
    host_peer = ProcessIdentity(**custody.AuthenticatedCleanupActor.current().verify())
    state = host._registered_runtime_state
    if (
        any(getattr(runtime_peer, k) != owner[k] for k in ("pid", "uid", "birth_id"))
        or owner["runtime_instance_id"] != state["runtime_instance_id"]
        or owner["coordinator_epoch"] != state["coordinator_epoch"]
        or grant.get("host") != {"pid": host_peer.pid, "birth_id": host_peer.birth_id}
        or grant.get("operation_id") != preparation.operation_id
        or grant.get("channel_id") != preparation.channel_id
        or grant.get("acceptance_mode") != _ACTIVATION_RECEIPT_MODE
    ):
        raise FrameOwnerError("runtime_identity_mismatch")
    launch = request["profile"].get("host_launch")
    if launch is not None and (
        Path(launch["boot_manifest_path"]) != host.boot_manifest_path
        or launch["boot_manifest_hash"].removeprefix("sha256:") != host.boot_manifest_hash
        or tuple(
            dict.fromkeys(
                Path(p)
                for p in [
                    launch["pack_root"],
                    *(v["path"] for v in launch.get("additional_pack_roots", [])),
                ]
            )
        )
        != host.pack_roots
    ):
        raise FrameOwnerError("source_mismatch")
    record = host.capabilities.get("rendering.timeline_visualize")
    if record is None:
        raise FrameOwnerError("renderer_unavailable")
    # Existing preflight resolves the Host's qualified renderer after trusted
    # boot. Launch env intentionally cannot carry renderer authority selectors.
    admitted = record.preflight.get("remotion", {})
    if getattr(host, "_remotion_closure_binding", None) is not None:
        # timeline_visualize also serves static queries. Authoring scenes use
        # the separately admitted renderer and its REAL launch-bound validator,
        # rather than fabricating a Remotion check on that static capability.
        from astrid.core.rendering.remotion_runtime import remotion_runtime_status
        status = remotion_runtime_status(require_explicit_project=True)
        admitted = {"ok": status.available,
                    "project_dir": str(status.project_dir) if status.project_dir else None,
                    "node_executable": str(status.node_executable) if status.node_executable else None}

    if (
        not admitted.get("ok")
        or not admitted.get("project_dir")
        or not admitted.get("node_executable")
    ):
        raise FrameOwnerError("renderer_unavailable")
    environment = {
        k: os.environ[k] for k in ("HOME", "LANG", "LC_ALL", "LC_CTYPE", "PATH") if k in os.environ
    }
    environment.update(
        ASTRID_REMOTION_PROJECT_DIR=admitted["project_dir"],
        ASTRID_NODE_EXECUTABLE=admitted["node_executable"],
    )
    context = dict(
        runtime_realm_id=request["profile"]["workspace_uuid"],
        runtime_instance_id=state["runtime_instance_id"],
        runtime_session_id=state["runtime_session_id"],
        executor_id=host.executor_id,
        host_instance_id=grant["executor_incarnation"],
        source_epoch=host.source_epoch,
        provider_id="astrid-v1",
        provider_digest=provider_digest(),
        source_digest="sha256:" + record.source_digest,
        dependency_digest="sha256:" + record.dependency_digest,
        renderer_closure=renderer_closure(host, environment),
        owner_generation=host._authoring_scene_session(environment).frame_owner.generation,
        capability_digest=record.capability_digest,
        executor_source_digest="sha256:"
        + _canonical_digest({k: v.source_digest for k, v in host.capabilities.items()}),
        executor_dependency_digest="sha256:"
        + _canonical_digest({k: v.dependency_digest for k, v in host.capabilities.items()}),
    )
    config = AuthoringSceneConfig(
        Path(request["profile"]["support_root"]),
        host_peer,
        runtime_peer,
        context,
        host.boot_manifest_hash,
    )
    validate_host(host, config, environment)
    return config, environment
