"""Single, pure preparation exchange with an explicitly bound local Host.

No execution/cleanup channel, producer imports, discovery, retry, or persistence.
The startup binding is owned by daemon composition, never public request data.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import stat
import sys
import time
import uuid
from typing import Callable

from banodoco_local import custody_broker as custody
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
STARTUP_FIELDS = set(CONTEXT_FIELDS + BINDING_FIELDS) | {"support_root", "socket_path", "readiness_record_path", "runtime_process", "host_process", "source_digest", "dependency_digest", "preparation_source_digest", "preparation_dependency_digest", "host_instance_id", "boot_manifest_hash", "deadline_ms"}


class InputFactsUnavailableError(CapabilityUnavailableError):
    code = "input_facts_unavailable"


def unavailable(reason):
    return CapabilityUnavailableError("storage preparation unavailable", details={"reason": reason})


@dataclass(frozen=True)
class StorageUnavailable:
    """Validated operational refusal, never a substitute for binding validation."""
    capability_id: str
    reason: str


@dataclass(frozen=True)
class StagedStorageBinding:
    relay: LocalPreparationRelay | None = None
    unavailable: StorageUnavailable | None = None
    check: Callable[[], None] = lambda: None
    check_authority: Callable[[], None] = lambda: None


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
        self._selected_host_check = None
        self._selected_host_ready = None
        b = self._binding
        for key in CONTEXT_FIELDS + BINDING_FIELDS + ("source_digest", "dependency_digest"):
            if key in {"runtime_epoch", "storage_estimate_contract"}:
                continue
            if not isinstance(b[key], str) or not b[key]:
                raise unavailable("startup_binding_invalid")
        if (type(b["runtime_epoch"]) is not int or b["runtime_epoch"] <= 0
                or type(b["deadline_ms"]) is not int or not 0 < b["deadline_ms"] <= 30000
                or not all(_sha(b[k]) for k in ("capability_digest", "preparation_source_digest", "preparation_dependency_digest"))):
            raise unavailable("startup_binding_invalid")
        if (not isinstance(b["host_instance_id"], str) or not b["host_instance_id"]
                or not isinstance(b["boot_manifest_hash"], str)
                or re.fullmatch(r"[0-9a-f]{64}", b["boot_manifest_hash"]) is None):
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
            path = Path(b[key])
            if not path.is_relative_to(root) or path == root:
                compact = path.parent
                if (key != "socket_path" or path.name != "s"
                        or compact.parent != custody.DARWIN_CUSTODY_SOCKET_PARENT
                        or not compact.name.startswith("runtime-cb-")
                        or compact.resolve(strict=True) != compact):
                    raise unavailable("endpoint_not_contained")
        if b["socket_path"] == b["readiness_record_path"]:
            raise unavailable("endpoint_path_invalid")

    @property
    def binding(self):
        return copy.deepcopy(self._binding)

    @property
    def context(self):
        b = self._binding
        return {"runtime": {k: b[k] for k in CONTEXT_FIELDS},
                **{k: copy.deepcopy(b[k]) for k in BINDING_FIELDS}}

    def request_envelope(self, request, request_id=None):
        return {"protocol": PROTOCOL, "command": COMMAND,
                "request_id": request_id or uuid.uuid4().hex,
                "context": self.context, "request": copy.deepcopy(request)}

    def readiness_record(self):
        b = self._binding
        return {"protocol": PROTOCOL, "command": COMMAND, "context": self.context,
                "host_instance_id": b["host_instance_id"], "host_peer": b["host_process"],
                "runtime_peer": b["runtime_process"], "boot_manifest_hash": b["boot_manifest_hash"],
                "socket_path": b["socket_path"], "capability_id": b["capability_id"],
                "capability_digest": b["capability_digest"], "source_digest": b["preparation_source_digest"],
                "dependency_digest": b["preparation_dependency_digest"],
                "estimator": b["storage_estimate_contract"]["estimator"],
                "executor_source_digest": "sha256:" + b["source_digest"].removeprefix("sha256:"),
                "executor_dependency_digest": "sha256:" + b["dependency_digest"].removeprefix("sha256:")}

    def validate_response(self, response, envelope):
        correlation = {k: v for k, v in envelope.items() if k != "request"}
        if (set(response) not in (set(correlation) | {"preparation"}, set(correlation) | {"refusal"})
                or any(canonical(response[k]) != canonical(v) for k, v in correlation.items())):
            raise invalid_reply("reply_correlation")
        if "refusal" in response:
            refusal = response["refusal"]
            if not isinstance(refusal, dict) or set(refusal) != {"code"} or not isinstance(refusal["code"], str) or not refusal["code"]:
                raise invalid_reply("refusal_schema")
            raise unavailable(refusal["code"])
        return validate_preparation(response["preparation"], envelope["request"], self._binding)

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
                private_root = (p.parent if key == "socket_path" and not p.is_relative_to(root) else root)
                if part == private_root or private_root in part.parents:
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

    def check_readiness(self):
        """File/registration check only; no IPC while catalog holds its mutex."""
        self._paths()
        if self._selected_host_ready is not None:
            self._selected_host_ready()

    def startup_listener_present(self, timeout):
        """Authenticate the listening peer without sending a frame or a spec."""
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as channel:
                channel.settimeout(timeout)
                channel.connect(self._binding["socket_path"])
                if AuthenticatedCleanupActor.private_peer(channel).verify() != self._binding["host_process"]:
                    raise unavailable("host_peer_mismatch")
                return True
        except (FileNotFoundError, ConnectionRefusedError, TimeoutError):
            return False
        except CustodyError as exc:
            raise unavailable("peer_identity_unsupported") from exc

    def exchange(self, request):
        b = self._binding
        end = time.monotonic() + b["deadline_ms"] / 1000
        def remaining():
            seconds = end - time.monotonic()
            if seconds <= 0:
                raise unavailable("preparation_deadline")
            return seconds
        try:
            if self._selected_host_check is not None:
                self._selected_host_check()
            self._paths()
            if AuthenticatedCleanupActor.current().verify() != b["runtime_process"]:
                raise unavailable("runtime_process_changed")
            envelope = self.request_envelope(request)
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
                if self._selected_host_check is not None:
                    self._selected_host_check()
                return self.validate_response(response, envelope)
        except (TimeoutError, socket.timeout) as exc:
            raise unavailable("preparation_deadline") from exc
        except CustodyError as exc:
            raise unavailable("peer_identity_unsupported") from exc
        except OSError as exc:
            raise unavailable("endpoint_unavailable") from exc


class _StartupProgress:
    """Only verified, forward milestones renew the idle budget, at most twice.

    No heartbeat, repeated file write or replacement generation earns time.
    Registration, readiness and listener each get one preparer-sized budget;
    the whole exchange is capped at three budgets after static discovery.
    """
    def __init__(self, seconds):
        self.started = time.monotonic()
        self.budget = seconds
        self.end = self.started + seconds
        self.limit = self.started + 3 * seconds
        self.stage = "registration"
        self.generation = None
        self.readiness = "pending"
        self.listener = None

    def advance(self, stage):
        if time.monotonic() >= self.end:
            raise unavailable("preparation_startup_deadline")
        if self.stage != stage:
            self.stage = stage
            self.end = min(self.limit, time.monotonic() + self.budget)

    def snapshot(self):
        return dict(stage=self.stage, elapsed_ms=max(0, int((time.monotonic() - self.started) * 1000)),
            generation_sha256=self.generation,
            registration="pending" if self.stage == "registration" else "validated",
            readiness=self.readiness, listener_present=self.listener,
            phase_budget_ms=int(self.budget * 1000), total_budget_ms=int(3 * self.budget * 1000))


def bind_selected_host(daemon, profile, handle):
    diagnostic = {}
    try:
        return _bind_selected_host(daemon, profile, handle, diagnostic)
    except BaseException as exc:
        if isinstance(exc, (CapabilityUnavailableError, InvalidPreparationReplyError)):
            exc.details = {**(exc.details or {}), "startup": copy.deepcopy(diagnostic)}
        raise
    finally:
        daemon.local_preparation_diagnostic = copy.deepcopy(diagnostic)
        if diagnostic:
            try:
                print(json.dumps({"event": "storage_preparation_startup", **diagnostic}, sort_keys=True),
                      file=sys.stderr, flush=True)
            except BaseException:
                pass


def _bind_selected_host(daemon, profile, handle, diagnostic):
    """Stage only the retained authenticated launch; publish no service state.

    Static Astrid discovery supplies capability source scopes from the selected
    immutable launch roots. It starts no process/listener and runs no estimator.
    The live registration independently supplies the executor/source epoch.
    """
    from astrid.core.execution.generic_host import GenericPackHost, _canonical_digest

    launch = profile.host_launch
    if profile.execution_mode != "host_only_cpu" or not launch:
        return StagedStorageBinding()
    inventory = GenericPackHost(pack_roots=[launch["pack_root"],
        *(item["path"] for item in launch.get("additional_pack_roots", []))],
        capability_matrix=launch.get("capability_matrix"))
    try:
        records = inventory.discover()
        candidates = [v for v in records if v.has_request_storage_estimator]
        if not candidates:
            return StagedStorageBinding()
        if len(candidates) != 1:
            raise unavailable("capability_binding_unavailable")
        record = candidates[0]
        source = _canonical_digest({v.id: v.source_digest for v in records})
        dependency = _canonical_digest({v.id: v.dependency_digest for v in records})
        contract = copy.deepcopy(record.request_storage_estimate_contract)
    finally:
        inventory.shutdown()
    service = daemon.service
    progress = _StartupProgress(daemon.local_worker_preparer.timeout_seconds)
    root = Path(profile.support_root)
    expected_generation = None
    expected_binding = None
    while True:
        diagnostic.update(progress.snapshot())
        if time.monotonic() >= progress.end:
            raise unavailable("preparation_startup_deadline")
        if (daemon.local_worker_preparer.current_handle() is not handle
                or handle.closed or not handle.activated):
            raise unavailable("selected_host_changed")
        report = daemon.local_worker_preparer.report(handle)
        host = handle.retained.verify()
        validate_process(host)
        if (report["owner_epoch"] != service.runtime_instance_id
                or any(report["processes"]["host"][k] != host[k] for k in ("pid", "birth_id"))):
            raise unavailable("selected_host_changed")
        with service.store._mutex:
            from .daemon import WORKER_ACTOR
            from .local_worker import _credential_commit_generation
            token, _ = daemon.credentials._read_actor(WORKER_ACTOR)
            daemon.credentials.require(token, "worker:execute")
            metadata = daemon.credentials.actor_metadata(WORKER_ACTOR)
            receipt = metadata.get("local_launch_receipt") if isinstance(metadata, dict) else None
            generation = (_credential_commit_generation(daemon.credentials, WORKER_ACTOR), copy.deepcopy(metadata))
            if expected_generation is None:
                expected_generation = generation
            elif generation != expected_generation:
                raise unavailable("selected_activation_changed")
            rows = service.store.conn.execute("SELECT * FROM executors WHERE readiness='ready'").fetchall()
            # Identity is the fixed launch executor ID, never the first socket.
            executor_id = launch.get("executor_id", "astrid-pack-host")
            row = next((v for v in rows if v["id"] == executor_id), None)
            if row is not None and receipt is not None:
                daemon._assert_local_relinquish_receipt(receipt, metadata)
                if (row["source_digest"] != source or row["dependency_digest"] != dependency
                        or receipt.get("owner_epoch") != report["owner_epoch"]
                        or any(receipt["host"].get(k) != report["processes"]["host"][k]
                               for k in ("pid", "birth_id"))):
                    # Keep this internal: startup diagnostics are also public
                    # error details. Only fixed field names may reach this log.
                    try:
                        mismatches = [name for name, changed in (
                            ("source_digest", row["source_digest"] != source),
                            ("dependency_digest", row["dependency_digest"] != dependency),
                            ("owner_epoch", receipt.get("owner_epoch") != report["owner_epoch"]),
                            ("host_pid", receipt["host"].get("pid") != report["processes"]["host"]["pid"]),
                            ("host_birth_id", receipt["host"].get("birth_id") != report["processes"]["host"]["birth_id"]),
                        ) if changed]
                        print(json.dumps({"event": "storage_preparation_selected_source_changed",
                                          "mismatches": mismatches}, sort_keys=True),
                              file=sys.stderr, flush=True)
                    except BaseException:
                        pass  # Diagnostics must never replace the original refusal.
                    raise unavailable("selected_source_changed")
                binding = dict(realm_id=service.realm["id"], runtime_instance_id=service.runtime_instance_id,
                    runtime_session_id=service.runtime_session_id, runtime_epoch=service.store._current_runtime_epoch(),
                    executor_id=executor_id, source_epoch=row["source_epoch"], capability_id=record.id,
                    capability_digest=record.capability_digest, storage_estimate_contract=contract,
                    support_root=str(root), socket_path=str(root / "storage-preparation/s"),
                    readiness_record_path=str(root / "storage-preparation/ready.json"),
                    runtime_process=AuthenticatedCleanupActor.current().verify(), host_process=host,
                    source_digest=source, dependency_digest=dependency,
                    preparation_source_digest="sha256:" + record.source_digest,
                    preparation_dependency_digest="sha256:" + record.dependency_digest,
                    host_instance_id=receipt["executor_incarnation"],
                    boot_manifest_hash=launch["boot_manifest_hash"].removeprefix("sha256:"),
                    deadline_ms=min(30000, max(1, int(daemon.local_worker_preparer.timeout_seconds * 1000))))
            else:
                binding = None
        if binding is not None:
            # Validate the complete startup shape, registration and estimator
            # before treating any operational refusal as independent of authoring.
            relay = LocalPreparationRelay(binding)
            with service.store._mutex:
                context = service._preparation_binding_context(binding)
                refusal = service._preparation_unavailability(binding, context)
            def check_selected_ready():
                if (daemon.local_worker_preparer.current_handle() is not handle
                        or handle.closed or not handle.activated):
                    raise unavailable("selected_host_changed")
                with service.store._mutex:
                    token, _ = daemon.credentials._read_actor(WORKER_ACTOR)
                    daemon.credentials.require(token, "worker:execute")
                    current = daemon.credentials.actor_metadata(WORKER_ACTOR)
                    if (_credential_commit_generation(daemon.credentials, WORKER_ACTOR), current) != expected_generation:
                        raise unavailable("selected_activation_changed")
                    daemon._assert_local_relinquish_receipt(receipt, current)
            def check_authority():
                check_selected_ready()
                current_report = daemon.local_worker_preparer.report(handle)
                if (handle.retained.verify() != host
                        or current_report["owner_epoch"] != service.runtime_instance_id
                        or any(current_report["processes"]["host"][k] != host[k] for k in ("pid", "birth_id"))):
                    raise unavailable("host_peer_changed")
            def check_selected():
                check_authority()
                with service.store._mutex:
                    if service._preparation_binding_context(binding) != context:
                        raise unavailable("selected_source_changed")
            check_selected()
            identity = tuple(binding[k] for k in CONTEXT_FIELDS + ("host_instance_id", "source_epoch"))
            if expected_binding is None:
                expected_binding = identity
                progress.generation = hashlib.sha256(canonical(identity)).hexdigest()
                progress.advance("readiness")
            elif identity != expected_binding:
                raise unavailable("selected_activation_changed")
            if refusal is not None:
                progress.stage = "unavailable"
                diagnostic.update(progress.snapshot())
                return StagedStorageBinding(unavailable=refusal, check=check_selected,
                                            check_authority=check_authority)
            readiness = Path(binding["readiness_record_path"])
            try:
                fd = os.open(readiness, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            except FileNotFoundError:
                pass
            else:
                try:
                    facts = os.fstat(fd)
                    if (not stat.S_ISREG(facts.st_mode) or facts.st_uid != os.getuid()
                            or facts.st_mode & 0o077):
                        raise unavailable("readiness_not_private")
                    raw = os.read(fd, FRAME_LIMIT + 1)
                    if len(raw) > FRAME_LIMIT:
                        raise unavailable("readiness_oversized")
                    startup = decode(raw)
                    binding["socket_path"] = startup.get("socket_path", binding["socket_path"])
                    # Validate the entire record even while the socket is late.
                    # A malformed/stale file is fatal, never progress.
                    relay = LocalPreparationRelay(binding)
                    if canonical(startup) != canonical(relay.readiness_record()):
                        raise unavailable("readiness_stale")
                    progress.readiness = "validated"
                    if progress.stage == "readiness":
                        progress.advance("listener")
                finally:
                    os.close(fd)
            relay = LocalPreparationRelay(binding)
            try:
                relay._paths()
            except FileNotFoundError:
                if progress.stage == "listener":
                    progress.listener = False
            else:
                progress.listener = relay.startup_listener_present(min(0.05, max(0.001, progress.end - time.monotonic())))
                if not progress.listener:
                    diagnostic.update(progress.snapshot())
                    time.sleep(min(0.05, max(0.0, progress.end - time.monotonic())))
                    continue
                check_selected()
                if time.monotonic() >= progress.end:
                    raise unavailable("preparation_startup_deadline")
                relay._selected_host_check = check_selected
                relay._selected_host_ready = check_selected_ready
                progress.stage = "ready"
                progress.readiness = "validated"
                diagnostic.update(progress.snapshot())
                return StagedStorageBinding(relay=relay, check=check_selected,
                                            check_authority=check_authority)
        elif expected_binding is not None:
            raise unavailable("selected_activation_changed")
        diagnostic.update(progress.snapshot())
        time.sleep(min(0.05, max(0.0, progress.end - time.monotonic())))
