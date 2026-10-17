"""Private Runtime -> existing GenericPackHost authoring receiver.

The startup object comes only from the accepted native launch. Neither requests
nor environment variables select the endpoint, owner, renderer or purpose.
"""

from __future__ import annotations

import copy
import os
import select
import socket
import stat
import tempfile
import threading
import time
from dataclasses import asdict, dataclass, replace
from pathlib import Path

from . import authoring_scene_protocol as wire
from . import custody_broker as custody
from .remotion_frame_owner import FrameOwnerError
from .storage_preparation_transport import ProcessIdentity, _directory, _inode, read_frame


@dataclass(frozen=True)
class AuthoringSceneConfig:
    support_root: Path
    host_peer: ProcessIdentity
    runtime_peer: ProcessIdentity
    binding: dict
    boot_manifest_hash: str
    socket_root: Path | None = None

    def __post_init__(self):
        wire.context(self.binding)
        if (
            type(self.host_peer) is not ProcessIdentity
            or type(self.runtime_peer) is not ProcessIdentity
            or not self.support_root.is_absolute()
            or not wire.sha("sha256:" + self.boot_manifest_hash)
        ):
            raise FrameOwnerError("startup_invalid")
        object.__setattr__(self, "binding", copy.deepcopy(self.binding))
        if self.socket_root is not None and (
            self.socket_root.parent != custody.DARWIN_CUSTODY_SOCKET_PARENT
            or not self.socket_root.name.startswith("runtime-cb-")
            or self.socket_root.resolve(strict=True) != self.socket_root
        ):
            raise FrameOwnerError("startup_invalid")

    @property
    def socket_path(self):
        return (self.socket_root or self.support_root / "authoring-scene") / "s"

    @property
    def readiness_path(self):
        return self.support_root / "authoring-scene" / "ready.json"

    @property
    def record(self):
        record = dict(
            protocol=wire.PROTOCOL,
            operation=wire.OPERATION,
            purpose=wire.PURPOSE,
            context=self.binding,
            host_peer=asdict(self.host_peer),
            runtime_peer=asdict(self.runtime_peer),
            boot_manifest_hash=self.boot_manifest_hash,
        )
        if self.socket_root is not None:
            record["socket_root"] = str(self.socket_root)
        return record


def _actor(identity):
    return custody.AuthenticatedCleanupActor(
        lambda: custody.current_process_audit_token(identity.pid), custody.default_process_identity
    )


def check_endpoint(config):
    """No aliases, public parent, stale record or endpoint substitution."""
    fd = _directory(config.socket_path.parent)
    ready_fd = None
    try:
        ready_fd = _directory(config.readiness_path.parent)
        facts = os.stat("s", dir_fd=fd, follow_symlinks=False)
        if (
            not stat.S_ISSOCK(facts.st_mode)
            or facts.st_uid != os.getuid()
            or stat.S_IMODE(facts.st_mode) != 0o600
        ):
            raise FrameOwnerError("endpoint_invalid")
        record = os.open("ready.json", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=ready_fd)
        try:
            info = os.fstat(record)
            if (
                not stat.S_ISREG(info.st_mode)
                or info.st_uid != os.getuid()
                or stat.S_IMODE(info.st_mode) != 0o600
                or os.read(record, wire.LIMIT + 1) != wire.encoded(config.record) + b"\n"
            ):
                raise FrameOwnerError("endpoint_changed")
        finally:
            os.close(record)
        return _inode(os.fstat(ready_fd)), _inode(os.fstat(fd)), _inode(facts)
    finally:
        if ready_fd is not None:
            os.close(ready_fd)
        os.close(fd)


