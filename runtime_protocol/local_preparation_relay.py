"""Single, pure preparation exchange with an explicitly bound local Host.

No execution/cleanup channel, producer imports, discovery, retry, or persistence.
The startup binding is owned by daemon composition, never public request data.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import stat
import time
import uuid

from banodoco_local.custody_broker import (AuthenticatedCleanupActor, CustodyError,
    current_process_audit_token, default_process_identity, _incarnation)
from .errors import CapabilityUnavailableError, ConflictError, ValidationError
from .storage_contract import storage_contract, validate_storage_estimate

PROTOCOL = "astrid.storage-preparation/v1"
COMMAND = "prepare_storage_estimate"
FRAME_LIMIT = 64 * 1024
PROCESS_FIELDS = {"pid", "uid", "birth_id", "audit_token_sha256", "audit_token_pidversion"}
CONTEXT_FIELDS = ("realm_id", "runtime_instance_id", "runtime_session_id", "runtime_epoch")
BINDING_FIELDS = ("executor_id", "source_epoch", "capability_id", "capability_digest", "storage_estimate_contract")
STARTUP_FIELDS = set(CONTEXT_FIELDS + BINDING_FIELDS) | {"support_root", "socket_path", "readiness_record_path", "runtime_process", "host_process", "source_digest", "dependency_digest", "preparation_source_digest", "deadline_ms"}


class InputFactsUnavailableError(CapabilityUnavailableError):
    code = "input_facts_unavailable"


def unavailable(reason):
    return CapabilityUnavailableError("storage preparation unavailable", details={"reason": reason})


class InvalidPreparationReplyError(ConflictError):
    code = "invalid_reply"


def invalid_reply(reason):
    return InvalidPreparationReplyError("invalid storage preparation reply", details={"reason": reason})


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def digest(value):
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def _sha(value):
    return isinstance(value, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", value) is not None


def _unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate key")
        value[key] = item
    return value


def decode(raw):
    try:
        value = json.loads(raw, object_pairs_hook=_unique, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        canonical(value)
        if not isinstance(value, dict):
            raise ValueError("not object")
        return value
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        raise invalid_reply("malformed_frame") from exc


def validate_process(value):
    if (not isinstance(value, dict) or set(value) != PROCESS_FIELDS
            or type(value.get("pid")) is not int or value["pid"] <= 0
            or type(value.get("uid")) is not int or value["uid"] < 0
            or type(value.get("audit_token_pidversion")) is not int or value["audit_token_pidversion"] <= 0
            or not isinstance(value.get("birth_id"), str) or not value["birth_id"]
            or not _sha(value.get("audit_token_sha256"))):
        raise unavailable("peer_identity_unsupported")


def validate_preparation(value, request, binding):
    keys = {"capability_id", "capability_digest", "schema_version", "spec", "input_facts", "spec_digest", "source_digest", "estimator", "storage_estimate", "preparation_digest"}
    if not isinstance(value, dict) or set(value) != keys:
        raise invalid_reply("preparation_schema")
    if (type(value["schema_version"]) is not int or value["schema_version"] != 1
            or any(canonical(value[k]) != canonical(request[k]) for k in request)
            or value["source_digest"] != binding["preparation_source_digest"]
            or canonical(value["estimator"]) != canonical(binding["storage_estimate_contract"]["estimator"])
            or value["spec_digest"] != digest(request["spec"])
            or not _sha(value["preparation_digest"])):
        raise invalid_reply("preparation_binding")
    try:
        validate_storage_estimate(value["storage_estimate"])
    except ValidationError as exc:
        raise invalid_reply("storage_estimate_schema") from exc
    if value["preparation_digest"] != digest({k: v for k, v in value.items() if k != "preparation_digest"}):
        raise invalid_reply("preparation_digest")
    return copy.deepcopy(value)


class LocalPreparationRelay:
    """Production transport; A supplies this exact binding after Host startup.

    ``readiness_record()`` describes the dedicated listener's owner-only JSON
    record. It is source/boot binding, not a quote or a bearer credential.
    """
    def __init__(self, binding):
        if not isinstance(binding, dict) or set(binding) != STARTUP_FIELDS:
            raise unavailable("startup_binding_invalid")
        self._binding = copy.deepcopy(binding)
        b = self._binding
        for key in CONTEXT_FIELDS + BINDING_FIELDS + ("source_digest", "dependency_digest"):
            if key in {"runtime_epoch", "storage_estimate_contract"}:
                continue
            if not isinstance(b[key], str) or not b[key]:
                raise unavailable("startup_binding_invalid")
        if (type(b["runtime_epoch"]) is not int or b["runtime_epoch"] <= 0
                or type(b["deadline_ms"]) is not int or not 0 < b["deadline_ms"] <= 30000
                or not all(_sha(b[k]) for k in ("capability_digest", "preparation_source_digest"))):
            raise unavailable("startup_binding_invalid")
        for key in ("host_process", "runtime_process"):
            validate_process(b[key])
        try:
            if storage_contract({"storage_estimate_contract": b["storage_estimate_contract"]})["mode"] != "request_estimated":
                raise ValidationError("wrong mode")
        except ValidationError as exc:
            raise unavailable("startup_descriptor_invalid") from exc
        for key in ("support_root", "socket_path", "readiness_record_path"):
            if not isinstance(b[key], str) or not b[key]:
                raise unavailable("endpoint_path_invalid")
            p = Path(b[key])
            if not p.is_absolute() or ".." in p.parts:
                raise unavailable("endpoint_path_invalid")
        root = Path(b["support_root"])
        for key in ("socket_path", "readiness_record_path"):
            if not Path(b[key]).is_relative_to(root) or Path(b[key]) == root:
                raise unavailable("endpoint_not_contained")
        if b["socket_path"] == b["readiness_record_path"]:
            raise unavailable("endpoint_path_invalid")

    @property
    def binding(self):
        return copy.deepcopy(self._binding)

    def readiness_record(self):
        return {"protocol": PROTOCOL, **self.binding}

    def _paths(self):
        b = self._binding
        root = Path(b["support_root"])
        # Validate every ancestor for symlinks; private owner policy starts at
        # the task-owned support root. Sticky system parents are not ours.
        for key in ("socket_path", "readiness_record_path"):
            p = Path(b[key])
            for part in [*reversed(p.parents), p]:
                info = part.lstat()
                if stat.S_ISLNK(info.st_mode):
                    raise unavailable("endpoint_symlink")
                if part == root or root in part.parents:
                    if info.st_uid != os.getuid() or info.st_mode & 0o077:
                        raise unavailable("endpoint_not_private")
                    if part != p and not stat.S_ISDIR(info.st_mode):
                        raise unavailable("endpoint_parent_invalid")
            info = p.lstat()
            if key == "socket_path" and not stat.S_ISSOCK(info.st_mode):
                raise unavailable("endpoint_not_socket")
            if key == "readiness_record_path" and not stat.S_ISREG(info.st_mode):
                raise unavailable("readiness_not_regular")
        record = Path(b["readiness_record_path"])
        fd = os.open(record, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
                raise unavailable("readiness_not_private")
            raw = os.read(fd, FRAME_LIMIT + 1)
            if len(raw) > FRAME_LIMIT:
                raise unavailable("readiness_oversized")
            if canonical(decode(raw)) != canonical(self.readiness_record()):
                raise unavailable("readiness_stale")
        finally:
            os.close(fd)

    def exchange(self, request):
        b = self._binding
        end = time.monotonic() + b["deadline_ms"] / 1000
        def remaining():
            seconds = end - time.monotonic()
            if seconds <= 0:
                raise unavailable("preparation_deadline")
            return seconds
        try:
            self._paths()
            if AuthenticatedCleanupActor.current().verify() != b["runtime_process"]:
                raise unavailable("runtime_process_changed")
            envelope = {"protocol": PROTOCOL, "command": COMMAND, "request_id": uuid.uuid4().hex,
                        "runtime": {k: b[k] for k in CONTEXT_FIELDS},
                        **{k: b[k] for k in BINDING_FIELDS}, "request": request}
            encoded = canonical(envelope) + b"\n"
            if len(encoded) > FRAME_LIMIT:
                raise unavailable("preparation_frame_oversized")
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as channel:
                channel.settimeout(remaining())
                channel.connect(b["socket_path"])
                peer = AuthenticatedCleanupActor.private_peer(channel)
                if peer.verify() != b["host_process"]:
                    raise unavailable("host_peer_mismatch")
                self._paths()
                channel.settimeout(remaining())
                channel.sendall(encoded)
                raw = bytearray()
                while b"\n" not in raw:
                    channel.settimeout(remaining())
                    part = channel.recv(min(4096, FRAME_LIMIT + 1 - len(raw)))
                    if not part:
                        raise invalid_reply("truncated_frame")
                    raw.extend(part)
                    if len(raw) > FRAME_LIMIT:
                        raise invalid_reply("oversized_frame")
                frame, extra = bytes(raw).split(b"\n", 1)
                if extra:
                    raise invalid_reply("multiple_frames")
                response = decode(frame)
                context = {k: v for k, v in envelope.items() if k != "request"}
                if (set(response) not in (set(context) | {"preparation"}, set(context) | {"refusal"})
                        or any(canonical(response[k]) != canonical(v) for k, v in context.items())):
                    raise invalid_reply("reply_correlation")
                # A one-reply Host may close its connection immediately. Darwin
                # cannot reread LOCAL_PEERTOKEN on a disconnected socket. The
                # peer was authenticated above; now reobserve that exact live
                # native incarnation, never a UID/PID-only replacement.
                host = b["host_process"]
                observed = default_process_identity(host["pid"])
                if observed is None or _incarnation(observed, current_process_audit_token(host["pid"])) != host:
                    raise unavailable("host_peer_changed")
                if AuthenticatedCleanupActor.current().verify() != b["runtime_process"]:
                    raise unavailable("runtime_process_changed")
                self._paths()
                remaining()
                if "refusal" in response:
                    refusal = response["refusal"]
                    if not isinstance(refusal, dict) or set(refusal) != {"code"} or not isinstance(refusal["code"], str) or not refusal["code"]:
                        raise invalid_reply("refusal_schema")
                    raise unavailable(refusal["code"])
                return validate_preparation(response["preparation"], request, b)
        except (TimeoutError, socket.timeout) as exc:
            raise unavailable("preparation_deadline") from exc
        except CustodyError as exc:
            raise unavailable("peer_identity_unsupported") from exc
        except OSError as exc:
            raise unavailable("endpoint_unavailable") from exc
