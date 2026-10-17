"""One review listener retained by its existing authenticated child launch."""
from __future__ import annotations

import ctypes
import hashlib
import os
import socket
import sys
import threading
from pathlib import Path

from .process_group import process_birth_identity


class _FileInfo(ctypes.Structure):
    _fields_ = [("openflags", ctypes.c_uint32), ("status", ctypes.c_uint32),
                ("offset", ctypes.c_int64), ("kind", ctypes.c_int32), ("guards", ctypes.c_uint32)]


class _VInfoStat(ctypes.Structure):
    _fields_ = ([("dev", ctypes.c_uint32), ("mode", ctypes.c_uint16), ("nlink", ctypes.c_uint16),
                 ("ino", ctypes.c_uint64), ("uid", ctypes.c_uint32), ("gid", ctypes.c_uint32)]
                + [(name, ctypes.c_int64) for name in ("atime", "atimensec", "mtime", "mtimensec",
                    "ctime", "ctimensec", "birthtime", "birthtimensec", "size", "blocks")]
                + [("blksize", ctypes.c_int32), ("flags", ctypes.c_uint32),
                   ("gen", ctypes.c_uint32), ("rdev", ctypes.c_uint32), ("spare", ctypes.c_int64 * 2)])


class _SocketInfoPrefix(ctypes.Structure):
    # sys/proc_info.h: socket_fdinfo through socket_info.soi_state. The
    # oversized destination retains the complete native record; opaque kernel
    # handles are never exposed as metadata or authority.
    _fields_ = [("file", _FileInfo), ("stat", _VInfoStat),
                ("socket_handle", ctypes.c_uint64), ("pcb", ctypes.c_uint64),
                ("kind", ctypes.c_int), ("protocol", ctypes.c_int), ("family", ctypes.c_int),
                ("options", ctypes.c_short), ("linger", ctypes.c_short), ("state", ctypes.c_short)]


def _native_socket_info(channel):
    # Darwin advertises SO_ACCEPTCONN but getsockopt returns ENOPROTOOPT.
    # Inspect this process's exact descriptor through the documented libproc ABI.
    library = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
    library.proc_pidfdinfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                      ctypes.c_void_p, ctypes.c_int]
    library.proc_pidfdinfo.restype = ctypes.c_int
    buffer = ctypes.create_string_buffer(2048)
    used = library.proc_pidfdinfo(os.getpid(), channel.fileno(), 3, buffer, len(buffer))
    if not ctypes.sizeof(_SocketInfoPrefix) <= used < len(buffer):
        raise ValueError("review listener native state is unavailable")
    native = _SocketInfoPrefix.from_buffer(buffer)
    return native


def _is_listening(channel):
    if sys.platform != "darwin":
        return channel.getsockopt(socket.SOL_SOCKET, socket.SO_ACCEPTCONN) == 1
    native = _native_socket_info(channel)
    return (native.kind == socket.SOCK_STREAM and native.family == socket.AF_INET
            and bool(native.options & socket.SO_ACCEPTCONN) and not native.state & 0x2030)

def listener_identity(channel):
    info = os.fstat(channel.fileno())
    address = channel.getsockname()
    if (channel.family != socket.AF_INET
            or channel.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE) != socket.SOCK_STREAM
            or not _is_listening(channel)
            or type(address) is not tuple or len(address) != 2
            or address[0] != "127.0.0.1" or not 1 <= address[1] <= 65535):
        raise ValueError("review listener is not the retained loopback server")
    native = _native_socket_info(channel) if sys.platform == "darwin" else None
    incarnation = (native.socket_handle, native.pcb) if native is not None else (info.st_dev, info.st_ino)
    if not any(incarnation):
        raise ValueError("review listener native identity is unavailable")
    digest = hashlib.sha256(str(incarnation).encode("ascii")).hexdigest()
    return {"device": info.st_dev, "inode": info.st_ino, "host": address[0], "port": address[1],
            "socket_digest": digest}