class AuthoringSceneRelay:
    """Installed Runtime's trusted startup selection; no request selects this."""

    def __init__(self, config):
        if type(config) is not AuthoringSceneConfig:
            raise FrameOwnerError("startup_invalid")
        self.config = config
        self._closed = threading.Event()
        self._endpoint = check_endpoint(config)

    def close(self):
        self._closed.set()

    def check_live(self):
        c = self.config
        if self._closed.is_set():
            raise FrameOwnerError("invocation_revoked")
        c.runtime_peer.matches(custody.AuthenticatedCleanupActor.current().verify())
        c.host_peer.matches(_actor(c.host_peer).verify())
        if check_endpoint(c) != self._endpoint:
            raise FrameOwnerError("endpoint_changed")

    def exchange(self, request, *, guard, cancelled, timeout=30.0):
        wire.validate_request(request, self.config.binding)
        end = time.monotonic() + timeout

        def live():
            guard()
            self.check_live()
            if cancelled.is_set() or time.monotonic() >= end:
                raise FrameOwnerError("cancelled_or_timeout")

        live()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as channel:
            channel.settimeout(max(0.001, end - time.monotonic()))
            channel.connect(str(self.config.socket_path))
            peer = custody.AuthenticatedCleanupActor.private_peer(channel)
            self.config.host_peer.matches(peer.verify())
            live()
            channel.sendall(wire.encoded(request) + b"\n")
            # Check live principal/cancellation while blocked, not only on reply.
            while not select.select([channel], [], [], min(0.1, max(0, end - time.monotonic())))[0]:
                live()

            class LiveReader:
                def recv(self, count):
                    while True:
                        live()
                        if select.select(
                            [channel], [], [], min(0.1, max(0, end - time.monotonic()))
                        )[0]:
                            return channel.recv(count)

                def settimeout(self, seconds):
                    channel.settimeout(seconds)

            response = read_frame(LiveReader(), end)
            live()
            return copy.deepcopy(wire.validate_reply(response, request))