class _RetainedReviewListener:
    """Resource of a ChildBridge launch, never an independent authority."""

    def __init__(self, launch, policy, record, port):
        from ._child_pipe import _ChildBridgeLaunchBinding
        from .generic_host import _AuthenticatedAttempt, _ConfinementPolicy
        if type(launch) is not _ChildBridgeLaunchBinding or type(policy) is not _ConfinementPolicy:
            raise ValueError("review listener requires the existing typed launch")
        launch.verify()
        authority = getattr(launch.bridge.host, "_attempt_claim_authority", None)
        if (type(authority) is not _AuthenticatedAttempt or type(port) is not int or not 0 <= port <= 65535
                or record is None or record.id != "editorial.human_review"
                or launch.claim.get("operation") != record.id
                or policy.claim_binding != tuple(sorted(launch.claim.items()))
                or policy.private_write_root != launch.bridge.output_root
                or policy.attempt_root != launch.bridge.output_root.parent
                or policy.network.outbound_tcp or policy.network.broker is not None
                or policy.renderer_transport is not None or policy.renderer_reads is not None):
            raise ValueError("review listener requires its admitted operation and attempt")
        self.launch, self.policy, self.record = launch, policy, record
        self.owner_pid, self.owner_birth = os.getpid(), process_birth_identity()
        self.authority = authority
        self.claim = dict(launch.claim)
        self.source_digest, self.capability_digest = record.source_digest, record.capability_digest
        self.consumed = self.closed = False
        self._lock = threading.RLock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind(("127.0.0.1", port))
            self.socket.listen(128)
            self.identity = listener_identity(self.socket)
        except BaseException:
            self.socket.close()
            raise

    def validate(self, policy):
        if os.getpid() != self.owner_pid:
            raise ValueError("review listener creator changed")
        with self._lock:
            return self._validate(policy)

    def _validate(self, policy):
        from .generic_host import _admitted_source_roots, _verify_admitted_source

        bridge = self.launch.bridge
        authority = getattr(bridge.host, "_attempt_claim_authority", None)
        if (self.closed or os.getpid() != self.owner_pid or process_birth_identity() != self.owner_birth
                or bridge._launch_binding is not self.launch or self.launch.review_listener is not self
                or authority is not self.authority or dict(authority.fields) != self.claim
                or policy.attempt_root != self.policy.attempt_root
                or policy.private_write_root != self.policy.private_write_root
                or policy.claim_binding != self.policy.claim_binding
                or policy.network != self.policy.network
                or policy.renderer_transport is not None or policy.renderer_reads is not None
                or bridge.host.capabilities.get(self.record.id) is not self.record
                or self.record.source_digest != self.source_digest
                or self.record.capability_digest != self.capability_digest
                or listener_identity(self.socket) != self.identity):
            raise ValueError("review listener owner, source, claim, attempt or socket changed")
        bridge._live()
        _verify_admitted_source({"source_digest": self.source_digest,
            "source_roots": [str(root) for root in _admitted_source_roots(self.record.source_root, self.record.definition)]})
        return self.identity["port"]

    def endpoint(self):
        # Cleanup may follow revocation. This observes the retained resource,
        # never renews the cancelled claim or mints publication authority.
        if os.getpid() != self.owner_pid:
            raise ValueError("review listener creator changed")
        with self._lock:
            if self.closed or listener_identity(self.socket) != self.identity:
                raise ValueError("review listener endpoint changed")
            return self.identity["port"]

    def metadata(self):
        if os.getpid() != self.owner_pid:
            raise ValueError("review listener creator changed")
        with self._lock:
            self.validate(self.policy)
            return {"fd": 0, **self.identity, "attempt": str(self.policy.attempt_root),
                    "capability_id": self.record.id, "capability_digest": self.capability_digest,
                    "source_digest": self.source_digest}

    def consume(self):
        if os.getpid() != self.owner_pid:
            raise ValueError("review listener creator changed")
        with self._lock:
            self.validate(self.policy)
            if self.consumed:
                raise ValueError("review listener launch cannot be replayed")
            self.consumed = True
            return self.socket

    def close(self):
        with self._lock:
            self.socket.close()
            self.closed = True


class _InheritedReviewListener:
    def __init__(self, channel, metadata):
        self.socket, self.metadata = channel, dict(metadata)
        self.owner_pid = os.getpid()
        self.consumed = False
        expected = {key: metadata[key] for key in ("device", "inode", "host", "port", "socket_digest")}
        if listener_identity(channel) != expected:
            channel.close()
            raise ValueError("review listener differs from authenticated launch")

    def consume(self, out_path):
        expected = {key: self.metadata[key] for key in ("device", "inode", "host", "port", "socket_digest")}
        if (self.consumed or os.getpid() != self.owner_pid
                or Path(out_path).parent != Path(self.metadata["attempt"]) / "outputs"
                or listener_identity(self.socket) != expected):
            raise ValueError("review listener consumer, attempt or socket changed")
        self.consumed = True
        return self.socket

    def close(self):
        self.socket.close()