class AuthoringSceneListener:
    def __init__(self, host, config, environment):
        if type(config) is not AuthoringSceneConfig:
            raise FrameOwnerError("startup_invalid")
        self.host, self.config = host, config
        self.environment = dict(environment)
        self._stop = threading.Event()
        self._listener = self._active = self._thread = None
        self._lock = threading.Lock()
        self._root_fd = None
        self._socket_fd = None
        self._compact_root = None
        self._owned = {}

    def check_live(self):
        from .authoring_scene_startup import validate_host

        if self._stop.is_set() or self.host._shutdown.is_set():
            raise FrameOwnerError("host_shutdown")
        self.config.host_peer.matches(custody.AuthenticatedCleanupActor.current().verify())
        self.config.runtime_peer.matches(_actor(self.config.runtime_peer).verify())
        validate_host(self.host, self.config, self.environment)

    def start(self):
        self.check_live()
        support = _directory(self.config.support_root)
        try:
            try:
                os.mkdir("authoring-scene", 0o700, dir_fd=support)
            except FileExistsError:
                pass
            self._root_fd = _directory(self.config.readiness_path.parent)
        finally:
            os.close(support)
        try:
            if self.config.socket_root is not None:
                raise FrameOwnerError("startup_invalid")
            if (
                len(os.fsencode(self.config.socket_path))
                > custody.DARWIN_UNIX_SOCKET_PATH_MAX_BYTES
            ):
                # The same private scene receiver, with a short kernel address.
                # Its record remains in authenticated selected support; peers
                # still verify the retained Host and exact full source binding.
                self._compact_root = custody._create_compact_socket_root()
                self.config = replace(self.config, socket_root=self._compact_root)
            self._socket_fd = _directory(self.config.socket_path.parent)
            self._listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._listener.bind(str(self.config.socket_path))
            self._owned["s"] = _inode(os.lstat(self.config.socket_path))
            os.chmod(self.config.socket_path, 0o600, follow_symlinks=False)
            self._listener.listen(1)
            self._listener.settimeout(0.1)
            fd = os.open(
                "ready.json",
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=self._root_fd,
            )
            try:
                self._owned["ready.json"] = _inode(os.fstat(fd))
                with os.fdopen(fd, "wb", closefd=False) as stream:
                    stream.write(wire.encoded(self.config.record) + b"\n")
                    stream.flush()
                    os.fsync(fd)
            finally:
                os.close(fd)
            self._endpoint = check_endpoint(self.config)
            self._thread = threading.Thread(
                target=self._serve, name="astrid-authoring-scene", daemon=True
            )
            self._thread.start()
            return self
        except BaseException:
            self.close()
            raise

    def is_ready(self):
        try:
            self.check_live()
            return check_endpoint(self.config) == self._endpoint
        except Exception:  # noqa: BLE001 - readiness always refuses on failed custody.
            return False

    def _handle(self, channel):
        peer = custody.AuthenticatedCleanupActor.private_peer(channel)
        self.config.runtime_peer.matches(peer.verify())
        end = time.monotonic() + 30.0
        request = read_frame(channel, end)
        raw = wire.validate_request(request, self.config.binding)

        def guard():
            self.check_live()
            if check_endpoint(self.config) != self._endpoint:
                raise FrameOwnerError("endpoint_changed")
            self.config.runtime_peer.matches(peer.verify())
            if time.monotonic() >= end:
                raise FrameOwnerError("timeout")
            if select.select([channel], [], [], 0)[0]:
                # Protocol is one request/reply. EOF or extra input revokes it.
                raise FrameOwnerError("caller_closed_or_cancelled")

        guard()
        # Root and every name are selected by the Host; no wire paths survive.
        with tempfile.TemporaryDirectory(
            prefix="scene-", dir=self.config.readiness_path.parent
        ) as temporary:
            root = Path(temporary)
            scratch = root / "private"
            scratch.mkdir(mode=0o700)
            scene = copy.deepcopy(request["scene"])
            for oid, data in raw.items():
                (scratch / oid[7:]).write_bytes(data)
            for entry in scene["assets"]["assets"].values():
                oid = next(
                    entry[k] for k in ("media_id", "object_id", "content_sha256") if k in entry
                )
                entry["local_path"] = str(scratch / oid[7:])
                # Only verified bytes staged by this Host supply the renderer's
                # display location/type. No caller file or URL crossed the wire.
                entry["file"] = entry["local_path"]
                entry["type"] = request["dependencies"][oid]["media_type"].split("/", 1)[0]
            session = self.host._authoring_scene_session(self.environment)
            generation = session.frame_owner.generation
            if generation != self.config.binding["owner_generation"]:
                raise FrameOwnerError("owner_changed")
            lease = session.lease(
                self.environment, attempt=root, scratch=scratch, guard=guard, deadline=end
            )
            try:
                from astrid.packs.rendering.actions.timeline_visualize.composed_frame import (
                    renderer_environment_identity,
                )

                from .remotion_evaluation import RemotionEvaluationClient

                client = RemotionEvaluationClient.for_authoring_lease(
                    lease,
                    closure=renderer_environment_identity,
                    generation=generation,
                    guard=guard,
                )
                answer = client.query_scene(
                    revision_digest=request["scene_digest"], scene=scene, frames=request["frames"]
                )
                guard()
                response = wire.reply(request, answer)
            finally:
                lease.close()
        # Release the lease and staged CAS scratch before success is visible.
        guard()
        channel.sendall(wire.encoded(response) + b"\n")

    def _serve(self):
        while not self._stop.is_set():
            try:
                channel, _ = self._listener.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            with channel:
                with self._lock:
                    self._active = channel
                try:
                    self._handle(channel)
                except Exception as exc:  # noqa: BLE001 - isolate an invalid private invocation.
                    # EOF is the only failure reply. Never emit a success shape
                    # or reflect unauthenticated exception/path/credential text.
                    import json
                    import sys
                    import traceback
                    try:
                        print(json.dumps({'event': 'authoring_scene_request_refused',
                            'exception_class': type(exc).__name__[:80],
                            'frames': [{'file': Path(f.filename).name[:80], 'function': f.name[:80], 'line': f.lineno}
                                       for f in traceback.extract_tb(exc.__traceback__)[-6:]]}),
                            file=sys.stderr, flush=True)
                    except Exception:
                        pass  # Optional diagnostics never replace the refusal.
                finally:
                    with self._lock:
                        self._active = None

    def _remove(self, name):
        fd = self._socket_fd if name == "s" else self._root_fd
        if fd is None or name not in self._owned:
            return
        try:
            if (
                _inode(os.stat(name, dir_fd=fd, follow_symlinks=False))
                == self._owned[name]
            ):
                os.unlink(name, dir_fd=fd)
        except FileNotFoundError:
            pass

    def close(self):
        self._stop.set()
        self._remove("ready.json")
        if self._listener is not None:
            self._listener.close()
        with self._lock:
            if self._active is not None:
                try:
                    self._active.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
        if self._thread is not None:
            self._thread.join(timeout=31)
            if self._thread.is_alive():
                raise FrameOwnerError("authoring_shutdown_unresolved")
        self._remove("s")
        if self._socket_fd is not None:
            if self._compact_root is not None:
                if _inode(os.lstat(self._compact_root)) != _inode(os.fstat(self._socket_fd)):
                    raise FrameOwnerError("endpoint_changed")
                self._compact_root.rmdir()
                self._compact_root = None
            os.close(self._socket_fd)
            self._socket_fd = None
        if self._root_fd is not None:
            os.close(self._root_fd)
            self._root_fd = None
